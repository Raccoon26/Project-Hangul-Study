# PROJECT_STATUS — DEV-13

2026-10-05. 이전 상태는 `Docs/DEV-12_STATUS.md`에 보존했다. 중단 전 구현을 이어 받아 검증·문서화했으며 중단 대기시간은 작업시간에 포함하지 않았다. 이번 단계는 광고 위치 확대보다 entitlement, 학습 저장 분리, 기존 Major Resume 문제를 우선했다.

**구현은 추가했으나 출시 검증 완료는 아니다. Linux 환경에 Swift compiler/Xcode/iOS Simulator가 없어 SDK resolve, native build/117 XCTest, 실제 StoreKit 구매·광고 표시·동의·기기 UI는 실행하지 않았다. 수행한 검증은 Python/SQLite211개, strict Validator, Swift 구문/설정 검사다.**

## DEV-13 구현 / Ad architecture

- `MonetizationConfiguration`에서 Bundle의 build-substituted 설정을 읽는다. Debug/Release base configuration은 각각 `Config/Debug.xcconfig`, `Config/Release.xcconfig`다.
- 공식 GoogleMobileAds13.11.0 / GoogleUserMessagingPlatform3.1.0 SPM dependency를 Xcode project/generator에 연결했다. API는 현재 공식 Swift 명칭을 확인했다. 실제 다운로드·링크·실행은 Mac 검증이 필요하다.
- `AdService` 한 곳에서 광고 load/consent/presentation/cap을 관리한다. Google SDK import는 이 서비스에만 있다. 학습 repository, 완료 저장, SRS, Navigation에는 의존하지 않는다.
- 광고는 **Interstitial만**, **Vocabulary 세트 완료 한 곳만** 후보다. Home/banner/app-open/rewarded 광고 없음. Settings/Search/상세/문제/듣기/한글/문법/복습 카드 사이/알림 시작/Resume 시작에는 표시 호출이 없다.
- `VocabularyStudySessionView.perform`이 기존 `model.act`를 기다리고 성공·완료·동일 session·visible을 확인한 후 optional side effect로 호출한다. 광고 load를 기다려 완료시키거나 callback에서 progress/navigation을 변경하지 않는다.

## Frequency cap / Micro-session 보호

모두 충족해야 표시 후보가 된다:

1. 새 session으로 시작하여 현재 단어 세트20개 이상 완료.
2. 현재 세트에서 연속 foreground12분 이상. 화면이 inactive/background로 갔거나 기존 session을 재개한 경우 제외.
3. 마지막 광고 이후 완료 세트의 단어 누적60개 이상.
4. 마지막 표시 시도 이후30분 이상. 시계가 뒤로 가면 보수적으로 표시하지 않음.
5. StoreKit에서 무료 상태 확인, 구매 flow 아님, 유효한 configuration/consent, 현재 foreground, 준비된 광고50분 미만, 실제 controller에서 표시 가능.

`monetization.frequency.v1`에 누적량/마지막 시도일/최근100개 session UUID를 저장한다. 중복 callback은 재집계하지 않는다. 표시 직전에 cap을 소비하므로 SDK 표시 실패도 추가 광고를 늦출 수 있다. 수익보다 빈도 상한을 우선했다.

uptime 경과시간은 광고 자격에만 사용하며 학습 통계시간이라고 주장하지 않는다. Timer/polling 없음. preload는 학습 화면 진입에서 기회가 있을 때만, 실패 포함 요청 간격 최소10분. 준비되지 않았으면 바로 건너뛰고 늦게 load되었다고 자동 표시하지 않는다. 화면을 닫거나 구매하면 늦은 요청은 generation guard로 무효화된다.

## Debug / Production / Privacy

- **TEST ONLY:** `Config/Debug.xcconfig`에 Google 공식 테스트 App ID/Interstitial ID 한 쌍. Swift View/Service에 full ID 하드코딩 없음.
- **Production 현재 미설정:** `Config/Release.xcconfig`의 ADMOB_APP_ID / ADMOB_INTERSTITIAL_ID는 비어 있다. 이것은 이번 단계의 버그가 아니다. 빈 값/잘못된 형식/test publisher/서로 다른 publisher는 광고 비활성이다.
- Info.plist 키는 `GADApplicationIdentifier`, `AdMobInterstitialIdentifier`. 공식 quick-start의 SKAdNetwork50개를 포함했다. 실제 소유자 값 교체·최종빌드 검사 절차는 `RELEASE_CHECKLIST.md`에 있다.
- `Tools/check_monetization.py`: Release absent-safe 확인, `--require-ads`로 출시 설정 강제, `--built-info`로 실제 앱 plist 검사. 계정 소유권을 증명하는 도구는 아니다.
- Release는 UMP의 해당 launch 상태 갱신과 canRequestAds를 확인한다. 필요한 동의/개인정보 form은 사용자가 Settings에서 여는 방식이다. 첫 실행/학습 중 자동 form 없음. 동의가 없거나 확인 실패면 광고 없이 학습한다.
- Debug 공식 demo unit만 동의 게이트 없이 테스트 광고 요청을 허용한다. 소유자 UMP 게시 메시지가 없는 환경에서 SDK를 시험하기 위한 분리이며, Release 동의 검증을 대신하지 않는다.
- ATT 요청 없음. NPA 요청 및 publisher first-party ID 비활성화. 자체 user events/ID/학습량/시간을 광고 요청에 전달하지 않는다. SDK 진단/광고 데이터 수집까지 없다고 주장하지 않는다.
- 앱 privacy manifest는 UserDefaults 및 uptime 목적을 선언한다. SDK manifest/실제 수집/대상 연령·지역/consent/ATT 필요성/App Store 개인정보 응답은 DEV14에서 실제 archive로 재확인해야 한다.

## StoreKit / Entitlement architecture

상품 ID **`remove_ads`**, StoreKit2 **Non-Consumable**. 일본 목표 가격은 App Store Connect에서¥800으로 설정한다. 앱은 `Product.displayPrice`를 사용한다.800은 로컬 `.storekit` 테스트 설정에만 있고 구매 UI에 가격 문자열을 하드코딩하지 않았다.

`PurchaseService`는 product lookup, purchase/cancel/pending/unverified, currentEntitlements, latest verified revocation, Transaction.updates, finish, explicit AppStore.sync restore를 담당한다. 앱 소유 단일 instance, start guard 및 단일 observer를 사용한다. verified 적합 product/type만 권한을 부여하고 처리 후 finish한다. unverified는 권한을 부여하거나 finish하지 않는다. pending/cancel은 기존 권한을 변경하지 않는다. 구매/복원 busy guard로 연타를 막는다.

상태는 checking/free/verified/offlineProtected/verificationFailed를 구분한다. **free만 광고 허용**한다. startup 확인은 Home을 block하지 않는다. generation으로 오래된 entitlement scan이 새 구매/update를 덮어쓰지 않도록 한다. 구매 확인 즉시 AdService의 preload를 폐기하고, 실제 표시 직전에도 다시 확인한다.

Keychain의 device-only cache에는 정상 확인한 product/transaction ID/구매일만 저장한다. 단순 UserDefaults hasPurchased boolean이 아니다. cache는 StoreKit 검증 자체와 다르며 UI도 이전 확인 보호 상태로 구분한다. StoreKit의 locally verified entitlement가 우선이며, 일시적으로 확인할 수 없으면 이전 구매자의 광고를 보수적으로 차단한다. verified revocation 또는 사용자가 명시적으로 성공한 sync 후 구매없음이면 보호 cache를 해제한다. Debug/Release cache namespace는 분리했다. 새 기기에서는 cache 대신 StoreKit/Restore로 확인한다.

`設定 → 広告を削除・購入を復元`에서 간단한 일본어 구매/복원 UI를 제공한다. 이미 구매했으면 구매 버튼을 감춘다. 가격 조회 실패/구매없음/복원 실패는 일본어 안내, cancel은 일반 흐름, 구매 중 다른 학습 콘텐츠를 잠그지 않는다. 개인계정/서버/구독/별도 유료앱/cloud sync 없음.

## StoreKit 테스트 준비

`Config/RemoveAds.storekit`과 선택형 `HangulStudy-StoreKit` scheme을 추가했다. 일반 scheme Run/Release archive에는 local StoreKit 설정을 사용하지 않는다. config 파일은 test bundle resource다. Native StoreKit test는 실제 test bundle URL로 구성하여 상품 조회→구매→새 service→entitlement refresh→restore를 검사하도록 작성했다. **실행하지 않았다.**

## Requirements Coverage Audit

`Docs/DEV13_REQUIREMENTS_AUDIT.md`에 과거 요구사항을 기반/한글/발음/어휘/회독/SRS/문법/활용/듣기/curriculum/search/통계/유지학습/설정/알림/수익화로 나누어 실제 근거와 부분 범위를 기록했다. 문서의 “완료”만으로 native 동작을 보증하지 않았다.

이전 Major인 Continue 모듈 우선순위를 수정했다. 최근 저장 활동 시각을 모듈 간 비교한다. Production snapshot에는 optional updatedAt을 추가해 과거 JSON 디코딩을 유지한다. 과거 production은 해당 content/session의 최근 study_event를 index로 조회한다. Listening의 기본 Codable Date epoch(2001)를 SQL의 Unix time으로 변환한다. 이미 완료한 session은 제외하고, membership/답변/점수/SRS는 수정하지 않는다.

## Integration Audit

- 실제 source→strict validation→production 관계/버전/쿼리, 기존 전체 Python/SQLite regression 실행.
- `Content/production.json`, `Resources/content.sqlite`는 DEV12 ZIP과 byte-for-byte 동일. content13/schema4/reader7/user10 유지. 새로운 data나 user migration 없음.
- 광고 서비스는 user/content DB에 접근하지 않음. 학습 commit 후 한 callsite, core paywall 없음, main launch SDK 초기화 없음, 구매/consent중 광고 차단을 검사했다.
- Resume 실제 SQL: 최근 모듈/완료제외/legacy JSON/epoch/cold reopen/기존 SRS 보존 검사. synthetic300k events/legacy20 active query 첫0.374ms, 이후0.017~0.031ms. iPhone 성능 수치 아님.
- 실제 audio, StoreKit, UMP, SDK 광고, OS interruption, 연타/Navigation 실행은 남아 있다. 상세 실기기 체크리스트를 별도로 남겼다.

## Micro-session / Commute UX Audit

기존 Home Continue/短く復習는 그대로. 짧은 복습량과 중간 저장을 광고가 바꾸지 않는다. 단어4개/복습5~7개/듣기2개/알림/Resume는 광고 진입점이 없다. 모든 meaningful action의 기존 transaction을 유지하며 전체 session 완료를 저장 조건으로 만들지 않았다. Offline에서도 core 학습·search·favorites·통계 사용 가능 구조 유지. 구매/광고 network가 실패해도 core를 차단하지 않는다. 실제 기내모드/전화/force-kill/최대글자/VoiceOver/배터리는 미검증이다.

## Bugs Found

- 기존 Major: 가장 최근 Listening/Production 대신 오래된 Vocabulary를 Continue로 고정 제시.
- 새 연결 감사: entitlement scan/load 완료 경쟁, 초기에 checking이면 preload 기회 유실, 중복 boundary/delegate callback 위험.
- 기존 테스트: test resource 목록이 fixture 한 개로 고정되어 StoreKit test resource 추가를 오류로 취급.

## Bugs Fixed

- 실제 최근활동 SQL 및 backward-compatible Production timestamp 추가, indexed legacy fallback.
- 새 구매가 stale refresh보다 우선, preload generation/구매 직전 재검증, 화면이탈/foreground/구매 busy 확인, free 갱신 후 학습 preload 기회 제공.
- boundary UUID/cap 선소비, presented object identity callback guard. 광고 callback에 저장/다음 화면 이동 없음.
- 패키징 테스트에 새 test resource를 반영. fixture/production 분리와 Validator는 약화하지 않았다.

## Known Remaining Issues / DEV-14

- **Critical release gate:** native build/type-check/SDK resolve/117 XCTest/StoreKit Sandbox·TestFlight/실제 Google test ad·동의/기기 UI·VoiceOver 미검증. 이 프로젝트를 App Store 출시 검증 완료로 간주하지 말 것.
- **Major 기존 범위:** 상급 curriculum/실제 개별 발음 녹음/심화 placement·혼합 Unit/전체 활용·자유작문 공백. 이미 배포한 content가 삭제되면 active session 자동 skip은 없음.
- **Minor legacy Resume:** 과거 production에 timestamp도 답변event도 없으면 최근활동 근거가 없어0/tie-break 사용. 다음 action부터 정상 timestamp 저장.
- **Minor 기존 UX:** 단어복습 전용 짧은량 preference, 모드별 유지학습, daily 일반 알림. 실제 OS/접근성 검증 필요.
- **운영 정책:** EEA 등 동의필요 지역에서 Settings form을 열지 않으면 광고 없음. cache 확인 불가 때 이전 구매자를 보호하므로 확인될 때까지 광고를 덜 표시할 수 있다.
- 실제 Production AdMob ID 미제공은 의도된 비활성 상태다. 소유자 ID·상품·가격·개인정보 설정 위치는 `RELEASE_CHECKLIST.md`에 명확히 기록했다.
- 새 TODO/FIXME/dummy/학습 잠금/빈동작 버튼은 추가하지 않았다. native로 확인하지 못한 항목을 정상 동작했다고 기록하지 않았다.

## Tests / Build

- Python/SQLite **211 PASS / 50.490초**: `Docs/TEST_RESULTS_DEV13.txt`.
- strict Validator **오류0 / 기존 경고10**: `Docs/VALIDATION_DEV13.json`.
- Swift **86파일 syntax 검사** 및 project/plist 검사는 `Docs/STATIC_CHECKS_DEV13.json`. tree-sitter는 type-check가 아니다.
- Native XCTest **117 작성 / 실행0** (기존104 + monetization policy12 + StoreKit1). Xcode build/SDK resolve **실행0**.
- Release configuration 검사: Production ID absent→disabled 정상. test ID 검출/필수모드 missing 거부 검사 포함.

## 주요 파일

신규: Models/MonetizationPolicy.swift, Services/PurchaseService.swift, Services/AdService.swift, Views/RemoveAdsView.swift, Config/{Debug,Release}.xcconfig, Config/RemoveAds.storekit, Resources/PrivacyInfo.xcprivacy, Tests/{MonetizationTests,StoreKitPurchaseTests}.swift, Tools/check_monetization.py, Tools/ContentBuilder/test_dev13_integration.py, RELEASE_CHECKLIST.md, Docs/DEV13_REQUIREMENTS_AUDIT.md.

수정: App/shared services, Settings 진입, Vocabulary 완료 경계, Production timestamp/SQLiteCurriculum Resume, Info.plist, project generator/StoreKit scheme/verify.sh, 패키징·Continue 테스트. 전체 변경 목록은 `Docs/CHANGES_DEV13.txt`.
