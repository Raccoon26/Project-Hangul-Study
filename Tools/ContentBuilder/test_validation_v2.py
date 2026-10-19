import copy, json, sqlite3, tempfile, unittest, uuid
from pathlib import Path
from build_content import ROOT, build
from validator import ValidationError
from generate_synthetic import generate
from migrate_source_v1 import migrate

class ValidationV2Tests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.root=Path(self.temp.name)
        self.data=json.loads((ROOT/'Content/fixture.json').read_text())
    def tearDown(self): self.temp.cleanup()
    def run_build(self,**kwargs):
        source=self.root/'source.json'; source.write_text(json.dumps(self.data))
        return build(source,self.root/'out.sqlite',**kwargs)
    def rejects(self,code):
        with self.assertRaises(ValidationError) as caught: self.run_build()
        self.assertIn(code,{e['code'] for e in caught.exception.report['errors']})
    def test_required_field(self):
        del self.data['tables']['vocabulary'][0]['headword']; self.rejects('required_field')
    def test_level(self):
        self.data['tables']['content_items'][0]['level']='N5'; self.rejects('level')
    def test_pos(self):
        self.data['tables']['vocabulary'][0]['part_of_speech']='made_up'; self.rejects('part_of_speech')
    def test_empty_korean(self):
        self.data['tables']['examples'][0]['korean']='  '; self.rejects('empty_text')
    def test_empty_japanese(self):
        self.data['tables']['examples'][0]['japanese']=''; self.rejects('empty_text')
    def test_long_sentence(self):
        self.data['tables']['examples'][0]['korean']='가'*2001; self.rejects('text_too_long')
    def test_short_sentence_warns_without_deleting(self):
        self.data['tables']['examples'][0]['korean']='네'
        result=self.run_build()
        self.assertIn('short_sentence',{w['code'] for w in result['validation']['warnings']})
        self.assertEqual(result['rows']['examples'],1)
    def test_duplicate_candidates_are_retained(self):
        self.data['tables']['vocabulary'][1]['headword']=self.data['tables']['vocabulary'][0]['headword']
        result=self.run_build()
        self.assertIn('duplicate_headword_candidate',{w['code'] for w in result['validation']['warnings']})
        self.assertEqual(result['rows']['vocabulary'],2)
    def test_orphan_example(self):
        self.data['tables']['vocabulary_examples']=[]; self.rejects('orphan_example')
    def test_missing_grammar_reference(self):
        self.data['tables']['grammar_examples']=[{'grammar_id':str(uuid.uuid4()),'example_id':self.data['tables']['examples'][0]['id']}]
        self.rejects('missing_reference')
    def test_missing_vocabulary_reference(self):
        self.data['tables']['meanings'][0]['vocabulary_id']=str(uuid.uuid4()); self.rejects('missing_reference')
    def test_wrong_relation_kind(self):
        self.data['tables']['content_links'][0]['relation']='synonym'; self.rejects('relation_kind')
    def test_unknown_relation(self):
        self.data['tables']['content_links'][0]['relation']='typo'; self.rejects('relation_type')
    def test_optional_topik_requires_source(self):
        self.data['tables']['vocabulary'][0]['topik_level']=3; self.rejects('constraint')
    def test_schema_mismatch(self):
        self.data['metadata']['schema_version']=1; self.rejects('schema_version')
    def test_reordered_source_keeps_ids_and_revisions(self):
        first=self.run_build(); previous=self.root/'previous.sqlite'; Path(first['path']).rename(previous)
        for rows in self.data['tables'].values(): rows.reverse()
        self.data['metadata']['content_version']+=1
        result=self.run_build(previous=previous)
        with sqlite3.connect(previous) as old,sqlite3.connect(result['path']) as new:
            self.assertEqual(old.execute('SELECT id,revision FROM content_items ORDER BY id').fetchall(),new.execute('SELECT id,revision FROM content_items ORDER BY id').fetchall())
    def test_relationship_revision_required_for_both_endpoints(self):
        first=self.run_build(); previous=self.root/'previous.sqlite'; Path(first['path']).rename(previous)
        link=self.data['tables']['content_links'][0]
        affected={link['source_id'],link['target_id']}
        link['relation']='related'
        self.data['metadata']['content_version']+=1
        with self.assertRaises(ValidationError) as caught: self.run_build(previous=previous)
        self.assertEqual({e['location'] for e in caught.exception.report['errors'] if e['code']=='revision_required'},affected)
        for item in self.data['tables']['content_items']:
            if item['id'] in affected: item['revision']+=1
        self.run_build(previous=previous)
    def test_v1_upgrade_preserves_ids(self):
        migrated=self.root/'migrated.json'
        migrate(ROOT/'Tests/Fixtures/source-v1.json',migrated)
        result=build(migrated,self.root/'upgraded.sqlite',previous=ROOT/'Tests/Fixtures/content-v1.sqlite')
        with sqlite3.connect(ROOT/'Tests/Fixtures/content-v1.sqlite') as old,sqlite3.connect(result['path']) as new:
            self.assertEqual(old.execute('SELECT id FROM content_items ORDER BY id').fetchall(),new.execute('SELECT id FROM content_items ORDER BY id').fetchall())
    def test_source_duplicate_json_key(self):
        source=self.root/'bad.json'; source.write_text('{"metadata":{},"metadata":{},"tables":{}}')
        with self.assertRaises(ValidationError) as caught: build(source,self.root/'out.sqlite')
        self.assertIn('Duplicate JSON key',str(caught.exception))
    def test_jsonl_line_diagnostics_and_no_partial_publication(self):
        source=generate(self.root/'shards',3)
        result=build(source,self.root/'out.sqlite'); original=Path(result['path']).read_bytes()
        with (source/'vocabulary.jsonl').open('a') as f: f.write('{bad json}\n')
        with self.assertRaises(ValidationError) as caught: build(source,self.root/'out.sqlite')
        self.assertIn('vocabulary.jsonl:4',str(caught.exception))
        self.assertEqual(original,Path(result['path']).read_bytes())
    def test_jsonl_duplicate_id_across_shards(self):
        source=generate(self.root/'shards',3)
        manifest=json.loads((source/'manifest.json').read_text())
        (source/'extra.jsonl').write_text((source/'content_items.jsonl').read_text().splitlines()[0]+'\n')
        manifest['tables']['content_items'].append('extra.jsonl')
        (source/'manifest.json').write_text(json.dumps(manifest))
        with self.assertRaises(ValidationError) as caught: build(source,self.root/'out.sqlite')
        self.assertIn('duplicate_id_or_key',str(caught.exception))
    def test_path_traversal_rejected(self):
        source=generate(self.root/'shards',3)
        manifest=json.loads((source/'manifest.json').read_text()); manifest['tables']['vocabulary']=['../outside.jsonl']
        (source/'manifest.json').write_text(json.dumps(manifest))
        with self.assertRaises(ValidationError): build(source,self.root/'out.sqlite')
    def test_synthetic_production_flag_cannot_be_relabeled(self):
        source=generate(self.root/'shards',3)
        manifest=json.loads((source/'manifest.json').read_text()); manifest['metadata'].update(dataset_id='ko-ja-core',is_fixture=0)
        (source/'manifest.json').write_text(json.dumps(manifest))
        with self.assertRaises(ValidationError) as caught: build(source,self.root/'out.sqlite',production=True)
        self.assertIn('synthetic_production',str(caught.exception))
    def test_invalid_question_answer_rejected(self):
        item=copy.deepcopy(self.data['tables']['content_items'][0]); item.update(id=str(uuid.uuid4()),kind='question')
        self.data['tables']['content_items'].append(item)
        self.data['tables']['questions']=[dict(id=item['id'],question_type='multiple_choice',prompt_ja='開発用の問題',explanation_ja='開発用の説明',answer_json='{"correct_choice_ids":["missing"]}')]
        self.rejects('choice_answer')
    def test_negative_priority_and_wrong_integer_type(self):
        self.data['tables']['vocabulary'][0]['learning_priority']=-1; self.rejects('constraint')
        self.data['tables']['vocabulary'][0]['learning_priority']='1'; self.rejects('field_type')
    def test_extreme_integer_is_validation_error(self):
        self.data['tables']['vocabulary'][0]['learning_priority']=2**100
        self.rejects('integer_range')
    def test_invalid_unicode_is_validation_error(self):
        self.data['tables']['examples'][0]['japanese']='\ud800'
        self.rejects('invalid_unicode')
    def test_foreign_keys_stay_enabled(self):
        result=self.run_build()
        with sqlite3.connect(result['path']) as db:
            db.execute('PRAGMA foreign_keys=ON')
            with self.assertRaises(sqlite3.IntegrityError): db.execute("INSERT INTO grammar_examples VALUES('missing','missing')")

class ProgressSeparationTests(unittest.TestCase):
    def test_content_replacement_does_not_change_user_database(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); user=root/'user.sqlite'
            with sqlite3.connect(user) as db:
                db.executescript((ROOT/'Resources/user-schema-v1.sql').read_text())
                db.execute("INSERT INTO item_progress VALUES('00000000-0000-4000-8000-000000000001',1,2,3,2,1,4)")
                db.execute("INSERT INTO favorites VALUES('00000000-0000-4000-8000-000000000001',1)")
                db.execute("INSERT INTO srs_state VALUES('00000000-0000-4000-8000-000000000001','read','future',1,'{}',99,2,2)")
            before=user.read_bytes()
            content=root/'content.sqlite'; content.write_bytes((ROOT/'Tests/Fixtures/content-v1.sqlite').read_bytes())
            build(ROOT/'Content/fixture.json',root/'candidate.sqlite',previous=content)
            (root/'candidate.sqlite').replace(content)
            self.assertEqual(before,user.read_bytes())
            with sqlite3.connect(user) as db:
                db.executescript('BEGIN IMMEDIATE;'+(ROOT/'Resources/user-migration-v2.sql').read_text()+'COMMIT;')
                self.assertEqual(db.execute('SELECT study_count,correct_count,incorrect_count,completed_passes,acquisition_status,perceived_difficulty FROM item_progress').fetchone(),(3,2,1,4,'unassessed',None))
                self.assertEqual(db.execute('SELECT due_at FROM srs_state').fetchone()[0],99)
                self.assertEqual(db.execute('SELECT COUNT(*) FROM favorites').fetchone()[0],1)
                self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0],2)
                with self.assertRaises(sqlite3.IntegrityError): db.execute("UPDATE item_progress SET perceived_difficulty=6")
    def test_migration_rollback_preserves_v1(self):
        with sqlite3.connect(':memory:') as db:
            db.executescript((ROOT/'Resources/user-schema-v1.sql').read_text())
            try:
                db.executescript('BEGIN;'+(ROOT/'Resources/user-migration-v2.sql').read_text()+"INSERT INTO missing VALUES(1); COMMIT;")
            except sqlite3.DatabaseError: db.rollback()
            self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0],1)
            self.assertNotIn('acquisition_status',[r[1] for r in db.execute('PRAGMA table_info(item_progress)')])

if __name__=='__main__': unittest.main()
