"""Reproduce Content29 from immutable28 and reviewed fixed IDs/relations.
Only writes distinct temporary outputs; never imports into a user database.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
from build_content import ROOT

BASE_SHA = '521f047d3bb9fbb4056c651c6d6e561d18db79f3072f2f46acf6a76ff447ba36'


def prepare(output, revised):
    raw = gzip.decompress((ROOT/'Tests/Fixtures/content-v28-production.json.gz').read_bytes())
    assert hashlib.sha256(raw).hexdigest() == BASE_SHA
    source = json.loads(raw); tables = source['tables']
    manifest = json.loads((ROOT/'Content/data10-integration-ids.json').read_text())
    assert source['metadata']['content_version'] == manifest['from_version'] == 28
    source['metadata']['content_version'] = manifest['to_version']
    old_ids = {r['id'] for r in tables['content_items']}; changed = set()
    stamp = manifest['created_at']; examples = {r['id']:r for r in tables['examples']}
    tables['sources'].append(dict(id=manifest['source_id'], title='DATA10：初中級の短い聴解レッスンと復習参照', citation='既存の検収済み原文・問題IDを参照する学習配置。AI照合。独立教師検収・音声検聴は未実施。', url=None, accessed_at=None))

    def item(item_id, kind):
        assert item_id not in old_ids
        tables['content_items'].append(dict(id=item_id, kind=kind, revision=1, is_active=1, level='lower_intermediate', created_at=stamp, updated_at=stamp))
        tables['item_sources'].append(dict(content_id=item_id, source_id=manifest['source_id'], note='既存ID・順序・進行中snapshotを保持する参照配置。'))

    for course in manifest['courses']:
        item(course['id'], 'course')
        tables['courses'].append({k:course[k] for k in ('id','title_ja','description_ja','ordinal')})
        for unit in course['units']:
            item(unit['id'], 'tag')
            tables['tags'].append(dict(id=unit['id'], label_ja=unit['title_ja'], namespace='data10_unit'))
        for lesson in course['lessons']:
            item(lesson['id'], 'lesson')
            tables['lessons'].append(dict(id=lesson['id'], course_id=course['id'], title_ja=lesson['title_ja'], ordinal=lesson['ordinal']))
            tables['item_tags'].append(dict(content_id=lesson['id'], tag_id=lesson['unit_id']))
            assert len(lesson['listening_ids']) == len(set(lesson['listening_ids'])) == 5
            for ordinal, lid in enumerate(lesson['listening_ids']):
                assert lid in old_ids
                tables['lesson_items'].append(dict(lesson_id=lesson['id'], content_id=lid, ordinal=ordinal)); changed.add(lid)
    existing = {tuple(r[k] for k in ('source_id','target_id','relation')) for r in tables['content_links']}
    for rows, target, relation in ((manifest['prerequisites'], 'grammar_id', 'prerequisite'), (manifest['related_vocabulary'], 'vocabulary_id', 'related')):
        for row in rows:
            assert row['observed_form_ko'] in examples[row['example_id']]['korean']
            key = row['example_id'], row[target], relation
            assert key not in existing
            existing.add(key)
            tables['content_links'].append(dict(zip(('source_id','target_id','relation'),key)))
            changed.update(key[:2])
    assert changed <= old_ids
    for row in tables['content_items']:
        if row['id'] in changed:
            row['revision'] += 1; row['updated_at'] = stamp
    output.write_text(json.dumps(source,ensure_ascii=False,indent=2)+'\n')
    revised.write_text(json.dumps(sorted(changed),indent=2)+'\n')
    return dict(version=29, courses=3, lessons=72, units=6, memberships=360, relations=360, revised_ids=len(changed))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True); parser.add_argument('--revised',type=Path,required=True)
    args = parser.parse_args()
    protected = [(ROOT/p).resolve() for p in ('Content','Resources','Tests/Fixtures')]
    if args.output.resolve() == args.revised.resolve() or any(p.resolve().is_relative_to(d) for p in (args.output,args.revised) for d in protected):
        parser.error('use distinct temporary outputs outside protected inputs')
    print(json.dumps(prepare(args.output,args.revised)))
