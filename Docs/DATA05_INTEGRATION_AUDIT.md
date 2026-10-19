# DATA-05 Integration / Bugs

## 검증 구분

실행한 것은 Python Validator/Importer, 실제 production SQLite, Swift repository에서 추출한 SQL, 디스크 재개·트랜잭션·제약 검사, Swift 구문 파서다. **Swift 엔진·SwiftUI·AVFoundation을 Linux에서 실행한 결과가 아니다.** 테스트가 만든 UserProgress 샘플은 실제 사용자 파일이 아니다. 실제 사용자 데이터 파일은 제공되지 않았다.

| 연결 | 수행한 검증 | 남은 네이티브 검증 |
| --- | --- | --- |
| A Content → Vocabulary | 200 stable ID 전체 조회,210 meaning,예문/노트·검색·level·품사 조회 | 실제 카드 렌더링 |
| B Vocabulary → 회독 | 기존 sort 순서 보존, 새20개 set/position13 상태 저장·재개, membership UNIQUE | 추가 XCTest의 실제 reveal→learn→known→다음 회독 실행 |
| C 회독 → SRS | 실제 enrollment SQL, 중복 등록 방지, 기존 stage4 일정 보존, bounded due20 | 실제 회독 완료 트랜잭션/XCTest |
| D Vocabulary → Conjugation | 새8문제/7단어의 target·accepted·metadata·prerequisite 조회. ㄷ분기 오류 수정 | 전체 productionQuestions 생성, 새8형태와 ㄷ회귀 XCTest |
| E Example → Grammar | 11연결이 실제 grammarCard의 제한된 예문 조회에 모두 포함 | 화면 표시 |
| F Example → Listening | 신규4 source ID, level·TTS 원문·dictation accepted, 기존 Example 재사용 | 재생·듣기 제출 게이트 |
| G Listening → Progress/SRS | listening attempt 고유키, 중복답변 거부, skill별 SRS 분리·due | 새 문항 cold resume 및 등록 XCTest |
| H Audio | 공통 AudioPolicy/Service 호출, ko-KR/누락 음원 fallback·generation guard 소스 감사 | 기기 voice 유무/실제 음성/중단·복귀 |
| I Resume | 신규 vocabulary/listening JSON snapshot 디스크 재개, 기존 pass/review 회귀 SQL | Codable/앱 강제종료 후 재실행 |
| J Content update | v11→v12 strict previous gate; 기존 모든 ID·본문·lesson 구성·sort 보존, grammar8 revision만 관계 변경에 따라+1 | 실제 설치본 교체 후 확인 |

기존 grammar/한글/발음/활용/회독/SRS SQL 회귀와 15,000어휘·30,000예문 synthetic 테스트도 전체 suite에 포함된다. synthetic는 production에 들어가지 않는다.

## Navigation / 상태 경계 감사

- RootView의 각 NavigationStack, LearnView의 vocabulary/grammar/listening 경로, 학습 fullScreenCover의 종료·summary 갱신을 소스로 추적했다. 기존 back 버튼을 제거하거나 새 navigation 경로를 추가하지 않았다. **시뮬레이터 탭/뒤로가기 실행은 미수행**이다.
- 회독/SRS의 MainActor busy guard, expectedRevision, transaction, 고유 인덱스로 중복 저장을 방어하는 경로를 확인했다. 실제 SQL 중복 삽입·rollback 회귀 테스트가 통과한다.
- due0/대량 due, 빈 level query, missing ID, 복수 meaning, set1개/모두 known/모두 learn은 기존 SQL 또는 작성된 엔진 테스트로 구분해서 확인한다. Swift 엔진 경계 테스트는 미실행이다.
- example 없는 단어는 model에서 optional이다. 실제 production 신규 모든 meaning에는 예문이 있다. 없는 관계는 Validator가 거부한다.
- 홈은 날짜/시간 변경 및 scenePhase active에서 summary를 갱신한다. 듣기 화면은 playback token과 session revision으로 늦은 재생 완료를 거부한다.
- 음성이 없는 기기에서는 안내가 나오며 듣기 정답 제출은 열리지 않는다. 기본 뒤로가기로 나갈 수 있으나 기기 음성이 준비되기 전 해당 듣기 레슨을 완료할 수 없다. 이를 음성 재생 성공으로 기록하지 않는다.

## Bugs Found / Fixed

1. **ㄷ 불규칙의 조건·미래형 오류**: 기존 ConjugationEngine은 ㄷ→ㄹ 변경 후 원래 ㄹ받침처럼 처리하여 걷다에서 걸면/걸 거예요를 생성할 수 있었다. 걸으-를 유지하도록 수정. 걷다/듣다/묻다 회귀 기대값과 기존 살다의 살면/살 거예요를 함께 둔다. 소스 분기로 확인한 오류이며 Swift 실행 검증은 대기 중이다.
2. **비활성 어휘가 활용 목록에 남음**: productionVocabulary/productionQuestions가 question.is_active만 확인했다. vocabulary content_items의 활성 여부도 확인하도록 수정하고, active meaning 조회도 명시했다. 실제 SQLite에서 신규 target을 비활성화하여 목록·문제 조회 제외를 검사했다.
3. **활용 화면 background 음성 지속 경로**: onDisappear만 있어 홈 화면 전환 시 stop이 보장되지 않았다. scenePhase가 active가 아니면 stop 및 입력 focus 해제. 실제 AVFoundation 출력은 미검증이다.
4. **이전 문법 로딩의 늦은 오류**: task 취소/다른 grammarID 전환 후 이전 로딩 오류가 현재 화면 error를 덮을 수 있었다. CancellationError 무시 및 현재 grammarID 일치 시에만 오류 반영. 소스 경합 경로 수정이며 SwiftUI runtime 검증은 대기 중이다.

## Known Remaining Issues

- Xcode Debug/Release build, Swift type-check, XCTest82개, 시뮬레이터/실기기 UI·Navigation·Audio·Dynamic Type 검증은 실행하지 못했다. 구문 파서 통과는 이를 대체하지 않는다. Mac에서 `TEST_DESTINATION='platform=iOS Simulator,name=<installed device>' sh Tools/verify.sh` 실행 필요.
- 활용 엔진은 여전히 지원된 9형태와 검토된 override 범위다. 새 모든 predicate가 모든 형태의 직접입력 문제를 갖는 것은 아니다. 미지원 형태를 추측하지 않는다.
- SQLite warm query 성능만 측정했다. 실제 iOS cold launch/저사양 기기 메모리·성능 미측정.
- 검증 음원 없는 자모/발음 비교는 기존 녹음 대기 상태를 유지한다. 새 음원은 생성하지 않았다.
- 새 TODO/FIXME, placeholder, fixture UI 또는 독립 progress system은 추가하지 않았다.
