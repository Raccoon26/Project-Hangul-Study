"""Compare v13/current actual repository SQL; Linux DB timings, not app launch."""
import json,sqlite3,statistics,time,re
from build_content import ROOT
from test_data05_content import query

def run(path):
 c=sqlite3.connect(path.as_uri()+'?mode=ro',uri=True)
 code=(ROOT/'Repositories/SQLiteContentRepository.swift').read_text();base=re.findall(r'"""(.*?)"""',code,re.S)[0];parts=re.findall(r'sql \+= "([^"]+)"',code);clause=lambda s:next(p for p in parts if p.startswith(s))
 word=c.execute('SELECT id FROM vocabulary ORDER BY sort_key,id LIMIT 1').fetchone()[0]
 cases={'korean_search':(query('SQLiteLookup','WITH terms'),['학교']*3+[0]),'japanese_search':(query('SQLiteLookup','WITH terms'),['学校']*3+[0]),'broad_search':(query('SQLiteLookup','WITH terms'),['る']*3+[0]),'no_match':(query('SQLiteLookup','WITH terms'),['nomatch123']*3+[0]),'set_first20':(base+clause(' AND i.level=')+clause(' ORDER BY'),['beginner',20]),'card':(query('SQLiteVocabularyContent','SELECT v.headword'),[word]),'examples':(query('SQLiteContentRepository','SELECT DISTINCT e.id'),[word])}
 out={}
 for key,(sql,args)in cases.items():
  ms=[]
  for _ in range(30):
   start=time.perf_counter();rows=c.execute(sql,args).fetchall();ms.append((time.perf_counter()-start)*1000)
  out[key]={'median_ms':round(statistics.median(ms),4),'p95_ms':round(sorted(ms)[28],4),'rows':len(rows),'plan':[r[3]for r in c.execute('EXPLAIN QUERY PLAN '+sql,args)]}
 c.close();return out
if __name__=='__main__':print(json.dumps({'environment':'Linux sqlite3; warm connection; 30 repetitions; no iOS launch/UI measurement','before':run(ROOT/'Tests/Fixtures/content-v13-production.sqlite'),'after':run(ROOT/'Resources/content.sqlite')},ensure_ascii=False,indent=2))
