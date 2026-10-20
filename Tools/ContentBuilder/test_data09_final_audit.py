"""DATA09-5 exact editorial delta, content contracts and on-disk preservation; no native claims."""
import collections
import copy
import gzip
import hashlib
import json
import os
import random
import shutil
import sqlite3
import tempfile
import unittest
from pathlib import Path
from build_content import ROOT, build
from validator import ValidationError, signatures
from prepare_data09_final import prepare, BASE_SHA
from audit_data09_final import audit, registries
from test_lookup_sql import user
from test_data05_content import query

SOURCE=Path(os.environ.get('DATA09_FINAL_SOURCE',ROOT/'Tests/Fixtures/content-v23-production.json.gz'))
BUNDLE=Path(os.environ.get('DATA09_FINAL_BUNDLE',ROOT/'Tests/Fixtures/content-v23-production.sqlite'))


class Data09FinalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global SOURCE
        cls.released_source=tempfile.TemporaryDirectory()
        if SOURCE.suffix=='.gz':
            raw=gzip.decompress(SOURCE.read_bytes());SOURCE=Path(cls.released_source.name)/'content23.json';SOURCE.write_bytes(raw)
        cls.source=json.loads(SOURCE.read_text())
        cls.old_source=json.loads(gzip.decompress((ROOT/'Tests/Fixtures/content-v22-production.json.gz').read_bytes()))
        cls.db=sqlite3.connect(BUNDLE);cls.old=sqlite3.connect(ROOT/'Tests/Fixtures/content-v22-production.sqlite')
        cls.manifest=json.loads((ROOT/'Content/data09-final-corrections.json').read_text())
        cls.reg={r['key']:r for r in registries()}
        cls.revised=set(json.loads((ROOT/'Content/data09-final-revised-ids.json').read_text()))
    @classmethod
    def tearDownClass(cls):cls.db.close();cls.old.close();cls.released_source.cleanup()

    def test_immutable22_and_deterministic_strict23_reconstruction(self):
        self.assertEqual(hashlib.sha256(gzip.decompress((ROOT/'Tests/Fixtures/content-v22-production.json.gz').read_bytes())).hexdigest(),BASE_SHA)
        self.assertEqual(hashlib.sha256((ROOT/'Tests/Fixtures/content-v22-production.sqlite').read_bytes()).hexdigest(),'22c3257b4204309158dfdea0f0bfd7d870fa0c540bd21ee7f240673df052e0f4')
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'source.json';revised=Path(folder)/'revised.json';out=Path(folder)/'content.sqlite'
            prepare(source,revised)
            self.assertEqual(source.read_bytes(),SOURCE.read_bytes());self.assertEqual(set(json.loads(revised.read_text())),self.revised)
            report=build(source,out,ROOT/'Tests/Fixtures/content-v22-production.sqlite',production=True)
            self.assertEqual((report['validation']['error_count'],report['validation']['warning_count']),(0,10))
            self.assertEqual(out.read_bytes(),BUNDLE.read_bytes())

    def test_exact22_id_revision_and_approved_payload_delta_only(self):
        self.assertEqual(self.db.execute('SELECT schema_version,content_version,min_reader_version,is_fixture FROM content_metadata').fetchone(),(4,23,7,0))
        before,after=signatures(self.old),signatures(self.db)
        self.assertEqual(before.keys(),after.keys());self.assertEqual({i for i in before if before[i]!=after[i]},self.revised);self.assertEqual(len(self.revised),25)
        expected=copy.deepcopy(self.old_source)
        for p in self.manifest['patches']:
            r=next(r for r in expected['tables'][p['table']] if all(r[k]==v for k,v in p['key'].items()))
            self.assertEqual(r[p['field']],p['before']);r[p['field']]=p['after']
        for r in expected['tables']['content_items']:
            if r['id'] in self.revised:r['revision']+=1;r['updated_at']=self.manifest['updated_at']
        expected['metadata']['content_version']=23
        self.assertEqual(expected,self.source)
        # Full DB rows, including derived tables, are checked by strict reconstruction above.
        self.assertEqual(self.db.execute('PRAGMA integrity_check').fetchall(),[('ok',)])
        self.assertEqual(self.db.execute('PRAGMA foreign_key_check').fetchall(),[])

    def test_all_cohort_counts_choices_duplicates_and_input_contracts(self):
        report=audit(self.source);self.assertEqual(report['validation']['errors'],[])
        self.assertEqual(report['cohort'],dict(grammar=54,new_examples=216,questions=216,choices=648,new_direct_input=0))
        self.assertEqual(report['existing_input_contracts'],dict(text_input=1227,listening_input=1850))
        for table in self.old_source['tables']:
            self.assertEqual(len(self.source['tables'][table]),len(self.old_source['tables'][table]),table)
        for table,n in [('grammar',96),('examples',4813),('questions',3553),('vocabulary',2287)]:self.assertEqual(self.db.execute('SELECT COUNT(*) FROM '+table).fetchone()[0],n)

    def test_known_causal_tense_aspect_and_context_regressions(self):
        def grammar(key,field):return self.db.execute('SELECT '+field+' FROM grammar WHERE id=?',(self.reg[key]['id'],)).fetchone()[0]
        def question(key,n,field):return self.db.execute('SELECT '+field+' FROM questions WHERE id=?',(self.reg[key]['question_ids'][n-1],)).fetchone()[0]
        self.assertIn('一般的・反復的',grammar('A17','confusion_ja'))
        self.assertIn('必ず過去の事実だけとは限りません',grammar('A08','confusion_ja'))
        self.assertIn('主節の時制だけで決めず',grammar('B01','usage_constraints_ja'))
        self.assertIn('結果継続',grammar('B06','confusion_ja'));self.assertIn('今ドアを開ける動作',question('B06',4,'prompt_ja'))
        self.assertIn('들다＋려면',question('A09',2,'explanation_ja'))
        self.assertIn('지금 자는 것 같아요',question('B16',4,'prompt_ja'))
        self.assertNotIn('会議が長引いたこと',question('A01',3,'explanation_ja'))
        self.assertNotIn('P25',grammar('C05','confusion_ja'))

    def test_sibling_gender_context_is_visible_in_standalone_questions(self):
        for key,n in [('B03',3),('C11',1),('C11',3)]:
            qid=self.reg[key]['question_ids'][n-1]
            prompt=self.db.execute('SELECT prompt_ja FROM questions WHERE id=?',(qid,)).fetchone()[0]
            self.assertIn('この問題の동생は弟を指す場面です。',prompt)

    def test_no_answer_or_choice_id_change_to_inflight_questions(self):
        for r in self.reg.values():
            for qid in r['question_ids']:
                self.assertEqual(self.db.execute('SELECT answer_json FROM questions WHERE id=?',(qid,)).fetchone(),self.old.execute('SELECT answer_json FROM questions WHERE id=?',(qid,)).fetchone())
                self.assertEqual(self.db.execute('SELECT choice_id,ordinal FROM question_choices WHERE question_id=? ORDER BY ordinal',(qid,)).fetchall(),self.old.execute('SELECT choice_id,ordinal FROM question_choices WHERE question_id=? ORDER BY ordinal',(qid,)).fetchall())
        # Spacing is intentionally the knowledge being tested, not a duplicate choice.
        qid=self.reg['C17']['question_ids'][1]
        self.assertEqual([r[0] for r in self.db.execute('SELECT text FROM question_choices WHERE question_id=? ORDER BY ordinal',(qid,))],['듣을수록','들을 수록','들을수록'])

    def test_final_audit_rejects_observed_bad_explanations_and_duplicate_choices(self):
        for case in ('scope','plan_id','choice','multiple','input'):
            s=copy.deepcopy(self.source);g=next(r for r in s['tables']['grammar'] if r['id']==self.reg['A17']['id'])
            if case=='scope':g['confusion_ja']='一回限りの条件-(으)면'
            if case=='plan_id':g['confusion_ja']='P25 editorial key'
            qid=self.reg['A01']['question_ids'][0]
            choices=[r for r in s['tables']['question_choices'] if r['question_id']==qid]
            if case=='choice':choices[1]['text']=choices[0]['text']
            if case=='multiple':next(r for r in s['tables']['questions'] if r['id']==qid)['answer_json']='{"correct_choice_ids":["a","b"]}'
            if case=='input':next(r for r in s['tables']['questions'] if r['question_type']=='text_input')['answer_json']='{"accepted":[""]}'
            with self.subTest(case=case):self.assertGreater(audit(s)['validation']['error_count'],0)

    def test_strict_gate_rejects_no_revision_and_bad_reference_and_input(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'bad.json'
            for case in ('revision','reference','input'):
                s=copy.deepcopy(self.source)
                if case=='revision':
                    i=next(iter(self.revised));next(r for r in s['tables']['content_items'] if r['id']==i)['revision']=self.old.execute('SELECT revision FROM content_items WHERE id=?',(i,)).fetchone()[0]
                elif case=='reference':s['tables']['grammar_examples'][0]['example_id']='00000000-0000-4000-8000-000000000000'
                else:next(r for r in s['tables']['questions'] if r['question_type']=='text_input')['answer_json']='{"accepted":[""]}'
                p.write_text(json.dumps(s,ensure_ascii=False))
                with self.subTest(case=case),self.assertRaises(ValidationError):build(p,Path(folder)/'bad.sqlite',ROOT/'Tests/Fixtures/content-v22-production.sqlite',production=True)

    def test_all163_decisions_preserve_original_text_and_do_not_claim_human_review(self):
        original=json.loads((ROOT/'Docs/DATA09_PREREQUISITE_AUDIT.json').read_text())['records']
        report=json.loads((ROOT/'Docs/DATA09_FINAL_PREREQUISITES.json').read_text());records=report['records']
        self.assertEqual(len(records),163);self.assertEqual(collections.Counter(r['status'] for r in records),dict(resolved=120,unresolved=36,pedagogically_allowable=7))
        for before,after in zip(original,records):
            for f in ('index','example_id','korean','japanese'):self.assertEqual(before[f],after[f])
            self.assertFalse(after['human_reviewed']);self.assertFalse(after['reuse_approved']);self.assertTrue(after['reason_ko'])
            if before['primary_category']=='level_mismatch_candidate':self.assertEqual(after['status'],'unresolved')
            for i in after['supporting_grammar_ids']:self.assertIsNotNone(self.db.execute('SELECT id FROM grammar WHERE id=?',(i,)).fetchone())
            self.assertEqual(self.db.execute('SELECT korean,japanese FROM examples WHERE id=?',(after['example_id'],)).fetchone(),(after['korean'],after['japanese']))
        for i in (33,77,120,139):self.assertEqual(records[i-1]['status'],'unresolved')

    def test_sample_draw_and_editorial_coverage_are_fixed_and_honest(self):
        report=json.loads((ROOT/'Docs/DATA09_FINAL_SAMPLES.json').read_text());rng=random.Random(20261020095);expected=[]
        for b in 'ABC':
            units=[g for key,g in self.reg.items() if key.startswith(b)]
            for table,ids in [('grammar',[g['id'] for g in units]),('examples',[i for g in units for i in g['example_ids']]),('questions',[i for g in units for i in g['question_ids']])]:
                expected.extend(dict(batch=b,table=table,id=i) for i in rng.sample(ids,3 if table=='grammar' else 6))
        self.assertEqual(report['records'],expected);self.assertEqual(len(expected),45)
        ledger=json.loads((ROOT/'Docs/DATA09_FINAL_EDITORIAL.json').read_text())
        self.assertEqual({r['key'] for r in ledger['records']},set(self.reg))
        self.assertTrue(all(r['independent_native_teacher_review']=='NOT TESTED' for r in ledger['records']))

    def test_disk22_to23_swap_preserves_srs_favorite_and_question_snapshot(self):
        with tempfile.TemporaryDirectory() as folder:
            active=Path(folder)/'content.sqlite';path=Path(folder)/'user.sqlite';shutil.copyfile(ROOT/'Tests/Fixtures/content-v22-production.sqlite',active)
            d=user(path,10);gid=self.reg['B06']['id'];qid=self.reg['B06']['question_ids'][3]
            snapshot=json.dumps(dict(ids=[gid],order=[gid],position=0,page=3,contentVersion=22,question_id=qid,selected='a',revision=8))
            d.execute("INSERT INTO srs_state VALUES(?,'grammar','calendar_steps',1,'{\"stage\":4}',900,NULL,100)",(gid,))
            d.execute("INSERT INTO favorites(content_id,created_at,content_type) VALUES(?,100,'grammar')",(gid,))
            d.execute("INSERT INTO grammar_sessions VALUES('active','old-lesson',?,8,'active',100)",(snapshot,));d.commit();d.close()
            sha=hashlib.sha256(path.read_bytes()).hexdigest();shutil.copyfile(BUNDLE,active)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),sha)
            d=sqlite3.connect(path);self.assertEqual(d.execute('SELECT state_json FROM grammar_sessions').fetchone()[0],snapshot)
            for _ in range(2):d.execute(query('SQLiteGrammarProgress','INSERT INTO srs_state('),[gid,'calendar_steps',1,'{"stage":0}',0,0])
            self.assertEqual(d.execute('SELECT state_json,due_at FROM srs_state').fetchall(),[('{"stage":4}',900)])
            self.assertEqual(d.execute('SELECT content_id FROM favorites').fetchall(),[(gid,)])
            with sqlite3.connect(active) as c:self.assertIsNotNone(c.execute(query('SQLiteGrammarContent','SELECT g.*,i.revision'),[gid]).fetchone())
            d.close()
