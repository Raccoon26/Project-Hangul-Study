"""DATA-08-C bundle, release preservation and actual repository SQL contracts.

These tests exercise SQLite, not the Swift engine or iOS lifecycle.
"""
import collections
import copy
import hashlib
import json
import shutil
import sqlite3
import tempfile
import unittest
import unicodedata
import uuid
from pathlib import Path

from build_content import ROOT, build
from validator import ValidationError, signatures
from test_data05_content import query
from test_lookup_sql import user


class Data08BatchCTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = sqlite3.connect((ROOT/'Resources/content.sqlite').as_uri()+'?mode=ro', uri=True)
        cls.previous = ROOT/'Tests/Fixtures/content-v16-production.sqlite'
        cls.old = sqlite3.connect(cls.previous.as_uri()+'?mode=ro', uri=True)
        cls.registry = json.loads((ROOT/'Content/data08-c-ids.json').read_text())
        cls.words = {v['headword']: v for v in cls.registry['vocabulary']}
        cls.approved = set(json.loads((ROOT/'Content/data08-c-revised-ids.json').read_text()))

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        cls.old.close()

    def test_strict_source_rebuild_and_exact_release_delta(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)/'content.sqlite'
            result = build(ROOT/'Content/production.json', output, self.previous, production=True)
            self.assertEqual(result['validation']['error_count'], 0)
            self.assertEqual(result['validation']['warning_count'], 10)
            with sqlite3.connect(output) as rebuilt:
                self.assertEqual(signatures(rebuilt), signatures(self.db))
        deltas = dict(vocabulary=310, meanings=334, examples=619, learner_notes=146,
                      grammar=0, grammar_examples=17, questions=0, listening_items=0,
                      content_items=1412, vocabulary_examples=620)
        for table, delta in deltas.items():
            with self.subTest(table=table):
                self.assertEqual(self.db.execute('SELECT COUNT(*) FROM '+table).fetchone()[0]
                                 - self.old.execute('SELECT COUNT(*) FROM '+table).fetchone()[0], delta)
        self.assertEqual(self.db.execute('SELECT schema_version,content_version,min_reader_version,is_fixture,dataset_id FROM content_metadata').fetchone(),
                         (4, 17, 7, 0, 'ko-ja-core'))
        self.assertEqual(self.db.execute('PRAGMA integrity_check').fetchall(), [('ok',)])
        self.assertEqual(self.db.execute('PRAGMA foreign_key_check').fetchall(), [])

    def test_previous_release_bytes_and_all_existing_rows_preserved(self):
        self.assertEqual(hashlib.sha256(self.previous.read_bytes()).hexdigest(),
                         '112d3662f79a72ca61ad7140a5d937396c0bc9f71180dd5f35a403a040a91f29')
        before, after = signatures(self.old), signatures(self.db)
        self.assertTrue(set(before) <= set(after))
        self.assertEqual({i for i in before if before[i] != after[i]}, self.approved)
        self.assertEqual(len(self.approved), 46)
        for row in self.old.execute('SELECT * FROM content_items'):
            current = self.db.execute('SELECT * FROM content_items WHERE id=?', [row[0]]).fetchone()
            self.assertEqual(current[:2]+current[3:-1], row[:2]+row[3:-1])
            self.assertEqual(current[2], row[2]+int(row[0] in self.approved))
            if row[0] not in self.approved:
                self.assertEqual(current, row)
        tables = [r[0] for r in self.old.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
        for table in tables:
            if table in ('content_items', 'content_metadata', 'vocabulary_search'):
                continue
            with self.subTest(table=table):
                self.assertTrue(set(self.old.execute('SELECT * FROM '+table))
                                <= set(self.db.execute('SELECT * FROM '+table)))

    def test_real_batch_size_uuid_level_and_pos_balance(self):
        self.assertEqual(len(self.words), 310)
        self.assertEqual(len(self.registry['examples']), 619)
        self.assertEqual(collections.Counter(v['part_of_speech'] for v in self.words.values()),
                         dict(verb=138, adjective=45, adverb=44, expression=30, noun=53))
        new_ids = set(signatures(self.db)) - set(signatures(self.old))
        self.assertEqual(len(new_ids), 1412)
        for item_id in new_ids:
            self.assertEqual(str(uuid.UUID(item_id)), item_id)
            self.assertEqual(uuid.UUID(item_id).version, 4)
            self.assertEqual(self.db.execute('SELECT level,revision,is_active FROM content_items WHERE id=?', [item_id]).fetchone(),
                             ('lower_intermediate', 1, 1))
        self.assertTrue({v['id'] for v in self.words.values()} <= new_ids)
        self.assertEqual({v['theme'] for v in self.words.values()},
                         {'現代生活・デジタル・メディア', '仕事・計画・協働', '社会・抽象表現・日常会話'})

    def test_no_new_normalized_headword_or_sentence_duplicates(self):
        def norm(s):
            return ' '.join(unicodedata.normalize('NFC', s).casefold().split())
        old_heads = {norm(r[0]) for r in self.old.execute('SELECT headword FROM vocabulary')}
        old_sentences = {norm(r[0]) for r in self.old.execute('SELECT korean FROM examples')}
        heads = [norm(v['headword']) for v in self.words.values()]
        self.assertEqual(len(set(heads)), 310)
        self.assertFalse(old_heads & set(heads))
        sentences = []
        pairs = []
        for item_id in self.registry['examples']:
            ko, ja = self.db.execute('SELECT korean,japanese FROM examples WHERE id=?', [item_id]).fetchone()
            self.assertTrue(ko.strip() and ja.strip())
            self.assertEqual(ko, unicodedata.normalize('NFC', ko))
            self.assertEqual(ja, unicodedata.normalize('NFC', ja))
            sentences.append(norm(ko))
            pairs.append((norm(ko), norm(ja)))
        self.assertEqual(len(set(sentences)), 619)
        self.assertEqual(len(set(pairs)), 619)
        self.assertFalse(old_sentences & set(sentences))

    def test_every_card_meaning_example_and_note_uses_real_repository_sql(self):
        polysemous = 0
        for word in self.words.values():
            card = self.db.execute(query('SQLiteVocabularyContent', 'SELECT v.headword'), [word['id']]).fetchone()
            self.assertEqual(card[:2], (word['headword'], word['part_of_speech']))
            meanings = self.db.execute(query('SQLiteVocabularyContent', 'SELECT m.*'), [word['id']]).fetchall()
            self.assertEqual([m[0] for m in meanings], word['meaning_ids'])
            polysemous += len(meanings) == 2
            for meaning in meanings:
                example = self.db.execute(query('SQLiteVocabularyContent', 'SELECT e.id'), [meaning[0]]).fetchone()
                self.assertIn(example[0], word['example_ids'])
            if word['note_id']:
                self.assertEqual(self.db.execute(query('SQLiteVocabularyContent', 'SELECT n.id'), [word['id']]).fetchone()[0], word['note_id'])
        self.assertEqual(polysemous, 24)
        self.assertEqual(len(self.registry['notes']), 146)
        for word in ['구독하다', '연기하다', '비추다', '비치다', '소박하다']:
            self.assertEqual(len(self.words[word]['meaning_ids']), 2)

    def test_metadata_irregulars_and_confusion_corrections(self):
        expected = {'달갑다':'b', '미덥다':'b', '껄끄럽다':'b', '삼가다':'none',
                    '가라앉다':'none', '가라앉히다':'none', '비추다':'none', '비치다':'none',
                    '들뜨다':'none', '가꾸다':'none', '값지다':'none'}
        for word, kind in expected.items():
            row = self.db.execute('SELECT irregular_type FROM vocabulary WHERE id=?', [self.words[word]['id']]).fetchone()
            self.assertEqual(row[0], kind)
        for word in self.words.values():
            pos, batchim, irregular, reading, topik, frequency = self.db.execute(
                'SELECT part_of_speech,has_batchim,irregular_type,reading,topik_level,frequency_rank FROM vocabulary WHERE id=?', [word['id']]).fetchone()
            if pos in ('verb', 'adjective', 'expression'):
                self.assertIsNone(batchim)
            if pos == 'expression':
                self.assertIsNone(irregular)
            if pos in ('verb', 'adjective') and word['headword'].endswith('하다'):
                self.assertEqual(irregular, 'other')
            self.assertEqual((reading, topik, frequency), (None, None, None))
        for word in ('로그인','로그아웃','한참'):
            self.assertEqual(self.words[word]['part_of_speech'], 'noun')
        self.assertEqual(self.words['지나치다']['part_of_speech'], 'verb')
        self.assertEqual(self.words['눈을 붙이다']['lexical_category'], 'phrase')

    def test_curriculum_keyset_pages_existing_sort_prefix_and_twenty_item_sets(self):
        for level, total in [('intro', 306), ('beginner', 800), ('lower_intermediate', 1181)]:
            sql = 'SELECT v.id FROM vocabulary v JOIN content_items i ON i.id=v.id WHERE i.level=? ORDER BY sort_key,v.id'
            old = [r[0] for r in self.old.execute(sql, [level])]
            current = [r[0] for r in self.db.execute(sql, [level])]
            self.assertEqual(len(current), total)
            self.assertEqual(current[:len(old)], old)
            self.assertTrue(all(1 <= len(current[i:i+20]) <= 20 for i in range(0, total, 20)))
            seen, cursor = [], ''
            while True:
                page = self.db.execute(query('SQLiteCurriculum', 'SELECT id FROM content_items'),
                                       [level, 'vocabulary', cursor, 'vocabulary']).fetchall()
                if not page:
                    break
                self.assertLessEqual(len(page), 200)
                seen.extend(r[0] for r in page)
                cursor = page[-1][0]
            self.assertEqual(set(seen), set(current))

    def test_search_secondary_senses_notes_and_typed_relations(self):
        for term, word in [('비추다','비추다'), ('インストール','설치하다'), ('演じる','연기하다'),
                           ('仮眠','눈을 붙이다'), ('결제','결제')]:
            rows = self.db.execute(query('SQLiteLookup', 'WITH terms'), [term]*3+[0]).fetchall()
            self.assertIn((self.words[word]['id'], 'vocabulary'), rows)
            self.assertLessEqual(len(rows), 30)
        self.assertEqual(len(self.registry['relations']), 84)
        for link in self.registry['relations']:
            related = self.db.execute(query('SQLiteLookup', 'WITH related'), [link['source_id']]*5).fetchall()
            self.assertIn((link['target_id'], 'vocabulary'), related)
        for link in self.registry['grammar_links']:
            visible = {r[0] for r in self.db.execute(query('SQLiteGrammarContent', 'SELECT e.id,e.korean'), [link['grammar_id']])}
            self.assertIn(link['example_id'], visible)
            self.assertLessEqual(len(visible), 6)
            previous = {r[0] for r in self.old.execute('SELECT example_id FROM grammar_examples WHERE grammar_id=?', [link['grammar_id']])}
            self.assertTrue(previous <= visible)
        self.assertEqual(len(self.registry['grammar_links']), 17)

    def test_new_srs_enrollment_does_not_reset_due_and_short_queues_are_bounded(self):
        db = user(version=10)
        self.addCleanup(db.close)
        enroll = query('SQLiteReviewProgress', 'INSERT INTO srs_state(')
        for word in self.words.values():
            db.execute(enroll, [word['id'], 'calendar_steps', 1, '{"stage":0}', 100, 100])
            db.execute(enroll, [word['id'], 'calendar_steps', 1, '{"stage":0}', 900, 900])
        self.assertEqual(db.execute('SELECT COUNT(*),MIN(due_at),MAX(due_at) FROM srs_state').fetchone(), (310, 100, 100))
        due = query('SQLiteReviewProgress', 'SELECT content_id FROM srs_state WHERE')
        self.assertEqual(db.execute(due, ['calendar_steps', 1, 99, 20]).fetchall(), [])
        for limit in (5, 10, 20):
            self.assertEqual(len(db.execute(due, ['calendar_steps', 1, 100, limit]).fetchall()), limit)
        self.assertIn('INDEX', str(db.execute('EXPLAIN QUERY PLAN '+due, ['calendar_steps', 1, 100, 20]).fetchall()))

    def test_content16_to17_swap_preserves_user_bytes_and_partial_session(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            content, progress = p/'Content.sqlite', p/'User.sqlite'
            shutil.copyfile(self.previous, content)
            db = user(progress, 10)
            a_words = json.loads((ROOT/'Content/data08-a-ids.json').read_text())['vocabulary']
            b_words = json.loads((ROOT/'Content/data08-b-ids.json').read_text())['vocabulary']
            ids = [v['id'] for v in a_words[:10]+b_words[:10]]
            payload = json.dumps(dict(vocabularyIDs=ids, order=ids, position=4, round=1, deferred=ids[:2], contentVersion=16))
            db.execute(query('SQLiteVocabularyProgress', 'INSERT INTO vocabulary_sets('), ['old-set', 'lower_intermediate', 1, 100])
            for i, item_id in enumerate(ids):
                db.execute(query('SQLiteVocabularyProgress', 'INSERT INTO vocabulary_set_items('), ['old-set', item_id, i])
            db.execute(query('SQLiteVocabularyProgress', 'INSERT INTO vocabulary_sessions('), ['session', 'old-set', payload, 4, 100])
            for skill, table in [('vocabulary', 'vocabulary'), ('grammar', 'grammar'), ('listening', 'listening_items')]:
                item_id = self.old.execute('SELECT id FROM '+table+' LIMIT 1').fetchone()[0]
                db.execute('INSERT INTO srs_state VALUES(?,?,?,?,?,?,?,?)', [item_id, skill, 'calendar_steps', 1, '{"stage":4}', 300, 100, 100])
            db.execute("INSERT INTO favorites(content_id,created_at,content_type) VALUES(?,100,'vocabulary')", [ids[0]])
            db.execute("INSERT INTO user_metadata VALUES('settings.v1','{\"shortSession\":5}')")
            db.commit()
            db.close()
            before = progress.read_bytes()
            shutil.copyfile(ROOT/'Resources/content.sqlite', content)
            self.assertEqual(progress.read_bytes(), before)
            with sqlite3.connect(progress) as cold, sqlite3.connect(content) as current:
                self.assertEqual(cold.execute('SELECT state_json,status FROM vocabulary_sessions').fetchone(), (payload, 'active'))
                self.assertEqual(cold.execute('SELECT content_id FROM vocabulary_set_items ORDER BY ordinal').fetchall(), [(i,) for i in ids])
                self.assertEqual(cold.execute('SELECT COUNT(*) FROM srs_state').fetchone()[0], 3)
                self.assertEqual(cold.execute('PRAGMA user_version').fetchone()[0], 10)
                for item_id, kind in cold.execute('SELECT content_id,content_type FROM favorites'):
                    self.assertIsNotNone(current.execute(query('SQLiteLookup', 'SELECT i.level'), [item_id, kind]).fetchone())

    def test_corrupt_candidate_and_unapproved_old_revision_changes_are_rejected(self):
        original = json.loads((ROOT/'Content/production.json').read_text())
        example_id = self.registry['examples'][0]
        revised_id = next(iter(self.approved))
        old_revision = self.old.execute('SELECT revision FROM content_items WHERE id=?', [revised_id]).fetchone()[0]
        with tempfile.TemporaryDirectory() as tmp:
            for case in ('empty_ja', 'duplicate_id', 'old_revision_not_incremented'):
                candidate = copy.deepcopy(original)
                if case == 'empty_ja':
                    next(e for e in candidate['tables']['examples'] if e['id'] == example_id)['japanese'] = ''
                elif case == 'duplicate_id':
                    candidate['tables']['content_items'].append(copy.deepcopy(candidate['tables']['content_items'][-1]))
                else:
                    next(i for i in candidate['tables']['content_items'] if i['id'] == revised_id)['revision'] = old_revision
                source = Path(tmp)/'invalid.json'
                source.write_text(json.dumps(candidate, ensure_ascii=False))
                with self.subTest(case=case), self.assertRaises(ValidationError):
                    build(source, Path(tmp)/'invalid.sqlite', self.previous, production=True)

    def test_reviewed_payload_fingerprints_and_three_subgroup_gate_records(self):
        source = json.loads((ROOT/'Content/production.json').read_text())
        rows = {k: {r['id']: r for r in values if 'id' in r}
                for k, values in source['tables'].items()}
        review = json.loads((ROOT/'Docs/DATA08_C_EDITORIAL.json').read_text())
        records = {r['id']: r for r in review['records']}
        self.assertEqual(collections.Counter(w['subgroup'] for w in self.words.values()),
                         dict(C1=100, C2=100, C3=110))
        for word in self.words.values():
            payload = dict(vocabulary=rows['vocabulary'][word['id']],
                           meanings=[rows['meanings'][i] for i in word['meaning_ids']],
                           examples=[rows['examples'][i] for i in word['example_ids']],
                           note=rows['learner_notes'].get(word['note_id']))
            digest = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False,
                                               separators=(',', ':')).encode()).hexdigest()
            self.assertEqual(records[word['id']]['editorial_sha256'], digest)
            self.assertEqual(records[word['id']]['status'], 'approved_after_individual_self_review')
            self.assertTrue(all(m['usage_ja'].startswith('コロケーション：') for m in payload['meanings']))
            self.assertTrue(all(m['nuance_ja'] == '文体：'+word['register_ja'] for m in payload['meanings']))
        for stage in (1, 2, 3):
            audit = json.loads((ROOT/f'Docs/DATA08_C{stage}_AUDIT.json').read_text())
            report = json.loads((ROOT/f'Docs/DATA08_C{stage}_VALIDATION.json').read_text())
            self.assertEqual((audit['cumulative_vocabulary_rows'], audit['cumulative_examples']),
                             ([100,200,310][stage-1], [199,399,619][stage-1]))
            self.assertEqual(report['validation']['error_count'], 0)
            self.assertEqual(report['validation']['warning_count'], 10)
        self.assertEqual(hashlib.sha256((ROOT/'Content/production.json').read_bytes()).hexdigest(),
                         audit['source_sha256'])

    def test_existing_sentence_reused_without_new_identity_or_payload(self):
        self.assertEqual(len(self.registry['reused_examples']), 1)
        reuse = self.registry['reused_examples'][0]
        eid = '3fb4a617-a5ef-476b-9f40-0963a3ff9845'
        self.assertEqual(reuse['example_id'], eid)
        self.assertEqual(reuse['vocabulary_id'], self.words['퍼뜨리다']['id'])
        self.assertNotIn(eid, self.registry['examples'])
        self.assertIn(eid, self.words['퍼뜨리다']['example_ids'])
        self.assertEqual(self.db.execute('SELECT * FROM examples WHERE id=?', [eid]).fetchone(),
                         self.old.execute('SELECT * FROM examples WHERE id=?', [eid]).fetchone())
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM examples WHERE korean=?',
                         ['확인하지 않은 소문을 퍼뜨리지 마세요.']).fetchone()[0], 1)
        mid = self.words['퍼뜨리다']['meaning_ids'][0]
        self.assertIsNotNone(self.db.execute('SELECT 1 FROM vocabulary_examples WHERE meaning_id=? AND example_id=?',
                                            [mid, eid]).fetchone())
        self.assertIn(eid, self.approved)

    def test_whole_data08_targets_actual_unique_cohorts_and_separate_categories(self):
        all_words, all_examples, lexical, phrases = set(), set(), 0, 0
        for batch, count, ex in [('a',301,602), ('b',300,600), ('c',310,619)]:
            registry = json.loads((ROOT/f'Content/data08-{batch}-ids.json').read_text())
            ids = {w['id'] for w in registry['vocabulary']}
            examples = set(registry['examples'])
            self.assertEqual((len(ids), len(examples)), (count, ex))
            self.assertFalse(all_words & ids)
            self.assertFalse(all_examples & examples)
            for item_id in ids:
                pos, kind, active = self.db.execute('SELECT v.part_of_speech,i.kind,i.is_active FROM vocabulary v JOIN content_items i ON i.id=v.id WHERE v.id=?', [item_id]).fetchone()
                self.assertEqual((kind, active), ('vocabulary', 1))
                phrases += pos == 'expression'
                lexical += pos != 'expression'
            all_words |= ids
            all_examples |= examples
        self.assertEqual((len(all_words), lexical, phrases, len(all_examples)), (911,807,104,1821))
        self.assertTrue(800 <= len(all_words) <= 1200)
        self.assertTrue(800 <= lexical <= 1200)
        self.assertTrue(1300 <= len(all_examples) <= 2000)
        with sqlite3.connect(ROOT/'Tests/Fixtures/content-v14-production.sqlite') as baseline:
            self.assertEqual(self.db.execute('SELECT COUNT(*) FROM vocabulary').fetchone()[0]
                             -baseline.execute('SELECT COUNT(*) FROM vocabulary').fetchone()[0], 911)
            self.assertEqual(self.db.execute('SELECT COUNT(*) FROM examples').fetchone()[0]
                             -baseline.execute('SELECT COUNT(*) FROM examples').fetchone()[0], 1821)
        self.assertEqual(collections.Counter(w['lexical_category'] for w in self.words.values()),
                         dict(vocabulary=280, phrase=30))
