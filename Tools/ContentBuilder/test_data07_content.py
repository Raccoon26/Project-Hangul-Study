"""DATA07 real bundle and repository-SQL integration. This does not execute Swift."""
import collections,copy,hashlib,json,re,shutil,sqlite3,tempfile,unittest,uuid
from pathlib import Path
from build_content import ROOT,build
from validator import signatures,ValidationError
from test_data05_content import query
from test_lookup_sql import user

class Data07Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=sqlite3.connect(ROOT/'Resources/content.sqlite');cls.old=sqlite3.connect(ROOT/'Tests/Fixtures/content-v13-production.sqlite')
  cls.ids=json.loads((ROOT/'Content/data07-ids.json').read_text());cls.words={v['headword']:v for v in cls.ids['vocabulary']}
 @classmethod
 def tearDownClass(cls):cls.c.close();cls.old.close()
 def test_strict_import_exact_delta_and_schema_unchanged(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'new.sqlite';r=build(ROOT/'Content/production.json',p,ROOT/'Tests/Fixtures/content-v13-production.sqlite',production=True)
   self.assertEqual(r['validation']['error_count'],0);self.assertEqual(r['validation']['warning_count'],10)
   with sqlite3.connect(p) as c:self.assertEqual(signatures(c),signatures(self.c))
  # Cumulative Content13 -> current; DATA07's exact cohort remains checked below.
  for t,delta in [('vocabulary',1361),('meanings',1438),('examples',3117),('grammar',54),('questions',3571),('listening_items',2185),('grammar_examples',294),('learner_notes',350)]:
   self.assertEqual(self.c.execute('SELECT COUNT(*) FROM '+t).fetchone()[0]-self.old.execute('SELECT COUNT(*) FROM '+t).fetchone()[0],delta,t)
  self.assertEqual(self.c.execute('SELECT schema_version,content_version,min_reader_version,is_fixture FROM content_metadata').fetchone(),(4,29,7,0))
 def test_old_payloads_and_only_reviewed_endpoint_revision_changes(self):
  a,b=signatures(self.old),signatures(self.c);approved=set(json.loads((ROOT/'Content/data07-revised-ids.json').read_text()))
  subsequent=set(json.loads((ROOT/'Content/data08-a-revised-ids.json').read_text()))
  batch_b=set(json.loads((ROOT/'Content/data08-b-revised-ids.json').read_text()))
  batch_c=set(json.loads((ROOT/'Content/data08-c-revised-ids.json').read_text()))
  integration=set(json.loads((ROOT/'Content/data08-integration-revised-ids.json').read_text()))
  data09_a=set(json.loads((ROOT/'Content/data09-a-revised-ids.json').read_text()))
  data09_b=set(json.loads((ROOT/'Content/data09-b-revised-ids.json').read_text()))
  data09_c=set(json.loads((ROOT/'Content/data09-c-revised-ids.json').read_text()))
  data09_integration=set(json.loads((ROOT/'Content/data09-integration-revised-ids.json').read_text()))
  data10_integration=set(json.loads((ROOT/'Content/data10-integration-revised-ids.json').read_text()))
  self.assertEqual({id for id in a if a[id]!=b[id]},(approved | subsequent | batch_b | batch_c | integration | data09_a | data09_b | data09_c | data09_integration | data10_integration) & set(a));self.assertEqual(len(approved),30)
  for row in self.old.execute('SELECT * FROM content_items'):
   actual=self.c.execute('SELECT * FROM content_items WHERE id=?',[row[0]]).fetchone()
   self.assertEqual(actual[:2]+actual[3:-1],row[:2]+row[3:-1]);self.assertEqual(actual[2],row[2]+int(row[0]in approved)+int(row[0]in subsequent)+int(row[0]in batch_b)+int(row[0]in batch_c)+int(row[0]in integration)+int(row[0]in data09_a)+int(row[0]in data09_b)+int(row[0]in data09_c)+int(row[0]in data09_integration)+int(row[0]in data10_integration))
  for t in ['vocabulary','meanings','examples','grammar','questions','listening_items','courses','lessons','hangul','pronunciation_rules']:
   for row in self.old.execute('SELECT * FROM '+t):self.assertEqual(self.c.execute('SELECT * FROM '+t+' WHERE id=?',[row[0]]).fetchone(),row)
  for t in ['vocabulary_examples','grammar_examples','lesson_items','question_choices','content_links']:
   self.assertTrue(set(self.old.execute('SELECT * FROM '+t))<=set(self.c.execute('SELECT * FROM '+t)))
 def test_every_new_card_uuid_meaning_example_and_note(self):
  self.assertEqual(len(self.words),450)
  for word in self.words.values():
   id=word['id'];self.assertEqual(str(uuid.UUID(id)),id)
   row=self.c.execute(query('SQLiteVocabularyContent','SELECT v.headword'),[id]).fetchone();self.assertEqual(row[:2],(word['headword'],word['part_of_speech']))
   ms=self.c.execute(query('SQLiteVocabularyContent','SELECT m.*'),[id]).fetchall();self.assertEqual([m[0]for m in ms],word['meaning_ids'])
   self.assertEqual(len(word['example_ids']),2)
   for m in ms:
    e=self.c.execute(query('SQLiteVocabularyContent','SELECT e.id'),[m[0]]).fetchone();self.assertIn(e[0],word['example_ids']);self.assertTrue(e[1].strip()and e[2].strip())
   if word['note_id']:self.assertEqual(self.c.execute(query('SQLiteVocabularyContent','SELECT n.id'),[id]).fetchone()[0],word['note_id'])
  self.assertEqual(self.c.execute('PRAGMA foreign_key_check').fetchall(),[])
 def test_duplicate_semantics_and_no_new_duplicate_sentences(self):
  oldheads={r[0]for r in self.old.execute('SELECT headword FROM vocabulary')};self.assertFalse(oldheads&set(self.words))
  oldsentences={r[0]for r in self.old.execute('SELECT korean FROM examples')};new=[]
  for id in self.ids['examples']:
   text=self.c.execute('SELECT korean FROM examples WHERE id=?',[id]).fetchone()[0];self.assertNotIn(text,oldsentences);new.append(text)
  self.assertEqual(len(new),len(set(new)))
  for w in ['풀다','든든하다','입장','겨우','자신']:
   self.assertEqual(len(self.words[w]['meaning_ids']),2)
 def test_new_metadata_matches_existing_editorial_policy(self):
  for word in self.words.values():
   row=self.c.execute('SELECT part_of_speech,has_batchim,irregular_type,topik_level,frequency_rank,reading FROM vocabulary WHERE id=?',[word['id']]).fetchone()
   if row[0]in ['verb','adjective','expression']:self.assertIsNone(row[1])
   self.assertEqual(row[3:],(None,None,None))
   if row[0]in ['verb','adjective']and word['headword'].endswith('하다'):self.assertEqual(row[2],'other')
  for word,kind in [('붓다','s'),('되묻다','d'),('가렵다','b'),('타오르다','reu'),('덮다','none'),('잠그다','none')]:
   self.assertEqual(self.c.execute('SELECT irregular_type FROM vocabulary WHERE headword=?',[word]).fetchone()[0],kind)
  for word in ['한동안','당장']:self.assertEqual(self.words[word]['part_of_speech'],'noun')
 def test_level_set_order_and_curriculum_access_in_bounded_pages(self):
  for level,n in [('intro',306),('beginner',800),('lower_intermediate',1181)]:
   sql='SELECT v.id FROM vocabulary v JOIN content_items i ON i.id=v.id WHERE i.level=? ORDER BY sort_key,v.id'
   old=[r[0]for r in self.old.execute(sql,[level])];new=[r[0]for r in self.c.execute(sql,[level])]
   self.assertEqual(len(new),n);self.assertEqual(new[:len(old)],old)
   seen=[];cursor=''
   while True:
    rows=self.c.execute(query('SQLiteCurriculum','SELECT id FROM content_items'),[level,'vocabulary',cursor,'vocabulary']).fetchall()
    if not rows:break
    self.assertLessEqual(len(rows),200);seen.extend(r[0]for r in rows);cursor=rows[-1][0]
   self.assertEqual(set(seen),set(new))
   self.assertTrue(all(1<=len(new[i:i+20])<=20 for i in range(0,n,20)))
  self.assertEqual(collections.Counter(v['level']for v in self.words.values()),{'beginner':180,'lower_intermediate':270})
 def test_korean_japanese_secondary_meaning_search_and_related_detail(self):
  for term,head in [('정해지다','정해지다'),('返送','반송하다'),('心強い','든든하다'),('自分自身','자신'),('期限','기한')]:
   matches=self.c.execute(query('SQLiteLookup','WITH terms'),[term]*3+[0]).fetchall();self.assertIn((self.words[head]['id'],'vocabulary'),matches);self.assertLessEqual(len(matches),30)
  for r in self.ids['relations']:
   self.assertIn((r['target_id'],'vocabulary'),self.c.execute(query('SQLiteLookup','WITH related'),[r['source_id']]*5).fetchall())
  for r in self.ids['grammar_links']:
   self.assertIn(r['example_id'],[x[0]for x in self.c.execute(query('SQLiteGrammarContent','SELECT e.id,e.korean'),[r['grammar_id']])])
 def test_direct_input_and_four_listening_tasks_use_actual_sources(self):
  self.assertEqual({x['task']for x in self.ids['listening']},{'meaning','korean','dictation','comprehension'})
  self.c.row_factory=sqlite3.Row
  try:
   for r in self.ids['direct_input']:
    q=self.c.execute(query('SQLiteProduction','SELECT q.*'),[r['vocabulary_id']]).fetchone();self.assertEqual(q['headword'],r['lemma']);self.assertEqual(json.loads(q['answer_json'])['accepted'],[r['accepted']]);self.assertEqual(json.loads(q['rubric_json'])['overrides'],{})
   for r in self.ids['listening']:
    q=self.c.execute(query('SQLiteListening','SELECT q.*,l.id')+' AND l.id=? ORDER BY l.learning_order,l.id LIMIT 20',[r['id']]).fetchone()
    self.assertEqual(q['source_example_id'],r['example_id']);self.assertEqual(q['level'],r['level']);self.assertEqual(q['audio_mode'],'tts');self.assertIsNone(q['prompt_ko'])
    if r['task']=='dictation':self.assertIn(q['korean'],json.loads(q['answer_json'])['accepted'])
  finally:self.c.row_factory=None
 def test_content_replacement_preserves_user_bytes_and_partial_session(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp);content=p/'Content.sqlite';progress=p/'User.sqlite';shutil.copyfile(ROOT/'Tests/Fixtures/content-v13-production.sqlite',content)
   d=user(progress,10);oldids=[r[0]for r in self.old.execute('SELECT id FROM vocabulary ORDER BY sort_key,id LIMIT 20')]
   payload=json.dumps(dict(vocabularyIDs=oldids,order=oldids,position=4,round=1,deferred=oldids[:2],contentVersion=13))
   d.execute(query('SQLiteVocabularyProgress','INSERT INTO vocabulary_sets('),['set','intro',1,100])
   for i,id in enumerate(oldids):d.execute(query('SQLiteVocabularyProgress','INSERT INTO vocabulary_set_items('),['set',id,i])
   d.execute(query('SQLiteVocabularyProgress','INSERT INTO vocabulary_sessions('),['session','set',payload,4,100])
   for skill,table in [('vocabulary','vocabulary'),('grammar','grammar'),('listening','listening_items')]:
    id=self.old.execute('SELECT id FROM '+table+' LIMIT 1').fetchone()[0];d.execute('INSERT INTO srs_state VALUES(?,?,?,?,?,?,?,?)',[id,skill,'calendar_steps',1,'{"stage":4}',300,100,100])
   d.execute("INSERT INTO favorites(content_id,created_at,content_type)VALUES(?,100,'vocabulary')",[oldids[0]])
   d.execute("INSERT INTO user_metadata VALUES('curriculum.profile.v1','{\"level\":\"beginner\"}')")
   d.execute("INSERT INTO user_metadata VALUES('settings.v1','{\"shortSession\":5}')");d.commit();d.close();before=progress.read_bytes()
   shutil.copyfile(ROOT/'Resources/content.sqlite',content);self.assertEqual(before,progress.read_bytes())
   with sqlite3.connect(progress)as cold,sqlite3.connect(content)as c:
    self.assertEqual(cold.execute('SELECT state_json,status FROM vocabulary_sessions').fetchone(),(payload,'active'))
    self.assertEqual(cold.execute('SELECT content_id FROM vocabulary_set_items ORDER BY ordinal').fetchall(),[(i,)for i in oldids])
    self.assertEqual(cold.execute('SELECT COUNT(*)FROM srs_state').fetchone()[0],3)
    for id,kind in cold.execute('SELECT content_id,content_type FROM favorites'):self.assertIsNotNone(c.execute(query('SQLiteLookup','SELECT i.level'),[id,kind]).fetchone())
    self.assertEqual(cold.execute('PRAGMA user_version').fetchone()[0],10)
 def test_new_enrollment_deduplicated_and_due_queue_bounded(self):
  d=user(version=10);sql=query('SQLiteReviewProgress','INSERT INTO srs_state(');ids=[r['id']for r in self.words.values()]
  for id in ids:d.execute(sql,[id,'calendar_steps',1,'{"stage":0}',100,100])
  for id in ids:d.execute(sql,[id,'calendar_steps',1,'{"stage":0}',900,200])
  self.assertEqual(d.execute('SELECT COUNT(*)FROM srs_state').fetchone()[0],450);self.assertEqual(d.execute('SELECT DISTINCT due_at FROM srs_state').fetchall(),[(100.0,)])
  due=query('SQLiteReviewProgress','SELECT content_id FROM srs_state WHERE');self.assertEqual(d.execute(due,['calendar_steps',1,99,5]).fetchall(),[])
  self.assertEqual(len(d.execute(due,['calendar_steps',1,100,5]).fetchall()),5);self.assertEqual(len(d.execute(due,['calendar_steps',1,100,30]).fetchall()),30)
  self.assertIn('INDEX',str(d.execute('EXPLAIN QUERY PLAN '+due,['calendar_steps',1,100,5]).fetchall()));d.close()
 def test_empty_or_corrupt_new_data_is_not_silently_accepted(self):
  original=json.loads((ROOT/'Content/production.json').read_text());v=self.ids['vocabulary'][0];eid=v['example_ids'][0]
  with tempfile.TemporaryDirectory()as tmp:
   for case in ['empty_ja','bad_pos','bad_level','orphan_relation']:
    d=copy.deepcopy(original)
    if case=='empty_ja':next(e for e in d['tables']['examples']if e['id']==eid)['japanese']=''
    elif case=='bad_pos':next(e for e in d['tables']['vocabulary']if e['id']==v['id'])['part_of_speech']='名詞'
    elif case=='bad_level':next(e for e in d['tables']['content_items']if e['id']==v['id'])['level']='TOPIK2'
    else:d['tables']['content_links'][-1]['target_id']=str(uuid.uuid4())
    p=Path(tmp)/'bad.json';p.write_text(json.dumps(d,ensure_ascii=False))
    with self.subTest(case=case),self.assertRaises(ValidationError):build(p,Path(tmp)/'bad.sqlite',production=True)
