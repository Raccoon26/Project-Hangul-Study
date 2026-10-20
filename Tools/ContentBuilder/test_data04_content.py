"""DATA-04 actual release data + extracted repository SQL. No claim of Swift execution."""
import copy,json,re,sqlite3,tempfile,unittest
from pathlib import Path
from build_content import ROOT,build
from validator import signatures,ValidationError
class Data04Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.source=json.loads((ROOT/'Content/production.json').read_text());cls.ids=json.loads((ROOT/'Content/data04-ids.json').read_text())
  cls.db=sqlite3.connect(ROOT/'Resources/content.sqlite');cls.old=sqlite3.connect(ROOT/'Tests/Fixtures/content-v10-production.sqlite')
  code=(ROOT/'Repositories/SQLiteGrammarContent.swift').read_text();cls.sql=re.findall(r'"""(.*?)"""',code,re.S)+re.findall(r'"([^"\n]+)"',code)
 @classmethod
 def tearDownClass(cls):cls.db.close();cls.old.close()
 def query(self,start):return next(q for q in self.sql if q.strip().startswith(start))
 def test_rebuild_with_strict_previous_release_gate(self):
  with tempfile.TemporaryDirectory() as folder:
   p=Path(folder)/'content.sqlite';report=build(ROOT/'Content/production.json',p,ROOT/'Tests/Fixtures/content-v10-repaired-production.sqlite',production=True)
   self.assertEqual(report['validation']['error_count'],0);self.assertEqual(report['validation']['warning_count'],10)
   self.assertNotIn('duplicate_grammar_candidate',[w['code'] for w in report['validation']['warnings']])
   with sqlite3.connect(p) as rebuilt:self.assertEqual(signatures(rebuilt),signatures(self.db))
  self.assertEqual(self.db.execute('SELECT schema_version,content_version,min_reader_version,is_fixture FROM content_metadata').fetchone(),(4,23,7,0))
 def test_exact_delta_and_old_ids_payloads_membership_are_preserved(self):
  baseline=sqlite3.connect(ROOT/'Tests/Fixtures/content-v11-production.sqlite');self.addCleanup(baseline.close)
  # Pin this historical v10→v11 gate; DATA-05 tests strictly gate v11→current.
  expected={'grammar':(12,42),'examples':(1484,1537),'questions':(187,250),'lessons':(30,38),'listening_items':(24,27),'vocabulary':(726,726),'meanings':(772,772)}
  for table,(before,after) in expected.items():
   self.assertEqual(self.old.execute('SELECT COUNT(*) FROM '+table).fetchone()[0],before);self.assertEqual(baseline.execute('SELECT COUNT(*) FROM '+table).fetchone()[0],after)
  a,b=signatures(self.old),signatures(baseline);changed=set(json.loads((ROOT/'Content/data04-revised-ids.json').read_text()))
  self.assertEqual({id for id in a if a[id]!=b[id]},changed);self.assertEqual(len(changed),13)
  wish='893f53f1-ebaa-48d0-82ab-aadd66e84d80'
  for row in self.old.execute('SELECT * FROM content_items'):
   expected=list(row)
   if row[0] in changed:expected[2]+=1;expected[-1]='2026-10-03T00:40:00Z'
   self.assertEqual(baseline.execute('SELECT * FROM content_items WHERE id=?',[row[0]]).fetchone(),tuple(expected))
  for table in ['vocabulary','meanings','examples','questions','lessons','courses','pronunciation_rules','hangul','listening_items']:
   for row in self.old.execute('SELECT * FROM '+table):self.assertEqual(baseline.execute('SELECT * FROM '+table+' WHERE id=?',[row[0]]).fetchone(),row)
  for row in self.old.execute('SELECT * FROM grammar'):
   current=baseline.execute('SELECT * FROM grammar WHERE id=?',[row[0]]).fetchone()
   if row[0]==wish:self.assertEqual(current[:-1],row[:-1]);self.assertTrue(current[-1].startswith(row[-1]))
   else:self.assertEqual(current,row)
  for row in self.old.execute('SELECT * FROM lesson_items'):
   self.assertIn(row,baseline.execute('SELECT * FROM lesson_items WHERE lesson_id=?',[row[0]]).fetchall())
  self.assertEqual(baseline.execute('PRAGMA integrity_check').fetchone()[0],'ok');self.assertEqual(baseline.execute('PRAGMA foreign_key_check').fetchall(),[])
 def test_all_new_lessons_are_reachable_with_bounded_actual_queries(self):
  query=self.query('SELECT l.id,l.title_ja');members=self.query('SELECT g.id FROM lesson_items')
  for level,total in [('intro',22),('beginner',20)]:
   lessons=[];after=-1
   while True:
    page=self.db.execute(query,[level,after,2]).fetchall()
    if not page:break
    lessons+=page;after=page[-1][2]
   self.assertEqual(len(lessons),6);self.assertEqual(sum(l[3] for l in lessons),total)
   for lid,_,_,count in lessons:self.assertEqual(len(self.db.execute(members,[lid]).fetchall()),count)
  self.assertEqual({g['id'] for g in self.ids['grammar']},{r[0] for l in self.ids['lessons'] for r in self.db.execute(members,[l['id']])})
 def test_new_card_examples_questions_and_comparison_contract(self):
  lookup=self.query('SELECT g.*,i.revision');examples=self.query('SELECT e.id,e.korean');questions=self.query('SELECT q.*,i.revision');comparisons=self.query('SELECT g.id,g.pattern')
  self.db.row_factory=sqlite3.Row
  try:
   for g in self.ids['grammar']:
    row=self.db.execute(lookup,[g['id']]).fetchone()
    for field in ['meaning_ja','explanation_ja','form_ko','usage_constraints_ja']:self.assertTrue(row[field].strip())
    es=self.db.execute(examples,[g['id']]).fetchall();self.assertTrue(set(g['examples']).issubset({e['id'] for e in es}));self.assertLessEqual(len(es),6)
    qs=self.db.execute(questions,[g['id']]).fetchall();self.assertEqual(len(qs),2)
    for q in qs:
     choices=self.db.execute('SELECT choice_id,text FROM question_choices WHERE question_id=?',[q['id']]).fetchall();correct=json.loads(q['answer_json'])['correct_choice_ids']
     self.assertEqual(len(choices),3);self.assertEqual(len(correct),1);self.assertIn(correct[0],[c[0] for c in choices]);self.assertTrue(q['explanation_ja'].strip())
    for comparison in self.db.execute(comparisons,[g['id']]):self.assertTrue(comparison['confusion_ja'].strip())
  finally:self.db.row_factory=None
 def test_direct_input_and_listening_use_existing_sources_and_queries(self):
  code=(ROOT/'Repositories/SQLiteProduction.swift').read_text();queries=re.findall(r'"([^"\n]+)"',code)
  query=next(q for q in queries if q.startswith('SELECT q.*'))
  self.db.row_factory=sqlite3.Row
  try:
   expected={'present':'가요','past':'갔어요','future':'먹을 거예요','negativeShort':'안 가요','negativeLong':'먹지 않아요'}
   for x in self.ids['direct_input']:
    target=self.db.execute("SELECT target_id FROM content_links WHERE source_id=? AND relation='question_target'",[x['question_id']]).fetchone()[0]
    q=next(q for q in self.db.execute(query,[target]) if q['id']==x['question_id']);self.assertIn(expected[x['form']],json.loads(q['answer_json'])['accepted'])
    self.assertEqual(self.db.execute("SELECT target_id FROM content_links WHERE source_id=? AND relation='prerequisite'",[q['id']]).fetchone()[0],x['grammar_id'])
   listen=re.findall(r'"""(.*?)"""',(ROOT/'Repositories/SQLiteListening.swift').read_text(),re.S)[0]
   for x in self.ids['listening']:
    rows=self.db.execute(listen+' AND l.id IN (?) ORDER BY l.learning_order,l.id LIMIT 20',[x['id']]).fetchall();self.assertEqual(len(rows),1)
    self.assertIsNotNone(self.db.execute('SELECT 1 FROM grammar_examples WHERE grammar_id=? AND example_id=?',[x['grammar_id'],x['example_id']]).fetchone())
  finally:self.db.row_factory=None
 def test_existing_progress_disk_survives_content_replacement_and_new_due_enrollment(self):
  code=(ROOT/'Repositories/SQLiteGrammarProgress.swift').read_text();sql=re.findall(r'"([^"\n]+)"',code)
  insert=next(q for q in sql if q.startswith('INSERT INTO srs_state('));due=next(q for q in sql if q.startswith("SELECT content_id FROM srs_state WHERE skill='grammar'"))
  with tempfile.TemporaryDirectory() as folder:
   p=Path(folder)/'UserProgress.sqlite';user=sqlite3.connect(p)
   for name in ['user-schema-v1']+[f'user-migration-v{i}' for i in range(2,9)]:user.executescript((ROOT/f'Resources/{name}.sql').read_text())
   oldword=self.old.execute('SELECT id FROM vocabulary LIMIT 1').fetchone()[0];oldgrammar=self.old.execute('SELECT id FROM grammar LIMIT 1').fetchone()[0]
   for id,skill in [(oldword,'vocabulary'),(oldgrammar,'grammar')]:user.execute('INSERT INTO srs_state VALUES(?,?,?,?,?,?,?,?)',[id,skill,'calendar_steps',1,'{"stage":4}',200,None,10])
   saved={'ids':[oldgrammar],'order':[oldgrammar],'position':0,'page':2,'contentVersion':10}
   user.execute('INSERT INTO grammar_sessions VALUES(?,?,?,?,?,?)',['existing','old-lesson',json.dumps(saved),3,'active',10]);user.commit();user.close()
   # Reopen UserProgress alongside the new, independently replaced Content DB.
   user=sqlite3.connect(p);self.assertEqual(json.loads(user.execute('SELECT state_json FROM grammar_sessions').fetchone()[0]),saved)
   for id in [oldword,oldgrammar]:self.assertIsNotNone(self.db.execute('SELECT id FROM content_items WHERE id=?',[id]).fetchone())
   g=self.ids['grammar'][0]['id'];user.execute(insert,[g,'calendar_steps',1,'{"stage":0}',100,10]);user.execute(insert,[oldgrammar,'calendar_steps',1,'{"stage":0}',1,10])
   self.assertEqual(user.execute('SELECT state_json,due_at FROM srs_state WHERE content_id=?',[oldgrammar]).fetchone(),('{"stage":4}',200))
   self.assertEqual(user.execute(due,['calendar_steps',1,100]).fetchall(),[(g,)]);user.commit();user.close()
   with sqlite3.connect(p) as cold:self.assertEqual(cold.execute('SELECT COUNT(*) FROM srs_state').fetchone()[0],3)
 def test_new_grammar_invalid_contracts_are_rejected(self):
  first=self.ids['grammar'][0]
  with tempfile.TemporaryDirectory() as folder:
   for case in ['orphan','empty_form','empty_meaning','empty_answer','bad_level','bad_relation']:
    d=copy.deepcopy(self.source);t=d['tables'];g=next(g for g in t['grammar'] if g['id']==first['id']);q=next(q for q in t['questions'] if q['id']==first['questions'][0])
    if case=='orphan':t['content_links']=[l for l in t['content_links'] if not(l['source_id']==q['id'] and l['relation']=='question_target')]
    if case=='empty_form':g['form_ko']=''
    if case=='empty_meaning':g['meaning_ja']=''
    if case=='empty_answer':q['answer_json']='{"correct_choice_ids":[]}'
    if case=='bad_level':next(i for i in t['content_items'] if i['id']==g['id'])['level']='invalid'
    if case=='bad_relation':t['content_links'].append(dict(source_id=g['id'],target_id=first['examples'][0],relation='similar_grammar'))
    p=Path(folder)/'bad.json';p.write_text(json.dumps(d,ensure_ascii=False))
    with self.subTest(case=case),self.assertRaises(ValidationError):build(p,Path(folder)/'bad.sqlite',production=True)
 def test_spacing_only_grammar_duplicate_still_reported(self):
  d=copy.deepcopy(self.source);t=d['tables'];t['grammar'][1]['pattern']=''.join(t['grammar'][0]['pattern'].split())
  with tempfile.TemporaryDirectory() as folder:
   p=Path(folder)/'candidate.json';p.write_text(json.dumps(d,ensure_ascii=False));r=build(p,Path(folder)/'candidate.sqlite',production=True)
   self.assertIn('duplicate_grammar_candidate',[w['code'] for w in r['validation']['warnings']])

 def test_schema_header_matches_metadata_and_bad_ddl_is_rejected(self):
  from unittest.mock import patch
  self.assertEqual(self.db.execute('PRAGMA user_version').fetchone()[0],4)
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);(root/'Content').mkdir()
   ddl=(ROOT/'Content/content-schema-v4.sql').read_text().replace('PRAGMA user_version = 4;','PRAGMA user_version = 3;')
   (root/'Content/content-schema-v4.sql').write_text(ddl)
   with patch('build_content.ROOT',root),self.assertRaises(ValidationError) as error:build(ROOT/'Content/production.json',root/'bad.sqlite',production=True)
   self.assertIn('schema_header',[e['code'] for e in error.exception.report['errors']])
 def test_legacy_header_repair_is_hash_locked_and_preserves_all_semantics(self):
  from repair_dev09_header import repair
  with tempfile.TemporaryDirectory() as folder:
   output=Path(folder)/'repaired.sqlite';repair(ROOT/'Tests/Fixtures/content-v10-production.sqlite',output)
   with sqlite3.connect(output) as fixed:
    self.assertEqual(fixed.execute('PRAGMA user_version').fetchone()[0],4)
    self.assertEqual(signatures(fixed),signatures(self.old))
    self.assertEqual(fixed.execute('SELECT * FROM sqlite_master ORDER BY name').fetchall(),self.old.execute('SELECT * FROM sqlite_master ORDER BY name').fetchall())
   with self.assertRaises(ValueError):repair(ROOT/'Resources/content.sqlite',Path(folder)/'not-legacy.sqlite')
