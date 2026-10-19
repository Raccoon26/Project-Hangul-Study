# 현재 Production 재현 — DATA-08-8

Python3.10+ 표준 라이브러리만 사용한다. 현재 원본은 `Content/production.json`, Content19/Schema4/reader7이며 아래 DATA01 계약은 당시 이력이다. 프로젝트 루트에서 candidate를 `/tmp`에 만들고 기존 source/번들/fixture를 덮어쓰지 않는다.

```sh
python3 Tools/ContentBuilder/build_content.py Content/production.json /tmp/data08-8-rebuilt.sqlite --production --previous Tests/Fixtures/content-v18-production.sqlite --report /tmp/data08-8-build.json
python3 Tools/ContentBuilder/audit_data08_system.py --report /tmp/data08-8-system-audit.json
python3 Tools/ContentBuilder/audit_data08_closeout.py --rebuilt /tmp/data08-8-rebuilt.sqlite --build-report /tmp/data08-8-build.json --system-audit /tmp/data08-8-system-audit.json --report /tmp/data08-8-closeout.json
sh Tools/verify.sh --portable
```

현재19의 재현은18을 previous로 사용했다. 다음 실제 콘텐츠 변경에는 현재19를 보존한 DB를 previous로 사용한다. canonical JSON/DDL/고정ID와 과거 fixture를 보존하며, 재생성 가능한 번들 DB도 현 Xcode 배포 계약상 추적한다. 현재 최대Git blob17.9MB로 LFS는 필요 없다. 전체 byte/schema/row 일치 근거·native 미실행 상태는 [최종 보고](../../Docs/DATA08_CLOSEOUT.md)에 있다.

---

# Content Builder / Importer — DATA-01

전체 제작 계약은 프로젝트 루트의 **CONTENT_GUIDE.md**를 읽습니다. Python 3.10 이상, 외부 패키지 불필요입니다.

| 파일 | 역할 |
| --- | --- |
| source_reader.py | 단일 JSON/manifest + JSONL 스트리밍, 중복 key/경로 검증 |
| validator.py | 타입·enum·문장·관계·출처·UUID·업데이트 revision 검사, error/warning 보고서 |
| build_content.py | staging SQLite 작성, 검증, 파생 검색 index, ANALYZE, 원자적 게시 |
| migrate_source_v1.py | DEV-01 원본을 ID 유지하며 v2로 명시적 업그레이드 |
| generate_synthetic.py | 15,000 어휘/30,000 예문용 개발 데이터 재현 |
| benchmark.py | Swift 실제 SQL을 사용한 성능 측정 및 보고 |
| test_*.py | importer/validator/기록 분리/대용량 회귀 테스트 |

```sh
python3 Tools/ContentBuilder/build_content.py Content/fixture.json Resources/content-fixture.sqlite
python3 Tools/ContentBuilder/build_content.py Content/production.json candidate.sqlite --production --previous Tests/Fixtures/content-v4-production.sqlite
python3 Tools/ContentBuilder/build_content.py path/to/source --validate-only --report validation.json
python3 -m unittest discover -s Tools/ContentBuilder -v
```

이후 배포에는 `--previous 이전배포.sqlite`를 반드시 지정합니다. 모든 오류를 수정한 뒤 출력하며 실패 시 기존 출력은 보존합니다. --validate-only도 같은 import/validate 경로를 실행하지만 임시 파일을 버립니다. warning은 삭제·병합하지 않고 검수 대상으로 제공합니다. 대용량 테스트도 동일한 validation을 거칩니다.

DATA-01 production은 schema 3 / content 5 / reader 4입니다. schema 2 입력은 회귀 검증용으로 계속 지원합니다. `production-empty.json`과 `hangul-production.json`은 과거 snapshot이며 현재 앱 DB를 덮어쓰지 않습니다. 다음 DATA 배포는 현재 배포 DB를 `--previous`로 지정하세요. 한글/발음/음성 계약은 `CONTENT_GUIDE.md` 12~14절을 따릅니다.
