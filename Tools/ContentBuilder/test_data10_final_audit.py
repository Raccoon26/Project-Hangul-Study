"""DATA10 QA exact delta, UI source gates and on-disk SQL contracts, not iOS execution."""
import re,collections,copy,gzip,hashlib,json,os,random,shutil,socket,sqlite3,subprocess,tempfile,unittest,unicodedata
from pathlib import Path
from unittest.mock import patch
from build_content import ROOT,build
from validator import signatures,ValidationError
from prepare_data10_final import prepare,BASE_SHA
from audit_data10_final import audit,registries,view_contract,norm
from test_data05_content import query
from test_lookup_sql import user
SOURCE=Path(os.environ.get('DATA10_QA_SOURCE',ROOT/'Tests/Fixtures/content-v28-production.json.gz'))
BUNDLE=Path(os.environ.get('DATA10_QA_BUNDLE',ROOT/'Tests/Fixtures/content-v28-production.sqlite'))
class Data10FinalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global SOURCE
        cls.released_source=tempfile.TemporaryDirectory()
        if SOURCE.suffix=='.gz':
            raw=gzip.decompress(SOURCE.read_bytes());SOURCE=Path(cls.released_source.name)/'content28.json';SOURCE.write_bytes(raw)
        cls.src=json.loads(SOURCE.read_text());cls.t=cls.src['tables'];cls.items=registries();cls.by={r['key']:r for r in cls.items};cls.e={r['id']:r for r in cls.t['examples']};cls.q={r['id']:r for r in cls.t['questions']}
        cls.oldsrc=json.loads(gzip.decompress((ROOT/'Tests/Fixtures/content-v27-production.json.gz').read_bytes()));cls.db=sqlite3.connect(BUNDLE);cls.old=sqlite3.connect(ROOT/'Tests/Fixtures/content-v27-production.sqlite');cls.manifest=json.loads((ROOT/'Content/data10-final-corrections.json').read_text());cls.revised=set(json.loads((ROOT/'Content/data10-final-revised-ids.json').read_text()))
    @classmethod
    def tearDownClass(cls):cls.db.close();cls.old.close();cls.released_source.cleanup()
    def test_frozen27_and_deterministic_strict28_byte_reconstruction(self):
        self.assertEqual(hashlib.sha256(gzip.decompress((ROOT/'Tests/Fixtures/content-v27-production.json.gz').read_bytes())).hexdigest(),BASE_SHA)
        self.assertEqual(hashlib.sha256((ROOT/'Tests/Fixtures/content-v27-production.sqlite').read_bytes()).hexdigest(),'a937df17bfb88b69504811048c2660086af174dc7633d04f852a3ce10236b48c')
        with tempfile.TemporaryDirectory()as d:
            p=Path(d);s=p/'s.json';rev=p/'r.json';out=p/'c.sqlite';prepare(s,rev);self.assertEqual(s.read_bytes(),SOURCE.read_bytes());self.assertEqual(set(json.loads(rev.read_text())),self.revised)
            r=build(s,out,ROOT/'Tests/Fixtures/content-v27-production.sqlite',production=True);self.assertEqual((r['validation']['error_count'],r['validation']['warning_count']),(0,10));self.assertEqual(out.read_bytes(),BUNDLE.read_bytes())
    def test_exact_all188_fields179_revisions_and_no_insert_delete_or_membership_change(self):
        s=copy.deepcopy(self.oldsrc);owners=set()
        for p in self.manifest['patches']:
            r=next(r for r in s['tables'][p['table']]if all(r[k]==v for k,v in p['key'].items()));self.assertEqual(r[p['field']],p['before']);r[p['field']]=p['after'];owners.add(p['key'].get('id',p['key'].get('question_id')))
        for r in s['tables']['content_items']:
            if r['id']in self.revised:r['revision']+=1;r['updated_at']=self.manifest['updated_at']
        s['metadata']['content_version']=28;self.assertEqual(s,self.src);self.assertEqual(len(self.manifest['patches']),188);self.assertEqual(len(owners),175);self.assertEqual(len(self.revised),179)
        a,b=signatures(self.old),signatures(self.db);self.assertEqual(a.keys(),b.keys());self.assertEqual({i for i in a if a[i]!=b[i]},owners);self.assertEqual(len(self.revised-owners),4)
        for t in self.t:self.assertEqual(len(self.t[t]),len(self.oldsrc['tables'][t]),t)
        for t in ('content_links','lesson_items','grammar_examples','vocabulary_examples','item_sources'):self.assertEqual(self.t[t],self.oldsrc['tables'][t])
    def test_all180_scripts360_questions630_choices150_accepted_and_sql_source_integrity(self):
        r,_=audit(SOURCE,BUNDLE);self.assertEqual(r['cohort'],dict(originals=180,listening=360,questions=360,choices=630,accepted=150,tasks=dict(comprehension=180,dictation=150,meaning=18,korean=12)))
        self.assertEqual((r['metadata']['content_version'],r['metadata']['schema_version'],r['metadata']['min_reader_version']),(28,4,7));self.assertEqual(r['integrity'],[('ok',)]);self.assertFalse(r['foreign_keys']);self.assertEqual(r['total_source_rows'],69787)
        reviewed_ja={self.e[x['example_id']]['japanese']for x in self.items}
        for x in self.items:
            for z in x['tasks']:
                before=self.old.execute('SELECT answer_json FROM questions WHERE id=?',[z['question_id']]).fetchone()[0];after=self.q[z['question_id']]['answer_json']
                if z['task']!='dictation':self.assertEqual(json.loads(before),json.loads(after))
                if z['task']=='meaning':self.assertTrue({v for v, in self.db.execute('SELECT text FROM question_choices WHERE question_id=?',[z['question_id']])}<=reviewed_ja)
    def test_cancellation_recipient_passive_tendency_and_stale_surface_regressions(self):
        ex=lambda k:self.e[self.by[k]['example_id']]
        self.assertIn('約束そのものを取りやめる代わりに',ex('A13')['japanese']);self.assertIn('日時を変えて会う',ex('A13')['learning_point_ja']);self.assertIn('돌아가도',ex('A23')['korean']);self.assertNotIn('돌아가더라도',ex('A23')['korean'])
        self.assertNotIn('二人',self.q[self.by['A27']['tasks'][0]['question_id']]['prompt_ja']);self.assertIn('형에게 부모님께도',ex('B06')['korean']);self.assertIn('どちらかというと',ex('B21')['japanese']);self.assertNotIn('合うようです',ex('B21')['japanese'])
        self.assertIn('하고 싶냐고',ex('B53')['learning_point_ja']);self.assertNotIn('싶으냐고',ex('B53')['learning_point_ja']);self.assertIn('바로 반대하는 대신',ex('B56')['korean']);self.assertIn('私はその同僚を手伝うように言われた',ex('B57')['japanese']);self.assertNotIn('責める',ex('B57')['learning_point_ja'])
        qid=self.by['B30']['tasks'][0]['question_id'];a=json.loads(self.q[qid]['answer_json']);self.assertEqual(self.db.execute('SELECT text FROM question_choices WHERE question_id=? AND choice_id=?',[qid,a['correct_choice_ids'][0]]).fetchone()[0],'安全を優先し、床が乾くのを待つよう案内されたから')
    def test_all_dictations_exact_orthography_and_internal_punctuation_not_broadened(self):
        # Corpus-side equivalent only; actual Swift judge is separately native BLOCKED here.
        canon=lambda s:norm(s).rstrip('.!?');count=0
        for r in self.items:
            text=self.e[r['example_id']]['korean']
            for task in r['tasks']:
                if task['task']!='dictation':continue
                q=self.q[task['question_id']];self.assertEqual(json.loads(q['answer_json']),dict(accepted=[text]));self.assertIn('数字もハングルで書いてください',q['prompt_ja']);self.assertIn('文末の「.」「!」「?」は省略できます',q['prompt_ja']);count+=1
                self.assertEqual(canon(text),canon(text.rstrip('.!?')));self.assertNotEqual(canon(text),canon(re.sub(r'[.!?](?=\s)',',',text,count=1)));self.assertNotEqual(canon(text),canon(text+'틀린 내용'))
        self.assertEqual(count,150)
        engine=(ROOT/'LearningEngine/ConjugationEngine.swift').read_text();self.assertIn('while let last = text.last, ".!?".contains(last)',engine);self.assertIn('task == .dictation ? ProductionAnswer.judgeDictation',(ROOT/'Models/ListeningModels.swift').read_text())
    def test_ui_choices_and_accessibility_text_require_saved_completed_playback(self):
        ui=(ROOT/'Views/ListeningView.swift').read_text();model=(ROOT/'Models/ListeningModels.swift').read_text();view_contract(ui,model)
        before=subprocess.check_output(['git','show','f7d1835a8ce1b073a65e8a21d8b27f6e4eb523a9:Views/ListeningView.swift'],cwd=ROOT,text=True)
        with self.assertRaises((AssertionError,ValueError)):view_contract(before,model)
        for bad in (ui.replace('else if s.revealsChoices {','else {'),ui.replace('else if s.revealsChoices {','else if true {')):
            with self.assertRaises((AssertionError,ValueError)):view_contract(bad,model)
        self.assertIn('if success { self.completedPlaybackCount += 1 }',(ROOT/'Services/KoreanAudioService.swift').read_text());self.assertIn('testDATA10ChoicesWaitForCompletedPlaybackAndSurviveResume',(ROOT/'Tests/ListeningTests.swift').read_text())
    def test_validator_still_rejects_numeric_synonym_leaks_duplicate_choices_and_bad_revision(self):
        with tempfile.TemporaryDirectory()as d:
            for case in ('numeric','synonym','leak','duplicate','revision'):
                s=copy.deepcopy(self.src);r=self.by['A11'];q=next(q for q in s['tables']['questions']if q['id']==r['tasks'][1]['question_id']);text=self.e[r['example_id']]['korean']
                if case=='numeric':q['answer_json']=json.dumps(dict(accepted=[text,text.replace('두 시','2시')]),ensure_ascii=False)
                elif case=='synonym':q['answer_json']=json.dumps(dict(accepted=[text,'같은 뜻입니다.']),ensure_ascii=False)
                elif case=='leak':q['prompt_ko']=text
                elif case=='duplicate':
                    cid=r['tasks'][0]['question_id'];cc=[x for x in s['tables']['question_choices']if x['question_id']==cid];cc[1]['text']=cc[0]['text']
                else:
                    i=next(iter(self.revised));next(x for x in s['tables']['content_items']if x['id']==i)['revision']=self.old.execute('SELECT revision FROM content_items WHERE id=?',[i]).fetchone()[0]
                p=Path(d)/'bad.json';p.write_text(json.dumps(s,ensure_ascii=False))
                with self.subTest(case=case),self.assertRaises(ValidationError):build(p,Path(d)/'bad.sqlite',ROOT/'Tests/Fixtures/content-v27-production.sqlite',production=True)
    def test_old1936_all_three_kinds_unchanged_and_distribution_limitations_honest(self):
        old24=sqlite3.connect(ROOT/'Tests/Fixtures/content-v24-production.sqlite');a,b=signatures(self.old),signatures(self.db)
        for t,col in [('listening_items','id'),('listening_items','source_example_id'),('questions','id')]:
            sql='SELECT '+col+' FROM '+t+(' WHERE listening_id IS NOT NULL'if t=='questions'else'')
            for i, in old24.execute(sql):self.assertEqual(a[i],b[i]);self.assertNotIn(i,self.revised)
        old24.close();r=json.loads((ROOT/'Docs/DATA10_QA_CORPUS_ANALYSIS.json').read_text());self.assertEqual(r['baseline24']['listening'],1936);self.assertEqual(r['baseline24']['tasks']['dictation'],1850);self.assertEqual(r['combined28']['tasks']['dictation'],2000);self.assertEqual(r['combined28']['source_ids'],2116);self.assertEqual(r['verified_recordings'],0);self.assertFalse(r['new_source_complete_korean_duplicates_vs_old'])
    def test_disk_update_preserves_old_b06_snapshot_due_favorites_and_all_user_bytes(self):
        with tempfile.TemporaryDirectory()as d:
            p=Path(d);content=p/'content.sqlite';up=p/'user.sqlite';shutil.copyfile(ROOT/'Tests/Fixtures/content-v27-production.sqlite',content);u=user(up,10);r=self.by['B06'];lid,qid=r['tasks'][1]['listening_id'],r['tasks'][1]['question_id'];oldtext=self.old.execute('SELECT korean FROM examples WHERE id=?',[r['example_id']]).fetchone()[0]
            payload=json.dumps(dict(questions=[dict(id=qid,itemID=lid,transcript=oldtext,accepted=[oldtext])],heard=True,answer=oldtext,result='correct',contentVersion=27,revision=7,position=0,order=['c','a','b']))
            u.execute(query('SQLiteListening','INSERT INTO listening_sessions'),['active','practice:lower_intermediate:112',payload,0]);u.execute("INSERT INTO srs_state VALUES(?,'listening','calendar_steps',1,'{\"stage\":3}',123,90,90)",[lid]);u.execute("INSERT INTO favorites(content_id,created_at,content_type)VALUES(?,100,'vocabulary')",[self.old.execute('SELECT id FROM vocabulary ORDER BY id LIMIT 1').fetchone()[0]]);u.execute("INSERT INTO user_metadata VALUES('settings-opaque','keep')");u.commit();u.close();before=up.read_bytes();shutil.copyfile(BUNDLE,content);self.assertEqual(before,up.read_bytes())
            with sqlite3.connect(up)as u:self.assertEqual(u.execute('SELECT state_json FROM listening_sessions').fetchone()[0],payload)
            with sqlite3.connect(content)as c:self.assertNotEqual(c.execute('SELECT korean FROM examples WHERE id=?',[r['example_id']]).fetchone()[0],oldtext);self.assertIsNotNone(c.execute('SELECT id FROM listening_items WHERE id=?',[lid]).fetchone())
    def test_offline_actual_catalog_sql_all360_in_bounded20_pages(self):
        seen=set();q=query('SQLiteListening','SELECT q.*,l.id')
        with patch.object(socket,'socket',side_effect=AssertionError('offline')):
            for batch in range(103,121):
                ids=[x[0]for x in self.db.execute(query('SQLiteListening','SELECT l.id FROM listening_items'),['lower_intermediate',batch*20,(batch+1)*20])];self.assertEqual(len(ids),20)
                rows=self.db.execute(q+' AND l.id IN ('+','.join('?'for _ in ids)+') ORDER BY l.learning_order,l.id LIMIT20'.replace('LIMIT20','LIMIT 20'),ids).fetchall();self.assertEqual(len(rows),20);seen.update(ids)
        self.assertEqual(seen,{q['listening_id']for r in self.items for q in r['tasks']})
    def test_all180_prerequisite_receipts_and54_prior_observations_are_not_full_mastery(self):
        r=json.loads((ROOT/'Docs/DATA10_QA_PREREQUISITES.json').read_text());self.assertEqual(len(r['selected_records']),180);self.assertEqual({x['example_id']for x in r['selected_records']},{x['example_id']for x in self.items})
        for x in r['selected_records']:
            self.assertIn(x['observed_form_ko'],self.e[x['example_id']]['korean']);self.assertEqual(self.db.execute('SELECT pattern FROM grammar WHERE id=?',[x['grammar_id']]).fetchone()[0],x['pattern']);self.assertIn(x['grammar_level'],['intro','beginner','lower_intermediate'])
        self.assertEqual(len(r['surface_families_requiring_preview']),12);self.assertEqual(len({k for x in r['surface_families_requiring_preview']for k in x['item_keys']}),27);self.assertEqual(r['old163_unchanged']['unresolved'],36)
        for x in json.loads((ROOT/'Docs/DATA10_B_GRAMMAR_REUSE.json').read_text())['records']:self.assertIn(x['observed_form_ko'],self.e[x['example_id']]['korean'])
    def test_editorial_payload_receipts_sampling_and_human_audio_not_tested(self):
        r=json.loads((ROOT/'Docs/DATA10_QA_EDITORIAL.json').read_text());self.assertEqual(r['scope'],dict(originals=180,translations=180,questions=360,choices=630,accepted_answers=150));self.assertEqual(r['independent_human_review'],'NOT TESTED');self.assertEqual(r['actual_tts_audition'],'NOT TESTED');self.assertEqual(len(r['rows']),180);self.assertFalse(r['prompt_exact_leak_candidates'])
        for x in r['rows']:self.assertEqual(x['source_sha256'],hashlib.sha256(json.dumps(self.e[x['example_id']],ensure_ascii=False,sort_keys=True).encode()).hexdigest())
        sample=json.loads((ROOT/'Docs/DATA10_QA_SAMPLES.json').read_text());rng=random.Random(20261021105);expected=[r['key']for b in 'ABC'for r in rng.sample([x for x in self.items if x['key'].startswith(b)],6)];self.assertEqual([r['key']for r in sample['records']],expected)
        old=json.loads((ROOT/'Docs/DATA10_QA_OLD_SAMPLES.json').read_text());self.assertEqual(len(old['old_samples']),12);self.assertEqual(len(old['near10']),4);self.assertEqual(old['old_listening_sources_in_prior163'],163)
