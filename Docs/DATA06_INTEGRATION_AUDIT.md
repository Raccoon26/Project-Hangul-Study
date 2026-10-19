# DATA-06 Integration Audit — 2026-10-04

실행 환경: Linux/Python/SQLite. Xcode/Swift compiler 및 iOS simulator 없음. SQL 실행과 소스 감사, 작성했지만 실행하지 못한 XCTest를 구분한다. 기존 사용자 DB가 제공되지 않아 테스트용 디스크 DB로 검증했다.

| 경로 | 실제 수행 및 결과 | 남은 확인 |
| --- | --- | --- |
| Source → Validator → bundle | v12 previous 엄격 검증, v13 생성. 오류0/기존 경고10 | 독립 전문 언어 감수 |
| DB → Listening | 실제 repository SQL로 총111항목 level/batch 조회. 세션 최대20. 신규80개 source/translation/choice/accepted 일치 | Swift decoding/type-check 실행 |
| Example → Vocabulary/Grammar | 원본 예문1876개와 vocabulary_examples/grammar_examples 전부 보존. 기존 FK와 관계 검사 통과 | 앱 화면 표시 |
| Vocabulary/Grammar → 회독/SRS | 기존 SQL/migration/등록/저장/버전/ID 회귀 테스트 통과. Content만 변경하고 UserProgress migration 불변 | 실제 엔진과 UI의 native 회귀 |
| Conjugation/Direct Input | 기존 metadata/accepted/관계/engine 기대값 데이터 회귀 통과. shared ProductionAnswer 변경 없음 | Swift 활용/normalization XCTest 실행 |
| Audio → Listening | 같은 KoreanAudioService 사용, 문장 TTS metadata80개 검사. stop-before-play/generation token/normal·slow/실패 fallback 소스 감사 | ko-KR 실기기 청취, 빠른 재생 연타, interruption/background |
| Listening → Grading | Validator로 단일 정답·중복선택지·원문 받아쓰기 검사. 80문항 self review. 실제 Swift judge 검증 XCTest 추가 | XCTest 미실행, 실제 정오답 UI 미실행 |
| Listening → Progress/SRS | 실제 repository SQL로 attempt(0/1) 복합PK·중복 제출 거부, listening skill 분리, due80개→20개 제한/인덱스 검사 | Swift transaction 전체 실행 |
| Resume/retry | 디스크 닫기/열기로 revision/answer/position/retry snapshot 유지와 attempt분리 확인. 실제 20문항 all-wrong→cold resume→all-correct retry XCTest 추가 | 강제종료와 Swift Codable/queue 전이 실행 |
| Content update | v12의 모든 ID/본문/순서 보존. 예문80개 관계 revision만+1. 기존 SRS stage4 및 다른 skill 스케줄 SQL 보존 | 실제 기존 설치 데이터 upgrade |
| Navigation | 홈/듣기/batch/session/result/retry/복습 경로 소스 추적. 기존 back navigation 유지. 무음/빈목록 안내 및 탈출 경로 확인 | simulator back stack, 빠른 push/pop |
| Accessibility | 정답 원문은 result가 있을 때만 View 생성. 재생 접근성 label은 정답 텍스트를 포함하지 않음. 한국어 선택 문제의 선택지는 의도적으로 노출 | VoiceOver 실제 tree 검사, 큰 글씨 기기 검사 |

## Bugs Found

1. ListeningCatalogView는 첫 task 이후 날짜/foreground 변경에 due 수를 갱신하지 않았다. 화면을 계속 열어 둔 상태에서 복습 숫자가 낡을 수 있다.
2. Task로 보낸 ‘다음/제출/재생완료’ 작업이 실행될 때 최신 session을 읽어, 이미 지난 화면 revision에 대한 조작인지 구분하지 못했다. repository는 stale 저장을 방어하지만 UI의 지연 작업도 무시하는 것이 필요했다. 실제 기기 연타 재현은 미실행, 소스에서 확인한 race 위험이다.
3. 추가한 QA 테스트에서 unordered SELECT를 순서 고정 비교했고, attempt 컬럼을 is_retry로 잘못 참조했다. 제품 버그가 아닌 신규 테스트 오류였다.

## Bugs Fixed

1. active scene 및 NSCalendarDayChanged에서 due/active session을 다시 읽는다.
2. action 생성 시 revision을 캡처하고 실행 시 일치할 때만 repository에 전달한다. 이전 playback question/revision guard와 repository optimistic revision 검사는 유지했다.
3. QA는 동일 row 집합 비교와 실제 schema의 attempt를 사용하도록 정정했다. 최종174개 테스트 전부 통과.

## Edge cases / 정책

- 0개: 빈 상태 안내, 학습 기록 삭제 안 함. 1개: 재시도 대상이 그 하나뿐이면 바로 재등장할 수 있지만 한 번만 재시도한다.
- all-wrong: 첫 pass에서만 retry 추가; retry에서는 재추가하지 않음. retry 정답은 first-pass correct나 SRS 성공으로 올리지 않음.
- 답변 버튼: heard/result/busy/audio gate + revision + DB transaction/attempt PK로 중복 방어. 완료 후 next는 모델이 거부한다.
- missing source/inactive source/empty accepted/duplicate distractor/invalid level은 제작 Validator 거부. runtime는 active join으로 누락 source를 제외한다.
- 없는 녹음/없는 ko-KR voice: 안전한 안내, 제출 unlock 안 됨. 녹음 필수 항목을 임의 TTS로 대체하지 않음.
- 기존 due 항목을 향후 대량 폐기할 때 retired ID로 인해 빈 review batch가 될 수 있는 정책은 아직 보완 필요. 이번에는 ID를 폐기하지 않았다.
- audio source 변경은 Listening ID를 유지. 이미 시작된 session은 snapshot 음원 설정을 끝날 때까지 유지한다.

## Known Remaining Issues / Mac 실행 체크

아래 항목을 실제 수행했다고 간주하면 안 된다.

1. Tools/verify.sh로 Xcode Debug/Release build 및 84 XCTest 실행.
2. 새 初級練習4에서 normal→slow→stop 연타, 두 번 submit/next, 화면 닫기 및 background. 기존 음성 겹침/후속 재생이 없는지 확인.
3. 의미/한국어/받아쓰기/내용이해를 각 1개 이상 실제 채점. 받아쓰기는 빈입력·여러공백·NFD·띄어쓰기만누락·철자오류 확인.
4. 일부 오답→앱 강제종료→feedback/queue 재개→retry→완료→due 복습. score와 SRS가 두 번 갱신되지 않는지 확인.
5. VoiceOver로 정답 공개 전 원문/번역이 숨겨져 있는지 확인(한국어 선택지 제외). Dynamic Type, keyboard, back stack 검사.
6. actual voice의 발음/속도는 청취 감수 필요. TTS 적합성 판정은 문장 형태 기준이며 실제 음성을 인증한 것이 아니다.

## Self Review

80문항 전체를 별도 pass에서 재검토했다. 약속을 다음 주로 미룬 문장의 ‘来週に決めた’는 정답과 겹칠 수 있어 취소 distractor로 바꿨다. 나이/요일/직업 한국어 선택지3개는 기존 예문의 더 가까운 대안으로 바꿨다. 문법적으로 가능한 다른 뜻을 ‘잘못된 한국어’로 규정하지 않고 ‘실제로 들린 문장’을 묻는다.

재사용80개, 신규 문장0개. 2문장 comprehension2개. 받아쓰기20개는 정확한 원문 및 종결부호만 생략한 답을 저장한다. 신규 항목과 choice의 QA 전문은 DATA06_REVIEW_CATALOG.md. 의미의 사실성/복수정답을 검토했으나 외부 전문 감수는 미수행.

## 성능

Linux warm SQLite 100회 median: batch 목록0.0413ms, 20개 ID범위0.0179ms, 단일문항0.0090ms. ID범위 및 question lookup은 인덱스를 사용한다. batch 집계는 order covering index 스캔과 group-by temporary B-tree를 사용한다. 앱 시작/음성/기기 메모리 benchmark가 아니다. 111항목의 작은 데이터 측정에서 대규모 성능을 보장하지 않는다.
