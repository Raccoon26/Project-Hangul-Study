# DEV-09 Mac/iPhone 검증 — 아직 미수행

Linux에서는 Python/SQLite 149개, Swift 구문 검사를 수행했습니다. 아래는 실제 기기/네이티브 확인이 필요한 절차이며 실행 결과가 아닙니다.

1. `TEST_DESTINATION='platform=iOS Simulator,id=설치된ID' sh Tools/verify.sh`로 Debug/Release와 XCTest 78개 실행. 네이티브 실패가 있다면 다음 기능보다 먼저 수정합니다.
2. DEV-08 사용자 DB에 앱 업데이트. v7→v8 백업/비파괴 migration, 기존 단어·문법 SRS/회독/레슨/생산 세션 보존 확인.
3. 学ぶ→リスニング→入門→練習1의 12문항. 初級도12문항이며 네 유형이 각3개인지 확인.
4. 최초 자동재생 없음. 再生/ゆっくり/停止. 실제 완료 전 선택·받아쓰기 제출 불가. 실패·중단 callback은 heard/play count를 올리지 않아야 합니다.
5. 원문/번역은 제출 전 화면/VoiceOver tree에 없어야 합니다. Korean 선택형의 후보 자체는 읽을 수 있지만 어떤 것이 정답인지 미리 알리지 않아야 합니다.
6. 받아쓰기: 정확한 답/마침표 생략/앞뒤·중복 공백/띄어쓰기만 틀림/받침·모음·조사 오류/빈 입력/500자 초과. 정답 원문과 사용자 입력 비교 및 일본어 이유 확인.
7. 한국어 IME 조합 중 제출, 키보드 submit/閉じる, 작은 iPhone/가장 큰 글꼴에서 하단 버튼·입력 스크롤 확인.
8. 최초 전부 오답→한 번 재시도→또 전부 오답이어도 종료. 최초 correct/wrong과 retrySuccess가 별도인지 확인.
9. 재생 완료 직후/제출 직후/다음 직후/재시도 중 강제 종료. 같은 문제/저장된 선택지/결과/queue 재개. 제출 전 초안만 저장되지 않는 정책 확인.
10. 첫 제출 후 listening SRS stage0/다음날 등록. 기기 날짜를 검증용으로 변경하여 due에서만 복습 진입, correct stage증가/spacing보수간격/incorrectstage0 확인. retry성공은 stage를 재차 올리지 않아야 합니다.
11. 일반 연습 반복은 기존 SRS 날짜를 유지. 단어/문법 일정과 분리. backlog20개후 나머지 유지. Content 업데이트·source정렬변경에도 active snapshot 보존.
12. 한국어 voice 없는 기기, missing recording, 음성 재생 실패. 일본어 voice로 대체하지 않고 기록 유지. 녹음 seed는 없으므로 missing 경로는 XCTest를 사용합니다.
13. 전화/Siri/Bluetooth disconnect/route변경/화면이탈/background에서 정지·안전 복구. 실제 speaker/headphone 청취로 문장·normal/slow 발음 품질 확인. background audio권한 없음.
14. Light/Dark, Dynamic Type, VoiceOver와 TTS 상호작용, Reduce Motion 점검.
15. 기존 한글/발음/어휘/회독/SRS/문법/활용/직접입력 회귀 확인.

정답과 뜻이 유사한 다른 문장의 자유채점, speech recognition, 마이크, adaptive listening mastery는 지원하지 않습니다. 외부 교육 감수와 실제 TTS 청취도 출시 전에 필요합니다.
