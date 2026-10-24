# DATA-09 최종 종료 보고 — DATA-09-8

2026-10-20 UTC. **Content24 / Schema4 / minReader7 / UserProgress10**, Release **B—Conditional**. DATA09 콘텐츠 제작·AI 자체 감사·통합·portable 종료 검증과 Git 전달을 마무리한다. 독립 사람 검수, iOS/XCTest·실기기 출시 검증은 남는다. DATA10은 시작하지 않는다.

시작 main/origin/main `542816ccf1a8ce25a8a4865cbd8f2a7fcb73c03e`, 미커밋 변경0. `data09-8/final-closeout`에서 작업했다. 이번 콘텐츠 추가·수정·삭제·revision/Stable ID 재발급0, runtime 코드 변경0이다. Source/Bundle/과거 fixture95개 파일 byte를 보존했다. 실제 근거는 [구조·재구성 검사](DATA09_CLOSEOUT.json), [이번 최종 결과](DATA09_CLOSEOUT_RESULTS.json), [현재 전체 경로 검사](DATA09_CLOSEOUT_ROUTING.json), 누적 `DATA09_PROGRESS.md` §14다.

## 신규 수량과 전체 목표

| Batch | 신규 Grammar/문법 표현 | 별도 고정 Expression | 신규 고유 Example | 신규 Grammar Question |
| --- | ---: | ---: | ---: | ---: |
| A |18|0|72|72|
| B |18|0|72|72|
| C |18|0|72|72|
| **합계** |**54**|**0**|**216**|**216**|

Content19 대비 실제 ID 차집합을 registry와 대조했다. 목표45~60문법/표현·180~300예문·180~300문제를 충족한다.54개는 모두 grammar 테이블의 생산적 구조/종결어미이며 여러 품사/시제 이형태·인용 축약형을 따로 세지 않는다. 회화 기능 문법을 다시 Expression 수로 더하지 않는다. 기존 DATA08 Example4개 재사용은 신규216에 포함하지 않고 문법 예문 배치220개로 구분한다. 신규 Vocabulary0, 신규 고정 Vocabulary expression0이며 기존 전체 Vocabulary expression은 **163개**다. 과거 문서의104개는 DATA08 신규 표현 cohort이고 전체 표현 수가 아니다. 기존 원문은 역사 기록으로 남기고 이번 현재 보고에서 범위를 바로잡았다.

장기 Grammar/Expressions **350~500개**는 유지한다. 현재 Grammar96개이므로 같은 집계 기준 부족254~404개다. Vocabulary expression163개를 Grammar96에 더해 목표 달성으로 만들지 않는다.

## Level별 전체 Production

| Level | Vocabulary | Meaning | Example | Grammar | Question | Listening | Course / Lesson |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 한글 |0|0|0|0|59|0|1 /12|
| 入門 / intro |306|327|659|22|156|34|2 /20|
| 初級 / beginner |800|847|1,577|20|134|79|1 /6|
| 初中級 / lower_intermediate |1,181|1,246|2,577|54|3,204|1,823|4 /65|
| 中級·中上級·上級·マスター·維持 각각 |0|0|0|0|0|0|0 /0|
| **전체** |**2,287**|**2,420**|**4,813**|**96**|**3,553**|**1,936**|**8 /103**|

Example는 문장4,800+발음13, Grammar Question300(기존84+신규216)이다. source25테이블66,094행, content_items15,941/grammar_examples389/content_links6,499/lesson_items1,191, 현재 비활성0. 듣기는 TTS1,936이며 검증 녹음 asset0. Level은 내부 교육 Level이고 공인 TOPIK 등급이 아니다. 維持 content0은 통계 기반 유지학습 기능 부재를 뜻하지 않는다.

신규54문법은 실제3Grammar course/6Unit tag/18lesson에3개씩 고유 배치된다. 전체 문법은30레슨이다. 선행 설명 preview20개 추가와 관련35어휘로 향하는54관계, 기존 예문 Note reader→model→view를 연결했다. 실제 검수 입력26문제가 있는 관련6어휘에12Grammar에서 진입한다. 새54문형 전체 자동 활용/직접입력·Listening 생성으로 표현하지 않는다. 이번 실제 SQL 조회에서 전3,553문제/4,813예문 경로 누락0이다.

## 선행 문형163건의 최종 처리 상태

| 원래 분류 | 설명 coverage 해결 | 조건부 교육 허용 | 미해결 | 합계 |
| --- | ---: | ---: | ---: | ---: |
| 부족 문법 후보 |120|4|23|147|
| Level/배치 재검토 |0|0|8|8|
| 단순 검토 |0|3|5|8|
| **합계** |**120**|**7**|**36**|**163**|

[DATA09-5 최종 원장](DATA09_FINAL_PREREQUISITES.json)의163개 index/원Example ID·한일 원문/지원 Grammar ID를 현재 DB와 다시 대조했다. 분류를 새로 바꾸지 않았다. ‘해결’은 설명 범위를 AI가 확인했다는 뜻이며 사람 승인·모든 부수 문형 숙달·자동 재사용/배치 승인이 아니다. 조건부7개를 새 Grammar로 추가하거나 모두 승인된 재사용으로 세지 않았다. Level8건은 확정 오등급이라는 주장 없이 미해결로 남긴다.

현재96문법/93선행 edge는 잘못된 target·자기참조·순환0이다. 실제 curriculum ordinal상 후행 참조12개는 page0에서 선택적으로 설명을 미리 읽는 방식으로 지원한다. 기존 lesson/session 순서를 재작성하지 않았고 교육 순서 전부 해결을 주장하지 않는다.

## Batch·품질·수정 이력의 재확인

Content19 기준42문법→A20의60→B21의78→C22의96→교정23의96→통합24의96을 실제 frozen DB와 당시 수량 보고서에 대조했다. DATA09-7의96/4,813/3,553도 현재24와 일치한다. A/B/C exact gate는 당시20/21/22 fixture, 교정22→23 gate는23fixture, 통합23→24 gate는현재24를 검사한다. 오래된 미교정 fixture를 현재 승인 원본으로 배포하지 않는다.

DATA09-5의 assistant 한국어/일본어 별도 전수 자체 검수54문법·216신규예문·216문제·648선택지, 고위험18문법 및 관련18예문배치/18문제, 무작위9문법/18예문/18문제 검수 기록과 known-error 회귀를 보존했다. 서로 겹치는 표본을 새 고유 수량으로 더하지 않는다. 당시25ID/31필드 교정(의미/시제/결합·기본형·일본어 nuance/동생 성별 문맥 등)은 현재 본문에 유지된다. 이번은 그 결과와 payload/참조·회귀의 재확인이며 독립 원어민·교사 또는 외부 사전 검수 완료가 아니다(**NOT TESTED**).

DATA09-6 runtime 수정/보완은 예문 learning_point_ja 누락 수정, 코스/단원·선행 안내 연결, related vocabulary/실제 authored 입력 진입이다. DATA09-7은 snapshot·오답·늦은 저장 실패 rollback·중복 Progress 회귀를 추가했고 runtime 신규 수정0이었다. 이번8단계도 새 runtime 수정0이며 ‘전체 표현104’로 읽힐 수 있던 문서 집계 범위를 DATA08 신규104/전체163으로 명확히 했다.

DATA08 P1 세 건(비활성 카드 복습 정지, dictation 끝 .!? 생략 오답, listening due 퇴역 prefix로 후속 active 누락)의 수정 코드를 보존한다. 현행 SQL/corpus/source 회귀는 PASS지만 Swift 판정/API/UI·기기 재현 gate는 BLOCKED다. 일반 ProductionAnswer 정규화, 기존 SRS due·review_items/이벤트·고정 session snapshot을 보존했다.

## 원본·Bundle 재구성과 SHA

| 파일/유형 | 실제 크기·정책 |
| --- | --- |
| `Content/production.json` |17,472,029bytes. 유일 canonical UTF-8 Production 원본, 반드시 Git 보존 |
| `Content/content-schema-v4.sql`, Importer/Validator, registry/교정·통합 manifest | 원본 재생성/고정 ID/검수 계약, 보존 |
| `Resources/content.sqlite` |18,841,600bytes. 재생성 가능하지만 Xcode가 실제로 포함하는 배포 자산이므로 계속 추적 |
| `Tests/Fixtures/*` | 과거 strict 비교/회귀용 불변 fixture, 보존 |
| 기존 tracked 숨김 임시 DB | legacy 파일 그대로 보존; 현재 app source 선택 대상 아님 |
| 새 candidate/synthetic/빌드 결과 | `/tmp` 또는 기존 ignored 경로. 이번 재구성 `/tmp/data09-8-rebuilt.sqlite`, 배포/추적하지 않음 |

Source를 기존 Importer에 넣고 실제 직전23 fixture를 `--previous`로 지정했다. 동일24 재현 검사이므로 버전/fixture를 새로 만들지 않았다. 다음 실제 콘텐츠 변경은 현재24 원본/DB를 먼저 보존한다.

```text
Source  081ed35c7cd78345af1c1793fc450acaa2931f173cef00aaa960c8ef42318540
Bundle  56a7fa8b5358e254eeb324e706860d150d20c8ec013ba0b6f602cf14d93cceff
Rebuilt 56a7fa8b5358e254eeb324e706860d150d20c8ec013ba0b6f602cf14d93cceff
```

**SHA 불일치 없음.** 전체31테이블의 모든 열·중복 행 multiplicity(파생 vocabulary_search·sqlite_stat1 포함), schema/index/trigger SQL, table_xinfo/FK/index metadata, integrity_check/FK를 비교해 일치했다. strict Validator0errors/기존10warnings, build4.0429초. Source25테이블66,094행, 기존 원본/Resources/fixture95파일의 baseline byte 불변을 확인했다. SQLite3.53.1/Python3.12.14/Linux에서 재구성했다. 다른 SQLite 환경에서 binary가 달라지면 논리 행/schema와 binary SHA를 분리해 원인을 조사해야 하며 불일치를 조용히 통과시키지 않는다.

기존 Progress/SRS/Favorites/Difficult/Statistics/Settings/Resume·진행중 Session 호환성은 전체 회귀의 임시 UserProgress1~10 migration, Content19/23→24 디스크 교체, 고정 ID/membership/snapshot/선택·SRS due 보존으로 확인한다. 개인 iPhone DB·Swift Codable·실제 UserDefaults/Keychain 실행으로 표현하지 않는다. UserProgress를 콘텐츠 버전에 맞춰 재작성/삭제하지 않는다.

## Validator·Build/Test·대용량 Git

[최종 결과](DATA09_CLOSEOUT_RESULTS.json)와 [원시 전체 로그](DATA09_CLOSEOUT_TEST_LOG.txt)가 실행 수·시간의 기준이다. 구조/보존 점검580건은 unittest 수와 별개이며 더해 테스트 수를 부풀리지 않는다. 경고10개는 기존 짧은 발음 예시5건+동형어 후보5건이고, DATA08 구조 감사5경고와 DATA09 계약0경고를 별도로 기록한다.

- **PASS**: strict Importer0errors/10warnings, 전체 DB/SHA/schema 일치, integrity ok/FK0, 종료 점검580/580, 현재 routing·ID/중복/참조·Stage1~7 근거 재확인.
- **PASS(가능한 범위)**: 이번 전체 Python Unit/SQLite Integration/Regression 및 monetization 검사 **365/365,405.161초,실패/오류/skip0,exit0**. 최종 수/시간은 RESULTS와 전체 로그 참조. 과거 단계 PASS를 이번 실행으로 대체 인용하지 않는다.
- **BLOCKED**: xcodebuild/swift 실행파일 없음. iOS Debug/Release/device build·SDK resolve·type-check·XCTest141정의/실행0, iPhone 오프라인/3~10분/음성·중단·강제종료/VoiceOver·메모리/Dead Button·Crash/실제 StoreKit·AdMob/Keychain/UserDefaults.
- **NOT TESTED**: 독립 원어민·교사/외부 사전 검수. AI 전수 검수/Validator로 사람 승인이나 언어 완전 정확성을 보장하지 않는다.
- **UNVERIFIABLE**: 저장소에서 확보되지 않은 원래 DEV01~14/DATA01~07 완전 명세. 사후 STATUS/REVIEW를 원문 전체로 간주하지 않는다.

접근 가능한 전체 Git refs의 `rev-list --objects --all`/`cat-file --batch-check`로 blob 크기를 조사했다. **50MiB 초과0/100MiB 초과0**, 최대18,841,600bytes. 기존 대용량 오류 원문 로그가 없어 과거 원인을 추측하지 않는다. 현재 원본과 번들은 일반 push 가능한 크기이며 **Git LFS 불필요**하다. 원본 삭제·광범위 ignore·이력 재작성·force push0. 재생성 가능하다는 이유로 현재 Bundle/fixture를 Git에서 빼지 않는다.

## 남은 P0/P1·다음 Content Gap·종료

실행된 portable/DB 범위에서 미수정으로 재현된 새 P0/P1 0이다. iOS native 실행0이므로 앱 전체 P0/P1 부재를 보장하지 않는다. DATA08 P1 세 건과 DATA09 통합 수정의 native 확인 gate가 남는다. Release **B—Conditional**을 유지한다.

다음 공백은 선행 미해결36건(그중 Level8), Grammar 장기 부족254~404개·중급 이상 콘텐츠0, 검증 녹음0, 새 문법의 추가 authored 직접입력/Listening·통합 교육 순서/독립 언어 검수다. 모든9형 외 활용/ㅎ사전 override·자유작문/혼합 scheduler·원격 update·고정 회독 retire 자동대체는 부분/미구현 계약을 유지한다. 광고·구매·설정/권한 코드는 변경하지 않으며 contentVersion과 독립성을 유지한다. 이번 작업은 **DATA09-8에서 종료, DATA10 자동 시작0**이다.

재현 명령(프로젝트 루트, Python 표준 라이브러리):

```sh
python3 Tools/ContentBuilder/build_content.py Content/production.json /tmp/data09-8-rebuilt.sqlite --production --previous Tests/Fixtures/content-v23-production.sqlite --report Docs/DATA09_CLOSEOUT_BUILD.json
python3 Tools/ContentBuilder/audit_data09_system.py --report Docs/DATA09_CLOSEOUT_ROUTING.json
python3 Tools/ContentBuilder/audit_data09_closeout.py --rebuilt /tmp/data09-8-rebuilt.sqlite --build-report Docs/DATA09_CLOSEOUT_BUILD.json --routing Docs/DATA09_CLOSEOUT_ROUTING.json --report Docs/DATA09_CLOSEOUT.json
sh Tools/verify.sh --portable
```

기존 위임과 이번 명시 요청에 따라 정상 commit/push/PR/merge로 main에 전달한다. 최종 commit·PR·merge SHA/원격 동기화는 `DATA09_PROGRESS.md`의 Git 전달 기록, 해당 PR/Git과 최종 응답이 기준이다. 원격 CI가 없으면 로컬 PASS를 원격 실행 PASS로 바꾸지 않는다.


## DATA-10-7 후속 Native 확인 (2026-10-24, 전체 완료 아님)

DATA09 당시 Cloud/native BLOCKED 기록은 역사로 보존한다. 실제 Mac Xcode27.1·iOS26.0.1 Simulator NativeSmallAwake76 및 최신80 Unit155 전체에서 `GrammarLearningTests.testDATA09UnitsPrerequisitesNotesAndVocabularyAreReachable`, `testDATA09LowerIntermediateGrammarSRSAndVersionedColdResume`, `testDATA09All18LessonsQuizSRSAndResume`이 PASS했다. 실제18레슨/54문형의 출제·SRS·이전 버전/cold resume 경로를 실행한 결과이며 독립 사람 언어 검수는 아니다. DATA10-7에서는 되다/뵈다·검수한 네ㅎ형·구매 cache·입력 초안 등 runtime 수정도 별도 재검증하고 있다.

Source/Production/기존 ID/revision/관계·UserProgress schema는 보존했다. 전체 Native76은169/165 PASS/4 FAIL이고 접근성 등 미완료 gate가 있어 DATA10-7/출시 승인을 선언하지 않는다. [DATA10_PROGRESS §7](../DATA10_PROGRESS.md)·[Native 보고](DATA10_NATIVE_REGRESSION.md)의 최신 결과와 Release B—Conditional을 따른다.
