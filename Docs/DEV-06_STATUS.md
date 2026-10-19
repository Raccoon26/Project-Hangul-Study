# PROJECT_STATUS — DEV-06

**SRS 기반 장기복습 엔진과 DEV-05 회독 연동**을 구현했습니다. 2026-10-01, 45분 제한 작업입니다. DEV-05 상태는 `Docs/DEV-05_STATUS.md`에 보존했습니다. 새 어휘나 별도 콘텐츠 source를 만들지 않았으며 Content DB/Importer/Validator/한글·발음·음성 구조를 유지합니다.

## 구현한 흐름

`회독 세트 완료 → 기존 srs_state에 등록 → 예정일 도래 → 学ぶ / 今日の復習 → 실제 production 어휘 회상 → 意味を見る → 難しい / もう少し / 覚えた → 다음 예정일 저장 → 재실행 후 재개`

- 회독 완료와 SRS 등록은 **같은 SQLite transaction**입니다. 처음부터 `覚えてる`로 통과한 단어도 등록됩니다.
- DEV-05에서 이미 완료한 시도는 앱 시작 시 50시도 단위로 찾아 등록합니다. 완료 당시 시각을 firstLearnedAt으로 쓰며 과거 예정일이면 밀린 복습으로 나타납니다. 등록 마커와 `ON CONFLICT DO NOTHING`으로 중복 등록/재학습에 의한 기존 단계 초기화를 막습니다.
- 기존 사용자 DB의 `srs_state(content_id,skill)`를 그대로 사용합니다. 회독의 남은 ID/round와 SRS stage를 합치지 않습니다. 새 세션/결과 표도 같은 UserProgress 파일 안에 있습니다.
- 실제 DATA-01 vocabulary, ordered meanings, 연결 example, note를 기존 ContentRepository에서 ID 단건 조회합니다.
- 한 복습 세션은 기본 20개, 저장소 상한 30개입니다. 총 due 수는 따로 표시하고, 세션을 시작해도 미진행 항목은 사라지지 않습니다.
- 복습 화면도 뜻 공개 전 결과 선택을 금지합니다. 의미 공개·결과 확정·현재 위치가 디스크에 저장됩니다.

## 버전 / 저장

| 대상 | DEV-06 |
| --- | --- |
| Content schema / content / reader | **3 / 5 / 4 유지** |
| Production 어휘 / 의미 / 신규 문장 | **226 / 244 / 447 유지** |
| UserProgress schema | **4 → 5** |
| SRS algorithm / algorithm_version | **calendar_steps / 1** |

`Resources/user-migration-v5.sql`은 새 세션/결과 표와 인덱스만 추가합니다. 기존 srs_state, 회독, 한글/발음 세션, 즐겨찾기, 정오답 이력을 삭제하지 않습니다. 기존 migration 전 WAL 포함 SQLite backup, transaction, 미래 버전 거부 정책을 유지합니다. Content DB로 FK/cascade delete는 없습니다.

## 단계형 SRS 정책

`StepReviewScheduler`는 독립적인 순수 Swift 달력 계산입니다. 간격 배열은 **[1, 3, 7, 14, 30, 60, 120]일**, stage는 0~6입니다.

| 동작 | 단계 | 다음 예정일 |
| --- | --- | --- |
| 회독 최초 완료 | 0 | 다음 달력 날짜 자정 |
| 覚えた | 1단계 상승, 최대 6 | 새 단계의 간격 후 자정 |
| もう少し | 현재 단계 유지 | 현재 간격과 3일 중 짧은 간격 후 자정 |
| 難しい | 0으로 복귀 | 다음 달력 날짜 자정 |
| stage 6에서 覚えた | 6 유지 | 120일 뒤 다시 복습, 삭제하지 않음 |

간격은 **실제 판정일 기준**입니다. 밀린 복습을 수행한 뒤 옛 예정일에 간격을 더해 즉시 또 due로 만드는 방식이 아닙니다. 연속 성공은 覚えた에서 증가하고 다른 결과에서 0이 됩니다. failureCount는 難しい에서만 증가합니다. reviewCount는 결과 확정 1회당 1 증가합니다.

회독 직후 이미 본 카드를 또 정답으로 기억하는 상황을 줄이기 위해 SRS의 첫 간격을 다음 날로 정했습니다. 처음 알고 있던 단어도 강한 장기기억으로 추정하지 않고 모두 stage 0부터 시작합니다. 여러 회독이 필요했는지는 `neededRepetition`으로 보존해 향후 초기 정책을 조정할 수 있습니다. 이번에는 검증되지 않은 차등 초기 단계를 적용하지 않았습니다.

**같은 날 재학습 queue는 이번에 추가하지 않았습니다.** 難しい는 같은 세션에 재삽입하지 않고 다음 날로 예약합니다. 고정 session snapshot에서 각 ID는 한 번만 판정하므로 즉시 재등장/무한 반복이 없습니다. 달력 기준이라 자정 직전에 판정하면 다음 복습까지 24시간보다 짧을 수 있습니다. 최소 경과시간 기반 재학습은 후속 정책 버전에서 검토해야 합니다.

이 간격은 이해하기 쉬운 첫 제품 정책이며 과학적으로 최적화·개인화된 알고리즘이라고 주장하지 않습니다. SM-2/FSRS/AI 개인화는 구현하지 않았습니다.

## 상태 모델

기존 srs_state의 `state_json`에 `SRSState`를 저장합니다.

- stage, nextReviewAt, lastReviewedAt
- reviewCount, consecutiveSuccesses, failureCount, lastResult
- firstLearnedAt, optional difficulty(현재 nil, 0~1 예약)
- neededRepetition, schedulingTimeZone

콘텐츠 stable ID와 skill은 기존 행의 복합 PK입니다. JSON은 콘텐츠 본문 캐시가 아닙니다. due_at과 last_review_at도 기존 열에 저장하여 조회 시 JSON 전체를 파싱할 필요가 없습니다. JSON 단계·카운터·시각·timezone과 열의 due_at 일치 여부를 읽을 때 검사합니다. algorithm/version이 다른 상태는 덮어쓰거나 추정 변환하지 않습니다.

회독 완료/known이나 SRS 최상위 단계 때문에 acquisition_status를 acquired로 강제하지 않습니다. 정답/오답 퀴즈 지표에도 자기평가를 섞지 않습니다.

## 날짜 / 시간대

- 저장: Foundation Date의 UTC epoch instant. 날짜 문자열 하드코딩/locale 의존 parsing 없음.
- 간격 계산: 명시적 Gregorian Calendar + 판정 시의 TimeZone. 현재 현지 날짜 시작에 calendar day를 더합니다. 하루를 무조건 86,400초로 더하지 않아 DST에 대응합니다.
- 기존 due instant는 여행·timezone 변경으로 다시 쓰지 않습니다. 다음 판정 때 새 시간대를 사용합니다. 여행 중에는 화면의 현지 달력 날짜와 원래 예약 시간대의 자정이 다르게 보일 수 있습니다.
- due 조회는 `due_at <= now`. 일반적인 예약 시간대에서는 예정일 자정부터 due이며 미래 instant는 제외합니다.
- overdue는 현재 시간대의 오늘 시작보다 due_at이 이른 항목입니다. 오늘 완료 수는 현재 시간대의 [오늘 시작, 내일 시작) instant 범위로 셉니다.
- 결과에는 UTC reviewed_at과 당시 time_zone/local_day를 모두 기록합니다.
- 홈은 표시/복귀, calendar day 변경, UIApplication significant-time-change 알림에 요약을 갱신합니다. 매초 polling/background timer는 없습니다.
- 복습 도중 날짜/시간대가 바뀌어도 이미 저장한 session ID/순서는 재계산하지 않습니다. 새로운 예정일만 실제 판정 시각/시간대로 계산합니다.
- 시스템 시계를 이전 firstLearnedAt/lastReviewedAt보다 뒤로 돌리면 결과를 거부하고 기존 기록을 보존합니다. 미래 서버 시계 검증은 없습니다.
- DEV-05 과거 시도의 timezone은 별도로 저장되지 않았으므로 최초 backfill에는 업그레이드 당시 기기 timezone을 사용합니다. 과거 날짜를 정밀 복원했다고 주장하지 않습니다.

## Due query / backlog

`idx_srs_skill_due(skill,algorithm,algorithm_version,due_at,content_id)` 인덱스로 count 및 earliest-due 우선 LIMIT 조회를 수행합니다. 전체 progress를 메모리에 로드해 날짜 필터링하지 않습니다.

- 총 due 개수와 overdue 개수는 SQL COUNT.
- 시작은 오래된 due 순서와 stable ID tie-break, LIMIT 20(저장소 최대 30).
- 생성된 review_items에 ID/ordinal snapshot 저장. 시작 자체로 due_at을 옮기지 않음.
- 미판정 단어는 due 상태로 유지하며 active session 재개를 우선.
- 완료 후 남은 due가 있으면 `次の復習へ`로 다음 묶음. 새 단어 학습은 항상 선택 가능.
- 15,000개 SRS 행에서 10,000개 due count와 20개 선택, 지정 인덱스 사용·임시 정렬 없음을 Python/SQLite로 검사했습니다. iPhone 속도/메모리 실측은 미수행입니다.

## UserProgress의 새 표

| 표 | 목적 |
| --- | --- |
| srs_enrolled_passes | 등록한 vocabulary 시도 UUID; 과거 완료 backfill/중복 처리 마커 |
| review_sessions | UUID, skill, active/completed, 시작/갱신/완료 시각; skill당 active 1개 |
| review_items | session/content ID/ordinal, 노출/공개 시각, 결과, 판정 시각, 다음 예정일, 이전/다음 stage, timezone/local_day, 기존 study_event ID |
| 기존 srs_state | 유일한 장기복습 상태 저장소 |

노출은 기존 study_events의 viewed + item_progress/daily_statistics와 같은 transaction으로 기록합니다. 재개된 같은 session/card는 노출을 중복 가산하지 않습니다. `review_items`의 확정 결과는 review completed/result/next scheduled date 이력입니다. 별도 서버/Analytics SDK가 없습니다.

판정은 `srs_state 갱신 + review_items 결과 + session 완료/위치`를 한 transaction으로 처리합니다. 이미 확정된 session/content ID의 중복 제출은 첫 결과를 유지하며 다음 카드에 적용하지 않습니다. 공개 전/다른 카드 제출은 거부합니다. 저장 실패 시 UI는 판정을 멈추고 기록을 다시 읽습니다.

## UI / 기존 기능

- 홈 `今日の復習`를 `入門単語`보다 먼저 표시합니다. 전체 due 수, 시작/이어하기 버튼만 중심에 두었습니다. 새 단어 학습을 잠그지 않습니다.
- `VocabularyCardContentView`로 기존 어휘 카드의 한국어/뜻/예문/note/음성 표현만 분리하여 회독과 복습에서 공유합니다. 별도 vocabulary source나 TTS 엔진을 만들지 않았습니다.
- 정식 한국어는 큰 Dynamic Type 글자, 의미는 공개 후 표시, 시스템 배경/기존 포인트 컬러/full-screen/하단 action을 유지합니다.
- 세 판정 버튼은 충분한 높이의 세로 배치입니다. VoiceOver label/hint, 색상과 독립적인 텍스트를 제공합니다. 애니메이션을 추가하지 않았습니다.
- Audio Service normal/slow/stop, recorded-required 및 ko-KR/녹음 없음 fallback을 재사용합니다. 카드 이동/닫기/background에서 중단합니다.
- `記録`에는 오늘의 복습 완료 수와 overdue 수만 추가했습니다. 복잡한 통계 dashboard는 아닙니다.
- 한글·발음 UI/engine/Audio Service와 production content는 기존 그대로입니다. 회독 완료 hook과 공유 카드 추출 외 기존 회독 정책을 바꾸지 않았습니다.

## 실제 검증 결과

- **Python/SQLite 116개 통과**: 기존 104개 + 신규 SRS SQL 12개. 로그 `Docs/TEST_RESULTS_DEV06.txt`.
- 신규 SQL 검증: due 경계/미래 제외, 15,000개 backlog 인덱스/20개 제한, 재등록 보존/skill 분리, 공개 gate, 디스크 재개, 결과/예정일/완료 원자성, 실패 rollback, active 세션 제약, 날짜 범위 집계, v4→v5 기존 진도 보존, backfill 마커, 실제 repository SQL compile 및 콘텐츠 FK 부재.
- 기존 suite에는 15,000 vocabulary/30,000 examples Importer 및 한글·발음·회독 SQL 회귀가 포함됩니다.
- Production Validator: **오류 0 / 기존 경고 8**, `Docs/DEV06_CONTENT_VALIDATION.json`. Source/DB 바이트는 DEV-05와 같습니다.
- Swift **45개 파일** tree-sitter 구문 검사, plist/XML, Xcode 참조/리소스 및 SQLite integrity/FK 검사 완료. `Docs/STATIC_CHECKS_DEV06.txt`.
- Native **SRSTests 16개 추가**, 전체 XCTest **58개 작성**: 초기 등록, 최초 known, 단계/최상위 유지, unsure/failure, 자정, DST 23/25시간, timezone, clock rewind, 재등록/반복 회독 보존, 반복 필요 flag, due, 공개/재개/중복 판정, backlog, 과거 완료 backfill.

**미수행:** Linux에 Swift compiler/Xcode/iOS simulator가 없습니다. Swift type-check, Debug/Release build, XCTest 실행, 실기기 UI/VoiceOver/음성, 실제 앱 강제 종료·재실행과 OS 날짜 알림 전달은 실행하지 못했습니다. Python SQL과 구문 검사는 Swift 실행을 대체하지 않습니다. Native 테스트를 작성했다고 실행 통과로 기록하지 않습니다.

Mac 실행: `TEST_DESTINATION='platform=iOS Simulator,id=실제ID' sh Tools/verify.sh`. 상세 수동 확인은 `Docs/VALIDATION_DEV06.md`.

## 주요 변경 파일

- Models/SRSModels.swift / LearningEngine/StepReviewScheduler.swift
- Repositories/SQLiteReviewProgress.swift / 기존 SQLiteVocabularyProgress 완료 hook
- Resources/user-migration-v5.sql / UserDatabaseMigration / RepositoryProtocols
- Services/AppContainer.swift — 과거 완료 backfill
- ViewModels/ReviewViewModel.swift / AppModel.swift
- Views/ReviewSessionView.swift / VocabularyCardContentView.swift / LearnView / RecordsView
- 기존 VocabularyStudySessionView — 같은 카드 View 재사용, 완료 안내
- Tests/SRSTests.swift / 기존 Foundation·VocabularyPass의 버전/등록 기대값
- Tools/ContentBuilder/test_srs_sql.py / generate_project.py / Xcode project
- README / CONTENT_GUIDE 16절 / DATA_PROGRESS / ARCHITECTURE

DEV-01의 ReviewScheduling/ReviewState 계약은 보존했지만, quiz StudyOutcome으로 세 자기평가를 억지로 매핑하지 않습니다. 실제 DEV-06 정책은 StepReviewScheduler + ReviewRating입니다.

## 알려진 한계 / 다음 단계

1. Mac native build/XCTest와 실기기 검증을 먼저 수행해야 합니다. 특히 최대 Dynamic Type에서 하단 3개 버튼/ScrollView, 시뮬레이터 날짜 변경/재개, Korean TTS 청취를 확인하세요.
2. 같은 날 짧은 재학습 queue, 학습량 제한 개인화, 최적 interval 추정은 미구현입니다. 현재 실패는 다음 날입니다.
3. 누락/비활성 콘텐츠는 기록을 삭제하지 않고 해당 세션을 멈춥니다. retired-ID/alias 처리·명시적 skip/세션 해제 정책은 후속 작업입니다. 자동 습득 처리하지 마세요.
4. 알고리즘 변경 시 algorithm_version과 기존 state migration을 함께 설계해야 합니다. 기존 due를 무조건 다시 계산하거나 재학습 완료로 낮추지 마세요.
5. 날짜 경계는 달력 날짜이므로 24시간 고정 간격이 아닙니다. 여행은 기존 UTC 예정일 보존 정책입니다. UI에 예정일 표시를 추가할 때 이 정책을 유지하세요.
6. grammar/pronunciation/listening/sentence는 기존 (content_id,skill) 키와 독립 StepReviewScheduler를 사용할 수 있습니다. 현재 selector/presentation만 vocabulary 전용입니다. 다음 확장에서는 skill별 대상 조회/화면을 추가하며 새 progress DB를 만들지 마세요.
7. 기록은 로컬이며 앱 삭제/기기 분실용 cloud sync/export는 없습니다. 집중 시간을 측정하지 않아 duration_ms=0입니다.
8. AI/SRS 개인화, grammar 전체 과정, TOPIK, 광고/IAP/서버/로그인/신규 대량 DATA/발음 채점은 이번에 구현하지 않았습니다.

새 TODO/FIXME 코드 마커나 가짜 학습 결과를 넣지 않았습니다.
