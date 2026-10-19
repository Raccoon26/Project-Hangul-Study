"""Execute the actual SQL strings in SQLiteProgressRepository against on-disk SQLite.
This validates SQL, constraints, transactions and reopen semantics, not Swift execution.
The native XCTest suite covers the repository's control flow on macOS/Xcode.
"""
import json, re, sqlite3, tempfile, unittest
from pathlib import Path
from build_content import ROOT

class LearningSQLTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.path=Path(self.temp.name)/'user.sqlite'
        self.db=sqlite3.connect(self.path)
        self.db.execute('PRAGMA foreign_keys=ON')
        for name in ['user-schema-v1','user-migration-v2','user-migration-v3']:
            self.db.executescript((ROOT/f'Resources/{name}.sql').read_text())
        source=(ROOT/'Repositories/SQLiteProgressRepository.swift').read_text()
        self.lines=re.findall(r'"([^"\n]+)"',source)
        self.multiline=re.findall(r'"""(.*?)"""',source,re.S)
    def tearDown(self): self.db.close(); self.temp.cleanup()
    def sql(self,prefix):
        return next(q for q in self.lines if q.startswith(prefix))
    def begin(self,session='session-1',steps=('first','second')):
        with self.db:
            self.db.execute(self.sql('INSERT INTO lesson_sessions('),[session,'lesson',3,123,json.dumps(steps),steps[0],1,1])
            self.db.execute(self.sql('INSERT INTO lesson_progress('),['lesson',1,steps[0]])
    def answer(self,step='first',outcome='correct',choice='answer',event='event-1'):
        with self.db:
            correct=int(outcome=='correct'); incorrect=int(outcome=='incorrect')
            self.db.execute(self.multiline[0],[event,step,1,2,'2026-09-30','Asia/Tokyo','hangul',outcome,0,'session-1',3])
            self.db.execute(self.multiline[1],[step,2,2,1,correct,incorrect])
            self.db.execute(self.multiline[2],['2026-09-30','Asia/Tokyo',1,correct,incorrect,0])
            self.db.execute(self.sql('INSERT INTO lesson_step_results('),['session-1',step,event,outcome,choice])
    def test_answer_and_cursor_survive_database_reopen(self):
        self.begin();self.answer()
        with self.db:
            self.db.execute(self.sql('UPDATE lesson_sessions SET current_content_id='),['second',3,'session-1'])
            self.db.execute(self.sql('UPDATE lesson_progress SET last_content_id='),['second','lesson'])
        self.db.close();self.db=sqlite3.connect(self.path)
        row=self.db.execute(self.sql('SELECT * FROM lesson_sessions WHERE lesson_id='),['lesson']).fetchone()
        self.assertEqual(row[3],123);self.assertEqual(row[5],'second')
        result=self.db.execute(self.sql('SELECT content_id,outcome,selected_choice_id'),['session-1']).fetchone()
        self.assertEqual(result,('first','correct','answer'))
        self.assertEqual(self.db.execute('SELECT last_content_id FROM lesson_progress').fetchone()[0],'second')
    def test_feedback_keeps_cursor_and_correct_incorrect_counters(self):
        self.begin();self.answer(outcome='incorrect',choice='wrong')
        self.assertEqual(self.db.execute('SELECT current_content_id FROM lesson_sessions').fetchone()[0],'first')
        self.assertEqual(self.db.execute(self.multiline[3],[100]).fetchone()[:3],(1,0,1))
    def test_late_result_failure_rolls_back_event_and_counters(self):
        self.begin()
        with self.assertRaises(sqlite3.IntegrityError): self.answer(outcome='viewed',choice='not-allowed')
        for table in ['study_events','item_progress','daily_statistics','lesson_step_results']:
            self.assertEqual(self.db.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0],0)
    def test_one_active_session_and_duplicate_answer_constraints(self):
        self.begin();self.answer()
        with self.assertRaises(sqlite3.IntegrityError): self.begin(session='session-2')
        with self.assertRaises(sqlite3.IntegrityError): self.answer(event='event-2')
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM study_events').fetchone()[0],1)
    def test_completion_and_repeat_preserve_prior_history(self):
        self.begin(steps=('first',));self.answer()
        with self.db:
            self.db.execute(self.sql("UPDATE lesson_sessions SET status='completed'"),[3,3,'session-1'])
            self.db.execute(self.sql("UPDATE lesson_progress SET status='completed'"),[3,'first','lesson'])
        self.begin(session='session-2',steps=('first',))
        self.assertEqual(self.db.execute('SELECT completed_count FROM lesson_progress').fetchone()[0],1)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM lesson_sessions').fetchone()[0],2)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM study_events').fetchone()[0],1)
    def test_content_database_replacement_does_not_change_progress(self):
        self.begin();self.answer()
        before=list(self.db.iterdump())
        content=Path(self.temp.name)/'content.sqlite'
        content.write_bytes((ROOT/'Resources/content.sqlite').read_bytes())
        content.unlink()
        content.write_bytes((ROOT/'Resources/content-fixture.sqlite').read_bytes())
        self.assertEqual(before,list(self.db.iterdump()))
        for table in ['lesson_progress','lesson_sessions','lesson_step_results']:
            targets=[x[2] for x in self.db.execute(f'PRAGMA foreign_key_list({table})')]
            self.assertNotIn('content_items',targets)
    def test_v2_migration_keeps_existing_records(self):
        with sqlite3.connect(':memory:') as db:
            db.executescript((ROOT/'Resources/user-schema-v1.sql').read_text())
            db.executescript((ROOT/'Resources/user-migration-v2.sql').read_text())
            db.execute("INSERT INTO favorites VALUES('retired-id',1)")
            db.execute("INSERT INTO lesson_progress VALUES('legacy-lesson','completed',1,2,'legacy-step')")
            db.executescript((ROOT/'Resources/user-migration-v3.sql').read_text())
            self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0],3)
            self.assertEqual(db.execute('SELECT * FROM lesson_progress').fetchone(),('legacy-lesson','completed',1,2,'legacy-step',1))
            self.assertEqual(db.execute('SELECT content_id FROM favorites').fetchone()[0],'retired-id')
    def test_result_requires_user_session_and_event(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute(self.sql('INSERT INTO lesson_step_results('),['missing','stable-id','missing','correct','answer'])

if __name__=='__main__': unittest.main()
