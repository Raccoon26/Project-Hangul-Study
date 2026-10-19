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
