"""DEV12 bounded SQL statistics benchmark; temporary synthetic user DB only."""
import json,statistics,tempfile,time
from pathlib import Path
from test_lookup_sql import user
from test_data05_content import queries,query
from build_content import ROOT

def run(count=300000):
 with tempfile.TemporaryDirectory() as tmp:
  d=user(Path(tmp)/'progress.sqlite',10);now=1800000000
  rows=((str(i),str(i%15000),1,now-(i%730)*86400,'day','Asia/Tokyo','vocabulary_pass' if i%3 else 'production_present','viewed' if i%3 else 'correct',0,None,13)for i in range(count))
  d.executemany('INSERT INTO study_events VALUES(?,?,?,?,?,?,?,?,?,?,?)',rows);d.commit()
  aggregate=query('SQLiteStatistics','SELECT COUNT(CASE')
  lifetime=next(s for s in queries('SQLiteStatistics')if "AS seen" in s)
  report={'synthetic_events':count,'synthetic_vocabulary_ids':15000,'environment':'Linux SQLite; no iPhone launch/UI timing','queries':{}}
  for label,sql,args in [('today',aggregate,[now-86400,now]),('30_days',aggregate,[now-30*86400,now]),('lifetime',lifetime,[])]:
   elapsed=[]
   for _ in range(10):
    start=time.perf_counter();d.execute(sql,args).fetchall();elapsed.append((time.perf_counter()-start)*1000)
   report['queries'][label]={'median_ms':round(statistics.median(elapsed),3),'max_ms':round(max(elapsed),3),'plan':[r[3]for r in d.execute('EXPLAIN QUERY PLAN '+sql,args)]}
  d.close();return report
if __name__=='__main__':
 result=run();(ROOT/'Docs/PERFORMANCE_DEV12.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
