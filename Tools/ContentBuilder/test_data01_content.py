"""DATA-01 release gates against authored production data and actual Swift query SQL."""
import copy,json,re,sqlite3,tempfile,unittest,uuid
from collections import Counter
from pathlib import Path
from build_content import ROOT,build
from validator import signatures,ValidationError

class Data01ContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory();cls.folder=Path(cls.temp.name)
        cls.source=ROOT/'Content/production.json';cls.data=json.loads(cls.source.read_text())
        cls.registry=json.loads((ROOT/'Content/data01-ids.json').read_text())
        cls.path=cls.folder/'data01.sqlite'
        cls.report=build(cls.source,cls.path,previous=ROOT/'Tests/Fixtures/content-v4-production.sqlite',production=True)
        cls.db=sqlite3.connect(cls.path)
        cls.swift=(ROOT/'Repositories/SQLiteContentRepository.swift').read_text()
        cls.queries=re.findall(r'"""(.*?)"""',cls.swift,re.S)
    @classmethod
    def tearDownClass(cls):cls.db.close();cls.temp.cleanup()
    def clause(self,prefix):
        return next(s for s in re.findall(r'sql \+= "([^"]+)"',self.swift) if s.startswith(prefix))
    def test_release_counts_versions_and_integrity(self):
        self.assertEqual(self.db.execute('SELECT schema_version,content_version,min_reader_version,is_fixture,dataset_id FROM content_metadata').fetchone(),(4,16,7,0,'ko-ja-core'))
        for table,count in [('vocabulary',1977),('meanings',2086),('examples',3978),('courses',4),('lessons',38),('hangul',55),('pronunciation_rules',36)]:
            self.assertEqual(self.db.execute('SELECT COUNT(*) FROM '+table).fetchone()[0],count)
        self.assertEqual(len(self.registry['examples']),447)
        self.assertEqual(self.db.execute('PRAGMA integrity_check').fetchone()[0],'ok')
        self.assertEqual(self.db.execute('PRAGMA foreign_key_check').fetchall(),[])
    def test_all_existing_content_payloads_and_relationships_preserved(self):
        with sqlite3.connect(ROOT/'Tests/Fixtures/content-v4-production.sqlite') as previous:
            old=signatures(previous);new=signatures(self.db)
            self.assertEqual(len(old),225)
            self.assertTrue(all(new[id]==digest for id,digest in old.items()))
            old_items=previous.execute('SELECT * FROM content_items ORDER BY id').fetchall()
            for row in old_items:self.assertEqual(self.db.execute('SELECT * FROM content_items WHERE id=?',[row[0]]).fetchone(),row)
    def test_every_word_and_every_sense_has_reviewed_examples(self):
        for v in self.registry['vocabulary']:
            row=self.db.execute('SELECT headword,part_of_speech FROM vocabulary WHERE id=?',[v['id']]).fetchone()
            self.assertEqual(row,(v['headword'],v['part_of_speech']))
            meanings=self.db.execute('SELECT id,meaning_ja FROM meanings WHERE vocabulary_id=? ORDER BY ordinal',[v['id']]).fetchall()
            self.assertEqual([x[0] for x in meanings],v['meaning_ids'])
            examples=self.db.execute(self.queries[1],[v['id']]).fetchall()
            self.assertEqual({r[0] for r in examples},set(v['example_ids']))
            self.assertEqual(len(examples),2)
            for mid,_ in meanings:
                self.assertGreater(self.db.execute('SELECT COUNT(*) FROM vocabulary_examples WHERE meaning_id=?',[mid]).fetchone()[0],0)
            for _,ko,ja in examples:self.assertTrue(ko.strip() and ja.strip())
    def test_stable_uuid_registry_matches_database_and_reordered_source(self):
        for id, in self.db.execute('SELECT id FROM content_items'):self.assertEqual(str(uuid.UUID(id)),id)
        shuffled=copy.deepcopy(self.data)
        for rows in shuffled['tables'].values():rows.reverse()
        source=self.folder/'reordered.json';source.write_text(json.dumps(shuffled,ensure_ascii=False))
        path=self.folder/'reordered.sqlite';build(source,path,previous=ROOT/'Tests/Fixtures/content-v4-production.sqlite',production=True)
        with sqlite3.connect(path) as other:self.assertEqual(signatures(self.db),signatures(other))
    def test_actual_swift_keyset_pagination_and_intro_filter(self):
        seen=[];cursor=None
        while True:
            query=self.queries[0]+self.clause(' AND i.level=');values=['intro']
            if cursor:query+=self.clause(' AND (v.sort_key>');values += [cursor[0],cursor[0],cursor[1]]
            rows=self.db.execute(query+self.clause(' ORDER BY'),values+[50]).fetchall()
            if not rows:break
            self.assertLessEqual(len(rows),50);seen.extend(r[0] for r in rows)
            cursor=(rows[-1][3],rows[-1][0])
        self.assertEqual(len(seen),306);self.assertEqual(len(set(seen)),306)
        self.assertTrue({v['id'] for v in self.registry['vocabulary']}.issubset(set(seen)))
        self.assertEqual(self.db.execute(self.queries[0]+self.clause(' AND i.level=')+self.clause(' ORDER BY'),['advanced',50]).fetchall(),[])
    def test_part_of_speech_query_and_targeted_taxonomy(self):
        expected={'noun':515,'pronoun':14,'bound_noun':19,'verb':762,'adjective':296,'adverb':222,'numeral':10,'determiner':6,'expression':133}
        for pos,count in expected.items():
            rows=self.db.execute('SELECT id FROM vocabulary WHERE part_of_speech=?',[pos]).fetchall()
            self.assertEqual(len(rows),count)
        self.assertEqual(self.db.execute("SELECT part_of_speech FROM vocabulary WHERE headword='어떻다'").fetchone()[0],'adjective')
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM vocabulary WHERE headword='어떻게'").fetchone()[0],0)
    def test_korean_japanese_and_secondary_meaning_prefix_search(self):
        query=self.queries[0]+self.clause(' AND v.id IN')+self.clause(' ORDER BY')
        for prefix,expected in [('학교','학교'),('友達','친구'),('食事','밥'),('立ち上がる','일어나다'),('使う','쓰다')]:
            rows=self.db.execute(query,[prefix,prefix+chr(0x10ffff),50]).fetchall()
            self.assertIn(expected,[r[1] for r in rows])
        rows=self.db.execute(query,['쓰다','쓰다'+chr(0x10ffff),50]).fetchall()
        self.assertEqual(len(rows),2);self.assertEqual(len({r[0] for r in rows}),2)
    def test_duplicate_candidates_are_explicitly_reviewed_not_discarded(self):
        warnings=self.report['validation']['warnings']
        self.assertEqual(self.report['validation']['error_count'],0)
        self.assertEqual(Counter(w['code'] for w in warnings),{'short_sentence':5,'duplicate_headword_candidate':5})
        self.assertEqual({w['location'] for w in warnings if w['code']=='duplicate_headword_candidate'},{'차','일','쓰다','저','적다'})
        for word in ['차','일','쓰다']:
            rows=self.db.execute('SELECT v.id,v.part_of_speech,m.meaning_ja FROM vocabulary v JOIN meanings m ON m.vocabulary_id=v.id AND m.ordinal=0 WHERE v.headword=?',[word]).fetchall()
            self.assertEqual(len(rows),2);self.assertNotEqual(rows[0][2],rows[1][2])
    def test_irregular_metadata_without_invented_pronunciation_or_rank(self):
        expected={'듣다':'d','걷다':'d','모르다':'reu','빠르다':'reu','쉽다':'b','어렵다':'b','덥다':'b','춥다':'b','뜨겁다':'b','차갑다':'b','어떻다':'h','하다':'other','공부하다':'other','일하다':'other','좋아하다':'other','피곤하다':'other','닫다':'none','씻다':'none','입다':'none','좋다':'none','크다':'none','팔다':'none'}
        for word,value in expected.items():self.assertEqual(self.db.execute('SELECT irregular_type FROM vocabulary WHERE headword=?',[word]).fetchone()[0],value)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM vocabulary WHERE reading IS NOT NULL OR topik_level IS NOT NULL OR frequency_rank IS NOT NULL').fetchone()[0],0)
        for word,pos,batchim in self.db.execute('SELECT headword,part_of_speech,has_batchim FROM vocabulary'):
            if pos in ('verb','adjective','expression'):self.assertIsNone(batchim)
            else:self.assertEqual(batchim,int((ord(word[-1])-0xac00)%28!=0))
    def test_notes_tags_and_sentence_deduplication(self):
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM content_links l JOIN vocabulary v ON v.id=l.source_id WHERE l.relation='learner_note'").fetchone()[0],382)
        tag=self.registry['batch_tag_id']
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM item_tags it JOIN vocabulary v ON v.id=it.content_id WHERE it.tag_id=?',[tag]).fetchone()[0],226)
        self.assertEqual(self.db.execute('SELECT COUNT(DISTINCT korean) FROM examples e JOIN item_tags it ON it.content_id=e.id WHERE it.tag_id=?',[tag]).fetchone()[0],447)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM vocabulary_examples').fetchone()[0],3894)
    def test_malformed_data01_rows_rejected_by_existing_validator(self):
        vocab=self.registry['vocabulary'][0];eid=vocab['example_ids'][0]
        mutations={
            'duplicate':lambda x:x['tables']['vocabulary'].append(copy.deepcopy(x['tables']['vocabulary'][0])),
            'required':lambda x:x['tables']['vocabulary'][0].pop('headword'),
            'pos':lambda x:x['tables']['vocabulary'][0].update(part_of_speech='名詞'),
            'level':lambda x:next(i for i in x['tables']['content_items'] if i['id']==vocab['id']).update(level='TOPIK1'),
            'translation':lambda x:next(e for e in x['tables']['examples'] if e['id']==eid).update(japanese=''),
            'missing_meaning':lambda x:x['tables']['vocabulary_examples'][0].update(meaning_id='00000000-0000-4000-8000-000000000000'),
            'orphan':lambda x:x['tables'].update(vocabulary_examples=[r for r in x['tables']['vocabulary_examples'] if r['example_id']!=eid],item_tags=[r for r in x['tables']['item_tags'] if r['content_id']!=eid]),
        }
        for name,mutate in mutations.items():
            with self.subTest(name=name):
                data=copy.deepcopy(self.data);mutate(data)
                path=self.folder/f'invalid-{name}.json';path.write_text(json.dumps(data,ensure_ascii=False))
                with self.assertRaises(ValidationError):build(path,self.folder/'must-not-publish.sqlite',production=True)
    def test_bundled_database_matches_validated_source(self):
        with sqlite3.connect((ROOT/'Resources/content.sqlite').as_uri()+'?mode=ro',uri=True) as bundle:
            self.assertEqual(signatures(bundle),signatures(self.db))
            self.assertEqual(bundle.execute('SELECT * FROM content_metadata').fetchall(),self.db.execute('SELECT * FROM content_metadata').fetchall())

if __name__=='__main__':unittest.main()
