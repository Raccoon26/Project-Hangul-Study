"""Readable JSON for small sources; streaming, sharded JSONL for DATA batches."""
import json
from pathlib import Path


def strict_json(text):
    def pairs(items):
        result={}
        for key,value in items:
            if key in result: raise ValueError(f'Duplicate JSON key: {key}')
            result[key]=value
        return result
    def reject_constant(value): raise ValueError(f'Non-finite JSON number: {value}')
    return json.loads(text,object_pairs_hook=pairs,parse_constant=reject_constant)

class SourceReader:
    def __init__(self,path):
        path=Path(path)
        self.path=path/'manifest.json' if path.is_dir() else path
        self.root=self.path.parent.resolve()
        self.document=strict_json(self.path.read_text(encoding='utf-8'))
        if not isinstance(self.document,dict) or set(self.document)-{'metadata','tables','source_format'}:
            raise ValueError('Source must contain metadata, tables and optional source_format only')
        self.metadata=self.document.get('metadata')
        self.tables=self.document.get('tables')
        if not isinstance(self.metadata,dict) or not isinstance(self.tables,dict):
            raise ValueError('metadata and tables must be objects')
        self.sharded=self.document.get('source_format')=='jsonl-v1'
        if self.document.get('source_format') not in (None,'jsonl-v1'):
            raise ValueError('Unsupported source_format')
        self.files={}
        used=set()
        for table,values in self.tables.items():
            if not isinstance(values,list): raise ValueError(f'{table}: expected array')
            if self.sharded:
                resolved=[]
                for value in values:
                    if not isinstance(value,str): raise ValueError(f'{table}: shard path must be text')
                    p=Path(value)
                    candidate=(self.root/p).resolve()
                    if p.is_absolute() or '..' in p.parts or '\\' in value or not candidate.is_relative_to(self.root):
                        raise ValueError(f'Unsafe shard path: {value}')
                    if candidate in used: raise ValueError(f'Shard listed twice: {value}')
                    if candidate.suffix!='.jsonl' or not candidate.is_file(): raise ValueError(f'Missing JSONL shard: {value}')
                    used.add(candidate); resolved.append(candidate)
                self.files[table]=resolved
    def rows(self,table):
        if self.sharded:
            for path in self.files[table]:
                with path.open(encoding='utf-8') as f:
                    for line_number,line in enumerate(f,1):
                        if not line.strip(): continue
                        location=f'{path.relative_to(self.root)}:{line_number}'
                        try: row=strict_json(line)
                        except ValueError as error: raise ValueError(f'{location}: {error}') from error
                        yield location,row
        else:
            for i,row in enumerate(self.tables[table]): yield f'{self.path.name}:{table}[{i}]',row
