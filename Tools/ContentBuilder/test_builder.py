import copy, json, sqlite3, tempfile, unittest
from pathlib import Path
from build_content import ROOT, build

class BuilderTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.directory=Path(self.temp.name)
        self.data=json.loads((ROOT/'Content/fixture.json').read_text())
    def tearDown(self): self.temp.cleanup()
    def run_build(self,data=None,name='out.sqlite',**kwargs):
        source=self.directory/'source.json'
        source.write_text(json.dumps(self.data if data is None else data))
        output=self.directory/name
        build(source,output,**kwargs)
        return output
    def test_fixture_integrity_and_relations(self):
        with sqlite3.connect(self.run_build()) as db:
            self.assertEqual(db.execute('PRAGMA integrity_check').fetchone()[0],'ok')
            self.assertEqual(db.execute('PRAGMA foreign_key_check').fetchall(),[])
            self.assertEqual(db.execute('SELECT COUNT(*) FROM vocabulary').fetchone()[0],2)
    def test_fixture_forbidden_in_production(self):
        with self.assertRaises(ValueError): self.run_build(production=True)
    def test_duplicate_id_rejected(self):
        self.data['tables']['content_items'].append(self.data['tables']['content_items'][0])
        with self.assertRaises(ValueError): self.run_build()
    def test_invalid_id_rejected(self):
        self.data['tables']['content_items'][0]['id']='generated-from-position'
        with self.assertRaises(ValueError): self.run_build()
    def test_dangling_reference_rejected(self):
        self.data['tables']['lesson_items'][0]['content_id']='missing'
        with self.assertRaises(ValueError): self.run_build()
    def test_wrong_kind_rejected(self):
        self.data['tables']['content_items'][0]['kind']='grammar'
        with self.assertRaises(ValueError): self.run_build()
    def test_unknown_table_rejected(self):
        self.data['tables']['bad; DROP TABLE vocabulary']=[]
        with self.assertRaises(ValueError): self.run_build()
    def test_revision_required(self):
        old=self.run_build(name='old.sqlite')
        self.data['metadata']['content_version']+=1
        self.data['tables']['vocabulary'][0]['headword']='변경'
        with self.assertRaises(ValueError): self.run_build(previous=old)
        self.data['tables']['content_items'][0]['revision']+=1
        self.run_build(previous=old)
    def test_removal_rejected_but_tombstone_allowed(self):
        old=self.run_build(name='old.sqlite')
        self.data['metadata']['content_version']+=1
        item=self.data['tables']['content_items'].pop()
        self.data['tables']['learner_notes']=[]
        self.data['tables']['content_links']=[]
        with self.assertRaises(ValueError): self.run_build(previous=old)
        self.data=json.loads((ROOT/'Content/fixture.json').read_text())
        self.data['metadata']['content_version']+=1
        self.data['tables']['content_items'][-1]['is_active']=0
        self.data['tables']['content_items'][-1]['revision']+=1
        self.run_build(previous=old)
    def test_failed_import_preserves_previous_output(self):
        output=self.run_build()
        original=output.read_bytes()
        self.data['tables']['vocabulary'][0]['unexpected']='bad'
        with self.assertRaises(ValueError): self.run_build()
        self.assertEqual(original,output.read_bytes())
    def test_future_reader_rejected(self):
        self.data['metadata']['min_reader_version']=999
        with self.assertRaises(ValueError): self.run_build()
    def test_user_schema_and_no_content_fk(self):
        with sqlite3.connect(':memory:') as db:
            db.executescript((ROOT/'Resources/user-schema-v1.sql').read_text())
            db.execute("INSERT INTO favorites VALUES('retired-content',0)")
            self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0],1)
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute("INSERT INTO item_progress(content_id,first_seen_at,last_seen_at,study_count) VALUES('x',0,0,-1)")
    def test_dataset_or_version_downgrade_rejected(self):
        old=self.run_build(name='old.sqlite')
        with self.assertRaises(ValueError): self.run_build(previous=old)
        self.data['metadata']['content_version']+=1
        self.data['metadata']['dataset_id']='different'
        with self.assertRaises(ValueError): self.run_build(previous=old)
    def test_empty_production_package(self):
        data=json.loads((ROOT/'Content/production-empty.json').read_text())
        self.run_build(data,production=True)

if __name__=='__main__': unittest.main()
