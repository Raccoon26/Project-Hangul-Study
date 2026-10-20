"""DATA09-8 read-only release closeout: rebuilt tables/schema/SHA, archives, IDs and Git sizes.
No native execution or independent language review is certified by this tool.
"""
import argparse
import collections
import hashlib
import json
import re
import sqlite3
import subprocess
from pathlib import Path
from audit_data08_closeout import ROOT,LEVELS,sha,load,connect,count,git
from audit_data09_final import registries

BASELINE='542816ccf1a8ce25a8a4865cbd8f2a7fcb73c03e'


def run(args):
    checks=[]
    def check(name,ok):checks.append(dict(check=name,status='PASS' if ok else 'FAIL'))
    source=load(ROOT/'Content/production.json');build=load(args.build_report);routing=load(args.routing)
    bundle=ROOT/'Resources/content.sqlite';db=connect(bundle);rebuilt=connect(args.rebuilt)
    tables=lambda c:[r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    names=tables(db);same_names=names==tables(rebuilt);check('All table names including derived tables',same_names)
    comparisons={}
    for t in names:
        a=collections.Counter(db.execute(f'SELECT * FROM "{t}"'));b=collections.Counter(rebuilt.execute(f'SELECT * FROM "{t}"')) if same_names else {}
        comparisons[t]=dict(rows=sum(a.values()),equal=a==b);check('All columns and duplicate multiplicities: '+t,a==b)
        for pragma in ('table_xinfo','foreign_key_list','index_list'):
            check(pragma+': '+t,list(db.execute(f'PRAGMA {pragma}("{t}")'))==list(rebuilt.execute(f'PRAGMA {pragma}("{t}")')))
    schema='SELECT type,name,tbl_name,sql FROM sqlite_master ORDER BY type,name'
    schema_equal=list(db.execute(schema))==list(rebuilt.execute(schema));check('Complete schema/index/trigger SQL',schema_equal)
    integrity={}
    for name,c in [('bundle',db),('rebuilt',rebuilt)]:
        integrity[name]=dict(integrity_check=c.execute('PRAGMA integrity_check').fetchall(),foreign_key_check=c.execute('PRAGMA foreign_key_check').fetchall())
        check(name+' integrity/FK',integrity[name]==dict(integrity_check=[('ok',)],foreign_key_check=[]))
    bundle_sha,rebuilt_sha=sha(bundle),sha(args.rebuilt);binary_equal=bundle_sha==rebuilt_sha==build['sha256']
    check('Byte-exact SHA including Importer report',binary_equal)
    mismatch=None if binary_equal else dict(status='FAIL',logical_rows_equal=all(c['equal'] for c in comparisons.values()),schema_equal=schema_equal,current_sqlite=sqlite3.sqlite_version,investigation='SHA mismatch requires separate investigation; see row/schema comparisons. Do not replace bundle or certify binary reconstruction.')
    check('Strict previous23 Validator errors0/warnings10',build['validation']['error_count']==0 and build['validation']['warning_count']==10)
    check('Current routing and DATA09 contracts errors0',routing['structural']['validation']['error_count']==0 and routing['data09_contracts']['validation']['error_count']==0)
    check('No inaccessible questions/examples',routing['coverage']['unrouted_questions']==routing['coverage']['unreachable_examples']==0)
    counts={t:count(db,t) for t in names};batches={};allg=set();alle=set();allq=set()
    for b in 'abc':
        registry=load(ROOT/f'Content/data09-{b}-ids.json')['grammar']
        g={r['id'] for r in registry};e={i for r in registry for i in r['example_ids']};q={i for r in registry for i in r['question_ids']}
        check('Batch '+b+' new disjoint IDs',not(g&allg or e&alle or q&allq))
        check('Batch '+b+' 18/72/72 present',len(g)==18 and len(e)==len(q)==72 and all(db.execute('SELECT 1 FROM content_items WHERE id=? AND is_active=1',[i]).fetchone() for i in g|e|q))
        allg|=g;alle|=e;allq|=q;batches[b.upper()]=dict(grammar=18,fixed_expressions=0,new_unique_examples=72,grammar_questions=72)
    old=connect(ROOT/'Tests/Fixtures/content-v19-production.sqlite')
    for t,ids in [('grammar',allg),('examples',alle),('questions',allq)]:
        before={r[0] for r in old.execute('SELECT id FROM '+t)};after={r[0] for r in db.execute('SELECT id FROM '+t)}
        check('Content19 delta exactly DATA09 '+t,after-before==ids and before<=after)
    check('Unreduced DATA09 targets',45<=len(allg)<=60 and 180<=len(alle)<=300 and 180<=len(allq)<=300)
    for query,title in [('SELECT id,kind,created_at FROM content_items','Stable ID/kind/created_at'),('SELECT id,sort_key FROM vocabulary','vocabulary sort keys'),('SELECT * FROM lesson_items','old lesson membership/order'),('SELECT id,learning_order FROM listening_items','listening order')]:
        check('All Content19 '+title+' preserved',set(old.execute(query))<=set(db.execute(query)))
    for t in ('vocabulary','meanings','listening_items'):
        check('No DATA09 '+t+' additions or deletions',set(old.execute('SELECT id FROM '+t))==set(db.execute('SELECT id FROM '+t)))
    old.close()
    stages=[]
    for stage,v,filename,key in [(1,19,'DATA09_BASELINE',None),(2,20,'DATA09_A_COUNTS','counts'),(3,21,'DATA09_B_COUNTS','production'),(4,22,'DATA09_C_COUNTS','production'),(5,23,'DATA09_FINAL_COUNTS','counts'),(6,24,'DATA09_INTEGRATION_COUNTS','counts'),(7,24,'DATA09_SYSTEM_RESULTS',None)]:
        path=bundle if v==24 else ROOT/f'Tests/Fixtures/content-v{v}-production.sqlite';c=connect(path)
        actual={t:count(c,t) for t in ('grammar','examples','questions','vocabulary','meanings','listening_items')};doc=ROOT/f'Docs/{filename}.json';record=load(doc)
        if key:check(f'Stage{stage} archived counts vs actual{v}',all(record[key][t]==n for t,n in actual.items()))
        elif stage==1:check('Stage1 actual42Grammar',actual['grammar']==42)
        else:check('Stage7 actual counts',all(record['production_counts']['counts'][t]==n for t,n in actual.items()))
        stages.append(dict(stage=stage,content_version=v,actual_counts=actual,evidence=str(doc.relative_to(ROOT)),sha256=sha(doc)));c.close()
    prereq=load(ROOT/'Docs/DATA09_FINAL_PREREQUISITES.json');records=prereq['records']
    statuses=collections.Counter(r['status'] for r in records);check('163 original candidates exactly once',len(records)==163 and len({r['index'] for r in records})==163)
    check('Prior candidate classifications120/7/36 preserved',dict(statuses)==dict(resolved=120,pedagogically_allowable=7,unresolved=36))
    for r in records:
        check('Original prerequisite Example retained '+str(r['index']),db.execute('SELECT korean,japanese FROM examples WHERE id=?',[r['example_id']]).fetchone()==(r['korean'],r['japanese']))
        check('Supporting grammar references '+str(r['index']),all(db.execute('SELECT 1 FROM grammar WHERE id=?',[i]).fetchone() for i in r.get('supporting_grammar_ids',[])))
    levels={}
    for level in LEVELS:
        levels[level]={t:db.execute(f'SELECT COUNT(*) FROM "{t}" t JOIN content_items i ON i.id=t.id WHERE i.level=?',[level]).fetchone()[0] for t in ('vocabulary','meanings','examples','grammar','questions','listening_items','courses','lessons')}
    preserved=[]
    for p in git('ls-files','-z','Content','Resources','Tests/Fixtures').decode().split('\0'):
        if not p:continue
        raw=git('show',BASELINE+':'+p);same=hashlib.sha256(raw).hexdigest()==sha(ROOT/p);check('Protected artifact unchanged: '+p,same)
        preserved.append(dict(path=p,bytes=(ROOT/p).stat().st_size,sha256=sha(ROOT/p)))
    raw=git('rev-list','--objects','--all')
    lines=subprocess.run(['git','-C',str(ROOT),'cat-file','--batch-check=%(objecttype) %(objectname) %(objectsize) %(rest)'],input=raw,capture_output=True,check=True).stdout.decode().splitlines()
    blobs=[]
    for line in lines:
        kind,oid,size,*path=line.split(' ',3)
        if kind=='blob':blobs.append(dict(oid=oid,bytes=int(size),path=path[0] if path else ''))
    sizes=dict(reachable_blob_count=len(blobs),over50MiB=[b for b in blobs if b['bytes']>50*1024**2],over100MiB=[b for b in blobs if b['bytes']>100*1024**2],largest=sorted(blobs,key=lambda b:b['bytes'],reverse=True)[:12])
    check('No GitHub100MiB reachable blob',not sizes['over100MiB'])
    tracked=[]
    for p in git('ls-files','-z').decode().split('\0'):
        if p:tracked.append(dict(path=p,bytes=(ROOT/p).stat().st_size))
    sizes['largest_working_tracked_files']=sorted(tracked,key=lambda b:b['bytes'],reverse=True)[:12]
    native=sum(len(re.findall(r'func\s+test\w*\s*\(',p.read_text())) for p in (ROOT/'Tests').glob('*.swift'))
    result=dict(stage='DATA-09-8',status='PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL',baseline_commit=BASELINE,metadata=source['metadata'],source_sha256=sha(ROOT/'Content/production.json'),bundle_sha256=bundle_sha,rebuilt_sha256=rebuilt_sha,sha_mismatch_investigation=mismatch,reconstruction_tables=comparisons,schema_equal=schema_equal,integrity=integrity,validation=build['validation'],build_seconds=build['seconds'],source_tables=len(source['tables']),source_rows=sum(map(len,source['tables'].values())),counts=counts,levels=levels,batches=batches,data09=dict(grammar=len(allg),fixed_expressions=0,unique_examples=len(alle),grammar_questions=len(allq),vocabulary_expression_delta=0,existing_vocabulary_expressions=db.execute("SELECT COUNT(*) FROM vocabulary WHERE part_of_speech='expression'").fetchone()[0],classification_basis='All54 are productive grammar structures/endings in grammar table, per final Batch reviews; no new fixed vocabulary expressions. Draft pedagogical_type labels are not runtime item counts.'),stages=stages,prerequisites=dict(count=len(records),counts=dict(statuses),prior_evidence_sha256=sha(ROOT/'Docs/DATA09_FINAL_PREREQUISITES.json'),policy=prereq['policy'],current_dag=routing['prerequisites']),preserved_artifacts=preserved,git_sizes=sizes,routing=routing['coverage'],native=dict(status='BLOCKED',definitions=native,executed=0),independent_human_review='NOT TESTED',checks=checks,limitation='Read-only DB/SQL/archives evidence; not Swift/iOS or language certification.')
    db.close();rebuilt.close();return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('rebuilt','build-report','routing','report'):p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();r=run(a);a.report.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(status=r['status'],checks=len(r['checks']),failed=[c for c in r['checks'] if c['status']=='FAIL'],data09=r['data09'],source_sha=r['source_sha256'],bundle_sha=r['bundle_sha256'],rebuilt_sha=r['rebuilt_sha256']),ensure_ascii=False))
    raise SystemExit(0 if r['status']=='PASS' else 1)
