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

분석·검수/실행 근거 commit `baa78564b5e1d7c439937997257e947f22b8c973`를 `codex/data10-1-listening-analysis`에 정상 push했고 [PR #18](https://github.com/Raccoon26/Project-Hangul-Study/pull/18)을 생성·이 채팅에 연결했다. PR은 MERGEABLE/CLEAN, `statusCheckRollup=[]`, required checks 조회는 ‘no checks reported’(CLI exit1)였으며 규칙/Actions workflow0이다. **필수 원격 검사가 없는 상태이며 CI PASS가 아니다.** 로컬363/365·native136/141과 명령143/미완료 gate를 PR 본문에 명시했다. 실패한 필수 CI를 우회하거나 admin/force merge하지 않는다.

이 인계 기록은 문서만 보충하고 검증한 Source/Bundle/fixture/runtime/테스트를 바꾸지 않는다. 사용자 위임대로 정상 merge 후 fetch/ff-only로 로컬 main을 맞추고 전체SHA 일치/status를 확인한다. 자기 merge SHA 기록을 위해 재커밋하지 않으며 **실제 최종 merge SHA·main=origin/main·clean 상태는 PR/Git과 최종 응답이 기준**이다. 다음 환경은 fetch 후 최신 main에서 시작한다. 분석·환경 설정은 DATA10-1에서 종료하며 다음 Batch 자동 시작0이다.


## 2. DATA-10-2 / 初中級 Listening Batch A (2026-10-20 JST)

명시 요청으로 신규 상황60개·문제120개를 제작한다. DATA10-1의 혼합 Level Batch A 계획은 이번 初中級 범위로 조정하며 전체150~250원문/300~500문제 목표는 유지한다. 누적60/120, 남은 목표90~190/180~380이고 다음 단계는 시작하지 않는다. **Release B—Conditional** 유지.

### 2.1 시작 동기화·권한·환경 보존

- 지정 clone `/Users/shinchanhyeok/Desktop/Project-Hangul-Study`, 시작 clean main/미커밋0, `git fetch origin` 후 HEAD=origin/main=`6748af987f59050ec78db63be944ad5acd6e02b9`(PR #18 병합). origin fetch/push=`https://github.com/Raccoon26/Project-Hangul-Study.git`.
- `git status`, `git remote -v`, `gh auth status`, repo/default/main/권한 ADMIN 확인. keyring의 Raccoon26 HTTPS/repo·workflow 인증. main protection404/규칙0/Actions workflow0. 실제 PR 전달·merge 결과는 아래 §2.5와 최종 Git/PR이 기준이다.
- `codex/data10-2-listening-batch-a` 별도 branch, 기존 checkout 사용·worktree0. 기존 변경 삭제·stash·force/reset·이력 재작성0. PROJECT_STATUS/CONTENT_GUIDE/DATA_PROGRESS/RELEASE_CHECKLIST/DATA08·09 기록/Docs/DATA09_CLOSEOUT/실제 듣기 엔진·DDL·Validator를 대조했다.
- 실제 직전24 Source/DB를 `Tests/Fixtures/content-v24-production.json.gz`/`.sqlite`에 불변 보존했다. 기존95파일은24 snapshot 두 개를 통한 당시 Source/Bundle 보존과 나머지 원본 byte 보존을 확인한다. 현재 Source/Bundle만25로 정상 증가하며 기존 엔티티·payload/revision 변경0이다.
- Mac의 기존 Python3.11.6/SQLite3.44.0은 시스템 그대로다. 새 격리 writer는 SQLite3.53.1/STAT4없음/zone allocator 비사용이다. 고정 원본 SHA·setup 도구·재현법은 [writer 기록](Docs/DATA10_WRITER.md), [compile profile](Docs/DATA10_A_WRITER_PROFILE.json). 기존24의 전체 byte/SHA를 실제 재현해 DATA10-1의 writer 문제를 해결했다. 통계 행 삭제/재정렬·header 수정/Validator·assertion 완화0.

### 2.2 실제 증가·유형·배치

Content24→**25** / Schema4 / reader7 / UserProgress10 유지. Vocabulary2,287/Meaning2,420/Grammar96/Course8/Lesson103 불변. Example4,813→**4,873**(+60, 문장4,860+발음13), Listening1,936→**2,056**(+120), Question3,553→**3,673**(+120), content_items15,941→16,241(+300). 기존 본문/ID/created_at/revision/order/membership/관계 변경·삭제/비활성화0, 추가 provenance source1개(학습 엔티티 수에서 제외).

| Level | 시작→종료 Listening | 의미 /한국어 /받아쓰기 /내용이해 | 실제 증가 |
| --- | --- | --- | ---: |
| 入門 |34→34|4 /23 /3 /4|0|
| 初級 |79→79|28 /4 /25 /22|0|
| 初中級 |1,823→1,943|18 /12 /1,852 /61|120|
| 전체 |1,936→2,056|50 /39 /1,880 /87|120|

6영역(일상/약속변경/교통/쇼핑/서비스/부탁·거절) 각각10원문/20문제. 새4유형은 의미18·한국어12·받아쓰기30·내용60이다. 각2~3문장의 연속 발화/안내를 원문1개로 세고, 같은 Example로 Listening2/Question2를 만든다. **기존 source 재사용0 /신규 source60 /신규 source의 추가 참조60**, 한국어 오답 후보도 실제 Batch의 다른 학습 원문을 사용한다. 오답용 filler Example·단어 재생으로 수량을 채우지 않는다.

새 UUID300개(Example60/Listening120/Question120)를 authoring 원장에1회 고정했다. 모든 신규 ID canonical UUID/active/level 일치, 기존 revision 승인목록은 빈 배열이다. learning_order2060~2179, batch103~108(화면練習104~109), 같은 source 두유형은3구간 차이로 분리한다. 기존 batch102의 부분 구간/빈칸/실행중 snapshot은 재작성하지 않는다. 자동SRS source 중복 선택과 기존 번호형 UI 한계는 남는다.

### 2.3 Batch Self Review·중복·근거

assistant가60한일 원문·120prompt/정답/해설·270선택지·30정확한 accepted를 작성 후 별도 재독하고 원고20필드를 교정했다. A08 기존 첫 문장 중복을 독자 장면으로 재작성, A22 승차역/목적역 모호함 제거, A35 비현실적 오답 교정, A44 문자 번역, A59 자연스러운 일본어, A05 설명을 수정했다. 추가 실제 선택지 재독에서 A18 성별을 임의로 정하지 않는 자연스러운 번역, A22 오답 중복, A31 조사 중복, A41 한일 어색한 결합을 교정했다. 원고 승인 timestamp는 실제 UTC로 바로잡았으며 기존 created_at 변경0이다. 원고 교정 전 portable 두 시도는 각각 중단(exit130)했고 완료/PASS로 합산하지 않는다. writer wrapper 초기 전체 실행은373개 중368PASS/1FAIL/4ERROR(누적 기대수량1·iterdump 미지원4)였으며 기대수량 교정·표준 dump 위임 후 전체를 다시 실행한다.

[항목별 교정·검수](Docs/DATA10_A_SELF_REVIEW.json), [전60원문/120문제·선택지](Docs/DATA10_A_ITEMS.md), [기존4,813예문과 가까운 후보 각3개](Docs/DATA10_A_SIMILARITY.json), [검수 범위/한계](Docs/DATA10_A_REVIEW.md). 전체 기존+Batch내 NFC/공백 한국어·한일쌍·마지막 .!? 제외 완전 중복0, 단순 치환/동일 원문 재발급0이다. 짧은 정형 표현·주제 공유까지 교육적 의미 중복0을 인증하지 않는다. 기존163선행120/7/36·Level8미해결을 그대로 둔다.

한국어 자연스러움/높임·시제·지시대상/조건·변경 전후·이유/다음 행동·일본어 해석·오답 비동치/정답 유일성을 자체 검토했다. 예 A20은 다음 주에 일정을 다시 정하는 뜻이고 실제 만남일 미정, A55는 내일 불가/모레 가능, A59는 먼저 발표할 필요를 부정한다. 내부 初中級 편집 Level이며 공인 TOPIK/빈도/독립 전문가 인증이 아니다. TTS120개이며 실제 녹음0, 외부 대본·음원 복사0/자체 저작 provenance 명시. 독립 사람·교사/전수 사전·실제 TTS 검청은 NOT TESTED다.

Dictation accepted는 정확한 원문1개씩이며 마지막 .!? 생략은 기존 Swift 판정만 사용한다. 내부 문장부호·철자 차이/띄어쓰기 경고를 구분하고 자유작문·일반 직접입력 정규화를 확대하지 않는다. 정답 공개 전 transcript는 기존 prompt_ko=null/기존 UI 정책을 유지하며 실제 VoiceOver 검증은 별도 gate다.

### 2.4 검사 결과

최종 실행 결과는 아래 표와 [실제 결과 JSON](Docs/DATA10_A_TEST_RESULTS.json)에 기록한다. 작성 중의 부분/중단 실행을 최종 PASS에 합산하지 않는다.

| 검사 | 실제 결과 | 범위·한계 |
| --- | --- | --- |
| strict24→25 /후속 재구성 |0errors/기존10warnings·byte/SHA 일치|짧은 발음예시5+동형어 후보5 유지. Validator 완화0|
| 전수 Source/DB·95파일·Stable ID |25테이블67,385행 일치/integrity ok/FK0·기존15,941 fingerprint/본문/순서/revision 보존|Content24 source/DB는 불변 snapshot. 신규UUID300·중복/고아0|
| writer cold setup rehearsal |별도 새 디렉터리 설치→24/25 byte/SHA·표준 dump 왕복 PASS|시스템 Python/DB·통계 행 편집0|
| 최종 verify portable |**373/373 PASS**,684.789초,실패/오류/skip0,phase exit0|최종 고정 원고 기준. 전용8개 포함, 과거23/24 byte gate도 PASS|
| Debug/Release Simulator·Release device architecture |**3/3 build PASS**, SDK resolve PASS|jobs1, unsigned architecture build. 실제 iPhone/서명 archive 아님|
| 최종 verify XCTest |**142실행·137PASS/5FAIL/skip0**,929 assertion/0unexpected·suite34.741초,phase/full command exit65|봉인 xcresult 요약과 전체 raw gzip 보존. 진단 대기 강제 중단이 아닌 정상 실패 종료|
| 새 Batch A native |**120문제·4유형/원문60·played gate/정답·모든 오답/받아쓰기·내부부호·spacing PASS**|새1메서드, 전체142에 포함. 실제 음성 검청/화면 인증 아님|
| DATA08 P1 세 건 |**native5메서드 PASS**(전체142에 포함)|전체1,880 dictation 종결부호 검사 포함. 실기기 화면·음성·VoiceOver 별도|
| 독립 사람/실제 기기·구매/광고 |NOT TESTED / BLOCKED|Release B—Conditional 유지|

Source25 SHA `ddb21c13e12624da2f208d3f842309ab79a075b986cea832424857cdae763941`, Bundle/재구성 SHA `01652666fc34cbc2d69a2d8a82f8aca778b20045b629df7d8623ee3e87a64500`.

final command는 위 final results JSON과 `Docs/DATA10_A_XCODE_WRAPPER.txt`를 따른다. 기존 verify.sh를 그대로 실행하고 wrapper는 작업1개/별도 DerivedData/result/비병렬 테스트/진단 수집 설정만 지정했다. Debug/Release/device gate·XCTest를 생략하지 않았다. [전체 로그 gzip](Docs/DATA10_A_FINAL_VERIFY_LOG.txt.gz), [봉인 xcresult 요약](Docs/DATA10_A_XCRESULT_SUMMARY.json).

native 실패5개는 DATA10-1과 동일한 DATA06 cohort 가정1, 발음 course 가정2, 되다/뵈다 활용·꿰다 기대값1, cold Purchase cache1이다. 새 Batch/native 회귀 실패0·runtime 수정0. [기존 발견·원인/한계](Docs/DATA10_NATIVE_FINDINGS.md)를 유지하며929개 서로 다른 제품 버그나 실제 구매/모든 앱 실패로 합산하지 않는다. simulator는 새 임시 기기만 생성·사용/정리하며 기존 사용자 Simulator/진도는 삭제하지 않는다.

초기 검사 실패와 중단을 숨기지 않는다. 초안 전용8개는 검사 코드의 SQL 투영키/문장 경계 가정에서1FAIL/1ERROR가 났고 수정 후 최종8 PASS. writer 초기 전체373는368PASS/1수량FAIL/4dumpERROR였으며 최종 전체373 PASS로 재검증했다. 별도9개·dump2개 targeted PASS와 동결 전 native142/137/5를 최종 고유 수에 더하지 않는다. 초기 로그와 기록은 결과 JSON/보존 gzip에 있다.


### 2.5 Git 전달·다음 환경

검증한 Content25/원고·회귀·기록을 작업 branch에서 정상 commit/push하고 PR로 전달한다. 원격 필수 검사/mergeability를 다시 확인해 정상 병합하며, 최종 main=origin/main의 전체 SHA·clean 상태는 PR/Git과 최종 응답을 기준으로 남긴다. 자기 merge SHA를 기록하기 위한 재귀 commit은 하지 않는다. 실제 PR/전달 commit은 아래 후속 기록에 추가한다. 다음 단계 자동 시작0, force push/reset/기존 Production 삭제0.


### 2.6 실제 Commit/Push/PR 인계

검증/제작 commit `e07e823ef9f9feed54e1930d0c9ebe0486a201da`를 별도 branch `codex/data10-2-listening-batch-a`에 저장했다. 첫 일반 HTTPS push는 RPC HTTP400/sideband disconnect로 실패했고 remote head가 없어 PR 생성도 실패했다(생성된 PR0). 인증 API는 Raccoon26/ADMIN으로 정상이며 전체 접근 가능한972 blob 중50/100MiB 초과0·최대19,214,336bytes였다. 파일 삭제/축소/LFS/이력 재작성으로 우회하지 않았다.

`git -c http.version=HTTP/1.1 -c http.postBuffer=524288000 push -u origin codex/data10-2-listening-batch-a`의 **일반 push 재시도 성공** 후 remote head가 위 commit과 일치함을 확인했다. 설정은 해당 명령에만 적용하고 global/repo 설정은 바꾸지 않았다. 전송 경로의 세부 HTTP400 원인은 단정하지 않는다. [객체 크기·전달 기록](Docs/DATA10_A_GIT_DELIVERY.json).

[PR #19](https://github.com/Raccoon26/Project-Hangul-Study/pull/19)를 생성하고 채팅에 연결했다. 최초 head는 위 제작 commit, MERGEABLE/CLEAN·statusCheckRollup=[]였다. `gh pr checks --required`는 no checks reported(exit1), 규칙/Actions workflow0으로 **필수 원격 검사가 없는 상태이며 CI PASS가 아니다**. 최종 portable373 PASS·3build PASS·native137/142와 명령65/기존5실패·B—Conditional을 PR 본문에 명시했다.

이 인계 보충은 문서·전달 근거만 추가하고 검증한 Source/Bundle/코드/테스트를 바꾸지 않는다. 보충 commit 정상 push 후 최신 head의 검사/mergeability를 확인해 user 위임대로 정상 merge한다. 실패한 필수 CI나 admin/force로 우회하지 않는다. 병합 후 로컬 main을 fetch/ff-only하고 origin/main과 전체SHA·clean 상태를 대조하며 최종 실제 merge SHA는 PR/Git·최종 응답을 따른다. DATA10-2에서 종료하고 다음 단계는 시작하지 않는다.
