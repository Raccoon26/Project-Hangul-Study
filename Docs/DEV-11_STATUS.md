# PROJECT_STATUS — DEV-11

2026-10-04 구현 후 중단, 2026-10-05 재개하여 검증·안정화·문서화를 진행했다. DEV-10 기록은 `Docs/DEV-10_STATUS.md`에 보존했다.

**실행 환경은 Linux이며 Swift compiler/Xcode/iOS Simulator가 없다. Python/SQLite 실행 검사와 Swift 구문 검사는 수행했지만, Xcode build/type-check/XCTest/실기기 UI·음성·VoiceOver를 실행했다고 주장하지 않는다. 출시 전 Mac/iPhone 검증이 필요하다.**

## 구현 범위

- 기존 단어 탭을 `調べる`로 연결했다. 한국어 어휘·표현, 모든 활성 일본어 meaning, 문법 표기·핵심 의미·일본어 설명을 검색한다.
- 단어 상세: 실제 card의 핵심/복수 의미·예문·사용/뉘앙스·note, 추가 예문, 발음 표기(있는 경우), 주요 활용, 관련어/문법, 음성, 저장, 재학습, 기존 코스 진입.
- 문법 상세: 기존 GrammarCard의 의미·형태·설명·조건·예문·일본인 note·비교 문법과 관련 어휘 이동. production 상세/엔진을 새 데이터 배열로 대체하지 않았다.
- 학습관리: 즐겨찾기/어려운 항목/최근 본 항목, 전체/단어/문법 필터, 페이지 조회, 누락된 즐겨찾기 콘텐츠의 안전한 안내·해제.
- 단일 상세 또는 목록의 최대20항목을 기존 Review UI·상태 전이·문법 채점 엔진으로 수동 연습한다. 신규 독립 학습 엔진이 아니다.
- 홈에 새 dashboard/card를 추가하지 않았다. 기존 Curriculum/학습/기록/설정 경로를 유지했다.

## 검색 구조 / Query / Ranking / 성능

`SQLiteContentRepository.lookup`이 read-only Content DB에서 SQL CTE로 후보를 검색한다. exact=0 → prefix=1 → substring=2를 항목별 최소값으로 계산하고 표제어/문법 표기, stable ID로 순서를 고정한다. 일본어 복수 meaning은 모두 대상이다. Example 일본어 번역, note 전체, 활용형은 검색 대상이 아니다.

입력 NFC/앞뒤 공백 제거/소문자, 최대100자. 빈 입력은 전체 DB 목록을 반환하지 않는다. `%`, `_`, 따옴표는 LIKE wildcard나 SQL이 아닌 문자 그대로 취급한다. 바인딩 파라미터만 사용한다. 한국어 활용형→기본형 자동 분석, 오타 교정, 초성 검색, 일본어 표기 변형 자동 동의어 검색은 구현하지 않았다.

300ms debounce, 취소 및 generation token으로 늦은 결과를 버린다. 검색/즐겨찾기는30행씩, 관련 항목20개, recent최대30개, 수동 연습20개. SQL은 substring 후보 scan이므로 모든 검색이 인덱스 seek라는 주장은 하지 않는다. 기존 PK/관계 index를 활용하고 Content schema/index 변경은 하지 않았다. 반환 페이지 이외 텍스트를 Swift에서 전체 로드/필터링하지 않는다.

`Docs/PERFORMANCE_DEV11.json`: 실제 production 검색 중앙값 약0.22~1.01ms. 별도 temporary synthetic vocabulary15,000 / examples30,000 / grammar500에서 약4.41~57.91ms, 측정 최대59.90ms. 10회 SQL 측정이며 iPhone UI, 디스크 cold start, 추가 상세 row 조회까지 포함한 성능이 아니다. fixture를 앱 bundle에 넣지 않았다.

## 상세 / 관계 / 활용 / 음성

VocabularyCard와 GrammarCard를 재사용한다. 관계는 explicit related/synonym/antonym/confusable 및 similar/contrast, 공유 Example의 vocabulary↔grammar 참조에서 조회한다. generic ‘関連する’로 표시하여 공유 예문만으로 유의어라고 주장하지 않는다. 목적지 kind와 active ID를 다시 검사한다. 없는 ID/meaning 손상은 오류 안내와 뒤로가기/재시도, 없는 note/관련어/활용은 빈 section을 만들지 않는다.

활용은 `ConjugationEngine.generate`의 현재·과거·미래를 사용한다. 기존 production question의 검수된 override를 읽고 충돌하는 override는 오류로 거부한다. 지원하지 않는 품사/불규칙의 형태는 추측해서 만들지 않는다. noun에는 활용표가 없다. 상세만을 위한 별도 활용 규칙이나 DB 저장 형태를 만들지 않았다.

기존 VocabularyCardContentView/GrammarExampleView와 KoreanAudioService의 normal/slow/stop을 재사용한다. 상세가 사라지거나 background로 가면 stop한다. 서비스의 기존 play-before-stop 및 generation 정책을 유지한다. 실제 한국어 voice 재생·속도·발음 품질은 미검증이다.

## UserProgress / Favorites / Recent / Difficult

**Content schema4 / content13 / reader7 유지, UserProgress8→9**. Content source와 DB는 DEV-10 ZIP과 byte-for-byte 동일하다. 기존 UUID/정렬/세트 membership/Content Version을 변경하지 않았다.

`user-migration-v9.sql`은 기존 favorites에 content_type(vocabulary/grammar)을 추가하고 recent_content를 생성한다. 이전 즐겨찾기 UI는 vocabulary 전용이었으므로 기존 행은 vocabulary로 보존한다. 전역 콘텐츠 UUID는 기존 PK(content_id)로 중복 방지하며 kind도 저장·조회·삭제 조건에 포함한다. 별도 Content DB flag나 즐겨찾기 데이터베이스는 없다. 기존 migration backup/transaction 정책을 사용한다. 생성된 Xcode project에 v9 resource를 포함했다.

최근 본 항목은 (stableID,type) upsert 후 최신30개만 보존한다. 조회 기록은 학습 event/SRS/회독/완료 수를 변경하지 않는다. 실제 학습을 시작한 뒤에는 기존 엔진의 노출/문제 결과 기록이 동작한다.

어려운 항목은 기존 SRS에서 다음을 모두 만족해야 한다:

- vocabulary 또는 grammar, 현재 scheduler algorithm/version
- last_review_at이 현재~과거30×24시간 범위
- failureCount>=2, consecutiveSuccesses<2, stage<4
- 마지막 결과 difficult 또는 unsure

한 번의 오래된 실패로 영구 고정하지 않는다. 최근 remembered, stage4 이상, 성공 연속2회, 오래된 실패는 제외한다. 이것은 예정된 SRS 결과 기준이며 수동 연습 오답만으로 이 목록을 바꾸지 않는다.

## Favorites / Difficult → Learning 재진입 정책

기존 review_sessions/review_items에 `vocabulary_practice` 또는 `grammar_practice` scope를 사용한다. 읽을 때 base kind와 isPractice로 구분하여 기존 카드/문제/노출/공개/판정 로직을 재사용한다. 예정된 vocabulary/grammar review session과 유일키가 충돌하지 않는다.

- 한 종류당 미완료 수동 연습1개. 이미 진행 중이면 새 목록으로 덮어쓰지 않고 그 snapshot을 재개한다. UI에 이 정책을 표시한다.
- 상세는1항목, 목록은 현재 로드된 항목 중 해당 kind의 앞20개를 연습한다. 모든 즐겨찾기를 자동 순회하는 별도 queue는 없다. 목록의 다른 항목은 상세에서 개별 연습 가능하다.
- 문제·선택·reveal·result는 기존 review tables에 저장한다. 앱 재시작 후 같은 session ID/현재 item/공개 상태로 재개한다. 홈 Continue도 practice UUID로 라우팅한다.
- 수동 연습은 **기존 SRS를 초기화하거나 stage/due를 바꾸지 않으며 새 SRS도 등록하지 않는다**. 이번 결과는 practice session에만 저장한다. 아직 정규 학습하지 않은 항목은 상세의 ‘コースで順番に学ぶ’에서 기존 회독→SRS 경로를 이용할 수 있다.
- practice review_items의 next_due_at/stage 값은 기존 CHECK를 충족하는 참조 값이며 실제 예약이 아니다. 예약의 유일한 기준은 srs_state다. 새 SRS가 없는 경우 initial 기준값만 결과 행에 기록한다. 향후 통계는 session의 *_practice scope를 구분해야 한다.
- 수동 연습이 grammar curriculum 완료로 오인되지 않도록 grammar SRS를 생성하지 않는다. 기존 Vocabulary set/Grammar round 기록도 수정하지 않는다.

## Integration Audit

상세: `Docs/DEV11_INTEGRATION_AUDIT.md`. 실행 로그: `Docs/TEST_RESULTS_DEV11.txt`.

- Python/SQLite 전체191개 PASS. 신규11개는 실제 repository SQL로 한국어/일본어/복수 의미/문법 설명/순위/페이징/관계/typed lookup, v8→v9 favorite 이관/중복/삭제/cold reopen, recent 제한·진도 독립, difficult 회복/시간 범위, practice/scheduled scope 분리, override 충돌 부재를 검사한다.
- 기존 Curriculum/Hangul/Pronunciation/Vocabulary/Grammar/Production/Listening/SRS/Content update SQL regression을 함께 실행했다.
- Swift75파일 구문 오류0. XCTest94개 작성, **미실행**(신규6개). 새 native tests는 실제 검색/활용일치/즐겨찾기 재실행/수동 어휘 SRS 불변/문법 quiz practice·완료 비오염/지연된 카드 조작 거부를 포함한다.
- Xcodeproject generator app65/test10 소스 + v9 migration resource. 네이티브 컴파일 및 UI tests는 미실행.

## Bugs Found

- 기록 화면의 ‘保存した単語’가 이제 문법도 포함하는 합계를 잘못 설명함.
- 비동기 상세 조회 결과가 빠른 항목 전환 후 이전 데이터로 UI를 덮어쓸 가능성.
- 큐에 늦게 실행된 복습 판정/정답 공개가 다음 카드에 적용될 가능성.
- 수동 연습에 기존 SRS 버튼 hint/완료 문구를 그대로 사용하면 복습 예정일이 변경됐다고 오해할 수 있음.
- v9 migration 파일을 코드에 추가해도 명시적인 project resource 목록에 빠지면 실행 시 migration 누락 오류가 됨(패키징 감사에서 발견).

## Bugs Fixed

- 기록 합계 label을 ‘保存した項目’로 변경.
- 상세 로드 generation/cancellation 확인 후 한 번에 결과 반영. 검색도 동일한 늦은 결과 방어.
- 버튼 렌더링 당시 item/question ID를 전달하고 ViewModel에서 현재 ID와 비교. 기존 DB idempotency guard 유지.
- 수동 연습 전용 제목/완료/hint로 SRS 미변경 정책을 명확히 표시. 학습 event skill도 practice로 구분.
- generator/Xcode project에 migration v9 포함, native migration test 기대 버전9로 갱신.

이는 소스·SQL 감사에서 확인한 위험과 수정이다. iOS에서 UI 버그를 재현·검증했다는 뜻은 아니다.

## Known Remaining Issues / 다음 단계

- Xcode build/type-check/XCTest94개와 실기기 navigation/keyboard/빠른 tap/Audio/VoiceOver/Dynamic Type 검증이 남아 있다. 구문 검사만으로 production 배포 가능을 보증하지 않는다.
- 수동 연습은 existing Review 재사용이다. 별도의 favorite-only 압축 회독이나 ‘수동 연습 결과로 SRS 재예약’은 지원하지 않는다. 기존 일정 보호를 우선했으며 UI와 위 정책에 명시했다.
- 누락/비활성 콘텐츠는 학습기록을 삭제하지 않고 안전한 오류로 남긴다. 해당 항목이 포함된 미완료 연습은 콘텐츠 복구 전 끝낼 수 없으며 닫기/다른 모듈 학습은 가능하다. 자동 skip/기록 삭제는 구현하지 않았다.
- 검색은 literal substring이고 OFFSET page이다. 최종 규모에서의 Linux SQL 성능은 측정했지만 구형 iPhone 성능과 여러 meaning 수가 더 늘었을 때는 별도 측정 필요. 필요하면 향후 제작 단계의 검색 인덱스를 확장한다.
- 상세에는 기존 Card의 bounded 제한(의미10/단어예문100/문법예문6/비교6/관련20)을 적용한다. 무제한 사전 페이지가 아니다.
- DEV-10의 상급 콘텐츠 부재/간이 진단/mixed Unit 미구현 한계도 유지한다.
- 신규 코드에 TODO/FIXME/dummy result 없음. 미검증 또는 미지원 사항을 숨기지 않고 이 절에 기록했다.

## 주요 파일

Models/LibraryModels.swift, Models/SRSModels.swift, Repositories/SQLiteLookup.swift, SQLiteSavedContent.swift, SQLiteReviewProgress.swift, SQLiteGrammarProgress.swift, SQLiteCurriculum.swift, RepositoryProtocols.swift, ViewModels/LookupViewModel.swift, ReviewViewModel.swift, GrammarViewModel.swift, Views/LookupView.swift, LookupDetailView.swift, RootView.swift, VocabularyListView.swift, ReviewSessionView.swift, GrammarReviewView.swift, CurriculumResumeView.swift, RecordsView.swift, Persistence/UserDatabaseMigration.swift, Resources/user-migration-v9.sql, Tests/LookupTests.swift, Tools/ContentBuilder/test_lookup_sql.py, benchmark_lookup.py 및 Xcode/문서. 전체 변경 목록은 Docs/CHANGES_DEV11.txt.
