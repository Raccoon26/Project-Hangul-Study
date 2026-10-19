# DEV-08 Mac/iPhone 확인 (아직 미수행)

1. HangulStudy.xcodeproj에서 Debug/Release를 빌드합니다. `TEST_DESTINATION='platform=iOS Simulator,id=설치된ID' sh Tools/verify.sh`로 XCTest 71개를 실행합니다.
2. 이전 DEV-07 사용자 DB 위에 업데이트하여 v7 백업/migration과 기존 모든 학습 기록을 확인합니다.
3. 学ぶ→活用→가다/먹다/어떻다 등에서 기본형·의미·어간·target form·설명과 관련 문법을 확인합니다.
4. 한국어 키보드 조합 중 입력, 키보드 submit, 答える, 閉じる, 작은 iPhone/큰 글꼴에서 스크롤·버튼 가림을 확인합니다.
5. 정확한 답, 보아요/봐요 등 복수 답, 앞뒤 공백, 연속 공백, 먹을거예요 띄어쓰기, 철자 오류, 빈 입력, 500자 초과를 확인합니다.
6. 기존 예문 빈칸과 조건이 명시된 일본어→한국어 문장을 풉니다. 답안 확인 전 자동 다음 이동이 없어야 합니다.
7. 제출 전 종료하면 초안만 사라지고 같은 질문을 재개해야 합니다. 제출 직후/다음/오답 retry 뒤 종료하면 선택·결과·queue를 복구하고 중복 이벤트가 없어야 합니다.
8. 오답은 첫 묶음 뒤 한 번만 재확인하고 무한 반복하지 않아야 합니다. 완료를 영구 mastery로 표시하지 않습니다.
9. 입력 후 vocabulary SRS 등록과 기존 SRS stage/date 보존을 확인합니다. 예정일에 今日の復習에서 단어 의미 회상을 진행합니다. 생산형 SRS 화면을 제공하는 버전은 아닙니다.
10. 실제 음성 normal/slow/stop, 한국어 voice 부재, 화면 이동 후 정지, VoiceOver/Light/Dark/Reduce Motion을 확인합니다.
11. 한글/발음/단어/단어 회독·SRS/문법 회독·SRS의 기존 경로를 확인합니다.

현재 Linux 증거는 Python/SQLite 142 tests, Swift tree-sitter syntax입니다. 실제 Swift 실행이나 iOS 사용성을 대신하지 않습니다.
