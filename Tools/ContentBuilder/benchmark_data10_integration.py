"""Re-run Cloud SQL timing from the project root; not device/UI performance."""
import json,sqlite3,time,statistics,sys,platform,socket,tempfile
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,'Tools/ContentBuilder')
from test_data05_content import query
from test_lookup_sql import user
m=json.loads(Path('Content/data10-integration-ids.json').read_text());r={'scope':'Cloud Python/SQLite warm queries, not Swift/UI/device startup, RSS or real 3-10 minute timing','repeats':40,'samples':{},'python':sys.version,'sqlite':sqlite3.sqlite_version,'platform':platform.platform(),'compile_options':[x[0]for x in sqlite3.connect(':memory:').execute('pragma compile_options')]}
with tempfile.TemporaryDirectory()as d, patch.object(socket,'socket',side_effect=AssertionError('network forbidden')):
 u=user(Path(d)/'user.sqlite',10);new=sqlite3.connect('Resources/content.sqlite');old=sqlite3.connect('Tests/Fixtures/content-v28-production.sqlite');lesson=m['courses'][0]['lessons'][0];ids=lesson['listening_ids'];scope='lesson:lower_intermediate:'+lesson['id'];u.execute(query('SQLiteListening','INSERT INTO listening_sessions'),['s',scope,json.dumps(dict(updatedAt=100,revision=0,contentVersion=29)),0])
 for c in m['courses']:
  for l in c['lessons']:
   for lid in l['listening_ids']:u.execute("INSERT INTO srs_state VALUES(?,'listening','calendar_steps',1,'{\"stage\":3}',100,0,0)",[lid])
 u.commit()
 def bench(name,fn):
  result=fn();times=[]
  for _ in range(40):
   start=time.perf_counter();fn();times.append((time.perf_counter()-start)*1000)
  r['samples'][name]=dict(p50_ms=round(statistics.median(times),4),p95_ms=round(sorted(times)[37],4),max_ms=round(max(times),4),rows=len(result))
 for version,c in [(28,old),(29,new)]:
  bench(f'v{version}_search_의견',lambda:c.execute(query('SQLiteLookup','WITH terms'),['의견']*3+[0]).fetchall())
  bench(f'v{version}_catalog_batch103',lambda:c.execute(query('SQLiteListening','SELECT l.id FROM listening_items'),['lower_intermediate',2060,2080]).fetchall())
  bench(f'v{version}_curriculum_listening_page',lambda:c.execute(query('SQLiteCurriculum','SELECT id FROM content_items'),['lower_intermediate','listening','','listening']).fetchall())
 bench('v29_typed_courses',lambda:new.execute(query('SQLiteListening','SELECT c.* FROM courses'),['lower_intermediate']).fetchall())
 bench('v29_lesson_five_ids',lambda:new.execute(query('SQLiteListening','SELECT a.id FROM lesson_items'),[lesson['id']]).fetchall())
 qsql=query('SQLiteListening','SELECT q.*,l.id')+' AND l.id IN ('+','.join('?'for _ in ids)+') ORDER BY l.learning_order,l.id LIMIT 20'
 bench('v29_session_five_question_rows',lambda:new.execute(qsql,ids).fetchall())
 bench('home_summary_user360_due',lambda:u.execute(query('SQLiteProgressRepository','SELECT COALESCE(SUM(study_count)'),[200]).fetchall())
 bench('srs_due_page20_user360',lambda:u.execute(query('SQLiteListening','SELECT content_id FROM srs_state'),['calendar_steps',1,200]).fetchall())
 bench('resume_lesson_snapshot',lambda:u.execute(query('SQLiteCurriculum','SELECT kind,target,level FROM')).fetchall())
 bench('statistics',lambda:u.execute(query('SQLiteStatistics','SELECT COUNT(CASE'),[0,200]).fetchall())
 bench('maintenance',lambda:u.execute(query('SQLiteStatistics','SELECT p.content_id FROM item_progress'),[200,10]).fetchall())
 r['bundle_bytes']={str(v):Path(p).stat().st_size for v,p in [(28,'Tests/Fixtures/content-v28-production.sqlite'),(29,'Resources/content.sqlite')]};new.close();old.close();u.close()
Path('Docs/DATA10_INTEGRATION_PERFORMANCE.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r['samples'],ensure_ascii=False))
