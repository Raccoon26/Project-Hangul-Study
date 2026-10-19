"""DEV-07 real SQLite/validator integration; Swift engine tests require Xcode."""
import copy,json,re,sqlite3,tempfile,unittest
from pathlib import Path
from build_content import ROOT,build
from validator import signatures,ValidationError

class GrammarContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.folder=Path(cls.tmp.name)
        cls.source=json.loads((ROOT/'Content/production.json').read_text())
        cls.path=cls.folder/'production.sqlite'
        cls.report=build(ROOT/'Content/production.json',cls.path,previous=ROOT/'Tests/Fixtures/content-v7-production.sqlite',production=True)
        cls.db=sqlite3.connect(cls.path)
        cls.registry=json.loads((ROOT/'Content/grammar-seed-ids.json').read_text())
        content=(ROOT/'Repositories/SQLiteGrammarContent.swift').read_text()
        cls.csql=re.findall(r'"""(.*?)"""',content,re.S)+re.findall(r'"([^"\n]+)"',content)
        user=(ROOT/'Repositories/SQLiteGrammarProgress.swift').read_text()
        cls.usql=re.findall(r'"([^"\n]+)"',user)
    @classmethod
    def tearDownClass(cls):cls.db.close();cls.tmp.cleanup()
    def query(self,prefix,queries=None):return next(q for q in (queries or self.csql) if q.strip().startswith(prefix))
    def user(self):
        db=sqlite3.connect(':memory:');db.execute('PRAGMA foreign_keys=ON')
        for name in ['user-schema-v1']+[f'user-migration-v{i}' for i in range(2,7)]:db.executescript((ROOT/f'Resources/{name}.sql').read_text())
        return db
    def test_production_counts_versions_and_preserved_old_content(self):
        self.assertEqual(self.db.execute('SELECT schema_version,content_version,min_reader_version FROM content_metadata').fetchone(),(4,16,7))
        for table,n in [('grammar',42),('grammar_examples',152),('questions',354),('vocabulary',1977),('examples',3978),('courses',4),('lessons',38)]:self.assertEqual(self.db.execute('SELECT COUNT(*) FROM '+table).fetchone()[0],n)
        with sqlite3.connect(ROOT/'Tests/Fixtures/content-v7-production.sqlite') as old:
            before,after=signatures(old),signatures(self.db)
            self.assertEqual(len(before),3380);self.assertTrue(all(after[id]==sig for id,sig in before.items() if id not in (json.loads((ROOT/"Content/dev08-revised-ids.json").read_text()) + json.loads((ROOT/"Content/dev09-revised-ids.json").read_text()) + json.loads((ROOT/"Content/data04-revised-ids.json").read_text()) + json.loads((ROOT/"Content/data05-revised-ids.json").read_text()) + json.loads((ROOT/"Content/data06-revised-ids.json").read_text()) + json.loads((ROOT/"Content/data07-revised-ids.json").read_text()) + json.loads((ROOT/"Content/data08-a-revised-ids.json").read_text()) + json.loads((ROOT/"Content/data08-b-revised-ids.json").read_text()))))
        self.assertEqual(self.report['validation']['error_count'],0)
        with sqlite3.connect(ROOT/'Resources/content.sqlite') as bundle:self.assertEqual(signatures(bundle),signatures(self.db))
    def test_actual_repository_level_lesson_search_example_comparison_queries(self):
        lessons=self.query('SELECT l.id,l.title_ja')
        search=self.query('SELECT g.id FROM grammar g JOIN content_items')
        lookup=self.query('SELECT g.*,i.revision')
        examples=self.query('SELECT e.id,e.korean')
        comparisons=self.query('SELECT g.id,g.pattern')
        for level in ['intro','beginner']:
            first=self.db.execute(lessons,[level,-1,1]).fetchall();self.assertEqual(len(first),1)
            second=self.db.execute(lessons,[level,first[0][2],1]).fetchall();self.assertEqual(len(second),1)
            self.assertNotEqual(first[0][0],second[0][0])
        self.assertEqual(self.db.execute(lessons,['master',-1,30]).fetchall(),[])
        for word in ['고 싶다','〜したい']:
            self.assertEqual(len(self.db.execute(search,['beginner','',word,word,word,50]).fetchall()),1)
        relation_count=0
        for item in self.registry:
            self.assertIsNotNone(self.db.execute(lookup,[item['id']]).fetchone())
            self.assertTrue(set(item['examples']).issubset({row[0] for row in self.db.execute(examples,[item['id']])}))
            relation_count+=len(self.db.execute(comparisons,[item['id']]).fetchall())
        self.assertEqual(relation_count,11)
    def test_five_question_tasks_choices_and_targets(self):
        tasks=set()
        query=self.query('SELECT q.*,i.revision')
        self.db.row_factory=sqlite3.Row
        try:
            for g in self.registry:
                rows=self.db.execute(query,[g['id']]).fetchall();self.assertEqual(len(rows),2)
                for q in rows:
                    task=json.loads(q['rubric_json'])['grammar_task'];tasks.add(task)
                    choices=self.db.execute('SELECT choice_id,text FROM question_choices WHERE question_id=?',[q['id']]).fetchall()
                    answer=json.loads(q['answer_json'])['correct_choice_ids']
                    self.assertEqual(len(answer),1);self.assertIn(answer[0],[c[0] for c in choices])
                    self.assertEqual(len({c[1] for c in choices}),len(choices))
        finally:self.db.row_factory=None
        self.assertEqual(tasks,{'meaning','context','blank','form','contrast'})
    def test_missing_explanation_bad_relation_invalid_task_and_old_reader_rejected(self):
        gid=self.registry[0]['id'];qid=self.registry[0]['questions'][0]
        changes={
          'empty':lambda d:next(g for g in d['tables']['grammar'] if g['id']==gid).update(explanation_ja=''),
          'form':lambda d:next(g for g in d['tables']['grammar'] if g['id']==gid).update(form_ko=None),
          'reader':lambda d:d['metadata'].update(min_reader_version=4),
          'task':lambda d:next(q for q in d['tables']['questions'] if q['id']==qid).update(rubric_json='{"grammar_task":"unknown"}'),
          'relation':lambda d:d['tables']['content_links'].append(dict(source_id=gid,target_id='00000000-0000-4000-8000-000000000000',relation='contrast_grammar')),
          'examples':lambda d:d['tables'].update(grammar_examples=[x for x in d['tables']['grammar_examples'] if x['grammar_id']!=gid]),
        }
        for name,fn in changes.items():
            with self.subTest(name=name):
                data=copy.deepcopy(self.source);fn(data);source=self.folder/(name+'.json');source.write_text(json.dumps(data,ensure_ascii=False))
                with self.assertRaises(ValidationError):build(source,self.folder/'rejected.sqlite',production=True)
    def test_duplicate_expression_is_review_candidate_not_deleted(self):
        data=copy.deepcopy(self.source);data['tables']['grammar'][1]['pattern']=data['tables']['grammar'][0]['pattern']
        path=self.folder/'duplicate.json';path.write_text(json.dumps(data,ensure_ascii=False))
        report=build(path,self.folder/'duplicate.sqlite',production=True)
        self.assertTrue(any(w['code']=='duplicate_grammar_candidate' for w in report['validation']['warnings']))
    def test_migration_v6_is_additive_and_user_content_replacement_independent(self):
        user=sqlite3.connect(':memory:')
        for name in ['user-schema-v1']+[f'user-migration-v{i}' for i in range(2,6)]:user.executescript((ROOT/f'Resources/{name}.sql').read_text())
        user.execute("INSERT INTO srs_state VALUES('old','vocabulary','calendar_steps',1,'{\"stage\":4}',99,NULL,10)")
        user.execute("INSERT INTO favorites VALUES('old',10)");user.commit()
        old_srs=user.execute('SELECT * FROM srs_state').fetchall()
        user.executescript((ROOT/'Resources/user-migration-v6.sql').read_text())
        self.assertEqual(user.execute('PRAGMA user_version').fetchone()[0],6)
        self.assertEqual(user.execute('SELECT * FROM srs_state').fetchall(),old_srs)
        self.assertEqual(user.execute('SELECT * FROM favorites').fetchall(),[('old',10)])
        for table in ['grammar_sessions','grammar_review_questions','srs_state']:
            self.assertNotIn('content_items',[r[2] for r in user.execute('PRAGMA foreign_key_list('+table+')')])
        user.close()
    def test_actual_grammar_srs_enrollment_due_and_reenrollment_preserve_state(self):
        user=self.user();insert=self.query('INSERT INTO srs_state(',self.usql)
        due=self.query("SELECT content_id FROM srs_state WHERE skill='grammar'",self.usql)
        for n in range(50):user.execute(insert,[f'id-{n:02}','calendar_steps',1,'{"stage":3}',n,0])
        user.execute(insert,['id-00','calendar_steps',1,'{"stage":0}',999,0])
        user.execute("INSERT INTO srs_state VALUES('word','vocabulary','calendar_steps',1,'{}',0,NULL,0)")
        self.assertEqual(user.execute('SELECT state_json,due_at FROM srs_state WHERE content_id=?',['id-00']).fetchone(),('{"stage":3}',0))
        self.assertEqual(len(user.execute(due,['calendar_steps',1,25]).fetchall()),20)
        self.assertNotIn(('word',),user.execute(due,['calendar_steps',1,100]).fetchall())
        self.assertEqual(user.execute(due,['calendar_steps',1,-1]).fetchall(),[])
        self.assertIn('idx_srs_skill_due',str(user.execute('EXPLAIN QUERY PLAN '+due,['calendar_steps',1,25]).fetchall()))
        user.close()
    def test_review_question_choice_snapshot_and_foreign_key_survive_reopen(self):
        path=self.folder/'user-resume.sqlite'
        with sqlite3.connect(path) as user:
            for name in ['user-schema-v1']+[f'user-migration-v{i}' for i in range(2,7)]:user.executescript((ROOT/f'Resources/{name}.sql').read_text())
            user.execute('PRAGMA foreign_keys=ON')
            user.execute("INSERT INTO review_sessions VALUES('session','grammar','active',1,1,NULL)")
            user.execute("INSERT INTO review_items(session_id,content_id,ordinal) VALUES('session','grammar',0)")
            insert=self.query('INSERT INTO grammar_review_questions(',self.usql)
            user.execute(insert,['session','grammar','{"id":"stable-question"}'])
            user.execute(self.query('UPDATE grammar_review_questions SET',self.usql),['choice-b',0,'session','grammar'])
            user.execute(insert,['session','grammar','{"id":"replacement-question"}'])
        with sqlite3.connect(path) as cold:
            self.assertEqual(cold.execute('SELECT question_json,selected_choice,correct FROM grammar_review_questions').fetchone(),('{"id":"stable-question"}','choice-b',0))
            cold.execute('PRAGMA foreign_keys=ON')
            with self.assertRaises(sqlite3.IntegrityError):cold.execute(insert,['absent','grammar','{}'])
    def test_all_new_repository_sql_prepares(self):
        with self.user() as user:
            for queries,db in [(self.usql,user),(self.csql,self.db)]:
                for sql in queries:
                    if sql.strip().split(' ')[0] in ['SELECT','INSERT','UPDATE','DELETE']:
                        with self.subTest(sql=sql):db.execute('EXPLAIN '+sql,[None]*sql.count('?')).fetchall()

if __name__=='__main__':unittest.main()
