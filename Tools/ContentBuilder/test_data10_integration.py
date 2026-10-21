"""DATA10 actual-data integration/SQL tests. Swift/audio/device gates are separate."""
import collections,copy,gzip,hashlib,json,os,shutil,socket,sqlite3,subprocess,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from build_content import ROOT,build
from prepare_data10_integration import prepare,BASE_SHA
from audit_data10_integration import audit
from audit_data10_final import registries,view_contract
from test_data05_content import query
from test_lookup_sql import user
from validator import signatures,ValidationError

SOURCE=Path(os.environ.get('DATA10_INTEGRATION_SOURCE',ROOT/'Content/production.json'))
BUNDLE=Path(os.environ.get('DATA10_INTEGRATION_BUNDLE',ROOT/'Resources/content.sqlite'))


class Data10IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src=json.loads(SOURCE.read_text());cls.t=cls.src['tables'];cls.m=json.loads((ROOT/'Content/data10-integration-ids.json').read_text());cls.items=registries()
        cls.oldsrc=json.loads(gzip.decompress((ROOT/'Tests/Fixtures/content-v28-production.json.gz').read_bytes()));cls.db=sqlite3.connect(BUNDLE);cls.old=sqlite3.connect(ROOT/'Tests/Fixtures/content-v28-production.sqlite')
        cls.revised=set(json.loads((ROOT/'Content/data10-integration-revised-ids.json').read_text()));cls.e={r['id']:r for r in cls.t['examples']}
        cls.lids={a['listening_id'] for r in cls.items for a in r['tasks']}
    @classmethod
    def tearDownClass(cls):cls.db.close();cls.old.close()

    def test_frozen28_strict29_reproduction_all31_tables_schema_and_bytes(self):
        self.assertEqual(hashlib.sha256(gzip.decompress((ROOT/'Tests/Fixtures/content-v28-production.json.gz').read_bytes())).hexdigest(),BASE_SHA)
        self.assertEqual(hashlib.sha256((ROOT/'Tests/Fixtures/content-v28-production.sqlite').read_bytes()).hexdigest(),'a9f1f5459597203d07a62a6a70fdf41db5f77b943c29e45ea5921c9c503ba8ad')
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);s=p/'s.json';rev=p/'rev.json';b=p/'b.sqlite';prepare(s,rev)
            self.assertEqual(s.read_bytes(),SOURCE.read_bytes());self.assertEqual(set(json.loads(rev.read_text())),self.revised)
            result=build(s,b,ROOT/'Tests/Fixtures/content-v28-production.sqlite',production=True)
            self.assertEqual((result['validation']['error_count'],result['validation']['warning_count']),(0,10))
            receipt=audit(SOURCE,BUNDLE,b);self.assertEqual(receipt['total_source_rows'],70823);self.assertEqual(receipt['sqlite_tables'],31);self.assertEqual(len(receipt['revised_ids']),747);self.assertEqual(receipt['new_entities'],81)

    def test_only_explicit747_endpoint_revisions_no_payload_or_existing_membership_changes(self):
        a,b=signatures(self.old),signatures(self.db);self.assertTrue(a.keys()<=b.keys());self.assertEqual({i for i in a if a[i]!=b[i]},self.revised)
        for table in ('vocabulary','meanings','examples','grammar','listening_items','questions','question_choices','grammar_examples','vocabulary_examples'):
            self.assertEqual(self.t[table],self.oldsrc['tables'][table],table)
        for table in ('courses','lessons','lesson_items','item_tags','content_links'):
            rows=self.oldsrc['tables'][table];self.assertEqual(self.t[table][:len(rows)],rows,table)
        self.assertEqual(self.db.execute('SELECT schema_version,content_version,min_reader_version FROM content_metadata').fetchone(),(4,29,7))

    def test_all_three_courses72_small_lessons_reachable_via_actual_typed_sql(self):
        courses=self.db.execute(query('SQLiteListening','SELECT c.* FROM courses'),['lower_intermediate']).fetchall()
        self.assertEqual({r[0] for r in courses},{r['id'] for r in self.m['courses']});seen=set()
        for course in self.m['courses']:
            lessons=self.db.execute(query('SQLiteListening','SELECT l.id,l.title_ja,COUNT(*)'),[course['id']]).fetchall();self.assertEqual(len(lessons),24)
            for lesson,row in zip(course['lessons'],lessons):
                self.assertEqual((row[0],row[2]),(lesson['id'],5))
                ids=[r[0] for r in self.db.execute(query('SQLiteListening','SELECT a.id FROM lesson_items'),[lesson['id']])]
                self.assertEqual(ids,lesson['listening_ids']);self.assertFalse(seen&set(ids));seen.update(ids)
                sources=[self.db.execute('SELECT source_example_id FROM listening_items WHERE id=?',[i]).fetchone()[0] for i in ids];self.assertEqual(len(set(sources)),5)
                self.assertEqual(self.db.execute("SELECT COUNT(*) FROM item_tags it JOIN tags t ON t.id=it.tag_id WHERE it.content_id=? AND t.namespace='data10_unit'",[lesson['id']]).fetchone()[0],1)
        self.assertEqual(seen,self.lids)

    def test_generic_lesson_engine_cannot_receive_listening_or_grammar_courses(self):
        generic=self.db.execute(query('SQLiteContentRepository','SELECT c.* FROM courses')).fetchall();self.assertEqual(len(generic),3)
        for cid,*_ in generic:
            self.assertEqual(self.db.execute("SELECT COUNT(*) FROM lessons l JOIN lesson_items m ON m.lesson_id=l.id JOIN content_items i ON i.id=m.content_id WHERE l.course_id=? AND i.kind IN ('grammar','listening')",[cid]).fetchone()[0],0)
        ids=self.db.execute(query('SQLiteCurriculum','SELECT id FROM content_items'),['lower_intermediate','lesson','','lesson']).fetchall();self.assertEqual(len(ids),47)
        self.assertFalse({r[0] for r in ids}&{l['id']for c in self.m['courses']for l in c['lessons']})

    def test_all360_question_example_grammar_vocabulary_chains_and_reviewed_surface_forms(self):
        qsql=query('SQLiteListening','SELECT q.*,l.id');seen=set()
        for row in self.m['prerequisites']+self.m['related_vocabulary']:
            self.assertIn(row['observed_form_ko'],self.e[row['example_id']]['korean'])
            refs=self.db.execute(query('SQLiteListening','SELECT i.id,i.kind FROM content_links'),[row['example_id']]).fetchall();self.assertEqual(len(refs),2)
            expected=row.get('grammar_id',row.get('vocabulary_id'));self.assertIn(expected,{x[0]for x in refs})
            for rid,kind in refs:
                self.assertIsNotNone(self.db.execute(query('SQLiteLookup','SELECT i.level'),[rid,kind]).fetchone())
                self.assertIn(self.db.execute('SELECT level FROM content_items WHERE id=?',[rid]).fetchone()[0],['intro','beginner','lower_intermediate'])
        for lid in self.lids:
            rows=self.db.execute(qsql+' AND l.id=? ORDER BY l.learning_order,l.id LIMIT 20',[lid]).fetchall();self.assertEqual(len(rows),1);seen.add(rows[0][0])
            # Listening targets use questions.listening_id (FK), not the Grammar
            # question_target link contract. Do not invent redundant relations.
            self.assertEqual(self.db.execute('SELECT COUNT(*) FROM questions WHERE id=? AND listening_id=?',[rows[0][0],lid]).fetchone()[0],1)
        self.assertEqual(len(seen),360)
        # The haircut context must not show 머리's default "head" meaning
        # as if it were the intended "hair" sense. Use the unambiguous verb.
        haircut=next(r for r in self.m['related_vocabulary'] if r['key']=='A41')
        self.assertEqual(haircut['headword'],'자르다')
        self.assertEqual(self.db.execute('SELECT meaning_ja FROM meanings WHERE vocabulary_id=? ORDER BY ordinal LIMIT 1',[haircut['vocabulary_id']]).fetchone()[0],'切る')

    def test_all180_origins_two_tasks_and_no_old1936_content_recount_or_audio_claim(self):
        old24=sqlite3.connect(ROOT/'Tests/Fixtures/content-v24-production.sqlite');previous={r[0]for r in old24.execute('SELECT id FROM listening_items')};old24.close()
        self.assertEqual(len(previous),1936);self.assertEqual(self.db.execute('SELECT COUNT(*) FROM listening_items').fetchone()[0],2296);self.assertFalse(previous&self.lids)
        for r in self.items:
            self.assertEqual(self.db.execute('SELECT COUNT(*) FROM listening_items WHERE source_example_id=?',[r['example_id']]).fetchone()[0],2)
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM listening_items WHERE audio_mode!='tts' OR audio_asset_id IS NOT NULL").fetchone()[0],0)
        p=json.loads((ROOT/'Docs/DATA10_QA_PREREQUISITES.json').read_text());self.assertEqual(p['old163_unchanged']['unresolved'],36);self.assertEqual(len(p['surface_families_requiring_preview']),12)

    def test_old20_question_batches_and_order_unchanged_alongside_new_five_question_scopes(self):
        sql=query('SQLiteListening','SELECT l.id FROM listening_items');seen=set()
        for batch in range(103,121):
            values=['lower_intermediate',batch*20,(batch+1)*20];rows=self.db.execute(sql,values).fetchall();self.assertEqual(rows,self.old.execute(sql,values).fetchall());self.assertEqual(len(rows),20);seen.update(r[0]for r in rows)
        self.assertEqual(seen,self.lids)

    def test_disk28_update_keeps_every_user_table_bytes_snapshot_due_settings_and_favorites(self):
        with tempfile.TemporaryDirectory()as d:
            p=Path(d);content=p/'content.sqlite';up=p/'user.sqlite';shutil.copyfile(ROOT/'Tests/Fixtures/content-v28-production.sqlite',content);u=user(up,10)
            r=self.items[0];lid,qid=r['tasks'][0]['listening_id'],r['tasks'][0]['question_id'];vid=self.m['related_vocabulary'][0]['vocabulary_id'];gid=self.m['prerequisites'][0]['grammar_id']
            payload=json.dumps(dict(id='opaque',scope='practice:lower_intermediate:103',questions=[dict(id=qid,itemID=lid,transcript=self.e[r['example_id']]['korean'],choices=['c','a','b'])],heard=True,result='incorrect',answer='b',retry=[0],position=0,revision=6,contentVersion=28,updatedAt=100))
            u.execute(query('SQLiteListening','INSERT INTO listening_sessions'),['session','practice:lower_intermediate:103',payload,0])
            for i,kind in [(lid,'listening'),(vid,'vocabulary'),(gid,'grammar')]:u.execute('INSERT INTO srs_state VALUES(?,?,?,1,?,900,90,90)',[i,kind,'calendar_steps','{"stage":3}'])
            for i,kind in [(vid,'vocabulary'),(gid,'grammar')]:u.execute('INSERT INTO favorites VALUES(?,100,?)',[i,kind])
            u.execute("INSERT INTO user_metadata VALUES('settings','{\"reviewLimit\":10}')");u.execute("INSERT INTO user_metadata VALUES('review.content-version.v1','28')")
            u.execute(query('SQLiteProgressRepository','INSERT INTO study_events'),['event',lid,1,100,'2026-10-21','UTC','listening_comprehension','incorrect',0,'session',28])
            u.execute(query('SQLiteProgressRepository','INSERT INTO item_progress'),[lid,100,100,1,0,1]);u.execute(query('SQLiteProgressRepository','INSERT INTO daily_statistics'),['2026-10-21','UTC',1,0,1,0]);u.commit()
            tables=[r[0]for r in u.execute("SELECT name FROM sqlite_master WHERE type='table'")];before={t:u.execute('SELECT * FROM '+t).fetchall()for t in tables};u.close();raw=up.read_bytes();shutil.copyfile(BUNDLE,content);self.assertEqual(raw,up.read_bytes())
            with sqlite3.connect(up)as cold:
                for t in tables:self.assertEqual(cold.execute('SELECT * FROM '+t).fetchall(),before[t],t)
                self.assertEqual(cold.execute(query('SQLiteCurriculum','SELECT kind,target,level FROM')).fetchone()[:2],('listening','practice:lower_intermediate:103'))
            with sqlite3.connect(content)as c:self.assertIsNotNone(c.execute('SELECT id FROM questions WHERE id=?',[qid]).fetchone())

    def test_new_lesson_resume_scope_retry_stats_and_completed_counts_use_saved_sql(self):
        with tempfile.TemporaryDirectory()as d:
            path=Path(d)/'u.sqlite';u=user(path,10);lesson=self.m['courses'][0]['lessons'][0];lid=lesson['listening_ids'][0];qid=self.db.execute('SELECT id FROM questions WHERE listening_id=?',[lid]).fetchone()[0];scope='lesson:lower_intermediate:'+lesson['id']
            payload=json.dumps(dict(scope=scope,questions=[qid],position=0,heard=True,result='incorrect',answer='b',retry=[0],revision=3,updatedAt=100,contentVersion=29))
            u.execute(query('SQLiteListening','INSERT INTO listening_sessions'),['s',scope,payload,0]);self.assertEqual(u.execute(query('SQLiteCurriculum','SELECT kind,target,level FROM')).fetchone()[:2],('listening',scope))
            for attempt,result in [(0,'incorrect'),(1,'correct')]:
                u.execute(query('SQLiteListening','INSERT INTO listening_attempts'),['s',qid,attempt,lid,'comprehension','a',result,0,100,None])
                u.execute(query('SQLiteProgressRepository','INSERT INTO study_events'),['e'+str(attempt),lid,1,100,'2026-10-21','UTC','listening_retry'if attempt else'listening_comprehension',result,0,'s',29])
            self.assertEqual(u.execute("SELECT COUNT(DISTINCT a.item_id) FROM listening_attempts a JOIN listening_sessions s ON s.id=a.session_id WHERE s.completed=1 AND a.attempt=0 AND a.item_id=?",[lid]).fetchone()[0],0)
            u.execute('UPDATE listening_sessions SET completed=1 WHERE id=\'s\'');self.assertIsNone(u.execute(query('SQLiteCurriculum','SELECT kind,target,level FROM')).fetchone())
            self.assertEqual(u.execute("SELECT COUNT(DISTINCT a.item_id) FROM listening_attempts a JOIN listening_sessions s ON s.id=a.session_id WHERE s.completed=1 AND a.attempt=0 AND a.item_id=?",[lid]).fetchone()[0],1)
            stats=u.execute(query('SQLiteStatistics','SELECT COUNT(CASE'),[0,200]).fetchone();self.assertEqual(stats[-2:],(0,1));u.commit();u.close()
            with sqlite3.connect(path)as cold:self.assertEqual(cold.execute('SELECT state_json FROM listening_sessions').fetchone()[0],payload)

    def test_duplicate_attempt_and_srs_keys_rollback_without_losing_prior_due(self):
        with tempfile.TemporaryDirectory()as d:
            u=user(Path(d)/'u.sqlite',10);lid=next(iter(self.lids));u.execute("INSERT INTO srs_state VALUES(?,'listening','calendar_steps',1,'{\"stage\":3}',900,90,90)",[lid]);u.commit();before=u.execute('SELECT * FROM srs_state').fetchall()
            with self.assertRaises(sqlite3.IntegrityError),u:
                u.execute('UPDATE srs_state SET due_at=0');u.execute("INSERT INTO srs_state VALUES(?,'listening','calendar_steps',1,'{}',0,0,0)",[lid])
            self.assertEqual(u.execute('SELECT * FROM srs_state').fetchall(),before)
            self.assertIn('if s.isReview {',(ROOT/'Repositories/SQLiteListening.swift').read_text());self.assertIn('} else { next = nil }',(ROOT/'Repositories/SQLiteListening.swift').read_text());u.close()

    def test_post_answer_context_and_audio_completion_stop_background_source_guards(self):
        ui=(ROOT/'Views/ListeningView.swift').read_text();model=(ROOT/'Models/ListeningModels.swift').read_text();view_contract(ui,model)
        feedback=ui.split('else if let result = s.result {',1)[1].split('} else if empty',1)[0];self.assertIn('ListeningFeedbackContextView(services:services,source:q.sourceID)',feedback)
        self.assertEqual(ui.count('ListeningFeedbackContextView(services:services'),1)
        for contract in ('playback = nil; audio.stop()','s.current?.id == play.question','s.revision == play.revision','activeListening(scope:scope)','if let lessonID = lessonID','questions = try ids.map'):
            self.assertIn(contract,ui)
        audio=(ROOT/'Services/KoreanAudioService.swift').read_text();self.assertIn('if success { self.completedPlaybackCount += 1 }',audio)
        resume=(ROOT/'Views/CurriculumResumeView.swift').read_text();self.assertIn('parts[0] == "lesson"',resume);self.assertIn('resumeScope:route.target',resume)

    def test_all150_dictations_keep_canonical_answers_and_general_input_policy(self):
        count=0
        for r in self.items:
            for a in r['tasks']:
                if a['task']=='dictation':
                    answer=json.loads(self.db.execute('SELECT answer_json FROM questions WHERE id=?',[a['question_id']]).fetchone()[0]);self.assertEqual(answer,dict(accepted=[self.e[r['example_id']]['korean']]));count+=1
        self.assertEqual(count,150)
        self.assertEqual(subprocess.check_output(['git','show','d76f0b89c38c892005de68aef206229234d141c9:LearningEngine/ConjugationEngine.swift'],cwd=ROOT),(ROOT/'LearningEngine/ConjugationEngine.swift').read_bytes())

    def test_strict_rejects_missing_id_unrevised_relation_and_dangling_reference(self):
        with tempfile.TemporaryDirectory()as d:
            for case in ('id','revision','reference'):
                s=copy.deepcopy(self.src)
                if case=='id':s['tables']['content_items']=[r for r in s['tables']['content_items']if r['id']!=self.items[0]['example_id']]
                elif case=='revision':
                    i=self.m['related_vocabulary'][0]['vocabulary_id'];next(r for r in s['tables']['content_items']if r['id']==i)['revision']=self.old.execute('SELECT revision FROM content_items WHERE id=?',[i]).fetchone()[0]
                else:s['tables']['content_links'][-1]['target_id']='00000000-0000-4000-8000-000000000000'
                p=Path(d)/'bad.json';p.write_text(json.dumps(s,ensure_ascii=False))
                with self.subTest(case=case),self.assertRaises(ValidationError):build(p,Path(d)/'bad.sqlite',ROOT/'Tests/Fixtures/content-v28-production.sqlite',production=True)

    def test_offline_queries_search_stats_and_maintenance_without_network(self):
        with patch.object(socket,'socket',side_effect=AssertionError('network forbidden')):
            for c in self.m['courses']:
                for l in c['lessons']:self.assertEqual(len(self.db.execute(query('SQLiteListening','SELECT a.id FROM lesson_items'),[l['id']]).fetchall()),5)
            for r in self.m['related_vocabulary']:
                rows=self.db.execute(query('SQLiteLookup','WITH terms'),[r['headword']]*3+[0]).fetchall();self.assertIn((r['vocabulary_id'],'vocabulary'),rows)
            for term in ('%',"' OR 1=1 --",'_'):self.assertEqual(self.db.execute(query('SQLiteLookup','WITH terms'),[term]*3+[0]).fetchall(),[])
            u=user(version=10);self.assertIsNotNone(u.execute(query('SQLiteStatistics','SELECT COUNT(CASE'),[0,200]).fetchone());self.assertEqual(u.execute(query('SQLiteStatistics','SELECT p.content_id FROM item_progress'),[0,20]).fetchall(),[]);u.close()

    def test_ads_purchase_entitlement_and_user_migration_sources_are_unchanged(self):
        names=subprocess.check_output(['git','ls-tree','-r','--name-only','d76f0b89c38c892005de68aef206229234d141c9','--','Monetization','Services','Resources'],cwd=ROOT,text=True).splitlines()
        protected=[n for n in names if n.startswith('Monetization/')or any(k in n for k in ('StoreKit','Purchase','Entitlement','AdMob','user-schema','user-migration'))]
        self.assertTrue(protected)
        for name in protected:self.assertEqual((ROOT/name).read_bytes(),subprocess.check_output(['git','show','d76f0b89c38c892005de68aef206229234d141c9:'+name],cwd=ROOT),name)
