"""DATA09 full cohort contracts and known editorial regression checks, not language certification."""
import argparse
import collections
import json
import re
import sqlite3
import unicodedata
from pathlib import Path
from build_content import ROOT
from validator import Report


def registries():
    return [g for b in 'abc' for g in json.loads((ROOT/f'Content/data09-{b}-ids.json').read_text())['grammar']]


def norm(text):
    return ''.join(unicodedata.normalize('NFC', text).split()).casefold()


def audit(source):
    tables=source['tables'];report=Report()
    rows={name:{r['id']:r for r in tables[name]} for name in ('grammar','examples','questions','content_items')}
    regs=registries()
    grammar={g['id'] for g in regs};examples={i for g in regs for i in g['example_ids']};questions={i for g in regs for i in g['question_ids']}
    for table,ids,wanted in [('grammar',grammar,54),('examples',examples,216),('questions',questions,216)]:
        if len(ids)!=wanted or not ids<=rows[table].keys():report.error('cohort_count',table,'Missing/repeated cohort ID')
    if report.error_count:return dict(validation=report.as_dict())
    for table,field,ids in [('grammar','pattern',grammar),('examples','korean',examples),('examples','japanese',examples)]:
        counter=collections.Counter(norm(r[field]) for r in tables[table])
        for i in ids:
            if counter[norm(rows[table][i][field])]!=1:report.error('cohort_duplicate',i,field)
    for g in regs:
        r=rows['grammar'][g['id']]
        for field in ('pattern','meaning_ja','explanation_ja','form_ko','usage_constraints_ja','confusion_ja'):
            if not isinstance(r.get(field),str) or not r[field].strip():report.error('grammar_required',g['id'],field)
            elif re.search(r'\bP\d{2}\b',r[field]):report.error('internal_plan_id',g['id'],field)
        for qid in g['question_ids']:
            q=rows['questions'][qid];choices=[r for r in tables['question_choices'] if r['question_id']==qid]
            try:
                answer=json.loads(q['answer_json'])['correct_choice_ids'];task=json.loads(q['rubric_json'])['grammar_task']
                assert q['question_type']=='multiple_choice' and len(choices)==3 and len(answer)==1 and answer[0] in {r['choice_id'] for r in choices}
                assert task in ('meaning','form','context','contrast')
                # Internal spacing is the deliberate tested distinction in C17.
                assert len({unicodedata.normalize('NFC', r['text']).strip().casefold() for r in choices})==3
                assert all('「'+r['text']+'」' in q['explanation_ja'] for r in choices)
            except (KeyError,ValueError,TypeError,AssertionError):report.error('grammar_single_answer',qid,'Single answer/3 distinct choices/rationale contract')
    # Narrow observed failures: these lints do not infer correctness of unseen prose.
    for g in regs:
        r=rows['grammar'][g['id']]
        joined=' '.join(str(v) for v in r.values())
        if any(x in joined for x in ('一回限りの条件-(으)면','後件の時制で全体の時を判断','すでに行う行為')):
            report.error('known_explanation_regression',g['id'],'Previously corrected scope/tense wording')
    a09=next(g for g in regs if g['key']=='A09')['question_ids'][1]
    if '들리다等と混同' in rows['questions'][a09]['explanation_ja']:report.error('wrong_base_form',a09,'들려면 derives from 들다')
    for key,n in [('B03',3),('C11',1),('C11',3)]:
        g=next(g for g in regs if g['key']==key)
        q=rows['questions'][g['question_ids'][n-1]]
        if 'この問題の동생は弟を指す場面です。' not in q['prompt_ja']:
            report.error('sibling_scene_missing',q['id'],'Standalone question must declare the assumed sibling gender')
    input_counts=collections.Counter()
    for q in tables['questions']:
        if q['question_type'] not in ('text_input','listening_input'):continue
        input_counts[q['question_type']]+=1
        try:
            accepted=json.loads(q['answer_json'])['accepted']
            assert isinstance(accepted,list) and accepted and all(isinstance(a,str) and a.strip() for a in accepted)
            normalized=[' '.join(unicodedata.normalize('NFC',a).split()) for a in accepted]
            assert len(set(normalized))==len(normalized)
        except (ValueError,KeyError,TypeError,AssertionError):report.error('accepted_contract',q['id'],'Empty/duplicate normalized accepted answers')
    return dict(validation=report.as_dict(),cohort=dict(grammar=len(grammar),new_examples=len(examples),questions=len(questions),choices=648,new_direct_input=0),existing_input_contracts=dict(input_counts),limitation='Structural and narrow regression checks only. AI reread is separately documented; native grading/native teacher review not certified.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path);parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args();result=audit(json.loads(args.source.read_text()))
    args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result));raise SystemExit(bool(result['validation']['error_count']))
