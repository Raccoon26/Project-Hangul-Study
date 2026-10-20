# DATA-09-7 / 요구사항·시스템 회귀 감사 — 현재 Production

**Content24 / Schema4 / reader7 / UserProgress10 유지.** 전체 portable **365/365 PASS**(415.721초, 실패·오류·skip0), DATA08 P1 전용10/10·새 문법 회귀6/6 PASS(전체와 중복). 실제 SQL로 전3,553문제/4,813예문 도달·누락0,96문법/93선행 edge 순환0·후행 참조12개는 선택적 설명 프리뷰로 지원한다. 새 런타임 P0/P1 재현0·수정0, Source/DB/ID/revision 변경0. 신규54문법/216고유예문/216문제·장기350~500 목표 유지.

19/23→24 strict 오류0/기존경고10·DB byte 재현·기존 Progress/SRS/session/통계 보존 회귀 PASS. **Xcode/Swift 없음: iOS Build·141정의 XCTest(기존139+이번2)/실행0·기기/음성/접근성/메모리/3~10분/StoreKit/AdMob BLOCKED**, 독립 사람·외부사전 NOT TESTED, 옛 원래 명세 전체 UNVERIFIABLE. native P1 확인 gate·선행 미해결36건·B—Conditional 유지. [상세 감사](Docs/DATA09_SYSTEM_REVIEW.md), [실행 결과](Docs/DATA09_SYSTEM_RESULTS.json), [누적 §13](DATA09_PROGRESS.md). 이번 DATA09-7에서 종료하며 다음 단계는 시작하지 않았다. 아래 수량·‘현재’·검사는 당시 이력이다.

---

# DATA-09-6 / Production·Curriculum 통합 — 현재 Production

**Content24 / Schema4 / reader7 / UserProgress10.** 검수된 신규54문법·216고유예문·216문제를 기존3코스/18레슨의6단원과 실제 학습 경로에 통합했다. 기존 ID·membership·순서·본문·정답을 유지하고 선행 복습20참조·35관련어휘로54관계를 보강, 누락되던 예문 Note를 표시한다. 새 UUID는 Unit tag6개, 기존107개 관계 endpoint revision만 각1 증가. 전체 Grammar96(入門22/初級20/初中級54), Example4,813, Question3,553, Vocabulary2,287. 장기Grammar/Expressions350~500 유지.

실제 직전23과 DATA09 전19 원본/DB를 각각 보존하고19→24/23→24 strict **0errors/기존10warnings**, Production 재구성 DB byte 일치. 최종 portable **359/359 PASS**(420.142초, 실패/오류/skip0), 전용13/13·조회 회귀4/4 PASS. Source25테이블66,094행·FK0/integrity ok, SQL/디스크에서 기존 Progress/Favorites/SRS/snapshot/통계 보존 확인. **Xcode/Swift/iOS/139 XCTest 실행0·실기기 접근성/메모리/3~10분·음성/Resume BLOCKED, 사람/외부 사전 검수 NOT TESTED, B—Conditional 유지**. 미해결 선행36건과 기존 native P1 gate는 완료로 바꾸지 않는다. [통합 보고](Docs/DATA09_INTEGRATION.md), [실제 결과](Docs/DATA09_INTEGRATION_RESULTS.json), [누적 기록 §12](DATA09_PROGRESS.md). DATA09-6에서 종료하며 다음 단계는 시작하지 않았다. 아래 수량/검사는 당시 이력이다.

---

# DATA-09-5 / 최종 품질 감사 — 현재 Production

**Content23 / Schema4 / reader7 / UserProgress10.** A~C 신규54문법·216고유예문·216문제 전수 AI 자체 검수, 고위험18개 문법·무작위45개 별도 재감사 후 **25개 ID/31필드** 교정. 수량·기존 ID·정답 ID·학습 배치·Progress/SRS 정책 유지. 선행 후보163건은 **해결120 / 조건부 교육 허용7 / 미해결36**이며 원래 Level 검토8건은 모두 미해결이다. 전체 Grammar96(入門22/初級20/初中級54), Example4,813, Question3,553(Grammar300), Vocabulary2,287.

최종 portable **346/346 PASS**(380.927초, 실패/오류/skip0, exit0), 전용11/11 PASS. strict0errors/기존10warnings·FK0/integrity ok·Source25테이블65,983행 및 Importer 재구성 DB byte 일치. **독립 원어민·교사/외부 사전 검수 NOT TESTED, Swift/Xcode/iOS/XCTest137정의·실행0 BLOCKED, B—Conditional 유지**. AI 검수·자동 검사와 사람 승인/출시 완료를 구분한다. 신규 목표54/216/216 및 장기Grammar/Expressions350~500 유지. [상세 감사](Docs/DATA09_FINAL_REVIEW.md), [실제 결과](Docs/DATA09_FINAL_RESULTS.json), [누적 기록 §11](DATA09_PROGRESS.md). DATA09-5에서 종료하며 다음 단계는 시작하지 않았다. 아래 ‘현재’·수량·PASS는 각 단계 당시 이력이다.

---

# DATA-09-4 / Batch C — 현재 Production

**Content22 / Schema4 / minReader7 / UserProgress10.** C 신규 初中級 Grammar18개·고유 신규 Example72개·Grammar Question72개를 한일 Self Review/중복·ID/strict 검증 후 반영했다. A/B/C 누적 **신규54문법·216고유예문·216문법문제**로 전체 목표45~60 /180~300 /180~300 충족. A/B의 기존 예문4개 재사용은 신규 수량에서 제외했다. 전체 Grammar96(入門22/初級20/初中級54), Example4,813(문장4,800+발음13), Question3,553(그중 Grammar300), Vocabulary2,287. 새 코스1·레슨6(59~64), 기존 본문·ID·배치 보존·기존 관계 끝점12개만 revision+1.

재개 후 portable **335/335 PASS**(641.737초, 실패/오류/skip0,exit0), 전용12/12 PASS. strict0errors/기존10warnings, Source25테이블65,983행 일치·integrity ok/FK0·Importer 재구성 DB byte/SHA 일치. 독립 사람·외부 사전 검수 NOT TESTED, Swift/Xcode/iOS build·XCTest137정의/실행0 BLOCKED, **B—Conditional 유지**. 수량 목표와 출시 검증 완료를 구분하고 장기Grammar/Expressions350~500을 유지한다. [DATA09_PROGRESS §10](DATA09_PROGRESS.md), [검수 범위](Docs/DATA09_C_REVIEW.md), [실제 수량](Docs/DATA09_C_COUNTS.json). 마지막 Batch C에서 종료하며 다음 단계/DATA10은 시작하지 않았다. 아래 A/B·DATA08의 ‘현재’·수량·검사는 당시 이력이다.

---

# DATA-09-3 / Batch B — 현재 Production

**Content21 / Schema4 / minReader7 / UserProgress10.** 신규 初中級 문법18개·고유 신규 예문72개·단일 선택 문제72개를 한일 Self Review/중복·ID/strict 검증 후 반영했다. DATA08 예문4개는 기존 ID로 재사용하여 신규 수량에서 제외했다. 전체 Grammar78(入門22/初級20/初中級36), Example4,741(문장4,728+발음13), Question3,481, Vocabulary2,287. 새 Grammar 코스1·레슨6(53~58), 기존 본문·ID·배치 보존·관계 끝점22개만 revision+1. Content20 Source/DB 불변 fixture 보존, strict0errors/기존10warnings·Source25테이블65,043행 일치·integrity ok/FK0.

이번 portable **323/323 PASS**(393.788초, 실패/오류/skip0, exit0). DATA09 누적 신규36문법/144고유예문/144문제, 전체 신규45~60 및 장기Grammar/Expressions350~500 목표 유지. 독립 사람·외부 사전 검수 NOT TESTED, Xcode/Swift/iOS build·XCTest137정의/실행0 BLOCKED, **B—Conditional 유지**. [DATA09_PROGRESS §9](DATA09_PROGRESS.md), [한일 검수 범위](Docs/DATA09_B_REVIEW.md), [실제 수량](Docs/DATA09_B_COUNTS.json). Batch B에서 종료하며 다음 단계는 시작하지 않았다. 아래 DATA09-2 이전의 ‘현재’·수량·검사 결과는 당시 이력이다.

---

# DATA-09-2 / Batch A — 현재 Production

**Content20 / Schema4 / minReader7 / UserProgress10.** 신규 初中級 문법18개·고유 예문72개·단일 선택 문제72개를 assistant 한일 Self Review/중복·Stable ID/strict 검증 후 반영했다. 전체 Grammar60(入門22/初級20/初中級18), Example4,669(문장4,656+발음13), Question3,409, Vocabulary2,287. 새 Grammar 코스1·레슨6(47~52), 기존 본문/ID/순서 보존·관계 끝점12개만 revision+1. 기존19 source/DB fixture 보존, strict0errors/기존10warnings·Source25테이블64,099행 일치·integrity ok/FK0.

이번 portable **311/311 PASS**(328.544초, failures/errors/skipped0, exit0). 독립 사람 언어 검수·외부 사전 대조 NOT TESTED, Swift/Xcode/iOS 빌드·XCTest137개/실기기 실행0(BLOCKED), **B—Conditional 유지**. 장기Grammar/Expressions350~500개 및 DATA09 신규45~60개 목표 유지. 이번은 Batch A에서 종료한다. [DATA09_PROGRESS §8](DATA09_PROGRESS.md), [검수·한계](Docs/DATA09_A_REVIEW.md), [실제 수량](Docs/DATA09_A_COUNTS.json). 아래 DATA09-1/DATA08 및 DEV/DATA 내용의 ‘현재’는 당시 이력이다.

---

# DATA-08-8 최종 확인 — Content19 / Schema4 / reader7 / UserProgress10

**수량·Source/DB 통합 목표 달성, 전체 완료 판정은 B—Conditional 유지. DATA-09 미착수.** 신규 Vocabulary **911개(일반 어휘807 + 표현104)** / 고유 신규 문장 Example **1,821개**. 일반 어휘만 세어도 목표800~1,200 범위에 들며, 예문 목표1,300~2,000도 충족한다. 기존 예문1개 재사용은 신규 수에 포함하지 않았다.

Production: Vocabulary **2,287**, Meaning **2,420**, Example **4,597(문장4,584 + 발음13)**, Grammar **42**, Listening **1,936**, Question **3,337**, Course **5**, Lesson **85**. Content19와 모든 기존 ID·원본·DB byte 유지. Importer 재구성 DB는 번들과 SHA-256까지 동일, strict **0 errors / 기존10 warnings**, FK0 / integrity ok, 종료 점검133건 PASS. 이번 portable **301/301 PASS**(270.967초, 실패/오류/skip0, exit0). iOS build/XCTest137개는 **BLOCKED**, 독립 사람 언어 검수는 **NOT TESTED**다.

현재 결과와 미완료 조건은 [DATA08_CLOSEOUT](Docs/DATA08_CLOSEOUT.md), 실제 수량·해시는 [CLOSEOUT.json](Docs/DATA08_CLOSEOUT.json), 단계별 기록은 [DATA08_PROGRESS](DATA08_PROGRESS.md) §16을 따른다. **아래 DATA-08-1~7 및 DEV/DATA 섹션의 ‘현재’·완료 표현·테스트 수는 각 단계 당시 이력이며 최신 상태로 합산하거나 대체하지 않는다.**

---

**DATA-08-7 감사: Content19 / Schema4 / reader7 / UserProgress10 유지, Source/DB 변경0.** P1 세 건(비활성 복습 복구·받아쓰기 문장부호·듣기 due 퇴역 prefix) 코드 수정. 전체 Python/SQL **301 PASS**, native137개/실행0·iOS Build **BLOCKED**. 원래 DEV01~14/DATA01~07 작업 명세 원문은 찾지 못해 전체 원문 준수는 확인 불가. 기존 목표911어휘/1,821예문 유지, B—Conditional. [감사·부분 구현·상태표](Docs/DATA08_SYSTEM_REVIEW.md), [DATA08_PROGRESS.md](DATA08_PROGRESS.md) §15. 아래는 단계별 이력이다.

---

**DATA-08-6: Content19 / Schema4 / minReader7 / UserProgress10.** 911어휘/1,821신규예문 목표 유지. 실제 Course1·Unit tag3·Lesson47에911어휘 배치, 듣기/받아쓰기1,821·활용/문장입력1,162문항 연결. Production Vocabulary2,287 / Example4,597 / Grammar42 / Listening1,936 / Question3,337. strict0errors/기존10warnings·integrity ok/FK0·전63,159행 Source/DB 일치. portable **291 PASS**(289.839초, failures/errors/skipped0, exit0), 전용11 PASS. 사용자 기록/active snapshot/5·10·20 복습 SQL 보존. native 정의132/실행0, 실제 iPhone/offline/TTS/3~10분과 사람 검수 미실행. B—Conditional 유지. 상세 [통합 기록](Docs/DATA08_INTEGRATION.md), [DATA08_PROGRESS.md](DATA08_PROGRESS.md) §14. 아래는 단계별 이력이다.

---

> **DATA-08-5 현재: Content18/schema4/reader7/UserProgress10.** assistant 전911어휘·1,821고유문장 재독·별도 무작위84개 감사,34어휘43필드 교정. portable **280 PASS**(failures/errors/skipped0, exit0). **사람·독립 원어민/교사 검수는 미실행**이며 자동 검사는 언어 품질 보증이 아닙니다. 문형 후보163예문의 선행 학습과 Level/Register의 독립 적합성 확인을 남깁니다. native 정의130개/실행0; Mac에서 전체130개와 새22불규칙+7규칙 혼동어의 현재/조건/미래 기대형,17→18 수정 어휘의 부분 session/SRS/즐겨찾기 보존을 검증해야 합니다. Xcode/SDK/Debug·Release·iPhone3~10분/offline/TTS/중단/VoiceOver/광고·StoreKit/알림 gate와 **B—Conditional**을 유지합니다. 아래 과거 gate/체크박스를 보존합니다. 상세 `DATA08_PROGRESS.md` §13.

---

> **DATA-08-4 / Batch C 현재: Content17/schema4/reader7/UserProgress10.** 신규310어휘/619문장·기존 예문1 재사용, 전체 DATA-08 911어휘/1,821신규문장 목표 달성. portable **269 PASS (failures/errors/skipped0, exit0)**. native 정의129개/실행0. Xcode/SDK link/Debug·Release/XCTest·iPhone QA 미실행, **B—Conditional 유지**. 아래 기존 gate/체크박스를 보존한다. Mac에서129개 전체와 삼가요·달가워요·미더워요·껄끄러워요·어설퍼요·가라앉아요·가라앉혀요·비춰요·비쳐요·가꿔요·들떠요, Content16→17의 A/B 사용자 기록 보존을 실행해야 한다. 실제3~10분·offline/TTS·중단·접근성·광고/StoreKit 검증은 별도다. 상세 `DATA08_PROGRESS.md` §12.

---

> **DATA-08-3 / Batch B 현재: Content16/schema4/reader7, UserProgress10.** 初中級300어휘/600문장 추가, 최종 portable **255개 PASS (failures/errors/skip0, exit0)**. native 정의128개/실행0. Xcode/SDK link/Debug·Release build/iPhone QA 미실행, B Conditional 유지. 아래 과거 체크박스와 gate는 보존한다. Mac에서 기존 전체128개와 새 글러요·걸러요·별달라요·색달라요·모자라요·넘쳐요·까다로워요·해로워요·이로워요·순조로워요, Content15→16 시 Batch A 포함 기존 사용자 기록 보존을 실제 검증해야 한다. 상세 `DATA08_PROGRESS.md` §11.

> **DATA-08-2 / Batch A 업데이트 (2026-10-19): 현재 Content15/schema4/reader7, UserProgress10.** 初中級301어휘/602문장 추가. portable243 tests PASS. native 테스트 정의127개이며 이번 native 실행/Debug·Release build/SDK link/실기기 검증은0입니다. 아래 과거123개 표기와 체크박스는 이력/미완료 gate로 보존합니다. Mac에서는 현재127개 전체와 DATA-08의 들러요·서툴러요·어질러요·너그러워요·맞춰요·맞혀요, Content14→15의 기존기록 보존을 실제로 실행해야 합니다. 현재도 B Conditional이며 제출 승인 아님.

> **DATA-07更新 / 2026-10-06:** Current bundle=Content14/schema4/reader7、UserProgress10。Portable232 tests PASS、Swift89ファイル構文確認のみ。Xcode build・XCTest・iPhone検証は未実施。DEV14のConditional判定と以下release gateは継続。新規初中級・追加直接入力/聴解・Content13からの保存状態をMacで必ず再検証してください。

# DEV-14 / App Store 출시 준비

2026-10-05. 이 문서는 소유자가 해야 하는 설정과 Mac/iPhone 검증을 구분한다. 현재 Production AdMob ID가 없는 것은 개발 오류가 아니다. 비어 있는 Release는 광고를 요청하지 않으며 학습 기능은 그대로 동작한다. 아래의 실제 결제/광고/기기 검증은 Linux 작업 환경에서 실행하지 않았다.

## 1. 프로젝트 열기

1. Mac에 Xcode 16 이상과 사용할 iOS Simulator를 설치한다. StoreKit 자동 테스트는 iOS 17 이상 대상으로 실행한다.
2. `HangulStudy.xcodeproj`를 연다. Package Dependencies에서 공식 GoogleMobileAds **13.11.0**, GoogleUserMessagingPlatform **3.1.0**을 다운로드/해결한다. 버전은 `Tools/generate_project.py`에 고정되어 있다. 실제 SDK resolve/build는 아직 미실행이다.
3. Signing & Capabilities에서 본인의 Apple Developer Team과 이 앱에 사용할 Bundle ID를 설정한다. 현재 `com.example.HangulStudy`는 개발용 식별자다. 단일 앱으로 운영하며 별도 유료 앱을 만들지 않는다. 재생성 시 사라지지 않도록 generator의 bundle 설정도 함께 바꾼다.
4. In-App Purchase capability, 앱 아이콘, 일본어 앱 설명/지원 URL/개인정보처리방침 URL/스크린샷을 출시용으로 준비한다. 개인정보/결제계정/은행정보를 소스나 ZIP에 넣지 않는다.

## 2. AdMob 실제 값 입력

1. 소유자가 직접 Google AdMob에 가입하고 이 iOS 앱을 등록한다. 등록한 앱의 **앱 ID**와 **전면 광고 단위 ID**를 확인한다.
2. `Config/Release.xcconfig` 파일의 아래 두 값만 채운다. App ID는 가운데 `~`, 광고 단위 ID는 `/`가 들어간다. 서로 다른 값을 뒤바꾸지 않는다.

| 파일 / 키 | 입력할 값 | 연결되는 앱 설정 |
| --- | --- | --- |
| Config/Release.xcconfig / ADMOB_APP_ID | 본인 AdMob 앱 ID | Resources/Info.plist / GADApplicationIdentifier |
| Config/Release.xcconfig / ADMOB_INTERSTITIAL_ID | 본인 Interstitial 광고 단위 ID | Resources/Info.plist / AdMobInterstitialIdentifier |
| Config/Debug.xcconfig | **변경하지 않음: Google 공식 테스트 값** | Debug 전용 |

3. `Config/Debug.xcconfig`의 Google demo 값을 Release로 복사하지 않는다. Swift View나 Service에 ID를 추가하지 않는다. Runtime도 Release의 테스트 publisher, 빈 값, 형식 오류, 다른 publisher 조합을 거부한다.
4. 프로젝트 폴더에서 `python3 Tools/check_monetization.py --require-ads`를 실행한다. Production 값을 입력하지 않은 개발 단계에서는 `--require-ads` 없이 실행하면 비활성 상태가 정상으로 표시된다.
5. Archive 후 **실제로 빌드된** `.app/Info.plist`에도 검사한다:

```sh
python3 Tools/check_monetization.py --built-info /실제/경로/HangulStudy.app/Info.plist --require-ads
```

6. 이 검사는 ID의 형식/환경을 검사하며 계정 소유권·광고 단위 활성 상태까지 증명하지 않는다. AdMob 관리 화면에서 소유권과 iOS 앱 연결을 직접 확인한다.
7. 현재 광고 형식은 Interstitial 한 종류다. Banner/App-open/Rewarded/학습 콘텐츠 잠금은 없다.

## 3. Consent / Privacy

- Production 광고를 활성화하기 전에 AdMob의 Privacy & messaging에서 대상 지역에 필요한 메시지를 설정·게시한다. UMP의 새 상태 확인 및 `canRequestAds`가 허용하지 않으면 앱은 광고를 표시하지 않는다.
- 동의 화면은 첫 실행에 자동으로 띄우지 않는다. `設定 → 広告を削除・購入を復元 → プライバシー設定を確認・変更`에서 사용자가 열 수 있다. 동의가 필요한 사용자가 이 설정을 열지 않으면 광고 없이 학습할 수 있다. 허용 지역/거절/철회/네트워크 오류를 실제 기기에서 각각 확인한다.
- **Debug 공식 테스트 광고만** UMP 동의 게이트를 사용하지 않는다. Google demo App ID에는 소유자 계정의 게시된 메시지가 없기 때문이다. 테스트 광고 표시는 consent 검증이 아니다. Release는 이 분기를 사용하지 않는다.
- 앱은 ATT 요청을 호출하지 않는다. `npa=1` 비개인화 요청, publisher first-party ID 비활성화를 사용한다. 그렇다고 Google SDK가 수집하는 진단/광고 데이터까지 없다는 뜻은 아니다. 앱 전체를 “수집 없음”으로 신고하지 않는다.
- `Resources/PrivacyInfo.xcprivacy`는 앱 자체의 UserDefaults(CA92.1), 이벤트 사이 경과시간 계산용 system uptime(35F9.1)을 선언한다. 학습정보/경과시간을 광고 요청에 넣지 않는다. SDK 자체 manifest를 포함한 Xcode privacy report를 생성하고 **실제 SDK 13.11.0** 수집 내용과 App Store Connect 개인정보 응답을 대조한다.
- 현재 Info.plist는 공식 quick-start에서 확인한 SKAdNetwork ID 50개를 포함한다. 출시 직전에 공식 목록과 재대조한다. Mediation/Analytics SDK는 추가하지 않았다.
- 실제 대상 연령·배포 지역·광고 설정에 필요한 처리와 동의 문구를 확인한다. IDFA 메시지나 추적을 나중에 활성화한다면 ATT/설명문/manifest/개인정보 신고를 함께 재검토한다. 현재 설정에 추적 권한이 있다는 가정으로 변경하지 않는다.

## 4. App Store Connect: 일회성 광고 제거

1. 본인 App Store Connect의 해당 앱에서 In-App Purchases를 열고 **Non-Consumable(비소모성)** 상품을 만든다. 구독/Consumable 상품을 선택하지 않는다.
2. Product ID를 정확하게 **`remove_ads`**로 입력한다. 이 ID는 `Models/MonetizationPolicy.swift`의 `MonetizationConfiguration.productID`와 같다. 배포 후 임의로 바꾸지 않는다.
3. 일본 판매 가격의 목표를 **¥800**으로 설정하고 Japan storefront에서 확인한다. `Config/RemoveAds.storekit`의 800은 로컬 테스트 가격일 뿐 App Store Connect 가격을 설정하지 않는다.
4. 일본어 상품명 `広告を削除`, 설명에 `買い切り / 一度きりの購入 / すべての広告を削除`를 명확히 쓴다. 교육 콘텐츠 추가 해제/영구 암기/구독 혜택을 광고하지 않는다. 모든 핵심 학습 기능은 무료다.
5. 판매 지역, 필요한 현지화, 심사용 스크린샷·설명, 상품 심사 상태를 확인한다. 소유자가 Apple의 계약/정산 절차를 직접 완료한다. 이 프로젝트에는 계정 비밀번호나 정산정보를 넣지 않는다.
6. 앱은 `Product.displayPrice`만 표시한다. 다른 storefront에서 실제 현지 가격을 표시하는지 확인한다.
7. 최초 IAP 제출에 필요한 앱 버전 연결·심사 정보를 App Store Connect에서 확인한다. Sandbox 및 TestFlight로 상품 조회/구매/복원을 검증한 뒤 실제 출시한다.

## 5. 실제 결제 없는 테스트

- Xcode에서 **HangulStudy-StoreKit** scheme을 선택하면 `Config/RemoveAds.storekit`으로 로컬 구매를 시뮬레이션한다. 일반 **HangulStudy** scheme의 Run에는 로컬 StoreKit 설정이 없다. Release archive에 `.storekit` 파일을 리소스로 넣지 않는다(test bundle 전용).
- Debug/Release entitlement cache의 Keychain namespace는 분리되어 있다. Debug 테스트 구매가 Release의 구매 상태로 이동하지 않는다. 로컬 테스트를 초기화할 때는 Xcode StoreKit Transaction Manager에서 거래 삭제/환불을 사용한다.
- `Tests/StoreKitPurchaseTests.swift`는 test bundle URL의 local configuration을 사용해 상품 조회→구매→새 서비스 인스턴스→entitlement refresh→복원을 검사한다. **작성했지만 미실행**이다. Simulator에서 StoreKit 테스트가 오류를 내면 무시하거나 production 결제로 우회하지 말고 설정/OS 테스트 환경을 먼저 확인한다.
- 정책 XCTest는 무료/구매/검증 중/오프라인 보호/미검증, pending/cancel, 환불, 긴 학습, 12분 미만, 20개 미만, 재개, 60개 누적, 30분 cap, 시계역행, 중복 완료, 저장 복원을 다룬다.

프로젝트 폴더에서:

```sh
xcodebuild -resolvePackageDependencies -project HangulStudy.xcodeproj -scheme HangulStudy
TEST_DESTINATION='platform=iOS Simulator,name=실제로 설치된 Simulator 이름' sh Tools/verify.sh
```

`verify.sh`는 Python/SQLite, Debug/Release build를 실행하고 TEST_DESTINATION을 지정하면 XCTest도 실행한다. 아직 실행하지 않은 native 검사 대신 Python 성공 결과를 제시하지 않는다.

## 6. 수익화 기기 QA (모두 확인 후 출시)

| 상황 | 기대 결과 |
| --- | --- |
| 신규 무료 사용자/앱 시작/알림에서 시작/Continue | 시작 광고 없음, Home/학습 사용 가능 |
| 단어4개/짧은 review/listening2개/3~10분 학습 | Interstitial 없음 |
| 오래 시작했던 session 재개/중간 background | 해당 화면 체류에서는 Interstitial 제외 |
| 새 단어 세트20개 이상, 연속 foreground12분 이상, 누적 완료60개, 마지막 광고30분 이상 | 완료 저장 후 준비된 광고만 후보. 항상 표시되는 것은 아님 |
| 광고 로드 실패/없음/오프라인/Production ID 없음 | 완료·다음 이동·SRS·Resume 정상, 대기 화면 없음 |
| 정상 구매/중복 tap | 한 purchase flow, verified 후 즉시 광고 차단/준비된 광고 폐기 |
| 취소/pending/unverified | entitlement 부여 안 함, 취소는 오류 alert 없음 |
| 환불/취소된 거래 | verified revocation 시 광고 제거 권한 해제 |
| 구매 뒤 kill/relaunch/오프라인 | StoreKit 로컬 검증 또는 이전 verified cache 보호로 광고 없음 |
| 재설치/새 기기 | 같은 Apple Account의 `購入を復元`으로 확인(학습 cloud sync와 별개) |
| Restore 구매 없음/실패 | 일본어 안내, 무한 spinner/crash 없음 |
| 광고 직전 background/닫기/구매/연타 | 늦은 load가 자동 표시되지 않고 duplicate presentation/저장 없음 |
| 광고 표시 중 interruption/중복 delegate callback | 이미 저장된 진도 유지, 과거 callback으로 새 광고 상태 변경 없음 |
| 광고 종료 | TTS 자동 재시작 없음, 광고 시간을 통계 학습시간에 추가하지 않음 |
| 큰 Dynamic Type/VoiceOver | 상품·가격·일회성·복원 명확, 학습 정답 유출 없음 |

로컬 정책 검증을 위해 release 광고 제한을 낮추지 않는다. 테스트에서 시간을 조절할 필요가 있으면 XCTest의 주입된 `AdBoundary`/Date 값으로 검사한다. 실제 UI 광고 QA는 원래 제한을 충족하는 학습으로 확인한다.

## 7. 이전 기능과 출시 차단 항목

`Docs/DEV14_REQUIREMENTS_AUDIT.md`와 `PROJECT_STATUS.md`의 미완료 항목을 확인한다. 실제 Xcode 빌드/123 XCTest/기기 UI·음성·알림·광고·구매는 아직 미검증이다. 상급 production curriculum, 검증된 개별 발음 녹음, 고급 placement/전체 활용/자유작문은 현재 범위에서 완성되지 않았다. 광고/IAP를 넣었다는 이유로 전체 앱을 출시 검증 완료로 취급하지 않는다.

## 공식 참고 (2026-10-05 확인)

- [Google iOS SDK 설정](https://developers.google.com/admob/ios/quick-start)
- [Interstitial 구현/테스트](https://developers.google.com/admob/ios/interstitial)
- [UMP 동의/개인정보 선택](https://developers.google.com/admob/ios/privacy)
- [Google 개인정보 전략](https://developers.google.com/admob/ios/privacy/strategies)
- [SDK App Store 데이터 신고](https://developers.google.com/admob/ios/privacy/data-disclosure)
- [Google 공식 SPM](https://github.com/googleads/swift-package-manager-google-mobile-ads)
- [Apple Non-Consumable 생성](https://developer.apple.com/help/app-store-connect/manage-in-app-purchases/create-consumable-or-non-consumable-in-app-purchases)
- [Apple currentEntitlements](https://developer.apple.com/documentation/storekit/transaction/currententitlements)
- [Apple StoreKit 테스트](https://developer.apple.com/documentation/storekittest/sktestsession)


## DEV-14 최종 gate / 실행 순서

현재 판정 B Conditional이며 제출 승인 아님. 체크박스는 실제 실행자가 결과/기기/OS/날짜를 적은 뒤 완료 표시한다.

- [ ] 프로젝트 루트에서 `sh Tools/verify.sh --portable`: Python/SQLite 검사만. 이것만 성공했다고 iOS 빌드 완료로 처리하지 않음.
- [ ] Mac에서 `xcodebuild -showdestinations -project HangulStudy.xcodeproj -scheme HangulStudy`로 설치된 iOS17+ Simulator 선택.
- [ ] `TEST_DESTINATION='platform=iOS Simulator,id=실제시뮬레이터UUID' sh Tools/verify.sh` 실행. Debug/Release Simulator, Release device unsigned build 및123 XCTest 결과 보관. 실제 UUID로 교체.
- [ ] Xcode Signing 설정 후 Product > Archive, Organizer > Validate App. 실제 SDK 개인정보 manifest 및 Release Info.plist 확인.
- [ ] App Icon, 고유 Bundle ID, Team, version/build, 일본어 설명/스크린샷/지원·개인정보 URL, 연령등급, 수출규정/광고 데이터 응답 완성.
- [ ] TestFlight 설치에서 신규/기존사용자 DB upgrade, StoreKit sandbox 구매·취소·pending·복원·환불·offline paid 확인. 로컬 StoreKit Configuration 성공과 실제 ASC 상품 확인을 구분.

### 실기기 회귀 표 (모두 아직 미실행)

| 경로 | 확인할 결과 |
| --- | --- |
| 신규→진단/skip→한글→발음 | 뒤로가기/완료/재개, 자모 TTS 없음, fallback 정상 |
| 어휘4/20→kill→Continue | 4개 저장, 나머지미완료, 공개전판정금지, 광고없음 |
| 회독20→8→3→0→SRS | membership유지/중복등록없음/완료한번 |
| 복습5개→background→재개→날짜변경 | 제출중복없음/due보존/시간대변경과DST |
| Grammar→quiz→회독→복습→Continue | 최근위치, 형태/예문/비교, 정오답/SRS |
| 직접입력→오답→닫기→retry | snapshot재개/정답정규화/띄어쓰기/최초정확도 |
| 듣기→normal/slow/stop→오답→retry | 음성겹침없음/종료시정지/score중복없음/무한반복없음 |
| VoiceOver 듣기/Dictation | 답 공개 전 transcript 접근 불가 |
| 검색→상세→favorite→홈→Continue | 학습상태변경없음/중복push없음 |
| 유지학습/통계/설정/알림거부 | 실제기록/빈상태/설정재실행유지/학습차단없음 |
| 비행기모드→어휘/문법/검색 | 로컬학습정상, audio불가안내, progress보존 |
| 최대DynamicType/작은기기/Dark/ReduceMotion | 버튼겹침/잘림없음,44pt,색상만의상태없음 |
| TestFlight구매→즉시닫기→오프라인재실행 | 광고차단/observer중복없음/복원정상 |
| 개인정보설정열기→즉시닫기/background | 지연된form이학습화면위에나오지않음 |

하나라도 데이터손실/crash/구매권한오류 발생 시 제출 중단. 재현 절차, 로그(개인정보 제거), 수정, 재검증 결과를 PROJECT_STATUS에 기록한다. Production AdMob 값을 안 넣고 광고 없는 Release를 유지하는 것은 허용된 설정이며 임의의 ID로 채우지 않는다.


## DATA-08-8 최종 release gate (아래 미체크 항목은 실제 실행 전 완료 표시 금지)

- [x] 원본/ID/기존 fixture 보존, Content19 byte-exact 재구성, strict 오류0/기존경고10, FK0/integrity ok, 전수 경로/수량 검증.
- [ ] Mac의 Xcode/Swift/공식 SDK resolve, Debug/Release Simulator 및 device-architecture build.
- [ ] 현재137 native XCTest 전체 실행(기존 Content swap·설정/진도 보존·불규칙·P1 세 건 포함).
- [ ] iPhone3~10분/한 손/큰 글씨/VoiceOver/즉시저장·중단·이어하기/강제 종료·통화/비행기 모드·TTS·메모리 검증.
- [ ] 실제 StoreKit 구매/복원/취소/철회/오프라인 권한과 Content Version 독립성, AdMob/동의/실제 Keychain 검증.
- [ ] 독립 사람의 한국어/일본어 검수·Level/Register 및163선행Grammar 후보 확인.

현재 B—Conditional이며 App Store 제출 승인·DATA08 완전 검수 완료가 아니다. 원래DEV/DATA명세 미확보 사항은 UNVERIFIABLE로 유지한다. DATA09 미착수. 최종 portable 실행 결과/명령은 [CLOSEOUT](Docs/DATA08_CLOSEOUT.md)을 따른다.


## DATA-09-A 추가 release gate

- [x] strict19→20/기존 ID·본문·순서·snapshot 보존 SQL,18신규문형/72예문/72문제,전체311portable 검사.
- [ ] Mac의 실제 Debug/Release/SDK·XCTest137개 및 새18카드/6레슨·SRS/Content19 active session의 native 확인.
- [ ] iPhone 입력·큰 글씨/VoiceOver·TTS·중단/이어하기·비행기 모드·3~10분/메모리·광고/StoreKit 실제 확인.
- [ ] 독립 사람의 한일 품질·Level/선행문형 및 외부사전 활용 확인.163후보의 새 관계/난도 전수 해결은 미완료.

B—Conditional 유지. Batch A snapshot 승인을 App Store 출시 승인으로 해석하지 않는다.
