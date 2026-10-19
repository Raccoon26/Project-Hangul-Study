"""Reproducible DATA-08 structural audit and narrow editorial regression lints.

This checks contracts and known mistakes, not Korean/Japanese correctness.
Language rereading, dictionary evidence and unresolved questions live in Docs.
Historical cohort registries identify released IDs; source rows are authoritative.
"""
import argparse
import collections
import hashlib
import json
import re
import sqlite3
import unicodedata
from pathlib import Path

from build_content import ROOT
from source_reader import strict_json
from validator import Report, metadata, row_fields


def norm(text):
    return ''.join(unicodedata.normalize('NFC', text).casefold().split())


def cohorts():
    return {b: json.loads((ROOT/f'Content/data08-{b.lower()}-ids.json').read_text())
            for b in 'ABC'}


def linguistic_lints(example):
    """Only observed failure patterns. Empty result is NOT language approval."""
    ko, ja = example.get('korean', ''), example.get('japanese', '')
    issues = []
    if '상담을 받' in ko and '相談を受け' in ja:
        issues.append('counselling_recipient_reversed')
    if any(text in ja for text in ('胸がわくわく', 'ぽっかりと寂しい', 'するのは不慣れ')):
        issues.append('reviewed_japanese_collocation')
    if re.search(r'실마리가.{0,8}풀[리렸려]', ko) or '糸口が開け' in ja:
        issues.append('clue_and_solution_collocation_mixture')
    return issues


def audit(source, db_path=None):
    report = Report()
    metadata(source['metadata'], report)
    tables = source['tables']
    schema = sqlite3.connect(':memory:')
    schema.executescript((ROOT/'Content/content-schema-v4.sql').read_text())
    columns = {t: {r[1]: r for r in schema.execute(f'PRAGMA table_info("{t}")')}
               for t in tables}
    scanned = 0
    for table, values in tables.items():
        if not columns[table]:
            report.error('unknown_table', table, 'No schema table')
            continue
        pk = [c for c, info in columns[table].items() if info[5]]
        seen = set()
        for index, row in enumerate(values):
            location = f'{table}:{index}'
            row_fields(table, row, columns[table], location, report)
            scanned += 1
            key = tuple(row.get(c) for c in pk)
            if pk and key in seen:
                report.error('duplicate_primary_key', location, str(key))
            seen.add(key)
        for fk in schema.execute(f'PRAGMA foreign_key_list("{table}")'):
            _, _, parent, child_col, parent_col, *_ = fk
            parent_values = {r.get(parent_col) for r in tables.get(parent, [])}
            for row in values:
                value = row.get(child_col)
                if value is not None and value not in parent_values:
                    report.error('missing_reference', table, f'{child_col}={value}')
    if report.error_count:
        schema.close()
        return dict(validation=report.as_dict(), source_rows_scanned=scanned,
                    source_tables_scanned=len(tables), scope=None,
                    limitation='Invalid source: cohort/language lints not evaluated.')
    rows = {t: {r['id']: r for r in values if 'id' in r} for t, values in tables.items()}
    registry = cohorts()
    words = [w for r in registry.values() for w in r['vocabulary']]
    word_ids = {w['id'] for w in words}
    meaning_ids = {i for w in words for i in w['meaning_ids']}
    example_ids = {i for w in words for i in w['example_ids']}
    note_ids = {w['note_id'] for w in words if w['note_id']}
    if len(word_ids) != len(words):
        report.error('overlapping_cohorts', 'A/B/C', 'Vocabulary IDs reused across batches')
    heads = collections.defaultdict(list)
    ko_sentences = collections.defaultdict(list)
    ja_sentences = collections.defaultdict(list)
    for row in tables['vocabulary']:
        heads[norm(row['headword'])].append(row['id'])
    for row in tables['examples']:
        ko_sentences[norm(row['korean'])].append(row['id'])
        ja_sentences[norm(row['japanese'])].append(row['id'])
    for group in heads.values():
        if len(group) > 1 and word_ids.intersection(group):
            report.error('duplicate_data08_headword', 'vocabulary', str(group))
    for group in ko_sentences.values():
        if len(group) > 1 and example_ids.intersection(group):
            report.error('duplicate_data08_korean', 'examples', str(group))
    links = {(r['source_id'], r['target_id'], r['relation']) for r in tables['content_links']}
    ve = {(r['meaning_id'], r['example_id']) for r in tables['vocabulary_examples']}
    ge = {(r['grammar_id'], r['example_id']) for r in tables['grammar_examples']}
    for word in words:
        wid = word['id']
        v = rows['vocabulary'].get(wid)
        if v is None:
            report.error('missing_cohort_payload', wid, 'vocabulary')
            continue
        if len(set(word['example_ids'])) != 2:
            report.error('cohort_examples', wid, 'Expected two distinct example references')
        actual_meanings = {m['id'] for m in tables['meanings'] if m['vocabulary_id'] == wid}
        if actual_meanings != set(word['meaning_ids']):
            report.error('cohort_meanings', wid, 'Released meaning membership differs')
        ordinals = []
        for mid in word['meaning_ids']:
            m = rows['meanings'].get(mid)
            if m is None:
                report.error('missing_cohort_payload', mid, 'meaning')
                continue
            ordinals.append(m['ordinal'])
            if m['part_of_speech'] != v['part_of_speech']:
                report.error('cohort_meaning_pos', mid, 'Meaning POS differs from this cohort lemma')
            refs = {eid for meaning, eid in ve if meaning == mid}
            if not refs or not refs <= set(word['example_ids']):
                report.error('cohort_sense_examples', mid, 'Missing or unrelated example')
        if sorted(ordinals) != list(range(len(ordinals))):
            report.error('cohort_ordinal', wid, str(ordinals))
        if {eid for mid, eid in ve if mid in word['meaning_ids']} != set(word['example_ids']):
            report.error('cohort_example_membership', wid, 'Example membership differs')
        note_id = word['note_id']
        if note_id and (wid, note_id, 'learner_note') not in links:
            report.error('cohort_note_reference', wid, str(note_id))
        if v['part_of_speech'] in ('verb', 'adjective', 'expression') and v['has_batchim'] is not None:
            report.error('predicate_batchim', wid, 'Must be null')
        if v['part_of_speech'] == 'expression' and v['irregular_type'] is not None:
            report.error('phrase_irregular', wid, 'Must be null')
        if v['part_of_speech'] in ('verb', 'adjective') and v['headword'].endswith('하다') and v['irregular_type'] != 'other':
            report.error('hada_metadata', wid, 'Existing engine contract requires other')
    for table, ids in [('vocabulary', word_ids), ('meanings', meaning_ids),
                       ('examples', example_ids), ('learner_notes', note_ids)]:
        for item_id in ids:
            item = rows['content_items'].get(item_id)
            if not item or item['is_active'] != 1 or item['level'] != 'lower_intermediate':
                report.error('cohort_active_level', item_id, table)
    for eid in example_ids:
        if eid in rows['examples']:
            for code in linguistic_lints(rows['examples'][eid]):
                report.error(code, eid, 'Observed pattern requires editorial correction')
    for nid in note_ids:
        note = rows['learner_notes'].get(nid)
        if not note:
            report.error('missing_cohort_payload', nid, 'note')
            continue
        if any(t in note['explanation_ja'] for t in ('独立Grammar教材は追加', '新規語として重複登録', '活用形として数えない', '慣用表現として登録')):
            report.error('editorial_delivery_text', nid, 'Production note describes content creation/counting')
    for batch in registry.values():
        for relation in batch['relations']:
            triple = tuple(relation[k] for k in ('source_id', 'target_id', 'relation'))
            if triple not in links:
                report.error('cohort_relation', str(triple), 'Missing released relation')
        for link in batch['grammar_links']:
            if (link['grammar_id'], link['example_id']) not in ge:
                report.error('cohort_grammar_reference', str(link), 'Missing released grammar reference')
    if db_path:
        with sqlite3.connect(Path(db_path).resolve().as_uri()+'?mode=ro', uri=True) as db:
            if db.execute('PRAGMA integrity_check').fetchall() != [('ok',)]:
                report.error('database_integrity', str(db_path), 'integrity_check failed')
            for violation in db.execute('PRAGMA foreign_key_check'):
                report.error('database_fk', str(db_path), str(violation))
            for table, values in tables.items():
                names = list(columns[table])
                defaults = {c: schema.execute('SELECT '+info[4]).fetchone()[0] if info[4] is not None else None
                            for c, info in columns[table].items()}
                expected = {tuple(r.get(c, defaults[c]) for c in names) for r in values}
                projection = ','.join('"'+c+'"' for c in names)
                actual = set(db.execute(f'SELECT {projection} FROM "{table}"'))
                if expected != actual or len(values) != len(actual):
                    report.error('source_bundle_mismatch', table, 'Source and DB rows differ')
            cursor = db.execute('SELECT * FROM content_metadata')
            meta = dict(zip((col[0] for col in cursor.description), cursor.fetchone()))
            if meta != dict(singleton=1, **source['metadata']):
                report.error('source_bundle_metadata', 'metadata', 'Source and DB differ')
    schema.close()
    return dict(validation=report.as_dict(), source_rows_scanned=scanned,
                source_tables_scanned=len(tables),
                scope=dict(vocabulary=len(word_ids), meanings=len(meaning_ids),
                           unique_examples=len(example_ids), example_placements=sum(len(w['example_ids']) for w in words),
                           notes=len(note_ids), lexical_relations=sum(len(r['relations']) for r in registry.values()),
                           grammar_references=sum(len(r['grammar_links']) for r in registry.values())),
                by_batch={b: dict(vocabulary=len(r['vocabulary']), new_examples=len(r['examples']),
                                 pos=dict(collections.Counter(rows['vocabulary'][w['id']]['part_of_speech'] for w in r['vocabulary'])))
                          for b, r in registry.items()},
                japanese_duplicate_candidates=[group for group in ja_sentences.values()
                                               if len(group) > 1 and example_ids.intersection(group)],
                limitation='Structural checks and narrow observed-error lints only; no automated claim of Korean/Japanese correctness or human review.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--database', type=Path)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    data = strict_json(args.source.read_text())
    result = audit(data, args.database)
    result['source_sha256'] = hashlib.sha256(args.source.read_bytes()).hexdigest()
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('scope', 'validation')}, ensure_ascii=False))
    raise SystemExit(int(bool(result['validation']['error_count'])))


if __name__ == '__main__':
    main()
