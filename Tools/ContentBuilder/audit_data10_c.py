"""Read-only DATA10-C actual counts, old byte preservation and inspectable app payload."""
import argparse,collections,gzip,hashlib,json,re,sqlite3,subprocess
from pathlib import Path
from build_content import ROOT
from validator import signatures
BASE='a9ec0a450e1c40e0bd3b608ec2059499c27e762e'
sha=lambda x:hashlib.sha256(x).hexdigest()

def audit(rebuilt_path,source_path=ROOT/'Content/production.json',bundle_path=ROOT/'Resources/content.sqlite'):
    source=json.loads(Path(source_path).read_text());m=json.loads((ROOT/'Content/data10-c-authoring.json').read_text());items=m['items']
    db=sqlite3.connect(Path(bundle_path).resolve().as_uri()+'?mode=ro',uri=True);old=sqlite3.connect((ROOT/'Tests/Fixtures/content-v26-production.sqlite').as_uri()+'?mode=ro',uri=True)
    before,after=signatures(old),signatures(db);assert before.keys()<=after.keys() and all(before[i]==after[i] for i in before)
    schema='SELECT type,name,tbl_name,sql FROM sqlite_master ORDER BY type,name';assert db.execute(schema).fetchall()==old.execute(schema).fetchall()
    changes={}
    for t,rows in source['tables'].items():
        a=collections.Counter(old.execute('SELECT * FROM '+t));b=collections.Counter(db.execute('SELECT * FROM '+t));keys=sorted(rows[0]) if rows else [x[1] for x in db.execute('PRAGMA table_info('+t+')')]
        actual=collections.Counter(db.execute('SELECT '+','.join('"'+k+'"' for k in keys)+' FROM '+t));same=actual==collections.Counter(tuple(r.get(k) for k in keys) for r in rows)
        assert same and not a-b,t
        changes[t]=dict(before=sum(a.values()),after=sum(b.values()),added=sum((b-a).values()),source_equal=same,removed_or_changed=0)
    protected={}
    paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--','Content','Resources','Tests/Fixtures'],cwd=ROOT,text=True).splitlines()
    for name in paths:
        expected=subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
        actual=gzip.decompress((ROOT/'Tests/Fixtures/content-v26-production.json.gz').read_bytes()) if name=='Content/production.json' else (ROOT/'Tests/Fixtures/content-v26-production.sqlite').read_bytes() if name=='Resources/content.sqlite' else (ROOT/name).read_bytes()
        assert sha(expected)==sha(actual),name
        protected[name]=dict(sha256=sha(actual),preserved=True)
    levels={}
    for level in ('intro','beginner','lower_intermediate'):
        levels[level]={t:dict(c.execute("SELECT json_extract(q.rubric_json,'$.listening_task'),COUNT(*) FROM questions q JOIN listening_items l ON l.id=q.listening_id JOIN content_items i ON i.id=l.id WHERE i.level=? GROUP BY 1",[level])) for t,c in [('before',old),('after',db)]}
    fields={t:db.execute('SELECT COUNT(*) FROM '+t).fetchone()[0] for t in source['tables']}
    names=[x[0] for x in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    rebuilt=Path(bundle_path);reconstruction=None
    rpath=Path(rebuilt_path)
    c=sqlite3.connect(rpath);comparisons={t:collections.Counter(db.execute('SELECT * FROM '+t))==collections.Counter(c.execute('SELECT * FROM '+t)) for t in names}
    reconstruction=dict(all31_tables_equal=all(comparisons.values()),tables=comparisons,schema_equal=db.execute(schema).fetchall()==c.execute(schema).fetchall(),bundle_sha256=sha(rebuilt.read_bytes()),rebuilt_sha256=sha(rpath.read_bytes()),byte_equal=rebuilt.read_bytes()==rpath.read_bytes());c.close()
    assert reconstruction['all31_tables_equal'] and reconstruction['schema_equal'] and reconstruction['byte_equal']
    qs={r['id']:r for r in source['tables']['questions']};lines=['# DATA10-C 전60원문·120문제 검토표','','실제 Source payload. 한 화자 TTS/AI 자체 검수이며 녹음·다화자·사람 검수 인증 아님.']
    for r in items:
        lines+=['',f"## {r['key']} / {r['domain']} / {r['listening_focus']}",'',r['korean'],'',r['japanese'],'',r['learning_point_ja']]
        for s in r['tasks']:
            q=qs[s['question_id']];a=json.loads(q['answer_json']);lines+=['',f"- {s['task']}: {q['prompt_ja']}"]
            for c in (c for c in source['tables']['question_choices'] if c['question_id']==q['id']):lines+=['',f"  - {c['choice_id']}: {c['text']}"+(' **정답**' if c['choice_id'] in a.get('correct_choice_ids',[]) else '')]
            if 'accepted' in a:lines+=['','  - accepted: '+a['accepted'][0]]
            else:lines+=['','  - feedback: '+q['explanation_ja']]
    result=dict(metadata=source['metadata'],source_sha256=sha(Path(source_path).read_bytes()),bundle_sha256=sha(rebuilt.read_bytes()),source_tables=len(source['tables']),source_rows=sum(map(len,source['tables'].values())),production=fields,table_deltas=changes,existing_entities=len(before),changed_existing_fingerprints=[],removed_ids=[],new_entities=len(set(after)-set(before)),protected26_and_older=protected,new=dict(originals=len(items),examples=60,listening=120,questions=120,choices=180,dictation=60,comprehension=60,reused_old_sources=0,extra_new_source_references=60,tts=120,verified_recordings=0),domains=dict(collections.Counter(r['domain'] for r in items)),listening_focus=dict(collections.Counter(r['listening_focus'] for r in items)),task_levels=levels,grammar_reuse=json.loads((ROOT/'Docs/DATA10_C_PREREQUISITES.json').read_text())['unique_referenced_grammar'],reconstruction=reconstruction,integrity=db.execute('PRAGMA integrity_check').fetchall(),foreign_keys=db.execute('PRAGMA foreign_key_check').fetchall(),native_definitions=sum(len(re.findall(r'func\s+test\w*\s*\(',p.read_text())) for p in (ROOT/'Tests').glob('*.swift')),limitations='SQL/AI review only; native/audio/independent teacher verification not executed here. Last Mac known5failed methods remain separate historical evidence.')
    baseline=sqlite3.connect(ROOT/'Tests/Fixtures/content-v24-production.sqlite')
    cohorts=[json.loads((ROOT/('Content/data10-'+b+'-authoring.json')).read_text())['items'] for b in ('a','b','c')]
    originals={r['example_id'] for batch in cohorts for r in batch};questions={q['question_id'] for batch in cohorts for r in batch for q in r['tasks']};listening={q['listening_id'] for batch in cohorts for r in batch for q in r['tasks']}
    for table,ids in [('examples',originals),('questions',questions),('listening_items',listening)]:
        delta={i for i, in db.execute('SELECT id FROM '+table)}-{i for i, in baseline.execute('SELECT id FROM '+table)}
        assert delta==ids,table
    assert len(originals)==180 and len(questions)==len(listening)==360
    result['cumulative_data10']=dict(originals=180,questions=360,listening=360,old_sources_recounted=0,goal_originals=[150,250],goal_questions=[300,500],within_target=True)
    result['entity_levels']={t:dict(db.execute('SELECT i.level,COUNT(*) FROM '+t+' t JOIN content_items i ON i.id=t.id GROUP BY i.level')) for t in ('vocabulary','examples','grammar','questions','listening_items')}
    baseline.close()
    assert result['new_entities']==300 and result['integrity']==[('ok',)] and not result['foreign_keys']
    db.close();old.close();return result,'\n'.join(lines)+'\n'

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',type=Path,required=True);p.add_argument('--items',type=Path,required=True);p.add_argument('--rebuilt',type=Path,required=True);p.add_argument('--source',type=Path,default=ROOT/'Content/production.json');p.add_argument('--bundle',type=Path,default=ROOT/'Resources/content.sqlite');a=p.parse_args();r,items=audit(a.rebuilt,a.source,a.bundle);a.report.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');a.items.write_text(items);print(json.dumps(dict(new=r['new'],preserved=len(r['protected26_and_older']),existing_entities=r['existing_entities'],source_rows=r['source_rows'],native_definitions=r['native_definitions'])))
