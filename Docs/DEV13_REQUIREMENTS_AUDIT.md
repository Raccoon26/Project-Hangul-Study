# DEV-13 Requirements / Integration Audit

2026-10-05. DEV-12 문서와 현재 소스·DB·진입점을 대조했다. 이전 상세 근거는 `DEV12_REQUIREMENTS_AUDIT.md`, 이번 코드 변경은 `CHANGES_DEV13.txt`에 남긴다. **‘소스 연결’과 ‘iOS 실행 검증’은 구분한다.** 이번 Linux 환경에서는 iOS/StoreKit/AdMob/UI/VoiceOver를 실행하지 못했다.

## Requirements Coverage Audit

| 범위 | 현재 근거와 판정 | 미완료 / 이번 수정 |
| --- | --- | --- |
| Content / UserProgress / IDs / versions | read-only bundle, 별도 user DB, Builder/Validator, schema4/content13/reader7/user10. 실제 DB 관계 검사 | 본문·ID 변경 없음. 삭제된 content의 active session 자동복구는 Major 잔여 |
| 한글 / 발음 / 자모 TTS 금지 | LessonSession, HangulComposition, production55/36, AudioPolicy | 기존 연결 유지. 개별 검증 녹음0, 실제 소리/기기 실행 미검증 |
| Vocabulary / 회독 | production card→뜻공개→판정→unknown-only→commit→SRS | 광고 호출은 commit 반환 이후 한 곳에만 추가. 학습 engine/repository에서 구매 의존 없음 |
| SRS / 날짜 / backlog / 여러 타입 | StepReviewScheduler, typed srs_state, bounded review, snapshots | 기존 테스트 유지. 실제 자정/시간대/OS lifecycle은 native QA 필요 |
| Grammar / 비교 / 문제 / 회독 / SRS | production42, GrammarCard/Question/Learning/Review | 수정 없음, SQL/관계 regression 실행. native 회독/Review 미검증 |
| Conjugation / Direct Input / Sentence | ConjugationEngine, ProductionAnswer, ProductionSession | optional updatedAt 추가, 과거 JSON 디코드 유지. 모든 활용/자유작문은 부분 구현 |
| Listening / Dictation / retry / Audio | 4유형111개, source Example, ListeningSession, AudioService | 광고 진입점 없음. 기존 저장/재시도/숨은 정답 처리 유지, 기기 QA 미실행 |
| Curriculum / Placement / Skip / Continue | 기존9단계/간이진단/모드별 경로 | **Major 수정:** 모듈 고정 우선순위 대신 최신 저장 활동 선택. 혼합 Unit/심화진단/상급 실제 콘텐츠는 부분 |
| Search / Details / Related / Saved | SQLiteLookup/SavedContent, LookupDetail, typed Favorites/Recent | 구매/광고 gate 없음. 조회가 SRS/회독을 변경하지 않는 기존 계약 유지 |
| Statistics / Maintenance | SQLiteStatistics, Records/Maintenance, 실제 event/due | 광고는 study_events를 쓰지 않음. 학습시간을 추정하지 않음. 자동혼합 유지학습은 미구현 |
| Micro-session / Resume / Offline | 기존 5/10/20 review, action별 transaction, bundle/local SQLite | Resume·중단·짧은 학습 광고 제외. 전체 Content preload 추가 없음 |
| Settings / Notifications | preferences/local reminder, Settings | 구매/복원 link만 추가. 알림 진입 광고 없음, due맞춤·요일·deep-link는 미구현 |
| Ads / IAP | AdService/PurchaseService/MonetizationPolicy/RemoveAdsView | 실제 코드 연결. GMA/UMP resolve·native build·실제 표시·구매 검증은 출시 gate |

사용자에게 전체 수년 과정이 완성되었다고 설명하지 않는다. 현재 Production은 어휘926/문장1863/문법42/Listening111이며 상급 데이터와 실제 개별 녹음은 부족하다.

## Integration Audit

| 연결 | 확인한 것 | 수행 범위 |
| --- | --- | --- |
| Content→전체 학습 | strict validator, 실제 bundle 관계·조회·enum·stable ID | Python/SQLite 211 PASS, source/DB DEV12 대비 불변 |
| Vocabulary→회독→SRS→광고 | model.act 성공/완료 확인 뒤 optional side effect; 광고가 DB/Navigation을 소유하지 않음 | callsite 검사 + 기존 SQL regression. Swift/UI 실행 아님 |
| IAP→AdService | checking/cache/unverified는 광고 차단, verified 변화 시 preload 폐기, load generation와 표시 직전 재검사 | source/policy XCTest 작성. StoreKit 실행0 |
| Ads→Audio/Navigation | 표시 직전 audio.stop, callback은 광고 내부 상태만 정리 | 소스 검사. 실제 playback/SDK callback은 기기 QA |
| Ads→Progress/Statistics | 광고 서비스에 repository 의존0, 완료 저장 후 광고, 광고시간 집계 없음 | 소스 검사. DB와 production payload 변경0 |
| Content Version→구매 | 구매 ID/Keychain/StoreKit과 content/schema/user migration 독립 | 소스 및 DB 불변 검사. 기존 update regression 유지 |
| Resume→Home | 각 active session의 timestamp를 SQL 비교, listening JSON 2001 epoch를 Unix로 변환 | 실제 query, cold reopen, 기존 progress/SRS 불변 PASS |
| 오래된 Production→Resume | 새 optional updatedAt, 기존 snapshot은 해당 content/session의 최신event로 fallback | 실제 SQL + content_id 시간 index 사용, JSON/기록 변경 없음 |
| Settings→구매/복원/개인정보 | 일본어 Form, localized price, 구매중 버튼 비활성, 복원·privacy action 연결 | 구문/소스 검사. UI/권한창 미실행 |
| AdMob Debug→Release | Debug 공식 demo IDs, Release empty-safe, test publisher 차단 | config 검사/검사도구 실행. 실제 Release build 미실행 |

## Micro-session / Commute UX Audit

- Home Continue/짧은 복습 진입은 기존대로 유지한다. 단어·문법·듣기 학습 중 광고를 끼우는 호출은 없다.
- 4개 단어, 5~7개 짧은 복습, 듣기2개, 알림/Resume 직후에는 광고 경계 자체가 없다. Vocabulary 세트20개 이상을 마쳐도 연속 foreground12분 미만이면 제외한다.
- 기존 세션을 재개했거나 화면 체류 중 inactive/background가 있었다면 그 체류에서는 광고를 제외한다. 방해가 있었던 사용자를 수익화 목적으로 새 세션으로 취급하지 않는다.
- 새 세트의 실제 완료 항목 누적60개, 마지막 표시 시도 후30분, 현재 세트20개 및12분을 모두 요구한다. 중간 종료는 완료로 세지 않는다. uptime는 광고 자격용 경과시간이며 학습 통계시간이 아니다.
- 진행상태 저장은 기존 SQLite transaction이며 광고 성공/실패/닫힘과 무관하다. 화면이 사라진 뒤 completion Task가 끝나도 광고를 표시하지 않는다.
- Offline/음성 없이 가능한 학습은 그대로다. 광고·상품 조회는 비동기이며 Home/학습 진행을 대기시키지 않는다. 초기에 Google SDK를 초기화하지 않는다.
- 지속 timer/polling/background work 추가0. 광고 요청은 학습 진입에서만, 재시도는 최소10분 간격이다. 실제 배터리/launch 지연은 미측정이다.
- SwiftUI Dynamic Type/시스템색/44pt 버튼 유지. Settings에 작은 진입점 추가, 새 Tab/banner/학습 paywall 없음. 실제 VoiceOver/최대글자/한손 검증은 남았다.

## Bugs Found

1. DEV12 Major: Continue가 모듈 우선순위 때문에 가장 최근 Listening/Production보다 오래된 단어 세션을 제시함.
2. 구현 중 방어 공백: 초기 entitlement 확인보다 먼저 단어 화면이 열리면 preload 기회가 없어짐; 오래 걸린 load가 구매 이후 완료될 수 있음.
3. 구현 중 방어 공백: 중복 completion/delegate와 stale entitlement refresh가 빈도·권한 상태를 덮어쓸 위험.
4. 기존 패키징 테스트가 test resource 목록을 한 파일로 고정해 StoreKit test resource 추가를 실패로 판정함.

## Bugs Fixed

1. 최신 활동순으로 변경. Production optional updatedAt 및 legacy event fallback, Listening updatedAt의 epoch 변환. 실제 SQL에서 완료 세션 제외/차가운 재실행/서로 다른 모듈 순서를 검사했다. fallback는 기존 content_id/date index로 조회한다.
2. free 상태로 확인된 후 학습 화면에서 preload 재시도, purchase state 변경 때 객체 폐기/generation 증가, 실제 표시 직전 entitlement/busy/foreground/visible 확인. load callback에서 표시하지 않는다.
3. UUID boundary 중복 제거/빈도 선소비, presented object identity로 오래된 callback 무시. verified transaction 도착 시 generation을 올려 이전 refresh 결과의 덮어쓰기 방지.
4. 패키징 테스트 기대값을 fixture와 StoreKit test resource 두 개로 갱신. production/fixture 분리 검사는 그대로다. Validator 규칙은 변경하지 않았다.

위 SDK 관련 항목은 코드 감사에서 발견한 위험과 방어 수정이다. 실제 iPhone에서 재현·수정 확인했다고 주장하지 않는다.

## Known Remaining Issues

- **Critical 출시 검증 gate:** Xcode Debug/Release type-check/build, SDK resolve,117 XCTest(정책12+StoreKit1 신규), 실제 구매/복원/환불/offline/광고·동의·음성·알림·Navigation·VoiceOver 미실행. Python211개 통과는 이를 대체하지 않는다.
- **Major 콘텐츠/제품 범위:** 상급 curriculum/검증된 개별 녹음/심화 placement/혼합 Unit/전체 활용·자유작문 미완성. 기존 범위를 광고 상품으로 잠그지 않았다.
- **Major active content 누락:** active stable ID가 삭제되면 오류+닫기 경로이며 자동 skip/replacement 없음. 이미 배포한 ID를 삭제하지 말 것.
- **Minor legacy Resume:** 과거 production snapshot에 timestamp가 없고 아직 답변 event도 없으면 최근활동을 복원할 근거가 없어 timestamp0/tie-break를 쓴다. 다음 의미있는 action부터 updatedAt을 저장한다.
- **Minor 기존 UX:** 짧은 preference는 단어 SRS용, 유지학습 자동혼합 없음, 알림은 일반 daily invitation. 기존 디바이스 UI 검증 필요.
- **운영 정책:** Release consent가 필요한 사용자는 Settings에서 직접 확인하기 전까지 광고 없음. 동의 노출률보다 학습 방해 방지를 우선한 선택이며 버그로 숨기지 않는다.
- Production AdMob ID 미제공은 의도된 비활성 configuration이며 버그/미완성으로 분류하지 않는다. App Store Connect 실제 상품/가격 설정은 소유자의 출시 전 작업이다.

## 검사 결과

- `TEST_RESULTS_DEV13.txt`: **211 tests / 50.490s / OK**. 초기 전체 실행의 fixture resource 문자열 기대값 실패를 수정한 뒤 전체 재실행했다.
- `VALIDATION_DEV13.json`: 오류0/기존 검토 경고10. 콘텐츠/사용자 schema 버전 변경 없음.
- `STATIC_CHECKS_DEV13.json`: Swift86파일 구문 검사, native117 작성/실행0. 정확한 최종 결과는 해당 파일 기준.
- `PERFORMANCE_DEV13.json`: 실제 Resume SQL, synthetic300,000 events/legacy active20. 첫조회0.374ms, 이후0.017~0.031ms. iPhone launch 측정 아님.
- 실제 Mac/iPhone QA와 환경 설정은 루트 `RELEASE_CHECKLIST.md`에 기록했다.
