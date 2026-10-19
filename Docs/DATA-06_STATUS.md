# PROJECT_STATUS — DATA-06

2026-10-03 작업 후 중단, 2026-10-04 재개하여 검수·테스트·문서화를 마무리했다. 새 콘텐츠 생성은80개에서 중단했다. 이전 DATA-05 상태와 집계는 `Docs/DATA-05_STATUS.md`, `Docs/DATA-05_PROGRESS.md`에 보존했다.

**Linux에서 Xcode build/Swift type-check/XCTest/실제 음성 및 UI 조작은 실행하지 못했다. 데이터 반영과 아래 실행 테스트는 완료했지만 iOS end-to-end 배포 검증 완료라고 주장하지 않는다.**

## 실제 추가 결과

- 신규 production Listening80개 + Questions80개. 의미선택20 / 한국어선택20 / 받아쓰기20 / 내용이해20.
- 入門21 / 初級59. 기존 production Example80개를 source UUID로 재사용. 신규 Example0, 중복 Korean 문장 생성0. 2문장 comprehension2개.
- 주제: 가족·자기소개·집·식사·학교·직장·약속·시간·쇼핑·교통·여행·날씨·감정·연락·부탁.
- 모든 새 항목은 원문/일본어/선택지/해설 self review와 기존 Validator를 통과. 기존 DATA-01~05 본문/ID/순서 변경0. 관계 추가 endpoint인 예문80개만 revision+1.
- 별도 DB/문장 source/진도/음성/채점 엔진을 만들지 않았다. UI 변경은 날짜 갱신/지연 조작 방어에 한정.

## DB / Content Version / set 정책

**Content schema4 / content13 / min reader7 / UserProgress8**. Source=`Content/production.json`, 실제 앱 bundle=`Resources/content.sqlite`.

v12 snapshot=`Tests/Fixtures/content-v12-production.sqlite`. 이를 previous로 strict build 수행. 기존 source question/listening/order/lesson/vocabulary membership 후보를 그대로 유지했다. 신규 listening은 level별 learning_order60부터 추가하여 기존20개 구간을 변경하지 않는다. intro 새 batch3(20)+4(1), beginner 새 batch3(20)+4(20)+5(19). 실행 중 session은 기존 질문 snapshot을 유지한다.

신규항목ID는 UUID이며 `Content/data06-ids.json`은 QA 목록이다. `data06-revised-ids.json`은 승인된 기존 예문 revision 목록. 배열 index는 ID가 아니다. audio source를 녹음으로 바꿔도 Listening ID를 유지한다. 새배포는 content14 이상과 v13 previous를 사용한다.

실제 DB: Vocabulary926(入門306/初級620), Meanings982, Examples1876(문장1863+발음예시13), Grammar42(入門22/初級20), Listening111(入門34/初級77), Questions342. Dictation총28. DATA_PROGRESS.md/Docs/DATA06_COUNTS.json 참조.

## Validator / Self Review

오류0 / 기존경고10(동형어 후보 저/차/일/쓰다/적다5, 짧은 발음예시5). validation rule/스키마/normalization을 약화하지 않았다. 누락·비활성 source, 빈 번역/accepted, 중복 선택지, 잘못된 level 등 negative case 거부 확인.

80문항을 다시 읽어 한국어·일본어·정답 유일성·난이도·선택지를 검토했다. 모호한 의미 distractor1개와 나이/요일/직업 한국어 distractor3항목을 개선했다. 받아쓰기는 원문/종결부호 생략만 저장, NFC/공백 처리는 기존 ProductionAnswer를 사용한다. 단어 의미가 비슷한 다른 문장을 정답으로 추가하지 않았다. 자세한 전문은 Docs/DATA06_REVIEW_CATALOG.md.

## Integration Audit

`Docs/DATA06_INTEGRATION_AUDIT.md`에 흐름별 실제 검사/미검증/실기기 체크를 구분했다.

- Repository: 총111개를 실제 level/batch SQL로 조회, 모든 batch20 이하. 신규80개 source와 answer 일치.
- Progress/SRS: 실제 SQL로 디스크 snapshot 재개, attempt 중복 거부, first/retry 구분, skill 분리. 기존 SRS stage4와 due 유지. due80개 중20개 조회·미래 제외·인덱스 확인.
- Content update: 모든 v12 ID/본문/순서 보존, 예문80 revision만+1. 기존 어휘/문법·한글/발음·활용/직접입력·듣기 SQL 회귀 유지.
- Grading/retry: 기존 shared judge 재사용. 실제 신규80개 정오답·빈입력·공백·NFD·오타 및 20문항 실패→재개→retry 완료 XCTest2개 추가. **native 실행은 미수행**.
- Audio/Navigation/접근성: 공통 AudioService의 normal/slow/stop/누락 fallback과 conditional transcript view, scene 종료 정지 경로 소스 감사. **실제 음성/화면/VoiceOver 테스트는 미수행**.

### Bugs Found

1. 듣기 catalog의 due 수가 화면을 계속 열어 둔 상태에서 날짜/foreground 전환 시 갱신되지 않음.
2. Task 실행까지 지연된 버튼/음성완료 조작이 이전 화면 revision인지 UI에서 확인하지 않는 race 위험. 실기기 연타 재현은 미수행.
3. 새 QA 테스트의 순서 가정 및 잘못된 컬럼명. 제품 오류와 구분한다.

### Bugs Fixed

1. scene active와 NSCalendarDayChanged에서 due와 activeReview 갱신.
2. submit/next/audio completion에 expectedRevision을 캡처하여 최신 session과 일치하는 조작만 저장. 기존 DB revision/transaction/PK 방어 유지.
3. QA를 row집합 비교와 실제 attempt 컬럼으로 수정, 전체 테스트 재실행 통과.

### Known Remaining Issues

- Xcode build/type-check, 84 XCTest, 실제 Audio·Navigation·VoiceOver·앱 강제종료 재개는 Mac/iOS 확인 필요. 작성된 XCTest를 실행한 것으로 집계하지 않는다.
- ko-KR voice가 없으면 제출을 열지 않고 안내/뒤로가기로 처리. TTS 음질/속도 실제 감수 필요.
- 현재 retry는 최대1회, 대상1개이면 즉시 다시 등장 가능. 무한 반복하지 않는다. retry 성공은 SRS 장기 성공으로 올리지 않는다.
- 향후 콘텐츠 대량 폐기 시 retired due ID의 처리 정책 보완 필요. 이번 작업은 기존 ID 폐기0.
- 현재 신규 intro는 주로 한국어 선택, beginner는 의미/받아쓰기/이해 문제다. 전체4유형균형은 맞췄으나 각level의 세부유형비율까지 동일하지 않다.
- 외부 전문언어 감수 미수행. 새 TODO/FIXME/placeholder 추가0.

## Build / Tests

- **Python/SQLite174개 PASS**: 기존168+신규6. 원본로그 Docs/TEST_RESULTS_DATA06.txt. Validator 부정 입력, 실제 query, large synthetic, migration/버전/관계/진도 회귀 포함.
- **Swift62파일 syntax error0**, tree-sitter. 컴파일/타입검사 아님.
- **Native XCTest84개 작성·미실행**(이번2개 추가). 기존 Audio fallback/normal/slow/stop/late completion 테스트 유지.
- Linux warm SQLite100회 median: batch목록0.0413ms / batch IDs0.0179ms / 단일question0.0090ms. 앱 시작 또는 실기기 성능 수치 아님.
- swift/xcodebuild 없음. `Tools/verify.sh`를 Mac에서 실행하고 audit의 manual 목록을 확인해야 한다.

## 주요 변경 파일 / 다음 단계

Content/production.json, data06-ids.json, data06-revised-ids.json, Resources/content.sqlite, Views/ListeningView.swift, Tests/ListeningTests.swift, Tools/ContentBuilder/test_data06_content.py, 기존콘텐츠 현재버전/count/승인revision 검증, 제작/진행/감사 문서.

다음 DEV/DATA는 먼저 native 검증을 완료한다. 그 후 새 콘텐츠는 schema4/UserProgress8 유지, v13 snapshot을 previous로 저장하고 기존 stable ID/세트/SRS를 보존한다. 새 녹음은 검증된 asset만 연결하며 비교·자모 TTS 금지 정책을 유지한다.
