# DEV-10 Integration Audit — 2026-10-04

실행 환경: Linux/Python/SQLite. Swift compiler/Xcode/iOS Simulator 없음. 아래 ‘SQL’은 Swift repository의 실제 SQL을 추출하여 테스트 DB에서 실행한 것이다. ‘소스 검토’는 기기 동작 확인을 의미하지 않는다.

| 연결 | 실제 확인 | 남은 네이티브 검증 |
| --- | --- | --- |
| Curriculum → Content | 실제 active level별 ID query; 200개 page; vocabulary926/grammar42/listening111, 비문법 lesson26 | 화면 표시/큰 글자/scroll 성능 |
| Curriculum → Vocabulary/Grammar | 기존 level별 set/lesson 화면으로 연결하는 소스 검토; 기존 set/grammar SQL regression 통과 | 실제 회독·완료·화면 복귀 |
| Curriculum → Conjugation/Input | 실제 active production question_target을 가진23 lemma의 bounded level query 통과 | 키보드·focus·submit UI |
| Curriculum → Listening | 기존 level/batch 및 exact scope 재개 연결; source/normalization/retry SQL regression 통과 | 음성 normal/slow/stop·빠른 조작 |
| Profile/Skip → Progress | 실제 user_metadata upsert/reopen; 기존 session/favorite/3종 SRS 불변 확인 | 앱 force quit 이후 시작 위치 표시 |
| Diagnostic → Resume | production ID와 snapshot contract; Swift XCTest 작성, 미실행 | 실제8문항 로드·재시작·중도 종료·오디오 unavailable |
| Home → Continue | 실제6종 session UNION 및 완료 session 제외 SQL 통과 | 각 fullScreen/NavigationStack dismiss/back |
| Completion → Level | DISTINCT 완료 ID, listening 최초 attempt+완료session, retry중복제외 SQL 통과 | 학습 후 홈/코스 summary 갱신 |
| Review → Course 독립 | profile/re-diagnostic가 기존 SRS를 수정하지 않는 SQL 검증; 기존 due/backlog/날짜 SQL regression | 자정·timezone·foreground에 숫자 갱신 |
| Content Update | production source/DB가 DATA06과 byte-identical; 기존 content update tests 통과 | 실제 iOS 앱 업데이트 설치 |
| 접근성/디자인 | listening 진단 원문 Text 비생성, native labels/44pt controls/시스템 색 소스 검토 | VoiceOver 정답 비노출, 최대 Dynamic Type, Light/Dark |

## 실행 결과

- `python3 -m unittest discover -s Tools/ContentBuilder -v`: 180 PASS. 전체 로그 `TEST_RESULTS_DEV10.txt`.
- Tree-sitter Swift 68파일 구문 오류0. `STATIC_CHECKS_DEV10.txt`.
- Xcodeproject generator: app59/test9파일. XCTest88개 작성, 미실행.
- source/DB 무변경이므로 Content Version13 유지. Validator 우회 및 데이터 fixture 대체 없음.

## 발견 및 수정한 위험

- legacy `practice:intro` scope 손실: 원문 resumeScope 전달.
- 빈/잘못된 LessonFlow index: 배열 범위 guard.
- 진단 재시작 stale input/audio completion: 초기화와 stop.
- profile 저장 중 경험 선택 변경: 버튼 및 Picker 비활성화.

실기기에서 재현했다는 뜻은 아니다. 수정된 Swift path는 네이티브 실행이 필요하다.

## Mac/iPhone 필수 검증 시나리오

1. Xcode 프로젝트를 열어 signing team 선택 후 simulator build/test. 모든88 XCTest를 실행하고 경고/에러 수정.
2. 신규 사용자: 경험 선택 → 한글 lesson → 퀴즈 → 완료 → 홈. 시작 위치를 初級으로 바꿔도 기존 완료 수 유지.
3. 실제 DATA06 데이터로 단어20개 회독 → 일부 모르기 → 다음 회독 → 완료 → SRS; 앱 종료 후 동일 stable IDs 재개.
4. 문법 lesson, 입력, 듣기 각 미완료 session을 만든 뒤 홈 Continue가 문서의 모듈 우선순위로 여는지 확인. legacy scope도 재개.
5. 진단 답변·중간 종료·재개·다시 진단·음성 skip. 정답 연타로 점수가 중복 증가하지 않고 저장 위치와 UI가 일치하는지 확인.
6. 듣기 화면을 VoiceOver로 탐색하여 정답 원문이 공개 전 노출되지 않는지 확인. speaker 연타, normal/slow, back/background 시 stop 확인.
7. 듣기 오답 → retry → 완료 → review → 앱 종료/재실행. score/SRS 중복 저장 없음 확인.
8. due0 / due다수 / empty상위level / 빈course / 잘못된contentID / 한국어voice없음 상황에서 설명과 복귀 경로 확인.
9. 자정/기기timezone/foreground 변화 후 오늘의 복습 숫자, 저장된 nextReviewDate 보존 확인.
10. 홈 → 코스 → 각 모듈 → 결과 → 홈 → review → 뒤로가기. 중복 push/dead-end 검사. 최대 글자 크기/Light/Dark 검사.

## 현재 범위의 한계

- authored mixed Unit 자동진행과 일일 학습량 추천 scheduler는 없음. 기존 small set/lesson/batch를 level에서 선택한다.
- 상급 진단/공인 placement는 없음. 간이8문항은 하위3단계만 추천한다.
- 모든 module의 전역 last-interaction순서는 없음. 고정 priority와 가능한 timestamp를 사용한다.
- SQLite/소스 검사만으로 Navigation·Audio·VoiceOver·Swift type correctness를 보증할 수 없다.
