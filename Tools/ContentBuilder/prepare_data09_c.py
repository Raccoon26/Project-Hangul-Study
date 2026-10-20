"""Reconstruct DATA09-C candidate from immutable21 + reviewed authoring + fixed IDs.

Writes only the explicitly selected candidate; never replaces the bundle or user DB.
UUID allocation is a separate, one-time --allocate-ids action.
"""
import argparse
import datetime
import gzip
import json
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REUSED = {}


def authored():
    units=[]
    for line in (ROOT/'Docs/DATA09_C_AUTHORING.tsv').read_text().splitlines():
        parts=line.split('|');kind=parts.pop(0)
        if kind=='G':
            assert len(parts)==10,parts
            key,pattern,meaning,explanation,form,constraints,note,plan,compare,prereq=parts
            units.append(dict(key=key,pattern=pattern,meaning=meaning,explanation=explanation,form=form,constraints=constraints,note=note,plan=plan,compare=compare.split(', '),prereq=prereq,examples=[],questions=[]))
        elif kind=='E':
            assert len(parts)==3
            units[-1]['examples'].append(dict(zip(('korean','japanese','learning_point_ja'),parts)))
        else:
            assert kind in ('M','F','C','X') and len(parts)==8,(kind,parts)
            prompt,ko,correct,wrong1,wrong2,reason,reason1,reason2=parts
            units[-1]['questions'].append(dict(task={'M':'meaning','F':'form','C':'context','X':'contrast'}[kind],prompt=prompt,korean=ko or None,choices=[correct,wrong1,wrong2],reasons=[reason,reason1,reason2]))
    assert len(units)==18 and len({u['key'] for u in units})==18
    for u in units:
        assert len(u['examples'])==4 and len(u['questions'])==4
        assert [q['task'] for q in u['questions']]==['meaning','form','context','contrast']
    return units


def prepare(args):
    units=authored()
    registry_path=ROOT/'Content/data09-c-ids.json'
    if args.allocate_ids:
        if registry_path.exists():raise ValueError('IDs already allocated; reuse registry')
        new=lambda:str(uuid.uuid4())
        registry=dict(stage='DATA-09-4',batch='C',content_version=22,previous_content_version=21,schema_version=4,created_at=datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z'),course_id=new(),source_id=new(),lesson_ids=[new() for _ in range(6)],grammar=[dict(key=u['key'],id=new(),example_ids=[new() for _ in range(4)],question_ids=[new() for _ in range(4)]) for u in units])
        registry_path.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n')
    registry=json.loads(registry_path.read_text())
    source=json.loads(gzip.decompress((ROOT/'Tests/Fixtures/content-v21-production.json.gz').read_bytes()))
    assert source['metadata']['content_version']==21
    source['metadata']['content_version']=22
    tables=source['tables'];old_ids={r['id'] for r in tables['content_items']};new_ids=[]
    stamp=registry['created_at'];sid=registry['source_id'];links=[];reused=set()
    def entity(item_id,kind):
        assert item_id not in old_ids and item_id not in new_ids
        new_ids.append(item_id)
        tables['content_items'].append(dict(id=item_id,kind=kind,revision=1,is_active=1,level='lower_intermediate',created_at=stamp,updated_at=stamp))
        tables['item_sources'].append(dict(content_id=item_id,source_id=sid,note='本プロジェクトで独自執筆。assistantの韓日再読、独立した人の検収は未実施。'))
    def link(a,b,relation):links.append(dict(source_id=a,target_id=b,relation=relation))
    tables['sources'].append(dict(id=sid,title='HangulStudy DATA09-C：推測・引用・話し手の態度',citation='本プロジェクト独自の文法説明・韓国語例文・日本語訳・単一選択問題。assistantによる編集・再読。独立原語話者/教師の監修、公式難度認定、外部辞書照合は未実施。',url=None,accessed_at=None))
    cid=registry['course_id'];entity(cid,'course')
    tables['courses'].append(dict(id=cid,title_ja='初中級文法・推測と会話の意図',description_ja='推測の根拠、引用の視点、会話での提案・意向・態度を短い単位で学びます。既存の文法学習・復習を使います。',ordinal=max(r['ordinal'] for r in tables['courses'])+1))
    titles=['修飾・名詞化と推測の根拠','可能性・疑問内容・発言の報告','引用内容と依頼・誘いの伝達','質問の伝達と相手への提案','意向・依頼・約束の使い分け','共有の確認・変化の関係・気付き']
    for j,lid in enumerate(registry['lesson_ids']):
        entity(lid,'lesson');tables['lessons'].append(dict(id=lid,course_id=cid,title_ja=titles[j],ordinal=59+j))
    existing={r['pattern']:r['id'] for r in tables['grammar']}
    ids={r['key']:r for r in registry['grammar']}
    assert set(ids)=={u['key'] for u in units}
    all_grammar={**existing,**{u['pattern']:ids[u['key']]['id'] for u in units}}
    for j,u in enumerate(units):
        r=ids[u['key']];gid=r['id'];entity(gid,'grammar')
        tables['grammar'].append(dict(id=gid,pattern=u['pattern'],title_ja=u['meaning'],meaning_ja=u['meaning'],explanation_ja=u['explanation'],form_ko=u['form'],usage_constraints_ja=u['constraints'],confusion_ja=u['note']))
        tables['lesson_items'].append(dict(lesson_id=registry['lesson_ids'][j//3],content_id=gid,ordinal=j%3))
        for eid,example in zip(r['example_ids'],u['examples']):
            entity(eid,'example');tables['examples'].append(dict(id=eid,**example));tables['grammar_examples'].append(dict(grammar_id=gid,example_id=eid))
        reuse=REUSED.get(u['key'])
        if reuse:
            assert reuse in old_ids
            tables['grammar_examples'].append(dict(grammar_id=gid,example_id=reuse));reused.add(reuse)
        for qn,(qid,q) in enumerate(zip(r['question_ids'],u['questions'])):
            entity(qid,'question');correct_position=(j+qn)%3
            order=[1,2];order.insert(correct_position,0)
            choices=[dict(question_id=qid,choice_id=chr(97+n),ordinal=n,text=q['choices'][v]) for n,v in enumerate(order)]
            answer=dict(correct_choice_ids=[chr(97+correct_position)])
            rationale=' '.join('「'+q['choices'][v]+'」：'+q['reasons'][v] for v in order)
            tables['questions'].append(dict(id=qid,question_type='multiple_choice',direction='ko_ko' if q['task']=='form' else 'ko_ja',answer_schema_version=1,prompt_ja=q['prompt'],prompt_ko=q['korean'],explanation_ja=rationale,answer_json=json.dumps(answer,ensure_ascii=False),rubric_json=json.dumps(dict(grammar_task=q['task']),ensure_ascii=False)))
            tables['question_choices'].extend(choices);link(qid,gid,'question_target')
        for pattern in u['compare']:link(gid,all_grammar[pattern],'contrast_grammar')
        link(gid,all_grammar[u['prereq']],'prerequisite')
    revised=sorted({l[k] for l in links for k in ('source_id','target_id') if l[k] in old_ids}|reused)
    for row in tables['content_items']:
        if row['id'] in revised:row['revision']+=1;row['updated_at']=stamp
    tables['content_links'].extend(links)
    args.output.write_text(json.dumps(source,ensure_ascii=False,indent=2)+'\n')
    args.revised.write_text(json.dumps(revised,indent=2)+'\n')
    return dict(grammar=18,examples=72,questions=72,new_content_ids=len(new_ids),revised_existing_ids=len(revised),reused_examples=len(reused),candidate=str(args.output))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--revised',type=Path,required=True)
    parser.add_argument('--allocate-ids',action='store_true')
    args=parser.parse_args()
    protected=[(ROOT/p).resolve() for p in ('Content','Resources','Tests/Fixtures')]
    if args.output.resolve()==args.revised.resolve() or any(path.resolve().is_relative_to(folder) for path in (args.output,args.revised) for folder in protected):
        parser.error('candidate/revision outputs must be distinct and outside Content, Resources and release fixtures')
    print(json.dumps(prepare(args)))
