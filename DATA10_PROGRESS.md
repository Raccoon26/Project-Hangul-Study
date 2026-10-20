# DATA-10 진행 기록

## 1. DATA-10-1 / 듣기 분석·환경 설정 (2026-10-20 JST)

명시 요청에 따라 Mac 로컬 `/Users/shinchanhyeok/Desktop/Project-Hangul-Study`에서 진행한다. 분석·공통 환경 인계 규칙·신규150~250원문/300~500문제 제작 계획까지이며 실제 제작/통합·runtime 수정0. DATA09 콘텐츠 수량·통합 종료와 출시/사람 검증 완료를 구분하고 **Release B—Conditional**을 유지한다.

### 1.1 시작 Git·인증·환경

- `git status --short --branch`: clean main, tracked/untracked 변경0. origin fetch/push=`https://github.com/Raccoon26/Project-Hangul-Study.git`, 실제 clone/기본 main 확인.
- `git fetch origin` 성공. HEAD=origin/main=`3de2e08a2e934be545f0cbcbecef1ba479ddb233`, ahead/behind0. PR [#17](https://github.com/Raccoon26/Project-Hangul-Study/pull/17) MERGED(2026-10-20 16:32:17 JST), merge SHA와 일치.
- `gh auth status`: Raccoon26/keyring/HTTPS 인증, repo/workflow scope. `gh repo view`: ADMIN. main protection 조회404(`Branch not protected`), rulesets0, Actions workflows0. PR/merge 권한은 API 근거로 확인하고 실제 성공은 마지막 전달 결과로 기록한다. 토큰 원문 저장0.
- 별도 branch `codex/data10-1-listening-analysis`, 기존 checkout 사용·worktree0. 미커밋 변경 삭제·stash·force push/reset0.
- macOS27.0 arm64, Python3.11.6 / SQLite3.44.0, Xcode27.1(27A9275). `xcode-select -p`=`/Applications/Xcode.app/Contents/Developer`. iOS17.0 iPhone15Pro Simulator `99A1C568-FE33-46DE-80E1-32A41B4E2486` 설치 확인. Cloud의 이전 Xcode 없음 기록은 역사로 보존하고 이번 실행을 별도 기록한다.
- 공식 GoogleMobileAds13.11.0 / UMP3.1.0 resolve 성공(exit0). Xcode가 생성한 `Package.resolved`를 환경 재현용으로 보존한다. 기존 exact version/SDK·광고 ID·구매 정책을 변경하지 않는다.

### 1.2 실제 기준·증가·분석 결과

Content24 / Schema4 / minReader7 / UserProgress10. 시작=종료 Vocabulary2,287 / Meaning2,420 / Example4,813 / Grammar96 / Question3,553 / Listening1,936. 신규/수정/삭제/비활성/ID발급/revision변경0, bundle 교체0.

| Level | Listening 시작→종료 | 의미 /한국어 /받아쓰기 /내용이해 | 증가 |
| --- | --- | --- | ---: |
| 入門 |34→34|4 /23 /3 /4|0|
| 初級 |79→79|28 /4 /25 /22|0|
| 初中級 |1,823→1,823|0 /0 /1,822 /1|0|
| 그 이상/유지 |0→0|0 /0 /0 /0|0|
| 전체 |1,936→1,936|32 /27 /1,850 /27|0|

Source25테이블66,094행·DB 일치, integrity ok/FK0, active 참조·문제1:1·level/순서/bounded batch 점검. [전수 집계·95파일 SHA·28항목 재독 표본](Docs/DATA10_LISTENING_BASELINE.json), [분석·설계와 엔진 경로](Docs/DATA10_LISTENING_ANALYSIS.md).

듣기 내부 sourceID/정규화 Korean/한일쌍/종결부호 무시 중복0. 전체 Example에는 Korean동일/번역다름4쌍·동일한일쌍0, 자동병합0. 받아쓰기95.56%·初中級99.95%, 전 difficulty null, 多문장4개, 피드백=번역1,825개. 문자수·어절수는 입력부담 대리 지표이며 실제 청취 난도/시간/공인등급이 아니다. Grammar96 중29개, 신규54 중4개만 듣기와 연결; 신규216예문의 듣기 추가0. 기존 선행 후보163전부가 듣기에 있으며120해결/7조건부/36미해결(Level8포함) 유지.

assistant는 전수 구조/통계 조사와 별도로28개 표본의 한일·prompt·선택지·해설을 재독했다. 독립 사람/교사/실제음성·콘텐츠 전수 외부사전 검수는 **NOT TESTED**. native 활용 실패의 되다/뵈다/꿰다에 대해서만 한국어기초사전 활용을 제한적으로 확인했다([발견 근거](Docs/DATA10_NATIVE_FINDINGS.md)). 의미 중복·Level 적정성 전체 승인으로 표현하지 않는다. 신규 언어 교정·runtime 버그 수정0. 알려진 난도·SRS 중복 원문 가용성·기기 gate는 분석 문서에 남긴다.

### 1.3 후속 계획과 공통 인계

목표150~250고유 신규 원문/300~500문제를 유지하며 기준안200/400, 원문당2서로 다른 유형을 계획한다. 入門20/40·初級60/120·初中級120/240, 의미100·한국어60·받아쓰기80·내용160. 4Batch 각각50원문/100문제. 원문1개는 Example1개, 문제마다 Listening/Question을 각각 만들어 현1:1계약을 유지한다. 재사용은 관계로 별도 기록하고 원문/문제 목표에 중복 가산하지 않는다. source별2유형은 다른20문항 구간으로 분리하지만 자동SRS가 같은 원문 두항목을 함께 선정할 수 있는 현한계는 남는다.

AGENTS에 Mac/Cloud 공통 시작 fetch/status/auth/origin/main/미커밋/단계원장, clean main ff-only·별도branch, 환경 전환 전 checkpoint commit+push·이전환경중단·동시수정금지, 종료 commit/push/PR/check/merge/전체SHA대조·실패보고·force/reset금지를 추가했다. 이번 콘텐츠 제작0·다음 Batch 자동시작0.

### 1.4 이번 검사·native·미완료 gate

[실행 결과 JSON](Docs/DATA10_TEST_RESULTS.json)이 이번 수/exit의 기준이다. 과거365PASS/native141실행0을 이번 PASS로 인용하지 않는다.

| 검사/실행 | 실제 결과 | 상태·근거 |
| --- | --- | --- |
| 읽기 전용 전수 구조 감사 |34점검 PASS, Source25테이블66,094행 일치, integrity ok/FK0|별도 구조 점검이며 unittest 수에 가산하지 않음|
| 보호95파일·최종 재감사 |95/95 byte 보존, 최초/최종 감사 JSON 동일|Source/Bundle/과거 fixture·ID/revision 변경0|
| strict23→24 validate-only |exit0 /0errors /기존10warnings /33.4335초|짧은 발음예시5+동형어 후보5 유지. 언어·음성 승인 아님|
| Mac 동일24 임시 재구성 |exit0 /0errors /10warnings /16.1133초|원래31테이블 전행/공통schema/index metadata 동일·추가STAT4로32테이블, byte/schema/SHA 재현 FAIL|
| `sh Tools/verify.sh` 공통 portable 부분 |**365실행·363PASS/2FAIL/errors0/skip0,2,457.630초,exit1**|[전체 로그](Docs/DATA10_PORTABLE_LOG.txt). 실패2건은 아래 참조|
| SDK resolve |GoogleMobileAds13.11.0/UMP3.1.0,exit0|Package.resolved 보존|
| iOS17 direct Debug/XCTest 첫 시도 |126시작·121PASS/4FAIL·StoreKit1미종료·15미시작,command exit143|[원시 로그](Docs/DATA10_NATIVE_IOS17_LOG.txt), 미완료 실행|
| iOS26 direct 재시도 |**141전부 종료·136메서드PASS/5FAIL/skip0,assertion929실패/unexpected0,suite24.463초**|[원시 로그](Docs/DATA10_NATIVE_IOS26_LOG.txt). 종료 후 Simulator 진단 수집 대기→중단(exit143); sealed xcresult/정상명령종료 아님|
| 추가 설치 재시도/임시서명 진단 빌드 |각XCTest0·exit143|설치호출 대기/8GB 병렬컴파일 부담으로 각각 중단. 추가PASS0. [설치 로그](Docs/DATA10_NATIVE_INSTALL_RETRY_LOG.txt), [빌드 로그](Docs/DATA10_SIGNED_BUILD_INTERRUPTED_LOG.txt)|
| DATA08 P1 세 건 |**native5메서드 PASS**(전체141에 포함)|[세부 범위](Docs/DATA10_NATIVE_FINDINGS.md).1,850 dictation 판정·원SRS/버전보류·snapshot·ViewModel, 실기기 화면 전체/음성/VoiceOver는 별도|
| Debug app/test host build·link·실행 |직접 native 시도에서 실행됨, 경고 있음|Release Simulator/device architecture는 verify의 portable 실패로 미실행, 서명 archive 미실행|
| 실기기/독립 사람·전수 사전 |BLOCKED / NOT TESTED|iPhone/실제3~10분/오프라인·음성/중단/VoiceOver/IME/메모리/실제광고·구매 및 독립 언어 승인 미완료|

portable 실패는 `test_data09_final_audit...test_immutable22_and_deterministic_strict23_reconstruction`(line50)과 `test_data09_integration...test_preserved19_and23_sources_and_both_strict_update_gates`(line46)의 frozen DB byte 비교다. 현재 Mac SQLite3.44.0 ENABLE_STAT4의 추가 sqlite_stat4/32테이블과 header writer 차이를 [전31테이블·공통schema·index/FK/SHA 비교](Docs/DATA10_REBUILD_COMPARISON.json)로 분리했다. frozen23도 [별도 재구성/비교](Docs/DATA10_REBUILD_V23_COMPARISON.json)로 원래31테이블 전행·공통schema 일치/추가sqlite_stat4만 있음을 확인했다. DATA09의 당시 Linux SQLite3.53.1 byte-exact PASS를 취소하거나 이번에도 PASS로 복사하지 않는다. 통계 테이블 삭제·assertion/Validator 완화·bundle 덮어쓰기0. 다음 실제 배포 전 writer 환경 재현 gate가 남는다.

native 실패5메서드는 DATA06 batch 경계1개(3assertion), 발음 course 선택 가정2개(총918assertion), 실제 되다/뵈다 활용 및 꿰다 기대값 재검토1개(7assertion), cold 구매 cache1개(1assertion)다. **929개의 서로 다른 runtime 버그로 집계하지 않는다.** [분석·정적85개 영향 후보/후속 gate](Docs/DATA10_NATIVE_FINDINGS.md). 새로 재현한 활용 P1을 미수정으로 남기며 모든 테스트/제품 PASS를 주장하지 않는다.

이번 native 명령은 진단 수집/설치 대기·빌드 중단을 포함해 모두143으로 종료한 시도다. 실제141개 메서드 종료 로그와 명령 성공은 구분한다. iOS17/26 결과·중복 P1 메서드를 합산해 고유 테스트 수를 늘리지 않는다. 추가 서명 진단은 미완료이고 cold cache의 서명/Keychain 원인을 확정하지 않는다. source/DB·fixture와 runtime 코드·기존 테스트 assertion은 보존했다. Xcode 원시 로그의 생성된 끝공백은 그대로 보존하고 작성 파일의 diff whitespace 검사를 통과했다. 검사 중 형식만 바뀐 project/Info.plist는 semantic 동등 확인·변경본 보존 후 원래 byte를 복원했다.

실제 native 재시도 명령(이번 Mac UUID; 다른 환경은 설치 destination을 다시 조회):

```sh
xcodebuild -resolvePackageDependencies -project HangulStudy.xcodeproj -scheme HangulStudy
TEST_DESTINATION='platform=iOS Simulator,id=99A1C568-FE33-46DE-80E1-32A41B4E2486' sh Tools/verify.sh
xcodebuild -project HangulStudy.xcodeproj -scheme HangulStudy -configuration Debug -destination 'platform=iOS Simulator,id=99A1C568-FE33-46DE-80E1-32A41B4E2486' -derivedDataPath /tmp/hangul-data10-1/DerivedData -resultBundlePath /tmp/hangul-data10-1/NativeTests.xcresult CODE_SIGNING_ALLOWED=NO test
xcodebuild test-without-building -project HangulStudy.xcodeproj -scheme HangulStudy -configuration Debug -destination 'platform=iOS Simulator,id=ACF4487F-0A8A-4D78-B16D-98B2DE5C35AF' -derivedDataPath /tmp/hangul-data10-1/DerivedData -resultBundlePath /tmp/hangul-data10-1/NativeTests26.xcresult -parallel-testing-enabled NO -test-timeouts-enabled YES -default-test-execution-time-allowance 120 -maximum-test-execution-time-allowance 120 CODE_SIGNING_ALLOWED=NO
```

두 번째 추가 설치 재시도는 위 command에 `-collect-test-diagnostics never`와 새 result 경로 NativeFinal을 사용했다. 임시 서명 비교는 별도 SignedDerivedData/result 경로·`-only-testing:HangulStudyTests/StoreKitPurchaseTests`·`CODE_SIGNING_ALLOWED=YES CODE_SIGN_IDENTITY=-`를 사용했고 build 중단/XCTest0이다. 명령 원문과 각 결과 로그를 남기며 다음 Mac은 CoreSimulator 상태와 낮은 jobs/active architecture로 환경을 먼저 안정화해야 한다.


### 1.5 Git 전달

검증 후 정상 Commit→Push→PR→필수 검사 확인→main merge→로컬/원격 main 전체SHA 일치를 수행한다. 실제 PR·검사·merge 결과는 아래 전달 기록과 Git/최종 응답이 기준이다. 권한/CI/검증문제로 미완료인 항목을 성공으로 바꾸지 않는다.
