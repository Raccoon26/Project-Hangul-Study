"""DEV-06 actual repository SQL integration, not a Python scheduling implementation.
Native calendar/state-machine tests are SRSTests.swift and require Xcode.
"""
import json
import re
import sqlite3
import tempfile
import unittest
from pathlib import Path
from build_content import ROOT


class SRSSQLTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'user.sqlite'
        self.db = sqlite3.connect(self.path)
        self.db.execute('PRAGMA foreign_keys=ON')
        for name in ['user-schema-v1', 'user-migration-v2', 'user-migration-v3', 'user-migration-v4', 'user-migration-v5', 'user-migration-v6']:
            self.db.executescript((ROOT / f'Resources/{name}.sql').read_text())
        source = (ROOT / 'Repositories/SQLiteReviewProgress.swift').read_text()
        self.queries = re.findall(r'"([^"\n]+)"', source)
        self.study_sql = re.findall(r'"""(.*?)"""', (ROOT / 'Repositories/SQLiteProgressRepository.swift').read_text(), re.S)
    def tearDown(self): self.db.close(); self.temp.cleanup()
    def sql(self, prefix): return next(q for q in self.queries if q.startswith(prefix))
    def enroll(self, content_id='permanent-word-id', due=100, payload=None):
        self.db.execute(self.sql('INSERT INTO srs_state('), [content_id, 'calendar_steps', 1, json.dumps(payload or {'stage': 0}), due, 10])
    def session(self, ids=('permanent-word-id',)):
        with self.db:
            self.db.execute(self.sql('INSERT INTO review_sessions('), ['review-1', 100, 100])
            for n, content_id in enumerate(ids):
                self.db.execute(self.sql('INSERT INTO review_items('), ['review-1', content_id, n])
    def expose(self, content_id='permanent-word-id'):
        with self.db:
            self.db.execute(self.study_sql[0], ['event-' + content_id, content_id, 1, 100, '2026-10-01', 'Asia/Tokyo', 'vocabulary_review', 'viewed', 0, 'review-1', 5])
            self.db.execute(self.study_sql[1], [content_id, 100, 100, 1, 0, 0])
            self.db.execute(self.study_sql[2], ['2026-10-01', 'Asia/Tokyo', 1, 0, 0, 0])
            self.db.execute(self.sql('UPDATE review_items SET exposed_at='), [100, 'event-' + content_id, 'review-1', content_id])
    def reveal(self, content_id='permanent-word-id'):
        with self.db:
            self.db.execute(self.sql('UPDATE review_items SET revealed_at='), [101, 'review-1', content_id])
    def answer(self, content_id='permanent-word-id', rating='remembered', next_due=400):
        with self.db:
            self.db.execute(self.sql('UPDATE srs_state SET state_json='), [json.dumps({'stage': 1, 'nextReviewAt': next_due}), next_due, 102, 102, content_id, 'vocabulary'])
            self.db.execute(self.sql('UPDATE review_items SET result='), [rating, 102, next_due, 0, 1, 'Asia/Tokyo', '2026-10-01', 'review-1', content_id])
            remaining = self.db.execute(self.sql('SELECT COUNT(*) AS n FROM review_items WHERE session_id='), ['review-1']).fetchone()[0]
            self.db.execute(self.sql('UPDATE review_sessions SET status='), ['active' if remaining else 'completed', 102, None if remaining else 102, 'review-1'])
    def test_due_query_includes_past_and_exact_boundary_excludes_future(self):
        with self.db:
            self.enroll('past', 99); self.enroll('today', 100); self.enroll('future', 101)
        rows = self.db.execute(self.sql('SELECT content_id FROM srs_state WHERE'), ['calendar_steps', 1, 100, 20]).fetchall()
        self.assertEqual(rows, [('past',), ('today',)])
    def test_indexed_backlog_count_and_bounded_selection(self):
        with self.db:
            for n in range(15000): self.enroll(f'id-{n:05d}', n)
        sql = self.sql('SELECT content_id FROM srs_state WHERE')
        rows = self.db.execute(sql, ['calendar_steps', 1, 9999, 20]).fetchall()
        self.assertEqual(len(rows), 20)
        self.assertEqual(self.db.execute(self.sql('SELECT COUNT(*) AS n FROM srs_state WHERE'), ['calendar_steps', 1, 9999]).fetchone()[0], 10000)
        plan = ' '.join(str(x) for x in self.db.execute('EXPLAIN QUERY PLAN ' + sql, ['calendar_steps', 1, 9999, 20]))
        self.assertIn('idx_srs_skill_due', plan)
        self.assertNotIn('USE TEMP B-TREE', plan)
        self.session(tuple(row[0] for row in rows))
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM srs_state WHERE due_at<=9999').fetchone()[0], 10000)
    def test_reenrollment_does_not_reset_existing_stage_due_or_other_skill(self):
        with self.db:
            self.enroll(payload={'stage': 6}, due=999)
            self.enroll(payload={'stage': 0}, due=100)
            self.db.execute("INSERT INTO srs_state VALUES('permanent-word-id','grammar','future-policy',1,'{}',5,NULL,0)")
        rows = self.db.execute('SELECT skill,state_json,due_at FROM srs_state ORDER BY skill').fetchall()
        self.assertEqual(len(rows), 2)
        self.assertEqual(json.loads(rows[1][1])['stage'], 6); self.assertEqual(rows[1][2], 999)
    def test_reveal_requires_exposure_and_result_requires_reveal(self):
        self.enroll(); self.db.commit(); self.session()
        with self.assertRaises(sqlite3.IntegrityError): self.reveal()
        self.expose()
        with self.assertRaises(sqlite3.IntegrityError): self.answer()
        self.assertEqual(self.db.execute('SELECT due_at FROM srs_state').fetchone()[0], 100)
        self.reveal(); self.answer()
        self.assertEqual(self.db.execute('SELECT due_at FROM srs_state').fetchone()[0], 400)
    def test_resume_retains_snapshot_order_and_revealed_phase(self):
        self.session(('stable-b', 'stable-a')); self.expose('stable-b'); self.reveal('stable-b')
        self.db.close(); self.db = sqlite3.connect(self.path)
        rows = self.db.execute(self.sql('SELECT * FROM review_items WHERE'), ['review-1']).fetchall()
        self.assertEqual([row[1] for row in rows], ['stable-b', 'stable-a'])
        self.assertEqual(rows[0][3:5], (100, 101))
        self.assertIsNone(rows[0][5])
    def test_rating_and_completion_and_schedule_commit_together(self):
        self.enroll(); self.db.commit(); self.session(); self.expose(); self.reveal(); self.answer()
        self.assertEqual(self.db.execute('SELECT status,completed_at FROM review_sessions').fetchone(), ('completed', 102))
        self.assertEqual(self.db.execute('SELECT result,next_due_at FROM review_items').fetchone(), ('remembered', 400))
        self.assertEqual(self.db.execute('SELECT due_at,last_review_at FROM srs_state').fetchone(), (400, 102))
        self.assertEqual(self.db.execute('SELECT correct_count,incorrect_count,acquisition_status FROM item_progress').fetchone(), (0, 0, 'unassessed'))
    def test_invalid_rating_rolls_back_schedule_update(self):
        self.enroll(); self.db.commit(); self.session(); self.expose(); self.reveal()
        with self.assertRaises(sqlite3.IntegrityError): self.answer(rating='unknown')
        self.assertEqual(self.db.execute('SELECT due_at FROM srs_state').fetchone()[0], 100)
        self.assertIsNone(self.db.execute('SELECT result FROM review_items').fetchone()[0])
        self.assertEqual(self.db.execute('SELECT status FROM review_sessions').fetchone()[0], 'active')
    def test_single_active_session_per_skill(self):
        self.session()
        with self.assertRaises(sqlite3.IntegrityError):
            with self.db: self.db.execute(self.sql('INSERT INTO review_sessions('), ['review-2', 101, 101])
    def test_daily_count_uses_instant_range_and_overdue_uses_start_of_day(self):
        with self.db:
            self.enroll('old', 50); self.enroll('today', 100); self.enroll('future', 200)
        overdue = next(q for q in self.queries if q.startswith('SELECT COUNT(*) AS n FROM srs_state') and 'due_at<?' in q)
        self.assertEqual(self.db.execute(overdue, ['calendar_steps', 1, 100]).fetchone()[0], 1)
        self.session(('today',)); self.expose('today'); self.reveal('today'); self.answer('today')
        sql = self.sql('SELECT COUNT(*) AS n FROM review_items r JOIN review_sessions')
        self.assertEqual(self.db.execute(sql, [100, 103]).fetchone()[0], 1)
        self.assertEqual(self.db.execute(sql, [103, 200]).fetchone()[0], 0)
    def test_v4_migration_preserves_passes_favorites_and_existing_srs(self):
        db = sqlite3.connect(':memory:')
        try:
            for name in ['user-schema-v1', 'user-migration-v2', 'user-migration-v3', 'user-migration-v4']:
                db.executescript((ROOT / f'Resources/{name}.sql').read_text())
            db.execute("INSERT INTO favorites VALUES('stable',1)")
            db.execute("INSERT INTO vocabulary_sets VALUES('set','intro',1,1,1)")
            db.execute("INSERT INTO vocabulary_set_items VALUES('set','stable',0)")
            db.execute("INSERT INTO vocabulary_sessions VALUES('pass','set','{}',2,'completed',3)")
            db.execute("INSERT INTO srs_state VALUES('stable','vocabulary','other',1,'{}',3,NULL,1)")
            tables=['favorites','vocabulary_sets','vocabulary_set_items','vocabulary_sessions','srs_state']
            before={t:db.execute(f'SELECT * FROM {t}').fetchall() for t in tables}
            db.executescript((ROOT / 'Resources/user-migration-v5.sql').read_text())
            for t in tables:self.assertEqual(db.execute(f'SELECT * FROM {t}').fetchall(),before[t])
            self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0],5)
        finally: db.close()
    def test_backfill_marker_only_selects_unregistered_completed_passes(self):
        with self.db:
            self.db.execute("INSERT INTO vocabulary_sets VALUES('set','intro',1,1,1)")
            self.db.execute("INSERT INTO vocabulary_sessions VALUES('pass','set','{}',2,'completed',3)")
        sql = self.sql('SELECT state_json FROM vocabulary_sessions')
        self.assertEqual(len(self.db.execute(sql).fetchall()), 1)
        with self.db:self.db.execute(self.sql('INSERT INTO srs_enrolled_passes('), ['pass'])
        self.assertEqual(self.db.execute(sql).fetchall(), [])
    def test_all_queries_prepare_and_have_no_content_foreign_keys(self):
        for sql in self.queries:
            if sql.startswith(('SELECT ', 'INSERT ', 'UPDATE ')):
                self.db.execute('EXPLAIN ' + sql, [None] * sql.count('?')).fetchall()
        for table in ['review_sessions','review_items','srs_state']:
            self.assertNotIn('content_items', [r[2] for r in self.db.execute(f'PRAGMA foreign_key_list({table})')])

if __name__ == '__main__': unittest.main()
