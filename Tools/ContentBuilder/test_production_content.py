import json,re,sqlite3,unittest
from pathlib import Path
from validator import signatures
ROOT=Path(__file__).resolve().parents[2]
class ProductionTests(unittest.TestCase):
 def test_existing_ids_payloads_and_explicit_relationship_revisions(self):
  old=sqlite3.connect(ROOT/'Tests/Fixtures/content-v8-production.sqlite');new=sqlite3.connect(ROOT/'Tests/Fixtures/content-v10-production.sqlite')
  revised=set(json.loads((ROOT/'Content/dev08-revised-ids.json').read_text()))
  before,after=signatures(old),signatures(new)
  later=set(json.loads((ROOT/'Content/dev09-revised-ids.json').read_text()))
  self.assertEqual({k for k in before if before[k]!=after[k]},revised | later)
  self.assertEqual(len(revised),23)
  for row in old.execute('SELECT * FROM content_items'):
   current=new.execute('SELECT * FROM content_items WHERE id=?',(row[0],)).fetchone()
   expected=list(row)
   if row[0] in revised:expected[2]+=1;expected[-1]='2026-10-02T00:00:00Z'
   if row[0] in later:expected[2]+=1;expected[-1]='2026-10-02T10:20:00Z'
   self.assertEqual(current,tuple(expected))
  for table in ['vocabulary','meanings','examples','grammar','questions']:
   for row in old.execute('SELECT * FROM '+table):self.assertEqual(new.execute('SELECT * FROM '+table+' WHERE id=?',(row[0],)).fetchone(),row)
  old.close();new.close()
 def test_real_production_pool_and_bounded_queries(self):
  db=sqlite3.connect(ROOT/'Resources/content.sqlite');registry=json.loads((ROOT/'Content/production-drill-ids.json').read_text())
  self.assertEqual(len(registry),49);forms=set();modes=set();targets=set()
  for id in registry:
   row=db.execute('SELECT answer_json,rubric_json FROM questions WHERE id=?',(id,)).fetchone();a,r=map(json.loads,row)
   self.assertTrue(all(x.strip() for x in a['accepted']));forms.add(r['form']);modes.add(r['mode'])
   target=db.execute("SELECT v.id FROM content_links l JOIN vocabulary v ON v.id=l.target_id WHERE l.source_id=? AND l.relation='question_target'",(id,)).fetchone();self.assertIsNotNone(target);targets.add(target[0])
  self.assertEqual(len(targets),16);self.assertEqual(len(forms),9);self.assertEqual(modes,{'form','blank','sentence'})
  source=(ROOT/'Repositories/SQLiteProduction.swift').read_text()
  for query in re.findall(r'db.query\("([^"]+)"',source):
   if 'FROM questions' in query or 'FROM vocabulary' in query:
    self.assertIn('LIMIT',query);db.execute('EXPLAIN '+query,['']*query.count('?'))
  db.close()
 def test_additive_migration_preserves_srs_and_session_disk_snapshot(self):
  import tempfile
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/'user.sqlite';db=sqlite3.connect(path)
   for name in ['user-schema-v1']+[f'user-migration-v{i}' for i in range(2,7)]:db.executescript((ROOT/f'Resources/{name}.sql').read_text())
   db.execute("INSERT INTO srs_state VALUES('old','vocabulary','calendar_steps',1,'{}',123,NULL,1)");db.commit()
   before=db.execute('SELECT * FROM srs_state').fetchall();db.executescript((ROOT/'Resources/user-migration-v7.sql').read_text());self.assertEqual(db.execute('SELECT * FROM srs_state').fetchall(),before)
   payload=json.dumps({'position':2,'retry':[0,1],'result':'spacing','answer':'먹을거예요'})
   db.execute("INSERT INTO production_sessions VALUES('s','v',?,0)",(payload,));db.commit();db.close()
   db=sqlite3.connect(path);self.assertEqual(db.execute('SELECT state_json FROM production_sessions').fetchone()[0],payload);self.assertEqual(db.execute('pragma user_version').fetchone()[0],7);db.close()
 def test_validator_rejects_invalid_production_contract(self):
  import copy,tempfile
  from build_content import build
  from validator import ValidationError
  source=json.loads((ROOT/'Content/production.json').read_text());ids=json.loads((ROOT/'Content/production-drill-ids.json').read_text())
  with tempfile.TemporaryDirectory() as tmp:
   for case in ['form','empty','override','target','reader']:
    d=copy.deepcopy(source);q=next(q for q in d['tables']['questions'] if q['id']==ids[0]);r=json.loads(q['rubric_json'])
    if case=='form':r['form']='imaginary'
    if case=='empty':q['answer_json']='{"accepted":[""]}'
    if case=='override':r['overrides']={'present':''}
    if case=='target':d['tables']['content_links']=[x for x in d['tables']['content_links'] if x['source_id']!=q['id']]
    if case=='reader':d['metadata']['min_reader_version']=5
    q['rubric_json']=json.dumps(r);p=Path(tmp)/'bad.json';p.write_text(json.dumps(d,ensure_ascii=False))
    with self.subTest(case=case),self.assertRaises(ValidationError):build(p,Path(tmp)/'bad.sqlite',production=True)
