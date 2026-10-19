# PROJECT_STATUS — DEV-14 Release Candidate audit

2026-10-05. 이전 DEV-13 상태는 `Docs/DEV-13_STATUS.md`에 보존했다.

**판정: B — Conditional. App Store 제출 가능 판정이 아니다.** Linux에서 실행 가능한 데이터/SQL/정적 검사는 수행했으나 Xcode/Swift compiler가 없어 iOS build, SDK 링크, XCTest, 실제 StoreKit/광고/음성/기기 UI는 미실행이다. 아래 출시 gate를 모두 통과하기 전 배포하지 않는다. **Content: Expansion Required.** 장기 고급 과정 전체가 완성됐다고 표시하지 않는다.

## DEV-14 구현 / Bugs Fixed

1. `ConjugationEngine`: ㅚ+어→ㅙ 축약과 기존 ㅙ 유지 수정. 되다→돼요/됐어요/돼서, 뵈다→봬요, 꿰다→꿰요. native 회귀 테스트 작성; Swift 실행은 미검증.
2. `SQLiteGrammarProgress`: 문법 복습 답변 transaction에서 session.updated_at 갱신. Continue가 최신 문법 복습을 놓치는 문제 수정.
3. `SQLiteProduction`/ProductionView: Content 재조회 전에 저장된 직접입력 session snapshot을 복원. 관련 문법 설명 로딩 실패는 보조 안내로 표시하여 저장된 문제 진행을 막지 않음.
4. 직접입력 retry 이벤트를 `production_retry_*`로 구분. 첫 답변 정확도에서 retry를 제외하고 전체 시도 기록은 유지. 예전 이벤트는 신뢰할 수 있게 역분류할 수 없으므로 덮어쓰지 않으며 통계 화면에 한계를 안내.
5. `SQLiteProgressRepository`: 기존 DB의 dataset identity를 migration 전에 검사. 다른 dataset 파일을 변경한 뒤 거부하는 문제 방지.
6. `SQLiteConnection`: UTF-8 바이트 길이로 SQLite text bind/read. embedded NUL에서 입력이 잘리던 문제 수정.
7. `StudyDay`: 무한대/NaN 날짜 거부. Listening due/Grammar overdue 조회에서 지원 algorithm/version만 대상으로 삼음. 미래 버전 SRS 행은 삭제하지 않음.
8. `LearningErrorMessage`: DB 경로/SQL/내부 decoding 오류를 일본어 학습 UI에 그대로 노출하지 않도록 allow-list 적용.
9. `AdService`/RemoveAdsView: 비동기 개인정보 동의 갱신 중 화면 종료/background 시 늦은 form 표시 취소. SDK 실동작은 기기 확인 필요.
10. 문법 회독 판정 버튼은 큰 Dynamic Type에서 세로 배치 가능, 최소44pt 유지.
11. `Tools/verify.sh`: portable와 native 검증을 명시적으로 분리. 기본 실행은 Xcode/TEST_DESTINATION 없으면 실패하며 테스트를 조용히 생략하지 않음. Debug/Release simulator, Release device build와 XCTest 절차 포함.

## Architecture / 데이터 보존

Content SQLite(read-only bundle)와 UserProgress SQLite(writeable)는 분리. **Schema4 / Content13 / Reader7 / UserProgress10 유지.** 이번 변경은 새 학습 데이터/ID/DB schema를 추가하지 않는다. DEV-13 ZIP과 production.json 및 content.sqlite가 바이트 단위 동일함을 확인했다. 기존 stable UUID, 진행 중 set membership, SRS schedule을 재배정/초기화하지 않는다. 설정/광고 cap/검증된 구매 cache도 Content DB와 독립이다.

## Requirements Coverage Audit

전체 근거와 제한은 `Docs/DEV14_REQUIREMENTS_AUDIT.md` 참조. 실제 source/repository/persistence와 production DB를 확인했다. 문서의 완료 표시를 native QA 결과로 취급하지 않았다.

- 기반/한글/발음/어휘/문법/회독/SRS/직접입력/듣기/검색/관리/통계/설정/수익화는 코드 경로 존재, portable regression 대상.
- 상급 production curriculum, 전체 활용/자유작문, 전문 placement, 개별 발음 녹음은 부분 또는 미수록.
- iPhone UX/접근성/알림/결제/광고/오디오와 서명된 Release는 미검증. 이는 통과가 아니라 출시 gate다.

## Integration Audit

- Content→repository: strict source Validator, 실제 SQLite integrity/foreign keys, ID/meaning/example/level/search 관계 테스트.
- 회독→SRS: 기존 SQL 회귀에서 stable ID, 완료/중복/이전 schedule 보존 검사. native 엔진 실행과 구별.
- Grammar→Review→Continue: 답변 시 최근 시각을 실제 SQL로 검증.
- Production→Resume→통계: snapshot 우선 경로, retry 분리 SQL 검사 및 native 테스트 작성.
- Listening→grading/retry/progress/SRS: 기존 portable suite와 algorithm filter 검사. 실제 TTS 소리의 정확성은 검증 못 함.
- migration v1~10: 테스트 DB의 SRS/favorites 보존. 실제 사용자 파일을 수정하지 않음.
- 강제 종료: 별도 SQLite 프로세스에서4개 답변 commit 뒤 완료 변경을 commit하지 않고 강제 종료. 재개 DB는4개 완료/16개 미완료/세션 active, integrity 정상. iOS 앱 kill UI 테스트를 대신하지 않음.
- Ads/IAP: 학습 저장 이후 optional 광고, purchase/unknown 차단, cache/revocation/중복 guard 소스 및 portable 정책 검사. SDK/StoreKit 실행은 미검증.

## Micro-session / Commute UX Audit

Home Continue/오늘의 복습 진입 경로 유지. 각 답변/판정은 session 완료와 별개로 transaction 저장. 짧은 복습은 기존 엔진 bounded session 사용. 음성 없는 Vocabulary/Grammar 가능, 핵심 DB/network 독립. Listening은 재생 가능 환경 필요. 화면 종료/background에서 audio.stop 경로 존재. 주요 action 하단/min44pt, 지속 timer/polling/위치정보 없음. 실제 한 손 조작/전화 interruption/오프라인 TTS/notification 진입은 Mac+iPhone 체크리스트에 남김.

## Performance / Accessibility Audit

`Docs/PERFORMANCE_*_DEV14.json`은 Linux SQLite 측정이며 iPhone launch/FPS/배터리 수치가 아니다. 15,000어휘/30,000예문 생성·검증·DB build 성공, 전체 pagination stable ID15,000개. 300,000 study_events 통계 측정 포함. lifetime 집계는 전체 event index를 스캔하므로 장기 규모에서 비용이 증가한다; 통계 화면에서 실행하며 추후 캐시/증분 집계 판단.

SwiftUI semantic fonts/system backgrounds, VoiceOver labels/숨긴 listening 정답 경로를 소스에서 확인. Dynamic Type 버튼 개선. 모든 화면이 실제 최대 글자 크기/VoiceOver에서 통과했다고 주장하지 않는다. RTL은 이번 일본어 UI 대상 아님. 새로운 animation/배너/탭 없음.

## Tests / Build

최종 실행 기록: `Docs/TEST_RESULTS_DEV14.txt`, `INTEGRATION_DEV14.txt`, `STATIC_AUDIT_DEV14.json`, `VALIDATION_DEV14.json`.
- strict Validator 오류0/기존 경고10. 경고는 짧은 발음 예시5건 및 저/차/일/쓰다/적다 동형어 후보5건. 서로 다른 품사/의미로 유지; validator를 약화하지 않음.
- Swift88파일 tree-sitter 구문 오류0. 이는 typecheck/link/build가 아님.
- XCTest123개 작성(DEV14 신규6), **실행0**. iOS/StoreKit 테스트 성공 주장 없음.
- Python 테스트는 실제 SQLite/content 검사와 소스 계약 검사를 혼합한다. Swift 엔진을 실행하는 테스트가 아니다.
- 최종 suite 결과는 아래 Final verification에 기록.

## Bugs Found

위11개 항목 중 동작/안전성 문제를 수정했다. 첫 최종 회귀에서 기존 listening SQL 테스트2개가 새 algorithm bind 인자3개를 전달하지 않아 실패했다. 테스트 호출부에 현재 scheduler identity를 추가하고 기존 backlog/다른 skill 보존 assertion은 유지했다. 검증 규칙을 끄지 않았다.

## Known Remaining Issues / Release Gates

| 우선순위 | 남은 항목 | 재현/처리 |
| --- | --- | --- |
| Release gate | Xcode build/SDK resolution/native123 tests 미실행 | Mac에서 RELEASE_CHECKLIST 절차 실행; 실패 시 제출 금지 |
| Release gate | Bundle ID/Team/App Icon/ASC/개인정보 URL 미설정 | 소유자 설정과 실제 archive 점검 필요 |
| Release gate | 실제 구매/restore/offline/refund/광고/UMP QA | TestFlight sandbox 및 테스트 광고 기기 검증 필요 |
| Major | 활성 Vocabulary/Grammar review의 content가 비활성/삭제되면 안전 오류, 자동 skip/reconcile 없음 | 기존 ID를 삭제하지 말고 retirement 정책과 재개 복구를 다음 단계에서 보완 |
| Major: 범위 | 고급 단계 production 콘텐츠 부족 | 상위 level은 없음을 안내; 완성된 장기 전체 curriculum으로 마케팅 금지 |
| Major: 범위 | placement 낮은 단계의 간이 진단, 제한된 활용/작문 | 전체 레벨 진단/모든 예외/자유 작문 엔진 미완성 |
| Major: 품질 | 실제 한국어 TTS/일본어 교육 콘텐츠 전문가 검수 미실행 | 발음/음원 품질과 기기별 voice 가용성 검토 |
| Minor | 기존 직접입력 retry 통계는 first-attempt로 역분류 불가 | 새 기록만 분리, 과거 기록 보존/안내 |
| Minor/성능 | lifetime 통계 장기 event scan | 기기 실측 후 증분 집계 검토 |

검증한 범위에서 미수정 데이터 손실 P0를 재현하지 않았지만 미실행 환경까지 안전하다는 보증은 아니다. Production AdMob ID 부재 자체는 버그가 아니며 Release 광고 비활성은 정상 정책이다. App Store 제출은 위 gate 해결 후 별도 판정.

## DEV-15 / 다음 작업

Mac에서 native gate를 최우선 실행한다. Content를 늘리거나 광고 위치를 늘리기 전에 retired-content resume 정책과 실제 UI/SDK 결함을 해결한다. 새 데이터 작업은 Content14 이상, 기존 stable IDs/회원 기록 유지. 전체 release owner 작업은 RELEASE_CHECKLIST.md 참조.


### 측정값 (Linux / synthetic)

| 작업 | 측정 |
| --- | ---: |
| 15k어휘/30k예문 DB 생성 | 15.156초 / 50,712,576bytes |
| stable ID 단어조회 median | 0.0042ms |
| level50개조회 median | 5.2069ms |
| 예문관계 median | 0.0117ms |
| 전체15k pagination | 0.3368초 / unique15,000 |
| 15k어휘+500문법 substring검색 공통어 median | 62.013ms |
| 300k이벤트 오늘통계 median | 0.208ms |
| 300k이벤트30일통계 median | 3.080ms |
| 300k이벤트 lifetime통계 median | 178.483ms |

실제 UI frame time/메모리/배터리/기기 cold launch는 측정하지 않았다. broad substring 및 lifetime 비용은 크기가 커질수록 증가하므로 출시 전 기기 프로파일링 필요.

## Final verification

최종 `sh Tools/verify.sh --portable`: **221 tests / 55.537초 / OK**, monetization configuration guard 통과. 신규 DEV14 audit10개 포함. 단독 audit10개도 통과. 최초 SQL 테스트 인자 오류 수정 후 전체 재실행한 결과다. Swift88파일 구문 오류0. Production DB integrity=ok/외래키위반0/기존원본동일. Native build 및123 XCTest는 여전히 실행하지 않았으며 A Ready로 승격하지 않는다.

최종 결과물: HangulStudy-DEV-14.zip. 이전 상태/현재 변경목록/측정JSON/전체테스트로그/출시체크리스트를 포함한다.
