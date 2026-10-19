"""DEV-04 structural and SQL integration tests; not an auditory/TTS certification."""
import copy,json,re,sqlite3,tempfile,unittest
from pathlib import Path
from build_content import ROOT,build
from validator import signatures

class PronunciationContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory();cls.folder=Path(cls.temp.name)
        cls.source=ROOT/'Content/production.json';cls.data=json.loads(cls.source.read_text())
        cls.output=cls.folder/'production.sqlite'
        cls.report=build(cls.source,cls.output,previous=ROOT/'Tests/Fixtures/content-v3-production.sqlite',production=True)
        cls.db=sqlite3.connect(cls.output)
    @classmethod
    def tearDownClass(cls):cls.db.close();cls.temp.cleanup()
    def reject(self,mutate):
        data=copy.deepcopy(self.data);mutate(data)
        source=self.folder/'invalid.json';source.write_text(json.dumps(data,ensure_ascii=False))
        with self.assertRaises(ValueError):build(source,self.folder/'rejected.sqlite',production=True)
    def test_versions_integrity_and_reviewed_short_word_warnings(self):
        self.assertEqual(self.db.execute('SELECT schema_version,content_version,min_reader_version,is_fixture FROM content_metadata').fetchone(),(4,19,7,0))
        self.assertEqual(self.report['validation']['error_count'],0)
        # DATA-01/02/03 add five reviewed homograph groups; DEV-04 short-word warnings remain.
        self.assertEqual(self.report['validation']['warning_count'],10)
        warnings=self.report['validation']['warnings']
        self.assertEqual(sum(w['code']=='short_sentence' for w in warnings),5)
        self.assertEqual({w['location'] for w in warnings if w['code']=='duplicate_headword_candidate'},{'차','일','쓰다','저','적다'})
        self.assertEqual(self.db.execute('PRAGMA foreign_key_check').fetchall(),[])
        self.assertEqual(self.db.execute('PRAGMA integrity_check').fetchone()[0],'ok')
    def test_dev03_content_and_id_signatures_unchanged(self):
        with sqlite3.connect(ROOT/'Tests/Fixtures/content-v3-production.sqlite') as old:
            before=signatures(old);after=signatures(self.db)
            self.assertTrue(all(after[key]==value for key,value in before.items()))
            self.assertEqual(len(before),130)
    def test_course_order_and_rule_coverage(self):
        courses=self.db.execute('SELECT id,title_ja FROM courses ORDER BY ordinal').fetchall()
        self.assertEqual([r[1] for r in courses],['ハングル入門','発音・パッチム','入門文法','初級文法','初中級・会話と現代生活'])
        lessons=self.db.execute('SELECT title_ja,ordinal FROM lessons WHERE course_id=? ORDER BY ordinal',[courses[1][0]]).fetchall()
        self.assertEqual(len(lessons),14);self.assertEqual([r[1] for r in lessons],list(range(14)))
        self.assertEqual(lessons[0][0],'パッチムの位置');self.assertEqual(lessons[-1][0],'総合確認')
        kinds={r[0] for r in self.db.execute('SELECT DISTINCT rule_type FROM pronunciation_rules')}
        self.assertTrue({'batchim','liaison','nasalization','liquidization','palatalization','tensification','aspiration'}.issubset(kinds))
    def test_expected_spelling_and_reading_are_separate(self):
        pairs=dict(self.db.execute('SELECT spelling_ko,readings_json FROM pronunciation_presentations'))
        for spelling,reading in [('한국어','한구거'),('먹어요','머거요'),('한국말','한궁말'),('먹는','멍는'),('설날','설랄'),('같이','가치'),('읽다','익따'),('없다','업따'),('앉다','안따'),('좋다','조타')]:
            self.assertIn(reading,json.loads(pairs[spelling]))
    def test_actual_swift_pronunciation_and_audio_queries(self):
        source=(ROOT/'Repositories/SQLiteContentRepository.swift').read_text()
        queries=re.findall(r'"""(.*?)"""',source,re.S)
        presentation=next(q for q in queries if 'FROM pronunciation_rules r JOIN pronunciation_presentations' in q)
        audio=next(q for q in queries if 'FROM content_audio a' in q)
        similar=next(q for q in queries if 'FROM pronunciation_examples p' in q)
        for rule_id, in self.db.execute('SELECT id FROM pronunciation_rules').fetchall():
            self.assertIsNotNone(self.db.execute(presentation,[rule_id]).fetchone())
            self.assertIsNotNone(self.db.execute(audio,[rule_id]).fetchone())
            self.db.execute(similar,[rule_id]).fetchall()
    def test_tts_is_orthography_and_comparisons_require_recordings(self):
        for spelling,text in self.db.execute("SELECT p.spelling_ko,a.tts_text FROM content_audio a JOIN pronunciation_presentations p ON p.rule_id=a.content_id WHERE a.mode='tts'"):
            self.assertEqual(spelling,text)
            self.assertNotRegex(text,r'[ㄱ-ㆎᄀ-ᇿ\[\]/+]')
        comparisons=self.db.execute("SELECT mode,asset_id FROM content_audio WHERE usage='comparison'").fetchall()
        self.assertEqual(len(comparisons),6)
        self.assertTrue(all(row==('recorded_required',None) for row in comparisons))
    def test_listening_questions_hide_transcript_and_have_single_answer(self):
        rows=self.db.execute('SELECT q.id,q.prompt_ko,q.answer_json,a.tts_text FROM audio_questions aq JOIN questions q ON q.id=aq.question_id JOIN content_audio a ON a.content_id=aq.audio_content_id').fetchall()
        self.assertEqual(len(rows),3)
        for id,prompt,answer,text in rows:
            self.assertIsNone(prompt)
            correct=json.loads(answer)['correct_choice_ids'];self.assertEqual(len(correct),1)
            choice=self.db.execute('SELECT text FROM question_choices WHERE question_id=? AND choice_id=?',[id,correct[0]]).fetchone()[0]
            self.assertEqual(choice,text)
    def test_jamo_tts_rejected(self):
        self.reject(lambda x:x['tables']['content_audio'][0].update(mode='tts',usage='word_sentence',tts_text='ㄱ'))
    def test_comparison_tts_rejected(self):
        self.reject(lambda x:x['tables']['content_audio'][0].update(mode='tts',usage='comparison',tts_text='가'))
    def test_phonetic_markup_tts_rejected(self):
        self.reject(lambda x:x['tables']['content_audio'][0].update(mode='tts',usage='word_sentence',tts_text='[한궁말]'))
    def test_reading_substituted_for_spelling_rejected(self):
        def mutate(x):
            row=next(a for a in x['tables']['content_audio'] if a.get('tts_text')=='한국말');row['tts_text']='한궁말'
        self.reject(mutate)
    def test_missing_audio_reference_rejected(self):
        self.reject(lambda x:x['tables']['audio_questions'][0].update(audio_content_id='00000000-0000-4000-8000-000000000000'))
    def test_empty_or_invalid_readings_rejected(self):
        for value in ['[]','{}','[null]','["가","가"]']:
            self.reject(lambda x:x['tables']['pronunciation_presentations'][0].update(readings_json=value))
    def test_future_reader_and_malformed_reader_rejected(self):
        for value in [3,None,'4',999]:
            self.reject(lambda x:x['metadata'].update(min_reader_version=value))
    def test_multiple_readings_supported(self):
        data=copy.deepcopy(self.data)
        data['tables']['pronunciation_presentations'][0]['readings_json']='["한", "한ː"]'
        source=self.folder/'variants.json';source.write_text(json.dumps(data,ensure_ascii=False))
        # Structural capability only; not authored as a real pronunciation of this item.
        output=self.folder/'variants.sqlite';build(source,output,production=True)
        with sqlite3.connect(output) as db:
            value=db.execute('SELECT readings_json FROM pronunciation_presentations WHERE rule_id=?',[data['tables']['pronunciation_presentations'][0]['rule_id']]).fetchone()[0]
            self.assertEqual(len(json.loads(value)),2)

if __name__=='__main__':unittest.main()
