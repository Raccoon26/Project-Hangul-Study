# PROJECT_STATUS — DEV-12

2026-10-05. DEV-11 이력은 `Docs/DEV-11_STATUS.md`에 보존했다. 중단 전 작업을 이어서 안정화·감사·문서화했다. 45분 한도는 실제 작업 시간 기준이며 중단 대기시간을 작업으로 산정하지 않았다.

**이 환경은 Linux이며 Swift compiler/Xcode/iOS Simulator가 없다. SQLite/Python 테스트와 Swift 구문 검사는 실행했다. Xcode build/type-check/104 XCTest/기기 UI·음성·알림·VoiceOver는 실행하지 않았다. DEV-12 변경이 들어 있지만 전체 제품 또는 App Store 출시 검증까지 완료했다고 표현하지 않는다.**

## DEV-12 구현 내용

- Home `短く復習`: 기존 Vocabulary SRS/Review UI 그대로 사용하여 새 session5/10/20개. 기본5개. due만 조회하고 backlog는 유지한다. 이미 진행중인 session이 있으면 preference보다 저장된 membership/위치가 우선이다.
- Statistics: 오늘/최근7일/최근30일의 실제 학습 action, 문제 정답률, production 입력, listening 최초답변 정답률, 예정된 복습 완료. 실제 active vocabulary ID 기준 미학습 수, 학습확인/회독통과/SRS학습중/긴간격 단계, grammar 기록을 표시한다.
- Maintenance: 기존 due review, 어려운 어휘·문법, 활용/입력, 듣기/받아쓰기 진입.30일 이상 미확인이고 SRS와 active round에 없는 단어를 최대10개 기존 수동 연습으로 연결한다. 새 독립 progress/learning engine 없음.
- Settings: 짧은 단어복습량, local reminder on/off/시각. Dynamic Type/LightDark는 시스템 설정을 존중한다. 기존 normal/slow UI 재사용, 별도 font slider/음성엔진 없음.
- Notifications: 사용자가 toggle을 켜는 맥락에서만 권한 요청. 거부 후 재요청 popup 없음. UI disabled/busy, 권한회수/스케줄 실패/꺼짐 상태 pending 정리, 앱 재실행 및 설정 복귀 reconciliation.
- 학습 UI 지연 action guard 보완, 한글/발음 content release 재개 오류 수정, production 주요 action 하단 배치, 불필요한 시작 preload 제거.

## Statistics 구조 / 의미

`Models/StatisticsModels.swift`, `Repositories/SQLiteStatistics.swift`, `Views/RecordsView.swift`.

`study_events`를 현재 기기 시간대의 Gregorian 자정부터 now까지 절대 timestamp 범위로 SQL 집계한다.7/30일은 오늘 포함이다. 기존 event의 local_day를 다른 시간대로 잘못 합산하지 않는다. DST는 Calendar 날짜 연산, 미래 timestamp는 제외한다. SQL 결과 몇 행만 읽고 전체 event/Content를 Swift memory로 불러오지 않는다.

학습 action은 설명 확인/단어 노출/문제 답변 등의 기록 수다. 자기평가 `覚える / 覚えてる`나 SRS3평가를 정답/오답으로 바꾸지 않는다. 전체 정답률은 기존 correct/incorrect 이벤트(재시도 포함), Listening 하위 정답률은 `listening_retry` 제외다. Production spacing은 기존 채점정책에 따라 incorrect 집계된다. 통계 화면과 감사문서에 의미를 명시했다.

예정 복습 완료는 vocabulary/grammar의 완료 review_items와 listening review 최초attempt만 합한다. manual practice/retry를 새 예정복습 완료로 중복 집계하지 않는다. 미완료 session 안에서 이미 제출한 문항도 계산한다.

학습확인/회독통과/SRS는 겹칠 수 있는 별도 기록이다. stage>=4(30일 이상)를 `長い間隔で復習`로 표현하며 영구암기 주장은 하지 않는다. 미학습 수는 active Content ID를200개씩 읽고 typed learning event와 대조하므로 retired 항목을 전체수에서 무작정 빼지 않는다. 누적확인 수는 보존된 과거 기록도 포함한다. 정확한 시간 측정이 없어 총학습시간은 표시하지 않는다. XP/streak 압박 UI 없음.

## Maintenance / Short Session 정책

SRS로 이미 관리하는 항목은 due 시스템에 맡긴다. 미래 due를 오래된 항목 목록이 임의로 당기거나 duplicate SRS를 만들지 않는다. 오래된 미예약 단어 연습은 existing `vocabulary_practice` scope와 Review UI를 사용하고 SRS는 변경하지 않는다. 이미 수동 연습 중이면 그 session을 먼저 재개한다. active Content ID를 검증하고 missing ID는 기록을 삭제하지 않고 후보에서 제외한다.

어려운 항목은 기존 최근30일 반복실패/회복 조건을 재사용한다. 문법/production/listening은 기존 문제/예문 엔진과 catalog로 진입한다. 모든 타입을 자동으로 섞는 adaptive maintenance engine은 구현하지 않았다. 짧은 preference는 새 단어복습에만 적용; 문법/듣기 최대20개는 기존처럼 언제든 중단 가능하다.3분/5분/10분의 정확한 소요시간을 보장하지 않는다.

## Settings / Notification / Persistence

`LearningPreferencesStore`는 `UserDefaults`의 `learning.preferences.v1`에 Codable value를 저장한다. Content DB, UserProgress 기록과 역할을 분리했다. 설정 복원 시 enum과 시간 범위를 검사한다. preferred5/10/20량은 사용자 선택권이나 curriculum을 막지 않는다.

`SystemReminderBackend`는 UserNotifications의 단일 ID `learning.daily.reminder`를 매일 calendar hour/minute에 예약/교체한다. 첫 launch/foreground/설정진입은 권한 상태만 확인하며 requestAuthorization은 사용자 on action만 호출한다. 거절/오류는 off로 저장하고 pending/delivered reminder를 정리한다. 시스템에서 권한을 회수한 뒤 돌아오면 UI와 stored preference도 off가 된다.

알림은 “少しだけ、韓国語を復習しませんか…”라는 일반 초대이며 실제 due가 있다는 주장을 하지 않는다. due기반 background DB조회/polling/서버push/요일설정/deep link는 없다. 단말시간에 따르는 repeating trigger이며 DST/시간대/Focus/요약/실제 전달은 기기 QA가 필요하다. mock backend native tests는 작성했지만 미실행이다.

## DB / Version / Content

- Content schema4 / content13 / reader7 유지. Source와 production DB는 DEV11 ZIP 대비 byte-for-byte 동일. 신규 본문/ID/fixture 변경0.
- UserProgress9→10: `study_events(occurred_at,skill,outcome)`, `listening_attempts(occurred_at,is_review,attempt)`, `item_progress(last_seen_at,content_id)` index만 추가. 기존 table row/JSON/SRS/settings identity를 초기화하지 않는다.
- 기존 migration-before-backup, WAL/FULL, unknownfutureversion/dataset mismatch 안전 실패 유지. v10 SQL을 Xcode resource/generator에 포함했고 native migration 기대 버전도 갱신했다.
- 실제 DB: Vocabulary926 / Meanings982 / Examples1876 / Grammar42 / Listening111 / Questions342 / Pronunciation rules36 / hangul55(자모40 포함). `DATA_PROGRESS.md` 및 `PRODUCTION_COUNTS_DEV12.json` 참조.

## 성능 결정

Home 첫 화면 전에 legacy 단어50개/전체favorites/누적통계를 로드하던 것을 제거했다. legacy vocabulary view는 열릴 때 기존 paged 데이터를 요청한다. Home은 due/resume/count 등 기존 경량 요청만 한다. Statistics는 기록 탭 진입 시에만 SQL 집계한다. 신규 timer/위치/지속 background task 없음.

`PERFORMANCE_DEV12.json`: synthetic user events300,000 / vocabularyIDs15,000, 각10회. 오늘 범위 SQL 중앙0.181ms,30일2.837ms, 누적조회174.793ms(최대191.498ms). 날짜범위는 covering index 사용 확인. 누적조회는 SQL index scan이므로 O(1)이라 주장하지 않는다. iPhone launch/렌더/배터리 측정이 아니다. 실제 검색의15k/30k/500규모 측정은 DEV11 보고서를 유지한다.

## Requirements Coverage Audit

상세는 **`Docs/DEV12_REQUIREMENTS_AUDIT.md`**의 기능별 소스·판정·잔여검증 표를 확인한다.

구현을 실제 코드로 확인한 항목: DB/Builder/Validator/Stable ID, Hangul/발음, Vocabulary/회독/SRS, Grammar/quiz/회독/SRS, 제한된 Conjugation/accepted input, Listening4유형/retry/SRS, Curriculum선택/skip/간이진단, Search/Detail/Related/Favorites/Difficult/Recent. 이번 추가는 Statistics/Maintenance/ShortReview/Settings/Reminder다.

**부분/누락**: 수년 전체 production curriculum과 상급 data, 검증된 실제 개별 녹음, 혼합Unit/일일추천, 고급 placement, 자유작문/모든 활용예외, 여러 미완료 session의 ‘가장최근’ Continue 정책. 미검증을 완료로 표시하지 않았다.

## Integration Audit

실제 source → strict Validator → temporary DB build와 bundle 일치 검사, 기존 모듈별 Python/SQLite regression을 실행했다. 신규 SQL에서는 빈통계/범위경계/자기평가 제외/재시도/수동연습 제외/active ID/단계/maintenance중복제외/대량due/부분저장/cold reopen/v10보존/lessonrelease재개를 검사했다.

native integration tests: preference복원/권한거부/오류/회수/off정리, calendarDST, 실제review5개중4개→cold reopen/기존backlog, production content에 대한 grammar/vocabulary/lesson지연 action 보호를 작성했다. Native XCTest104개는 **실행0**. Audio normal/slow/fallback 기존 tests/소스는 유지, 실제 출력을 확인하지 못했다.

## Micro-session / Commute UX Audit

- 학습 진입: 저장된 Continue/단어 短く復習1 tap, 문법/듣기review2 taps. 새 사용자 시작위치 선택은 별도 단계.
- 저장: 의미있는 action별 transaction. 세션을 끝까지 해야 저장되는 구조 아님.20중4 저장/16미완료 SQL cold reopen PASS,5개 native test 작성.
- Resume: vocabulary/grammar/production/listening/lesson/review snapshots 재사용. 미제출 타이핑 한글까지 보존하지 않음.
- 중간 종료/배경: 이미 commit한 결과 유지, audio stop. 실제 force kill/전화/기기 lifecycle은 미검증.
- Offline: bundle content와 local user/settings, network dependency 없음. TTS voice 가용성 별도이며 단어/문법은 음성 없이 가능.
- 한손: 주요 학습 bottom action/large44pt, production도 이번 하단 이동. 실제 화면/최대 Dynamic Type 검증 남음.
- 배터리: 지속 timer/polling/location/background 없음. 진입 전 전체 Content memory load 없음. 배터리 실제 계측 없음.

## Bugs Found

- Major: 한글/발음 레슨의 동일steps가 content version 상승만으로 재개 거부.
- Major 방어 공백: 일부 View의 지연 task가 갱신된 state를 읽어 연타된 next/answer를 새 단계에 적용할 가능성.
- Minor: Settings의 DEV04/SRS미지원 문구, 불필요한 cold-start preload, production primary action 위치.
- 신규 검사: statistics skill 식별/production-only 노출 누락 가능, retired ID로 미학습수 잘못 계산 가능, off preference와 OS pending reminder 불일치 가능.

## Bugs Fixed

- 동일 stable step list + release 비역행이면 동일 session/cursor/results를 유지하고 version만 최신으로 갱신. steps가 바뀌면 기존 안전 차단 유지.
- vocabulary/grammar/production UI는 rendering당시 revision, lesson은 step ID+feedback 상태를 검증. 제출문자열을 Task 시작 전에 capture. 기존 DB revision/idempotency와 함께 동작.
- Settings 문구/일관성, legacy lazy load, production bottom action 수정.
- 실제 skill 기반 통계/active ID 대조, off/revoked/error 알림 cancel 보완.

이상은 소스/SQLite에서 확인한 오류·방어 공백과 수정이다. iOS 연타·Navigation 버그를 실기기에서 재현했다고 주장하지 않는다.

## Known Remaining Issues / DEV-13 전 확인

- **Critical release gate:** Xcode type-check/Debug·Release build/104 XCTest, iPhone lifecycle/audio/notification/VoiceOver 실행 필요. 출시 검증 미완료.
- **Major:** 상급 production curriculum/음원 공백. 현재 분량으로 수년 전체 콘텐츠 완성 주장 금지. 다음 DATA에서 기존ID 유지하며 확대.
- **Major:** Continue는 고정 모듈 순서(단어→문법→입력→듣기→레슨→복습). 여러 미완료 session이 있으면 항상 마지막 학습을 제시하지 않는다. 각 catalog로 재개 가능하지만 최근활동포인터/세션선택 개선 필요.
- **Major:** 삭제/비활성 content가 active session에 있으면 자동skip 없이 복구 전 학습이 막힐 수 있다. 기록은 삭제하지 않으며 닫기/다른학습 가능. DATA에서 배포ID삭제 금지.
- **Major:** 고급 placement, mixed Unit, 모든 활용/자유작문은 미완성. 현재 지원 범위와 시험급/공식빈도 혼동 금지.
- **Minor:** 짧은량 preference는 단어SRS만. Maintenance는 모드별 기존 진입이며 자동혼합은 없음. 알림은 매일 일반초대, due맞춤/요일/deeplink 없음.
- **Minor:** whole-history statistics는 SQL scan, 수백만event의 구형iPhone 계측 필요. 과거 삭제된content의 누적확인 기록은 보존한다.
- 신규 TODO/FIXME/임시콘텐츠/빈동작 버튼을 추가하지 않았다. 미지원·미검증은 위에 명시했다. 광고/IAP/로그인/서버/cloud는 이번 범위 밖이며 추가0.

## 테스트 / Build 결과

- Python/SQLite **203 PASS** (최종 로그 `Docs/TEST_RESULTS_DEV12.txt`). 기존191 + DEV12 12. 테스트 실패나 validation rule을 무시하지 않았다.
- strict production validation **오류0 / 기존검토경고10**, `Docs/VALIDATION_DEV12.json`. source/production DB 불변, integrity ok / FK0.
- Swift **80파일 구문 오류0**, project source/resource 누락0, plist parse 성공. 구문검사는 compiler type-check를 대체하지 않는다.
- Native XCTest **104개 작성 / 실행0**. Xcode build **실행0**, 환경에 실행파일 없음.
- 실행 가능한 core regression은 통과했으나 전체 실제제품 흐름과 OS상호작용이 검증됐다는 뜻은 아니다. 구체적인 Mac/iPhone 체크리스트는 상세 감사문서 끝에 있다.

## 주요 파일

신규: `Models/StatisticsModels.swift`, `Repositories/SQLiteStatistics.swift`, `Services/LearningPreferences.swift`, `Views/MaintenanceView.swift`, `Resources/user-migration-v10.sql`, `Tests/StatisticsAndSettingsTests.swift`, `Tools/ContentBuilder/test_dev12_sql.py`, `benchmark_statistics.py`.

수정: App/root preferences 연결, Records/Settings/Learn/Review/Production/Lesson/Vocabulary/Grammar UI 및 ViewModel action guard, RepositoryProtocols, SQLiteProgressRepository, UserDatabaseMigration, Foundation/Pronunciation tests, generator/Xcode/문서. 정확한 목록은 `Docs/CHANGES_DEV12.txt`.
