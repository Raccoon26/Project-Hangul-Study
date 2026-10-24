# DATA-10-7 Mac Native Full Regression

2026-10-24 JST 재개. 상태: **진행 중, NativeSmallAwake80 전체169·PhysicalReleaseFull81 순차 검증 중 / Draft PR24 / main 미병합**. 이 문서는 실행 근거와 남은 gate를 구분하며 DATA10-8/11을 시작하지 않는다.

## 환경·보존

- 기존 Mac clone, `codex/data10-7-native-regression`, 시작 main/origin/main `59d3bc7636c2b22ce7a0e21899fa1deeb2bbfedb` (PR #23). 시작 미커밋 변경0. 재개 시 변경은 이 단계에서 작성한 코드·검사뿐이며 삭제/stash/reset/force push0.
- origin `https://github.com/Raccoon26/Project-Hangul-Study.git`, Raccoon26 인증/ADMIN/default main. rulesets0/Actions workflows0. CI 없음과 CI PASS는 다르다.
- macOS27 arm64 / Xcode27.1(27A9275), iOS26.0.1 Simulator. 단일 Xcode build jobs, UI 실행은 한 Simulator씩 순차 실행한다. 앱 iOS16 deployment 유지, XCTest target만 iOS17(현재 XCTest SDK 요구)에 맞춘다.
- Content29/Schema4/reader7/UserProgress10 및 모든 Production/fixture 114개 파일의 SHA-256 보존. Source/DB/Stable ID/revision/learning_order/기존 membership 변경0. 새 optional session JSON 필드는 과거 snapshot을 그대로 decode하며 UserProgress schema/migration/사용자 DB를 재작성하지 않는다.
- 시스템 Python3.11.6/SQLite3.44.0 ENABLE_STAT4와 exact writer SQLite3.53.1을 구분한다. `setup_exact_writer.py`로 만든 외부 `/tmp` writer에서 임시 Content29 rebuild, frozen28 strict Validator 오류0/기존 경고10, 번들 전체 byte/SHA 일치. SHA `228d5572391d4c56509f83c57415c9b76b69c82ce2e7e48ebea82af97630b4af`.

## 발견 → 수정 → 검증

| 문제 | 원인·수정 | 회귀 근거 |
| --- | --- | --- |
| P0 Release 시작 crash | 빈 광고 ID에도 SDK load-time 초기화가 먼저 실행. IDs 없는 Release에서 compiler flag+두 SDK link 제외를 함께 적용하고 설정/built executable 검사를 추가 | 같은 iPhone Release UI43/45 및 Release Simulator 시작 UI68 PASS. 실제 Production ID/거래를 생성하지 않음 |
| P1 되다/뵈다 생성 오류 | Hangul medial index ㅚ→ㅚ 및 ㅙ→ㅚ 오매핑을 ㅚ→ㅙ/ㅙ 유지로 교정. 꿰다의 ㅞ는 그대로 보존 | 기존 ReleaseAudit + 새 NativeRegression의 85개 published -되다 ×3 Dictionary/engine 및 전체1,227 입력 rubric 조회 |
| P2 ㅎ형 사전 현재/과거 누락 | published 어떻다/빨갛다/파랗다/노랗다 네 lexical base만 검수하여 지원. authored override 우선, 미검수 ㅎ형은 기존 안전 오류 유지 | 네 항목 현재/과거/미래 실제 Dictionary 조회 및 unknown/override 검사 |
| P1 구매 cache 실패를 미구매로 취급 | Keychain missing과 OSStatus/decode failure 분리. 오류 시 광고 fail closed, verified StoreKit 권한 유지, 저장 실패 메시지 | 실제 signed Keychain CRUD/cold read/delete + 로컬 StoreKit 구매/복원 + 실패 주입. unsigned -34018은 진단 기록이며 성공으로 계산하지 않음 |
| P2 받아쓰기·활용 미제출 초안 유실 | optional draft/sequence, 매 입력의 actor transaction 저장, 같은 문항·turn/단조 sequence로 늦은 응답 방지. 판정/SRS/event 생성과 분리 | cold repository/legacy JSON/retry/late writes/no grade·event·SRS + 실제 UI 종료/재개/채점 |
| 오디오 observer Swift6 수명 경고 | immutable observer ownership wrapper가 deinit에서 token 해제. actor deinit에서 non-Sendable 배열 접근 제거 | backend weak release 검사 + 기존 중복 재생/중단/late callback 회귀 |
| P2 학습 진입이 긴 레슨 목록 아래 묻힘 | 기존 학습 모듈 Section을 코스 목록 앞에 배치, 기존 학습순서/ID 불변 | 初中級 듣기 진입 hittable/Content29 실제5문항 수료·Resume·사전 연결 |
| P2 검색 Return이 줄바꿈·키보드 유지로 이어짐 | 검색에만 newline→space/trim 및 focus 해제를 적용. 일반 입력/Dictation 정규화 불변 | 실제 iPhone 검색·즐겨찾기·설정 cold 유지 및 Release 시작 UI68 PASS |
| P2 홈 안내문 대비 부족 | 기본 안내문의 secondary style 대비 실패를 primary로 교정 | 필터/무시 없는 `performAccessibilityAudit()` 재실행 중 |
| 오래된 native cohort/기대값 실패 | DATA06 원래80개를 고정 registry로 검사하고 후속 문항은 별도 검증. DATA08 원래1,821개와 현재 전체 pagination을 구분. 발음 테스트는 원래 course UUID로 고정. 꿰다 past의 잘못된 기대값을 규범에 맞게 뀄어요로 교정 | 기존 테스트 삭제·skip·assertion 비활성화0. native 전체 재실행 |

규범 참고(국립국어원 한국어기초사전): [되다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=89858), [뵈다](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=65573), [꿰다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=37786), [파랗다](https://krdict.korean.go.kr/m/eng/searchResultView?ParaWordNo=71306&nation=eng), [노랗다](https://krdict.korean.go.kr/eng/dicSearch/wordLinkViewPopup?ParaWordNo=40101&nation=eng&nationCode=6). AI와 공개 규범의 대조이며 독립 원어민 승인/모든 활용 구현으로 표시하지 않는다.

## 실행 기록·한계

- 수정 전 native148: 142 PASS/6 FAIL/skip0. 오래된 cohort와 실제 활용 오류, unsigned Keychain 실패를 구분했다.
- 첫 전체 `Tools/verify.sh`: portable418 PASS/0 fail/skip0(984.232초), native155 PASS/0 fail, UI11 중7 PASS/4 FAIL. 전체 명령 exit65이며 성공으로 표시하지 않는다. 실제 XCTest는 합166/162 PASS/4 FAIL.
- UI 실패 중 복원된 입력란의 caret/선택, 키보드가 가린 검색 결과, navigation back button 오선택은 잘못된 테스트 조작을 고쳐 동일 검증을 다시 실행한다. 잘못 입력된 답을 앱이 오답 처리한 것은 채점 버그로 집계하지 않는다. 홈 대비 감사 실패는 실제 앱을 수정했다.
- 재현 로그·xcresult는 `/tmp/hangul-data10-7/`에 보존. 최종 봉인 결과와 재현 명령은 검사 종료 후 별도 원장으로 갱신한다.
- 실제 한국어 TTS 재생 완료/정답 공개/정상·느린 속도 UI를 검증하되 TTS를 녹음이나 사람이 검청한 음질로 표현하지 않는다. 검증 녹음0, 독립 사람/교사 및 기존163후보36미해결·신규12계열27원문 언어 gate 유지.
- 사용자 확인(2026-10-22): 케이블이 없어 현재 iPhone 연결 불가, 내일부터 가능. 자동 후속 작업/예약은 만들지 않았다. 실제 iPhone 연결0: 물리 기기의 VoiceOver 발화/통화·이어폰 중단/한 손·배터리·비행기모드/서명 설치는 BLOCKED. 실제 App Store Connect/AdMob 계정과 Production ID 미제공: production 거래/광고 gate BLOCKED. Release 광고 미설정 시 비활성 정책 보존.
- Portable socket 금지 로컬 조회 및 native SQLite 학습·SRS·저장 검증은 물리 기기 비행기모드 실행과 구분한다. 짧은 세션 광고 차단·권한·실패 nonblocking의 policy/로컬 StoreKit 검증을 production 광고 수신으로 표현하지 않는다.
- Release B—Conditional 유지. 최종 검증 전 DATA-10-7 완료/전체 PASS/main 병합을 선언하지 않는다.

## 10월23일 재개 근거

- main/origin/main과 시작 SHA 일치, 같은 작업 브랜치/미커밋 수정 보존. 실제 iPhone 미연결 재확인.
- SmallProduction21: SE3/iOS26.0.1/Dark/AXXXL, UI06 1/1 PASS(163.370초). 걷다3문항의 초안 cold resume/편집/정답/완료 실제 실행. UI 편집 메뉴는 UIKit 표시에 따라 MenuItem 또는 Button으로 찾아 조작하고 최종 입력 문자열을 정확히 확인한다.
- SmallProduction18 build 실패/실행0은 외부 SPM binary artifact Info.plist 유실. 기존 캐시 보존 후 새 Packages20 경로에서 고정13.11.0/3.1.0 재다운로드, 실제 Info.plist 및 후속 build/test로 복구 확인. 원본·lockfile 불변.
- 임시 Production 제출 NSLog 제거. UI 비동기 setup/teardown으로 MainActor 경고 해결. 키보드 전환 invalid frame warning은 조사 중. 전체 UI14 포함 최신 전체 결과는 아직 대기.

## Checkpoint 원장 (완료 아님)

NormalAudits22: 2 UI 실행/2 실패/skip0. Numeric row/긴 문구의 큰 글씨 배치 수정 후 NormalAudits25는 SPM artifact 누락으로 build 실패/실행0, 새 ignored Packages26에서 현재 재검사 중이다. 모든 접근성 이슈를 계속 실패로 기록한다. 최소 SwiftUI 재현도 유사한 실패가 있지만 제품 문제 전체를 SDK 탓으로 확정하지 않는다.

Mac 공간이 약200MB까지 감소했다. 사용자에게 프로젝트 외 파일 정리를 요청했다. 작업의 중복 export만 원본 xcresult와 manifest를 남긴 뒤 정리했으며, 종료된 작업 소유 QA device는 학습 기록을 별도 SHA 일치 복사해 보존했다. 사용자 기기/기존 Production 삭제0. [실행 요약](DATA10_NATIVE_RUNS.json), [원시 로그 archive](DATA10_NATIVE_CHECKPOINT_LOGS.tar.gz). 최신 전체 검사 미완료·접근성 실패가 남아 있으므로 main 병합 금지다.


## 실기기 재개와 Release 시작 오류

기존 checkpoint `f46013cf3ea050a36368a0ddb65bf2171cdeb51b`를 일반 push하고 [Draft PR #24](https://github.com/Raccoon26/Project-Hangul-Study/pull/24)를 생성했다. main 미병합이다. fetch/auth/ADMIN/default main·원격 head를 재확인했고 Production/fixture114파일 SHA 불일치0이다. 사용자가 약6GB를 추가 확보해 디스크 부족은 복구되었으나 과거 실패/중단을 PASS로 바꾸지 않는다. NormalAudits26은 `No space left on device` 때문에 결과 봉인에 실패해 exit73·미완료이며 원시 로그를 보존한다. 최소 probe28/30의 Mach server/Runner 초기화 watchdog 실패는 본문 실행0인 환경 오류다. 이후 같은 작업 소유 Simulator에서 최신 Unit155/155 PASS(skip0, FinalUnits39)로 재실행을 확인했다. 실제 StoreKit 로컬 검증 거래가 있을 때 cache write 실패를 주입해도 verified/광고 차단·저장 오류 메시지가 유지되는 추가 assertion도 포함한다.

iPhone13ProMax/iOS27.2가 연결되었고 사용자가 Xcode Accounts/Team·개발자 프로파일 신뢰를 설정했다. 유효 서명/개발 프로파일로 Release build·설치·launch 요청은 성공했지만, 실제 UI 검사를 통해 **P0 시작 직후 crash**를 재현했다. Google Mobile Ads SDK의 load-time 초기화가 빈 App ID에서 `GADInvalidInitializationException`을 던졌으며 기존 `configuration.enabled` runtime guard보다 먼저 실행됐다. 따라서 설치/launch 명령 exit0만으로 앱 정상 동작을 보고하면 안 된다.

Production ID를 추측하거나 Release에 테스트 ID를 넣지 않았다. IDs가 없는 Release에서 `HANGUL_ADS_DISABLED`와 두 SDK의 build-phase 제외를 함께 적용해 SDK를 로드하지 않는 기존 무료 학습 경로를 제공했다. Debug 공식 테스트 광고·기존 구매 권한/빈도 제한/transaction·UserProgress/데이터는 보존한다. 비활성 빌드도 기존 빈도 이력을 유지한다. 향후 실제 소유 Production IDs를 설정할 때는 두 제외 설정을 함께 해제하고 `check_monetization.py --require-ads`·실제 SDK/동의 검증을 다시 수행해야 한다. 검사 도구는 source 설정의 불일치와 built executable의 dynamic/static SDK 잔류도 거부한다. 관련 Portable 새 회귀1개/현재419개 정의, focused9/9 PASS.

수정 Release의 실제 실행 파일은 GoogleMobileAds/UMP dependency 및 SDK ObjC class가 없고 `--built-info` 검사 PASS다. 같은 iPhone의 PhysicalUISmoke43 **1/1 PASS(exit0)**: 학습 Home 진입·한국어 검색·키보드 닫힘·정확한 검색어 유지·사전 상세 열기를 실제 실행했다. 사용자 선택 서명 Team을 보존하도록 generator를 보완했고 ignored package cache의 Swift를 앱 소스로 수집하지 않도록 제외했다. 물리 기기에서는 Release UI-only scheme으로만 검사해 테스트용 Keychain 정리/StoreKit transaction 초기화를 실행하지 않는다. 인증서/Apple ID·기기 식별자를 포함하는 private 로그는 공개 archive/PR에 넣지 않는다.

최신 Portable418/418 PASS(1582.460초) 이후 새 Release 회귀를 포함한 전체419 재실행, Simulator 전체169 XCTest 및 iPhone UI14 전체 검사가 진행 중이다. 첫 세 실기기 경로(첫 학습·종료/재개, 검색/즐겨찾기/설정 유지, 자모/받침/비음화 수료)는 PASS했으나 아직 전체 완료가 아니다. UI10/14 접근성·나머지 실사용 경로/실기기 음성 검청·오프라인/메모리·계정 외부 gate는 실제 후속 결과로만 갱신한다. 필수 로컬 실패가 남으면 PR을 ready/merge하지 않는다.


## 최신 실기기 사용 확인·추가 회귀 (2026-10-23, 여전히 진행 중)

사용자가 직접 확인한 항목: 한국어 TTS가 iPhone 스피커에서 정상 청취됨; 비행기 모드와 Wi-Fi OFF에서 듣기 학습 후 앱 완전 종료/재실행·이어하기/결과 유지 정상(네트워크 복구); 큰 글씨에서 읽기/스크롤/버튼 조작 정상(설정 복구). 정확한 최대 글자 크기나 모든 화면을 인증한 것은 아니다. VoiceOver는 사용자가 아직 확인하지 못했다고 답했으므로 NOT TESTED다.

새 Release 시작 회귀를 포함한 전체 Portable52는 **419/419 PASS, failures/errors/skipped0, 935.882초, exit0**이다. Portable44의 fixture 파일 준비 오류1건은 수정 후 focused9/9와 이 전체 검사로 재검증했다. 최종 native46(iOS26)은 **169실행/166 PASS/3 FAIL/skip0/exit65**: UI04의 disabled transaction 버튼 조작, UI10/14 접근성 감사 실패였다. 실기기 전체 UI45는 **14실행/10 PASS/4 FAIL/skip0**: UI06/08 조작과 UI10/14 감사다. 이 실패를 전체 PASS로 덮어쓰지 않는다.

UI06 실패 당시 실제 입력은 `걸어요　`였고 키보드 위 답안 버튼 대신 오래된 accessibility activation point가 Space를 눌렀다. UI08도 isHittable만으로는 가려진 사전 참조의 화면 내 위치를 보장하지 못했다. 테스트는 enabled 대기·현재 frame 중심·내비게이션/탭바/고정 제출 버튼/키보드 경계 안 가시성을 확인하도록 수정했다. 정답/판정/검증 assertion은 유지한다. 같은 실기기 PhysicalInputContext51 **2/2 PASS**로 걷다 세 활용의 직접 입력·초안 cold resume·채점/완료와 실제 Content29 레슨5문항·참조 사전·레슨 resume/완료를 재검증했다. 화면 제출 toolbar를 임시 추가한 실험은 원인이 앱 배치가 아니므로 원복했다.

실기기 UI45의 나머지 통과 경로는 첫 실행/단계 선택·자모/받침/발음 변화·20어휘 회독/완료·문법/퀴즈/SRS·듣기12문항 네 유형·보통/느린 실제 TTS·받아쓰기·검색/즐겨찾기/설정 cold 유지·통계/유지학습/광고 제거 화면·긴 TTS 중 백그라운드 중단/재개다. 실제 구매나 Production 광고 수신은 실행하지 않았다.

접근성 크기의 숫자 행은 같은 Text identity를 보존하는 AnyLayout으로 세로 배치하고 긴 메뉴 텍스트는 body/unlimited line/fixed vertical size, 화면 제목은 inline으로 보완했다. 그러나 PhysicalAccessibilityMetrics61 **3실행/1 PASS/2 FAIL/skip0**이며 UI10/14의 Dynamic Type/대비/잘림 자동 감사는 여전히 실패한다. 저장소 밖 최소 SwiftUI TabView/List도 유사한 실패를 재현하지만 전부 SDK 문제로 단정하지 않는다. 이슈 필터/skip/assertion 제거0, 후속 원인 분석 중이며 필수 실패가 있어 병합하지 않는다.

같은 실기기 responsive launch+CPU+memory metric 3회 PASS: responsive first frame 1.071/0.904/1.029초, CPU 1.112/1.071/1.072초, peak physical memory 약30.6/30.9/30.7MB(십진). 측정 부하·범위가 다른 UI45의 launch-only 0.631/0.692/0.576초와 별도 기록한다. Instruments Leaks59 실제 iPhone 앱 attach31.255초의 대기 상태 추적에서 두 번의 녹색 검사와 빈 Leaks 상세를 확인했다. 이 구간 누수 보고0이며 장시간 학습/통화/배터리 수명 PASS로 확대하지 않는다. All Heap & Anonymous VM persistent10.76MiB/total11.43MiB는 trace 할당 지표이며 전체 앱 physical footprint와 동일하지 않다.

현재 iOS17 최신 전체169 검사64를 추가 실행 중이다. StoreKit 로컬 테스트가 오래 대기해 stack sample을 보존하고 조사 중이며 미완료를 통과로 세지 않는다. 실제 기기 개인 식별자/Apple ID/프로파일/학습 DB/trace는 private 작업 경로에만 보존한다. VoiceOver 실제 발화·전화/이어폰 중단·장시간 배터리·실제 App Store/AdMob 계정 gate는 NOT TESTED/BLOCKED를 유지한다. DATA10-7 완료·main 병합 전이다.


추가 보존 확인: 실기기 학습 DB의 읽기 전용 복사본67은 integrity_check=ok/FK 오류0/UserProgress10이다. 이전 복사본49 대비 조사한17개 학습 테이블의 기존 primary key 누락0이며 즐겨찾기1, Vocabulary SRS20/Grammar3/Listening18, 듣기 판정18개가 저장돼 있다. 실제 완주 듣기 세션12/12·레슨5/5 정답과 회독/문법 완료 JSON도 확인했다. 이 사적인 DB/식별자는 Git에 넣지 않고 집계만 기록한다. UI12는 반복 검사에서도 이미 들은 문항/판정을 정상 UI로 이어간 뒤 아직 듣지 않은 문항을 선택하도록 보완했으며 데이터 초기화를 추가하지 않았다.

별도 최소 재현65는 iOS17의 TabView+ScrollView+VStack(앱 SDK/DB 없음)에서도 initial/end 두 자동 감사가 실패했다. List를 전면 교체하는 실험은 실패를 해결하지 못해 제품에 적용하지 않았다. Apple Accessibility Inspector의 실제 iPhone 대상 연결도 감사 대상을 열지 못했으며 VoiceOver 실제 발화 확인을 대신했다고 주장하지 않는다. 표준 body font인 화면 아래 요소의 reflow/가시성 영향은 계속 조사한다.

현재 `Tools/verify.sh`의 최신 전체 실행68(419 portable → resolve → Debug/Release Simulator/기기 architecture → Release UI 시작 회귀 → Debug 전체169)이 진행 중이다. Release 시작 검사를 먼저 수행해 후속 Debug 감사 실패가 있어도 그 결과를 별도로 확보한다. 프로젝트 재생성은74 app Swift/16 unit source·모든 scheme/사용자 signing byte 동일을 확인했다. 새 검증 결과가 나올 때까지 IN_PROGRESS/Draft/main 미병합을 유지한다.


### 7.8 2026-10-24 중단 후 재개·실제 SRS 복습 확인 (진행 중)

같은 브랜치의 일반 push checkpoint `03b224a2b301fc3fdcdcb9477ba15a0f2d4eba07`와 Draft PR24를 이어간다. fetch/auth ADMIN/default main·origin을 재확인했다. main/origin/main59d3bc7… 불변, ahead/behind2/0, Production/fixture114 SHA 불일치0이다. 새 미커밋 수정은 UI 검사 조작 보완이며 앱/데이터 원본을 바꾸지 않는다. 사용자는 VoiceOver를 추후 확인/미확인 유지로 다시 명시했다. 현재 실제 iPhone 연결은 해제되어 있으며 어제의 서명 Release 학습·음성/오프라인/큰 글씨 확인을 오늘 새 실기기 실행으로 바꾸지 않는다.

중단 중 끝난 `Tools/verify.sh` 실행68: Portable419/419 PASS(1994.290초, failures/errors/skipped0), resolve·Debug/Release Simulator·unsigned Release 기기 architecture build PASS, 실제 Release UI 시작 회귀68 1/1 PASS. native Unit155/155 PASS(11.592초), UI01~10 중7 PASS/3 FAIL이고 UI11~14는 worker 준비 timeout 때문에 실행하지 못했다. xcresult 요약은 worker 오류1을 포함해166/162 PASS/4 FAIL/skip0이며, 실제 테스트 메서드는165/162 PASS/3 FAIL 및 별도 worker 오류1이다. 최신169 전체 통과로 주장하지 않는다. UI07/08은 재생 완료 대기,10은 대비/잘림·screenshot timeout, runtime에는 keyboard invalid frame 및 background publishing 경고가 있었다.

Mac 전원 로그는10월23일23:23 Clamshell Sleep과 이후 반복 Sleep/DarkWake,10월24일10:13의 사용자 wake를 기록했다. 검사 중 sleep과 긴 대기/worker 오류를 연관 가능성으로 조사하되 모든 실패를 절전 탓으로 확정하지 않는다. 오늘 재검사는 덮개 열린 상태에서 명령 수명에만 caffeinate -i를 적용하며 영구 시스템 설정을 바꾸지 않는다.

기존 작업용 QA Simulator에 자연스럽게 예정일이 지난 듣기7개가 있어 실제 복습 E2E를 추가했다. 첫 임시 검사72는 coordinate 탭이 Home 복습으로 이동하지 못했고 일반 탭의73은 정상 이동했으나 SRS UUID 정렬을 화면 snapshot 순서로 가정해 실패했다. 기존 엔진은 learning_order로 snapshot을 만들며 저장 순서는 그대로 보존한다.74는 이전에 들은 문항을 재생할 때 선택지가 이미 존재하더라도 재생 중 비활성인 정상 상태를 기다리지 못한 검사 실패였다. 실제 snapshot의 순서·heard 상태를 대조하고 활성화 대기를 추가했으며 판정·SRS·엔진 정렬은 변경하지 않았다. 제품 UI 검사도 키보드가 있을 때만 현재 frame 중심을 탭하고, 일반 내비게이션은 표준 탭을 유지한다. 선택지의 존재/활성화·정답·원문 노출 assertion을 유지한다.

ExistingDueReview75 **1/1 PASS(exit0)**: 실제7개 복습 재생/정답·첫 판정 cold resume·7/7 완료. DB에서 기존 SRS 키7개 보존, 각각 reviewCount0→1/stage0→1·미래 due7/7, firstLearnedAt 유지, 기존 연습 snapshot2개 byte 동일, integrity_check ok/FK0을 확인했다. 시계 변경·seed/reset·사용자 DB 직접 쓰기0이며 읽기 전용 조사와 UI 학습만 수행했다. 원본 QA app support는 사전 SHA 동일 복사본을 보존했다. 이 별도 임시 E2E는 저장소169개 XCTest에 중복 합산하지 않는다.

현재 새 작업용 iPhone SE3/iOS26.0.1·Dark에서 **전체169 NativeSmallAwake76**을 실행한다. Swift actor data-race runtime check도 켜서 background publishing 경고의 앱 actor 위반 여부를 조사한다. 기존 사용자/QA Simulator 데이터는 삭제하지 않았다. 필수 실패/미실행이 해소되기 전 완료/ready/main 병합 금지, DATA10-8/11 미착수다.

## 접근성 검사 해석 기준

Apple 문서의 [감사 범위](https://developer.apple.com/documentation/accessibility/performing-accessibility-audits-for-your-app)와 [WWDC23 자동 감사](https://developer.apple.com/videos/play/wwdc2023/10035/)를 대조했다. 자동 감사는 현재 화면에 한정되며 모든 접근성 사용성을 보장하지 않는다. 현재 UI10/14는 필터 없이 초기 viewport의 전 category를 검사하고, 실제 마지막 항목의 스크롤/가시성은 별도로 검증한다. 화면 아래 모든 영역을 자동 감사한 것으로 확대하지 않는다. 최소 재현의 유사 실패만으로 제품 실패를 무시하지 않으며, 실제 VoiceOver는 사용자가 추후 확인하기로 해 NOT TESTED를 유지한다.


### 7.9 깨어 있는 상태의 전체 재검사·작은 화면 조작 분리 (2026-10-24)

NativeSmallAwake76은 전체169 실행/165 PASS/4 FAIL/skip0/exit65다. Unit155/155 PASS(18.195초), UI10/14 자동 감사와 UI07 편집 메뉴·UI08 작은 화면의 즉시 isHittable 가정이 실패했다. actor runtime check에서 trap은 없었고 background publishing 경고는 재현되지 않았다. 키보드 표시 시 invalid-frame warning2건은 남는다. 실제 컴파일한 UI source snapshot을 별도 보존했으며 이후 보완한 검사로 과거 결과를 덮어쓰지 않는다.

UI07은 초안 복원 자체가 성공했지만 넓은 입력란의 빈 중앙을 길게 눌러 전체 선택 메뉴를 열지 못했다. 실제 텍스트의 앞쪽 좌표 재시도와 전체 삭제/최종 입력 문자열 assertion을 추가했다. 중단된 이전 QA 세션도 나머지 문항을 정상 학습으로 완료한 뒤 새12문항 검사를 시작하며 reset/seed/DB 쓰기로 우회하지 않는다. UI08은 버튼이 존재하나 SE3에서 화면 아래에 있어, 실제 스크롤로 도달한 뒤 hittable을 검사한다.

ListeningInputSmall78은2 실행/1 PASS/1 FAIL/skip0/exit65: UI08의 실제 Content29 5문항·정답 후 원문/사전·cold resume·완료 PASS. UI07은 텍스트 교체 이후 키보드가 열린 상태에서 위 재생 버튼을 스크롤하려다 실패했다. 화면 기록에서 키보드 툴바의 닫기 동작을 확인했고, 해당 받아쓰기 경로만 실제 닫기 버튼을 누른 뒤 재생하도록 보완했다. 활용 입력의 키보드 위 제출 검사와 채점/저장 assertion은 유지한다.

앱/DB/광고 SDK가 없는 KeyboardProbe77도 동일 프레임 경고를 냈으나 placeholder selector가 입력 후 바뀌어 두 테스트는 실패했다. 고정 field identifier로 비교한 KeyboardProbe79는3/3 PASS(exit0): 툴바 없음·Spacer 없는 툴바·Spacer 있는 툴바 모두 정확한 입력/제출을 통과했다. 경고는 두 툴바 case에만 재현됐다. 임의로 필수 키보드 닫기를 제거하거나 프레임 경고를 앱 crash/판정 실패로 집계하지 않는다. 이 임시 probe는 저장소169개에 합산하지 않는다.

자동 감사 스크린샷에서 Dark Home Resume 버튼이 어두운 카드 위 indigo 글자로 실제 대비 부족을 보였다. 해당 Text에 semantic primary 전경색을 적용했다. 다른 offscreen/스크롤 reflow의 대비·Dynamic Type·잘림 실패까지 해결했다고 주장하지 않는다. 이 제품 수정과 UI 보완을 포함해 전체169 NativeSmallAwake80을 다시 실행한다. iPhone13ProMax/iOS27.2의 무선 개발 연결도 다시 확인했고, 원본 app support의 읽기 전용 복사본을 보존한 뒤 signed Release UI-only 전체14 PhysicalReleaseFull81을 순차 대기시켰다. 실제 기기에서 Unit/StoreKit cache 초기화 검사는 실행하지 않는다.

Production/fixture114 SHA 불일치0·현재 bundle31테이블/integrity ok/FK0을 재확인했다. VoiceOver는 사용자 명시대로 추후/NOT TESTED, 필수 실패가 남으면 완료/ready/main 병합하지 않는다.
