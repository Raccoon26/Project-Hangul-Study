# DEV-11 Integration Audit

실행: Linux/Python/SQLite. Swift/iOS runtime 없음. SQL 테스트는 실제 repository 문자열을 추출하여 production/temporary user DB에 실행한다. 소스 검토와 네이티브 실행을 구분한다.

| 경로 | 확인한 근거 | 남은 검증 |
| --- | --- | --- |
| Content → Search | 한국어 exact/partial, 일본어 전체 의미, grammar pattern/meaning/explanation, rank, 페이지 중복 없음, literal SQL 문자 테스트 | iOS keyboard/debounce/취소 화면 |
| Search → Typed Detail | 실제 content kind+ID 조회, 잘못된 kind/없는 ID는 nil, 본문 DB 불변 | 실제 NavigationLink/back/빠른 tap |
| Detail → Related | 전체 production 단어/문법의 실제 related SQL, active target·유효 kind·자기참조 제외·20개 제한·cross-module link 확인 | 화면 비교 내용·연속 push/back |
| Detail → Conjugation | 기존 generator 직접 호출, production rubric override 일관성 SQL 검사, Native 비교 XCTest 작성 | Swift 엔진 테스트 실제 실행 |
| Favorites → UserProgress | v8→v9 이관, type별 저장/삭제, 중복 없음, cold reopen, 기존 curriculum profile 유지 | 실제 앱 업데이트 설치 |
| Recent → Progress | 최대30개·중복 갱신·타 학습/SRS table0변경 SQL 확인 | 화면 전환 중 cancellation |
| Difficult → SRS | 최근 반복실패만 포함; 오래된/단일실패/회복/높은stage/미래기록 제외 | 실제 복습 후 목록 UI 갱신 |
| Favorites → Practice | 기존 review tables, 예정 review와 독립된 unique scope; grammar quiz table 재사용 | 실제 card/question transition·완료 |
| Practice → SRS/Curriculum | Swift 분기에서 SRS update/insert 금지; native 보존/완료 비오염 tests 작성 | Native tests 실행 필수 |
| Practice → Resume | 실제 curriculum UNION이 scope가 아닌 session UUID로 practice를 반환, 기존6종 resume SQL regression | 앱 force quit/재개 UI |
| Audio → Detail | 공통 AudioService, 화면 이탈/background stop, normal/slow 명시적 전달 소스 확인 | 음성 청취/겹침/VoiceOver |
| Content Update | source/DB DEV10 ZIP과 동일, 기존 Content update/learning SQL tests PASS | 기기 앱 업데이트 후 session 재개 |
| Home/Curriculum/Listening | 기존 engine/query regression 실행, 새 진입만 연결 | 전체 iOS navigation walk-through |

## 실행 결과

전체 Python/SQLite191 PASS (`TEST_RESULTS_DEV11.txt`). Swift75파일 syntax error0 (`STATIC_CHECKS_DEV11.txt`). XCTest94개 작성, 실행0. Xcode build 실행0. Native integration이 모두 통과했다고 표현하지 않는다.

검색 성능은 `PERFORMANCE_DEV11.json`: production 및 synthetic15,000어휘/30,000예문/500문법, 각 검색10회. 큰 substring 결과의 중앙값57.905ms. 이것은 Linux SQL이며 iPhone 화면 성능이 아니다.

## 상태 / 버그 감사

- favorite 연타: UI saving guard + content_id unique upsert, type-aware remove.
- 검색/상세 응답 역전: generation + cancellation 확인 후 publish.
- 저장된 목록 필터 변경: generation/selection 검증, page30, typed result.
- review 지연된 답변: rendering 당시 content/question ID와 현재 ID 비교. DB는 committed item 재제출을 반환하여 중복 누적하지 않는다.
- 문법 포함 favorite count의 ‘단어’ label 수정.
- practice에서 기존 SRS 일정 변경을 암시하는 hint/완료 문구 수정.
- migration9 Xcode resource 누락 위험 수정.
- missing content/favorite는 오류/해제/복귀 경로이며 progress를 삭제하지 않는다. 미완료 practice의 누락 항목은 복구 전 학습이 막힐 수 있음을 PROJECT_STATUS에 명시.

## Mac/iPhone 출하 전 체크

1. Xcode build 및94 XCTest 실행. v8 사용자 DB 사본으로 v9 migration과 backup 확인.
2. 검색창에서 학교/学校/먹다/食べる/고 싶다/したい/없는검색어, 입력 연속 변경→취소→다시 입력. 정확한 항목/종류/뒤로가기 확인.
3. 단어 상세→예문 normal/slow/stop→관련 문법→비교 문법→back. 음성 중복/화면 종료 후 재생 없음 확인.
4. 단어와 문법 각각 저장/해제 연타→앱 종료→재실행. 목록 type 필터와 기록 숫자 확인.
5. 저장된 어휘/문법 수동 연습→의미 또는 문제→결과→중간 종료→홈 Continue→완료. 기존 회독 snapshot/SRS stage/due 불변 확인.
6. 예정된 review와 practice를 동시에 미완료로 만들고 각각 올바른 session으로 복원되는지 확인.
7. recent30개/빈목록/누락즐겨찾기/없는예문/미지원활용/한국어voice없음에서 crash·dead-end 검사.
8. 어려운 항목 생성 후 remembered 및 충분한 SRS 상승으로 제외되는지 확인. profile/Content update는 기존 기록을 유지해야 함.
9. 최대 Dynamic Type, Light/Dark, VoiceOver, Reduce Motion, keyboard focus와 빠른 연속 navigation 검사.
