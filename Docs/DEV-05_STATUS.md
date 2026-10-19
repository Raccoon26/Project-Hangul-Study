# PROJECT_STATUS — DEV-05

DEV-01~04와 DATA-01을 유지하면서 **회독 기반 실제 어휘 학습**을 추가했습니다. 이전 DATA-01 상태는 `Docs/DATA-01_STATUS.md`에 보존했습니다. 2026-10-01 작업. 중단 후 저장된 구현과 테스트 결과를 확인해 마무리했습니다. 활성 작업시간 45분 제한을 기준으로 새 기능 추가 없이 최종 검토·문서화·전달을 진행했습니다.

## 구현한 흐름

`学ぶ → 入門単語 → 新しいセットを始める / 続きから → 한국어 회상 → 意味を見る → 覚える / 覚えてる → 남은 단어만 다음 회독 → 完了 → 次のセットへ / もう一度見る`

- DATA-01의 **실제 226 vocabulary / 244 meanings / 447 예문**을 기존 read-only `Resources/content.sqlite`에서 조회합니다. 임시 단어 배열·새 source 포맷·중복 콘텐츠 저장소를 만들지 않았습니다.
- 기본 20개 단어로 세트를 생성합니다. 현재 전부 배정하면 20개×11세트 + 6개×1세트입니다. 이 수는 런타임에 하드코딩하지 않습니다. 전체 어휘 수는 SQL COUNT, 현재 세트는 실제 저장된 ID 개수입니다.
- 뜻을 공개한 뒤에만 판정합니다. `覚える`는 **다음 회독에 유지**, `覚えてる`는 **현재 시도에서 통과**입니다. 정답/오답 시험 점수나 영구 습득 판정이 아닙니다.
- 한 회독 안에서 틀린 단어를 끝에 계속 붙이지 않습니다. 회독 종료 화면에서 남은 수를 확인한 뒤 다음 회독으로 이동합니다. 20→8→3→0을 표현하는 순수 Swift 엔진을 구현했습니다.
- 다음 회독은 저장된 seed + stable set ID + 회독 번호로 섞습니다. 같은 seed/입력은 같은 순서입니다. 둘 이상 남으면 직전 마지막 단어가 바로 첫 카드가 되지 않게 조정합니다. 둘만 남으면 즉시 재등장 방지를 위해 이전 순서가 유지될 수 있습니다. 하나 남으면 명시적 다음 회독 버튼과 잠시 쉬어도 된다는 안내를 제공합니다.
- 마지막 회독의 남은 단어가 0이면 완료합니다. 완료 시도/세트 완료 횟수는 남고, 다시 보기는 새 시도 UUID/seed를 생성합니다. 진행 중 세트에 재시작 호출이 와도 기존 시도를 우선합니다.

## 아키텍처와 버전

기존 SQLite + actor repository + SwiftUI / @MainActor ViewModel 구조를 유지합니다.

| 대상 | 현재 | DEV-05 변경 |
| --- | --- | --- |
| Content schema | 3 | 없음 |
| Content version | 5 | 없음 |
| Reader contract | 4 | 없음 |
| UserProgress schema | **4** | v3→v4 비파괴 migration 추가 |
| Production source/DB/ID/Importer/Validator | DATA-01 그대로 | 바이트 보존 확인 |

Content DB는 읽기 전용입니다. UserProgress는 기존 Application Support의 같은 파일을 사용하고 migration 전 SQLite backup API로 WAL을 포함한 백업을 만듭니다. 새 v4 표도 콘텐츠 DB로 FK/cascade delete를 갖지 않습니다. 기존 한글·발음 세션, 정오답, 즐겨찾기, SRS 저장 표를 교체하거나 초기화하지 않습니다.

### 세트 구성

`VocabularySetCatalog`는 기존 ContentRepository의 `(sort_key,id)` keyset page를 **최대 100개씩** 읽고, 그 page의 ID 중 이미 사용자 세트에 배정된 항목을 제외합니다. 20개를 모으면 사용자 DB에 UUID와 멤버십을 한 번 저장합니다. DB rowid나 목록 offset을 학습 ID로 쓰지 않습니다.

- 세트 ID는 **사용자 학습 묶음의 로컬 영구 UUID**입니다. 콘텐츠 course/lesson ID를 가장하거나 source에 새 학습 문장을 복제하지 않습니다.
- `vocabulary_set_items`에는 실제 vocabulary stable ID와 그 세트 내부 표시 순서만 저장합니다. 이미 배정된 단어는 다른 새 세트에 중복 배정하지 않습니다. 다시 보기/SRS는 이 배정 제약과 독립적인 시도입니다.
- 콘텐츠 추가·정렬 변경·level 재분류가 기존 멤버십을 바꾸지 않습니다. 새 세트 생성은 처음부터 bounded scan하므로 앞쪽에 삽입된 새 어휘도 놓치지 않습니다.
- 전체 단어 corpus를 시작 시 메모리에 적재하지 않습니다. 세트 목록도 50개씩 페이지화하며, `続きから`는 가장 최근 active 세트 1개를 별도 조회합니다. 현재 카드는 ID로 한 개만 읽습니다.
- 세트 생성 시 scan은 총 배정량에 비례할 수 있습니다. 15,000개에서 최대 약 150개 page를 확인할 수 있으며, iPhone 실측은 미수행입니다. 향후 metadata/할당 인덱스를 최적화해도 영구 ID/저장 스키마를 재설계할 필요는 없습니다.

### 회독 상태 / 재개

`VocabularySession`은 시도 ID, set ID, 고정 vocabulary ID 목록, 시작 content version, seed, 시작/갱신/완료일, optimistic revision, 현재 회독, 현재 회독 순서, 위치, 이번 회독 통과 ID, 다음 회독 ID, 노출/의미 공개 여부, 총 노출, 현재 pass ID를 Codable snapshot으로 저장합니다. 위치는 **저장된 영구 ID 배열 내부 위치**이며 콘텐츠 DB row 순서가 아닙니다.

`vocabulary_sessions.state_json`은 단어 텍스트 캐시가 아닌 최대 25개 ID의 사용자 학습 상태입니다. 스냅샷 버전 변경이 필요하면 다음 사용자 migration으로 처리해야 합니다. 스냅샷 decode 시 중복·범위·집합 관계·공개/완료 상태를 검사하고 set 멤버십과 대조합니다.

매 카드 노출·의미 공개·판정·다음 회독을 동기적인 SQLite transaction으로 먼저 저장한 후 UI를 진행합니다. 13번째 카드에서 닫으면 동일 세트/회독/ID/의미 공개 상태를 복구합니다. 이미 기록한 같은 카드의 재개를 새 노출로 중복 집계하지 않습니다. background/닫기 시점에만 뒤늦게 저장하는 구조가 아닙니다.

`expectedRevision`으로 오래된 동작을 거부합니다. 저장/조회 실패 시 다음 판정을 막고 `記録を読み直す`를 제공합니다. 콘텐츠 version이 바뀌어도 vocabulary 시도는 ID snapshot으로 재개하며 새 카드 노출 이벤트에는 현재 콘텐츠 version/revision을 기록합니다. 비활성/누락된 단어는 기록을 삭제하거나 임의 통과시키지 않고 안내 후 멈춥니다.

### 사용자 DB v4

| 표 | 용도 |
| --- | --- |
| vocabulary_sets | 로컬 set UUID, level, 표시 번호, 생성일, 완료 횟수 |
| vocabulary_set_items | set → 실제 vocabulary stable ID, 고정 순서; content ID 전역 중복 배정 금지 |
| vocabulary_sessions | 시도 UUID, set ID, bounded state JSON, optimistic revision, active/completed, 갱신일; 세트당 active 1개 |
| vocabulary_events | exposure / learn / known / round_completed / set_completed 로컬 이벤트 |
| 기존 learning_passes / pass_items | 실제 회독과 해당 회독의 단어 처리 상태 |
| 기존 study_events / item_progress / daily_statistics | viewed 노출, 항목별·일별 학습량 |

기존 `learning_passes.scope_content_id`는 이 경로에서 로컬 set UUID를 받습니다(콘텐츠 FK가 없는 legacy scope 필드). pass_number는 그 set의 누적 회독 번호, session.round는 이번 시도의 회독 번호입니다. `pass_items.completed_at`은 해당 회독에서 **판정을 마침**이며 통과 여부는 vocabulary_events의 learn/known으로 구분합니다.

노출 이벤트와 study_count, 일별 집계, JSON 상태는 하나의 transaction입니다. 판정과 pass 처리, 회독/세트 완료 이벤트, 완료 횟수도 하나의 transaction입니다. 중간 실패는 모두 rollback합니다. 자기평가는 correct/incorrect로 기록하지 않으며, known에서 item_progress.completed_passes만 증가합니다. acquisition_status, perceived_difficulty, srs_state, due_at은 변경하지 않습니다. 실제 체류시간을 측정하지 않아 duration_ms는 0입니다.

## UI / 음성

- 기존 일본어 UI, 시스템 배경, indigo 포인트, native List/ScrollView, 하단 safe-area 버튼, SF Symbols를 유지했습니다.
- 학습은 full-screen으로 Tab Bar를 숨깁니다. 헤더는 닫기·세트·회독·카드 수, 얇은 진행 표시입니다.
- 한국어는 Dynamic Type 대응 큰 글자, 품사는 보조 표시입니다. 처음에는 일본어 의미를 View hierarchy에 넣지 않습니다.
- 공개 후 ordinal이 낮은 의미와 **그 의미에 연결된 실제 예문** 1개를 먼저 표시합니다. 추가 의미는 `ほかの意味` disclosure, 사용 설명/뉘앙스와 일본인용 note는 있을 때만 표시합니다. 현재 note는 첫 항목을 보여줍니다.
- `覚える / 覚えてる` 두 판정 버튼은 의미 공개 후에만 나타납니다. VoiceOver label/hint, 최소 44pt 음성/닫기 버튼, 큰 주요 버튼, 화면 폭/글자 크기에 따라 세로로 배치 가능한 버튼을 사용합니다. 애니메이션을 추가하지 않아 Reduce Motion에 별도 효과가 없습니다.
- 기존 **KoreanAudioService** normal/slow/stop을 재사용합니다. 실제 어휘·문장은 기본 시스템 TTS이며 콘텐츠에 명시된 recorded-required/tts 정책이 있으면 우선합니다. 검증 녹음/시스템 음성을 구별해 표시합니다. 자모 TTS 금지와 ko-KR 없음/녹음 누락 fallback을 유지합니다.
- 기존 기록 화면의 설명에 어휘 노출 집계와 자기평가/정오답 구분을 추가했습니다.
- 카드 이동·닫기·background에서 재생을 중단합니다. 학습 완료에 XP/코인/축하 애니메이션은 없습니다.

## 검증 결과

실제 수행한 검증:

- **Python/SQLite 104개 테스트 통과**: 기존 92개 + DEV-05 SQL 테스트 12개. 최종 로그: `Docs/TEST_RESULTS_DEV05.txt`.
- 새 SQL 테스트: production 226개 전체 의미/예문/65 notes 조회, 세트 멤버십/배정 충돌 rollback, 12개 bounded 세트 분할, JSON byte-preserving 재개, 한 active 시도/이벤트 제약, 완료 transaction rollback, 반복 이력, v3→v4 기존 학습 기록 보존, 콘텐츠 교체 독립성, 최근 재개 세트, 실제 repository SQL 준비/실행.
- 기존 92개에는 대용량 synthetic 15,000 vocabulary / 30,000 examples, Importer/Validator/관계/한글/발음/기존 진도 SQL 회귀가 포함됩니다. Python에서 Swift 알고리즘이 실행된 것으로 해석하지 않습니다.
- 기존 Validator production + previous v4 비교: **오류 0 / 경고 8**. 경고는 기존 짧은 발음 예시 5개와 의도된 차/일/쓰다 동형어 3그룹으로 변경 없습니다. `Docs/DEV05_CONTENT_VALIDATION.json`.
- Swift 38개 파일 tree-sitter 구문 검사, Xcode 프로젝트 파일·리소스·scheme 연결, plist/XML, Content DB integrity/FK 및 DATA-01 원본/기존 코스·음성 파일 보존을 확인했습니다. 상세: `Docs/STATIC_CHECKS_DEV05.txt`.

**수행하지 않은 검증:** Linux에 Swift compiler / Xcode / iOS simulator가 없습니다. Swift type-check, Debug/Release 빌드, XCTest 실행, 실제 앱 실행/강제 종료 후 UI 재개, VoiceOver/Dynamic Type 실기기 화면, 실제 한국어 음성 출력은 미수행입니다. 구문 검사와 Python SQL 테스트는 이를 대체하지 않습니다.

새 native `VocabularyPassTests.swift` **13개**를 작성했습니다(기존 29개 포함 총 42개). 20→8→3→0, all-known/all-unknown, 공개 전 판정 거부, deterministic shuffle, 1/2개 경계, Codable 13번째 카드 재개, 잘못된 상태 거부, 실제 repository 재개/버전 변경/중복 판정/반복 이력, 실제 DB의 정렬·추가 후 기존 세트 보호, production catalog/card 조회를 다룹니다. 기존 Foundation migration 기대값을 schema 4로 갱신했습니다. **작성 완료이며 실행 통과를 주장하지 않습니다.**

Mac에서 `TEST_DESTINATION='platform=iOS Simulator,id=...' sh Tools/verify.sh`로 Debug/Release와 XCTest를 실행하세요. 수동 검증 절차는 `Docs/VALIDATION_DEV05.md`입니다.

## 주요 파일

- Models/VocabularyStudyModels.swift — 카드 상세, set/시도 snapshot, 판정/오류
- LearningEngine/VocabularyPassEngine.swift — 순수 회독 전이/순서 변경
- Repositories/SQLiteVocabularyContent.swift — ID 기반 실제 meaning/example/note/audio 조회
- Repositories/SQLiteVocabularyProgress.swift — 원자적 배정·저장·재개·이벤트
- Services/VocabularySetCatalog.swift — bounded page 기반 새 set 배정
- ViewModels/VocabularyStudyViewModel.swift — 저장 성공 후 표시/판정 진행
- Views/VocabularyStudySetsView.swift / VocabularyStudySessionView.swift — 목록·회상·공개·판정·회독/세트 완료
- Resources/user-migration-v4.sql, Persistence/UserDatabaseMigration.swift — 사용자 migration
- RepositoryProtocols, AppModel, LearnView, ContentTaxonomy, generate_project.py / .xcodeproj — 기존 구조에 연결
- Tests/VocabularyPassTests.swift / Tools/ContentBuilder/test_vocabulary_sql.py — 검증
- CONTENT_GUIDE.md 15절 / Docs/ARCHITECTURE.md / README.md — 제작·개발 인계

## 알려진 한계 / DEV-06 인계

1. **먼저 Mac build/XCTest 및 실제 UI·음성·재실행 확인이 필요합니다.** 현 환경에서는 컴파일 성공/출시 가능 품질을 인증할 수 없습니다.
2. 새로운 단어 집합은 현재 DATA의 sort_key 순서에서 아직 배정하지 않은 단어로 구성합니다. 편집자가 설계한 교육적 lesson/주제별 순서가 아닙니다. 앞으로 curated set을 추가해도 이미 시작한 사용자 ID snapshot을 다시 계산하지 마세요.
3. 신규 set 배정은 bounded-memory 순차 scan입니다. 모든 단어를 로드하지 않지만 전체 배정 후 새 단어를 찾는 CPU/IO 비용은 증가합니다. 실제 대용량 iPhone profiling 후 최적화하세요.
4. 회독 완료는 이번 회상의 자기평가입니다. future SRS는 known/learn, exposure, completed_passes 등과 별도 scheduling을 연결해야 합니다. 처음부터 known을 선택한 단어도 영구 제외하지 마세요.
5. 콘텐츠 tombstone/누락이 진행 중 set에 생기면 안전하게 멈춥니다. 자동 alias 병합·대체·skip 정책은 미구현이며 기록을 보존한 명시적 정책이 필요합니다.
6. 기록은 로컬입니다. 앱 삭제·기기 분실을 위한 별도 backup/export/cloud 기능은 이번 범위가 아닙니다.
7. 한글/발음 기존 lesson은 기존의 보수적인 content-version 재시작 정책을 유지합니다. vocabulary의 ID snapshot 재개 정책과 혼동하지 마세요.
8. 의미 최대 10개, note 최대 10개를 카드 조회하며 기본 의미/예문 1개와 첫 note 위주로 표시합니다. 사전 전체 보기 UI는 별도 범위입니다.
9. 외부 서버/Analytics SDK/로그인/광고/IAP/전체 SRS/신규 대량 DATA/발음 채점은 구현하지 않았습니다.

코드에 새 TODO/FIXME 마커를 남기지 않았습니다. 기존 기능을 fixture·placeholder로 대체하지 않았습니다.
