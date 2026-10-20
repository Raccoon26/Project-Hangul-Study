"""DATA09 warm actual repository SQL benchmark; no Swift/device/memory certification."""
import argparse
import json
import platform
import socket
import sqlite3
import tempfile
import uuid
from pathlib import Path
from unittest.mock import patch
from build_content import ROOT
from benchmark_data08_integration import run,measure
from test_data05_content import query
from test_lookup_sql import user


def grammar_profile(bundle):
    with tempfile.TemporaryDirectory() as folder,patch.object(socket,'socket',side_effect=AssertionError('offline')):
        c=sqlite3.connect(bundle);d=user(Path(folder)/'user.sqlite',10)
        manifest=json.loads((ROOT/'Content/data09-integration-ids.json').read_text());ids=[r['grammar_id'] for r in manifest['related_vocabulary']]
        gid=ids[0]
        if not c.execute('select 1 from grammar where id=?',[gid]).fetchone():return dict(status='N/A: DATA09 cohort not in Content19')
        def card():
            rows=list(c.execute(query('SQLiteGrammarContent','SELECT g.*,i.revision'),[gid]))
            rows+=list(c.execute(query('SQLiteGrammarContent','SELECT e.id,e.korean'),[gid]))
            comparisons=c.execute(query('SQLiteGrammarContent','SELECT g.id,g.pattern,g.meaning_ja,g.confusion_ja'),[gid]).fetchall();rows+=comparisons
            for r in comparisons:rows+=list(c.execute(query('SQLiteGrammarContent','SELECT e.id,e.korean'),[r[0]]))
            questions=c.execute(query('SQLiteGrammarContent','SELECT q.*,i.revision'),[gid]).fetchall();rows+=questions
            for r in questions:rows+=list(c.execute(query('SQLiteGrammarContent','SELECT choice_id,text'),[r[0]]))
            rows+=list(c.execute(query('SQLiteGrammarContent','SELECT g.id,g.pattern,g.meaning_ja,g.form_ko'),[gid]))
            related=c.execute(query('SQLiteLookup','WITH related'),[gid]*5).fetchall();rows+=related
            for i,kind in related:rows+=list(c.execute(query('SQLiteLookup','SELECT i.level'),[i,kind]))
            return rows
        for i in ids:d.execute("insert into srs_state values(?,'grammar','calendar_steps',1,'{\"stage\":1}',100,0,0)",[i])
        d.commit()
        def due():
            rows=d.execute(query('SQLiteGrammarProgress','SELECT content_id FROM srs_state WHERE'),['calendar_steps',1,100]).fetchall()
            for (i,) in rows:c.execute(query('SQLiteGrammarContent','SELECT g.*,i.revision'),[i]).fetchall()
            return rows
        lid=manifest['units'][0]['lesson_ids'][0];members=[r[0] for r in c.execute(query('SQLiteGrammarContent','SELECT g.id FROM lesson_items'),[lid])]
        def persist():
            # SQL persistence cost only; real Swift snapshots/engine are separate native tests.
            payload=json.dumps(dict(ids=members,order=members,position=0,revision=0,contentVersion=24))
            with d:
                d.execute(query('SQLiteGrammarProgress','INSERT INTO grammar_sessions('),[str(uuid.uuid4()),str(uuid.uuid4()),payload,100])
            return len(members)
        result=dict(grammar_catalog=measure(lambda:list(c.execute(query('SQLiteGrammarContent','SELECT l.id,l.title_ja'),['lower_intermediate',-1,30]))),full_card_with_examples_quiz_comparisons_prerequisites_related=measure(card),grammar_srs_due20_headers=measure(due),grammar_session3_commit_sql=measure(persist))
        d.close();c.close();return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--bundle',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    result=dict(environment=dict(platform=platform.platform(),python=platform.python_version(),sqlite=sqlite3.sqlite_version),scope='Warm connections;30 repetitions;actual extracted Swift repository SQL, separate user10 SQLite, Python socket forbidden. No iPhone launch/UI/frame timing/VoiceOver/RAM or 3–10-minute measurement.',versions={})
    for version,path in [(19,ROOT/'Tests/Fixtures/content-v19-production.sqlite'),(23,ROOT/'Tests/Fixtures/content-v23-production.sqlite'),(24,a.bundle)]:
        result['versions'][str(version)]=dict(core=run(path),grammar=grammar_profile(path))
    a.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(dict(report=str(a.report),versions=list(result['versions']))))
