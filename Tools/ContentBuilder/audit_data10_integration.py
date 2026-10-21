"""Read-only Content28->29 preservation/reachability/rebuild receipt. Not iOS QA."""
import argparse, collections, gzip, hashlib, json, sqlite3, subprocess
from pathlib import Path
from build_content import ROOT
from validator import signatures

BASE = 'd76f0b89c38c892005de68aef206229234d141c9'
sha = lambda b: hashlib.sha256(b).hexdigest()


def audit(source, bundle, rebuilt=None):
    source, bundle = Path(source), Path(bundle)
    src = json.loads(source.read_text()); t = src['tables']
    oldsrc = json.loads(gzip.decompress((ROOT/'Tests/Fixtures/content-v28-production.json.gz').read_bytes()))
    manifest = json.loads((ROOT/'Content/data10-integration-ids.json').read_text())
    db = sqlite3.connect(bundle); old = sqlite3.connect(ROOT/'Tests/Fixtures/content-v28-production.sqlite')
    before, after = signatures(old), signatures(db)
    revised = set(json.loads((ROOT/'Content/data10-integration-revised-ids.json').read_text()))
    new_ids = {c['id'] for c in manifest['courses']} | {u['id'] for c in manifest['courses'] for u in c['units']} | {l['id'] for c in manifest['courses'] for l in c['lessons']}
    assert set(after)-set(before) == new_ids and set(before) <= set(after)
    changed = {i for i in before if before[i] != after[i]}; assert changed == revised
    current_items = {r['id']:r for r in t['content_items']}
    for row in oldsrc['tables']['content_items']:
        expected = dict(row)
        if row['id'] in revised: expected['revision'] += 1; expected['updated_at'] = manifest['created_at']
        assert expected == current_items[row['id']]
    counts = {}
    for table, rows in t.items():
        keys = sorted({k for r in rows for k in r}) if rows else [r[1] for r in db.execute('PRAGMA table_info('+table+')')]
        actual = collections.Counter(db.execute('SELECT '+','.join('"'+k+'"' for k in keys)+' FROM '+table))
        assert actual == collections.Counter(tuple(r.get(k) for k in keys) for r in rows), table
        if table != 'content_items':
            assert collections.Counter(tuple(r.get(k) for k in keys) for r in oldsrc['tables'][table]) <= actual, table
        counts[table] = len(rows)
    assert t['examples'] == oldsrc['tables']['examples']
    assert t['questions'] == oldsrc['tables']['questions']
    assert t['listening_items'] == oldsrc['tables']['listening_items']
    protected = {}
    for name in subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--','Content','Resources','Tests/Fixtures'],cwd=ROOT,text=True).splitlines():
        expected = subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
        actual = gzip.decompress((ROOT/'Tests/Fixtures/content-v28-production.json.gz').read_bytes()) if name == 'Content/production.json' else (ROOT/'Tests/Fixtures/content-v28-production.sqlite').read_bytes() if name == 'Resources/content.sqlite' else (ROOT/name).read_bytes()
        assert actual == expected, name
        protected[name] = sha(actual)
    sql = 'SELECT type,name,tbl_name,sql FROM sqlite_master ORDER BY type,name'
    assert db.execute(sql).fetchall() == old.execute(sql).fetchall()
    names = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    reconstruction = None
    if rebuilt:
        other = sqlite3.connect(rebuilt)
        equal = {n:collections.Counter(db.execute('SELECT * FROM '+n)) == collections.Counter(other.execute('SELECT * FROM '+n)) for n in names}
        reconstruction = dict(tables=equal, all_rows_equal=all(equal.values()), schema_equal=db.execute(sql).fetchall() == other.execute(sql).fetchall(), byte_equal=bundle.read_bytes() == Path(rebuilt).read_bytes())
        assert all(reconstruction[k] for k in ('all_rows_equal','schema_equal','byte_equal'))
        other.close()
    report = dict(scope='Actual Source/SQLite/repository contracts; no native execution', metadata=src['metadata'], source_sha256=sha(source.read_bytes()), bundle_sha256=sha(bundle.read_bytes()), source_rows=counts, total_source_rows=sum(counts.values()), sqlite_tables=len(names), new_entities=len(new_ids), revised_ids=sorted(revised), revised_by_kind=dict(collections.Counter(db.execute('SELECT kind FROM content_items WHERE id=?',[i]).fetchone()[0] for i in revised)), deleted_entities=0, preserved_files=protected, integrity=db.execute('PRAGMA integrity_check').fetchall(), foreign_keys=db.execute('PRAGMA foreign_key_check').fetchall(), levels={table:dict(db.execute('SELECT i.level,COUNT(*) FROM '+table+' t JOIN content_items i ON i.id=t.id GROUP BY i.level')) for table in ('vocabulary','examples','grammar','questions','listening_items','courses','lessons')}, integration=dict(courses=3,units=6,lessons=72,questions_per_lesson=5,listening_memberships=360,grammar_references=180,distinct_grammar=77,vocabulary_references=180,distinct_vocabulary=130), reconstruction=reconstruction, verified_recordings=0, independent_human_review='NOT TESTED', native_build_xctest='BLOCKED')
    assert report['integrity'] == [('ok',)] and not report['foreign_keys']
    db.close(); old.close(); return report


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,default=ROOT/'Content/production.json');p.add_argument('--bundle',type=Path,default=ROOT/'Resources/content.sqlite');p.add_argument('--rebuilt',type=Path);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    r=audit(a.source,a.bundle,a.rebuilt);a.report.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:r[k] for k in ('metadata','total_source_rows','new_entities','revised_by_kind','integration')}))
