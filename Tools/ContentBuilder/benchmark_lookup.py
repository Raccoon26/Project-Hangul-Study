#!/usr/bin/env python3
"""DEV11 search benchmark. All synthetic files live in a temporary directory."""
import json,sqlite3,tempfile,time,uuid,statistics
from pathlib import Path
from build_content import ROOT,build
from generate_synthetic import generate
from test_data05_content import query

def measure(db,terms):
 sql=query('SQLiteLookup','WITH terms');out={}
 for term in terms:
  times=[];rows=[]
  for _ in range(10):
   t=time.perf_counter();rows=db.execute(sql,[term,term,term,0]).fetchall();times.append((time.perf_counter()-t)*1000)
  out[term]={'median_ms':round(statistics.median(times),3),'max_ms':round(max(times),3),'returned':len(rows)}
 return out
if __name__=='__main__':
 report={'environment':'Linux Python sqlite3; SQL only, not iPhone latency','query':'same ranked literal substring query used by SQLiteLookup; 30 result limit'}
 with sqlite3.connect(ROOT/'Resources/content.sqlite') as d:
  report['production']=measure(d,['학교','学校','고 싶다','したい','る','nomatch123'])
 with tempfile.TemporaryDirectory() as tmp:
  t=time.perf_counter();root=Path(tmp);r=build(generate(root/'source',15000),root/'synthetic.sqlite')
  assert r['validation']['error_count']==0
  d=sqlite3.connect(root/'synthetic.sqlite')
  # Expand fixture grammar to500; no production files are written.
  columns=[r[1]for r in d.execute('pragma table_info(grammar)')];template=list(d.execute('SELECT * FROM grammar LIMIT 1').fetchone())
  item=list(d.execute("SELECT * FROM content_items WHERE kind='grammar' LIMIT 1").fetchone())
  for n in range(450):
   id=str(uuid.uuid4());gi=item.copy();gi[0]=id;d.execute('INSERT INTO content_items VALUES('+','.join('?'for _ in gi)+')',gi)
   row=template.copy();row[columns.index('id')]=id;row[columns.index('pattern')]='__SYNTHETIC__追加文法'+str(n)
   d.execute('INSERT INTO grammar VALUES('+','.join('?'for _ in row)+')',row)
  d.commit();assert d.execute('PRAGMA foreign_key_check').fetchall()==[]
  report['synthetic_counts']={t:d.execute('SELECT COUNT(*) FROM '+t).fetchone()[0] for t in ['vocabulary','examples','grammar']}
  report['synthetic_build_seconds']=round(time.perf_counter()-t,3)
  report['synthetic']=measure(d,['__synthetic__단어014999','__synthetic__意味014999','意味','文法','nomatch123'])
  d.close()
 print(json.dumps(report,ensure_ascii=False,indent=2))
