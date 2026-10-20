"""Actual production SQLite/extracted Swift SQL; not native Swift/audio execution."""
import copy,json,re,sqlite3,tempfile,unittest
from pathlib import Path
from build_content import ROOT,build
from validator import signatures,ValidationError
class ListeningTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.source=json.loads((ROOT/'Content/production.json').read_text())
  cls.code=(ROOT/'Repositories/SQLiteListening.swift').read_text()
  cls.content_sql=re.findall(r'"""(.*?)"""',cls.code,re.S)[0]
  cls.sql=re.findall(r'"([^"\n]+)"',cls.code)
 def query(self,prefix):return next(q for q in self.sql if q.startswith(prefix))
 def user(self):
  db=sqlite3.connect(':memory:');db.execute('PRAGMA foreign_keys=ON')
  for name in ['user-schema-v1']+[f'user-migration-v{i}' for i in range(2,9)]:db.executescript((ROOT/f'Resources/{name}.sql').read_text())
  return db
 def test_source_levels_tasks_and_no_sentence_duplication(self):
  db=sqlite3.connect(ROOT/'Resources/content.sqlite');db.row_factory=sqlite3.Row
  self.assertEqual(tuple(db.execute('SELECT schema_version,content_version,min_reader_version FROM content_metadata').fetchone()),(4,20,7))
  self.assertEqual(db.execute('SELECT COUNT(*) FROM listening_items').fetchone()[0],1936)
  self.assertEqual(db.execute('SELECT COUNT(*) FROM examples').fetchone()[0],4669)
  for level in ['intro','beginner']:
   rows=db.execute(self.content_sql+' AND i.level=? ORDER BY l.learning_order,l.id LIMIT 20',[level]).fetchall();self.assertEqual(len(rows),20)
   tasks=[json.loads(r['rubric_json'])['listening_task'] for r in rows]
   self.assertEqual({t:tasks.count(t) for t in tasks},dict(meaning=4 if level=='intro' else 8,korean=10 if level=='intro' else 3,dictation=3 if level=='intro' else 6,comprehension=3))
  self.assertEqual(db.execute(self.content_sql+' AND i.level=? ORDER BY l.learning_order,l.id LIMIT 20',['advanced']).fetchall(),[])
  id=db.execute('SELECT id FROM listening_items LIMIT 1').fetchone()[0]
  self.assertEqual(len(db.execute(self.content_sql+' AND l.id IN (?) ORDER BY l.learning_order,l.id LIMIT 20',[id]).fetchall()),1)
  self.assertEqual(db.execute('SELECT COUNT(*) FROM listening_items WHERE transcript_ko IS NOT NULL').fetchone()[0],0);db.close()
 def test_exact_previous_payloads_and_approved_revisions(self):
  old=sqlite3.connect(ROOT/'Tests/Fixtures/content-v9-production.sqlite');new=sqlite3.connect(ROOT/'Tests/Fixtures/content-v10-production.sqlite')
  approved=set(json.loads((ROOT/'Content/dev09-revised-ids.json').read_text()));a,b=signatures(old),signatures(new)
  self.assertEqual({id for id in a if a[id]!=b[id]},approved);self.assertEqual(len(approved),24)
  for row in old.execute('SELECT * FROM content_items'):
   expected=list(row)
   if row[0] in approved:expected[2]+=1;expected[-1]='2026-10-02T10:20:00Z'
   self.assertEqual(new.execute('SELECT * FROM content_items WHERE id=?',[row[0]]).fetchone(),tuple(expected))
  for table in ['vocabulary','meanings','examples','grammar','questions','pronunciation_rules','hangul']:
   for row in old.execute('SELECT * FROM '+table):self.assertEqual(new.execute('SELECT * FROM '+table+' WHERE id=?',[row[0]]).fetchone(),row)
  old.close();new.close()
 def test_validator_rejects_bad_source_audio_level_answers_and_distractors(self):
  with tempfile.TemporaryDirectory() as folder:
   for case in ['missing','empty','synonym','duplicate','wrong_korean','level','audio','leak','noquestion','id','order','question_level']:
    d=copy.deepcopy(self.source);t=d['tables'];l=t['listening_items'][0];q=next(q for q in t['questions'] if q.get('listening_id')==l['id'])
    if case=='missing':l['source_example_id']='00000000-0000-4000-8000-000000000000'
    elif case in ['empty','synonym']:
     q=next(q for q in t['questions'] if q['question_type']=='listening_input');q['answer_json']=json.dumps({'accepted':[] if case=='empty' else ['물을 마십니다.']})
    elif case=='duplicate':
     choices=[c for c in t['question_choices'] if c['question_id']==q['id']];choices[1]['text']=choices[0]['text']
    elif case=='wrong_korean':
     q=next(q for q in t['questions'] if q.get('listening_id') and json.loads(q['rubric_json'])['listening_task']=='korean');next(c for c in t['question_choices'] if c['question_id']==q['id'])['text']='dummy invalid'
    elif case=='level':next(i for i in t['content_items'] if i['id']==l['id'])['level']='master'
    elif case=='audio':l['audio_mode']='recorded_required'
    elif case=='leak':q['prompt_ko']='정답 미리 표시'
    elif case=='noquestion':t['questions']=[r for r in t['questions'] if r['id']!=q['id']]
    elif case=='id':t['listening_items'].append(copy.deepcopy(l))
    elif case=='order':t['listening_items'][1]['learning_order']=l['learning_order']
    elif case=='question_level':next(i for i in t['content_items'] if i['id']==q['id'])['level']='advanced'
    p=Path(folder)/'bad.json';p.write_text(json.dumps(d,ensure_ascii=False))
    with self.subTest(case=case),self.assertRaises(ValidationError):build(p,Path(folder)/'bad.sqlite',production=True)
 def test_migration_snapshot_play_answer_and_duplicate_protection(self):
  with tempfile.TemporaryDirectory() as folder:
   p=Path(folder)/'user.sqlite';db=sqlite3.connect(p)
   for name in ['user-schema-v1']+[f'user-migration-v{i}' for i in range(2,8)]:db.executescript((ROOT/f'Resources/{name}.sql').read_text())
   db.execute("INSERT INTO srs_state VALUES('old','vocabulary','calendar_steps',1,'original',123,NULL,1)");db.commit()
   before=db.execute('SELECT * FROM srs_state').fetchall();db.executescript((ROOT/'Resources/user-migration-v8.sql').read_text());self.assertEqual(before,db.execute('SELECT * FROM srs_state').fetchall())
   db.execute('PRAGMA foreign_keys=ON');payload=json.dumps({'position':3,'retry':[0,2],'result':'spacing','answer':'물을마셔요','revision':9,'heard':True,'questions':['stable-a','stable-b']})
   db.execute(self.query('INSERT INTO listening_sessions'),['session','practice:intro',payload,0])
   db.execute(self.query('INSERT INTO listening_plays'),['session','q',1,0,100]);db.execute(self.query('INSERT INTO listening_plays'),['session','q',0,1,101])
   values=['session','q',0,'item','dictation','물을마셔요','spacing',0,101,200]
   db.execute(self.query('INSERT INTO listening_attempts'),values);db.commit()
   with self.assertRaises(sqlite3.IntegrityError):db.execute(self.query('INSERT INTO listening_attempts'),values)
   db.rollback();db.close();db=sqlite3.connect(p)
   self.assertEqual(db.execute(self.query('SELECT state_json FROM listening_sessions WHERE scope='),['practice:intro']).fetchone()[0],payload)
   self.assertEqual(db.execute('SELECT normal_count,slow_count FROM listening_plays').fetchone(),(1,1));self.assertEqual(db.execute('SELECT result FROM listening_attempts').fetchone()[0],'spacing');self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0],8);db.close()
 def test_due_backlog_upsert_preserves_other_skill(self):
  db=self.user();insert=self.query('INSERT INTO srs_state')
  for i in range(45):db.execute(insert,[f'item-{i:03}','calendar_steps',1,'{"stage":0}',100,None,0])
  db.execute(insert,['future','calendar_steps',1,'{"stage":0}',1000,None,0]);db.execute("INSERT INTO srs_state VALUES('item-000','vocabulary','calendar_steps',1,'unchanged',10,NULL,0)")
  ids=db.execute(self.query('SELECT content_id FROM srs_state WHERE skill='),['calendar_steps',1,100]).fetchall();self.assertEqual(len(ids),20);self.assertEqual(ids[0][0],'item-000')
  count=self.query('SELECT COUNT(*) AS n FROM srs_state WHERE skill=');self.assertEqual(db.execute(count,['calendar_steps',1,100]).fetchone()[0],45)
  db.execute(insert,['item-000','calendar_steps',1,'{"stage":1}',200,100,100]);self.assertEqual(db.execute("SELECT state_json FROM srs_state WHERE content_id='item-000' AND skill='vocabulary'").fetchone()[0],'unchanged');self.assertEqual(db.execute(count,['calendar_steps',1,100]).fetchone()[0],44)
  self.assertIn('INDEX',str(db.execute('EXPLAIN QUERY PLAN '+self.query('SELECT content_id FROM srs_state WHERE skill='),['calendar_steps',1,100]).fetchall()));db.close()
 def test_all_new_sql_prepares(self):
  user=self.user();content=sqlite3.connect(ROOT/'Resources/content.sqlite')
  for sql in self.sql:
   if sql.startswith(('SELECT ','INSERT ','UPDATE ')):
    db=content if ('FROM question_choices' in sql or 'FROM listening_items' in sql) else user;db.execute('EXPLAIN '+sql,[None]*sql.count('?'))
  user.close();content.close()

 def test_batch_pagination_is_bounded_and_editorial_order_stable(self):
  db=sqlite3.connect(':memory:');source=sqlite3.connect(ROOT/'Tests/Fixtures/content-v10-production.sqlite');source.backup(db);source.close()
  query=self.query('SELECT l.learning_order/20 AS batch')
  self.assertEqual(db.execute(query,['intro',-1]).fetchall(),[(0,12)])
  id=db.execute("SELECT l.id FROM listening_items l JOIN content_items i ON i.id=l.id WHERE i.level='intro' ORDER BY l.learning_order DESC LIMIT 1").fetchone()[0]
  db.execute('UPDATE listening_items SET learning_order=20 WHERE id=?',[id])
  self.assertEqual(db.execute(query,['intro',0]).fetchall(),[(1,1)])
  batch=self.query('SELECT l.id FROM listening_items')
  self.assertEqual(db.execute(batch,['intro',20,40]).fetchall(),[(id,)])
  self.assertEqual(len(db.execute(batch,['intro',0,20]).fetchall()),11)
  db.close()
