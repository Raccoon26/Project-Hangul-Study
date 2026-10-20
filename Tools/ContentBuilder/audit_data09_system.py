"""DATA09-7 extends the existing exhaustive SQL route audit, without native claims."""
import argparse
import hashlib
import json
import platform
import sqlite3
import subprocess
from pathlib import Path
from audit_data08_system import run as routes
from audit_data09_final import audit,registries
from build_content import ROOT
from test_data05_content import query

BASELINE='fcb7897b8bf78ce138e1941d9e678d9c22128aed'


def run():
    r=routes();r['baseline_commit']=BASELINE
    r['original_specification_limit']='No complete original DEV01–14/DATA01–07 task specifications located in current tracked paths; archived reports are not full original specifications. DATA08/09 recorded requests and audit documents provide verifiable narrower contracts.'
    r['environment']=dict(platform=platform.platform(),python=platform.python_version(),sqlite=sqlite3.sqlite_version)
    source=json.loads((ROOT/'Content/production.json').read_text())
    r['data09_contracts']=audit(source);assert r['data09_contracts']['validation']['error_count']==0
    r['source_rows']=sum(map(len,source['tables'].values()))
    r['production_bytes_unchanged_from_baseline']={}
    for p in ('Content/production.json','Resources/content.sqlite'):
        before=subprocess.run(['git','show',f'{BASELINE}:{p}'],cwd=ROOT,check=True,capture_output=True).stdout
        assert before==(ROOT/p).read_bytes()
        r['production_bytes_unchanged_from_baseline'][p]=hashlib.sha256(before).hexdigest()
    r['monetization_and_preferences_unchanged_from_baseline']={}
    for p in ('Services/PurchaseService.swift','Services/AdService.swift','Models/MonetizationPolicy.swift','Services/LearningPreferences.swift'):
        before=subprocess.run(['git','show',f'{BASELINE}:{p}'],cwd=ROOT,check=True,capture_output=True).stdout
        assert before==(ROOT/p).read_bytes()
        r['monetization_and_preferences_unchanged_from_baseline'][p]=hashlib.sha256(before).hexdigest()
    c=sqlite3.connect((ROOT/'Resources/content.sqlite').as_uri()+'?mode=ro',uri=True)
    ids={g['id'] for g in registries()};allg={i for i, in c.execute('select id from grammar')};edges={g:[] for g in allg}
    forward=[];orders={g:(lesson,position) for g,lesson,position in c.execute('select g.id,l.ordinal,li.ordinal from grammar g join lesson_items li on li.content_id=g.id join lessons l on l.id=li.lesson_id')}
    for a,b in c.execute("select l.source_id,l.target_id from content_links l join grammar g on g.id=l.source_id where relation='prerequisite'"):
        assert b in allg and a!=b;edges[a].append(b)
        if orders[b]>=orders[a]:forward.append(dict(grammar_id=a,prerequisite_id=b,curriculum_order=orders[a],prerequisite_order=orders[b]))
    visited=set()
    def visit(g,path):
        assert g not in path,(g,path)
        if g in visited:return
        for p in edges[g]:visit(p,path|{g})
        visited.add(g)
    for g in allg:visit(g,set())
    searches=0
    for gid,pattern,meaning in c.execute('select id,pattern,meaning_ja from grammar'):
        for term in (pattern,meaning):
            found=set();offset=0
            while True:
                page=c.execute(query('SQLiteLookup','WITH terms'),[term.lower()]*3+[offset]).fetchall();found.update(page)
                if len(page)<30:break
                offset+=30
            assert (gid,'grammar') in found;searches+=1
    r['grammar_search_queries']=searches
    r['prerequisites']=dict(nodes=len(allg),edges=sum(map(len,edges.values())),acyclic=True,forward_or_same_order=forward,policy='Optional explanation previews support forward references without rewriting lesson/session order. Not evidence all incidental grammar is mastered; previous163 audit remains120 resolved/7 conditional/36 unresolved incl8 level concerns.')
    r['data09_lessons']=len({row[0] for row in c.execute('select lesson_id,content_id from lesson_items') if row[1] in ids})
    r['limits']=dict(native='BLOCKED: no Xcode/Swift/iOS SDK. Definitions are not executed tests.',independent_teacher_review='NOT TESTED',device_offline_audio_accessibility_memory_commute='BLOCKED',ai_language_review='Prior DATA09-5 AI full54/216/216 review preserved; this stage does structural/reference regression, not a fresh human language approval.')
    c.close();return r


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    r=run();a.report.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(coverage=r['coverage'],grammar_search_queries=r['grammar_search_queries'],source_rows=r['source_rows'],native=r['native']),ensure_ascii=False))
