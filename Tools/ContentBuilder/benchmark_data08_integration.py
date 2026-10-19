"""Actual local repository SQL/transactions. Not iPhone launch, Swift, or UI timing."""
import argparse
import json
import math
import platform
import socket
import sqlite3
import statistics
import tempfile
import time
import uuid
from pathlib import Path
from unittest.mock import patch
from build_content import ROOT
from test_data05_content import query, queries
from test_data08_integration import vocabulary_sql
from test_lookup_sql import user


def measure(action, repetitions=30):
    times=[];result=None
    for _ in range(repetitions):
        start=time.perf_counter();result=action();times.append((time.perf_counter()-start)*1000)
    return dict(median_ms=round(statistics.median(times),4),p95_ms=round(sorted(times)[math.ceil(.95*len(times))-1],4),max_ms=round(max(times),4),result_rows=len(result) if isinstance(result,list)else result)


def run(bundle):
    with tempfile.TemporaryDirectory()as tmp,patch.object(socket,'socket',side_effect=AssertionError('network unavailable in portable benchmark')):
        db=sqlite3.connect(bundle.resolve().as_uri()+'?mode=ro',uri=True);d=user(Path(tmp)/'user.sqlite',10)
        ids=[r[0]for r in db.execute('SELECT id FROM vocabulary ORDER BY sort_key,id')]
        for wid in ids:
            d.execute("INSERT INTO srs_state VALUES(?,'vocabulary','calendar_steps',1,'{\"stage\":1}',100,50,50)",[wid])
        d.commit()
        base,clause=vocabulary_sql();metrics={}
        def home_refresh():
            result=[]
            for level in ('intro','beginner'):
                result+=list(db.execute(query('SQLiteVocabularyContent','SELECT COUNT(*) AS count'),[level]))
                result+=list(d.execute(query('SQLiteVocabularyProgress','SELECT s.set_id'),[level]))
            result+=list(d.execute(query('SQLiteListening','SELECT COUNT(*) AS n FROM srs_state'),['calendar_steps',1,100]))
            result+=list(d.execute(query('SQLiteListening','SELECT content_id FROM srs_state WHERE skill='),['calendar_steps',1,100]))
            result+=list(d.execute(query('SQLiteListening','SELECT state_json FROM listening_sessions WHERE scope='),['review']))
            for repo,skill in [('SQLiteGrammarProgress','grammar'),('SQLiteReviewProgress','vocabulary')]:
                result+=list(d.execute(query(repo,'SELECT COUNT(*) AS n FROM srs_state'),['calendar_steps',1,100]))
                overdue=next(q for q in queries(repo)if q.startswith('SELECT COUNT(*) AS n FROM srs_state')and 'due_at<?'in q)
                result+=list(d.execute(overdue,['calendar_steps',1,0]))
                result+=list(d.execute(query(repo,'SELECT COUNT(*) AS n FROM review_items'),[0,86400]))
                result+=list(d.execute(query(repo,'SELECT 1 FROM review_sessions WHERE skill=')))
            result+=list(d.execute(query('SQLiteProgressRepository','SELECT p.lesson_id')))
            result+=list(d.execute(query('SQLiteCurriculum','SELECT kind,target,level FROM')))
            return result
        metrics['home_refresh_summary_and_resume_sql']=measure(home_refresh)
        def home():
            result=list(d.execute(query('SQLiteProgressRepository','SELECT COALESCE(SUM'),[100]))
            result+=list(d.execute(query('SQLiteCurriculum','SELECT kind,target,level FROM')))
            for kind in ('vocabulary','grammar','listening','lesson'):
                result+=list(db.execute(query('SQLiteCurriculum','SELECT id FROM content_items'),['lower_intermediate',kind,'',kind]))
            return result
        metrics['home_summary_resume_first_curriculum_pages']=measure(home)
        for label,term in [('ko_search','교류하다'),('ja_search','交流'),('broad_search','る'),('no_match','__no_content__')]:
            metrics[label]=measure(lambda term=term:list(db.execute(query('SQLiteLookup','WITH terms'),[term]*3+[0])))
        def review():
            due=list(d.execute(query('SQLiteReviewProgress','SELECT content_id FROM srs_state WHERE'),['calendar_steps',1,100,20]))
            for (wid,)in due:db.execute(query('SQLiteVocabularyContent','SELECT v.headword'),[wid]).fetchall()
            return due
        metrics['srs_due20_and_card_headers']=measure(review)
        metrics['vocabulary_first20']=measure(lambda:list(db.execute(base+clause(' AND i.level=')+clause(' ORDER BY'),['lower_intermediate',20])))
        course=db.execute("SELECT id FROM courses WHERE ordinal=4").fetchone()
        if course:
            lesson=db.execute('SELECT id FROM lessons WHERE course_id=? ORDER BY ordinal LIMIT 1',[course[0]]).fetchone()[0]
            metrics['authored_lesson20_query']=measure(lambda:list(db.execute(query('SQLiteContentRepository','SELECT i.id,i.kind'),[lesson])))
        set_ids=[r[0]for r in db.execute("SELECT v.id FROM vocabulary v JOIN content_items i ON i.id=v.id WHERE i.level='lower_intermediate' ORDER BY sort_key,v.id")]
        counter=0
        def create():
            nonlocal counter
            counter+=1;sid=str(uuid.uuid4());session=str(uuid.uuid4());start=(counter-1)*20;selected=set_ids[start:start+20]
            with d:
                d.execute(query('SQLiteVocabularyProgress','INSERT INTO vocabulary_sets('),[sid,'lower_intermediate',counter,100])
                for n,wid in enumerate(selected):d.execute(query('SQLiteVocabularyProgress','INSERT INTO vocabulary_set_items('),[sid,wid,n])
                # SQL persistence cost only: native engine makes/validates the real snapshot.
                payload=json.dumps(dict(vocabularyIDs=selected,order=selected,position=0,revision=0,contentVersionAtStart=19))
                d.execute(query('SQLiteVocabularyProgress','INSERT INTO vocabulary_sessions('),[session,sid,payload,0,100])
            return len(selected)
        metrics['set20_membership_and_session_commit_sql']=measure(create)
        self_counts=dict(vocabulary=len(ids),listening=db.execute('SELECT COUNT(*) FROM listening_items').fetchone()[0],questions=db.execute('SELECT COUNT(*) FROM questions').fetchone()[0],srs_rows=d.execute('SELECT COUNT(*) FROM srs_state').fetchone()[0])
        d.close();db.close()
        return dict(bundle_bytes=bundle.stat().st_size,counts=self_counts,queries=metrics)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--bundle',type=Path,default=ROOT/'Resources/content.sqlite');p.add_argument('--report',type=Path,required=True);args=p.parse_args()
    report=dict(environment=dict(platform=platform.platform(),python=platform.python_version(),sqlite=sqlite3.sqlite_version),repetitions=30,scope='Warm SQLite connections, actual Swift repository SQL; separate disk progress DB, socket creation forbidden in this Python process. No Swift/iPhone/UI/TTS or actual 3–10 minute timing. Session benchmark measures SQL writes, not engine execution.',before=run(ROOT/'Tests/Fixtures/content-v18-production.sqlite'),after=run(args.bundle))
    args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
