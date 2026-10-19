"""DEV14 executes SQLite queries/constraints and real subprocess durability checks.
These tests do not claim to execute Swift, StoreKit, SwiftUI or device lifecycle.
"""
import json, os, re, sqlite3, subprocess, sys, tempfile, unittest
from pathlib import Path
from build_content import ROOT
from test_data05_content import query
from test_lookup_sql import user

class Dev14AuditTests(unittest.TestCase):
 def test_grammar_answer_refreshes_continue_timestamp(self):
  code=(ROOT/'Repositories/SQLiteGrammarProgress.swift').read_text().split('func answerGrammarReview',1)[1]
  sql=re.search(r'db.execute\("(UPDATE review_sessions SET updated_at=[^"]+)"',code).group(1)
  d=user(version=10)
  d.execute("INSERT INTO review_sessions VALUES('g','grammar','active',1,1,NULL)")
  d.execute("INSERT INTO production_sessions VALUES('p','lemma',?,0)",[json.dumps({'updatedAt':20-978307200})])
  resume=query('SQLiteCurriculum','SELECT kind,target,level FROM')
  self.assertEqual(d.execute(resume).fetchone()[0],'production')
  d.execute(sql,[30,'g'])
  self.assertEqual(d.execute(resume).fetchone()[:2],('review','grammar'))
  d.close()
 def test_production_retry_does_not_inflate_first_attempt_accuracy(self):
  d=user(version=10)
  for i,(skill,result) in enumerate([('production_present','incorrect'),('production_retry_present','correct'),('production_past','correct')]):
   d.execute("INSERT INTO study_events VALUES(?, 'word',1,20,'day','UTC',?,?,0,'s',13)",[str(i),skill,result])
  row=d.execute(query('SQLiteStatistics','SELECT COUNT(CASE'),[10,30]).fetchone()
  self.assertEqual(row[:5],(3,2,1,1,1)) # overall actions include practice; first attempt metric does not.
  source=(ROOT/'Repositories/SQLiteProduction.swift').read_text()
  self.assertIn('s.retrying ? "production_retry_" : "production_"',source)
  d.close()
 def test_snapshot_lookup_is_content_independent_and_preserves_retry(self):
  d=user(version=10)
  payload=json.dumps({'id':'session','position':3,'retry':[0,1],'answer':'먹어요','contentVersion':12})
  d.execute("INSERT INTO production_sessions VALUES('session','word',?,0)",[payload])
  sql=query('SQLiteProduction','SELECT state_json FROM production_sessions WHERE scope_id=')
  self.assertEqual(d.execute(sql,['word']).fetchone()[0],payload)
  self.assertIsNone(d.execute(sql,['absent']).fetchone())
  d.execute('UPDATE production_sessions SET completed=1')
  self.assertIsNone(d.execute(sql,['word']).fetchone())
  ui=(ROOT/'Views/ProductionView.swift').read_text()
  self.assertLess(ui.index('activeProduction(scope:'),ui.index('productionQuestions(id:'))
  d.close()
 def test_ui_never_interpolates_raw_error_descriptions(self):
  for folder in ['Views','ViewModels']:
   for p in (ROOT/folder).glob('*.swift'):
    self.assertNotIn('error.localizedDescription',p.read_text(),str(p))
 def test_mismatched_dataset_gate_precedes_migration(self):
  source=(ROOT/'Repositories/SQLiteProgressRepository.swift').read_text()
  self.assertLess(source.index('existing.text("value") == datasetID'),source.index('UserDatabaseMigration.migrate'))
 def test_consent_delay_is_cancelled_when_purchase_screen_leaves(self):
  service=(ROOT/'Services/AdService.swift').read_text()
  self.assertIn('privacyPresentationID == presentationID',service)
  self.assertLess(service.index('privacyPresentationID == presentationID'),service.index('ConsentForm.presentPrivacyOptionsForm'))
  view=(ROOT/'Views/RemoveAdsView.swift').read_text()
  self.assertIn('.onDisappear { ads.cancelPrivacyPresentation() }',view)
  self.assertIn('if $0 != .active { ads.cancelPrivacyPresentation() }',view)
 def test_forced_process_exit_keeps_four_answers_not_entire_session(self):
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/'user.sqlite';d=user(path,10)
   d.execute("INSERT INTO review_sessions VALUES('s','vocabulary','active',1,1,NULL)")
   for n in range(20):d.execute("INSERT INTO review_items(session_id,content_id,ordinal) VALUES('s',?,?)",[str(n),n])
   d.commit();d.close()
   code='''import sqlite3,sys,os
c=sqlite3.connect(sys.argv[1]);c.execute('PRAGMA journal_mode=WAL');c.execute('PRAGMA synchronous=FULL')
for n in range(4):
 c.execute('BEGIN IMMEDIATE')
 c.execute("UPDATE review_items SET exposed_at=2,revealed_at=2,result='remembered',reviewed_at=2,next_due_at=100,previous_stage=0,next_stage=1,time_zone='Asia/Tokyo',local_day='2026-10-05' WHERE session_id='s' AND content_id=?",[str(n)])
 c.commit()
c.execute('BEGIN IMMEDIATE');c.execute("UPDATE review_sessions SET status='completed' WHERE id='s'")
os._exit(0)
'''
   subprocess.run([sys.executable,'-c',code,str(path)],check=True)
   d=sqlite3.connect(path)
   self.assertEqual(d.execute("SELECT count(*) FROM review_items WHERE result IS NOT NULL").fetchone()[0],4)
   self.assertEqual(d.execute("SELECT count(*) FROM review_items WHERE result IS NULL").fetchone()[0],16)
   self.assertEqual(d.execute('SELECT status FROM review_sessions').fetchone()[0],'active')
   self.assertEqual(d.execute('PRAGMA integrity_check').fetchone()[0],'ok');d.close()
 def test_each_historical_user_schema_migrates_without_losing_srs_favorites(self):
  for version in range(1,11):
   with self.subTest(version=version):
    d=user(version=version)
    d.execute("INSERT INTO user_metadata VALUES('dataset_id','ko-ja-core')")
    d.execute("INSERT INTO favorites(content_id,created_at) VALUES('keep',1)")
    d.execute("INSERT INTO srs_state VALUES('keep','vocabulary','calendar_steps',1,'{\"stage\":4}',999,1,1)")
    before=d.execute('SELECT * FROM srs_state').fetchall()
    for target in range(version+1,11):d.executescript((ROOT/f'Resources/user-migration-v{target}.sql').read_text())
    self.assertEqual(d.execute('SELECT * FROM srs_state').fetchall(),before)
    self.assertEqual(d.execute('SELECT content_id,created_at FROM favorites').fetchall(),[('keep',1)])
    self.assertEqual(d.execute('PRAGMA user_version').fetchone()[0],10)
    self.assertEqual(d.execute('PRAGMA foreign_key_check').fetchall(),[]);d.close()
 def test_listening_due_excludes_unsupported_algorithms_and_uses_index(self):
  d=user(version=10)
  for id,algorithm,version in [('known','calendar_steps',1),('future','calendar_steps',2),('other','other',1)]:
   d.execute("INSERT INTO srs_state VALUES(?,'listening',?,?, '{}',1,NULL,1)",[id,algorithm,version])
  sql=query('SQLiteListening',"SELECT content_id FROM srs_state WHERE skill='listening'")
  self.assertEqual(d.execute(sql,['calendar_steps',1,10]).fetchall(),[('known',)])
  plan=' '.join(str(r) for r in d.execute('EXPLAIN QUERY PLAN '+sql,['calendar_steps',1,10]))
  self.assertIn('idx_srs_skill_due',plan)
  self.assertEqual(d.execute('SELECT count(*) FROM srs_state').fetchone()[0],3)
  d.close()
 def test_duplicate_constraints_actually_reject_invalid_writes(self):
  d=user(version=10)
  d.execute("INSERT INTO srs_state VALUES('same','vocabulary','calendar_steps',1,'{}',1,NULL,1)")
  with self.assertRaises(sqlite3.IntegrityError):d.execute("INSERT INTO srs_state VALUES('same','vocabulary','calendar_steps',1,'{}',1,NULL,1)")
  d.execute("INSERT INTO review_sessions VALUES('one','grammar','active',1,1,NULL)")
  with self.assertRaises(sqlite3.IntegrityError):d.execute("INSERT INTO review_sessions VALUES('two','grammar','active',1,1,NULL)")
  d.close()
if __name__=='__main__':unittest.main()
