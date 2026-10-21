"""Reconstruct reviewed Content26 from frozen25 and one persistent UUID manifest.
CLI outputs are temporary candidates; never write Production or frozen inputs.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
from build_content import ROOT

BASE_SHA = 'ddb21c13e12624da2f208d3f842309ab79a075b986cea832424857cdae763941'


def prepare(output, revised):
    raw = gzip.decompress((ROOT/'Tests/Fixtures/content-v25-production.json.gz').read_bytes())
    assert hashlib.sha256(raw).hexdigest() == BASE_SHA
    source = json.loads(raw)
    manifest = json.loads((ROOT/'Content/data10-b-authoring.json').read_text())
    tables = source['tables']; stamp = manifest['created_at']
    assert source['metadata']['content_version'] == 25 and manifest['content_version'] == 26
    source['metadata']['content_version'] = 26
    tables['sources'].append(dict(id=manifest['source_id'], title='DATA10-B：初中級の気持ち・意見・判断のリスニング',
        citation='本プロジェクトでassistantが独自執筆した原文・日本語訳・問題。AI自己再読済み。独立原語話者・教師監修と実音声の検聴は未実施。TTSであり録音ではない。', url=None, accessed_at=None))
    items = manifest['items']; choice_number = 0
    def entity(i, kind):
        tables['content_items'].append(dict(id=i,kind=kind,revision=1,is_active=1,level='lower_intermediate',difficulty=None,created_at=stamp,updated_at=stamp))
        tables['item_sources'].append(dict(content_id=i,source_id=manifest['source_id'],note='DATA10-B 独自執筆・Batch Self Review。音声は端末の韓国語TTS。'))
    for row in items:
        entity(row['example_id'], 'example')
        tables['examples'].append(dict(id=row['example_id'],korean=row['korean'],japanese=row['japanese'],learning_point_ja=row['learning_point_ja']))
    for phase in range(2):
        for n, row in enumerate(items):
            spec = row['tasks'][phase]; task = spec['task']; lid = spec['listening_id']; qid = spec['question_id']
            entity(lid,'listening'); entity(qid,'question')
            tables['listening_items'].append(dict(id=lid,audio_asset_id=None,transcript_ko=None,explanation_ja=row['learning_point_ja'],source_example_id=row['example_id'],audio_mode='tts',learning_order=2180+phase*60+n))
            tables['content_links'].append(dict(source_id=lid,target_id=row['example_id'],relation='related'))
            if task == 'dictation':
                prompt = '聞こえた内容を韓国語で入力してください。文中の句読点は入力してください。文末の「.」「!」「?」は省略できます。'
                answer = dict(accepted=[row['korean']]); direction='ko_ko'
            else:
                if task == 'comprehension':
                    prompt = spec['prompt_ja']; correct = spec['correct']; distractors = spec['distractors']; direction='ko_ja'
                else:
                    field = 'japanese' if task == 'meaning' else 'korean'
                    prompt = '聞こえた場面全体の意味を選んでください。' if task == 'meaning' else '聞こえた内容と一致する韓国語を選んでください。'
                    correct = row[field]; start = n//10*10
                    alternatives = [items[start+(n%10+offset)%10] for offset in (1,2)]
                    distractors = [other[field] for other in alternatives]; direction='ko_ja' if task=='meaning' else 'ko_ko'
                position = choice_number % 3; choice_number += 1
                texts = list(distractors); texts.insert(position,correct)
                answer = dict(correct_choice_ids=['abc'[position]])
                for ordinal,text in enumerate(texts):
                    tables['question_choices'].append(dict(question_id=qid,choice_id='abc'[ordinal],ordinal=ordinal,text=text))
            tables['questions'].append(dict(id=qid,question_type='listening_input' if task=='dictation' else 'listening_choice',direction=direction,answer_schema_version=1,prompt_ja=prompt,prompt_ko=None,explanation_ja=(row['learning_point_ja'] if task=='dictation' else row['learning_point_ja']+' 正解の手がかり：「'+spec['correct_evidence_ko']+'」。'+''.join('「'+text+'」：'+why for text,why in zip(spec['distractors'],spec['distractor_explanations_ja']))),answer_json=json.dumps(answer,ensure_ascii=False),rubric_json=json.dumps(dict(listening_task=task),ensure_ascii=False),listening_id=lid,topik_level=None))
    assert choice_number == 60
    output.write_text(json.dumps(source,ensure_ascii=False,indent=2)+'\n')
    revised.write_text('[]\n')
    return dict(content_version=26,new_examples=60,reused_existing_sources=0,new_listening=120,new_questions=120,revised_existing_ids=0)


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--revised',type=Path,required=True);a=p.parse_args()
    protected=[(ROOT/f).resolve() for f in ('Content','Resources','Tests/Fixtures')]
    if a.output.resolve()==a.revised.resolve() or any(x.resolve().is_relative_to(d) for x in (a.output,a.revised) for d in protected):p.error('use distinct temporary outputs outside protected inputs')
    print(json.dumps(prepare(a.output,a.revised)))
