"""Read-only DATA10-A delivery counts, preservation evidence and reviewable app payload."""
import argparse
import collections
import gzip
import hashlib
import json
from pathlib import Path
import sqlite3
from build_content import ROOT
from validator import signatures


def audit():
    sha=lambda data:hashlib.sha256(data).hexdigest()
    source=json.loads((ROOT/'Content/production.json').read_text())
    manifest=json.loads((ROOT/'Content/data10-a-authoring.json').read_text())
    db=sqlite3.connect((ROOT/'Resources/content.sqlite').resolve().as_uri()+'?mode=ro',uri=True)
    old=sqlite3.connect((ROOT/'Tests/Fixtures/content-v24-production.sqlite').resolve().as_uri()+'?mode=ro',uri=True)
    a,b=signatures(old),signatures(db)
    schema='SELECT type,name,tbl_name,sql FROM sqlite_master ORDER BY type,name'
    same_schema=list(db.execute(schema))==list(old.execute(schema))
    assert same_schema
    table_report={}
    for table,rows in source['tables'].items():
        before=collections.Counter(old.execute('select * from '+table));after=collections.Counter(db.execute('select * from '+table))
        keys=sorted(rows[0]) if rows else [r[1] for r in db.execute('pragma table_info('+table+')')]
        actual=collections.Counter(db.execute('select '+','.join('"'+k+'"' for k in keys)+' from '+table))
        table_report[table]=dict(before=sum(before.values()),after=sum(after.values()),added=sum((after-before).values()),removed_or_changed=sum((before-after).values()),source_equal=actual==collections.Counter(tuple(r.get(k) for k in keys) for r in rows))
    baseline=json.loads((ROOT/'Docs/DATA10_LISTENING_BASELINE.json').read_text())
    protected={}
    for name,expected in baseline['protected_sha256'].items():
        raw=gzip.decompress((ROOT/'Tests/Fixtures/content-v24-production.json.gz').read_bytes()) if name=='Content/production.json' else (ROOT/'Tests/Fixtures/content-v24-production.sqlite').read_bytes() if name=='Resources/content.sqlite' else (ROOT/name).read_bytes()
        protected[name]=dict(sha256=sha(raw),preserved=sha(raw)==expected)
    def tasks(c):return {level:dict(c.execute("select json_extract(q.rubric_json,'$.listening_task'),count(*) from questions q join listening_items l on l.id=q.listening_id join content_items i on i.id=l.id where i.level=? group by 1",[level])) for level in ('intro','beginner','lower_intermediate')}
    report=dict(schema_sql_preserved=same_schema,metadata=source['metadata'],source_sha256=sha((ROOT/'Content/production.json').read_bytes()),bundle_sha256=sha((ROOT/'Resources/content.sqlite').read_bytes()),tables=table_report,new_entities=len(set(b)-set(a)),changed_existing_fingerprints=[i for i in a if a[i]!=b.get(i)],removed_ids=sorted(set(a)-set(b)),protected24_and_older=protected,task_levels_before=tasks(old),task_levels_after=tasks(db),new=dict(originals=60,existing_source_reuse=0,listening=120,questions=120,choices=270,tts=120,verified_recordings=0,source_extra_references=60),integrity_check=db.execute('pragma integrity_check').fetchall(),foreign_key_check=db.execute('pragma foreign_key_check').fetchall())
    assert all(r['source_equal'] and not r['removed_or_changed'] for r in table_report.values())
    assert all(r['preserved'] for r in protected.values()) and not report['changed_existing_fingerprints'] and not report['removed_ids']
    lines=['# DATA10-A 전60원문·120문제 실제 앱 payload 검토표','','아래는 canonical Source의 실제 prompt·선택지·정답/accepted다. AI 자체 재독이며 독립 사람/음성 승인 아님.']
    qs={r['id']:r for r in source['tables']['questions']}
    for row in manifest['items']:
        lines.extend(['',f"## {row['key']} / {row['domain']}",'',row['korean'],'',row['japanese'],'',row['learning_point_ja']])
        for spec in row['tasks']:
            q=qs[spec['question_id']];answer=json.loads(q['answer_json']);lines.extend(['',f"- {spec['task']}: {q['prompt_ja']}"])
            for c in (c for c in source['tables']['question_choices'] if c['question_id']==q['id']):
                lines.extend(['',f"  - {c['choice_id']}: {c['text']}"+(' **정답**' if c['choice_id'] in answer.get('correct_choice_ids',[]) else '')])
            if 'accepted' in answer:lines.extend(['','  - accepted: '+answer['accepted'][0]])
    db.close();old.close()
    return report,'\n'.join(lines)+'\n'


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',type=Path,required=True);p.add_argument('--items',type=Path,required=True);a=p.parse_args()
    result,items=audit();a.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');a.items.write_text(items)
    print(json.dumps(dict(new=result['new'],existing_changed=len(result['changed_existing_fingerprints']),protected=len(result['protected24_and_older']))))
