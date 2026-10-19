"""DATA-05 release gates using the real SQLite bundle and repository SQL.
Opaque JSON persistence checks do NOT execute Swift Codable/learning transitions.
Native end-to-end tests are in ProductionLearningTests.swift.
"""
import json,re,sqlite3,tempfile,unittest,uuid,copy
from pathlib import Path
from build_content import ROOT,build
from validator import signatures,ValidationError

def queries(name):
 text=(ROOT/f'Repositories/{name}.swift').read_text()
 return re.findall(r'"""(.*?)"""',text,re.S)+re.findall(r'"([^"\n]+)"',text)
def query(name,prefix):return next(q for q in queries(name) if q.strip().startswith(prefix))
class Data05Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ids=json.loads((ROOT/'Content/data05-ids.json').read_text());cls.db=sqlite3.connect(ROOT/'Resources/content.sqlite');cls.old=sqlite3.connect(ROOT/'Tests/Fixtures/content-v11-production.sqlite')
 @classmethod
 def tearDownClass(cls):cls.db.close();cls.old.close()
 def test_strict_previous_release_gate_and_exact_delta(self):
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/'bundle.sqlite';r=build(ROOT/'Content/production.json',path,ROOT/'Tests/Fixtures/content-v11-production.sqlite',production=True)
   self.assertEqual(r['validation']['error_count'],0);self.assertEqual(r['validation']['warning_count'],10)
   with sqlite3.connect(path) as new:self.assertEqual(signatures(new),signatures(self.db))
  for table,before,after in [('vocabulary',726,1376),('meanings',772,1457),('examples',1537,2776),('grammar',42,42),('questions',250,354),('listening_items',27,115),('content_items',3700,6552)]:
   self.assertEqual(self.old.execute('SELECT COUNT(*) FROM '+table).fetchone()[0],before);self.assertEqual(self.db.execute('SELECT COUNT(*) FROM '+table).fetchone()[0],after)
  self.assertEqual(self.db.execute('SELECT schema_version,content_version,min_reader_version,is_fixture FROM content_metadata').fetchone(),(4,14,7,0))
  self.assertEqual(self.db.execute('PRAGMA user_version').fetchone()[0],4)
 def test_all_existing_payloads_ids_membership_and_approved_relation_revisions(self):
  historical=sqlite3.connect(ROOT/'Tests/Fixtures/content-v12-production.sqlite')
  a,b=signatures(self.old),signatures(historical);historical.close();changed=set(json.loads((ROOT/'Content/data05-revised-ids.json').read_text()))
  self.assertEqual({id for id in a if a[id]!=b[id]},changed);self.assertEqual(len(changed),8)
  for row in self.old.execute('SELECT * FROM content_items'):
   actual=self.db.execute('SELECT * FROM content_items WHERE id=?',[row[0]]).fetchone();self.assertEqual(actual[:2]+actual[3:-1],row[:2]+row[3:-1]);self.assertEqual(actual[2],row[2]+int(row[0] in changed)+int(row[0] in json.loads((ROOT/'Content/data06-revised-ids.json').read_text()))+int(row[0] in json.loads((ROOT/'Content/data07-revised-ids.json').read_text())))
  for table in ['vocabulary','meanings','examples','grammar','questions','hangul','pronunciation_rules','listening_items','lessons','courses']:
   for row in self.old.execute('SELECT * FROM '+table):self.assertEqual(self.db.execute('SELECT * FROM '+table+' WHERE id=?',[row[0]]).fetchone(),row)
  for row in self.old.execute('SELECT * FROM lesson_items'):self.assertIn(row,self.db.execute('SELECT * FROM lesson_items WHERE lesson_id=?',[row[0]]).fetchall())
  old=[r[0]for r in self.old.execute('SELECT v.id FROM vocabulary v JOIN content_items i ON i.id=v.id WHERE i.level="beginner" ORDER BY sort_key,v.id')]
  new=[r[0]for r in self.db.execute('SELECT v.id FROM vocabulary v JOIN content_items i ON i.id=v.id WHERE i.level="beginner" ORDER BY sort_key,v.id')]
  self.assertEqual(new[:len(old)],old);self.assertEqual(set(new[len(old):]),{v['id']for v in self.ids['vocabulary']} | {v['id'] for v in json.loads((ROOT/'Content/data07-ids.json').read_text())['vocabulary'] if v['level']=='beginner'})
 def test_all_new_cards_meanings_notes_and_examples_through_actual_queries(self):
  card=query('SQLiteVocabularyContent','SELECT v.headword');meanings=query('SQLiteVocabularyContent','SELECT m.*');example=query('SQLiteVocabularyContent','SELECT e.id')
  self.assertEqual(len(self.ids['vocabulary']),200);self.assertEqual(len(self.ids['examples']),339)
  for v in self.ids['vocabulary']:
   self.assertEqual(str(uuid.UUID(v['id'])),v['id']);row=self.db.execute(card,[v['id']]).fetchone();self.assertEqual(row[:2],(v['headword'],v['part_of_speech']))
   ms=self.db.execute(meanings,[v['id']]).fetchall();self.assertEqual([m[0]for m in ms],v['meaning_ids'])
   for m in ms:
    e=self.db.execute(example,[m[0]]).fetchone();self.assertIn(e[0],v['example_ids']);self.assertTrue(e[1].strip() and e[2].strip())
  self.assertEqual(self.db.execute(card,['00000000-0000-4000-8000-000000000000']).fetchall(),[])
  self.assertEqual(self.db.execute('SELECT COUNT(*) FROM examples GROUP BY korean,japanese HAVING COUNT(*)>1').fetchall(),[])
  self.assertEqual(self.db.execute('PRAGMA foreign_key_check').fetchall(),[])
 def test_search_level_pos_and_bounded_set_selection(self):
  code=(ROOT/'Repositories/SQLiteContentRepository.swift').read_text();base=re.findall(r'"""(.*?)"""',code,re.S)[0];parts=re.findall(r'sql \+= "([^"]+)"',code)
  clause=lambda p:next(x for x in parts if x.startswith(p))
  for text,lemma in [('줍다','줍다'),('預ける','맡기다'),('顔が広い','발이 넓다')]:
   rows=self.db.execute(base+clause(' AND v.id IN')+clause(' ORDER BY'),[text,text+chr(0x10ffff),20]).fetchall();self.assertIn(lemma,[r[1]for r in rows])
  for level,total in [('intro',306),('beginner',800),('master',0)]:self.assertEqual(self.db.execute(query('SQLiteVocabularyContent','SELECT COUNT(*) AS count'),[level]).fetchone()[0],total)
  for pos in ['verb','adjective','adverb','noun','expression']:
   ids=[v['id']for v in self.ids['vocabulary'] if v['part_of_speech']==pos];self.assertTrue(ids)
   self.assertTrue(all(self.db.execute('SELECT part_of_speech FROM vocabulary WHERE id=?',[id]).fetchone()[0]==pos for id in ids))
 def test_actual_production_grammar_listening_relationships(self):
  sql=query('SQLiteProduction','SELECT q.*');self.db.row_factory=sqlite3.Row
  try:
   for p in self.ids['direct_input']:
    rows=self.db.execute(sql,[p['vocabulary_id']]).fetchall();q=next(r for r in rows if r['id']==p['question_id']);self.assertEqual(q['headword'],p['lemma']);self.assertIn(p['accepted'],json.loads(q['answer_json'])['accepted'])
    self.assertIsNotNone(self.db.execute("SELECT g.id FROM content_links l JOIN grammar g ON g.id=l.target_id WHERE l.source_id=? AND relation='prerequisite'",[q['id']]).fetchone())
   for g in self.ids['grammar_links']:
    rows=self.db.execute(query('SQLiteGrammarContent','SELECT e.id,e.korean'),[g['grammar_id']]).fetchall();self.assertIn(g['example_id'],[r['id']for r in rows])
   ids=self.db.execute(query('SQLiteListening','SELECT l.id FROM listening_items'),['beginner',40,60]).fetchall();self.assertEqual({r[0]for r in ids},{r['id']for r in self.ids['listening']})
   for l in self.ids['listening']:
    q=self.db.execute(query('SQLiteListening','SELECT q.*,l.id')+' AND l.id IN (?) ORDER BY l.learning_order,l.id LIMIT 20',[l['id']]).fetchone();self.assertEqual(q['source_example_id'],l['example_id']);self.assertEqual(q['level'],'beginner');self.assertEqual(q['audio_mode'],'tts')
    a=json.loads(q['answer_json']);task=json.loads(q['rubric_json'])['listening_task']
    if task=='dictation':self.assertIn(q['korean'],a['accepted'])
  finally:self.db.row_factory=None
 def test_new_set_and_srs_storage_resume_and_old_schedules_preserved(self):
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/'UserProgress.sqlite';u=sqlite3.connect(path)
   for name in ['user-schema-v1']+[f'user-migration-v{i}'for i in range(2,9)]:u.executescript((ROOT/f'Resources/{name}.sql').read_text())
   old=self.old.execute('SELECT id FROM vocabulary LIMIT 1').fetchone()[0]
   u.execute('INSERT INTO srs_state VALUES(?,?,?,?,?,?,?,?)',[old,'vocabulary','calendar_steps',1,'{"stage":4}',500,100,100]);saved=u.execute('SELECT * FROM srs_state').fetchall()
   ids=[v['id']for v in self.ids['vocabulary'][:20]];payload=json.dumps(dict(vocabularyIDs=ids,order=ids,position=13,round=1,deferred=ids[:3],revealed=True,contentVersion=12))
   u.execute(query('SQLiteVocabularyProgress','INSERT INTO vocabulary_sets('),['new-set','beginner',22,100])
   for n,id in enumerate(ids):u.execute(query('SQLiteVocabularyProgress','INSERT INTO vocabulary_set_items('),['new-set',id,n])
   u.execute(query('SQLiteVocabularyProgress','INSERT INTO vocabulary_sessions('),['new-session','new-set',payload,15,100]);u.commit();u.close();u=sqlite3.connect(path)
   self.assertEqual(u.execute(query('SQLiteVocabularyProgress','SELECT * FROM vocabulary_sessions WHERE id='),['new-session']).fetchone()[2],payload)
   enroll=query('SQLiteReviewProgress','INSERT INTO srs_state(')
   for id in ids+[old]:u.execute(enroll,[id,'calendar_steps',1,'{"stage":0}',100,100])
   self.assertEqual(u.execute('SELECT * FROM srs_state WHERE content_id=?',[old]).fetchall(),saved)
   self.assertEqual(u.execute('SELECT COUNT(*) FROM srs_state').fetchone()[0],21)
   due=query('SQLiteReviewProgress','SELECT content_id FROM srs_state WHERE')
   self.assertEqual(len(u.execute(due,['calendar_steps',1,100,20]).fetchall()),20)
   self.assertIn('INDEX',str(u.execute('EXPLAIN QUERY PLAN '+due,['calendar_steps',1,100,20]).fetchall()))
   u.commit();u.close()
   with sqlite3.connect(path) as cold:self.assertEqual(cold.execute('SELECT COUNT(*) FROM srs_state').fetchone()[0],21)
 def test_new_listening_resume_attempt_identity_and_skill_isolation(self):
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/'user.sqlite';u=sqlite3.connect(path)
   for name in ['user-schema-v1']+[f'user-migration-v{i}'for i in range(2,9)]:u.executescript((ROOT/f'Resources/{name}.sql').read_text())
   l=self.ids['listening'][0];payload=json.dumps({'current':l['question_id'],'source':l['example_id'],'heard':True,'revision':1,'contentVersion':12})
   u.execute(query('SQLiteListening','INSERT INTO listening_sessions'),['session','practice:beginner:2',payload,0])
   values=['session',l['question_id'],0,l['id'],'meaning','a','correct',0,100,200]
   u.execute(query('SQLiteListening','INSERT INTO listening_attempts'),values);u.commit()
   with self.assertRaises(sqlite3.IntegrityError):u.execute(query('SQLiteListening','INSERT INTO listening_attempts'),values)
   u.rollback();u.execute(query('SQLiteListening','INSERT INTO srs_state'),[l['id'],'calendar_steps',1,'{"stage":0}',200,100,100]);u.commit();u.close()
   with sqlite3.connect(path) as cold:
    self.assertEqual(cold.execute('SELECT state_json FROM listening_sessions').fetchone()[0],payload);self.assertEqual(cold.execute('SELECT skill,content_id FROM srs_state').fetchone(),('listening',l['id']))
 def test_new_bad_references_and_translations_rejected(self):
  original=json.loads((ROOT/'Content/production.json').read_text());target=self.ids['examples'][0]
  with tempfile.TemporaryDirectory() as tmp:
   for case in ['empty_ja','missing_relation','bad_pos']:
    d=copy.deepcopy(original)
    if case=='empty_ja':next(e for e in d['tables']['examples']if e['id']==target)['japanese']=''
    elif case=='missing_relation':d['tables']['vocabulary_examples'][-1]['meaning_id']=str(uuid.uuid4())
    else:next(v for v in d['tables']['vocabulary']if v['id']==self.ids['vocabulary'][0]['id'])['part_of_speech']='unknown'
    p=Path(tmp)/'bad.json';p.write_text(json.dumps(d,ensure_ascii=False))
    with self.subTest(case=case),self.assertRaises(ValidationError):build(p,Path(tmp)/'bad.sqlite',production=True)

 def test_retired_vocabulary_cannot_leak_into_active_production_pool(self):
  retired=self.ids['direct_input'][0]['vocabulary_id']
  scratch=sqlite3.connect(':memory:');self.db.backup(scratch)
  try:
   catalog=query('SQLiteProduction','SELECT DISTINCT v.id,v.headword')
   self.assertIn(retired,[r[0] for r in scratch.execute(catalog,[''])])
   scratch.execute('UPDATE content_items SET is_active=0 WHERE id=?',[retired])
   self.assertNotIn(retired,[r[0] for r in scratch.execute(catalog,[''])])
   self.assertEqual(scratch.execute(query('SQLiteProduction','SELECT q.*'),[retired]).fetchall(),[])
  finally:scratch.close()
