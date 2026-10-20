"""DATA-03 actual SQLite release/integration gates. Native execution is separate."""
import collections
import json
import re
import shutil
import sqlite3
import tempfile
import unittest
import uuid
from pathlib import Path
from build_content import ROOT, build
from validator import signatures


class Data03ContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.candidate = Path(cls.temp.name) / 'content.sqlite'
        cls.report = build(ROOT/'Content/production.json', cls.candidate,
                           previous=ROOT/'Tests/Fixtures/content-v6-production.sqlite', production=True)
        cls.db = sqlite3.connect(cls.candidate)
        cls.registry = json.loads((ROOT/'Content/data03-ids.json').read_text())
        cls.words = {v['headword']: v for v in cls.registry['vocabulary']}
        source = (ROOT/'Repositories/SQLiteContentRepository.swift').read_text()
        cls.base = re.findall(r'"""(.*?)"""', source, re.S)[0]
        cls.parts = re.findall(r'sql \+= "([^"]+)"', source)

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        cls.temp.cleanup()

    def clause(self, start):
        return next(q for q in self.parts if q.startswith(start))

    def test_v6_payloads_ids_revisions_relationships_and_sort_keys_unchanged(self):
        with sqlite3.connect(ROOT/'Tests/Fixtures/content-v6-production.sqlite') as old:
            before, after = signatures(old), signatures(self.db)
            self.assertEqual(len(before), 2288)
            self.assertEqual(len(after), 15935)
            self.assertTrue(all(after[id] == digest for id, digest in before.items() if id not in (json.loads((ROOT/"Content/dev08-revised-ids.json").read_text()) + json.loads((ROOT/"Content/dev09-revised-ids.json").read_text()) + json.loads((ROOT/"Content/data04-revised-ids.json").read_text()) + json.loads((ROOT/"Content/data05-revised-ids.json").read_text()) + json.loads((ROOT/"Content/data06-revised-ids.json").read_text()) + json.loads((ROOT/"Content/data07-revised-ids.json").read_text()) + json.loads((ROOT/"Content/data08-a-revised-ids.json").read_text()) + json.loads((ROOT/"Content/data08-b-revised-ids.json").read_text()) + json.loads((ROOT/"Content/data08-c-revised-ids.json").read_text()) + json.loads((ROOT/'Content/data09-a-revised-ids.json').read_text()) + json.loads((ROOT/'Content/data09-b-revised-ids.json').read_text()) + json.loads((ROOT/'Content/data09-c-revised-ids.json').read_text()) + json.loads((ROOT/"Content/data08-integration-revised-ids.json").read_text()))))
            for table in ['content_items', 'vocabulary', 'meanings', 'examples']:
                for row in old.execute('SELECT * FROM '+table):
                    if table=='content_items' and row[0] in (json.loads((ROOT/'Content/dev08-revised-ids.json').read_text()) + json.loads((ROOT/'Content/dev09-revised-ids.json').read_text()) + json.loads((ROOT/'Content/data04-revised-ids.json').read_text()) + json.loads((ROOT/'Content/data05-revised-ids.json').read_text()) + json.loads((ROOT/'Content/data06-revised-ids.json').read_text()) + json.loads((ROOT/'Content/data07-revised-ids.json').read_text()) + json.loads((ROOT/'Content/data08-a-revised-ids.json').read_text()) + json.loads((ROOT/'Content/data08-b-revised-ids.json').read_text()) + json.loads((ROOT/'Content/data08-c-revised-ids.json').read_text()) + json.loads((ROOT/'Content/data09-a-revised-ids.json').read_text()) + json.loads((ROOT/'Content/data09-b-revised-ids.json').read_text()) + json.loads((ROOT/'Content/data09-c-revised-ids.json').read_text()) + json.loads((ROOT/'Content/data08-integration-revised-ids.json').read_text())):
                        current=self.db.execute('SELECT * FROM content_items WHERE id=?',[row[0]]).fetchone()
                        self.assertEqual(current[2],row[2]+sum(row[0] in json.loads((ROOT/f'Content/dev{v}-revised-ids.json').read_text()) for v in ['08','09'])+int(row[0] in json.loads((ROOT/'Content/data04-revised-ids.json').read_text()))+int(row[0] in json.loads((ROOT/'Content/data05-revised-ids.json').read_text()))+int(row[0] in json.loads((ROOT/'Content/data06-revised-ids.json').read_text()))+int(row[0] in json.loads((ROOT/'Content/data07-revised-ids.json').read_text()))+int(row[0] in json.loads((ROOT/'Content/data08-a-revised-ids.json').read_text()))+int(row[0] in json.loads((ROOT/'Content/data08-b-revised-ids.json').read_text()))+int(row[0] in json.loads((ROOT/'Content/data08-c-revised-ids.json').read_text()))+int(row[0] in json.loads((ROOT/'Content/data08-integration-revised-ids.json').read_text()))+int(row[0] in json.loads((ROOT/'Content/data09-a-revised-ids.json').read_text()))+int(row[0] in json.loads((ROOT/'Content/data09-b-revised-ids.json').read_text()))+int(row[0] in json.loads((ROOT/'Content/data09-c-revised-ids.json').read_text())))
                        self.assertEqual(current[:2]+current[3:-1],row[:2]+row[3:-1])
                        continue
                    self.assertEqual(self.db.execute('SELECT * FROM '+table+' WHERE id=?', [row[0]]).fetchone(), row)
        self.assertEqual(self.db.execute('SELECT schema_version,content_version,min_reader_version,is_fixture FROM content_metadata').fetchone(), (4,23,7,0))
        with sqlite3.connect(ROOT/'Resources/content.sqlite') as bundle:
            self.assertEqual(signatures(bundle), signatures(self.db))

    def test_every_new_uuid_sense_example_and_note_is_in_production(self):
        self.assertEqual(len(self.words), 250)
        self.assertEqual(len(self.registry['examples']), 500)
        self.assertEqual(len(self.registry['notes']), 48)
        senses = 0
        for v in self.registry['vocabulary']:
            self.assertEqual(str(uuid.UUID(v['id'])), v['id'])
            row = self.db.execute('SELECT headword,part_of_speech FROM vocabulary WHERE id=?', [v['id']]).fetchone()
            self.assertEqual(row, (v['headword'],v['part_of_speech']))
            mids = [r[0] for r in self.db.execute('SELECT id FROM meanings WHERE vocabulary_id=? ORDER BY ordinal', [v['id']])]
            self.assertEqual(mids, v['meaning_ids']); senses += len(mids)
            eids = []
            for mid in mids:
                rows = self.db.execute('SELECT e.id,e.korean,e.japanese FROM vocabulary_examples ve JOIN examples e ON e.id=ve.example_id WHERE ve.meaning_id=?', [mid]).fetchall()
                self.assertGreaterEqual(len(rows), 1)
                self.assertTrue(all(ko.strip() and ja.strip() for _,ko,ja in rows))
                eids.extend(r[0] for r in rows)
            self.assertEqual(set(eids), set(v['example_ids']))
        self.assertEqual(senses, 268)
        for id in self.registry['notes']:
            self.assertIsNotNone(self.db.execute('SELECT id FROM learner_notes WHERE id=?', [id]).fetchone())
        self.assertEqual(self.db.execute('PRAGMA foreign_key_check').fetchall(), [])

    def test_level_keyset_and_editorial_order_append_without_old_reordering(self):
        with sqlite3.connect(ROOT/'Tests/Fixtures/content-v6-production.sqlite') as old:
            for level,total,old_count in [('intro',306,296),('beginner',800,180)]:
                seen=[]; cursor=None
                while True:
                    sql=self.base+self.clause(' AND i.level=');args=[level]
                    if cursor:
                        sql+=self.clause(' AND (v.sort_key>');args += [cursor[0],cursor[0],cursor[1]]
                    rows=self.db.execute(sql+self.clause(' ORDER BY'),args+[20]).fetchall()
                    if not rows: break
                    self.assertLessEqual(len(rows),20);seen.extend(r[0] for r in rows)
                    cursor=(rows[-1][3],rows[-1][0])
                self.assertEqual(len(seen),total);self.assertEqual(len(set(seen)),total)
                previous=[r[0] for r in old.execute('SELECT v.id FROM vocabulary v JOIN content_items i ON i.id=v.id WHERE i.level=? ORDER BY v.sort_key,v.id',[level])]
                self.assertEqual(seen[:old_count],previous)
                priorities=[self.db.execute('SELECT learning_priority FROM vocabulary WHERE id=?',[id]).fetchone()[0] for id in seen[old_count:]]
                self.assertEqual(priorities,sorted(priorities))
                new_sets=[seen[n:n+20] for n in range(old_count,len(seen),20)]
                self.assertTrue(all(0 < len(s) <= 20 for s in new_sets))
        self.assertEqual(collections.Counter(v['part_of_speech'] for v in self.words.values()), dict(verb=109,adjective=51,adverb=30,noun=52,bound_noun=8))
        self.assertEqual(collections.Counter(v['level'] for v in self.words.values()),dict(intro=10,beginner=240))
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM vocabulary WHERE learning_priority IS NOT NULL').fetchone()[0],1811)

    def test_actual_prefix_search_secondary_sense_and_intentional_homograph(self):
        sql=self.base+self.clause(' AND v.id IN')+self.clause(' ORDER BY')
        for prefix,word in [('걸리','걸리다'),('病気','걸리다'),('書き留める','적다'),('うらやましい','부럽다'),('意図','뜻')]:
            self.assertIn(word,[r[1] for r in self.db.execute(sql,[prefix,prefix+chr(0x10ffff),50])])
        self.assertEqual(self.db.execute("SELECT part_of_speech FROM vocabulary WHERE headword='적다' ORDER BY part_of_speech").fetchall(),[('adjective',),('verb',)])
        warnings=self.report['validation']['warnings']
        self.assertEqual(self.report['validation']['error_count'],0)
        self.assertEqual(collections.Counter(w['code'] for w in warnings),dict(short_sentence=5,duplicate_headword_candidate=5))
        self.assertEqual(self.db.execute('SELECT korean,japanese FROM examples GROUP BY korean,japanese HAVING COUNT(*)>1').fetchall(),[])

    def test_polysemy_irregulars_and_typed_relations(self):
        for word in ['걸리다','부드럽다','꿈','뜻','힘','혹시']:
            self.assertEqual(len(self.words[word]['meaning_ids']),2)
        for word,value in [('묻다','d'),('믿다','none'),('눕다','b'),('누르다','reu'),('오르다','reu'),('머무르다','reu'),('즐겁다','b'),('늘다','none'),('맞다','none')]:
            self.assertEqual(self.db.execute('SELECT irregular_type FROM vocabulary WHERE id=?',[self.words[word]['id']]).fetchone()[0],value)
        self.assertEqual(len(self.registry['relationships']),15)
        for r in self.registry['relationships']:
            self.assertIsNotNone(self.db.execute('SELECT 1 FROM content_links WHERE source_id=? AND target_id=? AND relation=?',[r['source_id'],r['target_id'],r['relation']]).fetchone())
            for id in [r['source_id'],r['target_id']]:self.assertIsNotNone(self.db.execute('SELECT 1 FROM vocabulary WHERE id=?',[id]).fetchone())
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM vocabulary WHERE reading IS NOT NULL OR topik_level IS NOT NULL OR frequency_rank IS NOT NULL').fetchone()[0],0)

    def test_v6_content_replacement_preserves_both_batches_pass_and_srs_and_new_due(self):
        folder=Path(self.temp.name)/'upgrade';folder.mkdir()
        content_path=folder/'content.sqlite'
        shutil.copyfile(ROOT/'Tests/Fixtures/content-v6-production.sqlite',content_path)
        with sqlite3.connect(content_path) as old:
            ids=[old.execute('SELECT v.id FROM vocabulary v JOIN content_items i ON i.id=v.id WHERE i.level=? ORDER BY v.sort_key,v.id LIMIT 1',[level]).fetchone()[0] for level in ['intro','beginner']]
        user_path=folder/'user.sqlite'
        sqls=re.findall(r'"([^"\n]+)"',(ROOT/'Repositories/SQLiteReviewProgress.swift').read_text())
        enroll=next(q for q in sqls if q.startswith('INSERT INTO srs_state('))
        due=next(q for q in sqls if q.startswith('SELECT content_id FROM srs_state WHERE'))
        with sqlite3.connect(user_path) as user:
            for name in ['user-schema-v1','user-migration-v2','user-migration-v3','user-migration-v4','user-migration-v5']:
                user.executescript((ROOT/f'Resources/{name}.sql').read_text())
            for n,id in enumerate(ids):
                key=f'old-{n}';level=['intro','beginner'][n]
                user.execute('INSERT INTO vocabulary_sets VALUES(?,?,1,1,0)',[key,level])
                user.execute('INSERT INTO vocabulary_set_items VALUES(?,?,0)',[key,id])
                user.execute('INSERT INTO vocabulary_sessions VALUES(?,?,?,3,?,123)',[key,key,json.dumps(dict(vocabularyIDs=[id],round=2,position=0,revealed=True)), 'active'])
                user.execute(enroll,[id,'calendar_steps',1,'{"stage":4,"reviewCount":9}',9999,123])
            user.commit();before=list(user.iterdump())
        shutil.copyfile(self.candidate,content_path)
        with sqlite3.connect(user_path) as user,sqlite3.connect(content_path) as content:
            self.assertEqual(list(user.iterdump()),before)
            for id in ids:
                self.assertIsNotNone(content.execute('SELECT 1 FROM vocabulary WHERE id=?',[id]).fetchone())
                user.execute(enroll,[id,'calendar_steps',1,'{"stage":0}',100,123])
                self.assertEqual(user.execute('SELECT state_json,due_at FROM srs_state WHERE content_id=?',[id]).fetchone(),('{"stage":4,"reviewCount":9}',9999))
            new=self.words['걸리다']['id']
            user.execute(enroll,[new,'calendar_steps',1,'{"stage":0}',100,123])
            self.assertEqual(user.execute(due,['calendar_steps',1,100,20]).fetchall(),[(new,)])
            user.commit()
        with sqlite3.connect(user_path) as reopened:
            self.assertEqual(reopened.execute('SELECT COUNT(*) FROM srs_state').fetchone()[0],3)
            self.assertEqual(reopened.execute('SELECT COUNT(*) FROM vocabulary_sessions').fetchone()[0],2)


if __name__=='__main__': unittest.main()
