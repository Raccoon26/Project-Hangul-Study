#!/usr/bin/env python3
"""Create an isolated, pinned SQLite3.53.1 writer (no system/Python/repo changes).
Requires Python3.11+ with pip, a C compiler and network for the initial build.
Use the printed PATH for existing build_content.py / Tools/verify.sh commands.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import sys
import tarfile
import urllib.request
import zipfile

SQLITE_URL='https://www.sqlite.org/2026/sqlite-amalgamation-3530100.zip'
SQLITE_SHA='36ad6e7f38540a3b21a2ac36340833f0a9e426bc1c752751c3ba669466827eae'
PYSQLITE_URL='https://files.pythonhosted.org/packages/28/43/6f1f3adc88f9f77a0f49a2959f6aac5f56900da5e60c65fa6fbcc9c0afae/pysqlite3-0.6.1.tar.gz'
PYSQLITE_SHA='dd7d2b7f3a29aebdbf569c359658b091d3345b5691d9ea765a5c3febe8872bf9'


def setup(destination):
    destination=destination.resolve()
    repo=Path(__file__).resolve().parents[2]
    if destination.is_relative_to(repo) or destination.exists():
        raise ValueError('Use a new directory outside the checkout; existing files are never overwritten')
    destination.mkdir(parents=True)
    def download(url,expected):
        data=urllib.request.urlopen(url,timeout=60).read()
        if hashlib.sha256(data).hexdigest()!=expected:raise ValueError('Download SHA mismatch: '+url)
        return data
    archive=destination/'sqlite.zip';archive.write_bytes(download(SQLITE_URL,SQLITE_SHA))
    with zipfile.ZipFile(archive) as z:
        for name in ('sqlite3.c','sqlite3.h'):
            (destination/name).write_bytes(z.read('sqlite-amalgamation-3530100/'+name))
    archive=destination/'pysqlite.tar.gz';archive.write_bytes(download(PYSQLITE_URL,PYSQLITE_SHA))
    with tarfile.open(archive) as t:
        # Never extract arbitrary archive paths or links.
        for member in t.getmembers():
            if not member.isfile():continue
            relative=Path(member.name)
            if relative.is_absolute() or '..' in relative.parts:raise ValueError('Unsafe archive path')
            target=destination/relative;target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(t.extractfile(member).read())
    package=destination/'pysqlite3-0.6.1'
    for name in ('sqlite3.c','sqlite3.h'):(package/name).write_bytes((destination/name).read_bytes())
    setup_file=package/'setup.py';text=setup_file.read_text()
    before="('SQLITE_ENABLE_STAT4', 1),";after="('SQLITE_WITHOUT_ZONEMALLOC', 1),"
    if text.count(before)!=1:raise ValueError('Unexpected pinned setup.py')
    setup_file.write_text(text.replace(before,after))
    subprocess.run([sys.executable,'-m','pip','install','--no-deps','--target',str(destination/'modules'),str(package)],check=True)
    profile=destination/'profile';profile.mkdir()
    (profile/'sitecustomize.py').write_text("""import sys
import sqlite3.dump as stdlib_dump
sys.path.insert(0, __MODULES__)
import pysqlite3
assert pysqlite3.sqlite_version == '3.53.1'
original_connect = pysqlite3.connect
class ExactConnection(pysqlite3.Connection):
    def iterdump(self):
        return stdlib_dump._iterdump(self)
def connect(*args, **kwargs):
    if len(args) < 6 and 'factory' not in kwargs:
        kwargs['factory'] = ExactConnection
    return original_connect(*args, **kwargs)
pysqlite3.Connection = pysqlite3.dbapi2.Connection = ExactConnection
pysqlite3.connect = pysqlite3.dbapi2.connect = connect
sys.modules['sqlite3'] = pysqlite3
sys.modules['sqlite3.dbapi2'] = pysqlite3.dbapi2
""".replace('__MODULES__', repr(str(destination/'modules'))))
    binary=destination/'bin';binary.mkdir()
    wrapper=binary/'python3'
    wrapper.write_text('#!/bin/sh\nexport PYTHONPATH='+shlex.quote(str(profile))+'${PYTHONPATH:+:$PYTHONPATH}\nexec '+shlex.quote(sys.executable)+' "$@"\n');wrapper.chmod(0o755)
    metadata=dict(sqlite_source_url=SQLITE_URL,sqlite_archive_sha256=SQLITE_SHA,pysqlite_source_url=PYSQLITE_URL,pysqlite_archive_sha256=PYSQLITE_SHA,profile_change=after,python=sys.executable)
    (destination/'profile.json').write_text(json.dumps(metadata,indent=2)+'\n')
    subprocess.run([str(wrapper),'-c','import sqlite3; print("SQLite",sqlite3.sqlite_version); assert not any("STAT4" in r[0] for r in sqlite3.connect(":memory:").execute("pragma compile_options"))'],check=True)
    print('export PATH='+shlex.quote(str(binary))+':"$PATH"')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('destination',type=Path);args=p.parse_args();setup(args.destination)
