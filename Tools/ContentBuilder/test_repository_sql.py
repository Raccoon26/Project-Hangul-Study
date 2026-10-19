"""Runs actual multiline SQL extracted from Swift; this is not a Swift execution test."""
import re, sqlite3, unittest
from build_content import ROOT

class RepositorySQLTests(unittest.TestCase):
    def setUp(self):
        self.db=sqlite3.connect(':memory:')
        self.db.executescript((ROOT/'Resources/user-schema-v1.sql').read_text())
        source=(ROOT/'Repositories/SQLiteProgressRepository.swift').read_text()
        self.sql=re.findall(r'"""(.*?)"""',source,re.S)
    def tearDown(self): self.db.close()
    def record(self,event_id,outcome,stamp):
        studied=int(outcome!='skipped'); correct=int(outcome=='correct'); incorrect=int(outcome=='incorrect')
        with self.db:
            self.db.execute(self.sql[0],[event_id,'stable-id',1,stamp,'2026-09-30','Asia/Tokyo','recognition',outcome,1000,None,1])
            self.db.execute(self.sql[1],['stable-id',stamp,stamp,studied,correct,incorrect])
            self.db.execute(self.sql[2],['2026-09-30','Asia/Tokyo',studied,correct,incorrect,1000])
    def test_actual_repository_upsert_and_summary(self):
        self.record('1','correct',100)
        self.record('2','incorrect',200)
        self.record('3','skipped',50)
        self.assertEqual(self.db.execute(self.sql[3],[1000]).fetchone(),(2,1,1,0,0))
        self.assertEqual(self.db.execute('SELECT first_seen_at,last_seen_at FROM item_progress').fetchone(),(50,200))
        self.assertEqual(self.db.execute('SELECT study_count,correct_count,incorrect_count,duration_ms FROM daily_statistics').fetchone(),(2,1,1,3000))
    def test_atomic_rollback_on_late_failure(self):
        self.db.execute("CREATE TRIGGER reject_statistics BEFORE INSERT ON daily_statistics BEGIN SELECT RAISE(ABORT,'test failure'); END;")
        with self.assertRaises(sqlite3.IntegrityError): self.record('1','correct',100)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM study_events').fetchone()[0],0)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM item_progress').fetchone()[0],0)
    def test_due_index_semantics(self):
        self.db.execute("INSERT INTO srs_state VALUES('a','read','future',1,'{}',10,0,0)")
        self.db.execute("INSERT INTO srs_state VALUES('a','listen','future',1,'{}',20,0,0)")
        self.db.execute("INSERT INTO srs_state VALUES('b','read','future',1,'{}',NULL,NULL,0)")
        self.assertEqual(self.db.execute(self.sql[3],[30]).fetchone()[-1],1)
    def test_actual_content_queries(self):
        content=sqlite3.connect(f'file:{ROOT}/Resources/content-fixture.sqlite?mode=ro',uri=True)
        source=(ROOT/'Repositories/SQLiteContentRepository.swift').read_text()
        queries=re.findall(r'"""(.*?)"""',source,re.S)
        rows=content.execute(queries[0]+' ORDER BY v.sort_key,v.id LIMIT ?',[1]).fetchall()
        self.assertEqual(len(rows),1)
        next_rows=content.execute(queries[0]+' AND (v.sort_key>? OR (v.sort_key=? AND v.id>?)) ORDER BY v.sort_key,v.id LIMIT ?',[rows[0][3],rows[0][3],rows[0][0],1]).fetchall()
        self.assertEqual(len(next_rows),1)
        self.assertNotEqual(rows[0][0],next_rows[0][0])
        examples=content.execute(queries[1],['00000000-0000-4000-8000-000000000004']).fetchall()
        self.assertEqual(examples[0][1],'물을 마셔요')
        lessons=content.execute(queries[2],['00000000-0000-4000-8000-000000000006']).fetchall()
        self.assertEqual(lessons[0][2],2)
        content.close()

if __name__=='__main__': unittest.main()
