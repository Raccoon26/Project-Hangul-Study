"""DATA-08 closeout evidence: read-only counts, preserved IDs, rebuilt DB and Git sizes.

Run the Importer and system audit first, with their outputs outside the checkout.
This records structural evidence, never native execution or language certification.
"""
import argparse
import collections
import hashlib
import json
import re
import sqlite3
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEVELS = ('hangul', 'intro', 'beginner', 'lower_intermediate', 'intermediate',
          'upper_intermediate', 'advanced', 'master', 'maintenance')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text())


def connect(path):
    return sqlite3.connect(Path(path).resolve().as_uri() + '?mode=ro', uri=True)


def count(db, table):
    return db.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def run(args):
    checks = []

    def check(name, condition):
        checks.append(dict(check=name, status='PASS' if condition else 'FAIL'))

    source = load(ROOT / 'Content/production.json')
    build = load(args.build_report)
    system = load(args.system_audit)
    bundle = ROOT / 'Resources/content.sqlite'
    db, rebuilt = connect(bundle), connect(args.rebuilt)
    table_names = [r[0] for r in db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    same_tables = table_names == [r[0] for r in rebuilt.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    check('Rebuilt table inventory including derived tables', same_tables)
    comparisons = {}
    for table in table_names:
        # ALL columns, duplicate multiplicity and derived sqlite_stat1 are included.
        expected = collections.Counter(db.execute(f'SELECT * FROM "{table}"'))
        actual = collections.Counter(rebuilt.execute(f'SELECT * FROM "{table}"')) if same_tables else {}
        comparisons[table] = dict(rows=sum(expected.values()), equal=expected == actual)
        check('Rebuilt all rows: ' + table, expected == actual)
    check('Rebuilt complete schema/index definitions', list(db.execute(
        'SELECT type,name,tbl_name,sql FROM sqlite_master ORDER BY type,name')) == list(rebuilt.execute(
        'SELECT type,name,tbl_name,sql FROM sqlite_master ORDER BY type,name')))
    check('Rebuilt byte-exact SHA-256', sha(bundle) == sha(args.rebuilt) == build['sha256'])
    check('Strict Validator has no errors', build['validation']['error_count'] == 0)
    check('Existing ten warnings retained', build['validation']['warning_count'] == 10)
    check('Source/bundle and route audit has no structural errors',
          system['structural']['validation']['error_count'] == 0)
    check('No unreachable examples or questions', system['coverage']['unreachable_examples'] == 0
          and system['coverage']['unrouted_questions'] == 0)
    integrity = {}
    for name, con in [('bundle', db), ('rebuilt', rebuilt)]:
        integrity[name] = dict(integrity_check=con.execute('PRAGMA integrity_check').fetchall(),
                               foreign_key_violations=con.execute('PRAGMA foreign_key_check').fetchall())
        check(name + ' integrity and FK', integrity[name] == dict(integrity_check=[('ok',)], foreign_key_violations=[]))

    baseline = connect(ROOT / 'Tests/Fixtures/content-v14-production.sqlite')
    batches, new_words, new_examples = {}, set(), set()
    for batch in ('a', 'b', 'c'):
        registry = load(ROOT / f'Content/data08-{batch}-ids.json')
        words = {w['id'] for w in registry['vocabulary']}
        examples = set(registry['examples'])
        check(batch + ' disjoint new IDs', not new_words.intersection(words) and not new_examples.intersection(examples))
        new_words.update(words)
        new_examples.update(examples)
        pos = collections.Counter(db.execute('SELECT part_of_speech FROM vocabulary WHERE id=?', (wid,)).fetchone()[0] for wid in words)
        batches[batch.upper()] = dict(vocabulary=len(words), lexical=len(words)-pos['expression'],
                                     phrases=pos['expression'], new_examples=len(examples), pos=dict(pos))
    old_words = {r[0] for r in baseline.execute('SELECT id FROM vocabulary')}
    old_examples = {r[0] for r in baseline.execute('SELECT id FROM examples')}
    check('Vocabulary delta exactly A+B+C', {r[0] for r in db.execute('SELECT id FROM vocabulary')} - old_words == new_words)
    check('Example delta exactly A+B+C', {r[0] for r in db.execute('SELECT id FROM examples')} - old_examples == new_examples)
    check('Unreduced DATA-08 targets', 800 <= len(new_words) <= 1200 and 1300 <= len(new_examples) <= 2000)
    old_ids = set(baseline.execute('SELECT id,kind,created_at FROM content_items'))
    check('All baseline Stable IDs/kinds/created_at retained', old_ids <= set(db.execute('SELECT id,kind,created_at FROM content_items')))
    check('All baseline sort keys retained', set(baseline.execute('SELECT id,sort_key FROM vocabulary')) <= set(db.execute('SELECT id,sort_key FROM vocabulary')))
    check('All baseline lesson memberships retained', set(baseline.execute('SELECT * FROM lesson_items')) <= set(db.execute('SELECT * FROM lesson_items')))
    check('All baseline listening order retained', set(baseline.execute('SELECT id,learning_order FROM listening_items')) <= set(db.execute('SELECT id,learning_order FROM listening_items')))
    check('No retired current content', db.execute('SELECT COUNT(*) FROM content_items WHERE is_active=0').fetchone()[0] == 0)
    stages = []
    for stage, version, evidence in [(1,14,'BASELINE'), (2,15,'A_COUNTS'), (3,16,'B_COUNTS'), (4,17,'C_COUNTS'), (5,18,'FINAL_COUNTS'), (6,19,'INTEGRATION_COUNTS'), (7,19,'SYSTEM_RESULTS')]:
        path = bundle if version == 19 else ROOT / f'Tests/Fixtures/content-v{version}-production.sqlite'
        con = connect(path)
        stats = {t: count(con,t) for t in ('vocabulary','meanings','examples','grammar','listening_items','questions')}
        record = load(ROOT / f'Docs/DATA08_{evidence}.json')
        reported = record.get('table_counts', record.get('counts'))
        if reported:
            check(f'Stage {stage} archived counts vs actual v{version}', all(reported[t] == n for t,n in stats.items()))
        stages.append(dict(stage=stage, content_version=version, actual_counts=stats,
                           evidence=f'Docs/DATA08_{evidence}.json', evidence_sha256=sha(ROOT / f'Docs/DATA08_{evidence}.json')))
        con.close()
    levels = {}
    for level in LEVELS:
        stats = {t: db.execute(f'SELECT COUNT(*) FROM "{t}" t JOIN content_items i ON i.id=t.id WHERE i.level=?', (level,)).fetchone()[0]
                 for t in ('vocabulary','meanings','examples','grammar','listening_items','questions','courses','lessons')}
        stats['sentence_examples'] = db.execute('SELECT COUNT(*) FROM examples e JOIN content_items i ON i.id=e.id WHERE i.level=? AND NOT EXISTS (SELECT 1 FROM pronunciation_examples p WHERE p.example_id=e.id)', (level,)).fetchone()[0]
        levels[level] = stats
    raw = git('rev-list', '--objects', '--all')
    sizes = subprocess.run(['git','-C',str(ROOT),'cat-file','--batch-check=%(objecttype) %(objectname) %(objectsize) %(rest)'],input=raw,stdout=subprocess.PIPE,check=True).stdout.decode()
    blobs = []
    for line in sizes.splitlines():
        kind, oid, size, *name = line.split(' ',3)
        if kind == 'blob':
            blobs.append(dict(oid=oid,bytes=int(size),path=name[0] if name else ''))
    git_sizes = dict(reachable_blob_count=len(blobs), over_50_MiB=[b for b in blobs if b['bytes']>50*1024*1024],
                     over_100_MiB=[b for b in blobs if b['bytes']>100*1024*1024],largest=sorted(blobs,key=lambda b:b['bytes'],reverse=True)[:12])
    check('No GitHub 100 MiB blob in reachable history', not git_sizes['over_100_MiB'])
    # Protect every existing Content/Resources/fixture byte, including legacy temp DB.
    preserved = []
    for name in git('ls-files','-z','Content','Resources','Tests/Fixtures').decode().split('\0'):
        if name:
            original = git('show', 'HEAD:' + name)
            check('Preserved tracked artifact: ' + name, hashlib.sha256(original).hexdigest() == sha(ROOT / name))
            preserved.append(dict(path=name,bytes=(ROOT/name).stat().st_size,sha256=sha(ROOT/name)))
    native_definitions = sum(len(re.findall(r'func\s+test\w*\s*\(', p.read_text())) for p in (ROOT/'Tests').glob('*.swift'))
    result = dict(stage='DATA-08-8',status='PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL',
                  evidence_base_commit=git('rev-parse','HEAD').decode().strip(),metadata=source['metadata'],
                  source_sha256=sha(ROOT/'Content/production.json'),bundle_sha256=sha(bundle),rebuilt_sha256=sha(args.rebuilt),
                  build_validation=build['validation'],build_seconds=build['seconds'],reconstruction_tables=comparisons,
                  integrity=integrity,checks=checks,stages=stages,batches=batches,
                  data08=dict(vocabulary=len(new_words),lexical=sum(b['lexical'] for b in batches.values()),phrases=sum(b['phrases'] for b in batches.values()),new_unique_examples=len(new_examples)),
                  production_counts={t:count(db,t) for t in table_names},by_level=levels,git_sizes=git_sizes,
                  preserved_artifacts=preserved,routing_coverage=system['coverage'],
                  native=dict(status='BLOCKED',definitions=native_definitions,executed=0),
                  independent_human_review=dict(status='NOT TESTED',executed=0),
                  limitation='Read-only SQL/structural and archive checks; not Swift/iOS execution or linguistic certification.')
    for con in (db,rebuilt,baseline):
        con.close()
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rebuilt', type=Path, required=True)
    parser.add_argument('--build-report', type=Path, required=True)
    parser.add_argument('--system-audit', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    result = run(args)
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],data08=result['data08'],failed=[c for c in result['checks'] if c['status']=='FAIL']),ensure_ascii=False))
    raise SystemExit(0 if result['status']=='PASS' else 1)
