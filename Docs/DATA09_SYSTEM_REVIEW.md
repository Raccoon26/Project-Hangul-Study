# DATA-09-7 시스템·요구사항 회귀 감사

2026-10-20 UTC. 시작 main `fcb7897b8bf78ce138e1941d9e678d9c22128aed` / `data09-7/system-audit`, 기존 미커밋 변경0. 현재 **Content24 / Schema4 / reader7 / UserProgress10**을 유지한다. 이번 작업은 감사·테스트 보강이며 runtime 코드·Production Source/DB·콘텐츠 revision 변경0이다. 실행된 SQL/portable 범위에서 새 P0/P1은 재현하지 않았다. 기존 native P1 확인 gate와 **B—Conditional**은 남는다.

[사용자 요청](DATA09_SYSTEM_REQUEST.md), [실행 감사](DATA09_SYSTEM_AUDIT.json), [최종 실행 결과](DATA09_SYSTEM_RESULTS.json)가 이번 근거다. AI 자체 검수와 사람 승인, SQL 실행과 Swift/iOS 실행을 구분한다.

## 실제 Production 수량

[DB 집계·무결성](DATA09_SYSTEM_COUNTS.json): Vocabulary2,287 / Meaning2,420 / Example4,813 / Grammar96 / Question3,553 / Listening1,936 / Course8 / Lesson103, 비활성 content_items0. 버전·ID·payload·배치 변경0이다.

| Level | Vocabulary | Example | Grammar | Question | Listening |
| --- | ---: | ---: | ---: | ---: | ---: |
| 한글 |0|0|0|59|0|
| 入門 |306|659|22|156|34|
| 初級 |800|1,577|20|134|79|
| 初中級 |1,181|2,577|54|3,204|1,823|
| 그 이상/유지 |0|0|0|0|0|

## 명세의 확인 가능 범위

`PROJECT_STATUS.md`, `CONTENT_GUIDE.md`, `DATA_PROGRESS.md`, `RELEASE_CHECKLIST.md`, `AGENTS.md`, DATA08/09 누적 기록, DATA08 closeout/system 및 DEV12~14 사후 감사와 실제 구현을 대조했다. DEV01~14/DATA01~07은 보존된 단계별 STATUS/REVIEW를 요구 계약의 근거로 사용했다. 21개 보고서 경로·해시·한계는 실행 감사의 specification_inventory에 있다.

현재 tracked 경로와 접근 가능한 Git history의 SPEC/REQUIREMENT 이름 조사에서도 **완전한 원래 작업 명세는 찾지 못했다**([경로 기록](DATA09_SYSTEM_SPEC_INVENTORY.txt)). 이름 검색만으로 다른 문서의 원문 존재 가능성까지 부정하지 않는다. 외부 공유 링크/ZIP 원문을 새로 확보하지 않았으므로 원래 모든 세부 요구의 완전 충족은 **UNVERIFIABLE**이다. 현재 대화와 저장된 DATA08/09 요청·계약은 확인 가능한 범위에서 감사했다.

## DEV-01~14 실제 대조

아래 PASS는 명시한 Python/SQLite/소스 계약 범위다. 모든 행의 Swift 실행·UI E2E·기기는 BLOCKED다.

| 단계 | 현재 구현·실행 근거 | 누락·부분·테스트 부족 |
| --- | --- | --- |
| DEV01 기반/저장 | ContentPackageValidator, SQLiteConnection/ProgressRepository, repository/learning SQL 회귀 | 번들 read-only·UserProgress 별도·transaction·event UUID 멱등성. 실제 앱 launch 미검증 |
| DEV02 DB/Importer/Stable ID | Source25테이블66,094행, builder/validator, 이전19/23 strict 및 byte 재현 | 원격 서명 update/download/recovery UI 미구현. 일반 Validator의 전체 prerequisite cycle gate는 없음; 이번 현재96문법 DAG 별도 전수 검사 |
| DEV03 한글 | HangulLearning/LessonSession/SQLiteContentRepository, hangul55·12레슨 | 조립/문제/즉시 저장 SQL 계약 유지. native 조립/발음/조작 미실행 |
| DEV04 발음/오디오 | pronunciation36·14레슨, AudioPolicy/KoreanAudioService, pronunciation tests | 실제 검증 녹음0. 설치 TTS/통화/route interruption/VoiceOver BLOCKED |
| DEV05 어휘/회독 | VocabularyPassEngine/SQLiteVocabularyProgress,2,287카드·2,420뜻, 고정 membership/revision | snapshot 보존. curated 혼합 scheduler 없음. 고정 회독의 retire 자동 대체/alias 병합 없음 |
| DEV06 SRS | StepReviewScheduler/SQLiteReviewProgress, unique(content_id,skill), due/deferral tests | 일정 재등록으로 기존 due 초기화 안 함. calendar native 실행/장기 효과 미검증 |
| DEV07 Grammar | GrammarLearning/SQLiteGrammarContent/Progress/VM,96카드·30레슨·300문항 | 신규54 실제3코스/6Unit tag/18레슨. 퀴즈/회독 Swift state machine 미실행. 선택적 선행 프리뷰는 숙달 강제 조건이 아님 |
| DEV08 활용/입력 | ConjugationEngine/ProductionAnswer/SQLiteProduction,612어휘·1,227문항 | 지원9형·authored override 범위. 새54문법 전체 자동 생성/자유작문 채점/전용 입력 due queue 없음. ㅎ사전 활용 override 부족(P2) 유지 |
| DEV09 듣기/받아쓰기 | SQLiteListening/ListeningSession/View,1,936항목·104batch, P1-02/03 현행 회귀 |4유형·TTS/저장/유한 retry. 실제 음성·채점 Swift/IME BLOCKED |
| DEV10 Curriculum/Resume | SQLiteCurriculum/CurriculumResumeView,9level·현재8course/103lesson | bounded 실제 membership·최신 committed activity. 간이 진단8문항, 상위 과정/혼합 Unit 자동 순서/개인화 추천 부분 |
| DEV11 검색/사전/저장 | SQLiteLookup/SavedContent, typed2,383상세·한일 검색 | literal substring. 오타/형태소/초성 검색 없음. 실제 IME/빠른 navigation/Dead Button 미검증 |
| DEV12 통계/유지/설정 | SQLiteStatistics·Maintenance·LearningPreferences, event/due/5·10·20/수동 practice SQL | 자동혼합 유지학습 없음. 설정·알림은 UserDefaults/native; SQL metadata fixture는 그 실행 증거 아님 |
| DEV13 광고/구매 | PurchaseService/AdService/MonetizationPolicy, policy·독립 저장키 회귀 | content/schema version 의존 없음. 실제 SDK resolve/Keychain/거래/환불/광고·동의 BLOCKED |
| DEV14 출시/빌드 | verify.sh/check_monetization, packaging/privacy/config 회귀 | Xcode/Swift 없음. Debug/Release/device build·SDK·서명/ASC·실기기 미완료. Release 광고 ID 미제공에 따른 비활성 유지 |

## DATA-01~09 보존·요구 대조

| 단계 | 확인한 실제 계약 | 남은 범위 |
| --- | --- | --- |
| DATA01~03 | ID registry·불변 fixture·뜻별 예문·다의어/동형어·Note·POS/불규칙, 해당 content tests | 원래 명세 전체·독립 사람 한일 검수 확인 불가 |
| DATA04 | 기존42문법/문제/비교/관계, v10→11 보존 회귀 | 과거 검수를 사람 승인으로 간주하지 않음 |
| DATA05 |200어휘/339예문 cohort·입력/듣기 참조 | 독립 언어/기기 평가 미확인 |
| DATA06 |80듣기·4유형·원Example ID·SRS 연결 | 실제 청취/중단·받아쓰기 미실행 |
| DATA07 |450어휘/900예문·初中級·기존 배포/입력 보존 | 후속 고급 문법/장문·녹음 부족 |
| DATA08 | A301/602+B300/600+C310/619=911V/1,821고유문장, 기존 payload SHA911개 일치·문장입력581개 첫Meaning/Example 일치 | native P1 확인·독립 사람 품질/난도 미검증.163후보 후속 미해결36 유지 |
| DATA09-1 | 기존42 및163후보 분석/54확장 설계·장기350~500 | 현재 전체96, 장기 부족254~404. 설명 coverage 판단을 모든 선행 숙달로 해석 안 함 |
| DATA09-2~4 | 신규54G/216고유E/216Q, 각18/72/72. 옛E4재사용 제외 | 목표45~60/180~300/180~300 충족. 새 문법 직접입력/Listening 신규 생성0 |
| DATA09-5 |25ID/31필드 교정·54/216/216 AI 전수/고위험/무작위 검수 이력·known editorial regression | 이번 구조/참조 감사로 새 사람/외부사전 승인 주장 안 함. 독립 원어민·교사 NOT TESTED |
| DATA09-6 | 실제6Unit·18레슨·선행20·관련V54관계, Note reader→view 전달·authored 입력만 진입 | forward prerequisite를 선택적 프리뷰로 지원. 실제 native Resume/입력/접근성은 BLOCKED |

## 전수 연결·선행·채점·Migration

실제 Swift repository에서 추출한 SQL을 현재 번들에 실행했다. Vocabulary2,287/Meaning2,420, Grammar96/30레슨/300문제, generic3코스/73레슨/90문제, Production612어휘/1,227문제, Listening1,936문제/104batch를 bounded pagination으로 조회했다. 합집합 **3,553문제·4,813예문 도달, 누락0**이다. 각 Grammar 문항의 단일 target·정답 choice·중복 없는 선택지·실제 grammar_examples 연결300개를 재확인했다. 이는 의미적으로 정답이 유일하다는 사람 판단이나 UI E2E가 아니다.

한국어 어휘2,287개, 일본어 뜻72개 간격 표본, 전체96문법의 한국어 pattern/일본어 meaning192개 검색을 실행했다. literal `%`/`_`/quote/injection·없는 ID·typed detail·Favorite/Difficult/Recent·Statistics·Resume 회귀도 전체 suite 대상이다. source/DB 무결성은 잘못된 번역/뉘앙스를 모두 검출하지 않는다.

전체96문법/93선행 edge의 active target·자기참조/순환 없음과 신규54 프리뷰≤8을 확인한다. 실제 레슨/항목 ordinal 기준 후행 또는 동일 순서 참조12개는 실행 감사에 ID로 남겼다. 기존 lesson/order/snapshot을 바꾸지 않고 page0에서 선행 설명을 미리 읽는 정책이다. 이것으로 교육적으로 최적인 순서/부수 문법 전부 해결을 주장하지 않는다. 기존163건의 **해결120/조건부7/미해결36, Level 검토8미해결**은 그대로다. 추가 언어 재분류는 하지 않았다.

새 portable6개는 전300문항/30레슨 전수, 잘못 선택한 문항 snapshot의 새 콘텐츠/재실행 보존, 늦은 저장 실패 시 answer/event/item_progress/daily_statistics/reveal/Resume timestamp 동시 rollback, UUID 중복 거부/실제 통계 불변, native guard 소스 계약을 확인한다. rollback/snapshot JSON은 SQL fixture이며 Swift Codable 검증이 아니다. 기존19/23→24 strict rebuild·모든 사용자 테이블/선택·SRS·Favorites·Difficult·진행 snapshot·통계 보존, user1~10 additive migration, dataset gate, process 강제 종료 회귀는 전체 suite에서 재실행한다.

새 native2개는 **18신규 레슨 전체** 실제 문제→회독→SRS→cold resume, 오답 선택 변경/잘못된 기억함 차단, active snapshot 우선, stale/완료 중복·review 재제출과 completed_passes/이벤트 중복 방지를 대상으로 작성했다. 총141정의/실행0: **BLOCKED**다. 작성된 테스트를 통과로 표시하지 않는다.

## DATA08 P1 세 건의 현재 회귀 상태

| 버그 | 이번 실제 확인 | 남은 gate |
| --- | --- | --- |
| P1-01 unavailable vocabulary/grammar/practice 때문에 복습 정지 | 현재 SQL로 deferral metadata·원SRS/due/이벤트/membership 보존, cold reopen·늦은 저장 실패 rollback·전20보류를 학습완료0으로 계산·중복보류/새버전 재확인 PASS | 실제 native API/UI unavailable 카드→보류·다음 카드 BLOCKED. 고정 회독/레슨 retire 자동대체로 확대하지 않음 |
| P1-02 받아쓰기 끝 문장부호 생략 오답 | 전1,850dictation의 accepted/끝 .!? 정책 corpus 검사 PASS, DATA08 영향1,821건 보존. ListeningQuestion→judgeDictation 소스 연결 유지 | Python 정책 검사이며 Swift judge1,850/IME/기기 BLOCKED. 일반 ProductionAnswer 정규화 불변 |
| P1-03 listening due 퇴역prefix가 뒤 active 은폐 | synthetic45due/첫25retire→2번째 page15active 도달·SRS45due 보존·나머지5pending, 실제 SQL PASS. 버전 변경 시 재확인하는 metadata 조건 소스 유지 | 실제 native pagination/audio/저장 snapshot UI BLOCKED |

기존 전용10/10을 현재 DB로 실행했다. 세 건의 runtime 수정 코드는 변경하지 않았다. 이번 실행 범위에서 새 P0/P1 재현0/수정0이며, native 미실행으로 crash/audio/실제 Progress 손실이 없다고 보장하지 않는다.

## 광고·구매·Offline·짧은 학습·성능

PurchaseService/AdService/MonetizationPolicy/LearningPreferences는 시작 commit과 byte 동일하다. `remove_ads`, Keychain debug/release v1, `monetization.frequency.v1`, `learning.preferences.v1`은 콘텐츠 버전과 독립이다. opaque cache 보존/소스 검사·기존 policy/monetization checks PASS는 실제 권한/Keychain/SDK 거래 실행이 아니다. 광고는 저장 성공한 Vocabulary 완료 경계만 사용하며 기존12분/60항목/30분 cap·Resume/짧은 학습 제외·구매 후 늦은 load 무효화 정책을 유지한다.

SQL benchmark와 기존 integration은 Python socket을 금지한 상태에서 로컬 DB를 읽고 썼다. actual core 경로에 네트워크 선행조건을 추가하지 않았다. 설치 voice/실제 비행기 모드/기기 UserDefaults/Keychain·3~10분 학습·한 손·VoiceOver·배경/강제 종료·TTS/메모리 누수는 **BLOCKED**다.

Linux warm SQLite30회 p95: Home summary/Resume7.7807ms, broad search6.1627ms, Grammar catalog0.9404ms, full card2.1516ms, Grammar SRS20 headers2.2862ms, 3항목 grammar session commit0.1770ms. [실측](DATA09_SYSTEM_PERFORMANCE.json). 동일 현재 SQL을19/23/24에 적용한 비교이며 코드 전후/iPhone 성능·RAM 실측은 아니다. shared cloud 편차가 있고 성능 보장값으로 쓰지 않는다.

## 검사·초기 실패·남은 상태

전체 `sh Tools/verify.sh --portable`는 **365/365 PASS,415.721초,실패/오류/skip0,exit0**다.19/23→24 strict0errors/기존10warnings·bundle byte 동일, DATA08 구조0errors/5warnings·DATA09 계약0/0이다. 최종 실행 수와 시간은 [RESULTS](DATA09_SYSTEM_RESULTS.json) 및 원시 `DATA09_SYSTEM_TEST_LOG.txt`가 기준이다. 새6개·기존P1 10개 전용 실행은 전체 suite와 중복이며 더해 고유 테스트 수를 부풀리지 않는다.

- **FAIL → 수정(Python harness)**: 초기 새6개 중1ERROR. exposed_at 없이 revealed_at을 넣어 UserProgress CHECK가 차단했다. 실제 노출 상태 fixture로 수정, repository/constraint 완화0. `DATA09_SYSTEM_INITIAL_TEST_LOG.txt` 보존.
- **FAIL → 수정(audit script)**: 최초 추가 감사가 grammar에 존재하지 않는 learning_order를 조회했다. 실제 curriculum lessons.ordinal/lesson_items.ordinal로 변경. `DATA09_SYSTEM_INITIAL_AUDIT_LOG.txt` 보존. Production 오류/버그 수정 수로 세지 않는다.
- **BLOCKED**: xcodebuild/swift 실행파일 없음, build/SDK resolve·141 XCTest 실행0, UI/기기·Audio·접근성·메모리·StoreKit/AdMob.
- **NOT TESTED**: 독립 사람 언어/교육·외부 사전 검수.
- **UNVERIFIABLE**: 확보되지 않은 원래 DEV01~14/DATA01~07 전체 명세.
- 현재 실행 범위에서 미수정 재현 P0/P1 0. native 확인 gate·선행36건·상위콘텐츠·검증 녹음/ㅎ사전 활용·혼합학습/원격 update 부분은 유지한다.

## 재현·Git·종료

```sh
python3 Tools/ContentBuilder/audit_data09_system.py --report Docs/DATA09_SYSTEM_AUDIT.json
python3 -m unittest discover -s Tools/ContentBuilder -p test_data09_system_audit.py -v
python3 -m unittest discover -s Tools/ContentBuilder -p test_data08_system_audit.py -v
python3 Tools/ContentBuilder/benchmark_data09_integration.py --bundle Resources/content.sqlite --report Docs/DATA09_SYSTEM_PERFORMANCE.json
sh Tools/verify.sh --portable
```

Production Source SHA `081ed35c7cd78345af1c1793fc450acaa2931f173cef00aaa960c8ef42318540`, bundle SHA `56a7fa8b5358e254eeb324e706860d150d20c8ec013ba0b6f602cf14d93cceff` 보존. 기존 원본/fixture/ID·광고·구매 코드 삭제/수정0, schema/content version 증가0, force push0. 기존 Git 위임에 따라 정상 commit/push/PR/merge로 전달하며 최종 SHA/PR은 Git 및 최종 응답에서 확인한다. DATA-09-7에서 종료하고 다음 단계/DATA10을 시작하지 않는다.
