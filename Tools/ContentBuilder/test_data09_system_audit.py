"""DATA09-7 actual SQLite regressions and explicit Swift source contracts.
No Swift engine, Codable, UI, StoreKit or device execution is claimed here.
"""
import json
import re
import sqlite3
import tempfile
import unittest
from pathlib import Path
from build_content import ROOT
from test_data05_content import query
from test_lookup_sql import user


def answer_sql(prefix):
    code = (ROOT/'Repositories/SQLiteGrammarProgress.swift').read_text().split('func answerGrammarReview', 1)[1]
    return next(q for q in re.findall(r'"([^"\n]+)"', code) if q.startswith(prefix))


class Data09SystemAuditTests(unittest.TestCase):
    def test_all_grammar_questions_have_one_target_one_answer_and_real_examples(self):
        with sqlite3.connect(ROOT/'Resources/content.sqlite') as c:
            count = 0
            for (gid,) in c.execute('SELECT id FROM grammar'):
                examples = c.execute(query('SQLiteGrammarContent','SELECT e.id,e.korean'), [gid]).fetchall()
                self.assertTrue(examples)
                self.assertTrue(all(c.execute('SELECT 1 FROM grammar_examples WHERE grammar_id=? AND example_id=?', [gid,r[0]]).fetchone() for r in examples))
                for q in c.execute(query('SQLiteGrammarContent','SELECT q.*,i.revision'), [gid]):
                    qid = q[0]
                    targets = c.execute("SELECT target_id FROM content_links WHERE source_id=? AND relation='question_target'", [qid]).fetchall()
                    self.assertEqual(targets, [(gid,)])
                    answer = json.loads(c.execute('SELECT answer_json FROM questions WHERE id=?',[qid]).fetchone()[0])['correct_choice_ids']
                    choices = c.execute(query('SQLiteGrammarContent','SELECT choice_id,text'),[qid]).fetchall()
                    self.assertEqual(len(answer),1)
                    self.assertEqual(sum(i == answer[0] for i,_ in choices),1)
                    self.assertEqual(len({t for _,t in choices}),len(choices))
                    count += 1
            self.assertEqual(count,300)

    def test_grammar_review_question_snapshot_and_wrong_choice_survive_new_content_and_reopen(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'user.sqlite'; d = user(path,10)
            d.execute("INSERT INTO review_sessions VALUES('s','grammar','active',1,1,NULL)")
            d.execute("INSERT INTO review_items(session_id,content_id,ordinal,exposed_at) VALUES('s','g',0,1)")
            original = json.dumps(dict(id='old-question',revision=1,choices=[dict(id='right',text='맞아요'),dict(id='wrong',text='틀려요')],correctID='right'))
            insert = query('SQLiteGrammarProgress','INSERT INTO grammar_review_questions(')
            d.execute(insert,['s','g',original])
            d.execute(answer_sql('UPDATE grammar_review_questions SET'),['wrong',0,'s','g'])
            d.execute(answer_sql('UPDATE review_items SET revealed_at='),[10,'s','g'])
            d.execute(answer_sql('UPDATE review_sessions SET updated_at='),[10,'s'])
            d.commit(); d.close()
            d = sqlite3.connect(path)
            d.execute(insert,['s','g','{"id":"new-question","correctID":"wrong"}'])
            self.assertEqual(d.execute('SELECT question_json,selected_choice,correct FROM grammar_review_questions').fetchone(),(original,'wrong',0))
            self.assertEqual(d.execute(query('SQLiteReviewProgress',"SELECT 1 FROM grammar_review_questions WHERE session_id=? AND content_id=? AND correct=1"),['s','g']).fetchall(),[])
            self.assertEqual(d.execute(query('SQLiteCurriculum','SELECT kind,target,level FROM')).fetchone()[:2],('review','grammar'))
            d.close()

    def test_late_grammar_answer_failure_rolls_back_answer_event_statistics_and_resume(self):
        d = user(version=10)
        d.execute("INSERT INTO review_sessions VALUES('s','grammar','active',1,1,NULL)")
        d.execute("INSERT INTO review_items(session_id,content_id,ordinal,exposed_at) VALUES('s','g',0,1)")
        d.execute(query('SQLiteGrammarProgress','INSERT INTO grammar_review_questions('),['s','g','{"id":"q"}'])
        d.commit()
        tables = ['review_sessions','review_items','grammar_review_questions','study_events','item_progress','daily_statistics']
        before = {t:d.execute('SELECT * FROM '+t).fetchall() for t in tables}
        d.execute("CREATE TRIGGER fail_answer BEFORE UPDATE ON review_sessions BEGIN SELECT RAISE(ABORT,'late save failure'); END")
        with self.assertRaisesRegex(sqlite3.IntegrityError,'late save failure'),d:
            d.execute(answer_sql('UPDATE grammar_review_questions SET'),['right',1,'s','g'])
            d.execute(query('SQLiteProgressRepository','INSERT INTO study_events'),['event','g',1,10,'2026-10-20','UTC','grammar_quiz_review','correct',0,'s',24])
            d.execute(query('SQLiteProgressRepository','INSERT INTO item_progress'),['g',10,10,1,1,0])
            d.execute(query('SQLiteProgressRepository','INSERT INTO daily_statistics'),['2026-10-20','UTC',1,1,0,0])
            d.execute(answer_sql('UPDATE review_items SET revealed_at='),[10,'s','g'])
            d.execute(answer_sql('UPDATE review_sessions SET updated_at='),[10,'s'])
        for t in tables:self.assertEqual(d.execute('SELECT * FROM '+t).fetchall(),before[t],t)
        d.close()

    def test_native_gates_cover_stale_action_wrong_answer_and_no_double_completion(self):
        # Source contract only; native tests below must execute on a Mac to verify semantics.
        engine=(ROOT/'LearningEngine/GrammarLearning.swift').read_text()
        repo=(ROOT/'Repositories/SQLiteGrammarProgress.swift').read_text()
        review=(ROOT/'Repositories/SQLiteReviewProgress.swift').read_text()
        self.assertIn('guard !original.completed',engine)
        self.assertIn('s.page == 3, s.selected == nil',engine)
        self.assertIn('guard s.page == 4',engine)
        self.assertIn('guard before.revision == revision',repo)
        self.assertIn('if current.selected != nil { return current }',repo)
        self.assertIn('ON CONFLICT(content_id,skill) DO NOTHING',repo)
        self.assertIn('session.currentID == contentID, session.exposed',repo)
        self.assertIn('session.currentID == contentID, session.revealed',review)
        self.assertIn('AND correct=1',review)
        tests=(ROOT/'Tests/GrammarLearningTests.swift').read_text()
        self.assertIn('testDATA09All18LessonsQuizSRSAndResume',tests)
        self.assertIn('testGrammarWrongReviewRetryAndStalePassCannotDuplicateProgress',tests)

    def test_grammar_quiz_event_ids_are_idempotent_in_real_statistics_sql(self):
        d=user(version=10)
        args=['same-event','g',1,10,'2026-10-20','UTC','grammar_quiz_review','incorrect',0,'s',24]
        insert=query('SQLiteProgressRepository','INSERT INTO study_events')
        with d:
            d.execute(insert,args)
            d.execute(query('SQLiteProgressRepository','INSERT INTO item_progress'),['g',10,10,1,0,1])
            d.execute(query('SQLiteProgressRepository','INSERT INTO daily_statistics'),['2026-10-20','UTC',1,0,1,0])
        with self.assertRaises(sqlite3.IntegrityError):d.execute(insert,args)
        self.assertEqual(d.execute(query('SQLiteStatistics','SELECT COUNT(CASE'),[0,20]).fetchone()[:3],(1,0,1))
        self.assertEqual(d.execute('SELECT COUNT(*),SUM(incorrect_count) FROM item_progress').fetchone(),(1,1))
        d.close()

    def test_all_grammar_lessons_have_bounded_unique_members_and_active_parents(self):
        with sqlite3.connect(ROOT/'Resources/content.sqlite') as c:
            seen=[];lessons=[]
            for level in ('intro','beginner','lower_intermediate'):
                after=-1
                while True:
                    page=c.execute(query('SQLiteGrammarContent','SELECT l.id,l.title_ja'),[level,after,7]).fetchall()
                    if not page:break
                    for r in page:
                        ids=[i[0] for i in c.execute(query('SQLiteGrammarContent','SELECT g.id FROM lesson_items'),[r[0]])]
                        self.assertEqual(len(ids),r[3]);self.assertEqual(len(ids),len(set(ids)));self.assertTrue(1<=len(ids)<=20)
                        seen.extend(ids);lessons.append(r[0])
                    after=page[-1][2]
            self.assertEqual(len(lessons),30);self.assertEqual(len(seen),96);self.assertEqual(len(set(seen)),96)
