"""DEV-10 executes the repository's actual SQL. Not native Swift/UI execution."""
import json,sqlite3,tempfile,unittest
from pathlib import Path
from build_content import ROOT
from test_data05_content import query

def user(path=':memory:'):
 d=sqlite3.connect(path)
 for n in ['user-schema-v1']+[f'user-migration-v{i}'for i in range(2,9)]:d.executescript((ROOT/f'Resources/{n}.sql').read_text())
 return d
class CurriculumSQLTests(unittest.TestCase):
 def setUp(self):self.db=sqlite3.connect(ROOT/'Resources/content.sqlite')
 def tearDown(self):self.db.close()
 def test_all_production_membership_paged_by_level_without_orphans(self):
  sql=query('SQLiteCurriculum','SELECT id FROM content_items')
  for kind,totals in [('vocabulary',{'intro':306,'beginner':800,'lower_intermediate':1181}),('grammar',{'intro':22,'beginner':20}),('listening',{'intro':34,'beginner':79,'lower_intermediate':1943}),('lesson',{'hangul':12,'intro':14,'lower_intermediate':47})]:
   for level,n in totals.items():
    ids=[];after=''
    while True:
     rows=self.db.execute(sql,[level,kind,after,kind]).fetchall();self.assertLessEqual(len(rows),200)
     if not rows:break
     ids += [r[0]for r in rows];after=rows[-1][0]
    self.assertEqual(len(ids),n);self.assertEqual(len(set(ids)),n)
   self.assertEqual(self.db.execute(sql,['master',kind,'',kind]).fetchall(),[])
 def test_curriculum_production_filter_uses_real_active_question_targets(self):
  sql=query('SQLiteCurriculum','SELECT DISTINCT v.id,v.headword');allids=[]
  for level in ['intro','beginner','lower_intermediate']:
   after=''
   while True:
    rows=self.db.execute(sql,[level,after]).fetchall();self.assertLessEqual(len(rows),30)
    if not rows:break
    allids += [r[0]for r in rows];after=rows[-1][0]
    for id,_ in rows:
     self.assertTrue(self.db.execute(query('SQLiteProduction','SELECT q.*'),[id]).fetchall())
  self.assertEqual(len(set(allids)),612)
  self.assertEqual(self.db.execute(sql,['advanced','']).fetchall(),[])
 def test_profile_skip_replacement_and_diagnostic_never_mutate_learning_tables(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'user.sqlite';d=user(p)
   d.execute("INSERT INTO srs_state VALUES('word','vocabulary','calendar_steps',1,'{\"stage\":4}',100,20,20)")
   d.execute("INSERT INTO srs_state VALUES('grammar','grammar','calendar_steps',1,'{\"stage\":2}',150,30,30)")
   d.execute("INSERT INTO srs_state VALUES('audio','listening','calendar_steps',1,'{\"stage\":3}',170,40,40)")
   d.execute("INSERT INTO favorites VALUES('word',10)");d.commit()
   tables=['srs_state','favorites','item_progress','study_events','lesson_progress','vocabulary_sessions','grammar_sessions','production_sessions','listening_sessions']
   before={t:d.execute('SELECT * FROM '+t).fetchall()for t in tables}
   get=query('SQLiteCurriculum','SELECT value FROM user_metadata');put=query('SQLiteCurriculum','INSERT INTO user_metadata')
   self.assertIsNone(d.execute(get,['curriculum.profile.v1']).fetchone())
   for level in ['intro','intermediate','maintenance','hangul']:
    data=json.dumps({'version':1,'level':level,'skippedHangul':level!='hangul'})
    d.execute(put,['curriculum.profile.v1',data]);d.execute(put,['curriculum.profile.v1',data])
   diagnostic=json.dumps({'id':'stable-session','items':['q1','q2'],'results':[True],'revision':1,'ended':False})
   d.execute(put,['curriculum.diagnostic.v1',diagnostic]);d.commit();d.close();d=sqlite3.connect(p)
   self.assertEqual(json.loads(d.execute(get,['curriculum.profile.v1']).fetchone()[0])['level'],'hangul')
   self.assertEqual(d.execute(get,['curriculum.diagnostic.v1']).fetchone()[0],diagnostic)
   self.assertEqual(d.execute('SELECT count(*) FROM user_metadata WHERE key LIKE "curriculum.%"').fetchone()[0],2)
   for t in tables:self.assertEqual(before[t],d.execute('SELECT * FROM '+t).fetchall())
   self.assertEqual(d.execute('PRAGMA user_version').fetchone()[0],8);d.close()
 def test_continue_routes_cover_modules_and_completed_sessions_drop_out(self):
  d=user();sql=query('SQLiteCurriculum','SELECT kind,target,level FROM')
  self.assertIsNone(d.execute(sql).fetchone())
  d.execute("INSERT INTO vocabulary_sets VALUES('set','beginner',1,10,0)")
  d.execute("INSERT INTO vocabulary_sessions VALUES('v','set','{}',0,'active',20)")
  d.execute("INSERT INTO grammar_sessions VALUES('g','grammar-lesson','{}',0,'active',30)")
  d.execute("INSERT INTO production_sessions VALUES('p','lemma','{}',0)")
  d.execute("INSERT INTO listening_sessions VALUES('l','practice:intro:3','{}',0)")
  d.execute("INSERT INTO lesson_sessions VALUES('h','hangul-lesson',13,1,'[]','char','active',10,40,NULL)")
  d.execute("INSERT INTO review_sessions VALUES('r','grammar','active',20,50,NULL)")
  for kind,target,table,update in [('review','grammar','review_sessions',"status='completed'"),('lesson','hangul-lesson','lesson_sessions',"status='completed'"),('grammar','grammar-lesson','grammar_sessions',"status='completed'"),('vocabulary','set','vocabulary_sessions',"status='completed'"),('production','lemma','production_sessions','completed=1'),('listening','practice:intro:3','listening_sessions','completed=1')]:
   self.assertEqual(d.execute(sql).fetchone()[:2],(kind,target));d.execute('UPDATE '+table+' SET '+update)
  self.assertIsNone(d.execute(sql).fetchone());d.close()
 def test_completion_not_exposure_skip_or_mastery(self):
  d=user();d.execute("INSERT INTO vocabulary_sets VALUES('set','intro',1,10,0)");d.execute("INSERT INTO vocabulary_set_items VALUES('set','word',0)")
  sql=query('SQLiteCurriculum','SELECT COUNT(DISTINCT i.content_id)').replace('\\(slots)','?')
  self.assertEqual(d.execute(sql,['word']).fetchone()[0],0)
  d.execute("UPDATE vocabulary_sets SET completed_count=2");self.assertEqual(d.execute(sql,['word']).fetchone()[0],1)
  stable=query('SQLiteCurriculum','SELECT COUNT(*) AS n FROM srs_state WHERE skill=').replace('\\(slots)','?')
  self.assertEqual(d.execute(stable,['vocabulary','word']).fetchone()[0],0)
  d.execute("INSERT INTO srs_state VALUES('word','vocabulary','calendar_steps',1,'{\"stage\":4}',100,10,10)")
  self.assertEqual(d.execute(stable,['vocabulary','word']).fetchone()[0],1)
  self.assertEqual(d.execute(stable,['grammar','word']).fetchone()[0],0)
  # New content changes the denominator only; completed IDs are not erased.
  self.assertEqual(d.execute(sql,['new-word']).fetchone()[0],0);self.assertEqual(d.execute(sql,['word']).fetchone()[0],1)
  d.close()
 def test_listening_completion_waits_for_full_session_and_deduplicates_repeats(self):
  d=user();sql=query('SQLiteCurriculum','SELECT COUNT(DISTINCT a.item_id)').replace('\\(slots)','?')
  d.execute("INSERT INTO listening_sessions VALUES('s','scope','{}',0)")
  d.execute("INSERT INTO listening_attempts VALUES('s','q',0,'item','meaning','b','incorrect',0,20,NULL)")
  self.assertEqual(d.execute(sql,['item']).fetchone()[0],0)
  d.execute("INSERT INTO listening_attempts VALUES('s','q',1,'item','meaning','a','correct',0,21,NULL)")
  d.execute("UPDATE listening_sessions SET completed=1")
  self.assertEqual(d.execute(sql,['item']).fetchone()[0],1);d.close()
