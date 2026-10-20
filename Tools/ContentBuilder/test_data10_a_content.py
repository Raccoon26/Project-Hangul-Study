"""DATA10-A exact 24->25 gate and actual repository SQL; no audio/human claims."""
import collections
import gzip
import hashlib
import json
import os
import re
import shutil
import sqlite3
import tempfile
import unicodedata
import unittest
import uuid
from pathlib import Path
from build_content import ROOT, build
from prepare_data10_a import prepare, BASE_SHA
from validator import signatures
from test_data05_content import query
from test_lookup_sql import user

SOURCE=Path(os.environ.get('DATA10_A_SOURCE',ROOT/'Content/production.json'))
BUNDLE=Path(os.environ.get('DATA10_A_BUNDLE',ROOT/'Resources/content.sqlite'))
norm=lambda s:' '.join(unicodedata.normalize('NFC',s).split())


class Data10ATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=json.loads(SOURCE.read_text());cls.t=cls.source['tables']
        cls.manifest=json.loads((ROOT/'Content/data10-a-authoring.json').read_text());cls.items=cls.manifest['items']
        cls.db=sqlite3.connect(BUNDLE);cls.old=sqlite3.connect(ROOT/'Tests/Fixtures/content-v24-production.sqlite')
    @classmethod
    def tearDownClass(cls):cls.db.close();cls.old.close()

    def test_immutable24_and_deterministic25_strict_rebuild(self):
        self.assertEqual(hashlib.sha256(gzip.decompress((ROOT/'Tests/Fixtures/content-v24-production.json.gz').read_bytes())).hexdigest(),BASE_SHA)
        self.assertEqual(hashlib.sha256((ROOT/'Tests/Fixtures/content-v24-production.sqlite').read_bytes()).hexdigest(),'56a7fa8b5358e254eeb324e706860d150d20c8ec013ba0b6f602cf14d93cceff')
        with tempfile.TemporaryDirectory() as folder:
            src=Path(folder)/'source.json';rev=Path(folder)/'revised.json';out=Path(folder)/'out.sqlite';prepare(src,rev)
            self.assertEqual(src.read_bytes(),SOURCE.read_bytes());self.assertEqual(json.loads(rev.read_text()),[]);self.assertEqual(json.loads((ROOT/'Content/data10-a-revised-ids.json').read_text()),[])
            r=build(src,out,ROOT/'Tests/Fixtures/content-v24-production.sqlite',production=True)
            self.assertEqual((r['validation']['error_count'],r['validation']['warning_count']),(0,10))
            self.assertEqual(out.read_bytes(),BUNDLE.read_bytes())

    def test_every_old_row_and_fingerprint_preserved_new_ids_exactly300(self):
        old_source=json.loads(gzip.decompress((ROOT/'Tests/Fixtures/content-v24-production.json.gz').read_bytes()))
        for table,rows in old_source['tables'].items():self.assertEqual(self.t[table][:len(rows)],rows,table)
        a,b=signatures(self.old),signatures(self.db)
        self.assertTrue(a.keys()<=b.keys());self.assertEqual({i for i in a if a[i]!=b[i]},set())
        expected={r['example_id'] for r in self.items}|{s[k] for r in self.items for s in r['tasks'] for k in ('listening_id','question_id')}
        self.assertEqual(set(b)-set(a),expected);self.assertEqual(len(expected),300)
        for table in self.t:
            old=collections.Counter(self.old.execute('SELECT * FROM '+table));new=collections.Counter(self.db.execute('SELECT * FROM '+table))
            self.assertFalse(old-new,table)
        for i in expected:self.assertEqual(str(uuid.UUID(i)),i)
        self.assertEqual(self.db.execute('select schema_version,content_version,min_reader_version from content_metadata').fetchone(),(4,25,7))

    def test_full_source_database_rows_integrity_and_precise_counts(self):
        for table,rows in self.t.items():
            keys=sorted(rows[0]) if rows else [r[1] for r in self.db.execute('pragma table_info('+table+')')]
            actual=collections.Counter(self.db.execute('SELECT '+','.join('"'+k+'"' for k in keys)+' FROM '+table))
            self.assertEqual(actual,collections.Counter(tuple(r.get(k) for k in keys) for r in rows),table)
        for t,n in [('examples',4873),('listening_items',2056),('questions',3673),('content_items',16241),('vocabulary',2287),('meanings',2420),('grammar',96)]:self.assertEqual(self.db.execute('select count(*) from '+t).fetchone()[0],n)
        self.assertEqual(self.db.execute('pragma integrity_check').fetchall(),[('ok',)]);self.assertEqual(self.db.execute('pragma foreign_key_check').fetchall(),[])
        self.assertEqual(len(self.db.execute("select name from sqlite_master where type='table'").fetchall()),31)

    def test_60_new_passages_no_old_or_internal_duplicate_even_without_final_punctuation(self):
        old=[(r[0],r[1]) for r in self.old.execute('select korean,japanese from examples')];seen=set()
        for r in self.items:
            ko,ja=norm(r['korean']),norm(r['japanese']);key=ko.rstrip('.!?')
            self.assertNotIn(key,{norm(a).rstrip('.!?') for a,b in old});self.assertNotIn(key,seen);seen.add(key)
            self.assertNotIn((ko,ja),{(norm(a),norm(b)) for a,b in old})
            self.assertGreaterEqual(len(re.findall(r'[.!?]',ko)),2);self.assertLessEqual(len(ko),120)
        self.assertEqual(len(seen),60);self.assertEqual(collections.Counter(r['domain'] for r in self.items),dict.fromkeys(['daily','reschedule','transport','shopping','service','request'],10))

    def test_four_tasks_unique_answer_all_choices_real_and_exact_dictation(self):
        tasks=collections.Counter();answers=collections.Counter()
        for r in self.items:
            for spec in r['tasks']:
                q=self.db.execute('select question_type,prompt_ko,answer_json,rubric_json from questions where id=?',[spec['question_id']]).fetchone()
                task=json.loads(q[3])['listening_task'];tasks[task]+=1;self.assertIsNone(q[1])
                answer=json.loads(q[2]);choices=self.db.execute('select choice_id,text from question_choices where question_id=? order by ordinal',[spec['question_id']]).fetchall()
                if task=='dictation':
                    self.assertEqual(q[0],'listening_input');self.assertEqual(answer,dict(accepted=[r['korean']]));self.assertFalse(choices)
                    # Internal punctuation is retained, only final punctuation may be omitted by Swift judge.
                    self.assertRegex(r['korean'],r'[.!?] ')
                else:
                    self.assertEqual(q[0],'listening_choice');self.assertEqual(len(choices),3);self.assertEqual(len({norm(t) for i,t in choices}),3)
                    ids=answer['correct_choice_ids'];self.assertEqual(len(ids),1);correct=dict(choices)[ids[0]];answers[ids[0]]+=1
                    self.assertEqual(correct,r['japanese'] if task=='meaning' else r['korean'] if task=='korean' else spec['correct'])
                    if task=='korean':
                        for _,text in choices:self.assertIsNotNone(self.db.execute('select 1 from examples where korean=?',[text]).fetchone())
        self.assertEqual(tasks,dict(comprehension=60,dictation=30,meaning=18,korean=12));self.assertEqual(answers,dict(a=30,b=30,c=30))

    def test_actual_bounded_repository_query_and_no_same_source_within_batch(self):
        q=query('SQLiteListening','SELECT q.*,l.id');seen=set()
        for batch in range(103,109):
            ids=[r[0] for r in self.db.execute(query('SQLiteListening','SELECT l.id FROM listening_items'),['lower_intermediate',batch*20,(batch+1)*20])]
            self.assertEqual(len(ids),20)
            rows=self.db.execute(q+' AND l.id IN ('+','.join('?' for _ in ids)+') ORDER BY l.learning_order,l.id LIMIT 20',ids).fetchall()
            cols=[c[0] for c in self.db.execute(q+' LIMIT 0').description];rows=[dict(zip(cols,r)) for r in rows]
            self.assertEqual(len(rows),20);self.assertEqual(len({r['source_example_id'] for r in rows}),20)
            for row in rows:
                self.assertEqual(row['audio_mode'],'tts');self.assertEqual(self.db.execute('select audio_asset_id,transcript_ko from listening_items where id=?',[row['item_id']]).fetchone(),(None,None));self.assertEqual(row['level'],'lower_intermediate');seen.add(row['id'])
        self.assertEqual(seen,{s['question_id'] for r in self.items for s in r['tasks']})
        for r in self.items:
            batches=[self.db.execute('select learning_order/20 from listening_items where id=?',[s['listening_id']]).fetchone()[0] for s in r['tasks']]
            self.assertEqual(batches[1]-batches[0],3)

    def test_content24_to25_keeps_on_disk_user_state_and_active_snapshot(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);active=root/'content.sqlite';shutil.copyfile(ROOT/'Tests/Fixtures/content-v24-production.sqlite',active)
            lid,qid=self.old.execute('select l.id,q.id from listening_items l join questions q on q.listening_id=l.id order by l.id limit 1').fetchone()
            d=user(root/'user.sqlite',10);snapshot=json.dumps(dict(item_id=lid,question_id=qid,heard=True,selected='b',position=2,retry=[1],revision=8,contentVersion=24,order=['a','b']))
            d.execute(query('SQLiteListening','INSERT INTO listening_sessions'),['existing','practice:lower_intermediate:10',snapshot,0])
            d.execute("insert into srs_state values(?,'listening','calendar_steps',1,'{\"stage\":3}',100,90,90)",[lid]);d.execute("insert into user_metadata values('opaque','preserved')");d.commit()
            tables=[r[0] for r in d.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'")];before={t:d.execute('select * from '+t).fetchall() for t in tables};d.close()
            shutil.copyfile(BUNDLE,active);d=sqlite3.connect(root/'user.sqlite')
            self.assertEqual(before,{t:d.execute('select * from '+t).fetchall() for t in tables});d.close()
            with sqlite3.connect(active) as c:self.assertIsNotNone(c.execute('select id from questions where id=?',[qid]).fetchone())

    def test_self_review_covers_every_item_choice_and_answer_without_recording_claim(self):
        review=json.loads((ROOT/'Docs/DATA10_A_SELF_REVIEW.json').read_text())
        self.assertEqual({r['example_id'] for r in review['items']},{r['example_id'] for r in self.items});self.assertEqual(review['scope'],dict(originals=60,translations=60,questions=120,choices=270,accepted_answers=30))
        self.assertTrue(all(r['result']=='AI_SELF_REVIEWED' for r in review['items']))
        self.assertTrue(all(s['task']!='dictation' or len(r['korean'])<=100 for r in self.items for s in r['tasks']))
