"""Reconstruct Content24 from immutable23 plus fixed, reviewed integration relations.
Never allocate IDs or overwrite a release snapshot/Production bundle.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
from build_content import ROOT

BASE_SHA='c8a74e3b61809aabe5d2dd88768446f986792f2585d40ef78327c50b2b6c5b1e'


def prepare(output,revised):
    raw=gzip.decompress((ROOT/'Tests/Fixtures/content-v23-production.json.gz').read_bytes())
    assert hashlib.sha256(raw).hexdigest()==BASE_SHA
    source=json.loads(raw);tables=source['tables']
    manifest=json.loads((ROOT/'Content/data09-integration-ids.json').read_text());stamp=manifest['created_at']
    assert source['metadata']['content_version']==23
    source['metadata']['content_version']=24
    old_ids={r['id'] for r in tables['content_items']};changed=set()
    tables['sources'].append(dict(id=manifest['source_id'],title='DATA09：文法の単元・先行復習・関連語',citation='既存の検収済み内容を参照する学習配置。assistant検討。独立原語話者・教師監修は未実施。',url=None,accessed_at=None))
    for u in manifest['units']:
        assert u['id'] not in old_ids
        tables['content_items'].append(dict(id=u['id'],kind='tag',revision=1,is_active=1,level='lower_intermediate',created_at=stamp,updated_at=stamp))
        tables['tags'].append(dict(id=u['id'],label_ja=u['title_ja'],namespace='data09_unit'))
        tables['item_sources'].append(dict(content_id=u['id'],source_id=manifest['source_id'],note='既存レッスン・教材IDと進行中の記録を保つ単元。'))
        for lesson in u['lesson_ids']:
            assert any(r['id']==lesson and r['course_id']==u['course_id'] for r in tables['lessons'])
            tables['item_tags'].append(dict(content_id=lesson,tag_id=u['id']));changed.add(lesson)
    existing={(r['source_id'],r['target_id'],r['relation']) for r in tables['content_links']}
    links=[{k:r[k] for k in ('source_id','target_id','relation')} for r in manifest['prerequisites']]
    links += [dict(source_id=r['grammar_id'],target_id=r['vocabulary_id'],relation='related') for r in manifest['related_vocabulary']]
    for link in links:
        key=tuple(link[k] for k in ('source_id','target_id','relation'));assert key not in existing,key
        existing.add(key);tables['content_links'].append(link);changed|={link['source_id'],link['target_id']}
    assert changed<=old_ids
    for r in tables['content_items']:
        if r['id'] in changed:r['revision']+=1;r['updated_at']=stamp
    output.write_text(json.dumps(source,ensure_ascii=False,indent=2)+'\n')
    revised.write_text(json.dumps(sorted(changed),indent=2)+'\n')
    return dict(version=24,new_unit_tags=6,added_relations=len(links),revised_existing_ids=len(changed))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--revised',type=Path,required=True);args=parser.parse_args()
    protected=[(ROOT/p).resolve() for p in ('Content','Resources','Tests/Fixtures')]
    if args.output.resolve()==args.revised.resolve() or any(p.resolve().is_relative_to(d) for p in (args.output,args.revised) for d in protected):parser.error('use distinct temporary outputs outside protected inputs')
    print(json.dumps(prepare(args.output,args.revised)))
