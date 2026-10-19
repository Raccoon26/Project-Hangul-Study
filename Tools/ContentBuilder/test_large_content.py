import sqlite3, tempfile, unittest
from pathlib import Path
from build_content import build
from generate_synthetic import generate, synthetic_id

class LargeContentTests(unittest.TestCase):
    def test_15000_vocabulary_30000_examples_and_prefix_index(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            result=build(generate(root/'source',15000),root/'synthetic.sqlite')
            self.assertEqual(result['validation']['error_count'],0)
            with sqlite3.connect(result['path']) as db:
                self.assertEqual(db.execute('SELECT COUNT(*) FROM vocabulary').fetchone()[0],15000)
                self.assertEqual(db.execute('SELECT COUNT(*) FROM examples').fetchone()[0],30000)
                self.assertEqual(db.execute('SELECT COUNT(*) FROM vocabulary_examples').fetchone()[0],30000)
                self.assertEqual(db.execute('PRAGMA foreign_key_check').fetchall(),[])
                word=synthetic_id('vocabulary',14999)
                self.assertEqual(db.execute('SELECT COUNT(*) FROM vocabulary_examples ve JOIN meanings m ON m.id=ve.meaning_id WHERE m.vocabulary_id=?',(word,)).fetchone()[0],2)
                rows=db.execute('SELECT vocabulary_id FROM vocabulary_search WHERE term>=? AND term<?',['__synthetic__意味014999','__synthetic__意味014999'+chr(0x10ffff)]).fetchall()
                self.assertEqual(rows,[(word,)])
                self.assertEqual(db.execute('SELECT is_fixture FROM content_metadata').fetchone()[0],1)
if __name__=='__main__': unittest.main()
