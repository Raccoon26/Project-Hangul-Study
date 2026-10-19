"""Production course integration checks. These execute SQLite/Importer, not Swift UI."""
import json, re, sqlite3, tempfile, unittest
from pathlib import Path
from build_content import ROOT, build

class HangulContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.path = Path(cls.temp.name)/'content.sqlite'
        cls.source = ROOT/'Content/hangul-production.json'
        build(cls.source, cls.path, production=True, previous=ROOT/'Tests/Fixtures/content-v2-production.sqlite')
        cls.db = sqlite3.connect(cls.path)
    @classmethod
    def tearDownClass(cls): cls.db.close(); cls.temp.cleanup()
    def test_production_versions_and_integrity(self):
        self.assertEqual(self.db.execute('SELECT schema_version,content_version,min_reader_version,is_fixture,dataset_id FROM content_metadata').fetchone(), (2,3,3,0,'ko-ja-core'))
        self.assertEqual(self.db.execute('PRAGMA integrity_check').fetchone()[0], 'ok')
        self.assertEqual(self.db.execute('PRAGMA foreign_key_check').fetchall(), [])
    def test_all_modern_jamo_exactly_once(self):
        symbols = [r[0] for r in self.db.execute("SELECT symbol FROM hangul WHERE category IN ('consonant','vowel')")]
        expected = set('ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㄲㄸㅃㅆㅉㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣㅐㅔㅒㅖㅘㅙㅚㅝㅞㅟㅢ')
        self.assertEqual(len(symbols), 40); self.assertEqual(set(symbols), expected)
    def test_lesson_order_and_all_runtime_queries(self):
        lessons = self.db.execute('SELECT id,title_ja,ordinal FROM lessons ORDER BY ordinal').fetchall()
        self.assertEqual([x[2] for x in lessons], list(range(12)))
        self.assertEqual([x[1] for x in lessons], ['はじめてのハングル','基本母音①','基本母音②','基本子音①','基本子音②','文字を組み立てる','濃音','複合母音①','複合母音②','パッチム入門','読んでみよう','総合確認'])
        swift = (ROOT/'Repositories/SQLiteContentRepository.swift').read_text()
        query = next(q for q in re.findall(r'"""(.*?)"""', swift, re.S) if 'LEFT JOIN hangul' in q)
        count = 0
        for lesson_id, _, _ in lessons:
            rows = self.db.execute(query, [lesson_id]).fetchall()
            self.assertGreater(len(rows), 0); self.assertLessEqual(len(rows), 200)
            self.assertTrue(any(row[1]=='question' for row in rows))
            self.assertTrue(all(row[1] in ('hangul','note','question') for row in rows))
            count += len(rows)
        self.assertEqual(count, 117)
    def test_single_choice_answers_are_valid_and_unique(self):
        for qid, answer, qtype in self.db.execute('SELECT id,answer_json,question_type FROM questions'):
            self.assertEqual(qtype, 'multiple_choice')
            correct=json.loads(answer)['correct_choice_ids']
            choices=self.db.execute('SELECT choice_id,text FROM question_choices WHERE question_id=?',[qid]).fetchall()
            self.assertEqual(len(correct),1)
            self.assertEqual(sum(x[0]==correct[0] for x in choices),1)
            self.assertEqual(len({x[1] for x in choices}),len(choices))
            targets=self.db.execute("SELECT target_id FROM content_links WHERE source_id=? AND relation='question_target'",[qid]).fetchall()
            self.assertGreater(len(targets),0)
    def test_stable_ids_match_registry_and_persist_across_rebuild(self):
        registry=json.loads((ROOT/'Content/hangul-ids.json').read_text())
        ids={x[0] for x in self.db.execute('SELECT id FROM content_items')}
        self.assertEqual(ids, set(registry.values()))
        second=Path(self.temp.name)/'second.sqlite'
        build(self.source,second,production=True)
        with sqlite3.connect(second) as db:
            self.assertEqual(ids,{x[0] for x in db.execute('SELECT id FROM content_items')})
    def test_audio_is_absent_and_no_jamo_tts(self):
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM hangul WHERE audio_asset_id IS NOT NULL').fetchone()[0],0)
        for path in ROOT.rglob('*.swift'):
            if 'Tests' not in path.parts and path.name != 'KoreanAudioService.swift': self.assertNotIn('AVSpeechSynthesizer',path.read_text())
        self.assertIn('AudioPolicy.permitsTTS(audio)', (ROOT/'Services/KoreanAudioService.swift').read_text())
    def test_app_packages_production_and_fixture_only_in_test_bundle(self):
        generator=(ROOT/'Tools/generate_project.py').read_text()
        self.assertIn('source_db="$SRCROOT/Resources/content.sqlite"',generator)
        self.assertNotIn('source_db="$SRCROOT/Resources/content-fixture.sqlite"',generator)
        self.assertIn("test_resource_files=['Resources/content-fixture.sqlite','Config/RemoveAds.storekit']",generator)
        self.assertNotIn('let allowFixture = true',(ROOT/'Services/AppContainer.swift').read_text())
    def test_hangul_referenced_by_lessons_and_confusions_present(self):
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM hangul h WHERE NOT EXISTS(SELECT 1 FROM lesson_items li WHERE li.content_id=h.id)').fetchone()[0],0)
        self.assertGreaterEqual(self.db.execute("SELECT COUNT(*) FROM content_links WHERE relation='related'").fetchone()[0],10)
        self.assertTrue(all(row[0].strip() for row in self.db.execute('SELECT explanation_ja FROM hangul')))

if __name__=='__main__': unittest.main()
