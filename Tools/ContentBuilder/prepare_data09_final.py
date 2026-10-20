"""Apply explicit DATA09-5 editorial patches to immutable Content22, producing23.

No UUIDs/relations/rows allocated or removed. Outputs must be outside protected inputs.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE_SHA = '13a6739bb93daee36426f04ac83b95f7244a62c227ea90b0ddda2d179eeeafeb'


def prepare(output, revised):
    raw = gzip.decompress((ROOT/'Tests/Fixtures/content-v22-production.json.gz').read_bytes())
    if hashlib.sha256(raw).hexdigest() != BASE_SHA:
        raise ValueError('Content22 source snapshot changed')
    source = json.loads(raw)
    manifest = json.loads((ROOT/'Content/data09-final-corrections.json').read_text())
    assert source['metadata']['content_version'] == manifest['previous_content_version'] == 22
    assert manifest['content_version'] == 23
    owners = set()
    touched = set()
    for patch in manifest['patches']:
        table, key, field = patch['table'], patch['key'], patch['field']
        assert table in ('grammar', 'examples', 'questions', 'question_choices')
        matches = [r for r in source['tables'][table] if all(r[k] == v for k, v in key.items())]
        assert len(matches) == 1, key
        row = matches[0]
        identity = (table, tuple(sorted(key.items())), field)
        assert identity not in touched, identity
        touched.add(identity)
        assert row[field] == patch['before'] and patch['before'] != patch['after'], identity
        row[field] = patch['after']
        owners.add(key.get('id', key.get('question_id')))
    assert len(owners) == 25 and len(touched) == 31
    for row in source['tables']['content_items']:
        if row['id'] in owners:
            assert row['updated_at'] < manifest['updated_at']
            row['revision'] += 1
            row['updated_at'] = manifest['updated_at']
    source['metadata']['content_version'] = 23
    output.write_text(json.dumps(source, ensure_ascii=False, indent=2)+'\n')
    revised.write_text(json.dumps(sorted(owners), indent=2)+'\n')
    return dict(content_version=23, fields=len(touched), revised_ids=len(owners), inserted=0, deleted=0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--revised', type=Path, required=True)
    args = parser.parse_args()
    protected = [(ROOT/p).resolve() for p in ('Content', 'Resources', 'Tests/Fixtures')]
    if args.output.resolve() == args.revised.resolve() or any(p.resolve().is_relative_to(d) for p in (args.output, args.revised) for d in protected):
        parser.error('use distinct candidate outputs outside protected inputs')
    print(json.dumps(prepare(args.output, args.revised)))
