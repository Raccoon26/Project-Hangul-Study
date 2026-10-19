# DEV-06 검증과 Mac 실행 인계

## 실행한 것

- Linux Python/SQLite 116개 테스트 통과: 기존 104 + SRS SQL 12.
- 실제 SQLiteReviewProgress.swift의 SQL을 추출하여 due/15000행 backlog/세션/결과/원자성/마이그레이션/조회 인덱스를 확인.
- Production validator 오류 0/기존 경고 8.
- Swift 45개 파일 구문 parser, 프로젝트 참조·리소스, plist/XML, production DB integrity/FK, DEV-05 content 및 기존 한글·발음·음성 보존 검사.

로그는 TEST_RESULTS_DEV06.txt / STATIC_CHECKS_DEV06.txt / DEV06_CONTENT_VALIDATION.json입니다. Python 테스트에서 Swift 달력 알고리즘이나 SwiftUI를 실행한 것은 아닙니다.

## Mac 자동 검증 — 이 환경에서 미수행

```sh
python3 Tools/generate_project.py
xcodebuild -showdestinations -project HangulStudy.xcodeproj -scheme HangulStudy
TEST_DESTINATION='platform=iOS Simulator,id=실제_SIMULATOR_ID' sh Tools/verify.sh
```

Debug/Release와 native XCTest 58개를 실행해야 합니다. SRSTests 16개는 날짜/전이/재개, 기존 42개는 회독·한글·발음·음성·기반 회귀입니다. Swift type-check/네이티브 빌드/테스트 통과는 아직 확인하지 않았습니다.

## 수동 시나리오 — 미수행

1. v4 DEV-05 UserProgress를 가진 앱을 업데이트합니다. migration backup, 기존 즐겨찾기/한글/발음/회독 이력과 완료 set의 SRS 등록을 확인합니다.
2. 첫 회독에서 전부 `覚えてる`로 완료합니다. 모든 stable ID가 stage 0/다음 날 due인지 확인합니다. 여러 회독을 거친 단어에는 neededRepetition=true가 저장되어야 합니다.
3. 예정일이 지난 환경에서 홈의 due 수와 복습을 시작합니다. 실제 production 뜻/예문/note/음성을 확인합니다. 뜻 공개 전 세 판정 버튼이 없어야 합니다.
4. `覚えた`: stage 증가/해당 간격, `もう少し`: stage 유지/최대 3일 간격, `難しい`: stage 0/다음 날을 확인합니다. 최고 stage에서도 120일 복습이 남아야 합니다.
5. 노출 전후/공개 전후/판정 직후 각각 앱 강제 종료 후 복원합니다. 같은 세션/ID/공개 상태로 재개하고 이미 확정한 결과나 노출을 중복 집계하면 안 됩니다.
6. 빠른 연속 탭과 background 이동 시 저장 중 버튼 잠금, 재생 정지, 저장 오류 재조회 흐름을 확인합니다.
7. due 50개 이상을 준비하면 첫 세션 20개만 시작하고 나머지는 due로 남아야 합니다. 완료 후 다음 세션으로 이동하며 새 어휘 학습도 계속 선택 가능해야 합니다.
8. 자정 전후/DST/시간대 변경에서 기존 due instant와 세션 snapshot이 보존되는지 확인합니다. 다음 판정은 새 timezone의 Gregorian day로 계산되어야 합니다. 홈은 날짜/복귀 알림에 갱신되어야 합니다.
9. 같은 단어의 회독을 다시 완료해도 기존 SRS stage/count/due가 초기화되지 않아야 합니다. SRS 판정이 회독 snapshot을 변경해서도 안 됩니다.
10. Content DB 정렬/새 단어 추가 후 stable ID로 같은 항목을 읽는지 확인합니다. 비활성/누락 ID는 기록을 지우지 않고 오류를 표시해야 합니다.
11. Light/Dark, 작은 iPhone, iPad, 최대 접근성 글자 크기, VoiceOver를 확인합니다. 세 판정 버튼과 뜻/예문 스크롤이 겹치지 않아야 합니다.
12. ko-KR 없는 기기/녹음 파일 누락/일반·느린 속도/화면 이동 정지를 기존 Audio Service와 함께 확인합니다.

캘린더 테스트용 날짜는 테스트 코드의 명시적 fixture입니다. 앱의 예정일을 하드코딩하거나 production DB를 synthetic로 바꾸지 않았습니다.
