# DATA10-1 첫 Mac native 실행에서 확인한 후속 gate

2026-10-20 JST. 기존 PR #17의 runtime/Tests를 바꾸지 않고 Xcode27.1에서 기존141개 XCTest suite를 시도했다. 첫 iOS17.0 iPhone15Pro 실행은126메서드 시작/121PASS·4FAIL·StoreKit1미종료 뒤 중단(exit143)했으며15개는 시작 전이었다. iOS26 재시도 및 최종 실행수/실패/exit/시간은 `DATA10_TEST_RESULTS.json`과 `DATA10_PROGRESS.md`를 따른다. 이번은 분석 단계이며 테스트 삭제·assertion 완화·엔진/데이터 수정0이다.

## DATA08 P1 native 회귀

| 기존 P1 | 실제 XCTest | 이번 확인 범위 |
| --- | --- | --- |
| P1-01 비활성 카드 복습 정지 | `SRSTests.testDATA08DeferredReviewsPreserveSchedulesAndRetryAfterContentUpdate`, `ReleaseAuditTests.testDATA08UnavailableVocabularyReviewContinuesWithoutLosingProgress`, `testDATA08UnavailableGrammarReviewContinuesWithoutLosingProgress` | PASS. vocabulary/grammar/practice API·원SRS·due·snapshot·completed/deferred 분리, cold reopen, 실제 ViewModel의 unavailable 안내/다음 진행 |
| P1-02 dictation 끝 .!? 생략 오답 | `ListeningTests.testDATA08AllDictationsAllowTerminalPunctuationOmissionOnly` | PASS. 현재1,850받아쓰기 실제 Swift 판정, 철자/내부 부호·일반 ProductionAnswer 비확대 |
| P1-03 listening due 퇴역 prefix 은폐 | `ListeningTests.testDATA08UnavailableListeningDueIsReleaseScopedAndPreservesSnapshots` | PASS.45due/25보류·버전 재확인·기존 snapshot·원SRS 보존 API. 실제 `ListeningStudyView.open()`의 화면 흐름 전체/전화·음성·VoiceOver는 미실행 |

위5개 메서드는 전체141개에 포함되며 추가 고유 테스트 수로 더하지 않는다. 실제 iPhone 조작·오디오·접근성 P1 gate는 남긴다.

## NATIVE-01 / 기존 DATA06 테스트의 cohort 경계 (테스트 보수 필요)

`Tests/ListeningTests.swift:111`의 `testData06RealItemsGradingAndAudioPolicy`가 intro/beginner의 batch>2 전체를 모은 뒤80개/각task20개를 기대한다. 실제 DATA06 registry는80개이며, 이후 DATA07이 beginner order200/201에 의미·Korean 각1개를 추가했다. 현재 query결과82, 의미21/Korean21로3assertion 실패한다.

추가 ID는 `499a1477-6fb9-4116-a332-12698dd62d46`(meaning/order200), `20ca4689-5519-4774-bf1b-a681d116a7b9`(korean/order201). 기존 `Content/data06-ids.json`으로 cohort를 고정하고 나머지 전체 조회/판정 검증은 유지하는 것이 후속 수정안이다.80을82로만 바꿔 당시 cohort 검증을 없애지 않는다. 이번 source/ID/learning_order를 되돌리지 않는다.

## NATIVE-02 / 발음 테스트의 courses.last 가정 (테스트 보수 필요)

`PronunciationTests.testPronunciationCourseQueriesAndQuizAnswers`는 course 목록이 한글/발음2개뿐이고 `courses.last`가 발음이라고 가정한다. 현재 generic courses에는 DATA08 vocabulary course도 있다. 그47레슨/911어휘 preview를 발음36규칙/14레슨/3듣기로 비교해 **917assertion**이 실패했다.917개의 독립 runtime 오류로 집계하지 않는다.

`testListeningGateAndPronunciationProgressReopen`도 `courses.last`에서 ‘単語を読んで聞く’를 찾아 XCTUnwrap1개가 실패했다. 이2메서드 합918assertion이며 실제 발음 코스 ID 또는 kind/목적에 따른 명시 조회로 고정하는 후속 보수가 필요하다. 저장소의 실제 발음36개·기존14레슨을 삭제하거나 임의로 코스를 재정렬해 통과시키지 않는다.

## NATIVE-03 / 활용 생성과 테스트 기대값 (출시 P1 후보, 미수정)

기존 `ReleaseAuditTests.testConjugationOeContractsToWaeAndWaeStaysWae`에서 **7assertion**이 실패했다. actual→테스트 expected는 되요→돼요, 됬어요→됐어요, 되서→돼서, 뵈요→봬요, 뵜어요→뵀어요, 뵈서→봬서, 뀄어요→꿨어요다. 마지막1개를 포함해 전부 엔진 오류라고 자동 판정하지 않는다.

실제 `LearningEngine/ConjugationEngine.swift`의 contracted table은 vowel11(ㅚ)을11로 유지한다. 되/뵈의6개 native 결과는 잘못된 축약 생성의 재현이며 **교육적 오답을 보여줄 수 있어 우선 P1로 추적**한다. [한국어기초사전 되다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=89858)의 되어/돼, [뵈다의 활용](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=65573)의 뵈어/봬를2026-10-20 확인했다. 이 사전 확인은 현재 모든 콘텐츠의 외부사전 검수 완료가 아니다.

반면 꿰다 과거 테스트의 expected `꿨어요`는 그대로 정답으로 인증할 수 없다. [한국어기초사전 꿰다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=37786)는 꿰어/꿰 활용을 제시한다. 후속 수정 시 꿰었다/뀄다 등 허용형과 테스트 expectation을 규범 근거로 먼저 확정해야 한다. 실패를 없애기 위해 엔진을 테스트의 오기 가능성에 맞추지 않는다.

현재 DB에 bare 되다/뵈다/꿰다 표제어는 없지만 `시작되다`·`변경되다` 등 **-되다 predicates85개**가 있다([전체 ID/정적 후보와 DATA06 초과2개](DATA10_NATIVE_IMPACT.json)). `SQLiteLookup.vocabularyDetail`은 authored question override를 수집한 뒤 실제 ConjugationEngine으로 present/past/future를 만든다.85개는 SQL 정적 영향 후보 수이며85개 UI/모든형을 실행해 오류 확정한 수가 아니다. Production authored answer·override와 Dictionary 생성의 영향 범위를 분리해 조사해야 한다. 현행 -고 문항/듣기 원문을 잘못된 생성형으로 덮어쓰지 않는다.

후속 명시 작업에서 공식 활용 근거→실제 관련85개/override 영향 조사→엔진과 잘못된 test 기대값의 필요한 최소 수정→전체 portable/native·Dictionary/Production/기존 snapshot 재검증 순으로 처리한다. 이번은 기록과 분석으로 종료하며 런타임 수정·Production 교체0이다.

## NATIVE-04 / StoreKit cold entitlement cache (원인 미확정, 미수정)

iOS17 첫 실행의 local StoreKit 메서드는 응답이 끝나지 않아 중단했다. storekitd 진단에는 AMSErrorDomain204/동기화 응답 누락 등이 있었지만 이것만으로 근본 원인이나 모든 StoreKit 경로를 단정하지 않는다.

iOS26 재시도에서는 해당 메서드가3.443초 만에 종료했고 `StoreKitPurchaseTests.swift:30`의 cold 새 인스턴스가 expected `offlineProtected` 대신 actual `checking`을 반환하는 **1assertion**이 실패했다. 해당 메서드의 purchase/verified·명시 refresh/restore의 다른 assertion은 실패하지 않았지만 메서드 전체는 FAIL이다. `PurchaseService.init`은 cache.read가 없으면 checking이며 `PurchaseCacheStore`는 Keychain read/write 실패 원인을 노출하지 않으므로 이번 근거로 서명/Keychain 환경 문제와 앱 저장 오류를 구분해 확정할 수 없다. 이 실행은 `CODE_SIGNING_ALLOWED=NO`다.

후속 Mac 작업은 실제 서명·Keychain 저장/읽기 상태를 진단한 local StoreKit 재검증과 기존 구매자의 cold/offline 보호를 우선 확인해야 한다. 실패를 skip하거나 실제 결제로 우회하지 않는다. Release/debug namespace·cache·권한 코드는 이번에 변경하지 않는다. 실제 기기/production 구매·광고·철회/오프라인 gate는 BLOCKED로 유지한다.

## Xcode 명령 종료·추가 진단의 한계

iOS26의 원시 로그에는 **141개 모두 종료(136메서드 PASS/5FAIL), assertion929실패, unexpected0, suite24.463초**가 있다. 그 뒤 Xcode의 `XCTHRunDestinationAllocator.collectSimulatorDiagnostics`가 semaphore 대기하는 것을 process sample로 확인해 명령을 중단했다(exit143). sealed xcresult/일반 exit65를 확보한 실행으로 표현하지 않는다. 원시 XCTest 종료와 Xcode 명령 정상 종료를 분리한다.

`-collect-test-diagnostics never` 재시도는 새 XCTest 시작 전에 `SimDevice.installApplication`/`host_support_mig_install_app_with_info`에서 대기하는 것이 확인돼 중단했다(exit143). 테스트0이며 기존141개 결과를 재통과한 것으로 더하지 않는다. 임시 서명으로 cold cache를 비교하려던 별도 빌드도 이 Mac의8GB 메모리/병렬 컴파일 부담 때문에 중단했고 XCTest0이다. 원인 확정/서명 검증 PASS로 표시하지 않는다. 다음 Mac 검증은 Xcode/CoreSimulator 상태를 재설정·확인하고 단일 Simulator/낮은 build jobs·active architecture로 같은141개와 Keychain 진단을 실행해야 한다. 기기/사용자 데이터를 erase하거나 앱·테스트를 완화해 우회하지 않는다.

실행 중 project.pbxproj/Info.plist의 형식 재직렬화가 감지됐다. 원래 파일과 변경본을 `/tmp/hangul-data10-1/xcode-rewrites`에 보존하고 plutil/plistlib로 전체 semantic tree가 동일함을 확인한 뒤 원래 byte를 복원했다. 값/설정 변경은 없고 최종95개 보호 파일을 다시 대조한다. 처음부터 있던 미커밋 변경은0이었다.

## 빌드 경고·출시 한계

Xcode27.1/Swift5 language mode는 `KoreanAudioService.deinit`의 non-Sendable observers 접근에 Swift6 전환 경고, AdService async 대안, SDK/TestKit deprecation, simulator 아키텍처/배포 target 경고를 출력했다. 빌드 성공과 경고0을 혼동하지 않는다. 억제 flag나 언어 모드 변경으로 숨기지 않았고 후속 호환성 점검 대상으로 남긴다.

실제 음성·통화/이어폰·강제종료 UI·VoiceOver·IME·3~10분·메모리·서명 archive·기기 구매/광고·독립 원어민/교사 검수는 이 XCTest 실행만으로 완료되지 않는다. **Release B—Conditional, 새 활용 P1 미수정 및 나머지 출시 gate 유지.**
