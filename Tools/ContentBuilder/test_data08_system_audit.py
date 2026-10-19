"""DATA08-7 SQL/contract regressions. Does not execute Swift or iOS SDKs."""
import json
import re
import sqlite3
import tempfile
import unittest
from pathlib import Path
from build_content import ROOT
from test_data05_content import query
from test_lookup_sql import user


def deferral_sql(prefix):
    code=(ROOT/'Repositories/SQLiteReviewProgress.swift').read_text().split('func deferUnavailableReview',1)[1].split('/// Called inside',1)[0]
    return next(q for q in re.findall(r'"([^"\n]+)"',code) if q.startswith(prefix))


def defer(d,session,content,kind='vocabulary',version=19,stamp=100):
    # Real SQL used by the repository; this helper models the transaction, not Swift.
    key='review.deferred.v1.'+session
    previous=d.execute('SELECT value FROM user_metadata WHERE key=?',[key]).fetchone()
    ids=json.loads(previous[0])if previous else []
    if content in ids:return
    ids.append(content)
    items=d.execute('SELECT content_id,result FROM review_items WHERE session_id=? ORDER BY ordinal',[session]).fetchall()
    processed=sum(v is not None for _,v in items)+len(ids)
    with d:
        sql=deferral_sql('INSERT INTO user_metadata(')
        d.execute(sql,[key,json.dumps(ids)])
        d.execute(sql,['review.unavailable.v1.'+kind+'.'+content,str(version)])
        d.execute(deferral_sql('UPDATE review_sessions SET status='),['completed'if processed==len(items)else'active',stamp,stamp if processed==len(items)else None,session])


class Data08SystemAuditTests(unittest.TestCase):
    def test_legacy_active_review_retirement_reproducer_is_real(self):
        # Actual content lookup refuses inactive rows, while the active session keeps its IDs.
        source=sqlite3.connect(ROOT/'Resources/content.sqlite');d=sqlite3.connect(':memory:');source.backup(d);source.close()
        wid=d.execute('SELECT id FROM vocabulary ORDER BY id LIMIT 1').fetchone()[0]
        self.assertIsNotNone(d.execute(query('SQLiteVocabularyContent','SELECT v.headword'),[wid]).fetchone())
        d.execute('UPDATE content_items SET is_active=0 WHERE id=?',[wid])
        self.assertIsNone(d.execute(query('SQLiteVocabularyContent','SELECT v.headword'),[wid]).fetchone());d.close()
        old=(ROOT/'Docs/DATA08_SYSTEM_REPRO.json')
        if old.exists():self.assertTrue(json.loads(old.read_text())['baseline_retirement_blocks_without_recovery'])

    def test_defer_keeps_srs_events_membership_and_cold_cursor_for_both_skills_and_practice(self):
        for stored in ('vocabulary','grammar','vocabulary_practice','grammar_practice'):
            with self.subTest(skill=stored),tempfile.TemporaryDirectory()as tmp:
                path=Path(tmp)/'u.sqlite';d=user(path,10);kind=stored.removesuffix('_practice')
                d.execute(query('SQLiteReviewProgress',"INSERT INTO user_metadata(key,value) VALUES('review.content-version.v1'"),['19'])
                d.execute('INSERT INTO review_sessions VALUES(?,?,\'active\',1,1,NULL)',['s',stored])
                for i,w in enumerate(('missing','keep')):
                    d.execute("INSERT INTO review_items(session_id,content_id,ordinal) VALUES('s',?,?)",[w,i])
                    d.execute('INSERT INTO srs_state VALUES(?,?,\'calendar_steps\',1,\'{"stage":4}\',50,10,10)',[w,kind])
                d.execute("INSERT INTO favorites(content_id,created_at) VALUES('missing',1)");d.commit()
                before={t:d.execute('SELECT * FROM '+t).fetchall()for t in ('srs_state','favorites','study_events','item_progress','daily_statistics','review_items')}
                defer(d,'s','missing',kind);defer(d,'s','missing',kind)
                for t,rows in before.items():self.assertEqual(rows,d.execute('SELECT * FROM '+t).fetchall(),t)
                d.close();d=sqlite3.connect(path)
                ids=json.loads(d.execute("SELECT value FROM user_metadata WHERE key='review.deferred.v1.s'").fetchone()[0]);self.assertEqual(ids,['missing'])
                pending=[r[0]for r in d.execute("SELECT content_id FROM review_items WHERE session_id='s' AND result IS NULL ORDER BY ordinal")if r[0]not in ids]
                self.assertEqual(pending,['keep']);self.assertEqual(d.execute('SELECT status FROM review_sessions').fetchone()[0],'active')
                # Rating keep after one deferral must complete, without changing skipped row.
                d.execute("UPDATE review_items SET exposed_at=100,revealed_at=100 WHERE content_id='keep'")
                d.execute(query('SQLiteReviewProgress','UPDATE review_items SET result='),['remembered',100,300,4,4,'UTC','2026-10-19','s','keep'])
                raw=d.execute(query('SQLiteReviewProgress','SELECT COUNT(*) AS n FROM review_items WHERE session_id='),['s']).fetchone()[0]
                self.assertEqual(raw-len(ids),0);self.assertIsNone(d.execute("SELECT result FROM review_items WHERE content_id='missing'").fetchone()[0]);d.close()

    def test_all_deferred_completes_without_counting_learning_or_deleting_any_row(self):
        d=user(version=10);d.execute("INSERT INTO review_sessions VALUES('s','grammar','active',1,1,NULL)")
        for i in range(20):d.execute("INSERT INTO review_items(session_id,content_id,ordinal) VALUES('s',?,?)",[str(i),i])
        d.commit()
        for i in range(20):defer(d,'s',str(i),'grammar')
        self.assertEqual(d.execute('SELECT status,completed_at FROM review_sessions').fetchone(),('completed',100))
        self.assertEqual(d.execute('SELECT COUNT(*),COUNT(result),COUNT(reviewed_at) FROM review_items').fetchone(),(20,0,0))
        self.assertEqual(d.execute('SELECT COUNT(*) FROM study_events').fetchone()[0],0)
        self.assertEqual(d.execute('PRAGMA user_version').fetchone()[0],10);d.close()

    def test_release_scoped_quarantine_cannot_starve_later_due_and_retries_next_version(self):
        d=user(version=10);configure=query('SQLiteReviewProgress',"INSERT INTO user_metadata(key,value) VALUES('review.content-version.v1'")
        d.execute(configure,['19'])
        for kind,repo in [('vocabulary','SQLiteReviewProgress'),('grammar','SQLiteGrammarProgress')]:
            for i in range(45):
                w=f'{kind}-{i:03}'
                d.execute('INSERT INTO srs_state VALUES(?,?,\'calendar_steps\',1,\'{"stage":4}\',50,10,10)',[w,kind])
                if i<25:d.execute('INSERT INTO user_metadata VALUES(?,\'19\')',['review.unavailable.v1.'+kind+'.'+w])
            sql=query(repo,'SELECT content_id FROM srs_state WHERE')
            args=['calendar_steps',1,100]+([20]if kind=='vocabulary'else [])
            rows=d.execute(sql,args).fetchall();self.assertEqual(len(rows),20);self.assertTrue(all(int(w[0][-3:])>=25 for w in rows))
            due=query(repo,'SELECT COUNT(*) AS n FROM srs_state');self.assertEqual(d.execute(due,['calendar_steps',1,100]).fetchone()[0],20)
        before=d.execute('SELECT * FROM srs_state ORDER BY content_id,skill').fetchall()
        d.execute(configure,['20'])
        for repo in ('SQLiteReviewProgress','SQLiteGrammarProgress'):
            self.assertEqual(d.execute(query(repo,'SELECT COUNT(*) AS n FROM srs_state'),['calendar_steps',1,100]).fetchone()[0],45)
        self.assertEqual(d.execute('SELECT * FROM srs_state ORDER BY content_id,skill').fetchall(),before);d.close()

    def test_defer_rolls_back_metadata_if_session_save_fails(self):
        d=user(version=10);d.execute("INSERT INTO review_sessions VALUES('s','vocabulary','active',1,1,NULL)")
        d.execute("INSERT INTO review_items(session_id,content_id,ordinal) VALUES('s','word',0)");d.commit()
        d.execute("CREATE TRIGGER fail_defer BEFORE UPDATE ON review_sessions BEGIN SELECT RAISE(ABORT,'forced failure'); END")
        with self.assertRaises(sqlite3.IntegrityError):defer(d,'s','word')
        self.assertEqual(d.execute('SELECT COUNT(*) FROM user_metadata').fetchone()[0],0)
        self.assertEqual(d.execute('SELECT status FROM review_sessions').fetchone()[0],'active');d.close()

    def test_recovery_guard_and_no_srs_mutation_in_repository_or_error_ui(self):
        code=(ROOT/'Repositories/SQLiteReviewProgress.swift').read_text();section=code.split('func deferUnavailableReview',1)[1].split('/// Called inside',1)[0]
        self.assertIn('session.currentID == contentID',section);self.assertIn('if ids.contains(contentID.rawValue) { return session }',section)
        self.assertNotIn('DELETE ',section);self.assertNotIn('UPDATE srs_state',section);self.assertNotIn('recordInTransaction',section)
        for name in ('ReviewViewModel','GrammarViewModel'):
            text=(ROOT/f'ViewModels/{name}.swift').read_text();self.assertIn('unavailableID == expectedID',text);self.assertIn('configureReviewContentVersion',text)
        for name in ('ReviewSessionView','GrammarReviewView'):
            text=(ROOT/f'Views/{name}.swift').read_text();self.assertIn('この教材を保留して続ける',text);self.assertIn('deferredCount',text)

    def test_production_dictation_period_omission_bug_and_narrow_new_policy(self):
        c=sqlite3.connect(ROOT/'Resources/content.sqlite');rows=c.execute("SELECT q.id,e.korean,q.answer_json FROM questions q JOIN listening_items l ON l.id=q.listening_id JOIN examples e ON e.id=l.source_example_id WHERE json_extract(q.rubric_json,'$.listening_task')='dictation'").fetchall()
        normalize=lambda s:' '.join(s.split())
        def strip(s):return normalize(s).rstrip('.!?').rstrip()
        affected=[]
        for qid,text,answer in rows:
            accepted=json.loads(answer)['accepted'];omitted=strip(text)
            if omitted!=text and omitted not in [normalize(s)for s in accepted]:affected.append(qid)
            self.assertIn(strip(text),[strip(s)for s in accepted])
            self.assertNotIn(strip(text)+'틀린 내용',[strip(s)for s in accepted])
        self.assertGreaterEqual(len(affected),1821)
        # Structural route assertion only: native expectations execute judgeDictation on Mac.
        judge=(ROOT/'LearningEngine/ConjugationEngine.swift').read_text().split('static func judgeDictation',1)[1].split('static func normalize',1)[0]
        self.assertIn('".!?".contains(last)',judge);self.assertIn('text.removeLast()',judge)
        self.assertIn('ProductionAnswer.judgeDictation(answer,accepted:accepted)',(ROOT/'Models/ListeningModels.swift').read_text())
        self.assertIn('自由翻訳の自動採点ではありません',(ROOT/'Views/ProductionView.swift').read_text());c.close()

    def test_listening_inactive_prefix_no_longer_starves_later_active_items(self):
        source=sqlite3.connect(ROOT/'Resources/content.sqlite');content=sqlite3.connect(':memory:');source.backup(content);source.close()
        ids=[r[0]for r in content.execute('SELECT id FROM listening_items ORDER BY id LIMIT 45')]
        content.executemany('UPDATE content_items SET is_active=0 WHERE id=?',[(i,)for i in ids[:25]])
        d=user(version=10);d.execute(query('SQLiteReviewProgress',"INSERT INTO user_metadata(key,value) VALUES('review.content-version.v1'"),['19'])
        for i in ids:d.execute("INSERT INTO srs_state VALUES(?,'listening','calendar_steps',1,'{}',50,NULL,1)",[i])
        d.commit();before=d.execute('SELECT * FROM srs_state').fetchall();pages=0;selected=[]
        while True:
            pending=[r[0]for r in d.execute(query('SQLiteListening',"SELECT content_id FROM srs_state WHERE skill='listening'"),['calendar_steps',1,100])]
            if not pending:break
            pages+=1
            content.row_factory=sqlite3.Row
            rows=content.execute(query('SQLiteListening','SELECT q.*,l.id')+' AND l.id IN ('+','.join('?'for _ in pending)+') ORDER BY l.learning_order,l.id LIMIT 20',pending).fetchall()
            content.row_factory=None;available={r['item_id']for r in rows};missing=[i for i in pending if i not in available]
            for i in missing:d.execute(query('SQLiteListening','INSERT INTO user_metadata('),['review.unavailable.v1.listening.'+i,'19'])
            if rows:selected=[r['item_id']for r in rows];break
        self.assertEqual(pages,2);self.assertEqual(set(selected),set(ids[25:40]))
        self.assertEqual(d.execute('SELECT * FROM srs_state').fetchall(),before)
        self.assertEqual(d.execute(query('SQLiteListening','SELECT COUNT(*) AS n FROM srs_state'),['calendar_steps',1,100]).fetchone()[0],20)
        ui=(ROOT/'Views/ListeningView.swift').read_text();self.assertIn('await Task.yield()',ui);self.assertIn('deferUnavailableListening(ids:missing',ui)
        self.assertLess(ui.index('activeListening(scope:scope)'),ui.index('listeningDue(now:Date()).1'))
        d.close();content.close()

    def test_monetization_storage_is_independent_of_content_and_user_metadata(self):
        purchase=(ROOT/'Services/PurchaseService.swift').read_text();ads=(ROOT/'Services/AdService.swift').read_text();config=(ROOT/'Models/MonetizationPolicy.swift').read_text()
        for text in (purchase,ads,config):
            for forbidden in ('contentVersion','content_version','review.content-version','user_metadata','ContentPackageValidator'):
                self.assertNotIn(forbidden,text)
        self.assertIn('HangulStudy.purchase.release.v1',purchase);self.assertIn('HangulStudy.purchase.debug.v1',purchase)
        self.assertIn('monetization.frequency.v1',ads);self.assertIn('static let productID = "remove_ads"',config)
        self.assertIn('requestGeneration == generation',ads);self.assertIn('purchases.state.permitsAds',ads)

    def test_entitlement_and_frequency_sample_bytes_are_untouched_by_content_and_defer(self):
        # Synthetic opaque cache boundary only, not a Keychain/StoreKit verification.
        with tempfile.TemporaryDirectory()as tmp:
            path=Path(tmp)/'cache.json';data=json.dumps({'productID':'remove_ads','transactionID':42,'purchaseDate':100,'frequency':{'completedItems':40,'lastPresentation':10}}).encode();path.write_bytes(data)
            d=user(version=10);d.execute("INSERT INTO review_sessions VALUES('s','vocabulary','active',1,1,NULL)");d.execute("INSERT INTO review_items(session_id,content_id,ordinal) VALUES('s','missing',0)");d.commit()
            for version in (18,19,20):
                d.execute(query('SQLiteReviewProgress',"INSERT INTO user_metadata(key,value) VALUES('review.content-version.v1'"),[str(version)])
                self.assertEqual(path.read_bytes(),data)
            defer(d,'s','missing',version=20);self.assertEqual(path.read_bytes(),data);d.close()
