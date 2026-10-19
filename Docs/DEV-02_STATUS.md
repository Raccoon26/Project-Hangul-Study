# PROJECT_STATUS — DEV-02 완료

작성: 2026-09-30 (일본 시간). 작업 상한 45분. DEV-01 전체 프로젝트/상태 문서 및 저장된 ZIP과 작업 파일 일치를 확인한 뒤 확장했습니다. DEV-01 기록은 `Docs/DEV-01_STATUS.md`에 보존했습니다.

## 1. DEV-02에서 구현한 내용

- **시스템 SQLite3 유지**: 앱 번들 read-only 콘텐츠 DB와 Application Support 사용자 DB를 계속 분리
- 콘텐츠 **schema v2**: 어휘/의미/예문/문법/발음/활용의 상세 메타데이터, 출처, 발음 전후 예시, 문제 유형/방향/답 계약 보완
- 단계 enum 9개, 품사 enum 16개를 SQL·Python·Swift에서 일치시킴. TOPIK/빈도는 선택값이며 어휘에 지정하면 출처 필수
- JSON 단일 파일과 **manifest + 테이블별 JSONL shard** Importer. JSONL은 스트리밍, 앱은 JSON을 읽지 않음
- Validator의 오류/경고 보고서: 원본 파일/줄·항목 위치, 최대 200개 상세/전체 오류 개수
- 중복 ID/키, 표제어 중복 후보, 필수값/타입/enum, 빈 문장/번역, 초과 길이, 고아 예문, 누락 참조, 관계 kind, 비정상 숫자/Unicode, 버전 검증
- 정답 JSON의 유형별 구조 검사, 듣기 참조 필수, 실제 미디어 파일/해시 검사 유지
- 기존 ID/kind/created_at 보존, revision 하락 금지, **관계 변경까지** revision 증가 검사 확장
- 파생 vocabulary_search 생성 + ANALYZE. Swift 저장소의 단계/한국어·일본어 접두어 검색 페이지 API 추가
- 사용자 **schema v2**: 습득 상태/체감 난이도 컬럼 추가. 기존 v1은 SQLite backup API 스냅샷 후 transactional migration
- 15,000 어휘/30,000 예문 synthetic 생성기, 실제 저장소 SQL 기반 benchmark, 전체 규모 자동 테스트
- `CONTENT_GUIDE.md`에 필수/선택 필드 사전·단계/품사·관계·정답 형식·추가/검증/배포 절차 작성
- 기존 4탭/북마크/단어 상세 동작 유지. 검색 UI나 학습 알고리즘은 선행 구현하지 않음

## 2. DB 기술과 구조

외부 런타임 패키지 없이 Apple 시스템 SQLite3를 사용합니다. Python 표준 sqlite3는 콘텐츠 제작 도구에만 사용합니다.

| 영역 | 주요 구조 |
| --- | --- |
| 공통 | content_metadata, content_items(영구 UUID/revision/tombstone/level/difficulty) |
| 어휘 | vocabulary + meanings(다의어/품사/뉘앙스/사용 설명), 선택 발음/받침/불규칙/우선순위/출처 있는 TOPIK·빈도 |
| 예문 | examples + vocabulary_examples + grammar_examples, learning_point_ja |
| 문법/발음 | grammar의 의미/형태/조건/혼동, pronunciation_rules + pronunciation_examples의 표기/실제 발음 |
| 활용 | conjugations의 기본 어휘/활용형/종류/말높임/규칙·불규칙/발음 규칙 연결 |
| 듣기/문제 | media_assets, listening_items, questions, question_choices, 방향/답 스키마 버전 |
| 과정·관계 | courses, lessons, lesson_items, tags, item_tags, learner_notes, content_links, content_aliases |
| 근거·조회 | sources, item_sources, 파생 vocabulary_search |

정확한 SQL은 `Content/content-schema-v2.sql`, 전체 필드 설명은 `CONTENT_GUIDE.md`입니다. v1 SQL은 과거 계약/테스트를 위해 보존했습니다.

## 3. UserProgress와 분리

콘텐츠는 번들 `content.sqlite`, 사용자 기록은 `user.sqlite`입니다. Debug는 작은 fixture를 사용하고 기록은 `user-development.sqlite`로 분리합니다. synthetic 성능 DB는 앱에 포함하지 않습니다.

사용자 DB는 콘텐츠 UUID 텍스트만 참조하며 다른 DB로 foreign key/cascade delete하지 않습니다. `dataset_id`가 다른 corpus와 잘못 연결되는 것을 막습니다. 정상 콘텐츠 교체는 사용자 파일을 열거나 재작성하지 않습니다.

기존 item_progress/SRS/due/event/favorite/회독/레슨/통계 테이블을 유지했습니다. v2에서 item_progress에 acquisition_status(unassessed/learning/acquired/maintaining), perceived_difficulty(null 또는 1~5)를 추가했습니다. 과거 횟수만 보고 습득 완료를 추정하지 않으므로 기본값은 unassessed입니다. 평가 화면/알고리즘은 아직 없습니다.

기존 v1 migration은 SQLite backup API를 사용해 WAL까지 반영된 스냅샷을 만든 후, 컬럼과 user_version을 한 트랜잭션에서 갱신합니다. 실패하면 rollback하며 자동 삭제하지 않습니다. 새 DB는 기존 v1 생성 SQL 뒤에 v2를 적용합니다.

## 4. Importer / Validator 구조

- source_reader.py: JSON/JSONL 입력, 중복 JSON key/비유한 숫자/잘못된 shard 경로 검증
- validator.py: 타입·enum·길이·공백·관계·출처 제약·orphan·UUID·정답 구조·이전 배포 비교. 경고는 자동 삭제하지 않음
- build_content.py: 임시 DB 생성→바인딩 INSERT→모든 validation→파생 검색 term→ANALYZE/integrity→원자적 출력. 실패 시 기존 파일 보존
- migrate_source_v1.py: 기존 ID/created_at 유지, legacy POS 명시 변환, revision/content_version 증가
- generate_synthetic.py / benchmark.py: 실제 교육 데이터와 분리된 성능 재현

업데이트는 **전체 source 스냅샷**입니다. DATA 추가 시 이전 shard와 tombstone을 manifest에 계속 포함해야 합니다. 새 batch만 넣고 이전 내용을 버리는 merge importer는 아닙니다.

## 5. Stable ID / 버전

실제 콘텐츠는 최초 UUID 발급 후 원본에 영구 저장합니다. 순서/문자열/rowid를 ID로 사용하지 않습니다. 삭제 대신 inactive tombstone과 상세 행을 보존하고 다른 개념으로 ID를 재사용하지 않습니다.

- schema_version=2: 콘텐츠 구조
- content_version: dataset별 배포 번호, 현재 작은 fixture/빈 production은 2
- revision: 개별 항목, 현재 DEV-01 항목은 ID 유지하며 2
- min_reader_version=2: 현재 콘텐츠를 읽는 앱 계약
- 사용자 PRAGMA user_version=2: 콘텐츠와 별개

관계 행이 바뀌면 모든 콘텐츠 끝점의 revision을 증가해야 합니다. 이전 배포를 `--previous`로 비교합니다. v1→v2 source 업그레이드를 실제 실행해 기존 9개 UUID가 동일함을 확인했습니다.

## 6. 테스트 결과

**Python/SQLite 자동 테스트 49개 통과** (`Docs/TEST_RESULTS.txt`). 테스트를 위해 validation을 끄거나 invalid 행을 성공 결과에서 제외하지 않았습니다.

검사 범위: importer/validator, v1→v2 stable ID, source 재정렬 시 ID/revision 유지, 관계 수정 시 양 끝점 revision 요구, 잘못된 입력 거부, schema/content version, 실제 Swift 내 SQL, JSONL 줄 위치, failed import 원자성, 사용자 DB byte 보존, 사용자 migration/rollback, 15,000/30,000 corpus.

추가 확인:

- Swift **20파일** 구문 파싱 오류 없음
- Xcode 프로젝트 독립 파싱, 2 target/공유 Scheme/소스·리소스 존재와 포함 확인
- 실제 리소스 복사 shell phase에서 Debug fixture/Release production 선택 확인
- SQLite integrity/FK 및 Swift·Python·SQL 단계/품사 enum 일치 확인
- TODO/FIXME, fatalError, try!, as! 코드 없음

**Xcode/Swift 컴파일러가 없는 Linux 환경**이므로 iOS 컴파일·링크·시뮬레이터·XCTest **10개** 실행은 못 했습니다. 네이티브 빌드 성공으로 표현하지 않습니다. 특히 Apple 환경 backup API 실행은 추가 XCTest로 준비했지만 아직 실행하지 못했습니다.

## 7. Synthetic 대용량 결과

실제 교육 콘텐츠는 생성하지 않았습니다. `__SYNTHETIC__` 표시와 개발용 dataset/fixture flag를 가진 **15,000 어휘, 15,000 의미, 30,000 예문, 50 문법 및 관계**를 생성·검증했습니다. 결과 DB는 앱이나 배포 ZIP에 넣지 않으며 스크립트로 재현합니다.

최종 실측(Linux/Python SQLite, 장치 성능 아님):

| 지표 | 결과 |
| --- | ---: |
| DB 생성·검증 | 10.48초 |
| DB 크기 | 50,712,576 bytes (약 48.36 MiB) |
| 도구 프로세스 peak RSS | 약 68.68 MiB |
| 15,000 ID 전체 페이지 순회 | 약 0.268초, 중복 없음 |
| ID 조회 median | 0.0037 ms |
| 첫 50개 median | 0.1499 ms |
| 단계별 50개 median | 3.8348 ms |
| 한국어 접두어 50개 median | 2.8863 ms |
| 일본어 접두어 50개 median | 2.8766 ms |
| 예문 관계 조회 median | 0.0097 ms |

세부 환경/p95/쿼리 계획은 `Docs/PERFORMANCE.json`. 30회 warm 반복이며 iPhone cold launch/스크롤 성능을 측정한 것은 아닙니다. 20,000 어휘도 generator의 --count로 확장할 수 있지만 이번 실제 대규모 측정은 15,000개입니다.

## 8. 변경/추가된 주요 파일

- `Content/content-schema-v2.sql`, `ContentPackageValidator.swift`, 작은 fixture/production JSON과 번들 DB
- `Tools/ContentBuilder/source_reader.py`, `validator.py`, `build_content.py`, `migrate_source_v1.py`
- `generate_synthetic.py`, `benchmark.py`, `test_validation_v2.py`, `test_large_content.py`, 기존 테스트의 v2 계약 반영
- `Models/ContentTaxonomy.swift`, `ContentModels.swift`, ContentRepository protocol/SQLiteContentRepository 검색 API
- `Persistence/SQLiteConnection.swift` backup API, `UserDatabaseMigration.swift`, `Resources/user-migration-v2.sql`
- `Tests/FoundationTests.swift`, `Tests/Fixtures/content-v1.sqlite`, `source-v1.json`
- `Tools/generate_project.py`, 재생성된 `.xcodeproj`, 설정 화면 개발 단계 표시
- `CONTENT_GUIDE.md`, README, ARCHITECTURE, VALIDATION, TEST_RESULTS, PERFORMANCE, 이 상태 문서

## 9. 알려진 문제·미구현

1. **실제 Xcode 빌드/네이티브 테스트 미검증**. 다음 단계 우선 작업입니다.
2. 실제 교육 콘텐츠는 작은 개발 fixture만 있고 Release는 빈 DB입니다. 출시 가능한 교육 상품이 아닙니다.
3. 자동 검증은 한국어/일본어 자연스러움·교육적 정확성·출처 신뢰도를 입증하지 않습니다. DATA 단계 검수 필요.
4. 검색은 정규화된 **접두어 검색 API**이며 아직 검색 UI/FTS/형태소/퍼지 검색은 없습니다.
5. 과정/레슨 메타데이터는 일괄 조회, 단어별 예문은 최대 100개입니다. 필요 시 해당 API 페이지 확장.
6. prerequisite 그래프 전체 순환 검증은 미구현입니다. alias 순환은 검사합니다.
7. 미디어 파일/해시는 검증하지만 앱 리소스 자동 복사·오디오 다운로드·재생은 미구현입니다.
8. 원격 콘텐츠 업데이트/서명 검증, 사용자 백업 복구 UI/내보내기/클라우드 동기화, migration backup 정리 정책은 미구현입니다.
9. source validation의 중복 후보/업데이트 fingerprint는 도구에서 O(N) 메모리를 사용합니다. 앱 시작 시 대규모 JSON을 로드한다는 뜻은 아닙니다.
10. source의 metadata/일반 TEXT가 과도하게 길거나 손상된 경우 거부하지만 linguistic quality의 모든 문제를 자동 찾을 수는 없습니다.
11. 앱 아이콘/최종 브랜드/배포 서명/스토어 준비는 미구현입니다.
12. 전체 학습 세션·회독·SRS·작문 채점·문법 UI·TOPIK 전체·광고·IAP는 이번 범위에 따라 구현하지 않았습니다.

## 10. 다음 DEV/DATA 주의사항

1. Mac에서 `Tools/verify.sh`와 `⌘U`로 Debug/Release 및 XCTest 10개를 먼저 실행합니다. 문제가 있으면 재현 로그와 수정 내용을 기록합니다.
2. `CONTENT_GUIDE.md`를 먼저 읽고 동일 source 계약을 사용합니다. 데이터를 Swift 배열이나 UserDefaults로 대체하지 않습니다.
3. fixture/synthetic/production dataset과 사용자 파일을 섞지 않습니다. 성능용 fake 데이터를 실제 단어장으로 배포하지 않습니다.
4. DATA 추가는 전체 manifest + 이전배포 --previous 검증으로 진행하고 ID·tombstone을 유지합니다. 콘텐츠 증가와 schema 변경을 구분합니다.
5. 새로운 enum/문제 유형을 추가하면 SQL·Python·Swift 및 답/채점 계약을 함께 변경하고 호환성을 시험합니다.
6. 새 검색 query로 바꾸면 pagination cursor를 초기화합니다. 화면 전체 어휘 preload를 만들지 않습니다.
7. 새 사용자 migration은 백업/rollback/과거 DB 회귀 테스트를 추가합니다. WAL DB 본체만 복사하거나 자동 reset하지 않습니다.
8. 이번 단계의 습득/체감 난이도는 저장 기반입니다. SRS나 습득 완료 알고리즘이 구현됐다고 가정하지 않습니다.
9. 실제 DATA 분량·학습 기능 범위는 다음 사용자 요청으로 확정합니다. 이번 단계에서 후속 콘텐츠를 임의로 선행 생성하지 않았습니다.

## TODO 기록

코드에 TODO/FIXME 마커는 없습니다. 미구현 사항은 위 9~10절에 기록했습니다. 기존 기능을 가짜 결과/임시 placeholder로 바꾸지 않았습니다.
