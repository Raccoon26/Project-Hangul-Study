"""Apply explicit DATA10 QA patches to immutable27; preserve IDs, rows and snapshots."""
import argparse,gzip,hashlib,json
from pathlib import Path
from build_content import ROOT
BASE_SHA='88e9599648182e2fd4372eecb738da60321913632cae32e0e25922048f5aef8b'

def prepare(output,revised):
    raw=gzip.decompress((ROOT/'Tests/Fixtures/content-v27-production.json.gz').read_bytes())
    assert hashlib.sha256(raw).hexdigest()==BASE_SHA
    source=json.loads(raw);m=json.loads((ROOT/'Content/data10-final-corrections.json').read_text())
    assert source['metadata']['content_version']==m['previous_content_version']==27 and m['content_version']==28
    owners=set();touched=set();changed_examples=set()
    for p in m['patches']:
        table,key,field=p['table'],p['key'],p['field']
        assert table in ('examples','listening_items','questions','question_choices')
        identity=(table,tuple(sorted(key.items())),field);assert identity not in touched;touched.add(identity)
        rows=[r for r in source['tables'][table] if all(r[k]==v for k,v in key.items())];assert len(rows)==1
        row=rows[0];assert row[field]==p['before'] and p['before']!=p['after'],identity
        row[field]=p['after'];owners.add(key.get('id',key.get('question_id')))
        if table=='examples':changed_examples.add(key['id'])
    # Reader exposes listening revision for questions/audio sourced from Example.
    # Propagate dependent listening revisions even when their SQL fingerprint is unchanged.
    dependent={r['id'] for r in source['tables']['listening_items'] if r['source_example_id'] in changed_examples}
    revised_ids=owners|dependent
    for r in source['tables']['content_items']:
        if r['id'] in revised_ids:
            assert r['updated_at']<m['updated_at'];r['revision']+=1;r['updated_at']=m['updated_at']
    source['metadata']['content_version']=28
    output.write_text(json.dumps(source,ensure_ascii=False,indent=2)+'\n');revised.write_text(json.dumps(sorted(revised_ids),indent=2)+'\n')
    return dict(content_version=28,fields=len(touched),payload_owners=len(owners),dependent_revision_only=sorted(dependent-owners),revised_ids=len(revised_ids),inserted=0,deleted=0)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--revised',type=Path,required=True);a=p.parse_args()
    protected=[(ROOT/f).resolve() for f in ('Content','Resources','Tests/Fixtures')]
    if a.output.resolve()==a.revised.resolve() or any(x.resolve().is_relative_to(d) for x in (a.output,a.revised) for d in protected):p.error('use distinct temporary outputs outside protected inputs')
    print(json.dumps(prepare(a.output,a.revised)))
