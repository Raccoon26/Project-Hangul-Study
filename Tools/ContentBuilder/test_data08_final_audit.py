"""Final DATA-08 editorial corrections, immutable IDs and real SQL regressions.

Language expectations are authored review evidence, not a linguistic oracle.
These tests never substitute for Swift/Xcode or human language review.
"""
import collections
import copy
import gzip
import hashlib
import json
import random
import shutil
import sqlite3
import tempfile
import unittest
from pathlib import Path

from audit_data08_final import audit, cohorts, linguistic_lints, norm
from build_content import ROOT, build
from test_data05_content import query
from test_lookup_sql import user
from validator import Report, row_fields, signatures


class Data08FinalAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads((ROOT/'Content/production.json').read_text())
        cls.before_bytes = gzip.decompress((ROOT/'Tests/Fixtures/content-v17-production.json.gz').read_bytes())
        cls.before = json.loads(cls.before_bytes)
        cls.previous = ROOT/'Tests/Fixtures/content-v17-production.sqlite'
        cls.db = sqlite3.connect((ROOT/'Resources/content.sqlite').as_uri()+'?mode=ro', uri=True)
        cls.old = sqlite3.connect(cls.previous.as_uri()+'?mode=ro', uri=True)
        cls.registries = cohorts()
        cls.words = [w for r in cls.registries.values() for w in r['vocabulary']]
        cls.rows = {t: {r['id']: r for r in values if 'id' in r}
                    for t, values in cls.source['tables'].items()}
        cls.fixes = json.loads((ROOT/'Docs/DATA08_FINAL_FINDINGS.json').read_text())
        cls.approved = set(json.loads((ROOT/'Content/data08-final-revised-ids.json').read_text()))

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        cls.old.close()

    def test_full_source_and_bundle_audit_all_cohorts_and_references(self):
        result = audit(self.source, ROOT/'Resources/content.sqlite')
        self.assertEqual(result['validation']['error_count'], 0)
        self.assertEqual(result['source_rows_scanned'], 42909)
        self.assertEqual(result['source_tables_scanned'], 25)
        self.assertEqual(result['scope'], dict(vocabulary=911, meanings=963, unique_examples=1821,
                         example_placements=1822, notes=314, lexical_relations=201, grammar_references=46))
        self.assertEqual(result['japanese_duplicate_candidates'], [])

    def test_strict_content17_to18_rebuild_has_same_complete_sql_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)/'rebuilt.sqlite'
            result = build(ROOT/'Content/production.json', target, self.previous, production=True)
            self.assertEqual(result['validation']['error_count'], 0)
            self.assertEqual(result['validation']['warning_count'], 10)
            with sqlite3.connect(target) as rebuilt:
                for (table,) in self.db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
                    with self.subTest(table=table):
                        self.assertEqual(set(rebuilt.execute('SELECT * FROM '+table)),
                                         set(self.db.execute('SELECT * FROM '+table)))
        self.assertEqual(self.db.execute('SELECT schema_version,content_version,min_reader_version FROM content_metadata').fetchone(), (4,18,7))

    def test_exact_field_ledger_reverses_to_complete_released_source(self):
        self.assertEqual(hashlib.sha256(self.before_bytes).hexdigest(),
                         '7fee2b4591f1ecd732bdf8a88433a86644cbe665a609005556d985c80c3f604b')
        restored = copy.deepcopy(self.source)
        rows = {t: {r['id']:r for r in values if 'id' in r} for t,values in restored['tables'].items()}
        old_items = {r['id']:r for r in self.before['tables']['content_items']}
        self.assertEqual(len(self.fixes), 43)
        self.assertEqual(len({f['vocabulary_id'] for f in self.fixes}), 34)
        self.assertEqual({f['id'] for f in self.fixes}, self.approved)
        for fix in self.fixes:
            row = rows[fix['table']][fix['id']]
            self.assertEqual(row[fix['field']], fix['after'])
            row[fix['field']] = fix['before']
        for item_id in self.approved:
            rows['content_items'][item_id].update(old_items[item_id])
        restored['metadata']['content_version'] = 17
        self.assertEqual(restored, self.before)

    def test_no_identity_count_membership_or_order_changes_only_40_revisions(self):
        self.assertEqual(hashlib.sha256(self.previous.read_bytes()).hexdigest(),
                         '836dec2fac50508a177010dbf8f83a74a9e4660c8c42c1f08a75bd9207f286c6')
        old, current = signatures(self.old), signatures(self.db)
        self.assertEqual(set(old), set(current))
        self.assertEqual({i for i in old if old[i] != current[i]}, self.approved)
        self.assertEqual(len(self.approved), 40)
        for before in self.old.execute('SELECT * FROM content_items'):
            after = self.db.execute('SELECT * FROM content_items WHERE id=?', [before[0]]).fetchone()
            self.assertEqual(after[:2]+after[3:-1], before[:2]+before[3:-1])
            self.assertEqual(after[2], before[2]+int(before[0] in self.approved))
            if before[0] not in self.approved:
                self.assertEqual(after, before)
        for table in ('vocabulary_examples','grammar_examples','content_links','item_sources','item_tags','lesson_items'):
            self.assertEqual(self.old.execute('SELECT * FROM '+table).fetchall(),
                             self.db.execute('SELECT * FROM '+table).fetchall())

    def test_real_language_failures_detected_beyond_old_structural_validator(self):
        old_rows = {r['id']:r for r in self.before['tables']['examples']}
        expected = {'17ae5ef9-55a7-4f3e-ab1a-125ac52dd53f':'counselling_recipient_reversed',
                    '5e37b1f6-ba0e-492b-b39e-99483108c869':'reviewed_japanese_collocation',
                    'd38f0789-9846-4aec-8516-e5a0dffd47fa':'clue_and_solution_collocation_mixture'}
        for eid, code in expected.items():
            self.assertIn(code, linguistic_lints(old_rows[eid]))
            self.assertEqual(linguistic_lints(self.rows['examples'][eid]), [])
        initial = json.loads((ROOT/'Docs/DATA08_FINAL_INITIAL_AUDIT.json').read_text())
        self.assertEqual(initial['validation']['error_count'], 10)
        release17 = json.loads((ROOT/'Docs/DATA08_C_DB_BUILD.json').read_text())
        self.assertEqual(release17['validation']['error_count'], 0)
        for row in self.source['tables']['examples']:
            self.assertEqual(linguistic_lints(row), [])

    def test_mutations_missing_field_reference_duplicate_and_pos_are_rejected(self):
        wid = self.words[0]['id']
        mid = self.words[0]['meaning_ids'][0]
        for case in ('required_field','missing_reference','duplicate_id','normalized_headword','meaning_pos'):
            source = copy.deepcopy(self.source)
            values = source['tables']
            row = next(r for r in values['vocabulary'] if r['id'] == wid)
            if case == 'required_field':
                del row['headword']
            elif case == 'missing_reference':
                next(r for r in values['meanings'] if r['id'] == mid)['vocabulary_id'] = '00000000-0000-4000-8000-000000000000'
            elif case == 'duplicate_id':
                values['content_items'].append(copy.deepcopy(values['content_items'][-1]))
            elif case == 'normalized_headword':
                row['headword'] = ' ' + values['vocabulary'][0]['headword'] + ' '
            else:
                next(r for r in values['meanings'] if r['id'] == mid)['part_of_speech'] = 'noun'
            with self.subTest(case=case):
                self.assertGreater(audit(source)['validation']['error_count'], 0)

    def test_core_validator_rejects_hidden_control_text_but_allows_multiline_notes(self):
        row = copy.deepcopy(self.source['tables']['examples'][-1])
        columns = {r[1]:r for r in self.db.execute('PRAGMA table_info(examples)')}
        for char in ('\x01','\x08','\x1b','\x7f'):
            row['japanese'] = '確認'+char+'します。'
            report = Report()
            self.assertFalse(row_fields('examples',row,columns,'mutated-example',report))
            self.assertIn('control_character', {e['code'] for e in report.errors})
        row['japanese'] = '確認します。\n次へ進みます。'
        report = Report()
        self.assertTrue(row_fields('examples',row,columns,'multiline-example',report))

    def test_all_911_current_cards_meanings_notes_and_review_hashes(self):
        review = json.loads((ROOT/'Docs/DATA08_FINAL_EDITORIAL.json').read_text())
        records = {r['id']:r for r in review['records']}
        self.assertFalse(review['human_reviewed'])
        self.assertEqual(len(records), 911)
        for word in self.words:
            wid = word['id']
            payload = dict(vocabulary=self.rows['vocabulary'][wid],
                           meanings=[self.rows['meanings'][i] for i in word['meaning_ids']],
                           examples=[self.rows['examples'][i] for i in word['example_ids']],
                           note=self.rows['learner_notes'].get(word['note_id']))
            digest = hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
            self.assertEqual(digest, records[wid]['payload_sha256'])
            self.assertTrue(records[wid]['korean_reread'] and records[wid]['japanese_reread'])
            self.assertFalse(records[wid]['human_reviewed'])
            card = self.db.execute(query('SQLiteVocabularyContent','SELECT v.headword'),[wid]).fetchone()
            self.assertEqual(card[:2],(payload['vocabulary']['headword'],payload['vocabulary']['part_of_speech']))
            self.assertEqual([r[0] for r in self.db.execute(query('SQLiteVocabularyContent','SELECT m.*'),[wid])],word['meaning_ids'])
            if word['note_id']:
                self.assertEqual(self.db.execute(query('SQLiteVocabularyContent','SELECT n.id'),[wid]).fetchone()[0],word['note_id'])

    def test_corrected_phrase_search_and_same_identity_keep_saved_session_due(self):
        wid = 'dc74ca05-85f7-4cc8-b6a8-56f3ef0c6927'
        self.assertEqual(self.db.execute('SELECT headword FROM vocabulary WHERE id=?',[wid]).fetchone()[0],'실마리가 보이다')
        self.assertIn((wid,'vocabulary'), self.db.execute(query('SQLiteLookup','WITH terms'),['실마리가 보이다']*3+[0]).fetchall())
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            content, progress = p/'content.sqlite', p/'progress.sqlite'
            shutil.copyfile(self.previous,content)
            db = user(progress,10)
            changed = sorted({f['vocabulary_id'] for f in self.fixes} - {wid})[:19]
            ids = [wid]+changed
            payload = json.dumps(dict(vocabularyIDs=ids,order=ids,position=4,round=1,contentVersion=17))
            db.execute(query('SQLiteVocabularyProgress','INSERT INTO vocabulary_sets('),['audit-set','lower_intermediate',1,100])
            for index,item_id in enumerate(ids):
                db.execute(query('SQLiteVocabularyProgress','INSERT INTO vocabulary_set_items('),['audit-set',item_id,index])
                db.execute(query('SQLiteReviewProgress','INSERT INTO srs_state('),[item_id,'calendar_steps',1,'{"stage":4}',300,100])
            db.execute(query('SQLiteVocabularyProgress','INSERT INTO vocabulary_sessions('),['session','audit-set',payload,4,100])
            db.execute("INSERT INTO favorites(content_id,created_at,content_type) VALUES(?,100,'vocabulary')",[wid])
            db.execute("INSERT INTO user_metadata VALUES('settings.v1','{\"shortSession\":5}')")
            db.commit(); db.close()
            original = progress.read_bytes()
            shutil.copyfile(ROOT/'Resources/content.sqlite',content)
            self.assertEqual(progress.read_bytes(),original)
            with sqlite3.connect(progress) as saved, sqlite3.connect(content) as current:
                self.assertEqual(saved.execute('PRAGMA user_version').fetchone()[0],10)
                self.assertEqual(saved.execute('SELECT state_json,status FROM vocabulary_sessions').fetchone(),(payload,'active'))
                self.assertEqual(saved.execute('SELECT content_id FROM vocabulary_set_items ORDER BY ordinal').fetchall(),[(i,) for i in ids])
                self.assertEqual(saved.execute('SELECT COUNT(*),MIN(due_at),MAX(due_at) FROM srs_state').fetchone(),(20,300,300))
                self.assertEqual(current.execute('SELECT headword FROM vocabulary WHERE id=?',[wid]).fetchone()[0],'실마리가 보이다')
                due = query('SQLiteReviewProgress','SELECT content_id FROM srs_state WHERE')
                for limit in (5,10,20):
                    self.assertEqual(len(saved.execute(due,['calendar_steps',1,300,limit]).fetchall()),limit)

    def test_all_irregulars_and_regular_confusables_have_reviewed_native_expectations(self):
        risk = json.loads((ROOT/'Docs/DATA08_FINAL_RISK_FORMS.json').read_text())
        words = {self.rows['vocabulary'][w['id']]['headword']:w for w in self.words}
        irregulars = {name for name,w in words.items() if self.rows['vocabulary'][w['id']]['irregular_type'] not in (None,'none','other')}
        expected = {r['headword'] for r in risk['records'] if r['irregular_type'] != 'none'}
        self.assertEqual(len(expected),22)
        self.assertEqual(irregulars,expected)
        native = (ROOT/'Tests/ProductionLearningTests.swift').read_text()
        for r in risk['records']:
            current = self.rows['vocabulary'][words[r['headword']]['id']]
            self.assertEqual((current['part_of_speech'],current['irregular_type']),(r['part_of_speech'],r['irregular_type']))
            for key in ('present','condition','future'):
                self.assertIn('"'+r[key]+'"',native)
        self.assertEqual(risk['native_execution'],0)

    def test_separate_random_samples_and_actual_grammar_links_keep_limits(self):
        samples = json.loads((ROOT/'Docs/DATA08_FINAL_SAMPLES.json').read_text())
        words = [dict(w,batch=b) for b,r in self.registries.items() for w in r['vocabulary']]
        for stratum in samples['strata']:
            parts = stratum['stratum'].split(':')
            pool = [w for w in words if (w['level']==parts[1] if parts[0]=='level' else w['batch']==parts[1])
                    and (parts[0]!='batch_pos' or w['part_of_speech']==parts[2])]
            rng = random.Random(int(hashlib.sha256((samples['seed']+stratum['stratum']).encode()).hexdigest(),16))
            self.assertEqual([w['id'] for w in rng.sample(sorted(pool,key=lambda w:w['id']),len(stratum['sampled_ids']))],stratum['sampled_ids'])
        self.assertEqual((samples['draws'],len(samples['items'])),(85,84))
        self.assertTrue(all(w['reread_complete'] and not w['human_reviewed'] for w in samples['items']))
        grammar = json.loads((ROOT/'Docs/DATA08_FINAL_GRAMMAR.json').read_text())
        self.assertEqual((grammar['existing_grammar_count'],grammar['new_grammar_count']),(42,0))
        self.assertGreater(grammar['candidate_examples'],0)
        for link in grammar['links']:
            visible = [r[0] for r in self.db.execute(query('SQLiteGrammarContent','SELECT e.id'),[link['grammar_id']])]
            self.assertLessEqual(len(visible),6)
            self.assertIn(link['example_id'],visible)
