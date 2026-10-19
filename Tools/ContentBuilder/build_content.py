#!/usr/bin/env python3
"""Source JSON/JSONL -> validation -> atomic SQLite artifact. Python stdlib only."""
import argparse, hashlib, json, os, sqlite3, tempfile, time
from pathlib import Path
from source_reader import SourceReader
from validator import (Report, ValidationError, SCHEMA_VERSION, KINDS, canonical_uuid,
                       metadata, row_fields, database, previous_release, normalize)
ROOT=Path(__file__).resolve().parents[2]
valid_uuid=canonical_uuid  # Retain the DEV-01 public helper name.

def build(source,output,previous=None,production=False):
    started=time.perf_counter(); report=Report()
    try: reader=SourceReader(source)
    except (ValueError,OSError) as error:
        report.error('source_format',str(source),str(error)); raise ValidationError(report) from error
    meta=reader.metadata
    metadata(meta,report)
    if production and meta.get('is_fixture')!=0: report.error('production_fixture','metadata','Production rejects fixture content')
    output=Path(output).resolve()
    inputs={reader.path.resolve(),*(p for paths in reader.files.values() for p in paths)}
    if output in inputs or (previous and output==Path(previous).resolve()): report.error('output_path',str(output),'Output must not overwrite input or previous release')
    if report.error_count: raise ValidationError(report)
    output.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix='.content-',suffix='.sqlite',dir=output.parent); os.close(fd)
    con=None
    try:
        con=sqlite3.connect(tmp)
        con.executescript((ROOT/f"Content/content-schema-v{meta['schema_version']}.sql").read_text())
        if con.execute('PRAGMA user_version').fetchone()[0] != meta['schema_version']:
            report.error('schema_header',str(source),'Schema DDL user_version must match source metadata')
            raise ValidationError(report)
        allowed={r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}-{'content_metadata','vocabulary_search'}
        for table in set(reader.tables)-allowed: report.error('unknown_table',table,'Table is unknown or derived; source cannot write it')
        if report.error_count: raise ValidationError(report)
        columns={table:{r[1]:r for r in con.execute(f'PRAGMA table_info("{table}")')} for table in allowed}
        con.execute('BEGIN'); con.execute('PRAGMA defer_foreign_keys=ON')
        names=['singleton',*meta]
        con.execute(f'INSERT INTO content_metadata({",".join(names)}) VALUES({",".join("?" for _ in names)})',[1,*meta.values()])
        statements={}; counts={}
        for table in sorted(reader.tables):
            counts[table]=0
            try:
                for location,row in reader.rows(table):
                    if not row_fields(table,row,columns[table],location,report): continue
                    if meta['is_fixture']==0 and any(isinstance(value,str) and '__SYNTHETIC__' in value for value in row.values()):
                        report.error('synthetic_production',location,'Synthetic marker in production source'); continue
                    keys=tuple(sorted(row))
                    if not keys: report.error('empty_row',location,'Empty object'); continue
                    signature=(table,keys)
                    if signature not in statements:
                        fields=','.join('"'+key+'"' for key in keys)
                        statements[signature]=f'INSERT INTO "{table}"({fields}) VALUES({",".join("?" for _ in keys)})'
                    try:
                        con.execute(statements[signature],[row[key] for key in keys]); counts[table]+=1
                    except sqlite3.IntegrityError as error:
                        code='duplicate_id_or_key' if 'UNIQUE' in str(error) else 'constraint'
                        report.error(code,location,str(error))
            except (ValueError,OSError) as error: report.error('source_row',table,str(error))
        database(con,reader,report)
        if previous:
            old=None
            try:
                old=sqlite3.connect(Path(previous).resolve().as_uri()+'?mode=ro',uri=True)
                previous_release(con,old,meta,report)
            except sqlite3.DatabaseError as error: report.error('previous_database',str(previous),str(error))
            finally:
                if old is not None: old.close()
        if report.error_count: raise ValidationError(report)
        # Materialized normalized prefix terms; app never parses JSON or builds this index.
        def terms():
            for item_id,word,reading in con.execute('SELECT id,headword,reading FROM vocabulary'):
                yield normalize(word),item_id
                if reading: yield normalize(reading),item_id
            for item_id,meaning in con.execute('SELECT vocabulary_id,meaning_ja FROM meanings m JOIN content_items i ON i.id=m.id WHERE i.is_active=1'):
                yield normalize(meaning),item_id
        con.executemany('INSERT OR IGNORE INTO vocabulary_search(term,vocabulary_id) VALUES(?,?)',terms())
        con.commit(); con.execute('ANALYZE'); con.commit()
        if con.execute('PRAGMA integrity_check').fetchone()[0]!='ok':
            report.error('integrity','database','SQLite integrity check failed'); raise ValidationError(report)
        con.close(); con=None
        os.replace(tmp,output)
        return dict(path=str(output),sha256=hashlib.sha256(output.read_bytes()).hexdigest(),schema_version=meta['schema_version'],
                    content_version=meta['content_version'],rows=counts,seconds=round(time.perf_counter()-started,4),validation=report.as_dict())
    finally:
        if con is not None: con.close()
        if os.path.exists(tmp): os.unlink(tmp)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path); parser.add_argument('output',type=Path,nargs='?')
    parser.add_argument('--previous',type=Path); parser.add_argument('--production',action='store_true')
    parser.add_argument('--validate-only',action='store_true'); parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    if not args.validate_only and args.output is None: parser.error('output required unless --validate-only')
    try:
        if args.validate_only:
            with tempfile.TemporaryDirectory() as directory:
                result=build(args.source,Path(directory)/'validation.sqlite',args.previous,args.production)
                result.pop('path',None); result['validation_only']=True
        else: result=build(args.source,args.output,args.previous,args.production)
        status=0
    except ValidationError as error: result={'validation':error.report}; status=1
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
    return status
if __name__=='__main__': raise SystemExit(main())
