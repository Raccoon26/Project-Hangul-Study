#!/usr/bin/env python3
"""One-time, hash-locked correction of DEV-09's wrong SQLite header; never edits input.
This does not bypass the importer. The corrected snapshot must pass its normal
previous-release validator. Original artifact stays available for audit.
"""
import hashlib,sqlite3,sys
from pathlib import Path
from validator import signatures
ROOT=Path(__file__).resolve().parents[2]
def repair(source,destination):
 source,destination=Path(source).resolve(),Path(destination).resolve()
 if source==destination or destination.exists():raise ValueError('New output path required')
 if hashlib.sha256(source.read_bytes()).hexdigest()!='9c584bd0f7b4b213a1b8120fed77fe6b1ad0d3a08e5649f07ee067973351d8d0':raise ValueError('Not the exact shipped DEV-09 artifact')
 with sqlite3.connect(source.as_uri()+'?mode=ro',uri=True) as old:
  if old.execute('PRAGMA user_version').fetchone()[0]!=3 or old.execute('SELECT schema_version,content_version,min_reader_version FROM content_metadata').fetchone()!=(4,10,7):raise ValueError('Unexpected release')
  with sqlite3.connect(destination) as fixed:
   old.backup(fixed);fixed.execute('PRAGMA user_version=4');fixed.commit()
   assert signatures(old)==signatures(fixed)
   assert fixed.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
   assert fixed.execute('PRAGMA foreign_key_check').fetchall()==[]
 return hashlib.sha256(destination.read_bytes()).hexdigest()
if __name__=='__main__':print(repair(sys.argv[1],sys.argv[2]))
