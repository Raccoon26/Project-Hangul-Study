# DATA-04 검증

## 실행함

- `python3 -m unittest discover -s Tools/ContentBuilder -p 'test_*.py'`: **159 tests / 37.194s / OK**.
- normal production build + corrected v10 previous release gate: 오류0, 기존 경고10.
- SQLite integrity / foreign keys / header-metadata equality / exact stable IDs and payload changes.
- 실제 Swift repository에서 추출한 SQL: 문법 레슨 pagination, 30개 card/example/question/비교, 5개 직접입력, 3개 듣기 source, SRS due 및 기존 스케줄 보존.
- 실제 별도 UserProgress SQLite 디스크 재열기로 저장 데이터 보존. 사용자 데이터와 콘텐츠 DB를 합치지 않았음.
- Swift 62파일 tree-sitter 구문 검사. 앱54파일 DEV-09와 byte-identical. Xcode 프로젝트 Swift 참조, plist/XML 파싱.

## 실행하지 않음

- Xcode Debug/Release build / Swift type-check / XCTest80개 / Simulator.
- 실제 GrammarLearning 및 ConjugationEngine 네이티브 실행. SQL 검사와 별개임.
- iPhone VoiceOver/Dynamic Type/Light-Dark/UI, 실제 normal/slow TTS 음질·학습 적합성.
- 외부 언어·교육 전문가 감수.

## Mac에서 필요한 gate

```sh
sh Tools/verify.sh
TEST_DESTINATION='platform=iOS Simulator,id=YOUR_SIMULATOR_ID' sh Tools/verify.sh
```

새 XCTest `testDATA04AllNewLessonsPassResumeAndEnrollSharedSRS`는8개 신규 레슨 전체를 학습·문제·완료·SRS·cold resume으로 확인합니다. `testDATA04GrammarLinksGenerateAcceptedForms`는5개 대표 grammar와 실제 generated/accepted 답안 관계를 확인합니다. 실제 실행 전 성공을 주장하지 마세요.

실기기에서는 기존 문법 레슨 진행 중 상태가 있는 DB를 사용해 업데이트하고, 새 레슨 접근과 오늘의 복습, 듣기 練習2, 의미 공개/정오답/종료·재개를 확인하세요. 앱 번들에는 원본 v10 fixture가 아니라 정상 v11 content.sqlite만 들어갑니다.
