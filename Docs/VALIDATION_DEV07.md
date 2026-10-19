# DEV-07 네이티브 검증 체크리스트

Linux에서 수행한 Python/SQLite/구문 검사는 TEST_RESULTS_DEV07.txt와 STATIC_CHECKS_DEV07.txt를 확인합니다. 아래 항목은 **Mac/iPhone에서 아직 실행하지 않았습니다**.

1. Xcode 프로젝트 HangulStudy scheme으로 Debug/Release 빌드합니다.
2. 실제 설치된 시뮬레이터 ID로 `TEST_DESTINATION='platform=iOS Simulator,id=ID' sh Tools/verify.sh`를 실행합니다. XCTest 총 66개입니다.
3. `学ぶ → 文法 → 入門 → 名詞と助詞①`를 엽니다. 의미→형태/포인트→예문/비교→문제 2개→자기판정까지 확인합니다. 예문 normal/slow/stop과 음성 미설치 안내도 확인합니다.
4. 첫 문법만 覚える, 나머지는 覚えてる로 판정합니다. 次の回読へ에서 첫 문법만 남는지 확인합니다. 모두 통과하면 완료와 SRS 예정 저장을 확인합니다.
5. 설명 단계, 문제 선택 직후, 다음 회독 직전에 각각 앱을 강제 종료하고 재실행합니다. 같은 lesson/current grammar/page/question/선택 결과가 유지되는지 확인합니다. 중복 정답 카운트가 생기지 않아야 합니다.
6. 테스트 기기 날짜를 예정일 뒤로 이동하거나 테스트 전용 UserProgress의 due 값과 state_json을 함께 조정합니다. 배포 source의 날짜나 학습 상태를 변경하지 않습니다.
7. 홈 今日の復習의 文法에서 문제를 풉니다. 정답 전에는 SRS 판정 버튼이 없고, 오답 뒤 覚えた가 비활성인지 확인합니다. 難しい/もう少し/覚えた에 따라 기존 단계형 스케줄러가 예정일을 바꾸는지 확인합니다.
8. 문제 선택 직후 종료·재실행으로 같은 선택/정오답을 재개하고, 완료 후 다음 due 묶음/목록으로 돌아갑니다. 이미 등록한 문법의 회독을 다시 끝내도 SRS가 초기화되지 않아야 합니다.
9. 이전 DATA-03 설치 위에 업데이트하여 단어 세트·SRS·한글/발음 기록이 유지되고 UserProgress v5→v6 백업이 생성되는지 확인합니다.
10. 入門/初級 선택, 콘텐츠가 없는 상위 level 안내, 작은/큰 Dynamic Type, Light/Dark, VoiceOver, 작은 iPhone, iPad, Reduce Motion에서 터치·줄바꿈·스크롤을 확인합니다.
11. 기존 ハングル入門 / 発音・パッチム / 入門単語 / 初級単語 / 単語の復習 경로와 Audio를 확인합니다.

선택한 question은 로컬 snapshot으로 저장합니다. 콘텐츠 업데이트가 진행 중 문제를 교체하지 않습니다. 진행 중인 grammar가 비활성/삭제된 경우 안전하게 오류를 표시하고 기록을 보존합니다. 자동 대체나 기록 삭제는 하지 않습니다.
