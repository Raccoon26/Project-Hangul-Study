# DEV-12 Requirements Coverage / Integration Audit

2026-10-05. 문서의 완료 표시를 그대로 인용하지 않고 앱 진입점, repository SQL, state machine, persistence, production DB와 테스트를 대조했다. 여기서 **구현**은 실제 소스 경로가 있다는 뜻이며 iOS에서 실행을 통과했다는 뜻은 아니다. Linux에서는 Swift compiler/Xcode가 없어 native build·UI·실제 TTS·알림 전달·VoiceOver 실행을 검증하지 못했다. 사용자 명세에 없는 DEV-10/11의 세부사항은 보관된 상태 문서/소스 계약까지 검토했다.

## Requirements Coverage Audit

| 요구사항 | 실제 근거 | 판정 / 남은 범위 |
| --- | --- | --- |
| Content/UserProgress 분리, Stable ID, schema/content version | AppContainer, SQLiteContentRepository, SQLiteProgressRepository, content_metadata | 구현. read-only bundle과 별도 user DB, cross-DB cascade 없음. content13/schema4/reader7 유지, user10 additive index migration |
| Importer/Validator/대용량 | ContentBuilder build_content.py/validator.py, source JSON, 15k fixture tests | 구현. 앱 시작 시 JSON import 안 함. 최종 규모 synthetic는 production와 분리 |
| Content update → 기존 progress | stable membership/snapshot, dataset guard, migrate+backup, release regression | 구현/이번 수정. 무관한 release가 한글/발음 재개를 막던 version-only 조건 수정. 삭제/비활성 ID의 자동 skip은 미구현 |
| 한글40자모/조립/읽기/받침 | production hangul55행(자모40 포함), HangulComposition, LessonSession | 구현. 독립 UUID, 일본어 설명, lesson/quiz 저장 |
| 발음 변화/비교/일본인 설명 | pronunciation_rules36, 14레슨, AudioPolicy | 구현. 자모/개별 비교는 TTS 차단, 녹음 미제공 안내. 검증된 녹음 실제 파일0: 부분 구현(Major 콘텐츠 공백) |
| 어휘 production/meaning/example/note | VocabularyCardContentView, SQLiteVocabularyContent | 구현. 표시 시 production DB 직접 조회, 복수 의미/예문 bounded query |
| 어휘 회독/뜻 공개/unknown-only/완료 | VocabularyPassEngine, SQLiteVocabularyProgress | 구현. 약20개 고정 membership, unknown 다음 회독, snapshot/revision. 지연 UI 입력 guard 이번 보완 |
| 회독 → SRS/최초 알고 있던 단어 | enrollVocabularyReview, backfillVocabularyReviews | 구현. INSERT conflict는 기존 일정을 보존. 회독 통과를 영구 습득으로 처리하지 않음 |
| SRS due/stage/backlog/date/timezone | StepReviewScheduler, SQLiteReviewProgress | 구현. 1/3/7/14/30/60/120일 calendar policy, 최대20/30 조회, 미래 due 제외, type별 key. 실패는 다음날이며 같은 날 무한 재시도 없음 |
| SRS 여러 타입 | vocabulary/grammar/listening skill, review_items/listening_attempts | 구현. 공통 scheduler, 서로 다른 typed ID. 새 단어 회독과 장기복습 상태 분리 |
| 문법 설명/형태/조건/비교/note/예문 | GrammarCard, GrammarExplanationView, SQLiteGrammarContent | 구현. production42개/95 grammar-example 관계. 무제한 사전식 상세는 아님 |
| 문법5종 문제/회독/SRS | GrammarQuestion, GrammarLearning, GrammarReviewViewModel | 구현. 실제 문제의 kind 선택, snapshot/revision, SRS에서 question rotation. 지연 UI next/answer guard 이번 보완 |
| 활용/불규칙/직접입력/문장생산 | ConjugationEngine, ProductionAnswer, ProductionSession | 부분(Major 범위). 지원하는 초급9형태/대표 불규칙/명시적 override, accepted answer/spacing, authored sentence 입력 있음. 전체 자유작문/모든 활용·예외를 처리하는 엔진은 아님 |
| 듣기 의미/Korean/받아쓰기/내용이해 | ListeningQuestion/Session, SQLiteListening, production111 | 구현. actual Example ID source, normal/slow/stop, 원문은 답변 후 view 생성, bounded1 retry, progress/SRS atomic |
| Audio optional/fallback/interruption | KoreanAudioService, vocabulary/grammar/listening views | 코드상 구현. voice없음/녹음없음 안전 상태, old playback generation 차단, 화면이탈/background stop, routechange/interruption 처리. 실제 음성은 미검증 |
| 학습 단계9종/Skip/Placement | LearningLevel, CurriculumProfile, PlacementView | 부분(Major).9단계 선택/skip/저장/8문항 간이진단. 진단은 하위3단계 제안이며 상급 능력 측정 아님. 初中級~マスター 실제 production curriculum 없음 |
| guided progression/Continue | CurriculumLevelView, curriculumResume, CurriculumResumeView | 부분(Major). lesson/level progression, module별 재개는 있음. 여러 미완료 세션 중 고정 모듈 우선순위이며 항상 가장 최근 활동은 아님. 혼합 Unit/일일 추천 스케줄러 미구현 |
| 한국어/일본어 검색/상세/관계 | SQLiteLookup, LookupViewModel, LookupDetailView | 구현. 한일 의미/문법 검색, 활용 detail은 기존 엔진, typed related query. literal substring이며 형태소/오타/초성검색은 범위 밖 |
| Favorites/Difficult/Recent | SQLiteSavedContent, SavedContentView | 구현. 즐겨찾기 typed, recent30, 최근 반복실패+회복 조건. 검색 자체는 학습/SRS 변경 없음. 수동 연습은 의도적으로 별도 일정 갱신 안 함 |
| Statistics | SQLiteStatistics, RecordsView | 이번 구현. 오늘/7/30일 actions/채점/예정복습, production/listening, 실제 active ID 기준 미학습, 회독/학습/SRS 분리. 시간 측정 안 함 |
| Maintenance | MaintenanceView, maintenanceWords, existing review/production/listening | 이번 구현. due 우선 진입/어려운 문법/입력/듣기, 오래된 미예약 단어10개. 혼합 adaptive session은 아님. SRS 대상은 별도 오래된 목록 제외 |
| Micro-session | LearnView → ReviewSessionView(sessionLimit), Settings | 이번 구현. 5/10/20어휘 preference, due only, 기존 진행 세션 우선. 문법/듣기는 기존 최대20개를 언제든 중단. 시간보장/혼합3분 세션은 없음 |
| Settings/Notifications | LearningPreferencesStore, SystemReminderBackend | 이번 구현. UserDefaults JSON, 알림 on/off/time, 명시적 toggle에서만 요청, denied/failure/revoked 정리. 실제 iOS 권한창/전달 미검증 |
| Offline/배터리/앱 시작 | localSQLite, AppModel, no network/timer/backgroundtask | 코드상 구현. home 전에 legacy 전체favorites/통계/단어목록 preload 제거. native cold launch·배터리 수치 미측정 |
| 접근성/조용한 UI | system fonts/ScaledMetric, labels, 44pt, bottomActions | 코드상 대부분 구현. production primary action 이번 하단 이동. Dynamic Type 극단 크기/VoiceOver/one-hand 실기기 QA 남음 |

## Integration Audit

- Content → vocabulary/grammar/listening: 전체 Python regression이 실제 bundle 조회/관계/enum/level/accepted answers/source reference를 검사한다. source/DB는 DEV11 ZIP과 byte-for-byte 동일.
- 회독 → SRS: 기존 SQLite/XCTest 계약 유지. 스케줄 등록·중복 방지·review partial snapshots 검사를 재실행/추가했다. native engine XCTest는 작성만 했다.
- Progress → Statistics: 실제 repository SQL을 빈 DB, 날짜 양끝/미래/다른 시간대, listening retry, manual practice, stage구분으로 실행했다. 자기평가를 정오답으로 만들지 않는다.
- Maintenance → review: 오래된 후보 조회는 existing SRS와 active round를 제외한다. active Content ID만 최대10개 재확인 후 기존 practice UI에 전달한다. 문법/입력/듣기는 existing engine navigation.
- Settings → Notifications: backend protocol으로 허용/거절/재요청 방지/취소/오류/권한회수/재실행 tests 작성. 이 mock XCTest는 Linux에서 실행하지 못했다.
- Search/Favorites → 학습/SRS: DEV11 tests 유지. favorites/recent 쓰기는 user table만. 수동 연습은 scheduled review와 독립 scope이며 existing due를 변경하지 않음.
- Conjugation/Listening → 입력: 기존 normalize/accepted answer/spacing/retry tests 유지. production UI의 지연 revision과 입력값 capture 보완.
- v9→v10 migration: index만 추가, 기존 모든 table row/JSON/SRS 보존 SQL 실행. 미래 schema/손상 dataset 복구를 이유로 삭제하는 코드 없음.

## Micro-session / Commute UX Audit

| 시나리오 | 코드/실행한 검사 | 기기에서 남은 확인 |
| --- | --- | --- |
| A 오늘복습5개→4개 제출→닫기→재개 | beginReview limit, 기존 active 우선, 20중4개 저장/16미완료 disk cold reopen SQL PASS.5개 native end-to-end test 작성 | 앱 force kill/feedback/홈 route/UI |
| B vocabulary3개→background→복귀 | 매 expose/reveal/decision JSON transaction, native cold reopen/round tests 기존 유지. 지연 revision guard 추가 | 실제 background interruption timing |
| C listening2개→닫기→나중에 | revision/answer/retry/heard snapshot과 original scope 재개; SQLite listening tests PASS | 화면 back/kill/replay 오디오 |
| D 음성 없이 단어/문법 | AudioService availability는 버튼/안내만 변경하며 판정 gate에 사용 안 함 | voice삭제/이어폰 없는 실제 화면 |
| E offline | source→번들DB, user localSQLite, network API/timer/polling 없음. 실제 DB 읽기 regression PASS | 기내모드 launch/TTS 설치별 출력 |

Home에서 저장된 Continue 또는 단어의 短く復習는1회 tap으로 학습 fullScreen 진입. 문법/듣기 복습은 Today Review 후 모드선택까지2회 tap. 신규 사용자 시작위치 선택은 추가 단계다. 시간은 보장하지 않으며 한 세션을 끝내야 저장되는 구조가 아니다. 현재 처리 중인 action은 중복 입력을 막고 transaction이 완료되면 닫을 수 있다. 입력 중 한글/선택 전 상태는 저장 보장하지 않지만 제출 결과는 저장한다.

주요 학습 버튼은 하단 safeAreaInset, 최소44pt/large control. production 화면의 primary 버튼도 이번 이동. no haptic/confetti, no timer/위치정보/백그라운드 polling. Stats는 해당 탭에서만 조회. 실제 배터리/한손/최대글자 시각 검사는 수행하지 않았다.

## Bugs Found / Bugs Fixed

- **Major 수정**: 레슨 stable ID/순서가 같아도 무관한 content version 증가만으로 resume 거부 → 내용 순서가 동일하고 release가 역행하지 않으면 동일 session ID/cursor/results 유지, 새 event에 최신 version 적용. 실제 step list 변경 시 기존 안전 차단 유지.
- **Major 방어 보완**: vocabulary/grammar/production/lesson UI action Task가 실행될 때 새 current state를 읽을 수 있음 → 표시 당시 revision/step+answered 상태로 검증. DB stale/idempotency와 별도로 UI를 보호. 실제 연타 UI 재현 미수행.
- **Minor 수정**: Settings DEV04 개발문구/SRS미지원 안내 → 현재 기능/정책으로 수정.
- **Minor 수정**: launch에서 사용하지 않는 legacy word50/favorite전체/누적통계를 먼저 기다림 → legacy 화면에만 lazy load, Home 경량 summary, Statistics on demand.
- **Minor 수정**: production primary action이 설명 아래 scroll 중간 → 하단 고정 action1개.
- **새 기능 감사 중 수정**: 기록의 vocabulary skill 명칭(`vocabulary_pass`) 및 production-only 노출 누락 수정; active ID별 미학습 count로 retired history에 의한 추정 방지; 알림 off인데 오래된 pending request가 남으면 reconcile에서 취소.

## Known Remaining Issues / 분류

1. **Critical 출시 검증 gate**: Swift type-check/Xcode build/104 XCTest 및 iPhone 실제 lifecycle/navigation/Audio/Notification/VoiceOver 미실행. 이는 재현된 crash라는 뜻이 아니라 출시 적합성을 아직 보증할 수 없다는 뜻이다.
2. **Major 콘텐츠 공백**: 최종 15k어휘/30k예문/350~500문법 대비 현재926/1876/42. 상급단계와 녹음 콘텐츠는 부족. 수년 전체 실제 curriculum이 완성되었다고 표현하지 말 것.
3. **Major guided curriculum 부분**: 고정 모듈 Continue 우선순위(단어→문법→입력→듣기→레슨→복습), 여러 활성 세션의 최근 사용 포인터/선택목록 없음. 각각 catalog에서는 원래 session을 재개할 수 있다. 혼합 Unit와 심화진단 없음.
4. **Major 삭제된 콘텐츠**: active session ID가 비활성/누락되면 안전한 오류+닫기이며, 자동 skip/대체로 session을 끝내는 기능은 없음. 기존 progress는 삭제되지 않음. DATA는 이미 배포한 ID를 제거하지 말 것.
5. **Major 범위 제한**: Conjugation/문장 생산은 지원형태와 authored accepted-answer 문제에 한정. 자유작문/모든 활용·예외는 미지원. 유지학습은 기존 모드 진입이며 자동 혼합문제 추천 엔진은 아님.
6. **Minor UX**: 짧은량 preference는 새 단어 SRS session에만 적용; 진행중20개는 5개로 자르지 않음. 문법/듣기는 즉시중단 가능한 기존 세션 크기. 단어/문법을 단일 session에 섞지 않음.
7. **Minor 데이터 정의**: 전체 문제 정답률은 재시도 포함, listening 하위지표는 최초시도만. production spacing은 기존 모델에서 incorrect로 집계. SRS ‘長い間隔’은stage>=4, 실제 기억의 보증이 아님.
8. **Minor 알림**: daily generic invitation, due 자동취소/요일/deep-link 없음. 시스템 Focus/요약/DST/시간대별 전달은 OS와 기기 검증 필요. BackgroundDB작업 없음.

## Mac/iPhone 검증 절차 (미실행)

`Tools/verify.sh`를 Mac에서 실행하고 `TEST_DESTINATION`에 설치된 simulator를 지정하여104 XCTest 실행. Debug/Release build, v9 DB→v10 migration backup, 새 설치/기존 업데이트 둘 다 검사한다.

1. 신규 설치→開始位置→한글→2개학습→종료→Continue. content13→같은steps의 다음 release로 업데이트 후 기존 answers/count 유지.
2. due20개 준비→短く復習5→4판정→강제종료→재실행→1개남음; due전체16 유지. preference10/20 바꾸어도 시작된5개 membership 유지.
3. grammar/production/listening 각각2개 진행→background/전화/닫기→catalog재개; 빠른 submit/next 연타로2중점수/자동skip 없는지 확인.
4. 기내모드→단어/문법/search/favorite/통계/설정. Listening은 Korean voice 준비/없음 두 경우 확인. 화면이탈과 이어폰해제 시 음성중단.
5. 알림 첫설치에서 prompt없음→설정toggle→거절→다시toggle해도 popup반복없음; 시스템에서 허용→enable/time변경→off; 재실행/Focus/DST/시간대변경 확인.
6. 기록: 빈상태/1정답1오답/자기평가/재시도/자정·timezone변경. 오늘7일30일의 정의와 실제event 비교.
7. Home→Vocabulary→완료→Home→Review→Grammar→Listening→back→Search→Favorite→Practice→Records→Settings. Dynamic Type최대/VoiceOver hidden답안/LightDark/한손 버튼 확인.
