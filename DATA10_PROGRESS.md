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

## 3. DATA-10-3 / 初中級 Listening Batch B (2026-10-21 JST)

### 3.1 最新 main 동기화·환경 인계

Cloud `/workspace/Project-Hangul-Study`의 시작 clean main을 fetch하고 PR19 병합 main `238b6452d9a69d61f9e187c6176cd76bb240b098`으로 ff-only 동기화했다. origin fetch/push는 지정 `Raccoon26/Project-Hangul-Study`, gh 인증 Raccoon26/HTTPS·repo 기본main·viewerPermission ADMIN을 확인했다. 토큰 원문 기록0. `codex/data10-3-listening-batch-b`에서 작업했고 다른 환경의 미커밋 파일을 가져오거나 동시에 수정하지 않았다. 기존 미커밋0, 삭제/stash/force/reset0이다.

Python3.12.14/SQLite3.53.1/Linux이며 xcodebuild/swift는 없다. 기존25 Source/Bundle SHA와 DATA10_PROGRESS §1~2·관련 상태/검수·실제 엔진/DB를 대조했다. 추가 설치 없이 Cloud writer로 current25 전체 byte 재현을 먼저 확인했다. Mac의 과거142실행137PASS/5FAIL을 이번 Cloud의 실행/PASS로 복사하지 않는다. 실제 직전25는 새 불변 source.gz/DB fixture에 보존했다.

main protection 조회는 이번 토큰에서 HTTP403(Resource not accessible by integration)이어서 보호 없음으로 단정하지 않는다. rulesets=[]/Actions workflows0을 조회했다. 마지막 PR의 실제 필수 checks/mergeability와 정상 server merge를 확인하며 admin/force 우회하지 않는다.

### 3.2 실제 신규 콘텐츠·배치·문법 재사용

Content25→26, Schema4/reader7/UserProgress10 유지. 신규 상황60/내용이해60·받아쓰기60=120문제, Example60/Listening120/Question120·300UUID와 provenance source1개를 반영한다. 기존 source 재사용0, 신규 원문의 추가 참조60이며 문장·선택지·반복 source를 신규 원문으로 더하지 않는다. 감정8/의견8/판단7/이유7/결과7/경험8/계획8/의견차이7원문이다. 내용이해의 편집 초점12종은 핵심·세부·화자 의도·판단 근거·원인/결과·순서/조건/변화 등을 포함하며 전부 기존 comprehension 채점 엔진을 쓴다.

전체 Example4,873→4,933/Listening2,056→2,176/Question3,673→3,793/content_items16,241→16,541. V2,287/M2,420/G96/Course8/Lesson103은 불변이다. Listening은 入門34/初級79/初中級2,063, 전유형 의미50/한국어39/받아쓰기1,940/내용147이다. 새 learning_order2180~2299(batch109~114, 화면練習110~115),20문제씩6구간이다. 같은 원문의 두 유형은3구간 차이로 배치하고 기존 부분구간/순서/세션은 재작성하지 않았다. 기존 typed 목록의 실제 bounded SQL로120문항 모두 도달했다. 원문 단위 SRS 병합/새 topic UI는 구현하지 않았다.

DATA09 初中級54개 문법 모두에 자연스럽게 쓰인 형태와 기존 Grammar ID를 [용례표](Docs/DATA10_B_GRAMMAR_REUSE.json)에 기록했다. 필요조건/의무, 부사 대신/문법 -는 대신, 인용수혜자·추측과 확정·과거발견과 미래기대를 구분했다. 이는 편집상 실제 용례 재사용이며 새 grammar_examples/prerequisite·자동활용 지원 관계를 추가한 것은 아니다. 기존 Grammar endpoint/revision과163후보120해결/7조건부/36미해결(Level8포함)을 유지한다.

DATA10 누적120원문/240문제, 전체목표150~250/300~500 유지·남은30~130/60~260이다. 다음 Batch는 자동 시작하지 않는다.

### 3.3 언어 Self Review·중복·Transcript/채점

AI가60한국어/60일본어를 별도로 재독하고120prompt/해설/정답,180선택지,60정확한 accepted를 전수 확인했다. 각 객관식에 한국어 정답 근거와 두 오답 각각의 일본어 이유를 넣었고 a/b/c 정답은각20개다. [원고15필드 교정](Docs/DATA10_B_EDITORIAL_CORRECTIONS.json)과 공통 Dictation안내1곳을 수정했다. 후자는 실제 기존 채점이 허용하는 끝 .!? 생략을 정확히 안내하며 내부부호/철자/내용 차이는 허용하지 않는다. 채점 엔진·일반 ProductionAnswer·기존 질문은 변경하지 않았다.

기존4,873예문 전체(원래1,936TTS 및 A60원문 포함)와 B내 NFC/공백/종결부호 제거 한국어·한일쌍 완전 중복0. 가까운 후보는 bigram Jaccard 상위8→SequenceMatcher 상위3과 실제 문맥을 재독했다. 의미상 모든 paraphrase 부재나 외부 언어 품질 인증으로 표현하지 않는다. [실제60/120앱 payload](Docs/DATA10_B_ITEMS.md), [항목별 자체 검수](Docs/DATA10_B_SELF_REVIEW.json), [중복근거](Docs/DATA10_B_SIMILARITY.json).

전120항목은 한 화자의 시스템TTS, 녹음0이다. 보고/인용도 같은 음성의 연속 발화이며 다화자 녹음/서로 다른 목소리 재생을 가장하지 않았다. audio_asset_id/transcript_ko=null, source Example을 재사용한다. prompt_ko=null, transcript/번역/피드백은 기존 View의 result 이후에만 생성된다. 소스 검사를 실기기/VoiceOver 누출 검사 완료로 바꾸지 않는다. accepted는 정확한 원문1개씩이고 끝 .!?만 생략 가능하며 NFC/spacing/오답을 구분하는 기존 정책이다. 입력은100자 이하의2~3문장이고 실제3~10분 측정은 하지 않았다.

AI 자체 검수이며 독립 원어민·교사/전수 외부사전·실제 TTS 검청은 NOT TESTED다. Level은 내부 初中級 기준이고 공인 TOPIK·빈도·전문가 인증이 아니다. 외부 대본/녹음 복사0·자체 저작 provenance를 명시한다.

### 3.4 실제 검사·보존·미완료 gate

- 후보 전용9/9 PASS(18.647초). 최종 공통 안내 교정 후 후보9/9 PASS(19.094초). strict25→26 오류0/기존10경고, source25테이블68,586행·integrity ok/FK0. 전31테이블의 중복 포함 전행/schema/index·SHA 재구성 일치. 기존16,241개 fingerprint/payload/ID/revision/order/membership 보존, 기존99파일의 당시byte는 current25 source/DB snapshot과 나머지 실제파일로 보호했다.
- 처음 전체 시도는 live25 기대값의5FAIL 관찰 후 중단(exit130), 완료/PASS로 계산하지 않는다. 두 번째 전체382개는381PASS/누적delta기대값1FAIL(514.289초,errors/skip0,exit1). 실제26의 증가량으로 누적 기대값을 갱신했고 그 회귀1/1 PASS(7.166초), 쿼리6/6 PASS(0.086초)다. A exact24→25는 frozen25에 유지했다. 검사/Validator를 삭제·완화하지 않았으며 원시 초기 로그를 보존한다.
- 최종 Source SHA `012c199f219662b7832a84ef2f815307bd38ebb47e52ff6f31806dadbdd57d3f`, Bundle/재구성 SHA `47517c77f9dc02d3643000a8ce429cf7a655c2bddf45e5bf1f52b8e3fd9cd801`. 재구성 불일치0이다.
- **최종 portable382/382 PASS,578.139초,failures/errors/skipped0,exit0**. [전체 원시 로그](Docs/DATA10_B_PORTABLE_TEST_LOG.txt), [실제 결과](Docs/DATA10_B_TEST_RESULTS.json). 최종 입력 기준 전체를 재실행했으며 전용/targeted 수를 중복 가산하지 않는다.
- 새 portable9개는 strict/ID/전체행·중복·54용례·유일정답/오답근거·Offline bounded 조회·A snapshot/기존SRS/UserProgress·잘못된 accepted/Transcript/참조 거부를 검사한다. 임시 UserProgress/opaque JSON·SQL은 실제 개인 진도·Swift Codable·설정/Keychain 실행 인증이 아니다.
- 새 native1메서드(총143정의)는120문항/60source·정답/모든오답·Dictation/spacing/내부부호·played gate를 작성했다. 현재 Cloud build/XCTest 실행0/BLOCKED. 과거 Mac142실행137PASS/기존5FAIL(활용P1·구매cache·cohort/course 가정 등)과 DATA08 P1다섯 메서드 PASS는 역사기록으로 보존한다. 미수정 gate를 이번에 해결로 바꾸지 않는다.
- 실제 iOS/TTS·오디오중단/기기Offline/VoiceOver·메모리/즉시저장·Resume·광고/StoreKit은 BLOCKED 또는 미실행이다. 독립 사람/사전 NOT TESTED, Release B—Conditional 유지. 이번 runtime 코드 수정0이며 다음 단계는 시작하지 않는다.

### 3.5 Git 전달

실제 Source/Bundle/fixture·검수 원고·검사와 diff/파일크기를 확인한 후 일반 Commit/Push·main PR·필수 checks/mergeability 확인·정상 merge를 진행한다. Force Push·이력 재작성·기존 원본 삭제0. 최종 PR/merge SHA와 clean main=origin/main의 전체 SHA는 실제 Git/PR과 최종 응답을 기준으로 확인하며 자기 merge SHA 때문에 재귀 커밋하지 않는다. 다음 환경도 fetch 후 최신 main에서 시작한다.

### 3.6 Git/PR 전달 기록

검증한 콘텐츠/원고/검사/기록 commit `2c9fd5d7d7a0bc611f6105fdf2ec307160962e0b`를 `codex/data10-3-listening-batch-b`로 정상 push했고 [PR #20](https://github.com/Raccoon26/Project-Hangul-Study/pull/20)을 생성했다. GitHub 조회상 MERGEABLE, statusCheckRollup=[]이며 `gh pr checks --required`는 no checks reported(exit1)였다. 원격 CI PASS로 표현하지 않고 로컬382 PASS만 실행 근거로 삼는다. 보호 메타403을 우회하거나 admin/force merge하지 않으며 정상 server merge로 전달한다. 이 보충은 문서만 바꾸고 검증한 입력은 불변이다. 최종 merge SHA·상태·main=origin/main/clean 여부는 해당 PR/Git과 최종 응답이 기준이다. 다음 환경은 fetch로 최신 main을 받아 DATA10_PROGRESS §3와 남은 native/사람 gate를 먼저 확인한다.


## 4. DATA-10-4 / 最終 Listening Batch C (2026-10-21 JST)

### 4.1 시작 상태·실제 목표 대조

Cloud main/origin/main `a9ec0a450e1c40e0bd3b608ec2059499c27e762e`(PR20)을 fetch해 일치·clean/미커밋0을 확인했다. origin/gh Raccoon26·ADMIN/default main을 확인했고 `codex/data10-4-listening-batch-c`에서 작업했다. A60/120+B60/120의 실제 원문120/문제240, Content26의 Source/DB와 과거 기록을 대조했다. 원본26을 byte 그대로 source.gz/SQLite fixture에 보존하고 writer26 재현을 선행했다.

마지막 C60원문/120문제(내용이해60/받아쓰기60), 학교안내·직장안내·설명·비교·문제해결·의도 각10/20. 전체 **신규180원문/360문제**로 목표150~250/300~500을 충족한다. Content24 대비 새 Example180/Listening360/Question360 ID집합과 A/B/C 고정manifest의 일치를 확인했고 기존 듣기1,936/예문·추가참조·선택지·내부문장 중복 계산0이다.

### 4.2 승인 원본·배치·음성

Content27/Schema4/reader7/UserProgress10. 전체 V2,287/M2,420/E4,993/G96/Q3,913/L2,296/content_items16,841/Course8/Lesson103. Listening 入門34/初級79/初中級2,183, 전체 유형 meaning50/korean39/dictation2,000/comprehension207. 새 learning_order2300~2419(batch115~120)의6구간 각20문제로 실제 SQL 목록에서 도달했다. 기존 순서/부분구간/UserProgress·B session snapshot/SRS due/설정 opaque행을 보존했다. source 두유형은3구간 차이며 원문 단위 SRS 자동 병합을 구현하지 않았다.

신규120·전체2,296은 단일화자TTS/검증녹음0. 다화자 재생 가장0. prompt_ko=null, result 뒤 Transcript/번역/해설 생성. Dictation accepted는 원문1개씩, 끝 .!? 생략만 허용하며 내부부호/철자오류와 spacing warning을 구별한다. 기존 채점/일반입력·광고/구매·진도 런타임 변경0.

### 4.3 실제 검수·발견·수정

전60한국어/60일본어/120질문·해설·정답/180선택지/60accepted를 AI가 별도 재독했다. 한일 조사·활용·띄어쓰기·높임/시제/부정·범위·화자의도와 오답의 타당성을 대조했다. 후보 중133편집 이벤트/114고유필드를 교정했으며 Production133버그라는 뜻이 아니다. C09파일명 지시대상, 요청형/미수록 보조표현 단순화, C05/C23의 의미중복·부자연스러운 오답을 수정했다. 첫 후보8PASS/1FAIL 이후 정답근거 인용문 잔존을 전수 검색해 **C20/C49/C54 세 건**을 고쳤고 prepare의 literal근거/구별 선택지 gate를 보강했다. 승인 전 기존 Production 변경0·UUID 재발급0. 초기도구의 version assertion/어휘컬럼 오류도 수정했으며 초기 실패를 PASS로 기록하지 않는다.

기존4,933예문과 Batch내 완전중복0. 근접180후보를 실제 재독하고 공통어구와 새 문맥을 구분했다. 원문은2문장/38~63자/평균48.9자. 기존Grammar40개에 대한60선택참조·Vocabulary literal receipt를 남겼지만 lexical-only2/변형·확장3개를 구분했고 모든 토큰/부수문형의 선행 숙달을 인증하지 않는다. 원래163건120해결/7조건부/36미해결(Level8포함)과 Grammar ID/revision/관계 불변. 독립 원어민/교사·전수 외부사전·실제TTS 검청은 **NOT TESTED**다.

[전수 payload](Docs/DATA10_C_ITEMS.md), [AI검수](Docs/DATA10_C_SELF_REVIEW.json), [교정](Docs/DATA10_C_EDITORIAL_CORRECTIONS.json), [중복](Docs/DATA10_C_SIMILARITY.json), [선행/한계](Docs/DATA10_C_PREREQUISITES.json), [전체보고](Docs/DATA10_C_REVIEW.md).

### 4.4 검사·보존·잔여 gate

후보 첫9개8PASS/1FAIL(17.332초), 두 번째도1FAIL(18.016초,쓰기 전 중단으로 수정 미반영), 세 번째9PASS(17.383초), 최종 선택지 다듬기 후9/9PASS(18.145초). 초기 로그를 보존한다. 최종 portable **391/391 PASS (466.416초, failures/errors/skipped0, exit0)**. Source25테이블69,787행/31테이블 전체행·schema/index/byte SHA 재현 일치, strict previous26 오류0/기존경고10·integrity ok/FK0. 기존16,541개 fingerprint/ID/revision/payload/order/membership 및103기존파일 byte 보존, 신규300UUID/기존revision변경0.

Source SHA `88e9599648182e2fd4372eecb738da60321913632cae32e0e25922048f5aef8b`, Bundle/재구성 SHA `a937df17bfb88b69504811048c2660086af174dc7633d04f852a3ce10236b48c`. 재구성 불일치0. B25→26 정확한 gate를 frozen26으로 고정했다. 신규C portable9개/실제 native1개를 추가했으며 native는 현재144정의·실행0/BLOCKED. 후보/별도검사를 전체 고유 수에 중복 가산하지 않는다. [결과](Docs/DATA10_C_TEST_RESULTS.json), [원시 전체로그](Docs/DATA10_C_PORTABLE_TEST_LOG.txt), [수량/보존](Docs/DATA10_C_COUNTS.json).

SQLiteListening bounded warm120조회/2,400행 median0.294ms/max12.188ms. Python/SQL로 실제 iPhone cold실행·RAM·음성·3~10분·저장/Resume를 검증한 것은 아니다. 현재Cloud Xcode/Swift없음·iOS Build BLOCKED, 이전Mac142실행137PASS/5FAIL(활용P1·cold Purchase cache·cohort/course 가정) 미해결 유지. 독립 사람/TTS·기기Offline/VoiceOver·광고/StoreKit 실제 권한 gate는 남고 **Release B—Conditional**이다. 이번 런타임 수정0/기존 gate 해결0.

### 4.5 Git 전달

일반 commit/push·main대상PR·필수 checks/mergeability 확인·정상merge 후 fetch/ff-only하여 main=origin/main 전체SHA와clean을 확인한다. Force Push/원본삭제/이력재작성0. 접근 가능한1,028blob과 현재파일 모두50/100MiB초과0·현재최대20,025,344bytes로 LFS는 불필요하다. main protection 조회403은 보호없음으로 해석하지 않으며 rulesets=[]/Actions workflows0은 CI PASS가 아니다. 최종 PR·merge SHA는 Git/PR과 최종 응답이 기준이다. 이번 마지막 Batch에서 종료하고 후속 단계는 자동 시작하지 않는다.


### 4.6 실제 Commit/Push/PR 전달

검증한 원본/Bundle/fixture·원고·검수/회귀/기록 commit `dd247c92119867cf3408b4e6f57005348cf62677`를 `codex/data10-4-listening-batch-c`로 정상 push했고 [PR #21](https://github.com/Raccoon26/Project-Hangul-Study/pull/21)을 생성했다. 원격 head와 local commit이 일치한다. PR 조회는 MERGEABLE/CLEAN·statusCheckRollup=[]이며 `gh pr checks --required`는 no checks reported(exit1)였다. CI PASS라는 뜻은 아니며 실제 검증은 portable391PASS/strict·byte재현/AI검수 범위다. 보호메타403을 보호없음으로 해석하거나 admin/force로 우회하지 않는다. 이 보충은 문서만 변경하고 검증된 Source/Bundle/테스트를 바꾸지 않는다. 보충commit push 후 최신 head를 다시 확인해 정상 merge하고, main fetch/ff-only·origin/main 전체SHA/clean을 대조한다. 최종 merge SHA·상태는 PR/Git과 최종 응답이 기준이며 자기 SHA를 위한 사후commit을 반복하지 않는다. 이 마지막 Batch에서 종료한다.


## 5. DATA-10-5 / Listening·Dictation 전체 QA (2026-10-21 JST)

### 5.1 시작 상태와 검수 범위

main=origin/main `f7d1835a8ce1b073a65e8a21d8b27f6e4eb523a9`(PR21)을 fetch해 일치·clean·미커밋0을 확인하고 `codex/data10-5-listening-qa`에서 작업했다. gh Raccoon26/ADMIN/default main·origin, 상태/가이드/출시/AGENTS/누적 기록과 실제 Source/DB/View/모델/Audio/Reader/Validator를 대조했다. Python3.12.14/SQLite3.53.1/Linux, Xcode/Swift 없음. 기존27을 byte 그대로 재구성한 뒤 실제 원본/DB를 불변 fixture에 보존했다.

A~C **180한국어·180일본어/360문항·해설·정답/630선택지/150accepted 전수 AI 별도 재독**. 자연스러움·활용·조사·띄어쓰기·Level·높임·시제·범위·인용 수혜자·화자 의도·정답 유일성/오답 타당성·반복/선행 문법을 확인했다. batch별6개씩 무작위18원문 재감사와 고위험 집중 검토, 기존 Level별4개씩12원문/근접4쌍의 추가 AI 표본을 구분한다. 독립 사람·교사/전수 외부사전·실제TTS 검청 **NOT TESTED**, 검증 녹음0 유지. 기계 Validator는 언어·교육 타당성 인증이 아니다.

[전체QA보고](Docs/DATA10_QA_REVIEW.md), [실제180/360 payload](Docs/DATA10_QA_ITEMS.md), [AI원장](Docs/DATA10_QA_EDITORIAL.json), [별도표본](Docs/DATA10_QA_SAMPLES.json), [선행 검토](Docs/DATA10_QA_PREREQUISITES.json), [기존 기계분석](Docs/DATA10_QA_CORPUS_ANALYSIS.json), [기존 언어표본](Docs/DATA10_QA_OLD_SAMPLES.json).

### 5.2 재생 전 UI·VoiceOver 노출과 안내 수정

**QA-UI01/P1**: 기존 선택지는 재생 전에도 Text를 생성하고 disabled만 해 정답 문장/번역을 미리 읽을 수 있는 구조였다. `s.revealsChoices`의 heard/result/current/task 조건 아래에서만 보기를 생성하도록 고쳤다. result 뒤 Transcript/번역/정답/해설, 들은 뒤 Resume의 heard=true·다음 문항의 heard=false를 유지한다. 계산 속성만 추가해 Codable 저장 필드/UserProgress 변경0이다. 실제 VoiceOver로 관찰한 결과가 아니라 소스에서 발견·수정한 구조이며, 정적 회귀 PASS와 native 동적 확인 **BLOCKED**를 구분한다.

Audio 성공 시에만 완료 카운트를 올리고 stop/실패/화면 종료 시 미완료로 남는 경로, 오류 문구·접근성 라벨을 점검했다. 전체2,296 prompt의 전체 원문/번역 exact 포함0은 기계 확인이며 의미상 모든 힌트 부재의 증명은 아니다. 질문은 재생 전에 볼 수 있다. **QA-UI02/P2**: `句点は不要です`를 문중 부호 필수/문말 ASCII .!? 생략이라는 실제 계약으로 바꿨다.

### 5.3 언어·문항 교정과 accepted

언어/문항10유형을 교정했다. A13 취소/대안의 일본어 범위, A23 미수록 -더라도→기존 -아/어도, A27 근거 없는 二人 전제, B06 형/부모님의 인용 역할, B21 편이다의 경향/추측, B30 건조/안전확인의 정답 범위, B47 잠정 의향 해설, B53 싶냐고의 잔존 설명, B56 -기보다는→-는 대신, B57 일본어 수동태/비난 의도 과잉 설명이다. [명시 before/after](Content/data10-final-corrections.json).

현행 Validator는 canonical 원문/끝부호 변형만 허용하므로 `두 시/2시` 같은 숫자 변환은 미지원이다. 신규150prompt에 숫자도 한글로 쓰도록 명시했고 Validator/일반 입력 채점을 완화하지 않았다. accepted는 정확한 원문1개씩이며 한국어가 바뀐3항목도 맞췄다. 문중 부호·단어·철자는 오답, spacing은 별도다.

총188본문 필드/175payload ID·179revision+1(종속 Listening revision-only4포함), 신규/삭제ID0이다. 정답 choice ID/순서·관계·배치·기존 UserProgress는 그대로다. 공통 안내150개를150개의 서로 다른 제품 버그로 세지 않는다.

### 5.4 기존1,936과 교육적 경로·남은 선행 조건

기존 TTS1,936(고유source1,936)은 의미32/한국어27/받아쓰기1,850/내용이해27, 入門34/初級79/初中級1,823이다. 받아쓰기95.558%, 初中級 중1,822개가 받아쓰기다. 신규360은 source180·내용180/받아쓰기150/의미18/한국어12, 합산2,296/source2,116·받아쓰기2,000(87.108%)/내용207/의미50/한국어39다. 기존 원문8~35자/평균21.745, 신규36~78자/평균52.444, 전단일화자TTS·검증 녹음0이다.

완전 source+task 중복0, 신규 전체 원문/문장 조각 반복0이다. 기존 예문과 겹치는 한 조각 `금방 돌아올게요`는 A51 전체 맥락과 구분했다. 기존 근접4쌍 중 돌아보며/되돌아보며는 의미가 가까운 어휘별 예문, 나머지3쌍은 장소·형용사·부사의 최소대립이다. ID를 합치거나 삭제하지 않았다. 기존1,936개 언어를 전수 재검수했다고 주장하지 않는다.

기존 Grammar 선택참조180/고유77ID와 B의54관찰 형태를 현재 본문과 대조했으나 미수록/변형12계열·27원문은 사전 설명/교사 확인이 필요하다. 기존163후보 모두 기존 듣기 source에 포함되며120해결/7조건부/36미해결(Level우려8포함)을 유지한다.

[권고 경로](Docs/DATA10_QA_LEARNING_PATH.md)는 기존96Grammar/初中級3코스18레슨6Unit 복습→A103~105/B109~111/C115~117 내용이해→결과 후 사전/문법·기존 단문 보충→다음 기회에 A106~108/B112~114/C118~120의 두 번째 과제다. 20문항 상한·부분 중단/Resume를 유지하며 실제3~10분 완료를 보장하지 않는다. 새 추천/주제UI·선행 자동 잠금·원문SRS 병합·듣기Favorites를 구현한 것이 아니다. 현행 Favorites는 Vocabulary/Grammar만 지원한다.

### 5.5 버전·보존·실제 검사

Content28/Schema4/reader7/UserProgress10. 전체 V2,287/M2,420/E4,993/G96/Q3,913/L2,296/content_items16,841/Course8/Lesson103 불변, DATA10 신규180/360·목표150~250/300~500 충족 유지. 기존27의08:00:00Z batch stamp는 실제 QA 시각보다 미래인 메타데이터로 보존했다. created_at을 고치지 않고 이번 revision metadata는 단조 후행08:00:01Z를 사용했으며 실제 QA 시각은 별도 recorded_at_utc다.

A/B/C exact gate는25/26/27fixture에 고정, final27→28이 명시188필드/179revision만 허용한다. 기존106파일 byte·원본/fixture 보존, Source25테이블69,787행/DB31테이블 schema/index·중복 포함 전행·byte SHA 재구성 일치, strict previous27 오류0/기존10경고·integrity ok/FK0. 기존1,936의 E/L/Q fingerprint 및 모든 Stable ID/kind/created_at/순서가 보존됐다.

최초 후보12개는10PASS/1FAIL/1ERROR(28.969초). 검사 코드가 문중 마침표만 가정해 `?` 경계를 놓쳤고, Favorites에 미지원 listening 유형을 넣은 fixture 오류가 있었다. 문중 .!? 경계와 지원 Vocabulary favorite로 고쳐 규칙 완화 없이 최종 후보12/12 PASS(29.605초,exit0). 초기 로그를 보존한다.

새 portable12개는 strict/명시delta·전체 행·교정 회귀·150accepted·UI 생성/guard 제거 거부·숫자/동의어/누출/중복/미증가revision 거부·이전1,936 불변·실제360 offline bounded 조회·27→28디스크 교체/SRS due/기존Favorites/사용자byte·선행/AI범위를 검사한다. Python/opaque SQL JSON은 Swift Codable/실기기 인증이 아니다.

최종 전체 portable **403/403 PASS (477.897초, failures/errors/skipped0, exit0)**. Source SHA `521f047d3bb9fbb4056c651c6d6e561d18db79f3072f2f46acf6a76ff447ba36`, Bundle/재구성 SHA `a9f1f5459597203d07a62a6a70fdf41db5f77b943c29e45ea5921c9c503ba8ad`. [원시 로그](Docs/DATA10_QA_PORTABLE_TEST_LOG.txt), [실제 결과](Docs/DATA10_QA_TEST_RESULTS.json), [수량/보존](Docs/DATA10_QA_COUNTS.json). 추가 native1메서드·현재145정의/실행0, Xcode/Swift가 없어 iOS Build/XCTest·실제 UI/VoiceOver **BLOCKED**다. 이전 Mac142실행137PASS/5FAIL·활용P1/구매cache/cohort/course 가정은 미해결이다. 새 노출P1은 코드수정/정적PASS·native 확인 대기다. 독립 사람/TTS·기기Offline/음성중단/접근성/메모리/IME/3~10분·실제 광고/구매 권한은 미완료, **Release B—Conditional**·검증 녹음0을 유지한다.

### 5.6 Git 전달

diff·원본/fixture·대용량을 확인하고 정상 Commit/Push/main PR·필수 검사/mergeability를 확인한다. 이전 사용자 위임/AGENTS에 따라 정상 병합 후 fetch/ff-only로 main=origin/main·clean을 대조한다. 최종 PR/merge SHA는 Git/PR과 최종 응답이 기준이다. 접근 가능한1,078blob·현재파일의50/100MiB초과0, 최대20,037,632bytes로 LFS는 불필요하다. main protection API403을 보호없음으로 해석하지 않으며 rulesets=[]/Actions workflows0은 CI PASS가 아니다. Force Push/이력 재작성/기존 원본 삭제0, 자기 SHA를 위한 재귀 commit은 하지 않는다. 이번 QA에서 종료하며 다음 단계는 시작하지 않는다.


### 5.7 실제 Commit/Push/PR 전달

검증된 코드·교정 Source/Bundle·fixture·검수/검사 기록 commit `6cd189ecb9c0941d21169d63ad368bf2d69d4d0b`를 `codex/data10-5-listening-qa`로 정상 push했고 [PR #22](https://github.com/Raccoon26/Project-Hangul-Study/pull/22)을 생성했다. ls-remote/PR의 head와 로컬 commit이 일치한다. PR은 MERGEABLE/CLEAN·statusCheckRollup=[]이며 `gh pr checks --required`는 no checks reported(exit1)다. 원격 CI PASS가 아니라 로컬403PASS·strict/byte재현·정적회귀/AI검수 범위가 실행 근거다. 보호메타403을 보호없음으로 해석하거나 admin/force로 우회하지 않는다. 이 인계 보충은 문서만 바꾸고 검증된 Source/DB/코드/테스트는 불변이다. 이전 위임에 따라 보충commit을 정상 push한 후 최신head를 확인해 정상 병합·main fetch/ff-only와 origin/main 전체SHA/clean을 대조한다. 최종 merge SHA·상태는 해당PR/Git·최종응답을 기준으로 하며 자기SHA를 위한 재귀commit은 하지 않는다. DATA10-5 QA에서 종료하고 다음 단계는 시작하지 않는다.


## 6. DATA-10-6 — Listening/Dictation Production·Curriculum 통합 (2026-10-21)

### 6.1 시작 상태와 버전 보존

최신 main/origin/main `d76f0b89c38c892005de68aef206229234d141c9` clean·ahead/behind0/0, 지정 remote·ADMIN·기본 main을 확인하고 `codex/data10-6-listening-integration`에서 시작했다. Content28/Schema4/reader7/UserProgress10·전180원문/360문항 QA 기록이 실제 기준이다. 실제 직전28 source.gz/DB를 신규 불변 fixture로 보존했고 과거110개 Source/Resources/fixture 파일 byte를 대조했다. Source25테이블69,787행·DB31테이블의 변경 전28도 strict previous27로 SHA까지 재현했다.

처음 writer 설치는 Python 설정이 없는 clang을 선택해 실패했다. 설치된 GCC14의 CC/LDSHARED override를 새 격리 디렉터리에 적용해 SQLite3.53.1/STAT4 없음·기존 동일 writer profile을 구성했다. 시스템 Python/DDL/Validator/통계 배치를 수정하지 않았다. [환경](Docs/DATA10_INTEGRATION_ENVIRONMENT.json), [변경 전 strict 재현](Docs/DATA10_INTEGRATION_PREFLIGHT28.json), [writer 정책](Docs/DATA10_WRITER.md).

후보 Content29를 /tmp에 준비해 strict `--previous content-v28-production.sqlite --production` **오류0/기존경고10**을 통과했다. Schema4/reader7/UserProgress10 유지. 경고는 기존 한 글자 발음 예문5개·동형 표제어 후보5개로 신규 경고0이다. 기존27 미래 stamp를 보존하고 metadata 단조 후행08:00:02Z를 사용했으며 실제 시간은 별도 recorded_at_utc다. 다음 실제 변경은29를 먼저 보존한다.

### 6.2 실제 배치·원문 참조와 수량

신규 원문/문항 추가0, DATA10 누적 **180고유원문/360문항**·전체 목표150~250/300~500 충족 유지. 기존 원문 ID를 재사용하는 **3코스/72레슨/6Unit, 각5문항**을 추가했다. A/B/C 각24레슨이며 내용이해12개 후 별도 기회에 두 번째 과제12개를 배치한다. 같은 원문의 두 과제를 같은 레슨에 넣지 않았다. 기존103레슨·코스0~7·learning_order·20문항 배치103~120/부분 구간·session snapshot/선택지 순서·Vocabulary set membership 변경0이다.

신규 stable UUID81개는 고정 manifest에 발급 후 보존했다. lesson membership360·원문별 기존Grammar1개와Vocabulary1개(각180관계/고유77·130)를 추가했고 모든 관계 끝점 **747개**(L360/E180/G77/V130)만 승인 목록에 따라 revision+1/updated_at 갱신했다. 본문·정답·선택지/accepted 변경0, ID 삭제0이다. [고정 배치/관찰 형태](Content/data10-integration-ids.json), [승인revision](Content/data10-integration-revised-ids.json).

전체 **Vocabulary2,287 / Meaning2,420 / Example4,993 / Grammar96 / Question3,913 / Listening2,296 / Course11 / Lesson175**, source25테이블 **70,823행**, SQLite31테이블이다. level 분포와 전체 source/DB 행·schema/index·重複포함 byte 대조는 [수량/보존](Docs/DATA10_INTEGRATION_COUNTS.json)에 있다. 신규81개 배치 entity/360관계를 원문·문항 수로 합산하지 않는다.

初中級 Vocabulary1,181 / Example2,757 / Grammar54 / Question3,564 / Listening2,183. 入門306/659/22/156/34, 初級800/1,577/20/134/79, 한글 문항59개다. 모든 듣기 단일화자TTS/검증녹음0, 실제검청·독립 사람 NOT TESTED 유지.

### 6.3 실제 엔진·Resume·정답 공개 경로

Curriculum 初中級→듣기/듣기 Catalog→단계별 목록에서 전용 코스에 접근한다. `listeningCourses/listeningLessonIDs`가 기존 Course/Lesson 테이블을 읽고 ListeningStudyView/기존 ListeningSession 엔진에5문항을 전달한다. 일반 courses/curriculum lessonIDs에서 typed grammar/listening 레슨을 제외해 지원하지 않는 LessonStep kind 경로를 막았다. generic 初中級47레슨은 이전대로다.

해답 판정 후에만 Example learning_point_ja와 Grammar/Vocabulary 사전 링크를 생성한다. 기존 Grammar 학습·퀴즈/SRS, Vocabulary 회독/활용/문장 생성·Search/Favorites 화면을 재사용한다. 선택지·Transcript·번역/정답의 재생 전 노출 guard는 유지했다. 새로운 문항 유형·강제 선행 잠금·Listening Favorites/Transcript 검색은 추가하지 않았다.

새 scope `lesson:lower_intermediate:<stable lesson UUID>`의 Home Resume 파싱/lessonID 복원, active snapshot 우선 로드, membership 순서로 snapshot 구성을 연결했다. ContentVersion·choice order·heard·feedback·retry/position·기존 SRS due를 갱신 콘텐츠로 덮어쓰지 않는다. 같은 Listening ID/skill PK1개이며 두 task의 같은 source에 SRS2개가 생기는 기존 정책을 유지한다. retry를 first-pass 정답/SRS 승급으로 세지 않고 nonreview 재연습으로 due를 초기화하지 않는다.

재생완료·판정·다음 이동은 기존 transaction 즉시 저장을 사용한다. SQL에서 partial/완료 구분·retry 집계·중복PK/rollback·Resume를 확인했다. 미제출 입력 초안은 기존 @State뿐이라 화면/프로세스 종료 후 영속 복원되지 않는 **P2 한계**를 별도 기록한다. 판정·학습 위치 저장과 구분하며 초안 저장을 완료로 표시하지 않는다. 실제 background 복귀·audio interruption/stop/normal/slow·VoiceOver/IME·기기3~10분은 BLOCKED다.

### 6.4 검증 범위·발견/수정·성능

**INTEGRATION-L01/P2 수정**: A41의 머리 참조는 사전 기본 뜻「頭」를 표시하지만 원문은 머리카락 자르기 문맥이다. 같은 기존 어휘의 머리카락 의미까지 변경하는 대신, 명확한 기존 동사 `자르다 / 切る`(관찰형 자르지)로 새 참조만 교정하고 회귀 assertion을 추가했다. 원문·기존 어휘/뜻/ID는 보존했다. 최종28→29 후보를 다시 생성해15/15 PASS(21.958초) 후 반영했다.

전용 candidate 최초15개는14PASS/1FAIL(21.829초): 검사에서 Grammar용 question_target 관계를 듣기에 가정했다. 실제 듣기 FK인 questions.listening_id를 검사하도록 바로잡았으며 데이터/Validator 완화0이다. 최종 **15/15 PASS(21.958초)**. [최초 로그](Docs/DATA10_INTEGRATION_CANDIDATE_INITIAL.txt), [최종 로그](Docs/DATA10_INTEGRATION_CANDIDATE_FINAL.txt).

전용 검사는 실제28 freeze/strict29 결정적 재현·81새ID/747승인fingerprint·기존본문/배치 보존·3/72/360 도달·180G/180V 형태/참조·old1936와 새원문 구분·기존20문항 번호·전체사용자SQLite byte/snapshot/due/즐겨찾기/설정/통계/Resume·새scope와partial/완료/retry집계·SRS PK/rollback·해답후context/Audio guard정적·150canonical accepted·거부검사·network차단SQL·monetization/migration source불변을 포함한다. Python SQL/opaque JSON/정적검사는 Swift actor/Codable/실제UI 실행이 아니다.

전체 최초 실행418개는414PASS/1FAIL/3ERROR(552.020초,exit1)였다. 코스 전체 기대값8→11은 기존8개 제목/순서를 보존하면서 승인된3개를 뒤에 추가하도록 갱신했다. 전체 portable 최초 실행에서 구검사3개 오류를 발견했다. 2개는 '파일 첫 SQL=듣기 조회' 가정, 1개는 examples 조회를 UserProgress DB로 분류한 오류였다. 실제 SQL prefix/repository extension으로 query·DB를 선택하고 multiline SQL 준비 검사도 보강했다. 초기 로그를 보존한다. 최종 전체 portable **418/418 PASS (544.580초, failures/errors/skipped0, exit0)**. strict previous28·전체31테이블/Source70,823행/schema/index/byte 재현 PASS, iOS Build/XCTest/Simulator BLOCKED·독립 사람/TTS 검청 NOT TESTED를 구분한다. native3개 메서드 추가(현재148정의/실행0): 모든360실제문항/180참조, 5문항세션 cold Resume/ContentVersion보존/CAS/retry/반복연습due, 실제dictation 채점을 작성했다. Xcode/Swift exit127로 Build/XCTest/Simulator **BLOCKED**다.

[40회 warm SQL 측정](Docs/DATA10_INTEGRATION_PERFORMANCE.json): network socket 금지·이전28/현재29 search/catalog/curriculum과 현재 Home/SRS/Resume/5문항/통계/유지학습을 실행했다. search p95 0.8127→0.8156ms, 3코스1.2672ms·5문항0.0577ms·Home0.2965ms·SRS20개0.1704ms. 실제 Swift 생성·UI startup·RAM·학습3~10분 인증은 아니다. DB20,037,632→20,279,296bytes, 소량 지연 차이의 OS noise를 고려하고 원시 값을 그대로 보존한다.

### 6.5 남은 gate / Release B—Conditional

이번은 기존180개 한일 언어 QA를 보존하고 새참조180G/180V·코스 문구·불규칙 관찰형을 AI로 재확인한 통합 단계다. 독립 원어민·교사/외부 사전·TTS 검청 NOT TESTED, 검증녹음0이다. 기존163후보120해결/7조건부/36미해결(Level8), 신규12계열/27원문의 사전 설명/교사 확인 필요는 참조 배치만으로 해결되지 않는다.

이전 Mac142실행137PASS/5FAIL(되다/뵈다 활용 P1·StoreKit cold cache 원인미확정·cohort/course 가정 실패)을 유지하고 이번 Cloud 실행으로 덮어쓰지 않는다. DATA10-5 노출P1은 코드/정적PASS·실제VoiceOver대기, 이번 새runtime P0/P1 재현0은 전체앱 무결성 보장이 아니다. 판정 전 입력 초안 영속화P2·실기기 audio/interrupt/offline/background/IME/VoiceOver/Dynamic Type/RAM/실제3~10분·실제 AdMob/StoreKit 권한은 미실행이다. monetization/migration 파일 byte불변·정적검사/SQLite보존을 실제 권한 복원 PASS로 주장하지 않는다. **Release B—Conditional**.

[통합 상세/재현](Docs/DATA10_INTEGRATION_REVIEW.md), [실행 결과](Docs/DATA10_INTEGRATION_TEST_RESULTS.json). Production 원본/번들/모든과거fixture 추적을 유지하고50/100MiB크기를 확인한 후 정상 Commit/Push/PR/필수체크/mergeability·병합·main동기화를 수행한다. Force Push/이력 재작성/원본삭제0. 최종 Git/PR/SHA는 다음 전달 기록과 Git/PR·최종응답을 따른다. DATA10-6에서 종료하며 다음 단계를 시작하지 않는다.


### 6.6 최종 자동 검사와 Git 사전 점검

최종 전체 portable **418/418 PASS (544.580초, failures/errors/skipped0, exit0)**. strict previous28·전체31테이블/Source70,823행/schema/index/byte 재현 PASS, iOS Build/XCTest/Simulator BLOCKED·독립 사람/TTS 검청 NOT TESTED를 구분한다. [원시 최종 로그](Docs/DATA10_INTEGRATION_PORTABLE_TEST_LOG.txt), [원시 최초 실패 로그](Docs/DATA10_INTEGRATION_PORTABLE_INITIAL.txt), [검사 원장](Docs/DATA10_INTEGRATION_TEST_RESULTS.json). 최초 FAIL을 지우거나 후보/전용 검사 수를418개에 중복 합산하지 않는다. 변경 전28 및 최종29의 별도 strict 재구성과 byte 비교, 110개 과거 파일 보존, 전체 행·참조를 확인했다.

[Git 크기 사전 점검](Docs/DATA10_INTEGRATION_GIT_SIZE.json): 접근 가능한1,129blob/현재 보호 경로의50·100MiB 초과0, 현재 최대20,279,296bytes, 원본·번들·fixture 추적 유지. LFS 불필요·force push/이력 재작성0. 보호 API403은 권한 제한이며 보호없음으로 해석하지 않는다. rulesets=[]/Actions workflows0은 원격 CI PASS가 아니다. 최종 PR의 checks/mergeability와 정상 병합·main 전체SHA/clean을 별도 확인한다.


### 6.7 실제 GitHub 전달

검증된 Source/Bundle·불변28fixture·코스/참조·runtime/회귀·기록 commit `638d46a256344bae543368c90d21dd0498dea864`를 `codex/data10-6-listening-integration`에 일반 push했고 [PR #23](https://github.com/Raccoon26/Project-Hangul-Study/pull/23)을 생성했다. ls-remote/PR head와 로컬SHA 일치, main 대상 MERGEABLE/CLEAN·statusCheckRollup=[] 확인. `gh pr checks --required`는 no checks reported(exit1)로 원격 CI PASS가 아니다. 실행 근거는 로컬418PASS·strict/전행/byte 재현·정적/SQL/AI검수이며 Native/사람 gate는 유지한다.

이 인계 문서 보충은 검증된 코드/Source/Bundle/테스트를 바꾸지 않는다. 보충commit을 정상 push하고 최신head/checks/mergeability를 다시 확인한 후 기존 위임/정책에 따라 admin/force 우회 없는 정상 병합을 수행한다. 이후 fetch/ff-only로 main=origin/main 전체SHA/clean 및 배포 Source/Bundle hash를 확인한다. 최종 merge SHA와 상태는 Git/PR·최종 응답이 기준이며 자기SHA를 기록하려고 문서commit을 반복하지 않는다. DATA10-6에서 종료하고 다음 단계는 시작하지 않는다.

## 7. DATA-10-7 — Mac Native Full Regression (진행 중, 완료 아님)

### 7.1 시작과 보존

2026-10-21 Mac 로컬에서 명시 요청에 따라 시작했다. 지정 origin `Raccoon26/Project-Hangul-Study`, 인증 Raccoon26/ADMIN/기본 main, fetch 후 main/origin/main `59d3bc7636c2b22ce7a0e21899fa1deeb2bbfedb`·ahead/behind0/0·미커밋0을 확인하고 ff-only 후 `codex/data10-7-native-regression`을 생성했다. 현재 Content29/Schema4/reader7/UserProgress10·Source/배포DB·Stable ID/114개 보호 경로의 시작 SHA를 외부 작업 디렉터리에 기록했다. 이번 코드 회귀 작업에서 Production 교체·콘텐츠 버전 증가는 하지 않는다.

AGENTS/PROJECT_STATUS/CONTENT_GUIDE/DATA_PROGRESS/RELEASE_CHECKLIST/DATA08/09/10 원장과 DATA08/09 시스템 감사, DATA10 native findings·QA·통합 기록, DEV13/14의 Known Issues/부분 구현을 대조했다. 상위 신규 과정/전문 녹음/전체 자유작문/새 적응형 scheduler는 기존 범위 공백이며 이번 버그 수정으로 새로 구현한 것으로 주장하지 않는다. 기존 native 실패·실제 활용 오류·구매 cache·입력 초안 소실과 현재 모든 엔진의 실제 저장/복원을 우선 검증한다.

Xcode27.1(27A9275), macOS27/arm64/8GiB. 공식 고정 GoogleMobileAds13.11.0/UMP3.1.0 resolve 성공. 실제 iPhone 연결0, 새 작업용 iOS26.0.1 iPhone17Pro Simulator를 생성했다(기존 기기 erase/삭제0). Mac 기본 Python3.11.6/SQLite3.44 STAT4는 그대로이며 별도 `setup_exact_writer.py`로3.53.1 writer를 준비했다. 현재29→임시출력 strict previous28 오류0/기존10경고·배포DB byte/SHA `228d5572391d4c56509f83c57415c9b76b69c82ce2e7e48ebea82af97630b4af` 일치를 확인했다.

### 7.2 최초 native 재현과 수정 순환

수정 전 실제 최신148 XCTest **실행148/통과142/실패6/skip0**, 정상 exit65·봉인 xcresult. 930 assertion 실패는 대부분 발음 테스트가 Vocabulary 코스를 고른 결과이며930개 앱 버그로 세지 않는다. 기존5메서드 실패와 DATA08 전체 듣기 수량의 과거 가정1개가 추가됐다. 초기 실행 로그/xcresult 요약을 최종 보고에 보존한다.

1. 활용 P1: ㅚ/ㅙ medial index를 잘못 매핑해 되요/됬어요/되서·뵈요/뵜어요/뵈서를 생성했다. ㅚ→ㅙ·기존ㅙ 유지로 수정하고 기존 꿰다 과거 기대값의 ㅝ 오기를 ㅞ인 뀄어요로 교정했다. 한국어기초사전 되어(돼)·뵈어(봬)·꿰어(꿰)를 근거로 사용하며 전체 언어 검수로 확대하지 않는다. 현재85개 -되다 실제 사전 present/past/future와 전1,227 authored 입력문항을 확인하는 native 회귀를 추가했다.
2. 구매 cache: Keychain OSStatus를 버리던 처리를 명시 결과(없음/저장된 verified/접근·해독 실패)로 구분했다. 접근 실패를 free로 판정하지 않고 광고를 차단한다. 검증 거래만 cache에 쓰며 실패를 일본어로 안내한다. 실제 Keychain insert/update/cold read/delete와 실패 상태 회귀를 추가했고 unsigned Simulator의 기존 cold cache 실패는 정상 ad-hoc 서명 비교로 원인을 확인한다. 아직 재검사 전이므로 구매 PASS로 표시하지 않는다.
3. 오래된 테스트 cohort: DATA06의80 stable ID registry로 정확한 원배치를 확인하고 후속 DATA07도 validate한다. 발음 코스는 고유 ID로 조회한다. DATA08의1,821 고정 받아쓰기 검사를 유지하면서 전체 pagination은 현재 active DB ID 집합과 대조한다. 수량을 임의로 바꾸거나 데이터를 축소하지 않는다.

현재 관련 native 재검사 및 portable 실행 중이다. UI 도구는 Simulator 이름/경로/bundle 연결 실패·Xcode 접근 timeout을 반환했다. 실제 XCUITest 화면 대체 검증을 준비하며 수동/기기 UI PASS로 꾸미지 않는다. 전체 Debug/Release/device architecture·전체 native/portable·핵심 E2E와 문서/PR/병합은 아직 완료하지 않았다. DATA10-8/11은 시작하지 않는다.


### 7.3 2026-10-22 재개·UI 회귀 순환(아직 최종 완료 아님)

fetch 후 기준 main SHA 불변, 기존 단계 변경을 보존하여 같은 브랜치를 이어간다. 첫 전체 `sh Tools/verify.sh`에서 portable418/418 PASS(984.232초)·SDK resolve/Debug Simulator/Release Simulator/unsigned Release 기기 아키텍처 Build PASS, native155/155 PASS·UI11 중7 PASS/4 FAIL(전체166 중162 PASS/4 FAIL/skip0, exit65)이다. 최종 전체 PASS로 표시하지 않는다.

추가한 native7회귀는 활용85개/출제1,227개/ㅎ 사전 네 항목·실제 signed Keychain·cache fail closed·초안 cold/legacy/late-write/재시도·observer 해제를 검사한다. 미제출 초안 optional JSON을 추가했으며 schema/ID/Production114파일은 불변이다. 원래 엔진/Validator/일반 답안 정규화를 유지한다. DATA08 P1 관련 native 다섯 메서드도 전체 검사에 포함되어 PASS했다.

실제 XCUITest로 회독20어휘→2회독/완료·Grammar→퀴즈→SRS·사전 활용/즐겨찾기/설정 재시작 보존·자모/받침/비음화 수료·Content29 듣기5문항/정답 후 참조/레슨 Resume를 확인했다. 잘못된 편집 조작/과거12문항에20개 가정/선택한 레슨보다 최신 활성 Resume/VoiceOver transcript label/뒤로가기 버튼 오선택 등 테스트 오류는 재현 화면과 actual DB에 맞춰 고쳤다. 메뉴의 `すべてを選択`은 Button이 아니라 MenuItem임을 실제 AX tree로 확인했다. assertion을 제거하거나 잘못 입력된 답을 정답 처리하지 않는다.

새 UI12는 실제 긴 한국어 TTS 중 Home 버튼→백그라운드→복귀→중단된 재생의 답 공개 금지→정상 재재생/채점→판정 보존 PASS. 첫 responsive launch 관찰은 Debug Simulator 3회10.789/11.110/8.141초(평균10.013초)로 느렸으며 Mac/Simulator 부하와 앱 경로를 조사한다. 이를 실제 iPhone 성능/정상 속도 인증으로 표현하지 않는다. 홈 대비 감사 실패와 Dynamic Type 일부 대응 실패는 실제 화면 스타일을 수정하고 필터/무시 없는 감사를 반복한다. 작은 iPhone SE3·Dark·접근성 최대 글자 크기의 native/UI도 순차 검사 중이다.

사용자는 현재 케이블이 없어 iPhone 연결 불가·내일부터 가능하다고 확인했다. 물리 기기/배터리/VoiceOver 발화/비행기모드/실제 거래·광고와 독립 사람 검수는 BLOCKED/NOT TESTED를 유지하며 자동 예약/다음 단계를 만들지 않는다. 상세 진행·실패 근거는 `Docs/DATA10_NATIVE_REGRESSION.md`, 시작 SHA 원장은 `Docs/DATA10_NATIVE_BASELINE.json`, 원시 로그/xcresult는 `/tmp/hangul-data10-7`이다. 최종 전체 검사와 PR/병합은 아직 남아 있다.

### 7.4 2026-10-23 중단 지점 재개

Git fetch/auth/권한을 다시 확인했고 main/origin/main은 `59d3bc7636c2b22ce7a0e21899fa1deeb2bbfedb`, ahead/behind0/0이다. 미커밋 변경은 이 단계에서 작성한 파일이며 같은 브랜치에서 보존한다. 보호 대상114파일 SHA 불일치0을 재확인했다. 아직 최종 완료·Commit/Push/PR/병합 전이다.

다운로드된 SPM binary artifact의 Info.plist가 없어진 환경 실패로 SmallProduction18은 build 실패/테스트0이었다. 기존 생성 캐시는 외부 경로에 보존하고 새 `/tmp/hangul-data10-7/Packages20`에 동일 고정 AdMob13.11.0/UMP3.1.0을 resolve해 복구했다. 원본/Package.resolved/SDK 버전 변경0이다. `resolve-repair19`의 명령 exit0만으로 artifact 복구 PASS를 주장하지 않고, 실제6개 Info.plist와 후속 build/test를 확인했다.

`SmallProduction21.xcresult`: 작은 SE3/iOS26.0.1·Dark·접근성 최대 글씨에서 UI06 **1/1 PASS(163.370초, skip0, 명령 exit0)**. 실제 걷다 현재/과거/조건3문항, 미제출 초안 종료/복원/편집/정답/완료까지 확인했다. 이전 테스트의 입력란 조기 선택과 UIKit 편집 메뉴 차이를 고쳤다. 일반 크기에서는 MenuItem, 접근성 최대에서는 Button으로 보일 수 있어 두 실제 요소 유형을 지원하며 입력 후 정확한 문자열 assertion을 유지한다. 앱의 임시 제출 진단 로그는 제거했다. UI setup/teardown은 비동기 MainActor에서 실행해 새 actor 경고를 제거했다. 키보드 전환의 invalid-frame runtime warning은 별도 조사 대상으로 남기며 크래시/수정 완료로 표시하지 않는다.

일반 화면의 UI10/14 접근성 감사와 이후 최신 전체 검사를 계속한다. 현재 `xctrace list devices`에 실제 iPhone0이므로 물리 기기 gate는 계속 BLOCKED다. 사용자의 10월22일 케이블 미보유 답변은 당시 이력이며 오늘 연결 완료로 가정하지 않는다. DATA10-8/11은 시작하지 않는다.

### 7.5 안전한 checkpoint — 미완료 검증 보존

NormalAudits22는 UI10/14 **2실행/0 PASS/2 FAIL**, skip0/exit65다. 검색 화면 감사는 통과했지만 홈·학습 진입·통계·설정에 대비/Dynamic Type/텍스트 잘림 이슈가 남는다. 프레임이 스크롤/상단 바에 가려진 항목과 실제 큰 글씨 행 제약을 구분해 조사한다. 필터/skip0이며 아직 외부 도구 문제로 전부 확정하지 않았다. 저장소 밖 단순 SwiftUI 재현 앱 AuditProbe23/24도 비슷한 대비 실패가 났으며 제품 XCTest 수에는 합산하지 않는다. 원본 최소 재현은 `/tmp/hangul-data10-7/AuditProbe`다.

통계/설정의 값 표시를 접근성 크기에서 세로 배치하고 긴 Text/재개 버튼이 세로로 늘어나도록 수정했다. NormalAudits25는 다시 SPM Info.plist 유실로 **build 실패/테스트0**이었다. ignored `.build/data10-7/Packages26`에서 같은 고정 SDK를 resolve해6개 Info.plist를 확인했고 NormalAudits26을 실행 중이다. 이 새 화면 수정은 아직 검증 완료로 표시하지 않는다. 핵심 입력 판정/콘텐츠/사용자 DB migration은 불변이다.

Mac 여유 공간이 실제200MB 수준까지 감소했다. 작업에서 생성한 중복 attachment export17개(883,321,017bytes)만 정리했고 원본 봉인 xcresult와 manifest/로그는 보존했다. 이전 작업 소유 QA Simulator 두 개는 종료 상태에서 app support를 SHA 일치 복사해 보존한 뒤 정리했다. 사용자 소유 Simulator·개인 파일·Production/fixture는 삭제0이다. 사용자에게 프로젝트 외 개인 파일 정리로 여유 공간 확보를 요청했으며 답변 대기다. 공간과 SDK 유실의 인과를 확정하지 않는다.

검색/통계/설정 관련 focused Portable33/33 PASS(0.725초, exit0), 보호114파일 SHA 불일치0, diff whitespace 오류0. 봉인 실행31개 요약은 `Docs/DATA10_NATIVE_RUNS.json`, 원시69로그와 Validator/중복 export 정리 근거는 `Docs/DATA10_NATIVE_CHECKPOINT_LOGS.tar.gz`에 저장했다. 반복 검사 수를 고유 테스트 수로 합산하지 않는다.

이 checkpoint는 중단 시 수정과 실패 근거를 잃지 않기 위한 branch 보존이다. 최종 전체검사·물리기기·main 병합은 완료되지 않았다. 재개 순서: fetch/status 및 이 브랜치 확인 → 충분한 디스크 여유/SDK Info.plist 확인 → NormalAudits26 결과 확인/접근성 수정 반복 → 작업 소유 QA app 상태 보존 후 fresh install 전체 `Tools/verify.sh`(정상 서명·직렬·exact writer) → 모든 필수 검사 통과 후에만 PR ready/merge/main SHA 일치 확인. 실행 명령/xcresult는 `/tmp/hangul-data10-7`에 있다. 다음 DATA 단계는 시작하지 않는다.


### 7.6 2026-10-23 실기기 연결·서명·Release 시작 crash 수정 (검증 진행 중)

기존 checkpoint `f46013cf3ea050a36368a0ddb65bf2171cdeb51b`를 일반 push하고 [Draft PR #24](https://github.com/Raccoon26/Project-Hangul-Study/pull/24)를 생성했다. main 미병합이다. fetch/auth/ADMIN/default main·원격 head를 재확인했고 Production/fixture114파일 SHA 불일치0이다. 사용자가 약6GB를 추가 확보해 디스크 부족은 복구되었으나 과거 실패/중단을 PASS로 바꾸지 않는다. NormalAudits26은 `No space left on device` 때문에 결과 봉인에 실패해 exit73·미완료이며 원시 로그를 보존한다. 최소 probe28/30의 Mach server/Runner 초기화 watchdog 실패는 본문 실행0인 환경 오류다. 이후 같은 작업 소유 Simulator에서 최신 Unit155/155 PASS(skip0, FinalUnits39)로 재실행을 확인했다. 실제 StoreKit 로컬 검증 거래가 있을 때 cache write 실패를 주입해도 verified/광고 차단·저장 오류 메시지가 유지되는 추가 assertion도 포함한다.

iPhone13ProMax/iOS27.2가 연결되었고 사용자가 Xcode Accounts/Team·개발자 프로파일 신뢰를 설정했다. 유효 서명/개발 프로파일로 Release build·설치·launch 요청은 성공했지만, 실제 UI 검사를 통해 **P0 시작 직후 crash**를 재현했다. Google Mobile Ads SDK의 load-time 초기화가 빈 App ID에서 `GADInvalidInitializationException`을 던졌으며 기존 `configuration.enabled` runtime guard보다 먼저 실행됐다. 따라서 설치/launch 명령 exit0만으로 앱 정상 동작을 보고하면 안 된다.

Production ID를 추측하거나 Release에 테스트 ID를 넣지 않았다. IDs가 없는 Release에서 `HANGUL_ADS_DISABLED`와 두 SDK의 build-phase 제외를 함께 적용해 SDK를 로드하지 않는 기존 무료 학습 경로를 제공했다. Debug 공식 테스트 광고·기존 구매 권한/빈도 제한/transaction·UserProgress/데이터는 보존한다. 비활성 빌드도 기존 빈도 이력을 유지한다. 향후 실제 소유 Production IDs를 설정할 때는 두 제외 설정을 함께 해제하고 `check_monetization.py --require-ads`·실제 SDK/동의 검증을 다시 수행해야 한다. 검사 도구는 source 설정의 불일치와 built executable의 dynamic/static SDK 잔류도 거부한다. 관련 Portable 새 회귀1개/현재419개 정의, focused9/9 PASS.

수정 Release의 실제 실행 파일은 GoogleMobileAds/UMP dependency 및 SDK ObjC class가 없고 `--built-info` 검사 PASS다. 같은 iPhone의 PhysicalUISmoke43 **1/1 PASS(exit0)**: 학습 Home 진입·한국어 검색·키보드 닫힘·정확한 검색어 유지·사전 상세 열기를 실제 실행했다. 사용자 선택 서명 Team을 보존하도록 generator를 보완했고 ignored package cache의 Swift를 앱 소스로 수집하지 않도록 제외했다. 물리 기기에서는 Release UI-only scheme으로만 검사해 테스트용 Keychain 정리/StoreKit transaction 초기화를 실행하지 않는다. 인증서/Apple ID·기기 식별자를 포함하는 private 로그는 공개 archive/PR에 넣지 않는다.

최신 Portable418/418 PASS(1582.460초) 이후 새 Release 회귀를 포함한 전체419 재실행, Simulator 전체169 XCTest 및 iPhone UI14 전체 검사가 진행 중이다. 첫 세 실기기 경로(첫 학습·종료/재개, 검색/즐겨찾기/설정 유지, 자모/받침/비음화 수료)는 PASS했으나 아직 전체 완료가 아니다. UI10/14 접근성·나머지 실사용 경로/실기기 음성 검청·오프라인/메모리·계정 외부 gate는 실제 후속 결과로만 갱신한다. 필수 로컬 실패가 남으면 PR을 ready/merge하지 않는다.


### 7.7 실기기 사용 확인·추가 회귀 (2026-10-23, 여전히 진행 중)

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


### 7.9 깨어 있는 상태의 전체 재검사·작은 화면 조작 분리 (2026-10-24)

NativeSmallAwake76은 전체169 실행/165 PASS/4 FAIL/skip0/exit65다. Unit155/155 PASS(18.195초), UI10/14 자동 감사와 UI07 편집 메뉴·UI08 작은 화면의 즉시 isHittable 가정이 실패했다. actor runtime check에서 trap은 없었고 background publishing 경고는 재현되지 않았다. 키보드 표시 시 invalid-frame warning2건은 남는다. 실제 컴파일한 UI source snapshot을 별도 보존했으며 이후 보완한 검사로 과거 결과를 덮어쓰지 않는다.

UI07은 초안 복원 자체가 성공했지만 넓은 입력란의 빈 중앙을 길게 눌러 전체 선택 메뉴를 열지 못했다. 실제 텍스트의 앞쪽 좌표 재시도와 전체 삭제/최종 입력 문자열 assertion을 추가했다. 중단된 이전 QA 세션도 나머지 문항을 정상 학습으로 완료한 뒤 새12문항 검사를 시작하며 reset/seed/DB 쓰기로 우회하지 않는다. UI08은 버튼이 존재하나 SE3에서 화면 아래에 있어, 실제 스크롤로 도달한 뒤 hittable을 검사한다.

ListeningInputSmall78은2 실행/1 PASS/1 FAIL/skip0/exit65: UI08의 실제 Content29 5문항·정답 후 원문/사전·cold resume·완료 PASS. UI07은 텍스트 교체 이후 키보드가 열린 상태에서 위 재생 버튼을 스크롤하려다 실패했다. 화면 기록에서 키보드 툴바의 닫기 동작을 확인했고, 해당 받아쓰기 경로만 실제 닫기 버튼을 누른 뒤 재생하도록 보완했다. 활용 입력의 키보드 위 제출 검사와 채점/저장 assertion은 유지한다.

앱/DB/광고 SDK가 없는 KeyboardProbe77도 동일 프레임 경고를 냈으나 placeholder selector가 입력 후 바뀌어 두 테스트는 실패했다. 고정 field identifier로 비교한 KeyboardProbe79는3/3 PASS(exit0): 툴바 없음·Spacer 없는 툴바·Spacer 있는 툴바 모두 정확한 입력/제출을 통과했다. 경고는 두 툴바 case에만 재현됐다. 임의로 필수 키보드 닫기를 제거하거나 프레임 경고를 앱 crash/판정 실패로 집계하지 않는다. 이 임시 probe는 저장소169개에 합산하지 않는다.

자동 감사 스크린샷에서 Dark Home Resume 버튼이 어두운 카드 위 indigo 글자로 실제 대비 부족을 보였다. 해당 Text에 semantic primary 전경색을 적용했다. 다른 offscreen/스크롤 reflow의 대비·Dynamic Type·잘림 실패까지 해결했다고 주장하지 않는다. 이 제품 수정과 UI 보완을 포함해 전체169 NativeSmallAwake80을 다시 실행한다. iPhone13ProMax/iOS27.2의 무선 개발 연결도 다시 확인했고, 원본 app support의 읽기 전용 복사본을 보존한 뒤 signed Release UI-only 전체14 PhysicalReleaseFull81을 순차 대기시켰다. 실제 기기에서 Unit/StoreKit cache 초기화 검사는 실행하지 않는다.

Production/fixture114 SHA 불일치0·현재 bundle31테이블/integrity ok/FK0을 재확인했다. VoiceOver는 사용자 명시대로 추후/NOT TESTED, 필수 실패가 남으면 완료/ready/main 병합하지 않는다.


### 7.10 최신 전체 결과·최대 글씨·자연 due 어휘 (2026-10-24, 완료 아님)

전체 NativeSmallAwake80은 **169 실행/167 PASS/2 FAIL/skip0/exit65**다. Unit155와 기능 UI12개는 모두 통과했으며 UI10/14의 필터 없는 자동 접근성 감사만 실패했다. 활용 직접 입력·초안 cold resume·정확한 교체/채점, 듣기 네 유형12문항·정상/느린 재생·받아쓰기·Content29 레슨5문항/참조·저장/재개를 실제 UI로 확인했다. actor trap/background publishing 경고는 없었으며 keyboard invalid-frame 경고2건은 남았다. 과거76/78 실패 기록과 별도로 보존한다.

자연 예정일의 어휘 복습 VocabularyDue82는 **1/1 PASS(exit0)**다. 실제1카드의 답 공개 전 자기판정 불가→공개→프로세스 종료/재개 후 공개 유지→覚えた→1/1 완료→다시 실행 후 due 해소를 확인했다. 읽기 전용 DB 비교에서 SRS 키21개 보존, 대상1개 reviewCount0→1/stage0→1/미래 due·firstLearnedAt 유지, 다른20행 전체 동일, integrity ok/FK0이다. 시계/seed/reset/사용자 DB 직접 수정0이며 이 임시 E2E를 고유169개에 더하지 않는다. 기존 듣기7개 due E2E75도 별도 PASS다.

작은 SE3/Dark/최대 접근성 글씨에서 SmallAX84는2/1 PASS/1 FAIL: 검색/사전/즐겨찾기/설정 cold 유지02는 통과했고,09는 화면 아래 lazy List 행을 스크롤 전에 찾는 검사 가정으로 실패했다. SmallAX90의09는 유지학습/복습까지 도달했으나 긴 구매 설명 아래 복원 버튼도 같은 가정으로 실패했다. 실제 스크롤·화면 제목·가시성 assertion으로 보완한 **SmallAX93의09는1/1 PASS(144.982초, exit0)**다. 실제 구매/복원 거래는 누르지 않았다. 두 과거 실패를 삭제/skip하거나 전체 통과로 합산하지 않는다.

실제 Dark 캡처에서 낮은 대비였던 Home Resume·짧은 복습 및 검색/설정의 일반 텍스트 동작을 semantic primary로 보완하고 Resume는 줄 수 제한을 해제했다. DynamicFont89는 **1/1 PASS(exit0)**: 앱을 닫지 않고 시스템 글씨를 변경했을 때 Home 세 제목의 높이가40.5→83.5로 증가했고, 긴 Resume 전체 글자/통계/설정 도달을 확인했다.87의 offscreen 요소 즉시 조회 실패는 보존한다. HeaderProbe85의 세 기본/명시 font 모두 대비 실패·Dynamic Type 오류0, ViewportProbe88의 표준/geometry-clipped 모두 대비 실패였다. 최소 재현이므로 제품 헤더/화면 구조를 근거 없이 교체하지 않았다. 알 수 없는 자동 감사 이슈까지 SDK 문제로 단정하지 않으며 VoiceOver 실제 발화는 사용자 요청대로 NOT TESTED다.

FocusedPortable86은33/33 PASS(0.639초, failures/errors/skipped0, exit0). 최신 전체 Portable68의419/419 PASS와 strict frozen28→29/31테이블 byte 재현·기존10경고/오류0, Production/fixture114 SHA 불일치0을 유지한다. 신규 Production/ID/Content/UserProgress 변경0이다.

실기기 재시도81은 연결 상실로 destination을 찾지 못해 exit70/실행0이었으며 build/test PASS가 아니다. 사용자가 보류 후 다시 iPhone 준비를 알려 개발 연결을 확인했다. **최신 signed Release UI-only 전체14 PhysicalReleaseFull96 실행 중**이며 실제 사용자 기기에서 Unit/StoreKit 초기화 검사는 실행하지 않는다. 그 뒤 최신 전체169 NativeLatest91과 resolve/Debug/Release/기기 architecture/Release 시작 회귀92를 직렬 실행한다. 사적인 기기 로그/학습 DB는 공개하지 않는다. 필수 감사 실패/최신 전체 결과 대기로 Draft PR24·미병합·DATA10-7 IN_PROGRESS를 유지한다.


저장공간 추가 조사(10월24일 저녁): iPhone OS가 현재27.2/build24B115로 갱신되어 Xcode DeviceSupport6.7GiB가 새로 생성됐으며, 이전 build24B5110a6.6GiB도 남아 있었다. 사용자의 불필요 산출물 정리 요청에 따라 현재 build와 분리된 이전 DeviceSupport 캐시7,041,413,659bytes·종료된 작업용 QA Simulator3개의 Library/Caches915,739,819bytes·자체 DerivedData 재생성 모듈/색인을 정리했다. 학습 app container·Keychain·사용자 Simulator·원본/fixture·xcresult는 보존했다. 실제 df 가용 약0.1GiB→8.0GiB로 회복했다. 최신91/92는 새 Xcode 실행 전 공간 부족 때문에 잠시 대기를 해제했으며 결과 bundle/실행0을 확인 후 같은 명령으로 다시 직렬 대기시켰다. 검사 실패나 skip으로 집계하지 않는다.96 실제 iPhone 검사는 계속 진행한다.


### 7.11 사용자 실화면 제보·표시 회귀 수정 (2026-10-24 저녁, 재검증 중)

사용자가 검색 쪽 흰 버튼의 글자 누락·음성 버튼 배치 이상·기본 디자인의 부족을 직접 제보했다. 기능 버튼의 AX 이름/탭 성공만으로 실제 표시 PASS를 판단했던 검증 공백이다. 이 브랜치의 이전 탭 대비 수정에서 TabView의 semantic primary tint가 push 목적지에 전파되어 Dark 화면의 prominent 버튼이 흰 배경/흰 글자가 됐다. 기본 탭 root 안에만 있던 indigo는 목적지까지 보호하지 못했다. 이 수정은 main에 아직 병합하지 않았다.

새 UI15는 실제 검색→걷다 상세→「もう一度学ぶ」의 버튼 이미지를 검사한다. rounded border/shadow를 제외한 글자 영역의1/99 percentile 밝기 차이를 확인하며 AX label 존재만으로 통과시키지 않는다. 수정 전 DictionaryContrast101은1/1 FAIL/exit65, 실제 밝기 차이0.0(기준>0.20), 저장한 작은 crop에도 완전한 흰 버튼을 재현했다. color 검사 실패를 완화하지 않았다. 탭/목적지에 일관된 indigo를 적용하도록 primary tint 상속을 제거했다. 새 고유 정의는 Unit155+UI15=170이다.

사용자에게 보인 실제 화면에는 이어하기 시 외부 닫기 바와 내부 닫기 헤더가 중복되어 있었다. 자체 헤더를 갖는 어휘/문법/문자 레슨/복습 resume에서 외부 바를 숨기되 로딩/오류 중 닫기는 유지하고, 어휘 cold resume에 단일 헤더 assertion을 추가했다. 기본 디자인은 기능 중심의 미완성 시각 디자인이며 전면 신규 디자인/새 기능을 이번에 승인된 것으로 확대하지 않는다.

음성 조작은 재생 중에만 Stop을 생성하던 조건이 행 너비·ViewThatFits 선택을 바꿔 위치가 움직일 수 있었다. 보통/느리게/정지를 같은 자리에 유지하고, 정지는 미재생 시 명시적으로 비활성화한다. 접근성 큰 글씨는 재생 상태와 독립된 세로 AnyLayout을 사용한다. 듣기는 질문 지시문→재생→답 순으로 배치하고 실제 시스템 음성/검증 녹음 표기를 구분한다. 엔진·정답·heard/transaction/SRS·원문 비공개 정책은 유지했다.

UILayout102는2 실행/1 PASS/1 FAIL/exit65: 실제 긴 TTS의 재생 전후 버튼 좌표 불변·정지 활성/비활성·background 중단·정답 미노출·재생 후 정답/저장은 UI12 PASS(126.360초). UI15는 검색 탭 표준 tap 이후 실제 검색 화면으로 이동하지 않아 pixel 검사에 도달하기 전에 실패했다. 화면 캡처는 Home이 남아 있음을 확인했다. 실제 tab frame 중심 탭과 목적지 제목 assertion을 보완한 DictionaryContrast104에서 pixel 검사를 다시 실행 중이며 기존 실패를 통과로 바꾸지 않는다.

실기기 PhysicalReleaseFull96은 최신 Release build/설치 후 UI01~06(첫 실행·검색/설정·자모/받침/발음·회독·문법·활용/입력/재개)6개 PASS했다. 새 제보 수정이 우선이므로 이전 바이너리의07 실행 중 명시적으로 중단했다(exit75). xcresult는7실행/6 PASS/취소 오류1/skip0이며07 완료/08~14 실행을 주장하지 않는다. 최신 UI 수정 후 실제 iPhone Release 전체15(103)와 Simulator 전체170(91), Debug/Release/architecture/Release 시작 회귀92를 직렬 검증할 예정이다. 91/92는 불필요한 수정 전 전체 반복을 피하려고 Xcode 실행 전에 대기를 해제했으며 미실행이다.

사용자 저장공간 선호는 AGENTS.md에 반영했다. 중복 diagnostic export155,205,726bytes를 추가 정리했고 원본 xcresult/필수 실패 근거는 보존했다. 전체 검사 반복/중복 export/불필요 진단 수집을 늘리지 않는다. 현재 증거·실패 이슈는 남기며 VoiceOver NOT TESTED·필수 자동 감사 FAIL·Draft/main 미병합·DATA10-7 미완료를 유지한다.


후속 DictionaryContrast104는 **1/1 PASS(64.121초, exit0)**다. 실제 검색 상세의 흰 버튼을 indigo/가시적인 글자로 교정한 pixel 회귀가 통과했다. [수정 전 실제 버튼](Docs/DATA10_BUTTON_BEFORE.png) / [수정 후](Docs/DATA10_BUTTON_AFTER.png)는 각각4.5KB/12.6KB의 필요한 crop만 보존한다(이 문서가 Docs 안에서는 동일 폴더 파일을 참조한다). UI12의 위치 고정/정지/중단/정답 비공개126.360초 PASS와 구분하며102의 UI15 미진입 실패도 유지한다. 현재 동일 수정본의 signed iPhone Release 전체15 PhysicalLatest103을 실행 중이고 Simulator 전체170 NativeLatest91·빌드/Release smoke92를 직렬 대기시켰다. 이후 제품 수정이 없고 관련 검사가 끝나면 근거 없이 전체 검사를 반복하지 않는다.
