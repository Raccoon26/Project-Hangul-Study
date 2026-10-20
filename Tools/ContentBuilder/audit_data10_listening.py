"""Read-only DATA10-1 corpus inventory; heuristics are not language approval.

Run from any directory. No imports, UUID allocation, DB writes or retirement.
"""
import argparse
import collections
import hashlib
import json
import re
import sqlite3
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def normalize(text):
    return ' '.join(unicodedata.normalize('NFC', text).split())


def summary(values):
    values = sorted(values)
    return dict(n=len(values), min=values[0], median=values[len(values)//2],
                p90=values[int((len(values)-1)*.9)], max=values[-1])


def duplicate_groups(rows, key):
    groups = collections.defaultdict(list)
    for row in rows:
        groups[key(row)].append(row['id'])
    return [dict(key=k, ids=v) for k, v in sorted(groups.items()) if len(v) > 1]


def run():
    source = json.loads((ROOT/'Content/production.json').read_text())
    db = sqlite3.connect((ROOT/'Resources/content.sqlite').as_uri()+'?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    checks = {}
    metadata = dict(db.execute('SELECT * FROM content_metadata').fetchone())
    checks['source_metadata'] = all(metadata[k] == v for k, v in source['metadata'].items())
    # Compare every source row, including nulls; preserve multiplicity, not just IDs.
    for table, rows in source['tables'].items():
        columns = [r[1] for r in db.execute('PRAGMA table_info('+table+')')]
        payload = lambda row: json.dumps([row.get(k) for k in columns], ensure_ascii=False)
        actual = collections.Counter(payload(dict(r)) for r in db.execute('SELECT * FROM '+table))
        expected = collections.Counter(payload(r) for r in rows)
        checks['source_rows:'+table] = actual == expected
    checks['integrity'] = db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    checks['foreign_keys'] = not list(db.execute('PRAGMA foreign_key_check'))
    rows = [dict(r) for r in db.execute('''SELECT l.*,i.level,i.difficulty,i.is_active,
        e.korean,e.japanese,ei.is_active AS source_active,ei.level AS source_level,
        q.id AS question_id,q.question_type,q.prompt_ja,q.prompt_ko,q.explanation_ja AS feedback,
        q.answer_json,q.rubric_json,qi.is_active AS question_active,qi.level AS question_level
        FROM listening_items l JOIN content_items i ON i.id=l.id
        JOIN examples e ON e.id=l.source_example_id JOIN content_items ei ON ei.id=e.id
        JOIN questions q ON q.listening_id=l.id JOIN content_items qi ON qi.id=q.id
        ORDER BY i.level,l.learning_order,l.id''')]
    for r in rows:
        r['task'] = json.loads(r.pop('rubric_json'))['listening_task']
        r['answer'] = json.loads(r.pop('answer_json'))
        r['choices'] = [dict(c) for c in db.execute(
            'SELECT choice_id,text FROM question_choices WHERE question_id=? ORDER BY ordinal',
            (r['question_id'],))]
    checks['one_question_per_item'] = len(rows) == db.execute('SELECT COUNT(*) FROM listening_items').fetchone()[0] == len({r['id'] for r in rows})
    checks['active_and_matching_levels'] = all(r['is_active'] == r['source_active'] == r['question_active'] == 1 and r['level'] == r['source_level'] == r['question_level'] for r in rows)
    checks['reference_without_transcript_copy'] = all(r['source_example_id'] and r['transcript_ko'] is None for r in rows)
    checks['no_korean_prompt'] = all(r['prompt_ko'] is None for r in rows)
    checks['unique_level_order'] = len({(r['level'],r['learning_order']) for r in rows}) == len(rows)
    levels = {}
    for level in sorted({r['level'] for r in rows}):
        subset = [r for r in rows if r['level'] == level]
        batches = collections.Counter(r['learning_order']//20 for r in subset)
        levels[level] = dict(count=len(subset), tasks=dict(collections.Counter(r['task'] for r in subset)),
            difficulty_null=sum(r['difficulty'] is None for r in subset),
            characters=summary([len(normalize(r['korean'])) for r in subset]),
            eojeol=summary([len(normalize(r['korean']).split()) for r in subset]),
            order_min=min(r['learning_order'] for r in subset), order_max=max(r['learning_order'] for r in subset),
            next_fresh_batch_order=(max(batches)+1)*20, batches=len(batches), max_batch_size=max(batches.values()))
    checks['bounded_batches'] = all(v['max_batch_size'] <= 20 for v in levels.values())
    groups = dict(source_id=duplicate_groups(rows, lambda r:r['source_example_id']),
        korean=duplicate_groups(rows, lambda r:normalize(r['korean'])),
        pair=duplicate_groups(rows, lambda r:(normalize(r['korean']),normalize(r['japanese']))),
        terminal_punctuation=duplicate_groups(rows, lambda r:normalize(r['korean']).rstrip('.!?')))
    # Full Example corpus is the duplicate comparison universe for future authoring.
    examples = [dict(r) for r in db.execute('SELECT e.*,i.level FROM examples e JOIN content_items i ON i.id=e.id WHERE i.is_active=1')]
    all_duplicates = dict(korean=duplicate_groups(examples,lambda r:normalize(r['korean'])),
        pair=duplicate_groups(examples,lambda r:(normalize(r['korean']),normalize(r['japanese']))))
    sources = {r['source_example_id'] for r in rows}
    ge = list(db.execute('SELECT grammar_id,example_id FROM grammar_examples'))
    grammar_ids = {g for g, e in ge if e in sources}
    # Use DB diff against the immutable pre-DATA09 deployment, not authoring array order.
    old = sqlite3.connect((ROOT/'Tests/Fixtures/content-v19-production.sqlite').as_uri()+'?mode=ro',uri=True)
    new_grammar = {r[0] for r in db.execute('SELECT id FROM grammar')} - {r[0] for r in old.execute('SELECT id FROM grammar')}
    old.close()
    new_examples = {e for g,e in ge if g in new_grammar}
    coverage = dict(unique_listening_sources=len(sources), active_examples=len(examples),
        grammar_with_listening=len(grammar_ids), grammar_total=db.execute('SELECT COUNT(*) FROM grammar').fetchone()[0],
        data09_grammar_total=len(new_grammar), data09_grammar_with_listening=len(new_grammar & grammar_ids),
        data09_linked_examples=len(new_examples), data09_linked_examples_with_listening=len(new_examples & sources),
        multi_sentence_items=sum(len(re.findall(r'[.!?]+',r['korean'])) >= 2 for r in rows),
        feedback_equals_translation=sum(normalize(r['feedback']) == normalize(r['japanese']) for r in rows))
    prerequisites = json.loads((ROOT/'Docs/DATA09_FINAL_PREREQUISITES.json').read_text())
    coverage['existing_prerequisite_candidates_in_listening'] = dict(collections.Counter(
        r['status'] for r in prerequisites['records'] if r['example_id'] in sources))
    # Repeated three-eojeol endings flag templates for review, not semantic duplicates.
    tails = collections.defaultdict(list)
    for r in rows:
        words = normalize(r['korean']).split()
        if len(words) >= 4:
            tails[' '.join(words[-3:])].append(r['id'])
    repeated = [dict(ending=k,count=len(v),ids=v) for k,v in sorted(tails.items(),key=lambda x:(-len(x[1]),x[0])) if len(v)>=3]
    # Deterministic min/median/max per level/task for explicit assistant rereading.
    samples = []
    for level in sorted(levels):
        for task in ['meaning','korean','dictation','comprehension']:
            subset = sorted([r for r in rows if r['level']==level and r['task']==task],key=lambda r:(len(r['korean']),r['id']))
            if subset:
                samples.extend(subset[p] for p in sorted({0,len(subset)//2,len(subset)-1}))
    protected = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
        for folder in ['Content','Resources','Tests/Fixtures'] for p in sorted((ROOT/folder).rglob('*')) if p.is_file() and p.suffix not in ('.pyc',) and '__pycache__' not in p.parts}
    result = dict(scope='DATA10-1 read-only; no linguistic approval',metadata=metadata,
        source_rows=sum(map(len,source['tables'].values())), checks=checks,
        counts={t:db.execute('SELECT COUNT(*) FROM '+t).fetchone()[0] for t in ['vocabulary','meanings','examples','grammar','questions','listening_items']},
        audio_modes=dict(collections.Counter(r['audio_mode'] for r in rows)),levels=levels,
        tasks=dict(collections.Counter(r['task'] for r in rows)),duplicates=groups,
        full_example_duplicates=all_duplicates,coverage=coverage,repeated_three_eojeol_endings=repeated,
        assistant_review_samples=samples,protected_sha256=protected)
    db.close()
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path,required=True)
    args = parser.parse_args()
    result = run()
    args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k in ('counts','levels','coverage','tasks','checks')},ensure_ascii=False,indent=2))
    raise SystemExit(0 if all(result['checks'].values()) else 1)
