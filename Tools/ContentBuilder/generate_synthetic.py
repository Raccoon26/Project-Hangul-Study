#!/usr/bin/env python3
"""Generate explicitly NON-EDUCATIONAL JSONL shards. Never write under Resources."""
import argparse, json, uuid
from pathlib import Path
from validator import LEVELS
NAMESPACE=uuid.UUID('62d37d28-f238-4a09-a94e-e36820d2fb6d')
def synthetic_id(kind,key): return str(uuid.uuid5(NAMESPACE,f'{kind}:synthetic-entity-{key}'))
def generate(destination,count=15000):
    destination=Path(destination).resolve()
    project=Path(__file__).resolve().parents[2]
    if destination.is_relative_to(project/'Resources'): raise ValueError('Synthetic data cannot be placed in app Resources')
    if count<1: raise ValueError('count must be positive')
    destination.mkdir(parents=True,exist_ok=True)
    names=['content_items','vocabulary','meanings','examples','vocabulary_examples','grammar','grammar_examples','content_links']
    handles={name:(destination/(name+'.jsonl')).open('w',encoding='utf-8') for name in names}
    def emit(table,row): handles[table].write(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n')
    def item(kind,key,level):
        item_id=synthetic_id(kind,key)
        emit('content_items',dict(id=item_id,kind=kind,revision=1,is_active=1,level=level,created_at='2026-09-30T00:00:00Z',updated_at='2026-09-30T00:00:00Z'))
        return item_id
    grammar_count=min(count,50)
    try:
        for g in range(grammar_count):
            grammar_id=item('grammar',g,'intro')
            emit('grammar',dict(id=grammar_id,pattern=f'__SYNTHETIC__문법{g:06d}',title_ja=f'__SYNTHETIC__文法{g:06d}',explanation_ja='__SYNTHETIC__ 性能測定専用。学習教材ではありません'))
        for i in range(count):
            level=LEVELS[i%len(LEVELS)]
            vocab=item('vocabulary',i,level); meaning=item('meaning',i,level)
            emit('vocabulary',dict(id=vocab,headword=f'__SYNTHETIC__단어{i:06d}',part_of_speech='noun',sort_key=f'__SYNTHETIC__단어{i:06d}'))
            emit('meanings',dict(id=meaning,vocabulary_id=vocab,meaning_ja=f'__SYNTHETIC__意味{i:06d}',ordinal=0))
            if count>1 and i<1000:
                emit('content_links',dict(source_id=vocab,target_id=synthetic_id('vocabulary',(i+1)%count),relation='related_word'))
            for n in range(2):
                key=i*2+n; example=item('example',key,level)
                emit('examples',dict(id=example,korean=f'__SYNTHETIC__ 개발용 문장 {key:06d}',japanese=f'__SYNTHETIC__ 性能確認用の例文 {key:06d}',learning_point_ja='__SYNTHETIC__ 学習用ではありません'))
                emit('vocabulary_examples',dict(meaning_id=meaning,example_id=example))
                emit('grammar_examples',dict(grammar_id=synthetic_id('grammar',i%grammar_count),example_id=example))
    finally:
        for handle in handles.values(): handle.close()
    manifest=dict(source_format='jsonl-v1',metadata=dict(schema_version=2,content_version=1,min_reader_version=2,dataset_id='synthetic-dev-performance',is_fixture=1,source_locale='ja',target_locale='ko'),tables={name:[name+'.jsonl'] for name in names})
    (destination/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return destination
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('destination'); p.add_argument('--count',type=int,default=15000)
    a=p.parse_args(); print(generate(a.destination,a.count))
