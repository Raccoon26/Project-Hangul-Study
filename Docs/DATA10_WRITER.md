# DATA10 Mac/Cloud SQLite writer 재현

DATA10-1의 Mac Homebrew Python3.11.6/SQLite3.44.0 ENABLE_STAT4는 과거 배포와 byte가 달랐다. DATA10-2에서 시스템 설치·Production·Validator·DDL을 변경하지 않고 격리된 writer를 준비했다.

- Codex 번들 Python3.12.14/SQLite3.53.1은 STAT4 없이31테이블의 모든 행과 schema가 같았다. 그러나 마지막 sqlite_stat1 페이지의 행 배치가 달라 Content24 전체18,841,600bytes 중2,198bytes가 달랐다. 같은 SQLite 버전 문자열만으로 byte 재현을 인증하지 않는다.
- 공식 [SQLite3.53.1 소스](https://www.sqlite.org/2026/sqlite-amalgamation-3530100.zip), SHA256 `36ad6e7f38540a3b21a2ac36340833f0a9e426bc1c752751c3ba669466827eae`를 사용했다. 소스의 `analyzeDatabase`는 schema hash 순서로 통계를 생성하고 `rehash`는 실제 allocator 크기를 사용한다. Mac zone allocator/compile profile에 따른 행 배치 차이와 부합한다.
- [pysqlite3 0.6.1 원본](https://pypi.org/project/pysqlite3/0.6.1/), sdist SHA256 `dd7d2b7f3a29aebdbf569c359658b091d3345b5691d9ea765a5c3febe8872bf9`에 위 amalgamation을 정적으로 컴파일한다. 해당 wrapper의 STAT4 플래그를 빼고 SQLite의 `SQLITE_WITHOUT_ZONEMALLOC=1`을 사용한다. pysqlite3에 없는 `Connection.iterdump()`는 Python 표준 라이브러리 `sqlite3.dump._iterdump`에 그대로 위임하는 Connection subclass로 보완한다. 기존 사용자 DB 전후 dump 비교 assertion을 유지한다. 시스템 통계 행을 삭제/재정렬하거나 bundle header를 편집하지 않는다. 원래 ContentBuilder와 strict gate/byte assertion은 그대로 실행한다.
- 이 profile에서 **Content24 byte/SHA 전체 재현 성공**. frozen24 SHA `56a7fa8b5358e254eeb324e706860d150d20c8ec013ba0b6f602cf14d93cceff`. Content25도 별도 candidate 재구성→byte 비교를 수행한다. 23/24 역사 gate와 전체 결과는 `DATA10_A_TEST_RESULTS.json`/portable 로그를 따른다.

재현 명령(각 환경의 설치 Python3.11+/pip/C compiler 필요):

```sh
python3 Tools/ContentBuilder/setup_exact_writer.py /tmp/hangul-content-writer
export PATH="/tmp/hangul-content-writer/bin:$PATH"
python3 -c 'import sqlite3; print(sqlite3.sqlite_version)'
sh Tools/verify.sh --portable
python3 Tools/ContentBuilder/prepare_data10_a.py --output /tmp/data10-a.json --revised /tmp/data10-a-revised.json
python3 Tools/ContentBuilder/build_content.py /tmp/data10-a.json /tmp/data10-a.sqlite --previous Tests/Fixtures/content-v24-production.sqlite --production
cmp Resources/content.sqlite /tmp/data10-a.sqlite
```

setup은 새 외부 디렉터리만 허용하고, 다운로드 두 원본의 SHA를 검증하며, 기존 디렉터리를 덮어쓰지 않는다. repo/시스템 Python을 바꾸지 않고 해당 PATH의 python3에만 격리된 DB-API wrapper를 선택한다. 내려받은 원본·라이선스·profile.json을 출력 디렉터리에 보존한다. 컴파일된 라이브러리·candidate·빌드 산출물은 Git에 추가하지 않는다. 네트워크는 최초 환경 구성에만 필요하며 앱의 오프라인 계약은 바꾸지 않는다.

정상 설치 Python의 sqlite3는 여전히 원래 version/compile profile이므로 PATH 없이 byte 재현 성공을 가정하지 않는다. 다음 환경도 frozen fixture/현재 candidate의 **실제 byte 비교**를 먼저 실행하고 실패하면 원인을 보고한다. Content25 이후 후속 제작은 실제 직전 배포25를 새 previous로 보존한다. `prepare_data10_a`는 고정24→25만 재현하며 미래 Production을 입력으로 덮어쓰는 importer가 아니다.

DATA10-2에서 수정된 setup 도구를 새 외부 디렉터리에 다시 실행하는 cold rehearsal도 완료했다. 표준 dump 왕복 및24/25 전체 byte 비교는 [실제 결과](DATA10_A_COLD_WRITER_REHEARSAL.json)를 따른다. 초기 wrapper에 iterdump가 없어 발생한4개 검사 ERROR는 assertion을 바꾸지 않고 이 표준 구현 위임으로 해결했다. 최종 전체 실행 결과는 DATA10_A_TEST_RESULTS.json에 별도로 기록한다.
