"""DATA-06: actual bundle/repository SQL and disk integration, not Swift execution."""
import copy,json,sqlite3,tempfile,unittest,uuid
from pathlib import Path
from build_content import ROOT,build
from validator import signatures,ValidationError
from test_data05_content import query

class Data06Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ids=json.loads((ROOT/'Content/data06-ids.json').read_text())
  cls.db=sqlite3.connect(ROOT/'Resources/content.sqlite')
  cls.old=sqlite3.connect(ROOT/'Tests/Fixtures/content-v12-production.sqlite')
 @classmethod
 def tearDownClass(cls):cls.db.close();cls.old.close()
 def test_strict_release_and_exact_counts(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'content.sqlite';r=build(ROOT/'Content/production.json',p,ROOT/'Tests/Fixtures/content-v12-production.sqlite',production=True)
   self.assertEqual(r['validation']['error_count'],0);self.assertEqual(r['validation']['warning_count'],10)
   with sqlite3.connect(p) as db:self.assertEqual(signatures(db),signatures(self.db))
  for table,old,new in [('listening_items',31,1936),('questions',262,3553),('content_items',4503,15935),('examples',1876,4813),('vocabulary',926,2287),('grammar',42,96)]:
   self.assertEqual(self.old.execute('SELECT COUNT(*) FROM '+table).fetchone()[0],old)
   self.assertEqual(self.db.execute('SELECT COUNT(*) FROM '+table).fetchone()[0],new)
  self.assertEqual(self.db.execute('SELECT schema_version,content_version,min_reader_version,is_fixture FROM content_metadata').fetchone(),(4,23,7,0))
  self.assertEqual(self.db.execute('PRAGMA foreign_key_check').fetchall(),[])
 def test_existing_payloads_stable_ids_orders_and_only_approved_revisions(self):
  approved=set(json.loads((ROOT/'Content/data06-revised-ids.json').read_text()));a,b=signatures(self.old),signatures(self.db)
  subsequent=set(json.loads((ROOT/'Content/data07-revised-ids.json').read_text())) | set(json.loads((ROOT/'Content/data08-a-revised-ids.json').read_text())) | set(json.loads((ROOT/'Content/data08-b-revised-ids.json').read_text())) | set(json.loads((ROOT/'Content/data08-c-revised-ids.json').read_text())) | set(json.loads((ROOT/'Content/data08-integration-revised-ids.json').read_text())) | set(json.loads((ROOT/'Content/data09-a-revised-ids.json').read_text())) | set(json.loads((ROOT/'Content/data09-b-revised-ids.json').read_text())) | set(json.loads((ROOT/'Content/data09-c-revised-ids.json').read_text()))
  self.assertEqual(len(approved),80);self.assertEqual({id for id in a if a[id]!=b[id]},(approved | subsequent) & set(a))
  for row in self.old.execute('SELECT * FROM content_items'):
   expected=list(row)
   if row[0] in approved:expected[2]+=1;expected[-1]='2026-10-03T12:53:00Z'
   if row[0] in json.loads((ROOT/'Content/data07-revised-ids.json').read_text()):expected[2]+=1;expected[-1]='2026-10-06T00:00:00Z'
   if row[0] in json.loads((ROOT/'Content/data08-a-revised-ids.json').read_text()):expected[2]+=1;expected[-1]='2026-10-19T07:15:00Z'
   if row[0] in json.loads((ROOT/'Content/data08-b-revised-ids.json').read_text()):expected[2]+=1;expected[-1]='2026-10-19T07:56:45Z'
   if row[0] in json.loads((ROOT/'Content/data08-c-revised-ids.json').read_text()):expected[2]+=1;expected[-1]='2026-10-19T08:39:13Z'
   if row[0] in json.loads((ROOT/'Content/data08-integration-revised-ids.json').read_text()):expected[2]+=1;expected[-1]='2026-10-19T13:29:13Z'
   if row[0] in json.loads((ROOT/'Content/data09-a-revised-ids.json').read_text()):expected[2]+=1;expected[-1]=json.loads((ROOT/'Content/data09-a-ids.json').read_text())['created_at']
   if row[0] in json.loads((ROOT/'Content/data09-b-revised-ids.json').read_text()):expected[2]+=1;expected[-1]=json.loads((ROOT/'Content/data09-b-ids.json').read_text())['created_at']
   if row[0] in json.loads((ROOT/'Content/data09-c-revised-ids.json').read_text()):expected[2]+=1;expected[-1]=json.loads((ROOT/'Content/data09-c-ids.json').read_text())['created_at']
   self.assertEqual(self.db.execute('SELECT * FROM content_items WHERE id=?',[row[0]]).fetchone(),tuple(expected))
  for table in ['vocabulary','meanings','examples','grammar','questions','listening_items','hangul','pronunciation_rules','courses','lessons']:
   for row in self.old.execute('SELECT * FROM '+table):self.assertEqual(self.db.execute('SELECT * FROM '+table+' WHERE id=?',[row[0]]).fetchone(),row)
  for table in ['lesson_items','vocabulary_examples','grammar_examples']:
   self.assertTrue(set(self.old.execute('SELECT * FROM '+table)) <= set(self.db.execute('SELECT * FROM '+table)))
 def test_all_new_items_through_bounded_repository_pages(self):
  seen=[];batches=query('SQLiteListening','SELECT l.learning_order/20');idsql=query('SQLiteListening','SELECT l.id FROM listening_items');qs=query('SQLiteListening','SELECT q.*,l.id')
  for level,total in [('intro',34),('beginner',79),('lower_intermediate',1823)]:
   levelids=[]
   after=-1
   while True:
    page=self.db.execute(batches,[level,after]).fetchall()
    if not page:break
    for batch,count in page:
     ids=[r[0]for r in self.db.execute(idsql,[level,batch*20,(batch+1)*20])];self.assertEqual(len(ids),count);self.assertLessEqual(count,20)
     rows=self.db.execute(qs+' AND l.id IN ('+','.join('?'for _ in ids)+') ORDER BY l.learning_order,l.id LIMIT 20',ids).fetchall();self.assertEqual(len(rows),len(ids));levelids+=ids
    after=page[-1][0]
   self.assertEqual(len(levelids),total);seen+=levelids
  self.assertEqual(len(set(seen)),1936);self.assertTrue({v['id']for v in self.ids}<=set(seen))
  self.assertEqual(self.db.execute(batches,['master',-1]).fetchall(),[])
 def test_new_types_sources_audio_choices_and_exact_dictation(self):
  self.assertEqual(len(self.ids),80);self.assertEqual(len({r['source_example_id']for r in self.ids}),80)
  self.assertEqual({t:sum(r['task']==t for r in self.ids)for t in ['meaning','korean','dictation','comprehension']},{t:20 for t in ['meaning','korean','dictation','comprehension']})
  self.db.row_factory=sqlite3.Row
  try:
   for item in self.ids:
    self.assertEqual(str(uuid.UUID(item['id'])),item['id'])
    q=self.db.execute(query('SQLiteListening','SELECT q.*,l.id')+' AND l.id=? ORDER BY l.learning_order,l.id LIMIT 20',[item['id']]).fetchone()
    self.assertEqual(q['source_example_id'],item['source_example_id']);self.assertEqual(q['level'],item['level']);self.assertEqual(q['audio_mode'],'tts');self.assertIsNone(q['prompt_ko']);self.assertTrue(q['japanese'].strip())
    self.assertIsNotNone(self.old.execute('SELECT id FROM examples WHERE id=?',[item['source_example_id']]).fetchone())
    answer=json.loads(q['answer_json']);choices=self.db.execute('SELECT choice_id,text FROM question_choices WHERE question_id=? ORDER BY ordinal',[q['id']]).fetchall()
    if item['task']=='dictation':
     self.assertEqual(choices,[]);self.assertEqual(set(answer['accepted']),{q['korean'],q['korean'].rstrip('.!?。！？')})
    else:
     self.assertEqual(len(choices),3);self.assertEqual(len({c['text']for c in choices}),3)
     correct=next(c['text']for c in choices if c['choice_id']==answer['correct_choice_ids'][0])
     if item['task']=='meaning':self.assertEqual(correct,q['japanese'])
     if item['task']=='korean':self.assertEqual(correct,q['korean'])
  finally:self.db.row_factory=None
 def test_new_invalid_inputs_rejected_without_weakening_validator(self):
  source=json.loads((ROOT/'Content/production.json').read_text())
  with tempfile.TemporaryDirectory() as tmp:
   for case in ['missing_source','inactive_source','empty_answer','duplicate_choice','wrong_level','empty_translation']:
    d=copy.deepcopy(source);t=d['tables'];item=next(r for r in self.ids if r['task']==('dictation'if case=='empty_answer'else'meaning'))
    l=next(r for r in t['listening_items']if r['id']==item['id']);q=next(r for r in t['questions']if r['id']==item['question_id'])
    if case=='missing_source':l['source_example_id']=str(uuid.uuid4())
    elif case=='inactive_source':next(r for r in t['content_items']if r['id']==l['source_example_id'])['is_active']=0
    elif case=='empty_answer':q['answer_json']=json.dumps({'accepted':[]})
    elif case=='duplicate_choice':
     c=[r for r in t['question_choices']if r['question_id']==q['id']];c[1]['text']=c[0]['text']
    elif case=='wrong_level':next(r for r in t['content_items']if r['id']==q['id'])['level']='master'
    elif case=='empty_translation':next(r for r in t['examples']if r['id']==l['source_example_id'])['japanese']=''
    path=Path(tmp)/'bad.json';path.write_text(json.dumps(d,ensure_ascii=False))
    with self.subTest(case=case),self.assertRaises(ValidationError):build(path,Path(tmp)/'bad.sqlite',production=True)
 def test_disk_retry_attempt_identity_backlog_and_other_skills_preserved(self):
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/'UserProgress.sqlite';u=sqlite3.connect(path)
   for name in ['user-schema-v1']+[f'user-migration-v{i}'for i in range(2,9)]:u.executescript((ROOT/f'Resources/{name}.sql').read_text())
   oldid=self.old.execute('SELECT id FROM vocabulary LIMIT 1').fetchone()[0]
   for skill in ['vocabulary','grammar','listening']:u.execute('INSERT INTO srs_state VALUES(?,?,?,?,?,?,?,?)',[oldid,skill,'calendar_steps',1,'{"stage":4}',9000,500,500])
   preserved=u.execute('SELECT * FROM srs_state').fetchall()
   item=self.ids[0];payload=json.dumps({'questions':[v['question_id']for v in self.ids[:20]],'position':13,'retry':[0,2,5],'retrying':False,'heard':True,'result':'incorrect','answer':'b','revision':41,'contentVersion':13})
   u.execute(query('SQLiteListening','INSERT INTO listening_sessions'),['session','practice:beginner:3',payload,0])
   attempt=['session',item['question_id'],0,item['id'],item['task'],'b','incorrect',0,100,200]
   u.execute(query('SQLiteListening','INSERT INTO listening_attempts'),attempt);u.commit()
   with self.assertRaises(sqlite3.IntegrityError):u.execute(query('SQLiteListening','INSERT INTO listening_attempts'),attempt)
   u.rollback();retry=attempt.copy();retry[2]=1;retry[5]='a';retry[6]='correct';retry[-1]=None
   u.execute(query('SQLiteListening','INSERT INTO listening_attempts'),retry)
   enroll=query('SQLiteListening','INSERT INTO srs_state')
   for v in self.ids:u.execute(enroll,[v['id'],'calendar_steps',1,'{"stage":0}',200,None,100])
   due=query('SQLiteListening','SELECT content_id FROM srs_state WHERE skill=');count=query('SQLiteListening','SELECT COUNT(*) AS n FROM srs_state WHERE skill=')
   self.assertEqual(u.execute(count,['calendar_steps',1,199]).fetchone()[0],0);self.assertEqual(u.execute(count,['calendar_steps',1,200]).fetchone()[0],80);self.assertEqual(len(u.execute(due,['calendar_steps',1,200]).fetchall()),20)
   self.assertIn('INDEX',str(u.execute('EXPLAIN QUERY PLAN '+due,['calendar_steps',1,200]).fetchall()))
   self.assertEqual(set(u.execute('SELECT * FROM srs_state WHERE content_id=?',[oldid]).fetchall()),set(preserved))
   u.commit();u.close()
   with sqlite3.connect(path) as cold:
    self.assertEqual(cold.execute('SELECT state_json FROM listening_sessions').fetchone()[0],payload)
    self.assertEqual(cold.execute('SELECT attempt,result FROM listening_attempts ORDER BY attempt').fetchall(),[(0,'incorrect'),(1,'correct')])
    self.assertEqual(cold.execute('SELECT COUNT(*) FROM srs_state').fetchone()[0],83)
    self.assertEqual(cold.execute('PRAGMA user_version').fetchone()[0],8)
