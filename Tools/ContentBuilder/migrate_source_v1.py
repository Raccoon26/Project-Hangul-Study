#!/usr/bin/env python3
"""Explicit one-time DEV-01 JSON -> schema v2 source upgrade. IDs and created_at stay fixed."""
import argparse, json
from pathlib import Path
from source_reader import strict_json
POS_MAP={'名詞':'noun','表現':'expression'}
def migrate(source,destination):
    data=strict_json(Path(source).read_text())
    if data['metadata']['schema_version']!=1: raise ValueError('Expected v1 source')
    data['metadata']['schema_version']=2
    data['metadata']['min_reader_version']=2
    data['metadata']['content_version']+=1
    for item in data['tables'].get('content_items',[]): item['revision']+=1
    for row in data['tables'].get('vocabulary',[]):
        if row['part_of_speech'] not in POS_MAP: raise ValueError('Unknown legacy POS; map explicitly after review')
        row['part_of_speech']=POS_MAP[row['part_of_speech']]
    Path(destination).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('source'); p.add_argument('destination')
    a=p.parse_args(); migrate(a.source,a.destination)
