"""Read-only verification of authored DATA-09-1 analysis and design references.

No automatic linguistic classification, Production import or UUID allocation.
"""
import argparse
import collections
import hashlib
import json
import re
import sqlite3
import unicodedata
from pathlib import Path
from audit_data08_final import audit

ROOT = Path(__file__).resolve().parents[2]


def load(name):
    return json.loads((ROOT / name).read_text())


def run():
    baseline = load('Docs/DATA09_BASELINE.json')
    proposal = load('Docs/DATA09_GRAMMAR_PLAN.json')
    review = load('Docs/DATA09_PREREQUISITE_AUDIT.json')
    previous = load('Docs/DATA08_FINAL_GRAMMAR.json')
    source = load('Content/production.json')
    db = sqlite3.connect((ROOT/'Resources/content.sqlite').as_uri()+'?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    checks = []

    def check(name, passed):
        checks.append(dict(check=name, status='PASS' if passed else 'FAIL'))

    for path, expected in baseline['protected_files'].items():
        check('Preserved bytes: '+path, hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == expected)
    check('Content/Schema/reader unchanged', dict(db.execute('SELECT * FROM content_metadata').fetchone()) == baseline['metadata'])
    structural = audit(source, ROOT/'Resources/content.sqlite')
    check('All source fields match actual DB and retained DATA08 structural audit', structural['validation']['error_count'] == 0)
    grammar = {r['id']:dict(r) for r in db.execute('SELECT * FROM grammar')}
    check('Exactly42 existing Grammar, no lower_intermediate Grammar', len(grammar) == 42 and db.execute("SELECT COUNT(*) FROM grammar g JOIN content_items i ON i.id=g.id WHERE i.level='lower_intermediate'").fetchone()[0] == 0)
    check('Existing42 complete payloads retained', all(grammar[r['id']] == {k:v for k,v in r.items() if k in grammar[r['id']]} for r in baseline['grammar']))
    old = {r['id']:r for r in previous['candidates']}
    rows = review['records']
    check('Exactly163 unique original candidate IDs, no omitted rows', len(rows) == len({r['example_id'] for r in rows}) == 163 and {r['example_id'] for r in rows} == set(old))
    plans = proposal['units']
    keys = {p['plan_key']:p for p in plans}
    check('54 proposed teaching units within45–60; no runtime IDs/approvals', len(plans) == len(keys) == 54 and all(p['runtime_id'] is None and p['production_approved'] is False for p in plans))
    check('Long-term goal350–500 unchanged', proposal['long_term_goal']['min'] == 350 and proposal['long_term_goal']['max'] == 500)
    names = [re.sub(r'\s+', '', unicodedata.normalize('NFC', p['pattern'])) for p in plans]
    check('No exact duplicate draft/registered patterns', len(names) == len(set(names)) and not set(names).intersection(re.sub(r'\s+', '', unicodedata.normalize('NFC', g['pattern'])) for g in grammar.values()))
    for row in rows:
        eid = row['example_id']
        current = db.execute('SELECT e.korean,e.japanese,i.level FROM examples e JOIN content_items i ON i.id=e.id WHERE e.id=?',(eid,)).fetchone()
        check(f"Candidate{row['index']:03} actual pair/level/original features/quoted evidence", current is not None and tuple(current) == (row['korean'],row['japanese'],row['level_in_production']) and row['source_features'] == old[eid]['features'] and row['evidence_span'] in row['korean'])
        check(f"Candidate{row['index']:03} authored rationale/reference/no approval", bool(row['reason_ko']) and row['primary_category'] in ('missing_grammar','level_mismatch_candidate','review_only') and set(row['related_plan_keys']) <= set(keys) and not row['reuse_approved'] and not row['human_reviewed'])
    check('Category totals reflect actual163 decisions', dict(collections.Counter(r['primary_category'] for r in rows)) == review['counts'] and sum(review['counts'].values()) == 163)
    existing_edges = [(r[0],r[1]) for r in db.execute("SELECT l.source_id,l.target_id FROM content_links l JOIN grammar a ON a.id=l.source_id JOIN grammar b ON b.id=l.target_id WHERE l.relation='prerequisite'")]
    graph = {gid:[] for gid in grammar}
    for source_id,target_id in existing_edges:
        graph[source_id].append(target_id)
    for plan in plans:
        key = plan['plan_key']
        graph[key] = []
        references = plan['prerequisites']+plan['comparisons']
        check(key+' all references resolve; no self-comparison', all((r.get('plan_key') in keys and r['plan_key'] != key) if 'plan_key' in r else r.get('existing_grammar_id') in grammar for r in references))
        for ref in plan['prerequisites']:
            target = ref.get('plan_key', ref.get('existing_grammar_id'))
            graph[key].append(target)
        check(key+' prerequisite order and bounded question/examples design', all(int(r['plan_key'][1:]) < int(key[1:]) for r in plan['prerequisites'] if 'plan_key' in r) and plan['target_examples'] <= 6 and 1 <= plan['target_questions'] <= 20 and len(plan['comparisons']) <= 6)
        expected_ids = {r['example_id'] for r in rows if key in r['related_plan_keys']}
        check(key+' reuse ledger complete and unapproved', {r['example_id'] for r in plan['reuse_candidates']} == expected_ids and all(not r['approved'] for r in plan['reuse_candidates']))
        for ref in plan['reuse_candidates']:
            actual = {(r['id'],r['learning_order'],r['audio_mode']) for r in db.execute('SELECT id,learning_order,audio_mode FROM listening_items WHERE source_example_id=?',(ref['example_id'],))}
            check(key+' reusable listening IDs:'+ref['example_id'], actual == {(r['id'],r['learning_order'],r['audio_mode']) for r in ref['existing_listening']})
            actual_questions = {(r[0],r[1],r[2]) for r in db.execute("SELECT q.id,q.question_type,json_extract(q.rubric_json,'$.mode') FROM content_links l JOIN questions q ON q.id=l.source_id WHERE l.target_id=? AND l.relation='related'",(ref['example_id'],))}
            check(key+' reusable question IDs:'+ref['example_id'], actual_questions == {(r['id'],r['question_type'],r['production_mode']) for r in ref['existing_related_questions']})
    active,done = set(),set()

    def visit(key):
        if key in active:
            return False
        if key in done:
            return True
        active.add(key)
        for target in graph.get(key,[]):
            if not visit(target):
                return False
        active.remove(key)
        done.add(key)
        return True

    check('Existing19 plus proposed prerequisite edges form DAG', all(visit(k) for k in graph))
    lessons = collections.defaultdict(list)
    for plan in plans:
        lessons[plan['lesson_key']].append(plan)
    check('18 proposed3-item lessons appended after existing ordinal46', len(lessons) == 18 and all(len(v) == 3 and len({r['proposed_lesson_ordinal'] for r in v}) == 1 for v in lessons.values()) and min(p['proposed_lesson_ordinal'] for p in plans) > db.execute("SELECT MAX(l.ordinal) FROM lessons l JOIN content_items i ON i.id=l.id WHERE i.level='lower_intermediate'").fetchone()[0])
    counts = {t:db.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0] for t in ('vocabulary','meanings','examples','grammar','grammar_examples','listening_items','questions','courses','lessons')}
    result = dict(stage='DATA-09-1', status='PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL',
                  checks=checks,check_count=len(checks),category_counts=review['counts'],production_counts=counts,
                  source_tables=structural['source_tables_scanned'],source_rows=structural['source_rows_scanned'],
                  proposed_units=len(plans),proposed_lessons=len(lessons),existing_prerequisite_edges=len(existing_edges),
                  existing_and_proposed_DAG_nodes=len(graph),new_production_units=0,
                  source_sha256=hashlib.sha256((ROOT/'Content/production.json').read_bytes()).hexdigest(),
                  bundle_sha256=hashlib.sha256((ROOT/'Resources/content.sqlite').read_bytes()).hexdigest(),
                  limitation='Structural/coverage/design-reference checks only. No linguistic certification, confirmed Level reassignment, human approval, Swift execution or Production writes.')
    db.close()
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path,required=True)
    args = parser.parse_args()
    result = run()
    args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','check_count','category_counts','production_counts')},ensure_ascii=False))
    raise SystemExit(0 if result['status']=='PASS' else 1)
