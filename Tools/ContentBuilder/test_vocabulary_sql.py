"""Execute DEV-05's actual repository SQL, not a Python copy of its learning engine.
Swift engine/control-flow tests are in VocabularyPassTests.swift and require Xcode.
"""
import json
import re
import shutil
import sqlite3
import tempfile
import unittest
from pathlib import Path
from build_content import ROOT


def literals(path):
    return re.findall(r'"([^"\n]+)"', path.read_text())


class VocabularySQLTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'progress.sqlite'
        self.db = sqlite3.connect(self.path)
        self.db.execute('PRAGMA foreign_keys=ON')
        for name in ['user-schema-v1', 'user-migration-v2', 'user-migration-v3', 'user-migration-v4']:
            self.db.executescript((ROOT / f'Resources/{name}.sql').read_text())
        self.content = sqlite3.connect(f'file:{ROOT / "Resources/content.sqlite"}?mode=ro', uri=True)
        self.queries = literals(ROOT / 'Repositories/SQLiteVocabularyProgress.swift')
        self.content_queries = literals(ROOT / 'Repositories/SQLiteVocabularyContent.swift')
        self.ids = [r[0] for r in self.content.execute('SELECT v.id FROM vocabulary v JOIN content_items i ON i.id=v.id WHERE i.is_active=1 AND i.level=? ORDER BY v.sort_key,v.id LIMIT 20', ['intro'])]

    def tearDown(self):
        self.db.close(); self.content.close(); self.temp.cleanup()

    def sql(self, prefix, content=False):
        return next(q for q in (self.content_queries if content else self.queries) if q.startswith(prefix))

    def create_set(self, set_id='set-1', ids=None, number=1):
        with self.db:
            self.db.execute(self.sql('INSERT INTO vocabulary_sets('), [set_id, 'intro', number, 1])
            for n, content_id in enumerate(self.ids if ids is None else ids):
                self.db.execute(self.sql('INSERT INTO vocabulary_set_items('), [set_id, content_id, n])

    def start(self):
        self.create_set()
        # This opaque JSON fixture proves byte-preserving storage, not Swift Codable behavior.
        state = dict(setID='set-1', vocabularyIDs=self.ids, round=2, position=12,
                     revealed=True, deferred=self.ids[:3], totalExposures=33)
        with self.db:
            self.db.execute(self.sql('INSERT INTO vocabulary_sessions('), ['session-1', 'set-1', json.dumps(state), 9, 2])
            self.db.execute(self.sql('INSERT INTO learning_passes('), ['pass-1', 'set-1', 1, 1])
            for content_id in self.ids:
                self.db.execute(self.sql('INSERT INTO pass_items('), ['pass-1', content_id])
        return state

    def test_real_cards_have_ordered_meanings_examples_and_optional_notes(self):
        count = self.content.execute(self.sql('SELECT COUNT(*) AS count', True), ['intro']).fetchone()[0]
        self.assertEqual(count, 306)
        notes = 0
        for (content_id,) in self.content.execute('SELECT id FROM vocabulary'):
            card = self.content.execute(self.sql('SELECT v.headword', True), [content_id]).fetchone()
            self.assertTrue(card[0]); self.assertGreater(card[2], 0)
            meaning_rows = self.content.execute(self.sql('SELECT m.*', True), [content_id]).fetchall()
            self.assertGreater(len(meaning_rows), 0)
            for meaning in meaning_rows:
                example = self.content.execute(self.sql('SELECT e.id', True), [meaning[0]]).fetchone()
                self.assertTrue(example[1]); self.assertTrue(example[2])
            notes += len(self.content.execute(self.sql('SELECT n.id', True), [content_id]).fetchall())
        self.assertEqual(notes, 528)

    def test_set_membership_is_ordered_stable_and_allocation_race_rolls_back(self):
        self.create_set()
        rows = self.db.execute(self.sql('SELECT content_id FROM vocabulary_set_items WHERE set_id='), ['set-1']).fetchall()
        self.assertEqual([r[0] for r in rows], self.ids)
        with self.assertRaises(sqlite3.IntegrityError): self.create_set('set-2', number=2)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM vocabulary_sets').fetchone()[0], 1)

    def test_reopen_keeps_exact_opaque_state_and_stable_ids(self):
        state = self.start()
        self.db.close(); self.db = sqlite3.connect(self.path)
        row = self.db.execute(self.sql('SELECT * FROM vocabulary_sessions WHERE id='), ['session-1']).fetchone()
        self.assertEqual(json.loads(row[2]), state)
        self.assertEqual(row[3], 9)
        self.assertEqual(json.loads(row[2])['vocabularyIDs'][12], self.ids[12])

    def test_resume_shortcut_selects_latest_active_set_without_loading_catalog(self):
        self.start()
        self.assertEqual(self.db.execute(self.sql('SELECT s.set_id'), ['intro']).fetchone()[0], 'set-1')
        with self.db:
            self.db.execute(self.sql('UPDATE vocabulary_sessions SET state_json='), ['{}', 10, 'completed', 4, 'session-1'])
        self.assertIsNone(self.db.execute(self.sql('SELECT s.set_id'), ['intro']).fetchone())

    def test_one_active_attempt_and_unique_event_constraints(self):
        self.start()
        with self.assertRaises(sqlite3.IntegrityError):
            with self.db: self.db.execute(self.sql('INSERT INTO vocabulary_sessions('), ['session-2', 'set-1', '{}', 0, 3])
        event_sql = self.sql('INSERT INTO vocabulary_events(')
        with self.db: self.db.execute(event_sql, ['e1', 'session-1', self.ids[0], 1, 'known', 3])
        with self.assertRaises(sqlite3.IntegrityError):
            with self.db: self.db.execute(event_sql, ['e2', 'session-1', self.ids[0], 1, 'known', 4])
        with self.db: self.db.execute(event_sql, ['e3', 'session-1', None, 1, 'round_completed', 3])
        with self.assertRaises(sqlite3.IntegrityError):
            with self.db: self.db.execute(event_sql, ['e4', 'session-1', None, 1, 'round_completed', 4])

    def test_event_kind_requires_correct_target_and_real_user_session(self):
        self.start()
        for content_id, kind, session in [(None, 'exposure', 'session-1'), (self.ids[0], 'set_completed', 'session-1'), (self.ids[0], 'known', 'missing')]:
            with self.assertRaises(sqlite3.IntegrityError):
                with self.db: self.db.execute(self.sql('INSERT INTO vocabulary_events('), ['bad', session, content_id, 1, kind, 3])

    def test_completion_transaction_rolls_back_on_late_failure(self):
        self.start()
        with self.assertRaises(sqlite3.IntegrityError):
            with self.db:
                self.db.execute(self.sql('UPDATE pass_items SET completed_at='), [3, 'pass-1', self.ids[0]])
                self.db.execute(self.sql('UPDATE vocabulary_sets SET completed_count='), ['set-1'])
                self.db.execute(self.sql('INSERT INTO vocabulary_events('), ['event', 'session-1', None, 1, 'set_completed', 3])
                self.db.execute(self.sql('UPDATE vocabulary_sessions SET state_json='), ['{}', 10, 'invalid', 3, 'session-1'])
        self.assertEqual(self.db.execute('SELECT completed_count FROM vocabulary_sets').fetchone()[0], 0)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM vocabulary_events').fetchone()[0], 0)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM pass_items WHERE completed_at IS NOT NULL').fetchone()[0], 0)
        self.assertEqual(self.db.execute('SELECT revision FROM vocabulary_sessions').fetchone()[0], 9)

    def test_completion_and_repeat_preserve_history_without_srs_mastery(self):
        self.start()
        with self.db:
            self.db.execute(self.sql('UPDATE vocabulary_sets SET completed_count='), ['set-1'])
            self.db.execute(self.sql('UPDATE vocabulary_sessions SET state_json='), ['{"completed":true}', 10, 'completed', 3, 'session-1'])
            self.db.execute(self.sql('INSERT INTO vocabulary_sessions('), ['session-2', 'set-1', '{}', 0, 4])
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM vocabulary_sessions').fetchone()[0], 2)
        self.assertEqual(self.db.execute('SELECT completed_count FROM vocabulary_sets').fetchone()[0], 1)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM srs_state').fetchone()[0], 0)

    def test_migration_preserves_legacy_progress_and_audio_lesson_state(self):
        db = sqlite3.connect(':memory:')
        try:
            for version in ['user-schema-v1', 'user-migration-v2', 'user-migration-v3']:
                db.executescript((ROOT / f'Resources/{version}.sql').read_text())
            db.execute("INSERT INTO favorites VALUES('retired-stable-id',1)")
            db.execute("INSERT INTO lesson_progress VALUES('hangul-lesson','completed',1,2,'last-step',1)")
            db.execute("INSERT INTO lesson_sessions VALUES('s','pronunciation-lesson',5,42,'[\"step\"]','step','active',1,2,NULL)")
            before = {t: db.execute(f'SELECT * FROM {t}').fetchall() for t in ['favorites', 'lesson_progress', 'lesson_sessions']}
            db.executescript((ROOT / 'Resources/user-migration-v4.sql').read_text())
            self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0], 4)
            for table, rows in before.items(): self.assertEqual(db.execute(f'SELECT * FROM {table}').fetchall(), rows)
        finally: db.close()

    def test_content_replacement_has_no_user_foreign_key_or_write(self):
        self.start()
        before = list(self.db.iterdump())
        replacement = Path(self.temp.name) / 'content.sqlite'
        shutil.copyfile(ROOT / 'Resources/content.sqlite', replacement)
        with sqlite3.connect(replacement) as other:
            other.execute("UPDATE vocabulary SET sort_key='reordered-'||id")
            other.execute('UPDATE content_metadata SET content_version=content_version+1')
        self.assertEqual(before, list(self.db.iterdump()))
        for table in ['vocabulary_sets', 'vocabulary_set_items', 'vocabulary_sessions', 'vocabulary_events']:
            self.assertNotIn('content_items', [r[2] for r in self.db.execute(f'PRAGMA foreign_key_list({table})')])

    def test_all_production_ids_partition_into_bounded_sets(self):
        rows = self.content.execute('SELECT v.id FROM vocabulary v JOIN content_items i ON i.id=v.id WHERE i.level=? AND i.is_active=1 ORDER BY v.sort_key,v.id', ['intro']).fetchall()
        for start in range(0, len(rows), 20):
            self.create_set(f'set-{start}', [r[0] for r in rows[start:start + 20]], start // 20 + 1)
        counts = [r[0] for r in self.db.execute('SELECT COUNT(*) FROM vocabulary_set_items GROUP BY set_id')]
        self.assertEqual(sorted(counts), [6] + [20] * 15)
        self.assertEqual(sum(counts), 306)

    def test_actual_repository_queries_prepare_against_correct_databases(self):
        # EXPLAIN checks all SQL including queries exercised only by native tests.
        for queries, db in [(self.queries, self.db), (self.content_queries, self.content)]:
            for sql in queries:
                if not sql.startswith(('SELECT ', 'INSERT ', 'UPDATE ')): continue
                sql = sql.replace('\\(placeholders)', '?')
                db.execute('EXPLAIN ' + sql, [None] * sql.count('?')).fetchall()


if __name__ == '__main__': unittest.main()
