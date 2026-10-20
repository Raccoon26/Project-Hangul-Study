# DATA-09-7 user request

DATA-09-7을 진행하세요.
DEV-01~14 / DATA-01~08 및 DATA-09의 확인 가능한 기존 요구사항을 실제 코드·DB와 비교하여 누락·부분 구현·테스트 부족을 감사하세요.
특히 Grammar→Quiz→회독/SRS→Resume 흐름, 선행 문법 오류, 문제 채점, 중복 Progress, 잘못된 Example 참조, Content Migration, Search, Offline 동작을 검사하세요.
Content DB↔Curriculum↔Vocabulary↔Grammar↔Conjugation↔Sentence Production↔Listening↔SRS↔Search↔Statistics↔UserProgress 전체 연결도 회귀 검사하세요.
DATA-08에서 코드 수정한 P1 세 건의 실제 회귀 상태도 추적하세요. AdMob/StoreKit 권한과 콘텐츠 업데이트의 독립성을 유지하세요.
P0/P1은 우선 수정하고 재현 테스트를 추가하세요.
Portable/Unit/Integration/Regression Test 및 가능한 빌드를 실행하세요. Xcode가 없다면 iOS Build·XCTest137개·실기기 검증을 완료로 표시하지 마세요.
PASS/FAIL/BLOCKED/NOT TESTED를 구분하고 DATA09_PROGRESS.md에 기록하세요. 이번 단계에서 종료하세요.
