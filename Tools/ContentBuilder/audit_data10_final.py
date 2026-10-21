"""Read-only mechanical DATA10 QA contracts; language/human/audio review is separate."""
import argparse,collections,gzip,hashlib,json,re,sqlite3,subprocess,unicodedata
from pathlib import Path
from build_content import ROOT
from validator import signatures
BASE='f7d1835a8ce1b073a65e8a21d8b27f6e4eb523a9'
sha=lambda b:hashlib.sha256(b).hexdigest()
norm=lambda s:' '.join(unicodedata.normalize('NFC',s).split())
compact=lambda s:''.join(norm(s).split()).rstrip('.!?')
def registries():return [r for b in 'abc' for r in json.loads((ROOT/f'Content/data10-{b}-authoring.json').read_text())['items']]
def block(text,anchor):
    start=text.index(anchor)+len(anchor);depth=1;quoted=False;escape=False
    for n in range(start,len(text)):
        ch=text[n]
        if quoted:
            if escape:escape=False
            elif ch=='\\':escape=True
            elif ch=='"':quoted=False
        elif ch=='"':quoted=True
        elif ch=='{':depth+=1
        elif ch=='}':
            depth-=1
            if depth==0:return text[start:n]
    raise AssertionError('unclosed block '+anchor)
def view_contract(ui,model):
    choice=block(ui,'else if s.revealsChoices {');assert 'ForEach(q.choices)'in choice and 'Text(choice.text)'in choice
    assert ui.count('ForEach(q.choices)')==1
    feedback=block(ui,'else if let result = s.result {')
    for expression in ('Text(q.transcript)','Text(q.translation)','Text(q.explanation)','"正解："+correct.text'):
        assert expression in feedback
        assert expression not in ui.replace(feedback,'')
    policy=block(model,'var revealsChoices: Bool {');assert 'heard && result == nil && current != nil && current?.task != .dictation'in policy
    assert '句点は不要です'not in ui and '文中の句読点は入力してください'in ui and '文末の「.」「!」「?」は省略できます'in ui
    assert 'case .submit' in model and 'guard heard, result == nil' in model
    return dict(status='PASS_STATIC_SOURCE',choices_conditionally_created_after_completed_playback=True,feedback_only_after_result=True,dynamic_ui_voiceover='BLOCKED: no Xcode/device, not executed')
def audit(source_path,bundle_path,rebuilt_path=None):
    src=json.loads(Path(source_path).read_text());t=src['tables'];oldsrc=json.loads(gzip.decompress((ROOT/'Tests/Fixtures/content-v27-production.json.gz').read_bytes()))
    db=sqlite3.connect(Path(bundle_path).resolve().as_uri()+'?mode=ro',uri=True);old=sqlite3.connect(ROOT/'Tests/Fixtures/content-v27-production.sqlite')
    before,after=signatures(old),signatures(db);assert before.keys()==after.keys()
    m=json.loads((ROOT/'Content/data10-final-corrections.json').read_text());owners={p['key'].get('id',p['key'].get('question_id')) for p in m['patches']};changed={i for i in before if before[i]!=after[i]};assert changed==owners
    revised=set(json.loads((ROOT/'Content/data10-final-revised-ids.json').read_text()))
    revisions={i for i, in db.execute('SELECT id FROM content_items') if db.execute('SELECT revision FROM content_items WHERE id=?',[i]).fetchone()!=old.execute('SELECT revision FROM content_items WHERE id=?',[i]).fetchone()};assert revisions==revised
    source_rows={}
    for table,rows in t.items():
        assert len(rows)==len(oldsrc['tables'][table]),table
        keys=sorted(rows[0]) if rows else [r[1] for r in db.execute('PRAGMA table_info('+table+')')]
        assert collections.Counter(db.execute('SELECT '+','.join('"'+k+'"' for k in keys)+' FROM '+table))==collections.Counter(tuple(r.get(k) for k in keys) for r in rows),table
        source_rows[table]=len(rows)
    items=registries();examples={r['id']:r for r in t['examples']};questions={r['id']:r for r in t['questions']};listening={r['id']:r for r in t['listening_items']};choices=collections.defaultdict(list)
    for r in t['question_choices']:choices[r['question_id']].append(r)
    seen=set();tasks=collections.Counter();positions=collections.Counter();accepted=0;old24=sqlite3.connect(ROOT/'Tests/Fixtures/content-v24-production.sqlite');prior={compact(k) for k, in old24.execute('SELECT korean FROM examples')};lines=['# DATA10 QA / actual180 scripts and360 questions','', 'Mechanical payload export, separately AI reread. Independent human/audio NOT TESTED.']
    for r in items:
        e=examples[r['example_id']];key=compact(e['korean']);assert key not in seen and key not in prior;seen.add(key)
        lines+=['',r['key']+' / '+r['domain'],e['korean'],e['japanese'],e['learning_point_ja']]
        for s in r['tasks']:
            l=listening[s['listening_id']];q=questions[s['question_id']];a=json.loads(q['answer_json']);task=json.loads(q['rubric_json'])['listening_task'];tasks[task]+=1
            assert l['source_example_id']==e['id'] and q['listening_id']==l['id'] and q['prompt_ko']is None and l['audio_mode']=='tts' and l['audio_asset_id']is None and l['transcript_ko']is None
            lines+=[task+': '+q['prompt_ja']]
            if task=='dictation':
                assert a==dict(accepted=[e['korean']]) and '数字もハングルで'in q['prompt_ja'];accepted+=len(a['accepted']);lines+=['accepted: '+e['korean']]
            else:
                cc=sorted(choices[q['id']],key=lambda x:x['ordinal']);assert len(cc)==3 and len({norm(x['text'])for x in cc})==3 and len(a['correct_choice_ids'])==1
                cid=a['correct_choice_ids'][0];gold=next(x['text']for x in cc if x['choice_id']==cid);positions[(task,cid)]+=1
                if task=='meaning':assert gold==e['japanese']
                if task=='korean':assert gold==e['korean']
                lines+=[' / '.join(('*'if x['choice_id']==cid else'')+x['text']for x in cc),q['explanation_ja']]
    assert len(seen)==180 and sum(tasks.values())==360 and accepted==150
    # Released old1936 content stays byte-for-byte as SQL rows and stable fingerprints.
    old_lids={i for i, in old24.execute('SELECT id FROM listening_items')};old_qids={i for i, in old24.execute('SELECT id FROM questions WHERE listening_id IS NOT NULL')};old_eids={i for i, in old24.execute('SELECT source_example_id FROM listening_items')};assert not (old_lids|old_qids|old_eids)&revised
    protected={}
    for name in subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--','Content','Resources','Tests/Fixtures'],cwd=ROOT,text=True).splitlines():
        expected=subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
        actual=gzip.decompress((ROOT/'Tests/Fixtures/content-v27-production.json.gz').read_bytes()) if name=='Content/production.json' else (ROOT/'Tests/Fixtures/content-v27-production.sqlite').read_bytes() if name=='Resources/content.sqlite' else (ROOT/name).read_bytes()
        assert expected==actual,name;protected[name]=sha(actual)
    schema='SELECT type,name,tbl_name,sql FROM sqlite_master ORDER BY type,name';assert db.execute(schema).fetchall()==old.execute(schema).fetchall()
    reconstruction=None
    if rebuilt_path:
        c=sqlite3.connect(rebuilt_path);names=[r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")];equal={n:collections.Counter(db.execute('SELECT * FROM '+n))==collections.Counter(c.execute('SELECT * FROM '+n))for n in names};reconstruction=dict(tables=equal,all_tables_equal=all(equal.values()),schema_equal=db.execute(schema).fetchall()==c.execute(schema).fetchall(),byte_equal=Path(bundle_path).read_bytes()==Path(rebuilt_path).read_bytes());assert all(reconstruction[k]for k in ('all_tables_equal','schema_equal','byte_equal'));c.close()
    report=dict(scope='Mechanical full-corpus QA; language AI and independent humans are separate',metadata=src['metadata'],source_sha256=sha(Path(source_path).read_bytes()),bundle_sha256=sha(Path(bundle_path).read_bytes()),source_rows=source_rows,total_source_rows=sum(source_rows.values()),entities=len(after),new_entities=0,deleted_entities=0,patch_fields=len(m['patches']),changed_payload_ids=sorted(changed),revised_ids=sorted(revised),dependent_revision_only=sorted(revised-changed),cohort=dict(originals=180,listening=360,questions=360,choices=sum(len(choices[s['question_id']])for r in items for s in r['tasks']),accepted=150,tasks=dict(tasks)),old1936_unchanged=True,protected_files=protected,integrity=db.execute('PRAGMA integrity_check').fetchall(),foreign_keys=db.execute('PRAGMA foreign_key_check').fetchall(),levels={table:dict(db.execute('SELECT i.level,COUNT(*) FROM '+table+' t JOIN content_items i ON i.id=t.id GROUP BY i.level'))for table in ('vocabulary','examples','grammar','questions','listening_items')},view_contract=view_contract((ROOT/'Views/ListeningView.swift').read_text(),(ROOT/'Models/ListeningModels.swift').read_text()),reconstruction=reconstruction,verified_recordings=0,independent_human_review='NOT TESTED',actual_tts_audition='NOT TESTED')
    assert report['integrity']==[('ok',)]and not report['foreign_keys'];db.close();old.close();old24.close();return report,'\n'.join(lines)+'\n'
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,default=ROOT/'Content/production.json');p.add_argument('--bundle',type=Path,default=ROOT/'Resources/content.sqlite');p.add_argument('--rebuilt',type=Path);p.add_argument('--report',type=Path,required=True);p.add_argument('--items',type=Path,required=True);a=p.parse_args();r,lines=audit(a.source,a.bundle,a.rebuilt);a.report.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');a.items.write_text(lines);print(json.dumps(dict(cohort=r['cohort'],patch_fields=r['patch_fields'],payload_ids=len(r['changed_payload_ids']),revised_ids=len(r['revised_ids']),protected=len(r['protected_files']))))
