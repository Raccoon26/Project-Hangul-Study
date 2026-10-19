"""DEV11 real repository SQL + additive migration tests (not native UI execution)."""
import json,sqlite3,tempfile,time,unittest,uuid
from pathlib import Path
from build_content import ROOT
from test_data05_content import query

def user(path=':memory:',version=9):
 d=sqlite3.connect(path)
 for n in ['user-schema-v1']+[f'user-migration-v{i}' for i in range(2,version+1)]: d.executescript((ROOT/f'Resources/{n}.sql').read_text())
 return d
class LookupSQLTests(unittest.TestCase):
 def setUp(self):self.c=sqlite3.connect(ROOT/'Resources/content.sqlite')
 def tearDown(self):self.c.close()
 def search(self,term,offset=0):return self.c.execute(query('SQLiteLookup','WITH terms'),[term,term,term,offset]).fetchall()
 def title(self,row):return self.c.execute('SELECT '+('headword FROM vocabulary' if row[1]=='vocabulary' else 'pattern FROM grammar')+' WHERE id=?',[row[0]]).fetchone()[0]
 def test_korean_japanese_grammar_exact_prefix_contains_and_types(self):
  for term,head in [('학교','학교'),('学校','학교'),('먹다','먹다'),('食べる','먹다')]:
   rows=self.search(term);self.assertTrue(rows);self.assertEqual(self.title(rows[0]),head)
  for term in ['학','교','食','고 싶다','したい']:
   self.assertTrue(self.search(term),term)
  self.assertTrue(any(kind=='grammar' for id,kind in self.search('したい')))
  for term in ['존재하지않는검색어xyz',"' OR 1=1 --",'%','_']:
   self.assertEqual(self.search(term),[],term)
 def test_all_meanings_and_grammar_explanation_are_searchable(self):
  row=self.c.execute("SELECT m.vocabulary_id,m.meaning_ja FROM meanings m WHERE m.ordinal>0 ORDER BY length(m.meaning_ja) DESC LIMIT 1").fetchone()
  self.assertIn((row[0],'vocabulary'),self.search(row[1]))
  id,explanation=self.c.execute('SELECT id,explanation_ja FROM grammar ORDER BY length(explanation_ja) LIMIT 1').fetchone()
  self.assertIn((id,'grammar'),self.search(explanation.lower()))
 def test_ranking_is_exact_then_prefix_then_partial(self):
  sql=query('SQLiteLookup','WITH terms')
  db=sqlite3.connect(':memory:');self.c.backup(db)
  # An isolated synthetic query phrase lets the real query demonstrate all ranks.
  ids=[r[0]for r in db.execute('SELECT id FROM vocabulary LIMIT 3')]
  for id,term in zip(ids,['検査専用','検査専用の前方','後ろの検査専用']):db.execute('UPDATE vocabulary SET headword=? WHERE id=?',[term,id])
  self.assertEqual([r[0]for r in db.execute(sql,['検査専用']*3+[0])],ids);db.close()
 def test_search_pages_and_missing_typed_lookup(self):
  a=self.search('る');b=self.search('る',30);self.assertEqual(len(a),30);self.assertEqual(len(b),30);self.assertFalse(set(a)&set(b))
  sql=query('SQLiteLookup','SELECT i.level')
  for row in a:
   self.assertIsNotNone(self.c.execute(sql,row).fetchone())
   wrong='grammar' if row[1]=='vocabulary' else 'vocabulary';self.assertIsNone(self.c.execute(sql,[row[0],wrong]).fetchone())
  self.assertIsNone(self.c.execute(sql,['missing','vocabulary']).fetchone())
 def test_related_content_is_typed_active_and_links_both_modules(self):
  sql=query('SQLiteLookup','WITH related');cross=0
  for id,kind in self.c.execute("SELECT id,kind FROM content_items WHERE kind IN ('vocabulary','grammar') AND is_active=1"):
   rows=self.c.execute(sql,[id]*5).fetchall();self.assertLessEqual(len(rows),20);self.assertEqual(len(rows),len(set(rows)))
   for target,tk in rows:
    self.assertNotEqual(target,id);self.assertIsNotNone(self.c.execute(query('SQLiteLookup','SELECT i.level'),[target,tk]).fetchone());cross+=tk!=kind
  self.assertGreater(cross,0);self.assertEqual(self.c.execute(sql,['missing']*5).fetchall(),[])
 def test_favorites_v8_migration_idempotence_and_cold_reopen(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'u.sqlite';d=user(p,8);word='old-word'
   d.execute('INSERT INTO favorites VALUES(?,1)',[word]);d.execute("INSERT INTO user_metadata VALUES('curriculum.profile.v1','saved')")
   d.executescript((ROOT/'Resources/user-migration-v9.sql').read_text())
   self.assertEqual(d.execute('SELECT content_id,content_type FROM favorites').fetchall(),[(word,'vocabulary')])
   insert=query('SQLiteSavedContent','INSERT INTO favorites');grammar=str(uuid.uuid4())
   for _ in range(3):d.execute(insert,[grammar,2,'grammar'])
   d.commit();d.close();d=sqlite3.connect(p)
   self.assertEqual(d.execute('SELECT COUNT(*) FROM favorites').fetchone()[0],2)
   self.assertEqual(d.execute("SELECT value FROM user_metadata WHERE key='curriculum.profile.v1'").fetchone()[0],'saved')
   self.assertEqual(d.execute(query('SQLiteSavedContent','SELECT content_id,content_type FROM favorites'),['grammar','grammar',0]).fetchall(),[(grammar,'grammar')])
   d.execute(query('SQLiteSavedContent','DELETE FROM favorites'),[grammar,'vocabulary']);self.assertEqual(d.execute('SELECT COUNT(*) FROM favorites').fetchone()[0],2)
   d.execute(query('SQLiteSavedContent','DELETE FROM favorites'),[grammar,'grammar']);self.assertEqual(d.execute('SELECT COUNT(*) FROM favorites').fetchone()[0],1)
   self.assertEqual(d.execute('pragma user_version').fetchone()[0],9);d.close()
 def test_recent_is_bounded_deduplicated_and_not_learning(self):
  d=user();put=query('SQLiteSavedContent','INSERT INTO recent_content');trim=query('SQLiteSavedContent','DELETE FROM recent_content')
  for n in range(40):d.execute(put,[str(n),'grammar' if n%2 else 'vocabulary',n]);d.execute(trim)
  d.execute(put,['20','vocabulary',100]);d.execute(trim)
  rows=d.execute(query('SQLiteSavedContent','SELECT content_id,content_type FROM recent_content'),['','',0]).fetchall()
  self.assertEqual(len(rows),30);self.assertEqual(rows[0][0],'20')
  for table in ['srs_state','study_events','item_progress','vocabulary_sessions','grammar_sessions','listening_sessions','review_sessions']:
   self.assertEqual(d.execute('SELECT COUNT(*) FROM '+table).fetchone()[0],0)
  d.close()
 def test_difficult_uses_recent_repeated_failure_and_allows_recovery(self):
  d=user();now=10000000
  sql=query('SQLiteSavedContent','SELECT content_id,skill AS content_type')
  for id,changes,last in [('hard',{},now),('old',{},now-31*86400),('one',{'failureCount':1},now),('stable',{'stage':4},now),('recovered',{'consecutiveSuccesses':2,'lastResult':'remembered'},now),('future',{},now+1)]:
   state=dict(failureCount=2,consecutiveSuccesses=0,stage=0,lastResult='difficult');state.update(changes)
   d.execute("INSERT INTO srs_state VALUES(?,'vocabulary','step-v1',1,?,0,?,?)",[id,json.dumps(state),last,last])
  # Algorithm is declared centrally in Swift; SQL binding is the caller's value.
  self.assertEqual(d.execute(sql,['','','step-v1',1,now-30*86400,now,0]).fetchall(),[('hard','vocabulary')]);d.close()
 def test_manual_practice_identity_and_scheduled_review_are_independent(self):
  d=user();insert=query('SQLiteSavedContent','INSERT INTO review_sessions');items=query('SQLiteSavedContent','INSERT INTO review_items')
  ids=[str(uuid.uuid4()) for _ in range(3)]
  for id,skill in zip(ids,['vocabulary','vocabulary_practice','grammar_practice']):d.execute(insert,[id,skill,1,1]);d.execute(items,[id,'stable-content-id',0])
  self.assertEqual(d.execute(query('SQLiteSavedContent','SELECT id FROM review_sessions'),['vocabulary_practice']).fetchone()[0],ids[1])
  with self.assertRaises(sqlite3.IntegrityError):d.execute(insert,[str(uuid.uuid4()),'vocabulary_practice',1,1])
  with self.assertRaises(sqlite3.IntegrityError):d.execute(items,[ids[1],'stable-content-id',1])
  self.assertEqual(d.execute('SELECT COUNT(*) FROM srs_state').fetchone()[0],0)
  # Existing curriculum resume must route practice by saved session UUID, not by skill text.
  d.execute("UPDATE review_sessions SET status='completed' WHERE skill='vocabulary'")
  kind,target,level=d.execute(query('SQLiteCurriculum','SELECT kind,target,level')).fetchone();self.assertEqual(kind,'practice');self.assertIn(target,ids[1:]);d.close()
 def test_conjugation_override_queries_use_existing_authored_metadata(self):
  sql=query('SQLiteLookup','SELECT q.rubric_json')
  for id,lemma in self.c.execute("SELECT id,headword FROM vocabulary WHERE part_of_speech IN ('verb','adjective')"):
   values={}
   for row in self.c.execute(sql,[id]):
    for key,value in json.loads(row[0])['overrides'].items():
     self.assertTrue(value.strip());self.assertTrue(key not in values or values[key]==value,lemma);values[key]=value
 def test_v9_upgrade_preserves_all_existing_learning_snapshots_and_schedules(self):
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/'user.sqlite';d=user(path,8)
   vid=self.c.execute('SELECT id FROM vocabulary LIMIT 1').fetchone()[0]
   gid=self.c.execute('SELECT id FROM grammar LIMIT 1').fetchone()[0]
   lid=self.c.execute('SELECT id FROM listening_items LIMIT 1').fetchone()[0]
   snapshot=json.dumps({'position':2,'revision':7,'ids':[vid],'retry':[0],'contentVersion':13})
   d.execute("INSERT INTO vocabulary_sets VALUES('set','intro',1,1,2)")
   d.execute("INSERT INTO vocabulary_set_items VALUES('set',?,0)",[vid])
   d.execute("INSERT INTO vocabulary_sessions VALUES('word-session','set',?,7,'active',5)",[snapshot])
   d.execute("INSERT INTO grammar_sessions VALUES('grammar-session',?,?,7,'active',5)",[gid,snapshot])
   d.execute("INSERT INTO production_sessions VALUES('production-session',?,?,0)",[vid,snapshot])
   d.execute("INSERT INTO listening_sessions VALUES('listening-session','practice:intro',?,0)",[snapshot])
   d.execute("INSERT INTO review_sessions VALUES('review','grammar','active',1,5,NULL)")
   d.execute("INSERT INTO review_items(session_id,content_id,ordinal) VALUES('review',?,0)",[gid])
   for id,skill in [(vid,'vocabulary'),(gid,'grammar'),(lid,'listening')]:
    d.execute("INSERT INTO srs_state VALUES(?,?,'calendar_steps',1,?,1000,500,500)",[id,skill,json.dumps({'stage':4})])
   d.execute("INSERT INTO user_metadata VALUES(?,?)",["curriculum.profile.v1",json.dumps({"level":"beginner"})])
   tables=['vocabulary_sets','vocabulary_set_items','vocabulary_sessions','grammar_sessions','production_sessions','listening_sessions','review_sessions','review_items','srs_state','user_metadata']
   before={t:d.execute('SELECT * FROM '+t).fetchall()for t in tables}
   d.executescript((ROOT/'Resources/user-migration-v9.sql').read_text());d.commit();d.close()
   with sqlite3.connect(path) as cold:
    for t in tables:self.assertEqual(cold.execute('SELECT * FROM '+t).fetchall(),before[t],t)
    self.assertEqual(cold.execute('PRAGMA user_version').fetchone()[0],9)
    self.assertEqual(cold.execute(query('SQLiteCurriculum','SELECT kind,target,level')).fetchone(),('vocabulary','set','intro'))
if __name__=='__main__':unittest.main()
