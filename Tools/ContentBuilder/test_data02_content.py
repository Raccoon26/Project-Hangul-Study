"""DATA-02 release gates. Actual repository SQL; Swift flow execution requires Xcode."""
import collections
import json
import re
import shutil
import sqlite3
import tempfile
import unittest
from pathlib import Path
from build_content import ROOT, build
from validator import signatures


class Data02ContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.path = Path(cls.temp.name) / 'candidate.sqlite'
        cls.report = build(ROOT/'Content/production.json', cls.path,
                           previous=ROOT/'Tests/Fixtures/content-v5-production.sqlite', production=True)
        cls.db = sqlite3.connect(cls.path)
        cls.registry = json.loads((ROOT/'Content/data02-ids.json').read_text())
        cls.swift = (ROOT/'Repositories/SQLiteContentRepository.swift').read_text()
        cls.base = re.findall(r'"""(.*?)"""', cls.swift, re.S)[0]
        cls.parts = re.findall(r'sql \+= "([^"]+)"', cls.swift)
    @classmethod
    def tearDownClass(cls):
        cls.db.close(); cls.temp.cleanup()
    def part(self, prefix):
        return next(p for p in self.parts if p.startswith(prefix))
    def test_release_counts_and_no_existing_payload_or_relationship_changed(self):
        with sqlite3.connect(ROOT/'Tests/Fixtures/content-v5-production.sqlite') as old:
            before, after = signatures(old), signatures(self.db)
            self.assertEqual(len(before), 1220)
            self.assertTrue(all(after[k] == v for k, v in before.items() if k not in (json.loads((ROOT/"Content/dev08-revised-ids.json").read_text()) + json.loads((ROOT/"Content/dev09-revised-ids.json").read_text()) + json.loads((ROOT/"Content/data04-revised-ids.json").read_text()) + json.loads((ROOT/"Content/data05-revised-ids.json").read_text()) + json.loads((ROOT/"Content/data06-revised-ids.json").read_text()) + json.loads((ROOT/"Content/data07-revised-ids.json").read_text()) + json.loads((ROOT/"Content/data08-a-revised-ids.json").read_text()) + json.loads((ROOT/"Content/data08-b-revised-ids.json").read_text()) + json.loads((ROOT/"Content/data08-c-revised-ids.json").read_text()) + json.loads((ROOT/'Content/data09-a-revised-ids.json').read_text()) + json.loads((ROOT/'Content/data09-b-revised-ids.json').read_text()) + json.loads((ROOT/'Content/data09-c-revised-ids.json').read_text()) + json.loads((ROOT/"Content/data08-integration-revised-ids.json").read_text()))))
            self.assertEqual(len(after), 15935)
            for table in ['vocabulary','meanings','examples']:
                for row in old.execute('SELECT * FROM '+table):
                    self.assertEqual(self.db.execute('SELECT * FROM '+table+' WHERE id=?', [row[0]]).fetchone(), row)
        self.assertEqual(self.db.execute('SELECT schema_version,content_version,min_reader_version FROM content_metadata').fetchone(), (4,23,7))
        self.assertEqual(self.report['validation']['error_count'], 0)
    def test_all_new_ids_meanings_examples_notes_are_real_bundle_content(self):
        self.assertEqual(len(self.registry['vocabulary']),250)
        self.assertEqual(len(self.registry['examples']),500)
        self.assertEqual(len(self.registry['notes']),32)
        sense_count=0
        for v in self.registry['vocabulary']:
            row=self.db.execute('SELECT headword,part_of_speech FROM vocabulary WHERE id=?',[v['id']]).fetchone()
            self.assertEqual(row,(v['headword'],v['part_of_speech']))
            meanings=self.db.execute('SELECT id,meaning_ja FROM meanings WHERE vocabulary_id=? ORDER BY ordinal',[v['id']]).fetchall()
            self.assertEqual([m[0] for m in meanings],v['meaning_ids']);sense_count+=len(meanings)
            examples=[]
            for mid,meaning in meanings:
                self.assertTrue(meaning.strip())
                rows=self.db.execute('SELECT e.id,e.korean,e.japanese FROM vocabulary_examples ve JOIN examples e ON e.id=ve.example_id WHERE ve.meaning_id=?',[mid]).fetchall()
                self.assertGreaterEqual(len(rows),1)
                self.assertTrue(all(len(ko)>1 and len(ja)>1 for _,ko,ja in rows))
                examples.extend(r[0] for r in rows)
            self.assertEqual(set(examples),set(v['example_ids']))
            self.assertEqual(len(examples),2)
        self.assertEqual(sense_count,260)
        with sqlite3.connect(ROOT/'Resources/content.sqlite') as bundle:
            self.assertEqual(signatures(bundle),signatures(self.db))
    def test_level_keyset_queries_and_new_pos_balance(self):
        for level,total in [('intro',306),('beginner',800)]:
            seen=[];cursor=None
            while True:
                sql=self.base+self.part(' AND i.level=');args=[level]
                if cursor:sql+=self.part(' AND (v.sort_key>');args += [cursor[0],cursor[0],cursor[1]]
                rows=self.db.execute(sql+self.part(' ORDER BY'),args+[20]).fetchall()
                if not rows:break
                self.assertLessEqual(len(rows),20);seen += [r[0] for r in rows]
                cursor=(rows[-1][3],rows[-1][0])
            self.assertEqual(len(seen),total);self.assertEqual(len(set(seen)),total)
        counts=collections.Counter(v['part_of_speech'] for v in self.registry['vocabulary'])
        self.assertEqual(counts,dict(noun=98,verb=81,adjective=32,adverb=22,pronoun=4,determiner=5,numeral=6,bound_noun=2))
        self.assertEqual(collections.Counter(v['level'] for v in self.registry['vocabulary']),dict(intro=70,beginner=180))
    def test_actual_prefix_search_in_both_languages_and_secondary_senses(self):
        sql=self.base+self.part(' AND v.id IN')+self.part(' ORDER BY')
        for prefix,word in [('洗濯','빨래하다'),('予約する','예약하다'),('髪','머리'),('過ごす','보내다'),('両親','부모님'),('초대','초대하다')]:
            rows=self.db.execute(sql,[prefix,prefix+chr(0x10ffff),50]).fetchall()
            self.assertIn(word,[r[1] for r in rows])
    def test_duplicate_review_and_unique_sentence_pairs(self):
        warnings=self.report['validation']['warnings']
        self.assertEqual(collections.Counter(w['code'] for w in warnings),dict(short_sentence=5,duplicate_headword_candidate=5))
        self.assertEqual(self.db.execute("SELECT part_of_speech FROM vocabulary WHERE headword='저' ORDER BY part_of_speech").fetchall(),[('determiner',),('pronoun',)])
        pairs=self.db.execute('SELECT korean,japanese,COUNT(*) FROM examples GROUP BY korean,japanese HAVING COUNT(*)>1').fetchall()
        self.assertEqual(pairs,[])
    def test_irregulars_and_unknown_metadata_are_not_inferred_ranks(self):
        for word,value in [('가깝다','b'),('굽다','b'),('낫다','s'),('다르다','reu'),('배부르다','reu'),('넣다','none'),('좁다','none'),('늦다','none'),('예약하다','other')]:
            self.assertEqual(self.db.execute('SELECT irregular_type FROM vocabulary WHERE headword=?',[word]).fetchone()[0],value)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM vocabulary WHERE topik_level IS NOT NULL OR frequency_rank IS NOT NULL OR reading IS NOT NULL').fetchone()[0],0)
    def test_v5_progress_and_srs_survive_real_content_replacement_and_new_ids_enroll(self):
        folder=Path(self.temp.name)/'upgrade';folder.mkdir(exist_ok=True)
        content_path=folder/'content.sqlite';shutil.copyfile(ROOT/'Tests/Fixtures/content-v5-production.sqlite',content_path)
        with sqlite3.connect(content_path) as old:
            old_ids=[r[0] for r in old.execute('SELECT id FROM vocabulary ORDER BY sort_key,id LIMIT 20')]
        user_path=folder/'progress.sqlite'
        with sqlite3.connect(user_path) as user:
            for name in ['user-schema-v1','user-migration-v2','user-migration-v3','user-migration-v4','user-migration-v5']:
                user.executescript((ROOT/f'Resources/{name}.sql').read_text())
            user.execute("INSERT INTO vocabulary_sets VALUES('old-set','intro',1,1,0)")
            user.executemany("INSERT INTO vocabulary_set_items VALUES('old-set',?,?)",[(id,n) for n,id in enumerate(old_ids)])
            state=json.dumps(dict(vocabularyIDs=old_ids,round=2,position=12,revealed=True,deferred=old_ids[:3]))
            user.execute("INSERT INTO vocabulary_sessions VALUES('old-session','old-set',?,7,'active',123)",[state])
            sqls=re.findall(r'"([^"\n]+)"',(ROOT/'Repositories/SQLiteReviewProgress.swift').read_text())
            enroll=next(q for q in sqls if q.startswith('INSERT INTO srs_state('))
            user.execute(enroll,[old_ids[0],'calendar_steps',1,'{"stage":4,"reviewCount":9}',9999,123])
            user.execute('INSERT INTO favorites VALUES(?,123)',[old_ids[0]])
            user.commit();before=list(user.iterdump())
        shutil.copyfile(self.path,content_path)
        with sqlite3.connect(user_path) as user, sqlite3.connect(content_path) as content:
            self.assertEqual(list(user.iterdump()),before)
            for id in old_ids:self.assertIsNotNone(content.execute('SELECT headword FROM vocabulary WHERE id=?',[id]).fetchone())
            self.assertEqual(json.loads(user.execute('SELECT state_json FROM vocabulary_sessions').fetchone()[0])['vocabularyIDs'][12],old_ids[12])
            new_id=next(v['id'] for v in self.registry['vocabulary'] if v['level']=='beginner')
            user.execute(enroll,[new_id,'calendar_steps',1,'{"stage":0}',100,123])
            user.execute(enroll,[old_ids[0],'calendar_steps',1,'{"stage":0}',100,123])
            self.assertEqual(user.execute('SELECT state_json,due_at FROM srs_state WHERE content_id=?',[old_ids[0]]).fetchone(),('{"stage":4,"reviewCount":9}',9999))
            due=next(q for q in sqls if q.startswith('SELECT content_id FROM srs_state WHERE'))
            self.assertEqual(user.execute(due,['calendar_steps',1,100,20]).fetchall(),[(new_id,)])
            user.commit()
        with sqlite3.connect(user_path) as reopened:self.assertEqual(reopened.execute('SELECT COUNT(*) FROM srs_state').fetchone()[0],2)

if __name__=='__main__':unittest.main()
