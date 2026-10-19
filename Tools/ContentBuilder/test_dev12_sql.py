"""DEV12 executes repository SQL. Does not substitute for native lifecycle/UI tests."""
import json, sqlite3, tempfile, unittest, uuid
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from build_content import ROOT
from test_data05_content import query, queries
from test_lookup_sql import user

class Dev12SQLTests(unittest.TestCase):
 def setUp(self): self.d=user(version=10)
 def tearDown(self): self.d.close()
 def event(self,id,skill,outcome,at,content='word'):
  self.d.execute('INSERT INTO study_events VALUES(?,?,1,?,\'ignored-day\',\'UTC\',?,?,0,NULL,13)',[id,content,at,skill,outcome])
 def window(self,start,end):return self.d.execute(query('SQLiteStatistics','SELECT COUNT(CASE'),[start,end]).fetchone()
 def test_empty_statistics(self):
  self.assertEqual(self.window(0,100),(0,0,0,0,0,0,0))
  self.assertEqual(self.d.execute(next(q for q in queries('SQLiteStatistics') if '(SELECT COUNT(*) FROM review_items' in q),[0,100]*2).fetchone()[0],0)
 def test_event_bounds_accuracy_retry_and_no_self_rating_inflation(self):
  for args in [('before','vocabulary_pass','viewed',9),('start','vocabulary_pass','viewed',10),('pc','production_polite','correct',15),('pw','production_polite','incorrect',15),('lc','listening_meaning','correct',15),('lw','listening_dictation','incorrect',15),('retry','listening_retry','correct',15),('end','grammar_quiz_review','correct',20),('skip','grammar','skipped',15),('future','grammar','correct',21)]:self.event(*args)
  self.assertEqual(self.window(10,20),(7,4,2,1,1,1,1))
 def test_statistics_uses_time_index(self):
  plan=' '.join(str(r)for r in self.d.execute('EXPLAIN QUERY PLAN '+query('SQLiteStatistics','SELECT COUNT(CASE'),[0,100]))
  self.assertIn('idx_study_event_time',plan)
 def test_calendar_timezone_window_query(self):
  # Query receives absolute instants; stored event local_day/time_zone never dictates today's grouping.
  now=datetime(2026,3,9,0,30,tzinfo=ZoneInfo('America/New_York'))
  start=now.replace(hour=0,minute=0)-timedelta(days=1)
  self.assertEqual(now.timestamp()-start.timestamp(),23.5*3600)
  self.event('a','grammar','correct',start.timestamp())
  self.event('b','grammar','incorrect',start.timestamp()-1)
  self.assertEqual(self.window(start.timestamp(),now.timestamp())[:3],(1,1,0))
 def test_review_count_excludes_manual_and_listening_retry(self):
  for skill in ['vocabulary','grammar','vocabulary_practice','grammar_practice']:
   self.d.execute('INSERT INTO review_sessions VALUES(?,?,\'completed\',1,20,20)',[skill,skill])
   self.d.execute("INSERT INTO review_items(session_id,content_id,ordinal,exposed_at,revealed_at,result,reviewed_at,next_due_at,previous_stage,next_stage,time_zone,local_day) VALUES(?,'id',0,10,10,'remembered',20,100,0,1,'UTC','day')",[skill])
  self.d.execute("INSERT INTO listening_sessions VALUES('listen','review','{}',1)")
  for n,review,attempt in [(0,1,0),(1,1,1),(2,0,0)]:
   self.d.execute("INSERT INTO listening_attempts VALUES('listen',?,?,?,'dictation','x','correct',?,20,100)",[str(n),attempt,'item',review])
  self.assertEqual(self.d.execute(next(q for q in queries('SQLiteStatistics') if '(SELECT COUNT(*) FROM review_items' in q),[10,20]*2).fetchone()[0],3)
 def test_mastery_states_stay_separate(self):
  for n,skill,stage in [(0,'vocabulary',0),(1,'vocabulary',4),(2,'grammar',3),(3,'grammar',6)]:
   self.d.execute("INSERT INTO srs_state VALUES(?,?,'calendar_steps',1,?,100,0,0)",[str(n),skill,json.dumps({'stage':stage})])
  rows=self.d.execute(query('SQLiteStatistics','SELECT skill,COUNT'),['calendar_steps',1]).fetchall()
  self.assertEqual(sorted(rows),[('grammar',1,1),('vocabulary',1,1)])
 def test_maintenance_excludes_scheduled_future_due_active_and_recent(self):
  now=10000000;old=now-31*86400
  for n,name in enumerate(['old','recent','future-srs','due-srs','active']):
   self.d.execute('INSERT INTO item_progress(content_id,first_seen_at,last_seen_at) VALUES(?,1,?)',[name,now if name=='recent' else old])
   self.event('study-'+name,'vocabulary_practice','viewed',old,content=name)
   self.d.execute('INSERT INTO vocabulary_sets VALUES(?,\'intro\',?,1,0)',[name,n+1])
   self.d.execute('INSERT INTO vocabulary_set_items VALUES(?,?,0)',[name,name])
   self.d.execute("INSERT INTO vocabulary_sessions VALUES(?,?, '{}',0,?,1)",[name,name,'active' if name=='active' else 'completed'])
   self.d.execute("INSERT INTO vocabulary_events VALUES(?,?,?,1,'exposure',1)",[name,name,name])
  for name,due in [('future-srs',now+86400),('due-srs',now-86400)]:self.d.execute("INSERT INTO srs_state VALUES(?,'vocabulary','calendar_steps',1,'{}',?,1,1)",[name,due])
  sql=query('SQLiteStatistics','SELECT p.content_id FROM item_progress')
  self.assertEqual(self.d.execute(sql,[now-30*86400,5]).fetchall(),[('old',)])
 def test_unseen_only_counts_requested_active_ids_and_learning_events(self):
  self.event('a','vocabulary_pass','viewed',10,'active')
  self.event('b','grammar','viewed',10,'other-type')
  self.event('c','vocabulary_review','viewed',10,'retired')
  sql=query('SQLiteStatistics','SELECT COUNT(DISTINCT content_id) AS n').replace(r'\(slots)','?,?')
  self.assertEqual(self.d.execute(sql,['active','unseen']).fetchone()[0],1)
  self.assertEqual(self.d.execute(sql,['other-type','unseen']).fetchone()[0],0)
 def test_short_due_query_bounded_backlog(self):
  for n in range(100):self.d.execute("INSERT INTO srs_state VALUES(?,'vocabulary','calendar_steps',1,'{}',?,NULL,0)",[str(n),n])
  sql=query('SQLiteReviewProgress','SELECT content_id FROM srs_state')
  self.assertEqual(len(self.d.execute(sql,['calendar_steps',1,50,5]).fetchall()),5)
  self.assertEqual(self.d.execute("SELECT COUNT(*) FROM srs_state WHERE due_at<=50").fetchone()[0],51)
 def test_partial_review_four_of_twenty_cold_reopen(self):
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/'u.sqlite';d=user(path,10)
   d.execute("INSERT INTO review_sessions VALUES('s','vocabulary','active',0,10,NULL)")
   for n in range(20):d.execute("INSERT INTO review_items(session_id,content_id,ordinal) VALUES('s',?,?)",[str(n),n])
   for n in range(4):d.execute("UPDATE review_items SET exposed_at=1,revealed_at=2,result='remembered',reviewed_at=3,next_due_at=100,previous_stage=0,next_stage=1,time_zone='UTC',local_day='day' WHERE content_id=?",[str(n)])
   d.commit();d.close()
   d=sqlite3.connect(path)
   rows=d.execute(query('SQLiteReviewProgress','SELECT * FROM review_items'),['s']).fetchall()
   self.assertEqual(sum(r[5] is not None for r in rows),4)
   self.assertEqual(next(r[1]for r in rows if r[5] is None),'4')
   self.assertEqual(d.execute("SELECT status FROM review_sessions").fetchone()[0],'active');d.close()
 def test_additive_v10_preserves_all_tables(self):
  d=user(version=9)
  d.execute("INSERT INTO user_metadata VALUES('curriculum.profile.v1','saved')")
  d.execute("INSERT INTO srs_state VALUES('word','vocabulary','calendar_steps',1,'{\"stage\":4}',100,1,1)")
  d.execute("INSERT INTO listening_sessions VALUES('listening','review','{\"position\":2}',0)")
  d.execute("INSERT INTO favorites VALUES('word',1,'vocabulary')")
  tables=[r[0]for r in d.execute("SELECT name FROM sqlite_master WHERE type='table'")]
  before={t:d.execute('SELECT * FROM '+t).fetchall()for t in tables}
  d.executescript((ROOT/'Resources/user-migration-v10.sql').read_text())
  for t in tables:self.assertEqual(before[t],d.execute('SELECT * FROM '+t).fetchall(),t)
  self.assertEqual(d.execute('PRAGMA user_version').fetchone()[0],10);d.close()
 def test_lesson_content_release_update_preserves_cursor_results(self):
  self.d.execute("INSERT INTO lesson_sessions VALUES('s','lesson',12,1,'[\"a\",\"b\"]','b','active',1,2,NULL)")
  self.d.execute(query('SQLiteProgressRepository','UPDATE lesson_sessions SET content_version'),[13,'s'])
  self.assertEqual(self.d.execute('SELECT content_version,current_content_id,status,step_ids_json FROM lesson_sessions').fetchone(),(13,'b','active','["a","b"]'))
if __name__=='__main__':unittest.main()
