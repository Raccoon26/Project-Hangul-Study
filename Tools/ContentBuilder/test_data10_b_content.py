"""Strict DATA10-B25->26, corpus and SQLite contracts, not native/audio execution."""
import collections,copy,gzip,hashlib,json,os,shutil,socket,sqlite3,tempfile,unittest,uuid,unicodedata
from pathlib import Path
from unittest.mock import patch
from build_content import ROOT,build
from prepare_data10_b import prepare,BASE_SHA
from validator import signatures,ValidationError
from test_data05_content import query
from test_lookup_sql import user
SOURCE=Path(os.environ.get('DATA10_B_SOURCE',ROOT/'Content/production.json'))
BUNDLE=Path(os.environ.get('DATA10_B_BUNDLE',ROOT/'Resources/content.sqlite'))
norm=lambda s:' '.join(unicodedata.normalize('NFC',s).split())
compact=lambda s:''.join(norm(s).split()).rstrip('.!?')

class Data10BTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=json.loads(SOURCE.read_text());cls.t=cls.source['tables'];cls.items=json.loads((ROOT/'Content/data10-b-authoring.json').read_text())['items']
        cls.db=sqlite3.connect(BUNDLE);cls.old=sqlite3.connect(ROOT/'Tests/Fixtures/content-v25-production.sqlite')
    @classmethod
    def tearDownClass(cls):cls.db.close();cls.old.close()

    def test_frozen25_and_deterministic26_strict_reconstruction(self):
        self.assertEqual(hashlib.sha256(gzip.decompress((ROOT/'Tests/Fixtures/content-v25-production.json.gz').read_bytes())).hexdigest(),BASE_SHA)
        self.assertEqual(hashlib.sha256((ROOT/'Tests/Fixtures/content-v25-production.sqlite').read_bytes()).hexdigest(),'01652666fc34cbc2d69a2d8a82f8aca778b20045b629df7d8623ee3e87a64500')
        with tempfile.TemporaryDirectory() as folder:
            src=Path(folder)/'s.json';rev=Path(folder)/'r.json';out=Path(folder)/'out.sqlite';prepare(src,rev)
            self.assertEqual(src.read_bytes(),SOURCE.read_bytes());self.assertEqual(json.loads(rev.read_text()),[])
            r=build(src,out,ROOT/'Tests/Fixtures/content-v25-production.sqlite',production=True)
            self.assertEqual((r['validation']['error_count'],r['validation']['warning_count']),(0,10));self.assertEqual(out.read_bytes(),BUNDLE.read_bytes())

    def test_every_old_payload_revision_membership_and_exact300_new_ids(self):
        old=json.loads(gzip.decompress((ROOT/'Tests/Fixtures/content-v25-production.json.gz').read_bytes()))
        for t,rows in old['tables'].items():self.assertEqual(self.t[t][:len(rows)],rows,t)
        a,b=signatures(self.old),signatures(self.db)
        self.assertTrue(a.keys()<=b.keys());self.assertEqual({i for i in a if a[i]!=b[i]},set())
        ids={r['example_id'] for r in self.items}|{s[k] for r in self.items for s in r['tasks'] for k in ('listening_id','question_id')}
        self.assertEqual(set(b)-set(a),ids);self.assertEqual(len(ids),300)
        for i in ids:self.assertEqual(str(uuid.UUID(i)),i)
        for t in self.t:self.assertFalse(collections.Counter(self.old.execute('SELECT * FROM '+t))-collections.Counter(self.db.execute('SELECT * FROM '+t)),t)
        sql='SELECT type,name,tbl_name,sql FROM sqlite_master ORDER BY type,name';self.assertEqual(self.old.execute(sql).fetchall(),self.db.execute(sql).fetchall())

    def test_full_source_database_rows_counts_and_integrity(self):
        self.assertEqual(self.db.execute('SELECT schema_version,content_version,min_reader_version FROM content_metadata').fetchone(),(4,26,7))
        for t,rows in self.t.items():
            keys=sorted(rows[0]) if rows else [r[1] for r in self.db.execute('PRAGMA table_info('+t+')')]
            self.assertEqual(collections.Counter(self.db.execute('SELECT '+','.join('"'+k+'"' for k in keys)+' FROM '+t)),collections.Counter(tuple(r.get(k) for k in keys) for r in rows),t)
        for t,n in [('examples',4933),('listening_items',2176),('questions',3793),('content_items',16541),('vocabulary',2287),('meanings',2420),('grammar',96)]:self.assertEqual(self.db.execute('SELECT COUNT(*) FROM '+t).fetchone()[0],n)
        self.assertEqual(self.db.execute('PRAGMA integrity_check').fetchall(),[('ok',)]);self.assertEqual(self.db.execute('PRAGMA foreign_key_check').fetchall(),[])

    def test_60_novel_situations_domains_and54_grammar_context_occurrences(self):
        known={compact(k) for k, in self.old.execute('SELECT korean FROM examples')};seen=set()
        for r in self.items:
            k=compact(r['korean']);self.assertNotIn(k,known);self.assertNotIn(k,seen);seen.add(k)
            self.assertLessEqual(len(r['korean']),100);self.assertGreaterEqual(sum(r['korean'].count(c) for c in '.!?'),2)
        self.assertEqual(len(seen),60);self.assertEqual(collections.Counter(r['domain'] for r in self.items),dict(emotions=8,opinion=8,judgment=7,reason=7,result=7,experience=8,plan=8,disagreement=7))
        evidence=json.loads((ROOT/'Docs/DATA10_B_GRAMMAR_REUSE.json').read_text())['records'];self.assertEqual(len(evidence),54);self.assertEqual(len({r['grammar_id'] for r in evidence}),54)
        by={r['example_id']:r for r in self.items}
        for r in evidence:
            self.assertIn(r['observed_form_ko'],by[r['example_id']]['korean']);self.assertEqual(self.db.execute('SELECT pattern FROM grammar WHERE id=?',[r['grammar_id']]).fetchone()[0],r['pattern'])
        self.assertGreaterEqual(len({r['listening_focus'] for r in self.items}),8)

    def test_questions_unique_answer_individual_wrong_feedback_and_exact_dictation(self):
        tasks=collections.Counter();positions=collections.Counter()
        for r in self.items:
            for s in r['tasks']:
                kind,ko,answer,rubric,feedback=self.db.execute('SELECT question_type,prompt_ko,answer_json,rubric_json,explanation_ja FROM questions WHERE id=?',[s['question_id']]).fetchone();self.assertIsNone(ko)
                task=json.loads(rubric)['listening_task'];tasks[task]+=1;a=json.loads(answer)
                choices=self.db.execute('SELECT choice_id,text FROM question_choices WHERE question_id=? ORDER BY ordinal',[s['question_id']]).fetchall()
                if task=='dictation':self.assertEqual((kind,a,choices),('listening_input',dict(accepted=[r['korean']]),[]))
                else:
                    self.assertEqual(kind,'listening_choice');self.assertEqual(len(choices),3);self.assertEqual(len({norm(t) for _,t in choices}),3)
                    self.assertEqual(len(a['correct_choice_ids']),1);cid=a['correct_choice_ids'][0];positions[cid]+=1;self.assertEqual(dict(choices)[cid],s['correct']);self.assertIn(s['correct_evidence_ko'],r['korean'])
                    for text,why in zip(s['distractors'],s['distractor_explanations_ja']):self.assertIn(text,feedback);self.assertIn(why,feedback)
        self.assertEqual(tasks,dict(comprehension=60,dictation=60));self.assertEqual(positions,dict(a=20,b=20,c=20))

    def test_real_offline_sql_pages120_ids_and_no_repeated_source_within_page(self):
        seen=set();sources=collections.Counter();q=query('SQLiteListening','SELECT q.*,l.id')
        with patch.object(socket,'socket',side_effect=AssertionError('offline')):
            for batch in range(109,115):
                ids=[x[0] for x in self.db.execute(query('SQLiteListening','SELECT l.id FROM listening_items'),['lower_intermediate',batch*20,(batch+1)*20])];self.assertEqual(len(ids),20)
                cur=self.db.execute(q+' AND l.id IN ('+','.join('?' for _ in ids)+') ORDER BY l.learning_order,l.id LIMIT 20',ids);cols=[x[0] for x in cur.description];rows=[dict(zip(cols,x)) for x in cur]
                self.assertEqual(len({x['source_example_id'] for x in rows}),20)
                for x in rows:self.assertEqual(x['audio_mode'],'tts');seen.add(x['id']);sources[x['source_example_id']]+=1
        self.assertEqual(seen,{s['question_id'] for r in self.items for s in r['tasks']});self.assertEqual(len(sources),60);self.assertEqual(set(sources.values()),{2})
        for r in self.items:
            batches=[self.db.execute('SELECT learning_order/20 FROM listening_items WHERE id=?',[s['listening_id']]).fetchone()[0] for s in r['tasks']];self.assertEqual(batches[1]-batches[0],3)

    def test_upgrade_keeps_batch_a_snapshot_due_and_all_user_tables(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder);active=p/'content.sqlite';shutil.copyfile(ROOT/'Tests/Fixtures/content-v25-production.sqlite',active)
            a=json.loads((ROOT/'Content/data10-a-authoring.json').read_text())['items'][0];lid,qid=a['tasks'][0]['listening_id'],a['tasks'][0]['question_id']
            d=user(p/'user.sqlite',10);payload=json.dumps(dict(item_id=lid,question_id=qid,heard=True,selected='b',position=2,retry=[1],revision=8,contentVersion=25,order=['a','b']))
            d.execute(query('SQLiteListening','INSERT INTO listening_sessions'),['active','practice:lower_intermediate:103',payload,0]);d.execute("INSERT INTO srs_state VALUES(?,'listening','calendar_steps',1,'{\"stage\":3}',100,90,90)",[lid])
            d.execute("INSERT INTO user_metadata VALUES('settings-opaque','keep')");d.commit();tables=[x[0] for x in d.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")];before={t:d.execute('SELECT * FROM '+t).fetchall() for t in tables};d.close()
            shutil.copyfile(BUNDLE,active);d=sqlite3.connect(p/'user.sqlite');self.assertEqual(before,{t:d.execute('SELECT * FROM '+t).fetchall() for t in tables});d.close()
            with sqlite3.connect(active) as c:self.assertIsNotNone(c.execute('SELECT id FROM questions WHERE id=?',[qid]).fetchone())

    def test_review_transcript_release_tts_and_narrow_dictation_contract(self):
        review=json.loads((ROOT/'Docs/DATA10_B_SELF_REVIEW.json').read_text());self.assertEqual(review['scope'],dict(originals=60,translations=60,questions=120,choices=180,accepted_answers=60));self.assertEqual({r['example_id'] for r in review['items']},{r['example_id'] for r in self.items});self.assertTrue(all(r['result']=='AI_SELF_REVIEWED' for r in review['items']))
        # Python corpus expectation only; Swift judge uses a separately BLOCKED native method.
        sentence=lambda s:norm(s).rstrip('.!?')
        for r in self.items:
            self.assertEqual(sentence(r['korean']),sentence(r['korean'].rstrip('.!?')));self.assertNotEqual(sentence(r['korean']+'틀린 내용'),sentence(r['korean']))
            if '. ' in r['korean']:self.assertNotEqual(sentence(r['korean'].replace('. ', ', ',1)),sentence(r['korean']))
            for s in r['tasks']:self.assertEqual(self.db.execute('SELECT audio_asset_id,transcript_ko FROM listening_items WHERE id=?',[s['listening_id']]).fetchone(),(None,None))
        ui=(ROOT/'Views/ListeningView.swift').read_text();self.assertLess(ui.index('else if let result = s.result'),ui.index('Text(q.transcript)'))
        self.assertIn('task == .dictation ? ProductionAnswer.judgeDictation',(ROOT/'Models/ListeningModels.swift').read_text());self.assertIn('testDATA10BBatchAll120QuestionsUseRealGradingAndPlayedGate',(ROOT/'Tests/ListeningTests.swift').read_text())

    def test_validator_rejects_bad_accepted_leaked_transcript_and_missing_example(self):
        with tempfile.TemporaryDirectory() as folder:
            for case in ('accepted','leak','missing'):
                s=copy.deepcopy(self.source);r=self.items[0];q=next(q for q in s['tables']['questions'] if q['id']==r['tasks'][1]['question_id'])
                if case=='accepted':q['answer_json']=json.dumps(dict(accepted=['다른 내용입니다.']))
                elif case=='leak':q['prompt_ko']=r['korean']
                else:next(l for l in s['tables']['listening_items'] if l['id']==r['tasks'][0]['listening_id'])['source_example_id']='00000000-0000-4000-8000-000000000000'
                p=Path(folder)/'bad.json';p.write_text(json.dumps(s,ensure_ascii=False))
                with self.subTest(case=case),self.assertRaises(ValidationError):build(p,Path(folder)/'bad.sqlite',ROOT/'Tests/Fixtures/content-v25-production.sqlite',production=True)
