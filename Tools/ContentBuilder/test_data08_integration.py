"""Exact DATA08 Content18→19 release gate, pinned to immutable19.
Current20 and preservation of all19 payloads are tested by test_data09_a_content.
Uses current repository SQL, not Swift or device execution.
"""
import collections
import gzip
import hashlib
import json
import os
import re
import shutil
import socket
import sqlite3
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch
from audit_data08_final import audit, cohorts
from build_content import ROOT, build
from test_data05_content import query, queries
from test_lookup_sql import user
from validator import signatures, ValidationError

BUNDLE = Path(os.environ.get('DATA08_CANDIDATE', ROOT/'Tests/Fixtures/content-v19-production.sqlite'))


def vocabulary_sql():
    code = (ROOT/'Repositories/SQLiteContentRepository.swift').read_text()
    base = re.findall(r'"""(.*?)"""', code, re.S)[0]
    parts = re.findall(r'sql \+= "([^"]+)"', code)
    return base, lambda prefix: next(s for s in parts if s.startswith(prefix))


class Data08IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.released_source = tempfile.TemporaryDirectory()
        cls.source_path = Path(cls.released_source.name)/'content19.json'
        cls.source_path.write_bytes(gzip.decompress((ROOT/'Tests/Fixtures/content-v19-production.json.gz').read_bytes()))
        cls.source = json.loads(cls.source_path.read_text())
        cls.previous = ROOT/'Tests/Fixtures/content-v18-production.sqlite'
        cls.before_bytes = gzip.decompress((ROOT/'Tests/Fixtures/content-v18-production.json.gz').read_bytes())
        cls.before = json.loads(cls.before_bytes)
        cls.manifest = json.loads((ROOT/'Content/data08-integration-ids.json').read_text())
        cls.approved = set(json.loads((ROOT/'Content/data08-integration-revised-ids.json').read_text()))
        cls.words = [w for c in cohorts().values() for w in c['vocabulary']]
        cls.word_ids = {w['id'] for w in cls.words}
        cls.example_ids = {e for w in cls.words for e in w['example_ids']}
        cls.db = sqlite3.connect(BUNDLE.resolve().as_uri()+'?mode=ro', uri=True)
        cls.old = sqlite3.connect(cls.previous.as_uri()+'?mode=ro', uri=True)

    @classmethod
    def tearDownClass(cls):
        cls.db.close(); cls.old.close(); cls.released_source.cleanup()

    def test_strict_import_and_complete_source_bundle_integrity(self):
        report = audit(self.source, BUNDLE)
        self.assertEqual(report['validation']['error_count'], 0)
        self.assertEqual(report['source_rows_scanned'], sum(map(len, self.source['tables'].values())))
        self.assertEqual(report['scope']['vocabulary'], 911)
        self.assertEqual(report['scope']['unique_examples'], 1821)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)/'rebuilt.sqlite'
            result = build(self.source_path, out, self.previous, production=True)
            self.assertEqual(result['validation']['error_count'], 0)
            self.assertEqual(result['validation']['warning_count'], 10)
            with sqlite3.connect(out) as rebuilt:
                for (table,) in self.db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
                    self.assertEqual(set(rebuilt.execute('SELECT * FROM '+table)), set(self.db.execute('SELECT * FROM '+table)), table)
        self.assertEqual(self.db.execute('PRAGMA integrity_check').fetchall(), [('ok',)])
        self.assertEqual(self.db.execute('PRAGMA foreign_key_check').fetchall(), [])
        self.assertEqual(self.db.execute('SELECT schema_version,content_version,min_reader_version,is_fixture FROM content_metadata').fetchone(), (4,19,7,0))

    def test_exact_immutable_release18_and_all_old_rows_preserved(self):
        self.assertEqual(hashlib.sha256(self.previous.read_bytes()).hexdigest(), '3235c21699bb297a4447f0ce2068a2e949db136a2c4e08ca70d7a737a07308e3')
        before, after = signatures(self.old), signatures(self.db)
        self.assertEqual(set(after)-set(before), set(self.manifest['new_ids']))
        self.assertEqual({i for i in before if before[i] != after[i]}, self.approved)
        grammar_id = self.db.execute("SELECT id FROM grammar WHERE pattern='-고'").fetchone()[0]
        self.assertEqual(self.approved, self.word_ids | self.example_ids | {grammar_id})
        self.assertEqual(len(self.approved),2733)
        for table, old in self.before['tables'].items():
            current = self.source['tables'][table][:len(old)]
            if table == 'content_items':
                expected = [dict(r,revision=r['revision']+1,updated_at='2026-10-19T13:29:13Z') if r['id'] in self.approved else r for r in old]
                self.assertEqual(current, expected)
            else:
                self.assertEqual(current, old, table)
        self.assertEqual(len(self.manifest['new_ids']),4855)
        self.assertEqual(len(set(self.manifest['new_ids'])),4855)
        for item_id in self.manifest['new_ids']:
            self.assertEqual(str(uuid.UUID(item_id)),item_id)
            self.assertEqual(self.db.execute('SELECT level,is_active,revision FROM content_items WHERE id=?',[item_id]).fetchone(),('lower_intermediate',1,1))

    def test_real_course_unit_lesson_placement_all_911_once(self):
        course = self.manifest['course_id']
        self.assertIn(course, [r[0]for r in self.db.execute(query('SQLiteContentRepository','SELECT c.*'))])
        seen = []
        actual_lessons = self.db.execute(query('SQLiteContentRepository','SELECT l.id,l.title_ja'),[course]).fetchall()
        self.assertEqual(len(actual_lessons),47)
        for unit, batch_count, lesson_count in zip(self.manifest['units'],(301,300,310),(16,15,16)):
            self.assertEqual(len(unit['lessons']),lesson_count)
            unit_seen=[]
            for lesson in unit['lessons']:
                lid=lesson['id']
                self.assertIn((lid,unit['tag_id']),self.db.execute('SELECT content_id,tag_id FROM item_tags WHERE content_id=?',[lid]).fetchall())
                rows=self.db.execute(query('SQLiteContentRepository','SELECT i.id,i.kind'),[lid]).fetchall()
                ids=[r[0]for r in rows]
                self.assertEqual(ids,lesson['vocabulary_ids']); self.assertLessEqual(len(ids),20)
                self.assertTrue(all(r[1]=='vocabulary' for r in rows))
                for wid in ids:
                    self.assertIsNotNone(self.db.execute(query('SQLiteVocabularyContent','SELECT v.headword'),[wid]).fetchone())
                unit_seen+=ids
            self.assertEqual(len(unit_seen),batch_count);seen+=unit_seen
        self.assertEqual(set(seen),self.word_ids);self.assertEqual(len(seen),911)
        # The actual generic lesson runner must use the existing card reader, not unsupported kinds.
        code=(ROOT/'Repositories/SQLiteContentRepository.swift').read_text()
        self.assertIn('case "vocabulary":',code);self.assertIn('try readVocabularyCard(id: id)',code)
        self.assertIn('step.skill = "vocabulary_preview"',code)

    def test_set_allocator_order_and_old_membership_preserved_all_new_words_reachable(self):
        base, clause = vocabulary_sql()
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'user.sqlite';d=user(path,10)
            # Simulate an existing lower-intermediate user's first 20-word set.
            original=[r[0]for r in self.old.execute(base+clause(' AND i.level=')+clause(' ORDER BY'),['lower_intermediate',20])]
            sets=[];after=None;allocated=[]
            for number in range(1,61):
                ids=[];cursor=None
                while len(ids)<20:
                    sql=base+clause(' AND i.level=');args=['lower_intermediate']
                    if cursor:sql+=clause(' AND (v.sort_key>');args+=list(cursor)
                    page=self.db.execute(sql+clause(' ORDER BY'),args+[100]).fetchall()
                    if not page:break
                    pageids=[r[0]for r in page]
                    assigned={r[0]for r in d.execute('SELECT content_id FROM vocabulary_set_items WHERE content_id IN ('+','.join('?'for _ in pageids)+')',pageids)}
                    ids += [i for i in pageids if i not in assigned][:20-len(ids)]
                    cursor=(page[-1][3],page[-1][3],page[-1][0])
                    if len(page)<100:break
                if not ids:break
                sid=str(uuid.uuid4())
                with d:
                    d.execute(query('SQLiteVocabularyProgress','INSERT INTO vocabulary_sets('),[sid,'lower_intermediate',number,100])
                    for n,wid in enumerate(ids):d.execute(query('SQLiteVocabularyProgress','INSERT INTO vocabulary_set_items('),[sid,wid,n])
                sets.append(ids);allocated+=ids
            self.assertEqual(sets[0],original);self.assertEqual((len(sets),len(sets[-1])),(60,1))
            self.assertEqual(len(allocated),1181);self.assertEqual(len(set(allocated)),1181)
            self.assertTrue(self.word_ids <= set(allocated))
            old_id=next(iter(self.word_ids))
            d.execute("INSERT INTO srs_state VALUES(?,'vocabulary','calendar_steps',1,'{\"stage\":4}',900,100,100)",[old_id])
            enroll=query('SQLiteReviewProgress','INSERT INTO srs_state(')
            for _ in range(2):
                for wid in self.word_ids:d.execute(enroll,[wid,'calendar_steps',1,'{"stage":0}',300,100])
            self.assertEqual(d.execute('SELECT COUNT(*) FROM srs_state').fetchone()[0],911)
            self.assertEqual(d.execute('SELECT state_json,due_at FROM srs_state WHERE content_id=?',[old_id]).fetchone(),('{"stage":4}',900))
            d.commit()
            # Global UNIQUE prevents duplicate allocation, with no partial set left after rollback.
            with self.assertRaises(sqlite3.IntegrityError),d:
                d.execute(query('SQLiteVocabularyProgress','INSERT INTO vocabulary_sets('),['bad','lower_intermediate',61,100])
                d.execute(query('SQLiteVocabularyProgress','INSERT INTO vocabulary_set_items('),['bad',allocated[0],0])
            self.assertIsNone(d.execute("SELECT id FROM vocabulary_sets WHERE id='bad'").fetchone());d.close()

    def test_all_1821_listening_dictations_reuse_reviewed_text_and_paginate(self):
        expected={x['id']:x for x in self.manifest['listening']}
        self.assertEqual(len(expected),1821);seen={};after=-1;pages=0
        while True:
            batches=self.db.execute(query('SQLiteListening','SELECT l.learning_order/20'),['lower_intermediate',after]).fetchall()
            if not batches:break
            pages+=1;self.assertLessEqual(len(batches),30)
            for batch,count in batches:
                ids=[r[0]for r in self.db.execute(query('SQLiteListening','SELECT l.id FROM listening_items'),['lower_intermediate',batch*20,(batch+1)*20])]
                self.assertEqual(len(ids),count);self.assertLessEqual(count,20)
                self.db.row_factory=sqlite3.Row
                rows=self.db.execute(query('SQLiteListening','SELECT q.*,l.id')+' AND l.id IN ('+','.join('?'for _ in ids)+') ORDER BY l.learning_order,l.id LIMIT 20',ids).fetchall()
                self.db.row_factory=None
                self.assertEqual(len(rows),count)
                for row in rows:
                    if row['item_id'] not in expected:continue
                    m=expected[row['item_id']];seen[m['id']]=m
                    self.assertEqual(row['source_example_id'],m['example_id'])
                    self.assertEqual(json.loads(row['answer_json']),{'accepted':[row['korean']]})
                    self.assertEqual(json.loads(row['rubric_json']),{'listening_task':'dictation'})
                    self.assertIsNone(row['prompt_ko']);self.assertEqual(row['audio_mode'],'tts')
                    self.assertEqual(self.old.execute('SELECT korean,japanese FROM examples WHERE id=?',[m['example_id']]).fetchone(),(row['korean'],row['japanese']))
            after=batches[-1][0]
        self.assertEqual(seen,expected);self.assertEqual(pages,4)
        self.assertEqual({v['example_id']for v in seen.values()},self.example_ids)
        self.assertIn('.lowerIntermediate', (ROOT/'Views/ListeningView.swift').read_text().split('ForEach(')[1].split(')')[0])

    def test_all_predicates_connective_and_sentence_input_through_existing_queries(self):
        pred={w['id']for w in self.words if w['part_of_speech']in ('verb','adjective')}
        self.assertEqual({p['vocabulary_id']for p in self.manifest['production']},pred);self.assertEqual(len(pred),581)
        actual=set();after=''
        while True:
            page=self.db.execute(query('SQLiteCurriculum','SELECT DISTINCT v.id,v.headword'),['lower_intermediate',after]).fetchall()
            if not page:break
            actual.update(i for i,_ in page);after=page[-1][0]
        self.assertTrue(pred<=actual)
        self.db.row_factory=sqlite3.Row
        try:
            for record in self.manifest['production']:
                rows={r['id']:r for r in self.db.execute(query('SQLiteProduction','SELECT q.*'),[record['vocabulary_id']])}
                form=rows[record['form_question_id']];sentence=rows[record['sentence_question_id']]
                self.assertEqual(json.loads(form['answer_json']),{'accepted':[form['headword'][:-1]+'고']})
                self.assertEqual(json.loads(form['rubric_json'])['form'],'connective')
                self.assertEqual(json.loads(sentence['rubric_json'])['mode'],'sentence')
                ko,ja=self.old.execute('SELECT korean,japanese FROM examples WHERE id=?',[record['example_id']]).fetchone()
                self.assertEqual(json.loads(sentence['answer_json']),{'accepted':[ko]})
                self.assertIn(ja,sentence['prompt_ja']);self.assertIsNone(sentence['prompt_ko'])
                self.assertIsNotNone(self.db.execute("SELECT g.id FROM content_links l JOIN grammar g ON g.id=l.target_id WHERE l.source_id=? AND l.relation='prerequisite'",[form['id']]).fetchone())
        finally:self.db.row_factory=None
        # Expressions/nouns/adverbs remain vocabulary/dictionary/listening content, not conjugatable predicates.
        self.assertEqual(len(self.word_ids-pred),330)
        self.assertIn('let production = try await curriculumProduction(level:.intro,after:"")', (ROOT/'Repositories/SQLiteCurriculum.swift').read_text())

    def test_all_search_dictionary_cards_and_46_existing_grammar_references(self):
        sql=query('SQLiteLookup','WITH terms')
        for word in self.words:
            wid=word['id'];head=self.db.execute('SELECT headword FROM vocabulary WHERE id=?',[wid]).fetchone()[0]
            found=set();offset=0
            while True:
                page=self.db.execute(sql,[head]*3+[offset]).fetchall();found.update(page)
                if len(page)<30:break
                offset+=30
            self.assertIn((wid,'vocabulary'),found,head)
            self.assertIsNotNone(self.db.execute(query('SQLiteLookup','SELECT i.level'),[wid,'vocabulary']).fetchone())
            self.assertEqual(len(self.db.execute(query('SQLiteContentRepository','SELECT DISTINCT e.id'),[wid]).fetchall()),2)
        n=0
        for reg in cohorts().values():
            for ref in reg['grammar_links']:
                visible=self.db.execute(query('SQLiteGrammarContent','SELECT e.id'),[ref['grammar_id']]).fetchall()
                self.assertIn(ref['example_id'],[r[0]for r in visible]);n+=1
        self.assertEqual(n,46)

    def test_upgrade_keeps_progress_favorites_difficult_statistics_metadata_and_active_modules(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);progress=root/'user.sqlite';content=root/'content.sqlite';shutil.copyfile(self.previous,content)
            d=user(progress,10);ids=[w['id']for w in self.words[:20]];wid=ids[0]
            d.execute(query('SQLiteVocabularyProgress','INSERT INTO vocabulary_sets('),['set','lower_intermediate',1,100])
            for n,i in enumerate(ids):
                d.execute(query('SQLiteVocabularyProgress','INSERT INTO vocabulary_set_items('),['set',i,n])
                d.execute("INSERT INTO srs_state VALUES(?,'vocabulary','calendar_steps',1,?,300,200,200)",[i,json.dumps(dict(stage=1,failureCount=2,consecutiveSuccesses=0,lastResult='difficult'))])
            snapshot=json.dumps(dict(vocabularyIDs=ids,order=ids[::-1],position=4,round=2,revision=9,contentVersionAtStart=18))
            d.execute(query('SQLiteVocabularyProgress','INSERT INTO vocabulary_sessions('),['v','set',snapshot,9,100])
            d.execute("INSERT INTO grammar_sessions VALUES('g','old-grammar-lesson',?,4,'active',110)",[json.dumps(dict(position=2,revision=4,contentVersion=18))])
            d.execute(query('SQLiteProduction','INSERT INTO production_sessions'),['p',wid,json.dumps(dict(position=1,retry=[0],revision=3,updatedAt=120-978307200,contentVersion=18)),0])
            d.execute(query('SQLiteListening','INSERT INTO listening_sessions'),['l','practice:lower_intermediate:10',json.dumps(dict(position=1,heard=True,revision=3,updatedAt=130-978307200,contentVersion=18)),0])
            d.execute("INSERT INTO review_sessions VALUES('r','vocabulary','active',90,140,NULL)")
            d.execute("INSERT INTO review_items(session_id,content_id,ordinal) VALUES('r',?,0)",[wid])
            d.execute("INSERT INTO lesson_sessions VALUES('h','legacy-lesson',18,1,'[]','char','active',90,150,NULL)")
            d.execute(query('SQLiteProgressRepository','INSERT INTO lesson_progress('),['legacy-lesson',100,'char'])
            d.execute("UPDATE lesson_progress SET completed_count=2")
            d.execute(query('SQLiteSavedContent','INSERT INTO favorites'),[wid,100,'vocabulary'])
            for key,value in [('integration.opaque-metadata.v1',{'example':5}),('curriculum.profile.v1',{'version':1,'level':'lower_intermediate','skippedHangul':True})]:d.execute('INSERT INTO user_metadata VALUES(?,?)',[key,json.dumps(value)])
            d.execute(query('SQLiteProgressRepository','INSERT INTO study_events'),['e',wid,1,200,'2026-10-19','UTC','vocabulary_pass','incorrect',100,'v',18])
            d.execute(query('SQLiteProgressRepository','INSERT INTO item_progress'),[wid,200,200,1,0,1])
            d.execute(query('SQLiteProgressRepository','INSERT INTO daily_statistics'),['2026-10-19','UTC',1,0,1,100]);d.commit()
            tables=[r[0]for r in d.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
            before={t:d.execute('SELECT * FROM '+t).fetchall()for t in tables}
            stats=d.execute(query('SQLiteStatistics','SELECT COUNT(CASE'),[0,300]).fetchone()
            difficult_args=['','','calendar_steps',1,0,300,0]
            difficult=d.execute(query('SQLiteSavedContent','SELECT content_id,skill AS content_type'),difficult_args).fetchall()
            self.assertEqual(len(difficult),20);d.close();before_hash=hashlib.sha256(progress.read_bytes()).hexdigest()
            shutil.copyfile(BUNDLE,content)
            self.assertEqual(hashlib.sha256(progress.read_bytes()).hexdigest(),before_hash)
            with sqlite3.connect(progress)as cold,sqlite3.connect(content)as current:
                for t in tables:self.assertEqual(cold.execute('SELECT * FROM '+t).fetchall(),before[t],t)
                self.assertEqual(cold.execute('PRAGMA user_version').fetchone()[0],10)
                self.assertEqual(cold.execute(query('SQLiteStatistics','SELECT COUNT(CASE'),[0,300]).fetchone(),stats)
                self.assertEqual(cold.execute(query('SQLiteSavedContent','SELECT content_id,skill AS content_type'),difficult_args).fetchall(),difficult)
                for i in ids:self.assertIsNotNone(current.execute(query('SQLiteVocabularyContent','SELECT v.headword'),[i]).fetchone())
                resume=query('SQLiteCurriculum','SELECT kind,target,level FROM')
                self.assertEqual(cold.execute(resume).fetchone()[:2],('lesson','legacy-lesson'))
                for table,change,expected in [('lesson_sessions',"status='completed'",'review'),('review_sessions',"status='completed'",'listening'),('listening_sessions','completed=1','production'),('production_sessions','completed=1','grammar'),('grammar_sessions',"status='completed'",'vocabulary')]:
                    cold.execute('UPDATE '+table+' SET '+change);self.assertEqual(cold.execute(resume).fetchone()[0],expected)
                self.assertEqual(cold.execute('SELECT state_json FROM vocabulary_sessions').fetchone()[0],snapshot)
                for limit in (5,10,20):self.assertEqual(len(cold.execute(query('SQLiteReviewProgress','SELECT content_id FROM srs_state WHERE'),['calendar_steps',1,300,limit]).fetchall()),limit)

    def test_immediate_commit_reopen_and_failed_late_write_rolls_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'user.sqlite';d=user(path,10)
            lid=self.manifest['units'][0]['lessons'][0]['id'];wid=self.words[0]['id']
            with d:
                d.execute(query('SQLiteProgressRepository','INSERT INTO lesson_sessions('),['session',lid,19,123,json.dumps([wid]),wid,100,100])
                d.execute(query('SQLiteProgressRepository','INSERT INTO lesson_progress('),[lid,100,wid])
            d.close();d=sqlite3.connect(path)
            with d:
                d.execute(query('SQLiteProgressRepository','INSERT INTO study_events'),['event',wid,2,101,'2026-10-19','UTC','vocabulary_preview','viewed',0,'session',19])
                d.execute(query('SQLiteProgressRepository','INSERT INTO item_progress'),[wid,101,101,1,0,0])
                d.execute(query('SQLiteProgressRepository','INSERT INTO daily_statistics'),['2026-10-19','UTC',1,0,0,0])
                d.execute(query('SQLiteProgressRepository','INSERT INTO lesson_step_results('),['session',wid,'event','viewed',None])
            d.close();d=sqlite3.connect(path)
            self.assertEqual(d.execute('SELECT current_content_id FROM lesson_sessions').fetchone()[0],wid)
            self.assertEqual(d.execute('SELECT outcome FROM lesson_step_results').fetchone()[0],'viewed')
            # Duplicate submission fails atomically, retaining the committed first answer/cursor.
            with self.assertRaises(sqlite3.IntegrityError),d:
                d.execute(query('SQLiteProgressRepository','INSERT INTO study_events'),['duplicate',wid,2,102,'2026-10-19','UTC','vocabulary_preview','viewed',0,'session',19])
                d.execute(query('SQLiteProgressRepository','INSERT INTO lesson_step_results('),['session',wid,'duplicate','viewed',None])
            self.assertEqual(d.execute('SELECT COUNT(*) FROM study_events').fetchone()[0],1);d.close()

    def test_core_sql_remains_usable_when_python_network_calls_are_forbidden(self):
        # Deliberately fails if these portable operations acquire a network dependency.
        # This is not airplane-mode iOS/TTS verification.
        with patch.object(socket,'socket',side_effect=AssertionError('offline SQL used network')):
            d=user(version=10)
            self.assertIsNotNone(d.execute(query('SQLiteProgressRepository','SELECT COALESCE(SUM'),[300]).fetchone())
            self.assertTrue(self.db.execute(query('SQLiteLookup','WITH terms'),['교류하다']*3+[0]).fetchall())
            self.assertEqual(d.execute(query('SQLiteReviewProgress','SELECT content_id FROM srs_state WHERE'),['calendar_steps',1,300,5]).fetchall(),[])
            self.assertTrue(self.db.execute(query('SQLiteContentRepository','SELECT c.*')).fetchall());d.close()

    def test_corrupt_new_relation_and_missing_listening_question_rejected(self):
        # Mutation probes enforce the existing validator; no assertion/contract weakened.
        import copy
        for case in ('missing_target','missing_question','unrevised_endpoint'):
            source=copy.deepcopy(self.source)
            t=source['tables'];qid=self.manifest['production'][0]['form_question_id']
            if case=='missing_target':t['content_links']=[l for l in t['content_links']if not(l['source_id']==qid and l['relation']=='question_target')]
            elif case=='missing_question':t['questions']=[q for q in t['questions']if q['id']!=self.manifest['listening'][0]['question_id']]
            else:
                wid=self.words[0]['id'];old=self.old.execute('SELECT revision FROM content_items WHERE id=?',[wid]).fetchone()[0]
                next(i for i in t['content_items']if i['id']==wid)['revision']=old
            with tempfile.TemporaryDirectory()as tmp:
                path=Path(tmp)/'bad.json';path.write_text(json.dumps(source,ensure_ascii=False))
                with self.subTest(case=case),self.assertRaises(ValidationError):build(path,Path(tmp)/'out.sqlite',self.previous,production=True)
