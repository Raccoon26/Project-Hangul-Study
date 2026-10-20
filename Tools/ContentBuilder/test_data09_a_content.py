"""Exact DATA09-A19→20 gate pinned to immutable20. Live21 preservation is in B.
Never language or Swift certification.
"""
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
import uuid
from pathlib import Path
from unittest.mock import patch
from build_content import ROOT,build
from validator import signatures,ValidationError,normalize
from test_data05_content import query
from test_lookup_sql import user

SOURCE=Path(os.environ.get('DATA09_A_SOURCE',ROOT/'Tests/Fixtures/content-v20-production.json.gz'))
BUNDLE=Path(os.environ.get('DATA09_A_BUNDLE',ROOT/'Tests/Fixtures/content-v20-production.sqlite'))


class Data09BatchATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global SOURCE
        cls.released_source=tempfile.TemporaryDirectory()
        if SOURCE.suffix=='.gz':
            raw=gzip.decompress(SOURCE.read_bytes());SOURCE=Path(cls.released_source.name)/'content20.json';SOURCE.write_bytes(raw)
        cls.source=json.loads(SOURCE.read_text())
        cls.registry=json.loads((ROOT/'Content/data09-a-ids.json').read_text())
        cls.approved=set(json.loads((ROOT/'Content/data09-a-revised-ids.json').read_text()))
        cls.old=sqlite3.connect(ROOT/'Tests/Fixtures/content-v19-production.sqlite')
        cls.db=sqlite3.connect(BUNDLE.resolve().as_uri()+'?mode=ro',uri=True)
    @classmethod
    def tearDownClass(cls):cls.db.close();cls.old.close();cls.released_source.cleanup()

    def test_strict19_to20_rebuild_all_rows_and_original_bytes(self):
        self.assertEqual(hashlib.sha256((ROOT/'Tests/Fixtures/content-v19-production.sqlite').read_bytes()).hexdigest(),'57aeaf918d5eaaec3bbfaed02f87c5452cca8264540b923a70448b781adbe9e5')
        self.assertEqual(hashlib.sha256(gzip.decompress((ROOT/'Tests/Fixtures/content-v19-production.json.gz').read_bytes())).hexdigest(),'f97b3bd70d07a3945770b8d6940c4a53e29a9b70b565caf21fb927230c08b4a8')
        with tempfile.TemporaryDirectory() as folder:
            out=Path(folder)/'rebuilt.sqlite';r=build(SOURCE,out,ROOT/'Tests/Fixtures/content-v19-production.sqlite',production=True)
            self.assertEqual((r['validation']['error_count'],r['validation']['warning_count']),(0,10))
            with sqlite3.connect(out) as rebuilt:
                for table, in self.db.execute("SELECT name FROM sqlite_master WHERE type='table'"):
                    self.assertEqual(collections.Counter(rebuilt.execute('SELECT * FROM '+table)),collections.Counter(self.db.execute('SELECT * FROM '+table)),table)
        self.assertEqual(self.db.execute('SELECT schema_version,content_version,min_reader_version,is_fixture FROM content_metadata').fetchone(),(4,20,7,0))
        self.assertEqual(self.db.execute('PRAGMA integrity_check').fetchall(),[('ok',)])
        self.assertEqual(self.db.execute('PRAGMA foreign_key_check').fetchall(),[])

    def test_exact_counts_stable_uuid4_and_no_unapproved_entities(self):
        expected={'vocabulary':2287,'meanings':2420,'examples':4669,'grammar':60,'grammar_examples':241,'questions':3409,'listening_items':1936,'courses':6,'lessons':91,'content_items':15597}
        for table,n in expected.items():self.assertEqual(self.db.execute('SELECT COUNT(*) FROM '+table).fetchone()[0],n,table)
        new={r[0] for r in self.db.execute('SELECT id FROM content_items')}-{r[0] for r in self.old.execute('SELECT id FROM content_items')}
        wanted={self.registry['course_id'],*self.registry['lesson_ids']}
        for g in self.registry['grammar']:wanted|={g['id'],*g['example_ids'],*g['question_ids']}
        self.assertEqual(new,wanted);self.assertEqual(len(new),169)
        for item in new:
            self.assertEqual(str(uuid.UUID(item)),item);self.assertEqual(uuid.UUID(item).version,4)
            self.assertEqual(self.db.execute('SELECT level,revision,is_active FROM content_items WHERE id=?',(item,)).fetchone(),('lower_intermediate',1,1))

    def test_every_old_payload_membership_and_exact12_revision_endpoints_preserved(self):
        before,after=signatures(self.old),signatures(self.db)
        self.assertTrue(set(before)<=set(after));self.assertEqual({i for i in before if before[i]!=after[i]},self.approved);self.assertEqual(len(self.approved),12)
        for row in self.old.execute('SELECT * FROM content_items'):
            expected=list(row)
            if row[0] in self.approved:expected[2]+=1;expected[-1]=self.registry['created_at']
            self.assertEqual(self.db.execute('SELECT * FROM content_items WHERE id=?',(row[0],)).fetchone(),tuple(expected))
        for table, in self.old.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
            if table in ('content_items','content_metadata','vocabulary_search'):continue
            self.assertTrue(set(self.old.execute('SELECT * FROM '+table))<=set(self.db.execute('SELECT * FROM '+table)),table)

    def test_new_patterns_and72_pairs_have_no_normalized_old_or_internal_duplicates(self):
        for table,field,ids in [('grammar','pattern',[g['id'] for g in self.registry['grammar']]),('examples','korean',[e for g in self.registry['grammar'] for e in g['example_ids']]),('examples','japanese',[e for g in self.registry['grammar'] for e in g['example_ids']])]:
            norm=lambda x:''.join(normalize(x).split())
            old={norm(r[0]) for r in self.old.execute('SELECT '+field+' FROM '+table)}
            new=[norm(self.db.execute('SELECT '+field+' FROM '+table+' WHERE id=?',(i,)).fetchone()[0]) for i in ids]
            self.assertEqual(len(new),len(set(new)));self.assertFalse(old&set(new))

    def test_all18_cards_and_six_lessons_reachable_through_actual_repository_sql(self):
        lessons=self.db.execute(query('SQLiteGrammarContent','SELECT l.id,l.title_ja'),['lower_intermediate',-1,30]).fetchall()
        self.assertEqual([l[2] for l in lessons],list(range(47,53)));self.assertEqual([l[3] for l in lessons],[3]*6)
        seen=[]
        for row in lessons:seen += [r[0] for r in self.db.execute(query('SQLiteGrammarContent','SELECT g.id FROM lesson_items'),[row[0]])]
        self.assertEqual(seen,[g['id'] for g in self.registry['grammar']])
        for g in self.registry['grammar']:
            self.assertIsNotNone(self.db.execute(query('SQLiteGrammarContent','SELECT g.*,i.revision'),[g['id']]).fetchone())
            self.assertEqual({r[0] for r in self.db.execute(query('SQLiteGrammarContent','SELECT e.id,e.korean'),[g['id']])},set(g['example_ids']))
            self.assertEqual({r[0] for r in self.db.execute(query('SQLiteGrammarContent','SELECT q.*,i.revision'),[g['id']])},set(g['question_ids']))
            self.assertGreaterEqual(len(self.db.execute(query('SQLiteGrammarContent','SELECT g.id,g.pattern'),[g['id']]).fetchall()),1)
        search=query('SQLiteGrammarContent','SELECT g.id FROM grammar g JOIN content_items');after='';ids=[]
        while True:
            page=self.db.execute(search,['lower_intermediate',after,'','','',4]).fetchall()
            if not page:break
            ids += [r[0] for r in page];after=page[-1][0]
        self.assertEqual(set(ids),set(seen));self.assertEqual(len(ids),18)

    def test_72_single_choice_contracts_all_distractor_rationales_and_supported_tasks(self):
        self.db.row_factory=sqlite3.Row
        tasks=collections.Counter();answers=collections.Counter()
        try:
            for g in self.registry['grammar']:
                for qid in g['question_ids']:
                    q=self.db.execute('SELECT * FROM questions WHERE id=?',(qid,)).fetchone();answer=json.loads(q['answer_json'])['correct_choice_ids'];choices=self.db.execute('SELECT choice_id,text FROM question_choices WHERE question_id=? ORDER BY ordinal',(qid,)).fetchall()
                    task=json.loads(q['rubric_json'])['grammar_task'];tasks[task]+=1
                    self.assertEqual(q['question_type'],'multiple_choice');self.assertEqual(len(answer),1);self.assertEqual(len(choices),3)
                    self.assertIn(answer[0],[r[0] for r in choices]);answers[answer[0]]+=1
                    for _,text in choices:self.assertIn('「'+text+'」：',q['explanation_ja'])
                    self.assertEqual(self.db.execute("SELECT target_id FROM content_links WHERE source_id=? AND relation='question_target'",(qid,)).fetchall()[0][0],g['id'])
                    self.assertEqual(q['direction'],'ko_ko' if task=='form' else 'ko_ja')
        finally:self.db.row_factory=None
        self.assertEqual(tasks,dict(meaning=18,form=18,context=18,contrast=18));self.assertEqual(answers,dict(a=24,b=24,c=24))

    def test_reviewed_irregular_and_particle_forms_are_exact_authored_answers(self):
        expected=['듣기 때문에','만드느라고','놓치는 바람에','추워지다','살게 되다','들어야','산다면','듣거든','들으려면','공부하기 위해','잊지 않도록','확인하도록 하다','돕기로 하다','들을까 하다','들어야겠다','추울까 봐','읽다 보면','들을 필요가 있다']
        for g,wanted in zip(self.registry['grammar'],expected):
            qid=g['question_ids'][1];answer=json.loads(self.db.execute('SELECT answer_json FROM questions WHERE id=?',(qid,)).fetchone()[0])['correct_choice_ids'][0]
            self.assertEqual(self.db.execute('SELECT text FROM question_choices WHERE question_id=? AND choice_id=?',(qid,answer)).fetchone()[0],wanted)

    def test_combined_prerequisite_graph_has_no_cycle_and_all_targets_are_active(self):
        edges=collections.defaultdict(list)
        for a,b,active in self.db.execute("SELECT l.source_id,l.target_id,i.is_active FROM content_links l JOIN grammar g ON g.id=l.source_id JOIN grammar t ON t.id=l.target_id JOIN content_items i ON i.id=t.id WHERE relation='prerequisite'"):
            self.assertEqual(active,1);edges[a].append(b)
        def visit(key,path):
            self.assertNotIn(key,path)
            for target in edges[key]:visit(target,path|{key})
        for g in self.registry['grammar']:visit(g['id'],set())

    def test_invalid_revision_version_task_and_multiple_answers_are_rejected(self):
        first=self.registry['grammar'][0];gid=first['id'];qid=first['question_ids'][0]
        changes={
            'version':lambda s:s['metadata'].update(content_version=19),
            'revision':lambda s:next(r for r in s['tables']['content_items'] if r['id']==sorted(self.approved)[0]).update(revision=self.old.execute('SELECT revision FROM content_items WHERE id=?',(sorted(self.approved)[0],)).fetchone()[0]),
            'unsupported':lambda s:next(q for q in s['tables']['questions'] if q['id']==qid).update(rubric_json='{"grammar_task":"free_writing"}'),
            'multiple':lambda s:next(q for q in s['tables']['questions'] if q['id']==qid).update(answer_json='{"correct_choice_ids":["a","b"]}'),
            'no_examples':lambda s:s['tables'].update(grammar_examples=[r for r in s['tables']['grammar_examples'] if r['grammar_id']!=gid]),
        }
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'bad.json'
            for name,change in changes.items():
                with self.subTest(case=name):
                    source=copy.deepcopy(self.source);change(source);p.write_text(json.dumps(source,ensure_ascii=False))
                    with self.assertRaises(ValidationError):build(p,Path(folder)/'bad.sqlite',ROOT/'Tests/Fixtures/content-v19-production.sqlite',production=True)

    def test_disk_content_swap_preserves_user_snapshot_srs_and_duplicate_enrollment(self):
        with tempfile.TemporaryDirectory() as folder:
            active=Path(folder)/'content.sqlite';path=Path(folder)/'user.sqlite';shutil.copyfile(ROOT/'Tests/Fixtures/content-v19-production.sqlite',active)
            d=user(path,10);old_g=self.old.execute('SELECT id FROM grammar ORDER BY id LIMIT 1').fetchone()[0]
            d.execute("INSERT INTO srs_state VALUES(?,'grammar','calendar_steps',1,'{\"stage\":4}',900,NULL,100)",(old_g,));d.execute("INSERT INTO favorites(content_id,created_at,content_type) VALUES(?,100,'grammar')",(old_g,))
            snapshot=json.dumps(dict(ids=[old_g],order=[old_g],position=0,page=3,contentVersion=19,selected='b',revision=8))
            d.execute("INSERT INTO grammar_sessions VALUES('active','old-lesson',?,8,'active',100)",(snapshot,));d.commit();d.close()
            before=hashlib.sha256(path.read_bytes()).hexdigest();shutil.copyfile(BUNDLE,active)
            with patch.object(socket,'socket',side_effect=AssertionError('network forbidden')):
                with sqlite3.connect(active) as c:self.assertIsNotNone(c.execute(query('SQLiteGrammarContent','SELECT g.*,i.revision'),[old_g]).fetchone())
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),before)
            d=sqlite3.connect(path);self.assertEqual(d.execute('SELECT state_json FROM grammar_sessions').fetchone()[0],snapshot)
            enroll=query('SQLiteGrammarProgress','INSERT INTO srs_state(')
            for _ in range(2):
                d.execute(enroll,[old_g,'calendar_steps',1,'{"stage":0}',0,0])
                for g in self.registry['grammar']:d.execute(enroll,[g['id'],'calendar_steps',1,'{"stage":0}',0,0])
            self.assertEqual(d.execute("SELECT state_json,due_at FROM srs_state WHERE content_id=? AND skill='grammar'",(old_g,)).fetchone(),('{"stage":4}',900))
            self.assertEqual(d.execute('SELECT COUNT(*) FROM srs_state').fetchone()[0],19);self.assertEqual(d.execute('SELECT * FROM favorites').fetchall(),[(old_g,100,'grammar')])
            d.close()
