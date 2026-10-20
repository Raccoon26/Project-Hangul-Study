# DATA-09-6 Production·Curriculum 통합

현재19를 보존하라는 요청에 대해, DATA09 시작 전19 원본/DB fixture를 그대로 유지하고 실제 직전23도 추가 보존했다. 현재24의 검증은 **19→24와23→24를 별도로** 수행한다.19를 현재 버전으로 오인하거나23을19 fixture에 덮어쓰지 않는다. Source는 production.json 하나이며 `prepare_data09_integration.py`는 동결23과 고정 manifest로 동일24를 재현한다.

## 실제 콘텐츠 배치

기존 Course3/Lesson18/Grammar54의 UUID·membership·ordinal은 보존했다. Schema4의 tag/item_tags를 이용해6개 Unit(각3레슨)을 식별하고, 문법 목록에 실제 코스명/단원명을 표시한다. 기존 generic lesson 엔진의 문법 코스 제외 정책은 유지하고 Curriculum의 typed Grammar 경로를 사용한다. 단원 전체를 하나의 큰 session으로 합치지 않았으며 레슨은3문법/문법당4객관식이다.

선행 참조20개를 추가해 실제 카드의 뜻·형태·설명을 첫 페이지에서 선택적으로 복습한다. A10의 일반 관형, A18의 때절, B16의 명사화, C14의 동안/배경, C17의 게 되다 등이 포함된다. 뒤에 있는 기초 단원을 보기 위해 기존18레슨 순서나 진행 중 session을 바꾸지 않는다. 이 프리뷰는 학습 잠금이나 완료/SRS 등록이 아니다. 물리적 ordinal이 모든 부수 문형의 위상 순서라는 뜻도 아니다.

54개 Grammar에서35개 기존 어휘로 향하는 related 관계54개를 검토해 연결했다. 예문과 Dictionary 의미를 실제 대조했으며 단순 같은 번역·동의어로 추론하지 않았다. 문법 학습→사전 sheet→기존 Vocabulary/활용표/저장/연습과 사전의 양방향 관련 경로를 사용한다. 기존 공유 예문4개를 통한 관련어 연결도 보존했다.

기존 검수 입력 문제가 있는6개 관련어는26개 고유 기존 문제(형태19/문장4/빈칸3)를12개 Grammar에서 접근할 수 있다. 실제 문제가 있을 때만 입력 연습 버튼을 표시한다.54개 문형 전체의 자동 생성·직접입력 구현은 아니다. 신규 Grammar/Example/Question0, 누적54/216/216을 유지한다. 기존 ConjugationEngine의9형 지원과 새 문형의 범위를 분리한다.

## 수정·보완 사항

| 항목 | 이전 | 수정 |
| --- | --- | --- |
| 검수 Note | DB learning_point_ja가 grammarExamples/Example에서 빠져 화면에 전달되지 않음 | 기존 필드를 비영속 모델과 GrammarExampleView로 전달. B03/B11/B16/C11 성별 장면 Note 포함 |
| 코스/단원 | 문법18레슨이 평면 목록에 보임 | 기존 구조에6Unit tag를 더해 코스/단원명 표시 |
| 선행 형태 | prerequisite가 학습 설명에서 사용되지 않음 | 최대8개 실제 선행 카드의 선택적 사전 복습 |
| 어휘/입력 | 신규 문법은 공유 예문4개 외 관련 어휘 참조가 부족 | 명시 related54개·사전 양방향 연결·검수된 입력 문제만 기존 ProductionStudyView로 연결 |

Grammar/Example/Question/정답·선택지/어휘 본문·기존 순서 변경0. 새 content UUID는 Unit tag6개, 기존107개(Grammar54/어휘35/Lesson18)의 관계 endpoint revision만 각1 증가한다. Source·Schema·Reader·UserProgress를 구분하며 Content24/Schema4/reader7/UserProgress10이다. manifest와 exact23→24 gate가 허용된 변경 전체를 검증한다.

## 검증 범위와 한계

| 경로 | 실행 가능한 검사 | 미실행 범위 |
| --- | --- | --- |
| Importer/Validator |19/23 strict·전체 DB 재구성·ID/revision/관계·FK/integrity·고아 정의 검사 | 없음(언어 품질 인증은 별개) |
| Curriculum/Grammar/Quiz |54카드·18레슨·6단원·216문제·220예문 placement·선행 DAG와 실제 SQL | Swift/UI 실행 BLOCKED |
| Vocabulary/Conjugation/Input |35관련어의 의미·참조, 기존26입력 문제 계약·실제 query·지원 여부 조건 | Swift 생성/입력/IME BLOCKED; 새54문형 입력 지원 아님 |
| 회독/SRS |54개 중복 등록2회·기존due/state 유지·rollback·5/10/20 경계 | 실제 Swift 상태전이/기기 BLOCKED |
| Statistics/Resume/Favorites/Settings |19/23 실제 콘텐츠 ID로 교체·사용자 모든 테이블/파일SHA·통계·어려운 항목·snapshot 보존 | 개인DB/iOS Resume BLOCKED |
| Offline/접근성/짧은 학습 | socket 금지 SQL·즉시 transaction 저장/reopen·44pt/Text/Scroll/Disclosure·기존 page/stop 정책 소스 대조 | 비행기 모드/TTS/VoiceOver/Dynamic Type/실제3~10분·메모리 BLOCKED |

UserProgress10 DDL·migrations와 SRS·회독/Grammar 상태전이 코드는 변경하지 않았다. 진행 중 질문 snapshot과 원래 ContentVersion·선택/페이지/seed/order를 재작성하지 않는다. 읽기/선행 프리뷰는 완료를 만들지 않는다. 기존 deferred review의 새 Content Version 재확인 정책도 보존한다. SQLite의 설정 metadata fixture 보존과 실제 앱 UserDefaults/Keychain 검증은 구분한다. 기존 저장 키·서비스 코드는 유지했지만 실제 기기 설정/권한 확인은 native BLOCKED다.

전용 첫13검사에4 failure(가상 SRS seed2/열 인덱스1/ANALYZE 불변 비교1)를 수정했다. 이후13 PASS, 실제 콘텐츠 ID로 강화 후13 PASS. 첫 전체359검사에 오류4는 기존4열을 가정한 레슨 query fixture였고, 수량/ID assertion을 유지해6열에 맞췄다. 재실행4/4 PASS 후 최종 전체를 다시 검사한다. 초기·중간·최종 로그를 분리하며 초기 결과를 성공으로 바꾸지 않는다. native 회귀2개는 추가했지만139정의/실행0이다.

## 실제 로컬 성능 측정

동일 실행 환경·warm connection·각30회, 실제 repository SQL·별도 user10 SQLite·Python socket 금지다.19에는 DATA09 신규 Grammar가 없어 새 카드 측정은 N/A,23과24를 직접 비교했다. 아래는p95(ms)이며 기기 UI/메모리/시작 시간·3~10분 학습 실측이 아니다.

| 작업 | Content23 | Content24 |
| --- | ---: | ---: |
| Home summary/resume SQL |4.7652|4.6853|
| 넓은 검색 |4.4295|4.1834|
| Grammar catalog |0.7817|1.1135|
| 설명/예문/퀴즈/비교/선행/관련어 card |1.6653|2.2933|
| Grammar SRS due20 headers |1.6627|1.9652|
|3개 항목 session commit SQL |0.1316|0.1683|

추가 조회에 따른 비용은 이 로컬 측정에서 작았지만 iPhone 성능을 보증하지 않는다. [원시 측정](DATA09_INTEGRATION_PERFORMANCE.json)에19 기준 Home/Search/SRS/set/session 결과도 보존했다.

독립 원어민·교사/외부 사전 검수 **NOT TESTED**, Xcode/Swift/iOS build·139 XCTest·UI/VoiceOver·실기기 음성/메모리/중단·StoreKit/AdMob **BLOCKED**. 기존 B—Conditional/native P1 gate와 선행 후보 미해결36건은 유지한다. DATA09-7/DATA10은 시작하지 않는다. 최종 자동 검사·Git 결과는 [DATA09_PROGRESS §12](../DATA09_PROGRESS.md), [수량](DATA09_INTEGRATION_COUNTS.json), 최종 결과 JSON을 기준으로 한다.

## 최종 결과

최종 portable **359/359 PASS**(420.142초, failures/errors/skipped0,exit0), 전용13/13(22.336초)·조회 회귀4/4(0.763초) PASS.251개 최종 입력 파일 SHA를 확인한 후24를 반영하고, 실제 Production Source를19/23 각각 기준으로 재구성해 현재 DB와 byte/SHA까지 같음을 확인했다. Source25테이블66,094행·DB31테이블·integrity ok/FK0. 기존 원본·fixture·검수 근거121개 해시 보존.

현재24/Schema4/reader7/UserProgress10, Grammar96·Example4,813·Question3,553·Vocabulary2,287·Course8/Lesson103, 신규54/216/216 유지. [최종 결과 JSON](DATA09_INTEGRATION_RESULTS.json), [전체 로그](DATA09_INTEGRATION_TEST_LOG.txt), [19→24 실제 재구성](DATA09_INTEGRATION_RECONSTRUCTION19.json), [23→24 실제 재구성](DATA09_INTEGRATION_RECONSTRUCTION23.json). 초기359개 실행의 오류4 및 수정 전 중간 재실행 오류4는 각 실패 로그로 보존하며 최종 PASS와 합산하지 않는다. 독립 사람 검수·native/출시 gate는 위 미검증 상태 그대로다.
