"""DATA09 actual Content19/23->24 SQLite and extracted repository SQL; not Swift/iOS certification."""
import collections
import copy
import gzip
import hashlib
import json
import os
import shutil
import socket
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from build_content import ROOT,build
from validator import signatures,ValidationError
from prepare_data09_integration import prepare,BASE_SHA
from audit_data09_final import audit,registries
from test_lookup_sql import user
from test_data05_content import query
from audit_data08_final import cohorts

SOURCE=Path(os.environ.get('DATA09_INTEGRATION_SOURCE',ROOT/'Content/production.json'))
BUNDLE=Path(os.environ.get('DATA09_INTEGRATION_BUNDLE',ROOT/'Resources/content.sqlite'))


class Data09IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=json.loads(SOURCE.read_text());cls.manifest=json.loads((ROOT/'Content/data09-integration-ids.json').read_text())
        cls.registry={r['key']:r for r in registries()};cls.ids={r['id'] for r in cls.registry.values()}
        cls.approved=set(json.loads((ROOT/'Content/data09-integration-revised-ids.json').read_text()))
        cls.db=sqlite3.connect(BUNDLE);cls.old=sqlite3.connect(ROOT/'Tests/Fixtures/content-v23-production.sqlite')
    @classmethod
    def tearDownClass(cls):cls.db.close();cls.old.close()

    def test_preserved19_and23_sources_and_both_strict_update_gates(self):
        expected={19:('57aeaf918d5eaaec3bbfaed02f87c5452cca8264540b923a70448b781adbe9e5','f97b3bd70d07a3945770b8d6940c4a53e29a9b70b565caf21fb927230c08b4a8'),23:('0a4051d3c5423441b50348935d64559504f1553a55fd3ea472c84b40c9ebc025',BASE_SHA)}
        with tempfile.TemporaryDirectory() as folder:
            for v,(dbsha,srcsha) in expected.items():
                prev=ROOT/f'Tests/Fixtures/content-v{v}-production.sqlite'
                self.assertEqual(hashlib.sha256(prev.read_bytes()).hexdigest(),dbsha)
                self.assertEqual(hashlib.sha256(gzip.decompress((ROOT/f'Tests/Fixtures/content-v{v}-production.json.gz').read_bytes())).hexdigest(),srcsha)
                out=Path(folder)/f'from{v}.sqlite';result=build(SOURCE,out,prev,production=True)
                self.assertEqual((result['validation']['error_count'],result['validation']['warning_count']),(0,10))
                self.assertEqual(out.read_bytes(),BUNDLE.read_bytes())
        self.assertEqual(self.db.execute('PRAGMA integrity_check').fetchall(),[('ok',)])
        self.assertEqual(self.db.execute('PRAGMA foreign_key_check').fetchall(),[])
        self.assertEqual(self.db.execute('select schema_version,content_version,min_reader_version from content_metadata').fetchone(),(4,24,7))

    def test_exact107_endpoint_revisions_six_unit_ids_no_old_payload_or_membership_change(self):
        a,b=signatures(self.old),signatures(self.db)
        self.assertEqual(set(b)-set(a),{u['id'] for u in self.manifest['units']})
        self.assertEqual({i for i in a if a[i]!=b[i]},self.approved);self.assertEqual(len(self.approved),107)
        for r in self.old.execute('SELECT * FROM content_items'):
            expected=list(r)
            if r[0] in self.approved:expected[2]+=1;expected[-1]=self.manifest['created_at']
            self.assertEqual(self.db.execute('SELECT * FROM content_items WHERE id=?',(r[0],)).fetchone(),tuple(expected))
        for table, in self.old.execute("SELECT name FROM sqlite_master WHERE type='table'"):
            if table in ('content_metadata','content_items','vocabulary_search','sqlite_stat1'):continue
            self.assertTrue(set(self.old.execute('SELECT * FROM '+table))<=set(self.db.execute('SELECT * FROM '+table)),table)
        for t in ('grammar','examples','questions','question_choices','lesson_items','lessons','courses','vocabulary','meanings','grammar_examples','listening_items'):
            self.assertEqual(self.old.execute('SELECT * FROM '+t).fetchall(),self.db.execute('SELECT * FROM '+t).fetchall(),t)

    def test_deterministic24_source_and_revision_registry(self):
        with tempfile.TemporaryDirectory() as folder:
            out=Path(folder)/'source.json';rev=Path(folder)/'revised.json';prepare(out,rev)
            self.assertEqual(out.read_bytes(),SOURCE.read_bytes());self.assertEqual(set(json.loads(rev.read_text())),self.approved)
        self.assertEqual(audit(self.source)['validation']['errors'],[])
        for table,n in [('content_items',15941),('grammar',96),('grammar_examples',389),('questions',3553),('examples',4813),('vocabulary',2287),('content_links',6499)]:self.assertEqual(self.db.execute('SELECT COUNT(*) FROM '+table).fetchone()[0],n)

    def test_course_unit_lesson_runtime_query_reaches_all54_once_in_short_sets(self):
        rows=self.db.execute(query('SQLiteGrammarContent','SELECT l.id,l.title_ja'),['lower_intermediate',-1,30]).fetchall()
        self.assertEqual(len(rows),18);self.assertEqual([r[2] for r in rows],list(range(47,65)))
        self.assertEqual({r[4] for r in rows},{self.db.execute('select title_ja from courses where id=?',(u['course_id'],)).fetchone()[0] for u in self.manifest['units']})
        self.assertEqual({r[5] for r in rows},{u['title_ja'] for u in self.manifest['units']})
        seen=[]
        for u in self.manifest['units']:
            self.assertEqual(len(u['lesson_ids']),3)
            for lid in u['lesson_ids']:
                self.assertEqual(self.db.execute("select count(*) from item_tags it join tags t on t.id=it.tag_id where content_id=? and namespace='data09_unit'",(lid,)).fetchone()[0],1)
                ids=[r[0] for r in self.db.execute(query('SQLiteGrammarContent','SELECT g.id FROM lesson_items'),[lid])]
                self.assertEqual(len(ids),3);seen+=ids
        self.assertEqual(set(seen),self.ids);self.assertEqual(len(seen),54)
        # Keep generic lesson engine away from grammar-only lessons.
        generic={r[0] for r in self.db.execute(query('SQLiteContentRepository','SELECT c.*'))}
        self.assertFalse(generic & {u['course_id'] for u in self.manifest['units']})

    def test_prerequisites_active_acyclic_and_loaded_before_explanations(self):
        all_ids={r[0] for r in self.db.execute('select id from grammar')};edges=collections.defaultdict(list)
        for a,b in self.db.execute("select l.source_id,l.target_id from content_links l join grammar g on g.id=l.source_id where l.relation='prerequisite'"):
            self.assertIn(b,all_ids);edges[a].append(b)
        def visit(i,path):
            self.assertNotIn(i,path)
            for j in edges[i]:visit(j,path|{i})
        for i in all_ids:visit(i,set())
        q=query('SQLiteGrammarContent','SELECT g.id,g.pattern,g.meaning_ja,g.form_ko')
        for i in self.ids:
            rows=self.db.execute(q,[i]).fetchall();self.assertGreater(len(rows),0);self.assertLessEqual(len(rows),8)
            self.assertTrue(all(all(value for value in r) for r in rows))
        for key,pre in [('A10','C01'),('A18','B01'),('B16','C02'),('C14','B03'),('C17','A05')]:self.assertIn(self.registry[pre]['id'],edges[self.registry[key]['id']])
        view=(ROOT/'Views/GrammarLearningViews.swift').read_text();self.assertIn('先に確認したい形',view)
        self.assertIn('if page == 0',view);self.assertIn('表示するだけでは学習完了になりません',view)

    def test_all_216_questions_and_220_example_placements_keep_actual_approved_text(self):
        count=0
        for g in self.registry.values():
            examples=self.db.execute(query('SQLiteGrammarContent','SELECT e.id,e.korean'),[g['id']]).fetchall()
            self.assertTrue(4<=len(examples)<=6);self.assertTrue(set(g['example_ids'])<={r[0] for r in examples})
            for r in examples:self.assertTrue(r[1] and r[2])
            count+=len(examples)
            questions=self.db.execute(query('SQLiteGrammarContent','SELECT q.*,i.revision'),[g['id']]).fetchall()
            self.assertEqual({r[0] for r in questions},set(g['question_ids']))
            for qid in g['question_ids']:
                answer=json.loads(self.db.execute('select answer_json from questions where id=?',(qid,)).fetchone()[0])['correct_choice_ids']
                choices=self.db.execute(query('SQLiteGrammarContent','SELECT choice_id,text'),[qid]).fetchall()
                self.assertEqual(len(answer),1);self.assertEqual(len(choices),3);self.assertIn(answer[0],{r[0] for r in choices})
        self.assertEqual(count,220)

    def test_editorial_example_notes_reach_reader_model_and_view(self):
        for key,n in [('B03',2),('B11',1),('B16',3),('C11',1),('C11',2)]:
            g=self.registry[key];eid=g['example_ids'][n-1]
            row=next(r for r in self.db.execute(query('SQLiteGrammarContent','SELECT e.id,e.korean'),[g['id']]) if r[0]==eid)
            self.assertIn('弟・妹',row[3]);self.assertIn('弟の場面',row[3])
        self.assertIn('learningPoint: $0["learning_point_ja"]?.string',(ROOT/'Repositories/SQLiteGrammarContent.swift').read_text())
        self.assertIn('if let note = example.learningPoint',(ROOT/'Views/GrammarLearningViews.swift').read_text())

    def test_related_lexicon_dictionary_and_supported_input_routes_are_real(self):
        related=query('SQLiteLookup','WITH related');prod=query('SQLiteProduction','SELECT q.*');seen=set();supported=0;sentence=0
        for r in self.manifest['related_vocabulary']:
            gid,vid=r['grammar_id'],r['vocabulary_id'];seen.add(vid)
            self.assertIn((vid,'vocabulary'),self.db.execute(related,[gid]*5).fetchall())
            self.assertIn((gid,'grammar'),self.db.execute(related,[vid]*5).fetchall())
            lookup=self.db.execute(query('SQLiteLookup','SELECT i.level'),[vid,'vocabulary']).fetchone();self.assertIsNotNone(lookup)
            self.assertEqual(self.db.execute('select headword from vocabulary where id=?',(vid,)).fetchone()[0],r['headword'])
            questions=self.db.execute(prod,[vid]).fetchall()
            if questions:supported+=1
            for q in questions:
                cols=[x[0] for x in self.db.execute(prod,[vid]).description];item=dict(zip(cols,q));a=json.loads(item['answer_json']);rubric=json.loads(item['rubric_json'])
                self.assertTrue(a['accepted']);self.assertTrue(all(x.strip() for x in a['accepted']));self.assertIn(rubric['form'],['present','past','future','negativeShort','negativeLong','wish','connective','reason','condition'])
                sentence+=rubric['mode']=='sentence'
        self.assertEqual(len(seen),35);self.assertGreater(supported,0);self.assertGreater(sentence,0)
        code=(ROOT/'Views/LookupDetailView.swift').read_text();self.assertIn('if word?.hasProductionPractice == true',code);self.assertIn('ProductionStudyView(services:services,id:reference.contentID)',code)

    def test_literal_search_all54_by_korean_pattern_and_japanese_meaning(self):
        for g in self.registry.values():
            pattern,meaning=self.db.execute('select pattern,meaning_ja from grammar where id=?',(g['id'],)).fetchone()
            for term in (pattern,meaning):self.assertIn((g['id'],'grammar'),self.db.execute(query('SQLiteLookup','WITH terms'),[term.lower()]*3+[0]).fetchall())
        for term in ('%',"' OR 1=1 --",'_'):
            self.assertEqual(self.db.execute(query('SQLiteLookup','WITH terms'),[term]*3+[0]).fetchall(),[])

    def test_19_and23_update_preserves_all_user_tables_snapshots_settings_and_statistics(self):
        for version in (19,23):
            with self.subTest(previous=version),tempfile.TemporaryDirectory() as folder:
                root=Path(folder);active=root/'content.sqlite';path=root/'user.sqlite';shutil.copyfile(ROOT/f'Tests/Fixtures/content-v{version}-production.sqlite',active)
                old=sqlite3.connect(active)
                gid=self.registry['A01']['id'] if version==23 else old.execute('select id from grammar order by id limit 1').fetchone()[0]
                grammar_lesson=old.execute('select lesson_id from lesson_items where content_id=?',[gid]).fetchone()[0]
                grammar_question=old.execute("select source_id from content_links where target_id=? and relation='question_target' order by source_id limit 1",[gid]).fetchone()[0]
                legacy_lesson,char_id=old.execute('select li.lesson_id,h.id from lesson_items li join hangul h on h.id=li.content_id order by li.lesson_id,li.ordinal limit 1').fetchone()
                production_word=old.execute("select v.id from vocabulary v join content_links l on l.target_id=v.id join questions q on q.id=l.source_id where q.question_type='text_input' and json_extract(q.rubric_json,'$.production')=1 order by v.id limit 1").fetchone()[0]
                listening_id,listening_question=old.execute('select l.id,q.id from listening_items l join questions q on q.listening_id=l.id order by l.id limit 1').fetchone()
                old.close()
                d=user(path,10);ids=[w['id'] for c in cohorts().values() for w in c['vocabulary']][:20];wid=ids[0]
                d.execute(query('SQLiteVocabularyProgress','INSERT INTO vocabulary_sets('),['set','lower_intermediate',1,100])
                for n,i in enumerate(ids):
                    d.execute(query('SQLiteVocabularyProgress','INSERT INTO vocabulary_set_items('),['set',i,n]);d.execute("INSERT INTO srs_state VALUES(?,'vocabulary','calendar_steps',1,?,300,200,200)",[i,json.dumps(dict(stage=1,failureCount=2,consecutiveSuccesses=0,lastResult='difficult'))])
                d.execute("INSERT INTO srs_state VALUES(?,'grammar','calendar_steps',1,'{\"stage\":4}',900,200,200)",[gid])
                snapshot=json.dumps(dict(vocabularyIDs=ids,order=ids[::-1],position=4,round=2,revision=9,contentVersionAtStart=version))
                d.execute(query('SQLiteVocabularyProgress','INSERT INTO vocabulary_sessions('),['v','set',snapshot,9,100])
                d.execute("INSERT INTO grammar_sessions VALUES('g',?,?,4,'active',110)",[grammar_lesson,json.dumps(dict(ids=[gid],order=[gid],position=0,question_id=grammar_question,selected='a',revision=4,contentVersion=version))])
                d.execute(query('SQLiteProduction','INSERT INTO production_sessions'),['p',production_word,json.dumps(dict(position=1,retry=[0],revision=3,updatedAt=120-978307200,contentVersion=version)),0])
                d.execute(query('SQLiteListening','INSERT INTO listening_sessions'),['l','practice:lower_intermediate:10',json.dumps(dict(position=1,item_id=listening_id,question_id=listening_question,heard=True,revision=3,updatedAt=130-978307200,contentVersion=version)),0])
                d.execute("INSERT INTO review_sessions VALUES('r','vocabulary','active',90,140,NULL)");d.execute("INSERT INTO review_items(session_id,content_id,ordinal) VALUES('r',?,0)",[wid])
                d.execute("INSERT INTO lesson_sessions VALUES('h',?,?,1,?,?,'active',90,150,NULL)",[legacy_lesson,version,json.dumps([char_id]),char_id])
                d.execute(query('SQLiteProgressRepository','INSERT INTO lesson_progress('),[legacy_lesson,100,char_id]);d.execute('update lesson_progress set completed_count=2')
                for i,kind in [(wid,'vocabulary'),(gid,'grammar')]:d.execute(query('SQLiteSavedContent','INSERT INTO favorites'),[i,100,kind])
                for key,value in [('opaque','unchanged'),('settings','{"reviewLimit":10}'),('curriculum.profile.v1','{"version":1,"level":"lower_intermediate","skippedHangul":true}')]:d.execute('insert into user_metadata values(?,?)',[key,value])
                d.execute(query('SQLiteProgressRepository','INSERT INTO study_events'),['e',wid,1,200,'2026-10-20','UTC','vocabulary_pass','incorrect',100,'v',version])
                d.execute(query('SQLiteProgressRepository','INSERT INTO item_progress'),[wid,200,200,1,0,1]);d.execute(query('SQLiteProgressRepository','INSERT INTO daily_statistics'),['2026-10-20','UTC',1,0,1,100]);d.commit()
                tables=[r[0] for r in d.execute("select name from sqlite_master where type='table'")];before={t:d.execute('select * from '+t).fetchall() for t in tables}
                stats=d.execute(query('SQLiteStatistics','SELECT COUNT(CASE'),[0,300]).fetchone();d.close();sha=hashlib.sha256(path.read_bytes()).hexdigest()
                shutil.copyfile(BUNDLE,active);self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),sha)
                with sqlite3.connect(active) as current:
                    self.assertIsNotNone(current.execute(query('SQLiteGrammarContent','SELECT g.*,i.revision'),[gid]).fetchone())
                    self.assertIn((gid,),current.execute(query('SQLiteGrammarContent','SELECT g.id FROM lesson_items'),[grammar_lesson]).fetchall())
                    self.assertIsNotNone(current.execute('select id from questions where id=?',[grammar_question]).fetchone())
                    self.assertTrue(current.execute(query('SQLiteProduction','SELECT q.*'),[production_word]).fetchall())
                    self.assertIsNotNone(current.execute('select id from listening_items where id=?',[listening_id]).fetchone())
                    self.assertTrue(current.execute(query('SQLiteContentRepository','SELECT i.id,i.kind'),[legacy_lesson]).fetchall())
                with sqlite3.connect(path) as cold:
                    for t in tables:self.assertEqual(cold.execute('select * from '+t).fetchall(),before[t],t)
                    self.assertEqual(cold.execute(query('SQLiteStatistics','SELECT COUNT(CASE'),[0,300]).fetchone(),stats)
                    self.assertEqual(cold.execute(query('SQLiteCurriculum','SELECT kind,target,level FROM')).fetchone()[:2],('lesson',legacy_lesson))
                    difficult=cold.execute(query('SQLiteSavedContent','SELECT content_id,skill AS content_type'),['','','calendar_steps',1,0,300,0]).fetchall();self.assertEqual(len(difficult),20)
                    for limit in (5,10,20):self.assertEqual(len(cold.execute(query('SQLiteReviewProgress','SELECT content_id FROM srs_state WHERE'),['calendar_steps',1,300,limit]).fetchall()),limit)

    def test_54_grammar_srs_enrollment_twice_preserves_due_and_atomic_rollback(self):
        with tempfile.TemporaryDirectory() as folder:
            d=user(Path(folder)/'user.sqlite',10);gid=self.registry['A01']['id']
            d.execute("INSERT INTO srs_state VALUES(?,'grammar','calendar_steps',1,'{\"stage\":4}',900,100,100)",[gid]);d.commit()
            for _ in range(2):
                with d:
                    for i in self.ids:d.execute(query('SQLiteGrammarProgress','INSERT INTO srs_state('),[i,'calendar_steps',1,'{"stage":0}',0,100])
            self.assertEqual(d.execute('select count(*) from srs_state').fetchone()[0],54)
            self.assertEqual(d.execute('select state_json,due_at from srs_state where content_id=?',[gid]).fetchone(),('{"stage":4}',900))
            before=d.execute('select * from srs_state order by content_id').fetchall()
            with self.assertRaises(sqlite3.IntegrityError),d:
                d.execute('update srs_state set due_at=0');d.execute("INSERT INTO grammar_sessions VALUES('bad','l','{}',-1,'active',1)")
            self.assertEqual(d.execute('select * from srs_state order by content_id').fetchall(),before);d.close()

    def test_socket_forbidden_curriculum_cards_and_search_work_offline(self):
        with patch.object(socket,'socket',side_effect=AssertionError('network forbidden')):
            for gid in self.ids:
                self.assertIsNotNone(self.db.execute(query('SQLiteGrammarContent','SELECT g.*,i.revision'),[gid]).fetchone())
                self.assertTrue(self.db.execute(query('SQLiteGrammarContent','SELECT e.id,e.korean'),[gid]).fetchall())
            self.assertEqual(len(self.db.execute(query('SQLiteGrammarContent','SELECT l.id,l.title_ja'),['lower_intermediate',-1,30]).fetchall()),18)
            self.assertTrue(self.db.execute(query('SQLiteLookup','WITH terms'),['推測']*3+[0]).fetchall())

    def test_strict_validator_rejects_unrevised_relation_endpoints_and_missing_targets(self):
        with tempfile.TemporaryDirectory() as folder:
            for case in ('revision','reference','duplicate'):
                s=copy.deepcopy(self.source)
                if case=='revision':
                    vid=self.manifest['related_vocabulary'][0]['vocabulary_id'];old=self.old.execute('select revision from content_items where id=?',[vid]).fetchone()[0]
                    next(r for r in s['tables']['content_items'] if r['id']==vid)['revision']=old
                elif case=='reference':s['tables']['content_links'][-1]['target_id']='00000000-0000-4000-8000-000000000000'
                else:s['tables']['content_items'].append(dict(s['tables']['content_items'][-1]))
                p=Path(folder)/'bad.json';p.write_text(json.dumps(s,ensure_ascii=False))
                with self.subTest(case=case),self.assertRaises(ValidationError):build(p,Path(folder)/'bad.sqlite',ROOT/'Tests/Fixtures/content-v23-production.sqlite',production=True)
