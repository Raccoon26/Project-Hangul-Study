#!/usr/bin/env python3
"""Reproducible synthetic benchmark using the Swift repository's SQL, not iOS timings."""
import argparse, json, math, platform, re, resource, sqlite3, statistics, time
from pathlib import Path
from build_content import ROOT, build
from generate_synthetic import generate, synthetic_id
from validator import LEVELS

def run(directory,count=15000):
    directory=Path(directory); started=time.perf_counter()
    source=generate(directory/'source',count)
    generation=time.perf_counter()-started
    result=build(source,directory/'synthetic.sqlite')
    db=sqlite3.connect(Path(result['path']).as_uri()+'?mode=ro',uri=True)
    raw=(ROOT/'Repositories/SQLiteContentRepository.swift').read_text()
    queries=re.findall(r'"""(.*?)"""',raw,re.S)
    base=queries[0]
    def clause(prefix):
        return next(s for s in re.findall(r'sql \+= "([^"]+)"',raw) if s.startswith(prefix))
    order=clause(' ORDER BY')
    cases={
      'word_by_id':('SELECT headword FROM vocabulary WHERE id=?',[synthetic_id('vocabulary',count//2)]),
      'first_page_50':(base+order,[50]),
      'level_page_50':(base+clause(' AND i.level=')+order,['intro',50]),
      'korean_prefix_50':(base+clause(' AND v.id IN')+order,['__synthetic__단어000','__synthetic__단어000'+chr(0x10ffff),50]),
      'japanese_prefix_50':(base+clause(' AND v.id IN')+order,['__synthetic__意味000','__synthetic__意味000'+chr(0x10ffff),50]),
      'example_relationship':(queries[1],[synthetic_id('vocabulary',count//2)])}
    metrics={}
    for name,(sql,values) in cases.items():
        durations=[]
        for _ in range(30):
            start=time.perf_counter(); rows=db.execute(sql,values).fetchall(); durations.append((time.perf_counter()-start)*1000)
        assert rows,name
        metrics[name]=dict(median_ms=round(statistics.median(durations),4),p95_ms=round(sorted(durations)[math.ceil(.95*len(durations))-1],4),rows=len(rows),plan=[r[3] for r in db.execute('EXPLAIN QUERY PLAN '+sql,values)])
    seen=set(); cursor=None; start=time.perf_counter()
    while True:
        sql=base; values=[]
        if cursor:
            sql+=clause(' AND (v.sort_key>'); values=[cursor[0],cursor[0],cursor[1]]
        page=db.execute(sql+order,values+[100]).fetchall()
        if not page: break
        for row in page:
            assert row[0] not in seen; seen.add(row[0])
        cursor=(page[-1][3],page[-1][0])
    assert len(seen)==count
    assert db.execute('SELECT COUNT(*) FROM examples').fetchone()[0]==count*2
    assert db.execute('PRAGMA foreign_key_check').fetchall()==[]
    db.close()
    rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return dict(environment=dict(platform=platform.platform(),python=platform.python_version(),sqlite=sqlite3.sqlite_version),
                note='Synthetic development data only. Linux/Python SQLite measurements are not iPhone startup or UI benchmarks.',
                vocabulary=count,examples=count*2,generation_seconds=round(generation,4),build_seconds=result['seconds'],
                db_bytes=Path(result['path']).stat().st_size,peak_process_rss_mib=round(rss/(1024*1024 if platform.system()=='Darwin' else 1024),2),
                full_pagination_seconds=round(time.perf_counter()-start,4),pagination_unique_ids=len(seen),queries=metrics,validation=result['validation'])
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('directory'); p.add_argument('--count',type=int,default=15000); p.add_argument('--report',type=Path,required=True)
    a=p.parse_args(); result=run(a.directory,a.count)
    a.report.parent.mkdir(parents=True,exist_ok=True); a.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))
