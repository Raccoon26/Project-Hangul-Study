# DATA-09-8 / 최종 종료 — 현재 Production

**Content24 / Schema4 / reader7 / UserProgress10 유지.** 신규 Grammar54·별도 고정Expression0·고유Example216·GrammarQuestion216(각Batch18/0/72/72), 기존Example4재사용 제외. 전체Vocabulary2,287/Meaning2,420/Example4,813/Grammar96/Question3,553/Listening1,936. Vocabulary expression 전체163개 중 DATA08 신규104개이며 DATA09 추가0이다. 장기Grammar/Expressions350~500 유지.

Source→임시SQLite 재구성: **31테이블 전체 행/스키마/참조·SHA 일치**, Source25테이블66,094행·기존원본/Bundle/fixture95파일 byte 보존, Validator0errors/기존10warnings. 이번 portable **365/365 PASS(405.161초,실패/오류/skip0)**·종료점검580 PASS·전3,553문제/4,813예문 도달. 선행163건120해결/7조건부/36미해결(Level8포함) 유지. **iOS Build/XCTest141정의·실행0/기기 BLOCKED, 독립 사람·사전 NOT TESTED, Release B—Conditional**, native P1 gate 유지. 이번 runtime 수정/데이터변경0·SHA불일치0. [최종보고](Docs/DATA09_CLOSEOUT.md), [실행결과](Docs/DATA09_CLOSEOUT_RESULTS.json), [누적§14](DATA09_PROGRESS.md). DATA10 미착수. 아래 ‘현재’·검사는 당시 이력이다.

---

# DATA-09-7 / 요구사항·시스템 회귀 감사 — 현재 Production

**Content24 / Schema4 / reader7 / UserProgress10 유지.** 전체 portable **365/365 PASS**(415.721초, 실패·오류·skip0), DATA08 P1 전용10/10·새 문법 회귀6/6 PASS(전체와 중복). 실제 SQL로 전3,553문제/4,813예문 도달·누락0,96문법/93선행 edge 순환0·후행 참조12개는 선택적 설명 프리뷰로 지원한다. 새 런타임 P0/P1 재현0·수정0, Source/DB/ID/revision 변경0. 신규54문법/216고유예문/216문제·장기350~500 목표 유지.

19/23→24 strict 오류0/기존경고10·DB byte 재현·기존 Progress/SRS/session/통계 보존 회귀 PASS. **Xcode/Swift 없음: iOS Build·141정의 XCTest(기존139+이번2)/실행0·기기/음성/접근성/메모리/3~10분/StoreKit/AdMob BLOCKED**, 독립 사람·외부사전 NOT TESTED, 옛 원래 명세 전체 UNVERIFIABLE. native P1 확인 gate·선행 미해결36건·B—Conditional 유지. [상세 감사](Docs/DATA09_SYSTEM_REVIEW.md), [실행 결과](Docs/DATA09_SYSTEM_RESULTS.json), [누적 §13](DATA09_PROGRESS.md). 이번 DATA09-7에서 종료하며 다음 단계는 시작하지 않았다. 아래 수량·‘현재’·검사는 당시 이력이다.

---

# DATA-09 진행 기록

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

## 목표·권한·현재 상태

2026-10-20 JST. **DATA-09-1 분석·설계 완료 / Production 제작·수정·통합0.** 이번 사용자의 DATA09-1 명시적 요청에 따라 분석·설계만 진행했다. 이전 DATA08의 ‘완료 전 DATA09 착수 금지’를 DATA08 검증 완료로 바꿔 해석하지 않는다. DATA08의 B—Conditional, 사람 검수 NOT TESTED, native BLOCKED는 그대로 남는다. 이 요청은 DATA09-2 이후 콘텐츠 제작·버전 변경·배포의 자동 승인이 아니다.

장기 목표 **Grammar/Expressions350~500개** 유지. 현재 승인된 Grammar42개이며 일반 Vocabulary expression104개를 중복 합산하지 않는다. 이번 初中級 신규45~60개 가이드에 맞춰 **54개 교육 단위**를 계획했다. 전부 승인·통합될 경우 총96개이며 장기 목표까지254~404개가 더 필요하다. 현재 신규 Production Grammar/Expression은0개다.

## 1. 최신 main·기준선

- `git fetch origin` 후 main/origin/main 모두 `87be2a152495b7d0d195ec318092a35b982b2bc6`(PR #9), 시작 tracked/untracked 변경0. 작업 branch `data09-1/grammar-analysis`. 기존 변경 덮어쓰기·reset/force push 없음.
- 읽은 기준: PROJECT_STATUS.md / CONTENT_GUIDE.md(현 머리말·문법/활용/관계/버전 계약) / DATA_PROGRESS.md / AGENTS.md / Docs/DATA08_CLOSEOUT.md / DATA08_PROGRESS.md 및 FINAL_GRAMMAR·실제 SQLiteGrammarContent/GrammarModels/GrammarLearning/SQLiteProduction/Curriculum/Validator.
- 실제 **Content19 / Schema4 / minReader7 / UserProgress10**, dataset ko-ja-core/ja→ko/fixture0. Vocabulary2,287 / Meaning2,420 / Example4,597 / Grammar42 / Listening1,936 / Question3,337 / Course5 / Lesson85. 初中級 Grammar0.
- Source SHA `f97b3bd70d07a3945770b8d6940c4a53e29a9b70b565caf21fb927230c08b4a8`, bundle SHA `57aeaf918d5eaaec3bbfaed02f87c5452cca8264540b923a70448b781adbe9e5`. 기존 Content/Resources/fixture/runtime/tests/DATA08 기록246개 파일 hash 보존. 실제 사용자 iPhone의 UserProgress DB는 이 환경에 접근하지 않았으며 저장된 실제 사용자 데이터를 실행 검증했다고 주장하지 않는다.

기계 판독 근거는 [DATA09_BASELINE.json](Docs/DATA09_BASELINE.json). 기존42개 전체 본문/예문/문제 payload·Level·Stable ID·레슨 위치 및 보호 파일 해시를 기록했다.

## 2. 기존42개 내용·Level·순서

**入門22 / 初級20 / 初中級0**, 총12개 문법 레슨(각Level6개). 해당 Level 내 lesson.ordinal→lesson_items.ordinal이 학습 순서다. 기존12레슨·42 ID·본문·순서·구성은 변경하지 않았다.

| Level / lesson ordinal | 실제 내용 순서 |
| --- | --- |
| 入門0 | 이에요/예요 → 은/는 → 이/가 |
| 入門1 | 을/를 → 에 → 에서 |
| 入門2 | 아요/어요 → 있다/없다 → 이/가 아니다 → ㅂ니다/습니다 |
| 入門3 | 았/었어요 → 안 부정 → 지 않다 |
| 入門4 | 와/과·하고 → 도 → 만 → 에게/한테 |
| 入門5 | 부터 → 까지 → (으)로(수단) → (으)세요(요청) → 아/어 주세요 |
| 初級0 | 고 싶다 → 고 → 지만 |
| 初級1 | 아/어서(이유) → (으)면 → (으)니까 |
| 初級2 | (으)려고 하다 → (으)ㄹ 거예요(계획) → 고 있다(진행) |
| 初級3 | 아/어 보다 → (으)ㄴ 적 있다/없다 → (으)ㄹ 수 있다/없다 |
| 初級4 | 아/어야 하다 → 아/어도 되다 → (으)면 안 되다 → 지 마세요 |
| 初級5 | 는/(으)ㄴ 것 같다(현재추측) → 보다(비교) → 기 전에 → (으)ㄴ 후에 |

설명·제약·일본인 Note와 실제 ID/예문/질문은 [42개 상세 조사](Docs/DATA09_EXISTING_GRAMMAR.md)에 항목별 기록했다. Grammar 예문169연결/실제 질문84개(meaning39/form23/blank16/contrast5/context1), 비교 관계26행, Grammar→Grammar 선행 관계19행. 기존 Grammar→初中級 Example55연결(그중 DATA08 신규46)이 있어 Grammar Level만으로 예문 전체 선행 학습을 보장할 수 없다. 현재 예문은 단위당6개 이하이며 후속 연결의 표시 한도를 검토해야 한다.

기존 설명의 범위 한계(에서 출발점, 로 방향, 세요 일반존경, 것 같다 과거·미래, 아/어서 순서, 전체 명사화/관형형 등)를 기존 본문 보완과 별도 기능 교육으로 나눠 설계한다. 이미 부연된 지 않아도 되다 등을 신규54개로 다시 세지 않는다.

## 3. DATA08 선행 문형 후보163개 실제 재검토

각 후보의 원래 Example ID·한일 본문·Level·feature를 실제 DB와 확인하고 assistant가 문장별 근거와 계획키를 작성했다. 주분류는 한 문장당 하나이며 관련 문형은 복수 태그로 남긴다.

| 분류 | 고유 Example 수 | 판정 의미 |
| --- | ---: | --- |
| 부족 문법 | 147 | 실제 문형의 독립 교육/형태·의미 범위가 기존42개에 부족함. 잘못된 한국어라는 뜻은 아님 |
| Level·배치 불일치 재검토 후보 | 8 | 복합 인용·이유 일반화 부정·명사화·부정 범위의 부담으로 후반 初中級/中級 보정 검토. 공식 급수 오류 확정 아님 |
| 단순 검토 | 8 | 오탐 또는 기존 허가/부연 설명 중심. 다른 선행 공백까지 모두 해소됐다는 뜻 아님 |
| **합계** | **163** | 새 수정/승인/Level 변경0 |

Level 후보 번호9/25/45/79/124/127/149/159는 따로 보류했다. 실제 DB Level과 보존 기록 간 값 불일치는0이며 이8개를 오분류 확정·자동 승격하지 않는다.

자다+고2개, 올해+도1개, 이야기/계기+로4개, 부정 허가1개가 단순 검토8개다. 원래 feature165개/고유문장163개를 구분한다. 별도로 다고/라고10문장은 단순 발언 인용이 아니라 이유·양보/일반화 부정 문맥으로 재분석했다. 더니2개와 았/었더니4개, 명사 위하다/동사 기 위해, 달라고/주라고의 수혜자 관점도 구별했다.

[163개 개별 근거 표](Docs/DATA09_PREREQUISITE_AUDIT.md), [기계 판독 판정](Docs/DATA09_PREREQUISITE_AUDIT.json). 이 분석은 전1,821개 예문의 완전 형태 분석·새 사람 언어 검수·기존163개 문제의 해결 인증이 아니다.

## 4. 初中級54개 확장·재사용 설계

- Batch A18: 수식/명사화·결과 상태/변화·결정·시간·대화 의도/부탁. Batch B18: 발화 종류별 인용·내용 수식·판단·양보·이유. Batch C18: 목적/방침·우려/근접 사건·관찰/경험 결과·전환/경향.
- 3개×18레슨, 현재 初中級 lesson.ordinal 최대46 뒤47~64를 후보로 제안한다. 실제 Course/Lesson/Set/Content ID는 생성하지 않았다. 기존 generic runner가 아닌 기존 Grammar/Curriculum 경로를 사용한다. 전체 단위 목록·선행 DAG·비교는 [설계](Docs/DATA09_DESIGN.md), [54개 구조화 초안](Docs/DATA09_GRAMMAR_PLAN.json).
- P01~P54/L01~L18은 편집 키이며 Stable UUID가 아니다. 인용의 품사/시제 이형태, 위해/위한, 주실래요/줄래요를 별도 수량으로 부풀리지 않는다. 생산적 문형은 Grammar, 기존 고정 표현은 Vocabulary/expression ID 재사용으로 구분한다.
- 단위당 예문3연결/문제3개를 설계(각162 placements/신규문제 후보). 현재 승인/생성 수는0.163후보 안에서 관련 예문0인 단위25개는 전DB 탐색 또는 후속 명시된 제작이 필요하다. 나머지도 후보일 뿐 문장 전체 난도·선행형태·한일 의미·정답 유일성 검수가 끝난 것이 아니다.
- 동일 한일 문장 Example ID 공유, 기존 Listening/Dictation·Question ID 재사용 원칙과 실제 참조를 기록했다. 기존 문제를 복사·retarget하지 않는다. grammar_examples/비교/prerequisite 변경 시 기존 관계 끝점 revision allowlist를 후속 제작에서 검증한다.
- 실제 엔진9개 form만 직접입력에 사용한다.54문형의 자동 활용 지원을 주장하지 않는다. Grammar 객관식 meaning/context/blank/form/contrast와 기존 reader를 재사용한다. SQLiteProduction의 prerequisite LIMIT1에 맞춰 대표 하나만 지정하며 다른 선행은 Grammar DAG로 남긴다.
- 3~10분은 설계 목표다. 기존 즉시 저장·페이지 snapshot/중단/이어하기·SRS5/10/20·bounded query·Offline-first·선택적 TTS·광고 제거 권한 독립을 유지한다. 실측/실기기 PASS를 주장하지 않는다.

## 5. 실행 검증·한계·발견 사항

- **PASS**: 이번 strict `build_content.py --validate-only --production --previous Tests/Fixtures/content-v18-production.sqlite` 오류0/기존경고10. 같은19 원본의 검증이며 후보 DB는 임시 디렉터리에서 폐기했다. 현재19를 previous로 지정한 새 배포가 아니다. [실제 보고](Docs/DATA09_VALIDATION.json).
- **PASS**: 실제 기존 문법 회귀 `python3 -m unittest discover -s Tools/ContentBuilder -p test_grammar_content.py -v` **9/9**,31.101초, failures/errors/skipped0, exit0. [이번 원시 로그](Docs/DATA09_GRAMMAR_TEST_LOG.txt). DATA08 전체301 PASS는 과거 기록으로 보존하며 이번301개 재실행이라고 표시하지 않는다.
- **PASS**: 읽기 전용 `audit_data09_plan.py` **1,129개 구조·근거 점검**, exit0. Source25테이블63,159행/Bundle 일치,163개 실제 쌍/주분류/형태 인용,54개 참조/순서/상한, 기존19개 선행 관계를 포함한96노드 DAG, 기존246파일 byte 보존. 이 점검 수는 unittest9개와 합산하지 않는다. [전체 결과](Docs/DATA09_PLAN_CHECKS.json).
- **NOT TESTED / BLOCKED**: 이번 iOS Debug/Release/SDK·Swift/XCTest 실행0, Xcode 환경 부재 유지. Native137개는 과거 정의 수이며 이번 실행 수가 아니다. 실제 iPhone3~10분/TTS·통화/Offline·메모리·AdMob/StoreKit/실제 Progress는 미실행이다.
- **NOT TESTED**: 독립 사람의 한국어/일본어·Level 교정. 일본어 설명/제약·54문형은 설계 초안이다. 자동 Validator나 DAG로 언어 품질을 인증하지 않는다.
- 초기 문서 조립 검사에서 비교 라벨의 `.` 별칭과120번 후보의 잘못 인용한 문자열을 발견해 실제 DB 원문에 맞춰 수정했다. 원문 일치 assertion을 유지했으며 이는 새 Production 버그 수정/테스트 실패가 아니다. 런타임 수정0, 새 P0/P1 재현 조사 범위를 확장하지 않았다.

재현(프로젝트 루트):

```sh
python3 Tools/ContentBuilder/build_content.py Content/production.json --validate-only --production --previous Tests/Fixtures/content-v18-production.sqlite --report /tmp/data09-1-validation.json
python3 -m unittest discover -s Tools/ContentBuilder -p test_grammar_content.py -v
python3 Tools/ContentBuilder/audit_data09_plan.py --report /tmp/data09-1-audit.json
```

## 6. 남은 공백·후속 단계 원장

기존163개에 대한 분류는 완료했지만 선행 문형 보완은0건이다.54개는 제작·승인·배포가 끝나지 않았다. 고 나니/이유·발견 니, 일반존경/셨나요/네요, 려는, 은 끝에, 는 게 낫다, 감정 아/어하다, 아/어 두다, 어서는 안 되다, 피동 생성 등 추가 공백과25개 예문 후보 미확보 단위를 기록했다. 장기350~500개 목표에서 후속 범위를 검토하되 이번 단계를 자동 확대하지 않는다.

| 단계/묶음 | 상태 | 신규 승인 Grammar / Example / Question | 버전·검증·Git 근거 |
| --- | --- | --- | --- |
| DATA09-1 분석·설계 | 완료(analysis only) | 0 / 0 / 0 | Content19/Schema4 유지, strict0/10,9회귀 PASS,1,129구조 점검 PASS, 본 문서·Docs/DATA09_* |
| 후속 제작 Batch A/B/C | NOT STARTED | 0 / 0 / 0 | 각18단위 설계만 있음. 다음 명시 요청 이후 전후 수량/실제 증가·검수/오류/Source/DB hash/ID/revision/Git 기록 |
| 후속 전체 언어 감사·통합·Native/기기 검증 | NOT STARTED | 0 / 0 / 0 | 실제 실행 결과로만 PASS/FAIL/BLOCKED/NOT TESTED를 구분, 기존 DATA08 gate 보존 |

매 단계에 시작/종료 커밋·dirty 상태·actual count/Level·승인/보류/부족 수량·실행 명령/종료 코드·검수 주체·오류/같은 유형 재검색·원본/DB hash·Stable ID/관계·진도 보존을 누적한다. 이전 행/실패 로그를 덮어쓰지 않는다. 문서 변경으로 Content/Schema/UserProgress 버전을 올리지 않는다.

## 7. Git 전달·이번 단계 종료

기존 위임 범위에 따라 분석 문서와 읽기 전용 감사 도구를 일반 commit/push·PR로 전달한다. 최종 SHA/PR/merge·main 일치는 Git/PR과 최종 응답이 기준이다. 기존 Production 원본·DB·fixture·DATA08 결과와 기존 ID/Progress/SRS/runtime는 변경하지 않는다. 강제 push·이력 재작성·대용량 원본 삭제 없음. **이번 DATA09-1 분석·설계에서 종료하며 다음 제작 단계는 시작하지 않는다.**


## 8. DATA-09-2 — 初中級 Grammar Batch A

**신규 문법18 / 고유 신규 예문72 / 학습 문제72(선택지216).** 가이드15~20 /60~100 /60~100을 충족하며 수량 부족0/0/0이다. 시작 main/origin `94a57097416583617b10dc168ca85e223a039b9b`, 미커밋 변경0, 작업 branch `data09-2/grammar-batch-a`.

이번 사용자의 명시 요청에 따라 이유·원인·결과·조건·목적·의도·계획·가정 중심으로 이전54안의 Batch 순서를 조정했다. 기존 계획12개와 별도 기능6개를 선택했다. 기존54개 원문은 보존하고 대응을 [SCOPE](Docs/DATA09_A_SCOPE.json)에 기록했다. 전체 신규 가이드45~60개는 유지한다. 이번18개 이후 목표 대비 남은 승인량은27~42개이며, 미제작 원래 초안42개는 후속 선택 후보이지 자동 제작/승인 약속이 아니다. **장기Grammar/Expressions350~500개를 유지**한다.

### 실제 범위·배치·버전

| 항목 | Content19 → Batch A20 | 현재 初中級 |
| --- | ---: | ---: |
| Vocabulary / Meaning | 2,287 /2,420 → 동일 | 1,181 /1,246 |
| Grammar | 42 → **60** | **18** |
| Example | 4,597 → **4,669** | 2,433 |
| 문장 Example(발음13 제외) | 4,584 → **4,656** | 2,433 |
| Question | 3,337 → **3,409** | 3,060 |
| Grammar Example 관계 | 169 → 241 | 신규72관계 |
| Listening | 1,936 → 동일 | 1,823 |
| Course / Lesson | 5 /85 → **6 /91** | 2 /53 |
| content_items | 15,428 → 15,597 | 신규169엔티티 |

Grammar Level은 入門22 /初級20 /初中級18이며 나머지 단계0. Example는 入門659(문장646)/初級1,577/初中級2,433. Question은 한글59/入門156/初級134/初中級3,060이다. 새 Source 전체25테이블64,099행, strict0errors/기존10warnings, 구조 감사0errors/기존 row-field5warnings를 구분한다.

새 문법: 기 때문에/N 때문에, 느라고, 는 바람에, 아/어지다, 게 되다, 아/어야(필요 조건), V/A다면·N(이)라면, 거든(조건), (으)려면, 기 위해/N을·를 위해, 도록(목표), 도록 하다(지시·방침), 기로 하다, (으)ㄹ까 하다, 아/어야겠다, (으)ㄹ까 봐, 다 보면, (으)ㄹ 필요가 있다/없다. 품사·시제 이형태/위해·위한을 별도 수량으로 세지 않았다. 기존 의무·단순 조건·의도·원인과 의미 기능을 대조하고 단순 별명 재등록을 피했다.

3개씩6레슨(ordinal47~52)/새 Grammar 코스1개에 실제 배치한다. 기존 Grammar Catalog의 初中級 picker를 재사용하며 generic lesson runner로 우회하지 않는다. 레슨3항목·예문4/단위(조회 상한6)·문제4/단위(상한20), 비교 상한6·학습/검색 페이지 상한을 유지했다.3~10분은 기존 설계 목표로 유지하지만 실측 시간은 미검증이다.

기존 정책상 승인 콘텐츠의 Source/번들 metadata는 일치해야 하므로 **Content20 / Schema4 / minReader7 / UserProgress10**을 사용한다. 실제 Content19 번들과 원본 byte를 `Tests/Fixtures/content-v19-production.sqlite` / `content-v19-production.json.gz`에 먼저 보존했다. Content20은 이번 Batch A의 검증 snapshot이고 DATA09 전체 최종 통합·출시 승인이 아니다. 다음 실제 콘텐츠 변경은 현재20을 previous로 보존해야 한다.

기존15,428 ID/kind/created_at·본문·정렬·learning_order·lesson membership·Question/Choice ID는 보존한다. 새 비교·선행 관계 fingerprint에 참여한 기존 Grammar12개만 revision+1/updated_at 변경([allowlist](Content/data09-a-revised-ids.json)). 새169개 content UUID와 standalone Source UUID는 한 번 무작위 발급한 registry를 재사용했다. 기존 엔티티 삭제·비활성화·본문 변경0, 사용자DB·SRS·Progress·runtime·광고/구매 코드 변경0이다.

### 한국어/일본어 Self Review·문제 검수

assistant가 전18개 Pattern/Meaning/Explanation/Form/Usage Constraints/혼동 Note,72개 한일 예문,72개 문제·216개 선택지/해설을 개별 재독했다. 내부·기존 전체 DB 대비 한국어 문장/일본어 문장/한일 쌍 중복0, 새 Pattern 표면 중복0이며 의미 범위 차이도 별도로 검토했다. 독립 사람·원어민·교사 검수/외부 사전 대조는 **NOT TESTED**다. 자동 통과만으로 언어 품질을 인증하지 않는다.

초안32개 문자열을 교정했다. 미등록 던/았·었더니/으면서/아·어 두다/으니/미래 것 같다 등의 추가 선행 부담을 줄이고, 지시자·실행자·필요 조건의 일본어 부정 번역·수혜자 범위를 맞췄다. 문제 prompt 재사용 문장의 동시 교정도 occurrences로 기록했다. 제작 도구 비교 라벨2개도 실제 Pattern 참조로 정정하고 UUID를 다시 만들지 않았다. 실패/교정 전 초안은 Production에 승격하지 않았다.

듣기·듣거든의 ㄷ유지와 들어야·들으려면·들을까·들을 필요, 만드느라고/산다면의 ㄹ탈락과 살게/풀려면의 ㄹ유지, 추워지다/추울까의 ㅂ변화와 돕기로의 ㅂ유지를 구별했다. 높임 찾아뵙다/말씀해 주세요/하겠습니다·하세요의 대상·주체·register를 검토했다. 기존 Vocabulary에 없는 보조 어휘는 뜻을 예문/설명에서 제공하지만 새 Vocabulary 수량으로 세지 않는다. 불규칙 설명은 assistant 검토이며 실제 Swift 활용 생성·외부 사전 확인을 했다고 표시하지 않는다.

모든 학습 문제는 기존 `multiple_choice`, 단일 정답3선택지이며 meaning/form/context/contrast 각18개다. 정답 a/b/c 각24개이고 모든 정답/오답에 일본어 이유를 제공한다. form만 ko_ko, 일본어 의미·대조는 ko_ja다. 미지원 text_input/free-writing/새 ConjugationForm을 추가하지 않았다. text accepted 답안을 사용하는 대신 correct_choice_ids 정확히 한 개와 실제 선택지/대상 Grammar를 검증했다. 의미에 따라 여러 답이 가능할 수 있는 일반 빈칸을 억지로 한 정답으로 만들지 않았다.

[검수 범위·차이](Docs/DATA09_A_REVIEW.md), [전항목 카탈로그](Docs/DATA09_A_REVIEW_CATALOG.md), [검수 payload SHA](Docs/DATA09_A_EDITORIAL.json), [교정 이력](Docs/DATA09_A_EDITORIAL_CORRECTIONS.json), [실제 수량](Docs/DATA09_A_COUNTS.json).

### 실행 결과·회귀·보존

- **PASS**: strict19→20 Importer/Validator errors0/기존warnings10. 원본25테이블64,099행·metadata/PK/FK/Stable ID·DB 대조, integrity ok/FK0. Candidate source와 고정 UUID/authoring 재생성 결과 byte 일치.
- **PASS**: 전용 회귀10/10,24.039초,failures/errors/skipped0,exit0. 신규169ID/18문형·72예문·72문제,12개 정확한 revision,기존 모든 payload/레슨/질문 순서,실제 SQL 도달/중복/선행 DAG/정답·오답 이유/18개 기대 활용형,잘못된 버전/revision/문제 거부·UserProgress disk swap을 검사했다.
- **PASS**: 임시 검증 복사본의 전체 `sh Tools/verify.sh --portable` **311/311**,328.544초,failures/errors/skipped0,exit0. 기존301+신규10이며 전용10/누적9 재검사는 중복 합산하지 않는다. Source/DB와 실행 코드의 hash가 검증 복사본과 같은지 확인한 후 원래 Source/번들을20으로 원자적 승격했다.
- **FAIL → 수정**: 최초 전용10 중9 PASS/1 ERROR(23.554초,exit1)는 test Favorites seed의 v9+ content_type 컬럼 누락. 현재 typed schema/명시 컬럼과 cold reopen으로 수정했다. 초기 전체311 중309 PASS/2 FAIL(323.399초,exit1)는 DATA05 누적 revision 기대값에 새12개 allowlist 반영 누락 및 새 Grammar 코스의 정확한 목록 기대값 누락. 기대값을 구체적으로 갱신하고 Validator/보존 assertion은 유지했다. DATA05 전용9/9 재확인(14.182초) 및 최종311 PASS. 모든 초기/최종 로그를 보존했다.
- **BLOCKED / NOT TESTED**: native137정의/실행0, 실제 iOS build/SDK/기기·개인Progress/오디오·광고/StoreKit 검증0. 독립 사람·외부사전 검수0. Python/SQL과 assistant Self Review를 native/사람 완료로 표시하지 않는다. [검증 결과](Docs/DATA09_A_RESULTS.json), 로그 `Docs/DATA09_A_*TEST_LOG.txt`.

Content19→20 교체 회귀는 분리된 임시 UserProgress10에 기존 grammar session/질문 선택/Content19 snapshot·stage4/due900·typed Grammar favorite를 넣고 Content 파일만 교체했다. 사용자DB SHA/JSON byte가 그대로이며 cold reopen으로 유지된다. 새18개와 기존1개에 SRS 등록을2회 적용해 중복0·기존 stage/due·favorite 보존을 확인했다. 실제 개인의 사용자DB에 접근한 검사가 아니며 Swift Codable/상태 전이나 실제 iOS Settings·StoreKit을 실행한 것도 아니다. SQLite 조회 때 Python socket을 금지했다.

원래301개 회귀를 삭제하지 않았다. DATA08의 정확한18→19 델타 검사는 보존된19 Source/DB fixture로 고정하고 현재19→20의 모든 구행·새169ID·12revision·조회·새 문형은 신규10개가 검증한다. 나머지 live 과거 cohort 검사도 현재20의 정확한 count/revision을 확인하도록 갱신했다. 허용 목록 밖 변경이나 strict Validator를 완화하지 않았다. Native Settings 테스트의 현재 ContentVersion 기대값도20으로 맞췄지만 **Xcode/Swift/iOS SDK 부재로 빌드·XCTest137개/실기기 실행0**이다.

미완료: 독립 사람 한일/난도 검수, 기존163후보 전체의 새 Grammar 재연결/재배치, 새72예문의 독립 Listening/직접입력 문항 생성, iOS/오디오/메모리/광고·StoreKit/3~10분 실측. 기존 DATA08 B—Conditional 및 native P1 확인 gate를 유지한다. 이번은 Batch A에서 종료하고 다음 Batch를 시작하지 않는다.

재현(현재20 기준, 원본/번들/fixture를 출력으로 지정하지 않는다):

```sh
python3 Tools/ContentBuilder/prepare_data09_a.py --output /tmp/data09-a-source.json --revised /tmp/data09-a-revised.json
python3 Tools/ContentBuilder/build_content.py Content/production.json /tmp/data09-a-rebuilt.sqlite --production --previous Tests/Fixtures/content-v19-production.sqlite --report /tmp/data09-a-build.json
python3 Tools/ContentBuilder/audit_data08_final.py Content/production.json --database Resources/content.sqlite --report /tmp/data09-a-structure.json
python3 -m unittest discover -s Tools/ContentBuilder -p test_data09_a_content.py -v
sh Tools/verify.sh --portable
```

`prepare_data09_a.py`는 동결19+검수 authoring+기발급 UUID로 동일20을 재현하는 제작 근거 도구다. 후속 콘텐츠 변경에 덮어쓰기 importer로 사용하지 않는다. `--allocate-ids`는 최초 한 번만 사용했으며 재현 명령에는 넣지 않는다. 앱의 canonical Source는 계속 `Content/production.json` 하나다.

Git은 기존 위임대로 일반 commit/push·PR로 전달하며 force push·이력 재작성·원본 삭제 없음. 실제 최종 SHA/머지·main 일치는 Git/PR과 최종 응답이 기준이다. **DATA09-2에서 종료한다.**


## 9. DATA-09-3 / 初中級 Grammar Batch B

### 9.1 시작·기존 보존·제작 범위

2026-10-20 JST, `git fetch origin` 후 clean main/origin/main `dae7379788d48fc0d41447b47bca9486abdf1ebc`(PR #11)에서 branch `data09-3/grammar-batch-b`로 시작했다. 실제 Content20/Schema4/reader7/UserProgress10 및 Grammar60개(기존42+A18), Example4,669/Question3,409를 대조했다. PROJECT_STATUS/CONTENT_GUIDE/DATA_PROGRESS/RELEASE_CHECKLIST/AGENTS/DATA08_PROGRESS/DATA08_CLOSEOUT와 DATA09_PROGRESS·실제 Source/DB·SQLiteGrammarContent/Validator 계약을 확인했다.

원래54개 계획 중18개를 사용자의 이번 중심 영역에 맞춰 선택했다. 대조·양보·배경·경험·순서·진행 중 전환·변화 후 상태를 다루며 새 고정 Vocabulary/expression은0이다. 실제 목록·선행·비교는 [SCOPE](Docs/DATA09_B_SCOPE.json), 모든 문법·예문·정답/오답과 이유는 [검수 카탈로그](Docs/DATA09_B_REVIEW_CATALOG.md)에 있다. 의미가 유사한 기존 후에/새 고 나서, 기존 진행 고 있다/새 결과 상태 아·어 있다, 기존 다 보면/새 다 보니를 형태·의미 초점과 상황으로 대조했다. 이형태·시제·축약형을 별도 신규 단위로 세지 않았다.

기존 Content20 DB fixture SHA `c7b48bc8b27b7d436fadd41429d9dabf85acf615b632d8cc9a87ca5d6bc39886`, gzip 해제 Source SHA `0ccf5dee471d10dc39401e01f5db52e8093bb77da822626457f2dde9a9bf4e19`를 그대로 보존했다. 이전 fixture/원본·DATA08 및 A 검수 기록·앱 코드 보호 baseline203파일은 제작 전 byte 일치를 확인했다. 최종 허용 변경은 production Source/번들 및 아래22개 관계 metadata이며 이전 이력·본문·ID를 삭제하지 않았다.

### 9.2 실제 수량·배치·버전

|대상|시작20|Batch B 신규|현재21|
|---|---:|---:|---:|
|Vocabulary|2,287|0|2,287|
|Meaning|2,420|0|2,420|
|Example|4,669|72|4,741|
|Grammar|60|18|78|
|Question|3,409|72|3,481|
|Listening|1,936|0|1,936|
|Grammar→Example 관계|241|76(신규72+기존4)|317|
|Course|6|1|7|
|Lesson|91|6|97|

새18문형은 모두lower_intermediate다. Grammar Level은入門22/初級20/初中級36, Example은659(발음13포함)/1,577/2,505, Question은한글59/入門156/初級134/初中級3,132다. Vocabulary306/800/1,181 및 Listening34/79/1,823은 그대로다. Content_items15,766 / 원본25테이블65,043행 / 번들31테이블. 새 레슨ordinal53~58×문형3개는 기존 GrammarCatalog/Repository 경로에서 실제 조회된다. 문형당4신규예문·4문제, 재사용4문형만5예문으로 LIMIT6 안이다. generic Vocabulary 세트·기존 순서·레슨 ID를 변경하지 않았다.

DATA09 누적 신규 **Grammar36 / 고유 Example144 / Question144**. 이번 가이드15~20/60~100/60~100 충족·부족0. DATA08 재사용4는 신규예문에 포함하지 않았다. 전체 신규45~60 목표는유지되며 최소9~최대24문형이 남는다. 원래 초안24개는 미승인 상태이고 다음15~20개를 승인하면누적51~56개가 가능하다. 장기350~500 목표 대비현재총78개로272~422개가 남는다. 다음 단계를 자동 실행하지 않는다.

데이터만 바뀌므로 Content20→21만 갱신했다. Schema4/reader7/UserProgress10 유지, 중간 Batch 승인 snapshot이며 DATA09 전체 최종 통합/출시 완료가 아니다. Source SHA `d7bee9fa444f5d7e29675110aedcec97a231f0334a9e5b255452e83e2bf3a355`, 번들 SHA `0f53e4d93340d9ddc410d17a6cdd4aa1c3f4f69b2089e60b26a390cb9bdff009`. [전체 수량·Level·델타](Docs/DATA09_B_COUNTS.json).

### 9.3 한일 검수·중복·선행·문제

assistant가 전체18개 Meaning/Explanation/Form/Usage/혼동 Note, 신규72쌍과 재사용4쌍, 문제72개/선택지216개/모든 정답·오답 해설을 한국어·일본어 각각 재독했다. 직접 관찰과 자기 체험, 순서·즉시성·중단, 양보와 허가, 상태와 변화, 미수와 완료, 기회와 대체의 차이를 대비했다. 불규칙·ㄹ탈락/유지·시제·높임·분리쓰기와 번역의 사건 발생 여부를 강화 검토했다.

초안 문자열36건의 전후 수정 기록을 보존했다. 미수록 복합 문형의 예문 부담을 줄이고 일본어·상황의 모순·과거형 설명을 고쳤다. 같은 문자열이 문제 본문에서도 쓰인 경우 함께 수정되므로36개 독립 언어 오류라는 뜻은 아니다. [REVIEW](Docs/DATA09_B_REVIEW.md), [EDITORIAL](Docs/DATA09_B_EDITORIAL.json), [교정 전후](Docs/DATA09_B_EDITORIAL_CORRECTIONS.json). 독립 사람/원어민/교사 검수·외부 사전·공인 난도 확인은 NOT TESTED이며 자동 검사와 assistant 재독을 사람 승인으로 바꾸지 않는다.

새72문장 한일 각각 및18Pattern은 기존20 전체/Batch 내부NFC·공백 정규화 중복0이다. 모든 기존 payload/관계/질문/선택지/배치 행을 보존했고, 새 관계의 기존 끝점은 Grammar18+재사용Example4=정확히22개만revision+1/updated_at 갱신했다. [수정 허용ID](Content/data09-b-revised-ids.json). 새169content ID 및source ID1개는UUIDv4 최초1회 발급 후재사용한다. 기존 DATA08 예문4개와 원래 Listening/Question 관계는같다. 기존163후보를 모두해결했다고 집계하지 않는다.

meaning/form/context/contrast 각18문제, 각3선택지·정답1개, a/b/c각24개다. 지정 lemma·명시한 상황을 기준으로 답의 유일성과 오답 이유를 검토했다. 복수 자유입력 허용 표현을 새로 지원하는 문제가 아니며 기존 엔진 계약을 유지한다. 대표 선행1개/비교2개씩 연결했고 기존+A+B 결합 선행 DAG 순환0이다. 관형형의 로컬 결합 설명은 일반 관형형·명사화 전체 교육의 완료가 아니다. 출입구·전시회·어려움 등 모든 토큰의 사전 등재도 보장하지 않으며 Vocabulary 신규 수에 넣지 않았다.

### 9.4 실제 검증·수정·한계

- **PASS** strict20→21 Importer/Validator: 오류0 / 기존경고10(짧은 발음예문5 + 기존 동형어 후보5). 별도 structural row audit는 오류0 / 경고5이며25테이블65,043행을 확인했다. 경고를 삭제·병합·완화하지 않았다. integrity ok/FK0, Source→DB 전31테이블 일치 및 byte/SHA 재구성을 확인했다.
- **PASS** Batch B 전용12/12, 34.166초, 실패/오류/skip0, exit0. strict·Stable ID·22revision·모든 기존행과 관계·정규화 중복·실제 카드/레슨/검색 SQL·72채점계약·18기대활용·선행DAG·잘못된 입력 거부·4개 재사용·authoring 재현·UserProgress 교체를 검사했다. 첫 candidate도12/12(34.012초)였지만 별도 재독에서 추가8문자열을 개선한 후 최종12개를 재실행했다. 자동 PASS가 언어 교정을 대신하지 않는 사례다.
- **PASS** 전체 `sh Tools/verify.sh --portable` **323/323**, 393.788초, 실패/오류/skip0, exit0. 기존311개 + 신규12개이며 전용12개 재실행을 중복 합산하지 않는다. 임시 검증 복사본에서 candidate를 실행한 뒤 Source/DB·실행 코드의 hash 일치를 확인해 승격했다. 기존A의 정확한19→20 테스트10개는 불변20 fixture에 고정했고, 새B가 모든20→21 보존을 검사한다. 다른 live 과거 cohort는 현재 count/각 Batch별 누적 revision 기대값을 갱신했다. 보존 assertion/Validator를 완화하지 않았다.
- **도구 호출 수정**: 첫 Importer CLI에 존재하지 않는 `--output` 옵션을 사용해 argparse exit2였다. Importer 실행 전 거부되어 원본/DB 변경0. 기존 positional output 계약으로 고쳐 재실행했다. 언어·데이터 오류를 숨기거나 실패행을 버리지 않았다. 이번 초기/최종 unittest 실패0이다.
- **PASS(범위 한정)**: 임시 UserProgress10에 Batch A 문법의 stage4/due900·typed favorite·진행 중 grammar session(snapshot20/선택/페이지/revision)을 넣고 콘텐츠 파일만 교체했다. 사용자DB SHA/JSON byte 보존·cold reopen·기존 due/즐겨찾기 유지·기존1+신규18의 SRS 등록2회 후 중복0을 확인했다. 네트워크 socket을 금지한 SQLite 조회다. 실제 개인DB·Swift 상태 전이·기기 실행 검사는 아니다.
- **BLOCKED / NOT TESTED**: Linux/Python3.12.14, xcodebuild/swift 없음. iOS 빌드·XCTest137정의/실행0, 실기기 오디오/중단/3~10분·메모리·StoreKit/AdMob·실제 개인 진도 실행0. native 기대 ContentVersion을21로 맞췄지만 빌드 검증을 주장하지 않는다. 독립 사람·외부 사전 언어 검수0. 이번 범위에서 새 P0/P1 재현은 없으나 기존 native P1 검증 gate/B—Conditional은 해결로 바꾸지 않는다.

[기계 판독 결과](Docs/DATA09_B_RESULTS.json), [전체 원시 로그](Docs/DATA09_B_PORTABLE_TEST_LOG.txt), [전용 로그](Docs/DATA09_B_FOCUSED_TEST_LOG.txt). 실행 횟수와 정적/SQL/언어 재독의 범위를 구분한다. 기존 짧은 학습·즉시 저장·Offline-first·광고/구매 코드/권한을 변경하지 않았다.

### 9.5 재현·전달·남은 공백

```sh
python3 Tools/ContentBuilder/prepare_data09_b.py --output /tmp/data09-b-source.json --revised /tmp/data09-b-revised.json
python3 Tools/ContentBuilder/build_content.py Content/production.json /tmp/data09-b-rebuilt.sqlite --production --previous Tests/Fixtures/content-v20-production.sqlite --report /tmp/data09-b-build.json
python3 Tools/ContentBuilder/audit_data08_final.py Content/production.json --database Resources/content.sqlite --report /tmp/data09-b-structure.json
python3 -m unittest discover -s Tools/ContentBuilder -p test_data09_b_content.py -v
sh Tools/verify.sh --portable
```

prepare_data09_b는 불변20+authoring+고정ID로 이번21만 재현한다. `--allocate-ids`를 재현 명령에 넣지 않으며 후속 Production을 덮어쓰는 Importer로 사용하지 않는다. canonical Source는 production.json 하나다. Source/DDL/Importer/ID/검수 근거와 재생성 가능한 번들·불변 fixture를 구분해 모두 보존한다. 최대 추적 파일은50MiB 미만이며 원본 삭제/LFS/이력 재작성/force push 없이 일반 commit/push·PR로 전달한다. 최종SHA/PR/merge/main 일치는 Git과 최종 응답이 기준이다.

남은 콘텐츠: 인용의 발화 종류별 구조·명사화/수식·판단/추측·대화 의도·비례 변화, 기존163후보의 선행 전체 재연결 및 난도 검토, 신규 예문의 듣기/직접입력 재사용, 독립 사람/기기 검증. **DATA09-3/Batch B에서 종료하며 다음 단계는 시작하지 않았다.**


### 9.6 Git 전달 기록

콘텐츠 커밋 `0a9d846b98b528e2bbd7f920321afba8036550de`를 `data09-3/grammar-batch-b`에 일반 push했고 성공했다. 대용량 파일 오류0, force push/LFS/원본 삭제/이력 재작성0. [PR #12](https://github.com/Raccoon26/Project-Hangul-Study/pull/12)를 main 대상으로 생성했다. 이 전달 기록 작성 시점은 merge 전이며, 최종 merge/main 일치의 근거는 PR 상태·Git 이력과 최종 응답이다. 마지막 문서 점검에서 카탈로그 EOF 빈 줄 경고1건을 제거했으며 콘텐츠·테스트 코드·결과는 바뀌지 않았다.


## 10. DATA-09-4 / 마지막 Grammar Batch C

### 10.1 기준선·Coverage Gap·중단 후 재개

2026-10-20 JST. clean main/origin/main `7a56504e58c8ecb81de976c9a9c76d24546f536c`(PR #12)에서 `data09-4/grammar-batch-c`로 시작했다. PROJECT_STATUS/CONTENT_GUIDE/DATA_PROGRESS/RELEASE_CHECKLIST/AGENTS/DATA08_PROGRESS/DATA08_CLOSEOUT, A/B 결과·설계 및 실제 Source/DB를 확인했다. Content21/Schema4/reader7/UserProgress10, 기존 Grammar78개(원래42+A18+B18)였다. 기존 보호 대상221파일은 HEAD 대비 byte 일치를 확인했다.

A/B 승인 수량은 신규36문법/144예문/144문제다. 전체 목표45~60/180~300/180~300에서 최소 부족9/36/36을 계산하고 C18/72/72를 제작했다. 수식·명사화→추측/가능성·의문 내용→평서/명령/권유/질문 인용→제안/의향/부탁/약속→공유 확인/새 인식·정도 연동 순서로 보강했다. C05는 P25/P26을 한 단위로 합치고 C16지요/C18네요는 생산적 회화 어미로 추가했다. 원래54개 설계키47개를 다루며7개는 미승인 공백이다. 초기 설계 전부를 억지로 승인한 것이 아니다. 새18개는 모두Grammar이며 고정Vocabulary expression 재등록0, 기존expression104개 별도 보존. [범위·남은 공백](Docs/DATA09_C_SCOPE.json).

사용자의 ‘중단 지점부터’ 요청 시 작업 파일·40개 교정 기록·고정UUID·21fixture는 남았지만 /tmp의 candidate/검증 복사본/로그는 소실됐다. 실제 Production은21이어서 미검증 후보의 선반영은 없었다. 고정ID를 재발급하지 않고 같은 최종22를 재구성했으며 저장된 후보의 Source/DB SHA와 정확히 같았다. 새 로그는Docs에 직접 기록하고 전용/전체 검사를 다시 실행했다. 이전 대화의 초기12개 중10PASS/2FAIL(56.234초,B도구 import 오연결)·수정 후12PASS(63.769초)·번역 개선을 위해91개 PASS 후 중단(exit143) 관찰은 이번 실행 수에 합산하지 않는다. 원시 로그 소실과 완료 확인 불가능한 이전 최종 전체 실행을 [RESUME](Docs/DATA09_C_RESUME.md)에 명시했다. 이전 완료 불명 검사를 PASS로 표시하지 않는다.

### 10.2 실제 신규·전체 수량·Level·배치

|대상|Content21|C 신규|Content22|
|---|---:|---:|---:|
|Vocabulary|2,287|0|2,287|
|Meaning|2,420|0|2,420|
|Example|4,741|72|4,813|
|Grammar|78|18|96|
|Question|3,481|72|3,553|
|그중 Grammar Question|228|72|300|
|Listening|1,936|0|1,936|
|Grammar→Example 관계|317|72|389|
|Course|7|1|8|
|Lesson|97|6|103|

C 신규는 모두lower_intermediate다. Grammar은入門22/初級20/初中級54, Example659(발음13포함)/1,577/2,577, Question한글59/入門156/初級134/初中級3,204다. Vocabulary306/800/1,181 및 Listening34/79/1,823 유지. content_items15,935 / Source25테이블65,983행 / DB31테이블. 기존 Grammar 경로에 새 코스1·레슨59~64×3문형을 실제 배치했다. 문형별4예문/4문제는 기존 LIMIT6/20 안이고 카드·레슨·검색 SQL로 접근한다. 기존 레슨 membership·세트/ID/순서는 유지했다.

|DATA09 신규|A|B|C|검증 누적|전체 목표|
|---|---:|---:|---:|---:|---|
|Grammar/Expressions|18|18|18|**54**|45~60|
|고유 Example|72|72|72|**216**|180~300|
|Grammar Questions|72|72|72|**216**|180~300|

부족0. 기존42문법/84문법문제·기존 예문·A/B의DATA08 예문4개 재사용·관계 증가·고정Vocabulary expression104개는 신규 수량에 넣지 않았다. 현재 Grammar총96개로 장기350~500까지254~404개가 남는다. [전체 Count/Level/델타](Docs/DATA09_C_COUNTS.json).

데이터만 바뀌므로 Content21→22만 갱신하고 Schema4/reader7/UserProgress10 유지. 실제21 DB/gzip Source를 불변 fixture로 보존했다(DB SHA `0f53e4d93340d9ddc410d17a6cdd4aa1c3f4f69b2089e60b26a390cb9bdff009`, 해제 Source SHA `d7bee9fa444f5d7e29675110aedcec97a231f0334a9e5b255452e83e2bf3a355`). 새 Source SHA `13a6739bb93daee36426f04ac83b95f7244a62c227ea90b0ddda2d179eeeafeb`, 번들 SHA `22c3257b4204309158dfdea0f0bfd7d870fa0c540bd21ee7f240673df052e0f4`. Batch C 승인 snapshot이며 전체 출시 승인과 구분한다.

### 10.3 한국어/일본어·문제·선행·Stable ID 검수

assistant가18개 전체 Pattern/Meaning/Explanation/Form/Usage/혼동 Note,72개 한일 예문·learning point,72문제·216선택지·정답/오답 해설을 한국어와 일본어 각각 재독했다. 관찰한 근거와 가능성, 발언의 종류·시점·출처, 원래 발화자/보고자/행위자/수혜자, 의향/약속/부탁과 공유/새 인식의 차이를 상황·Register로 설명했다. 독립 사람·외부 사전·공인 난도 검수는 NOT TESTED다.

교정40개 문자열의 전후/occurrences를 남겼다. 미수록 기 명사화·았/었다가·보니/으니·인용 축약·불필요한 겸양 복합을 줄이고, 일본어 혼입·번역 대응·발화 진위 보장처럼 읽힐 질문을 고쳤다. 마지막 휴일→定休日 번역을休み로 바꿔 정기 휴무라는 추가 의미를 없앴다. 같은 문구가 문제에서도 쓰이면 함께 바뀌므로40개 독립 문장 오류나 사람 승인이라는 뜻은 아니다. 들은/들을/들으라고/들을까요/들을수록의ㄷ변화와 듣는다고의유지, 만든/산다고/머네요의ㄹ탈락, 추운/도울게요의ㅂ변화, 게요/께요·을수록 띄어쓰기·물으셨어요/주실래요의높임도 검토했다. [REVIEW](Docs/DATA09_C_REVIEW.md), [항목별 payload hash](Docs/DATA09_C_EDITORIAL.json), [교정 전후](Docs/DATA09_C_EDITORIAL_CORRECTIONS.json), [전체 카탈로그](Docs/DATA09_C_REVIEW_CATALOG.md).

기존multiple_choice만 사용했다. meaning/form/context/contrast 각18문항,3선택지/정답1개,a/b/c각24개다. 의미 문제도18개 다른 지시문으로 직접 작성했고 인용·시점·사람 역할·선택/약속·Register를 섞었다. 가능한 다른 문형이 이 문맥에서 왜 다른 의도가 되는지 설명했다. 선택지216문구는 서로 다르고 예문은13~36자지만 이것이 자동 언어 품질/학습효과 보증은 아니다. 지정 기본형·시제·문맥에서 정답을 검사했으며 자유입력/복수 허용 답안이나 Conjugation 자동생성 form을 추가하지 않았다.

새 Pattern18 및 한일72문장 각각은 기존21 전체·Batch 내부 NFC/공백 정규화 중복0이다. 새169content ID+source citation ID1개는UUIDv4 최초1회 발급 후 고정했다. 기존 본문/ID/created_at/레슨 배치/질문/선택지/관계 행을 모두 보존한다. 새 비교/선행 관계의 기존 Grammar12개 끝점만revision+1/updated_at을 바꾸고 [allowlist](Content/data09-c-revised-ids.json) 밖 변경0을 검사했다. 물리 삭제·비활성화·UserProgress 재작성0이다.

C01→C02→C05/C06→C07~11, C12→C13→C14/C15, C16→C18 순서다. 대표 primary prerequisite1개·비교2개씩 연결했고 기존/A/B/C 선행 DAG 순환0이다. 앞 레슨/설명도 함께 필요하며 primary 관계가 모든 선행 mastery를 강제한다는 뜻은 아니다. 기존163후보 전체의 재연결·Level 재판정도 완료 수량에 넣지 않았다.

### 10.4 재개 후 실제 실행·검증 한계

- **PASS** strict21→22 전체 Importer/Validator: 오류0/기존경고10(짧은 발음예문5+기존 동형어 후보5). 별도 structural row audit는25테이블65,983행·오류0/기존경고5. 경고 삭제·Validator 완화0. integrity ok/FK0, 원본 행·DB 대조와31테이블 재구성·byte/SHA 일치.
- **PASS** Batch C 전용 **12/12**, 54.833초, 실패/오류/skip0,exit0. 모든 기존 행·정확한12revision·169신규UUID·정규화중복·실제 레슨/카드/검색SQL·72채점계약/18기대형·선행DAG·오류 입력 거부·고정authoring 재현·누적 목표 실제ID/DB count·진도 보존을 검사했다. 재개 후 저장한 [전용 원시 로그](Docs/DATA09_C_FOCUSED_TEST_LOG.txt).
- **PASS** 전체 `sh Tools/verify.sh --portable` **335/335**, 641.737초, 실패/오류/skip0,exit0. 기존323+신규12이며 전용 재실행을 합산하지 않는다. A19→20/B20→21의 정확한 gate는20/21 불변 fixture로 유지하고 C가 모든21→22 구행을 보존한다. 다른 live cohort도 현재count와 각Batch별 누적revision을 정확히 갱신했다. 기존 보존 assertion/Validator는 유지했다. [이번 전체 원시 로그](Docs/DATA09_C_PORTABLE_TEST_LOG.txt).
- **PASS(범위 한정)** 임시 UserProgress10에 B06문법의stage4/due900·typed favorite·진행 중grammar session(snapshot21/선택/페이지/revision)을 저장하고 콘텐츠 파일만21→22 교체했다. 새 관계로B06 revision이 바뀌어도 사용자DB SHA/JSON byte·cold reopen·기존due/favorite가 유지됐다. 기존1+새18 SRS 등록2회 후 중복0, SQLite조회 중socket금지. 실제 개인DB·Swift 상태전이 검사가 아니다.
- **BLOCKED/NOT TESTED** Linux/Python3.12.14,swift/xcodebuild없음. native137정의/실행0, iOS Debug/Release/SDK·실기기오디오/중단·메모리·3~10분 실측·개인진도·AdMob/StoreKit실행0. native 기대ContentVersion을22로 맞췄지만 build/XCTest를 실행했다고 주장하지 않는다. 독립 사람·외부 사전 한일 검수0. 새 P0/P1은 이번 범위에서 재현하지 않았지만 기존 native P1/B—Conditional gate는 해결로 바꾸지 않는다.

최종candidate는 `/tmp/data09-c-verification` 복사본에서 검증했다. Source/DB·실행 코드 hash가 같은지 확인한 뒤 실제 Production에 승격했고, 실제 원본을 Importer로 재구성한 DB도 번들과 byte/SHA가 같다. 편집 검수18개 payload hash 역시 최종candidate와 맞았다. [기계 판독 결과](Docs/DATA09_C_RESULTS.json). 자동/assistant/사람/iOS 검증을 구분한다.

### 10.5 재현·잔여 공백·Git 전달

```sh
python3 Tools/ContentBuilder/prepare_data09_c.py --output /tmp/data09-c-source.json --revised /tmp/data09-c-revised.json
python3 Tools/ContentBuilder/build_content.py Content/production.json /tmp/data09-c-rebuilt.sqlite --production --previous Tests/Fixtures/content-v21-production.sqlite --report /tmp/data09-c-build.json
python3 Tools/ContentBuilder/audit_data08_final.py Content/production.json --database Resources/content.sqlite --report /tmp/data09-c-structure.json
python3 -m unittest discover -s Tools/ContentBuilder -p test_data09_c_content.py -v
sh Tools/verify.sh --portable
```

prepare는불변21+고정UUID+검수authoring으로이번22만 재현한다. 최초발급 `--allocate-ids`를 재현에 넣거나 후속Production을 덮어쓰는 용도로 쓰지 않는다. canonicalSource는production.json 하나다. 원본/DDL/Importer/registry/검수근거·재생성가능번들·불변fixture를 모두 보존한다. 최대 추적 파일50MiB 미만 확인 후 일반commit/push·PR을 사용하며 LFS/forcepush/이력재작성/원본삭제는 필요하지 않다. 최종merge/main일치는 PR/Git과 최종응답이 기준이다.

미승인 원래 초안7개는 기 명사화, 게 부사형, 줄 알다/모르다, ㄹ 텐데, 다고 해서…것은 아니다, 기만 하다, 는 척하다다. 회상던/았던·일반 존경/겸양 전체체계·인용 축약/부정 범위·기존163후보 선행/Level재심사·신규예문 Listening/Dictation/직접입력 재사용·독립 사람/기기 검수도 남는다. 모든 예문 토큰의Dictionary등재·자동 활용 지원을 주장하지 않는다. **마지막 Batch C의 수량/콘텐츠 제작은 완료했고 후속 단계/DATA10은 시작하지 않는다.**


### 10.6 Git 전달 기록

콘텐츠 커밋 `b76b9c4230e5fc216068bbb313a1d0a5027e5dcf`를 `data09-4/grammar-batch-c`에 일반 push했고 성공했다. 대용량 파일 오류0, force push/LFS/원본 삭제/이력 재작성0. [PR #13](https://github.com/Raccoon26/Project-Hangul-Study/pull/13)을 main 대상으로 생성했다. 이 기록은 merge 전 전달 시점이며, 최종 merge/main 일치는 PR 상태·Git 이력과 최종 응답으로 확인한다.


## 11. DATA-09-5 / A~C 최종 품질 감사

### 11.1 시작·실제 검수 범위

2026-10-20 UTC, clean main/origin/main `b61866a7669bc1bf3fa2211fe45b08457b34cb0e`(PR #13)에서 `data09-5/final-content-audit`로 시작했다. 사전 미커밋 변경0. 실제 Content22/Schema4/reader7/UserProgress10과 기존 문서·A/B/C 원본/검수 기록을 대조했다. 현재22 Source SHA `13a6739bb93daee36426f04ac83b95f7244a62c227ea90b0ddda2d179eeeafeb`, DB SHA `22c3257b4204309158dfdea0f0bfd7d870fa0c540bd21ee7f240673df052e0f4`를 gzip/SQLite 불변 fixture로 보존했다. 기존 DEV01~14/DATA01~08·원래42 Grammar·A/B/C authoring·registry·과거 fixture·런타임 코드를 보호했다.

assistant가 신규 **Grammar54개(각 Batch18), 고유 신규 Example216개(각72), Question216개(각72), 선택지648개와 전 해설**, 기존 DATA08 재사용 예문4개를 실제 DB에서 재독했다. 한국어 형태·의미·품사 결합·시제·불규칙·띄어쓰기·Register, 일본어 의미/설명/문체·높임·수혜자·부정 범위와 유사 문법 차이를 대조했다. 기존 전체 Grammar96개나 입력 문제3,077개의 언어 전수 재검수로 확대 표현하지 않는다.

전수 재독과 별도로 고위험18개 Grammar의 form/constraints/confusion +첫 Example18개 +선택 Question18개/전 선택지·해설을 재감사했다. 무작위는 seed20261020095·각 Batch3 Grammar/6 Example/6 Question, 총45개를 한 번 추출한 뒤 교정 candidate에서 별도로 재독했다. 전수/고위험/무작위의 겹침은 독립 검수자·추가 콘텐츠 수로 합산하지 않는다. 독립 표시되는 성별 문맥3문항도 추가 확인했다. **검수 주체는 모두 AI 자체 검수이며 독립 원어민·교사 검수 및 외부 사전 대조는 NOT TESTED**다.

문법별 검토 메모·실제 ID는 [EDITORIAL](Docs/DATA09_FINAL_EDITORIAL.json), 고위험/무작위의 항목별 재독 근거는 [REAUDIT](Docs/DATA09_FINAL_REAUDIT.json), 전체 방법·한계·수정표는 [FINAL_REVIEW](Docs/DATA09_FINAL_REVIEW.md)에 있다.

### 11.2 교정·버전·수량 보존

**13개 사항 /25개 ID /31필드**를 교정했다. 소유 엔티티는 Grammar9·Example8·Question8이며, 선택지3필드의 소유자는 해당 Question이다. `들려면`의 기본형(들다), 면의 일반·반복 조건, 니까의 근거 범위, 때절의 상대적 시제, 고 있다의 결과 유지 용법, 현재 추측 장면의 특정, 늦은 회의 종료의 원인 단정, 일본어 `数日間早寝`와 김에 설명, 신청 주체, 미도입 으니→니까, 노출된 내부 P25/P26, 동생의 성별 Note/독립 문항 장면을 수정했다. 으니 자체나 남동생 장면의 弟 번역을 비문으로 판정한 것이 아니다. 정확한 before/after/이유는 [manifest](Content/data09-final-corrections.json).

본문 교정으로 **Content22→23**, Schema4/reader7/UserProgress10 유지. 기존 Stable ID/kind/created_at/정답 choice ID/answer_json/선택지 ordinal/관계/Level/학습 순서를 보존하고 [25개 소유 ID](Content/data09-final-revised-ids.json)의 revision만1 증가했다. 신규·삭제·비활성화·진도 재작성0. 구 A/B/C authoring은 당시 근거로 보존하고, 현재 canonical Source는 production.json이다. `prepare_data09_final.py`는 동결22+명시 manifest로 같은23만 재현한다. C21→22 검사는22 불변 fixture로 고정하여 당시 assertion을 그대로 유지하고 새22→23 exact delta 검사를 추가했다.

A/B/C 신규 수량은 **54 Grammar /216고유 Example /216 Grammar Question**, 전체 목표45~60/180~300/180~300 충족 유지. 기존4개 예문 재사용은 신규로 계산하지 않는다. 장기 Grammar/Expressions350~500 목표를 유지하며 현재96 대비254~404개가 남는다.

### 11.3 DATA08 선행 후보163건

이전163개 ID·한국어·일본어·원래 분류를 보존하고 각 문장을 다시 읽어 [FINAL_PREREQUISITES](Docs/DATA09_FINAL_PREREQUISITES.json)에 판단·실제 지원 Grammar ID·미해결 이유를 기록했다.

| 원래 분류 | 해결 | 교육적으로 허용 가능 | 미해결 |
| --- | ---: | ---: | ---: |
| 부족 문법147 | 120 | 4 | 23 |
| Level·배치 검토8 | 0 | 0 | 8 |
| 단순 검토8 | 0 | 3 | 5 |
| **총163** | **120** | **7** | **36** |

‘해결’은 지적된 문형의 설명 범위를 현재 카드로 지원할 수 있다는 뜻이며, 모든 단어·부수 문형 숙달·사람 승인·실제 배치 완료가 아니다. N이라도 차선 선택만으로 신분/규모 양보를 해결하지 않았고, 평서 인용 수식만으로 달라는 요구/기다리라는 말투를 승인하지 않았다. P34 이유 일반화 부정, 고 나니/으니 발견, 려는·기 명사화·게 부사화·는 게 낫다·아어하다·아어두다·은 끝에·아어서는 안되다 등의 범위와 Level8건을 남겼다. 이번163건의 원문/Level/관계 변경·새 재사용 승인0. 기존 Batch B의 승인 재사용4개는 별도 flag로 표시하고 그대로 보존했다.

### 11.4 객관식·입력·교육적 한계

신규216문제는 모두 단일 객관식·각3선택지/정답1개. 문맥이 부족했던 F01/F07/F09 및 독립 성별 문맥3문항을 교정했고 정답·choice ID는 그대로다. C17의 `들을 수록`/`들을수록`은 의도된 띄어쓰기 구별이다. 감사 도구 개발 중 공백을 지운 중복 검사로 이 문항을 오탐1건 냈고, 문항의 지식 목표에 맞춰 선택지 내부 공백을 보존했다. 기존 Validator나 문항을 삭제/완화한 것이 아니다.

신규 문법용 직접입력은 **0 / 적용 대상 없음**. 기존 text_input1,227/listening_input1,850개는 accepted nonempty·정규화 중복 계약 전수 자동 확인, 기존 Swift ProductionAnswer 코드와 portable 회귀 범위를 대조했다. Swift 판정·IME·실제 iOS 입력 실행은 BLOCKED다. 일반 입력은 NFC/공백과 exact/spacing/incorrect를 구분하고, 끝 .!? 생략은 dictation에만 적용한다. 기존 엔진의9형 생성과 새54개 문형 전체 자동 생성을 혼동하지 않는다.

A/B 기본 의미 선택 프레임36개 등 교육적 반복성·변별도·실제 학습효과는 사람/학습자 검증이 남는다. 주선행 DAG는 순환/단원 순서 역참조0이나 예문 속 모든 부수 문형의 선행 숙달은 별도다. A10의 대화할 시간, A18의 신청할 때 등 공통 기초보다 먼저 보이는 조합은 사전 리뷰/도움말·수업 순서 검토가 필요하며 기존 단원 순서를 임의 변경하지 않았다. 미해결36개를 완료로 바꾸거나 이번 단계에서 새 문형·듣기·직접입력·통합 단계를 시작하지 않는다.

진행 중 GrammarSession은 문항 본문·해설·선택지를 포함한 bounded snapshot을 보존한다(Models/GrammarModels.swift, GrammarLearning.expose). 따라서 이번 교정은 Content23에서 새로 읽는 문항에 적용되며, 이미 저장된 세션의 과거 문구를 소급 재작성하지 않았다. 정답 ID를 유지해 기존 판정 계약을 보존했지만 실제 iOS Resume 확인은 BLOCKED다.

### 11.5 실제 자동 검사·Production 반영

- **PASS** 최종 candidate23에서 `sh Tools/verify.sh --portable`: **346/346**, 380.927초, failures/errors/skipped0, exit0. 전용11/11,16.794초, exit0. 첫28필드 candidate는345/345 PASS였으나 독립 성별 문맥3문항을 추가 교정한 뒤 전체를 다시 실행했다. 첫 결과는 PRELIMINARY 로그에 분리했으며 최종 검증으로 대체하지 않았다.
- **PASS** 기존 Importer·strict `--previous content-v22-production.sqlite`:0errors/기존10warnings(발음 단문5/기존 동형어5), 25개 Source 테이블65,983행·FK0·integrity ok. DATA08 구조 감사0errors/기존5warnings. DATA09 전용 계약0errors/0warnings. 기존 오형태/과도한 단정7개 문구를 Production 전 범위 재검색해 재등장0을 확인했다. broader trigger의 정상 문장·의도된 오답은 무조건 치환하지 않았다.
- **PASS** 전체96 Grammar/주선행73간선 DAG:순환0·누락 target0. 이 검사는 모든 예문의 부수 문형 선행 학습 완료를 뜻하지 않는다.
- **PASS** candidate 전체 검증 전후244개 코드/테스트/입력 SHA 일치, 기존 fixture·Batch 근거·런타임147개 파일을 baseline SHA와 대조해 보존. 검증 완료 candidate만 Production Source/DB로 반영했고, 실제 Production Source를 Importer로 다시 만들어 DB31개 테이블/파생 index/schema를 포함해 **byte/SHA까지 동일**함을 확인했다.
- **PASS / SQL 한정** 실제 repository SQL·임시 user10 디스크에 Content22→23 교체 시 기존 SRS stage4/due900·Favorites·부분 session snapshot 보존 및 중복 등록 시 due 불변 확인. 기존 전체 portable 통합·회귀도 통과했다. 실제 개인 DB·Swift Resume 실행과 혼동하지 않는다.
- **BLOCKED** xcodebuild/swift 실행 파일 없음. iOS Debug/Release/SDK·XCTest137정의/실행0·실기기 음성/IME/중단/메모리/3~10분·AdMob/StoreKit 미실행. **NOT TESTED** 독립 원어민·교사/외부 사전 검수. 새 P0/P1 런타임 오류는 이번 실행 범위에서 재현하지 않았고 기존 native P1 gate/B—Conditional은 유지한다.

| Level | Vocabulary | Example | Grammar | Question |
| --- | ---: | ---: | ---: | ---: |
| 한글 | 0 | 0 | 0 | 59 |
| 入門 | 306 | 659(발음13 포함) | 22 | 156 |
| 初級 | 800 | 1,577 | 20 | 134 |
| 初中級 | 1,181 | 2,577 | 54 | 3,204 |
| **전체** | **2,287** | **4,813(문장4,800)** | **96** | **3,553** |

Meaning2,420/Listening1,936/Course8/Lesson103/content_items15,935/grammar_examples389로 수량 변화0. Source SHA `c8a74e3b61809aabe5d2dd88768446f986792f2585d40ef78327c50b2b6c5b1e`, DB SHA `0a4051d3c5423441b50348935d64559504f1553a55fd3ea472c84b40c9ebc025`. JSON/SQLite 원본을 삭제하거나 Git 이력을 재작성하지 않았다. 새22 DB fixture18,812,928 bytes 및 gzip 원본2,459,174 bytes는100MiB 제한 아래라 LFS 전환은 필요하지 않았다.

근거: [실제 결과](Docs/DATA09_FINAL_RESULTS.json), [전체 로그](Docs/DATA09_FINAL_TEST_LOG.txt), [전용 로그](Docs/DATA09_FINAL_FOCUSED_LOG.txt), [strict build](Docs/DATA09_FINAL_BUILD.json), [실제 Production 재구성](Docs/DATA09_FINAL_RECONSTRUCTION.json), [Source/DB 수량](Docs/DATA09_FINAL_COUNTS.json), [입력 SHA](Docs/DATA09_FINAL_VERIFIED_INPUTS.json). `PROJECT_STATUS.md`, `CONTENT_GUIDE.md`, `DATA_PROGRESS.md`, `RELEASE_CHECKLIST.md`, `AGENTS.md`를 실제23과 미검증 gate에 맞춰 갱신했다. **DATA09-5에서 종료하며 DATA09-6/DATA10은 시작하지 않았다.**


### 11.6 Git 전달

콘텐츠/검수 commit `d3722f5e9e11480914fd453862595f06df3be5cf`를 `data09-5/final-content-audit`에 정상 push했다. [PR #14](https://github.com/Raccoon26/Project-Hangul-Study/pull/14)를 main 대상으로 생성했다. 기존 변경 손실·원본 삭제·이력 재작성·force push0, 신규 최대 blob18,812,928 bytes로 일반 Git push 성공. GitHub에 등록된 check는0개이며 로컬 portable PASS를 GitHub/native CI 실행으로 바꾸지 않는다. 최종 문서 전달 commit 및 main merge SHA/상태는 해당 PR의 head/merge 기록과 최종 응답을 따른다. 이 전달은 DATA09-5 범위이며 다음 단계는 시작하지 않는다.


## 12. DATA-09-6 / Production·실제 Curriculum 통합

### 12.1 시작·Content19와 실제 직전 버전 보존

clean main/origin/main `d1c7b5cd42773f156a421139e905f61994b905ca`(PR #14)에서 `data09-6/production-integration`로 시작했다. 기존 미커밋 변경0. 사용자가 지정한 Content19는 DATA09 시작 전 원본이며, 실제 업데이트 직전 Production은 이미 Content23/Schema4/reader7/UserProgress10이다. **19를23으로 덮어쓰거나 현재 DB를19라고 재명명하지 않았다.** 기존19 원본/DB fixture를 보존하고 실제23 원본/DB도 별도 불변 fixture에 저장했다. 두 기준 모두 대상으로 strict previous-version 검증을 수행한다.

- Content19 DB SHA `57aeaf918d5eaaec3bbfaed02f87c5452cca8264540b923a70448b781adbe9e5`, gzip 해제 Source SHA `f97b3bd70d07a3945770b8d6940c4a53e29a9b70b565caf21fb927230c08b4a8`.
- Content23 DB SHA `0a4051d3c5423441b50348935d64559504f1553a55fd3ea472c84b40c9ebc025`, Source SHA `c8a74e3b61809aabe5d2dd88768446f986792f2585d40ef78327c50b2b6c5b1e`.

PROJECT_STATUS/CONTENT_GUIDE/DATA_PROGRESS/RELEASE_CHECKLIST/AGENTS/DATA08_PROGRESS/DATA08_CLOSEOUT/DATA09_PROGRESS·실제 Source/DB·Grammar/Curriculum/Lookup/Production/SRS/Statistics/Resume 경로를 대조했다. A/B/C 및 최종 검수 원본·registry·과거 fixture·UserProgress schema를 보존한다. [보존 해시](Docs/DATA09_INTEGRATION_PRESERVATION.json).

### 12.2 단원·선행 복습·실제 모듈 연결

기존 신규54개 Grammar는 이미3개 코스/18개 레슨에 있었다. 기존 Course/Lesson/Grammar ID·lesson membership·ordinal·진행 중 snapshot 순서를 유지하면서, **6개 Unit tag**로 각 코스의6레슨을 두 단원(각3레슨)으로 묶었다. 실제 Grammar 목록 SQL이 코스명·단원명을 읽어 표시한다. 레슨당3개 문법·4문제/문법을 유지해 단원 전체를 한 세션으로 강제하지 않는다. Unit은 기존 tag/item_tags 구조를 사용하므로 Schema4 유지다.

| Course | Unit | 기존 Lesson ordinal |
| --- | --- | --- |
| 이유부터 계획 | 理由・変化・条件 | 47~49 |
| 이유부터 계획 | 目的・方針・必要性 | 50~52 |
| 대조와 경험 | 時間・途中・結果状態 | 53~55 |
| 대조와 경험 | 対照・経験・機会 | 56~58 |
| 추측과 회화 의도 | 修飾・推測・引用 | 59~61 |
| 추측과 회화 의도 | 伝える意図・会話の態度 | 62~64 |

검수 예문에서 필요한 일반 관형·명사화·시간·배경·결과/목표 상태 **선행 참조20개**를 실제 Grammar ID로 보강했다. A10→C01, A18→B01, B16→C02, C14→B03/B07, C17→A05 등이 포함된다. 레슨 순서를 뒤집는 대신 문법 첫 설명의 `先に確認したい形`에서 해당 카드의 뜻·형태·설명을 먼저 읽을 수 있다. 선행 참조는 강제 잠금/자동 학습 완료가 아니며, 이미 아는 사람은 짧게 넘어갈 수 있다. 물리적 레슨 ordinal이 모든 부수 문형의 위상 순서라는 주장도 하지 않는다. 새 선행 DAG와 실제 preview를 함께 검증한다.

54개 Grammar에 예문 문맥을 근거로 **35개 기존 어휘로 향하는 관련 관계54개**를 연결했다. 한국어 기본형과 실제 Dictionary 의미를 개별 대조했다. 동의어·자동 형태분석 결과로 표시하지 않는다. 관련어는 문법 학습에서 사전 sheet를 열어 뜻·기존 활용·저장·최근/어려운 항목 경로로 이어지며 기존 사전의 양방향 related 조회도 같은 참조를 사용한다. 기존 재사용 예문4개를 통한 관련어 경로도 보존한다.

이35개 어휘 중6개에는 기존 검수 입력26문제(형태19/문장4/빈칸3)가 있어12개 Grammar에서 해당 입력 연습으로 이어진다. `VocabularyDetail.hasProductionPractice`에 따라 실제 문제가 있을 때만 `活用・入力を練習`을 노출한다. 나머지 관련어의 사전 활용표와 문법 자체의 객관식을,54개 새 문형 전부의 자동 문장 생성/직접입력 지원으로 부풀리지 않는다. 신규 Grammar/Example/Question 추가0, DATA09 누적54/216/216·기존 예문4개 재사용 유지.

### 12.3 발견·수정한 연결 문제와 보존 정책

- **예문 검수 Note 누락 수정:** 기존 grammarExamples SQL/Example 모델이 `learning_point_ja`를 버려, DATA09의 일본인 학습자 Note와 동생 성별 장면 설명이 화면까지 전달되지 않았다. 기존 열을 읽어 비영속 Example 모델에 전달하고 GrammarExampleView에서 표시한다. B03/B11/B16/C11의 실제 예문으로 회귀 검사한다. DB 문장·번역·Note 본문은 바꾸지 않았다.
- **단원·선행 안내 연결 보완:** 기존3코스·18레슨은 문법 평면 목록에만 보였고 prerequisite 관계는 학습 설명에서 읽지 않았다. 코스/단원 표시와 최대8개 선행 카드의 선택적 사전 복습을 기존 학습 화면에 연결했다. 더 일반적인 관형형이 뒷단원이라는 문제에 대해, 기존 세션의 순서·진도를 바꾸지 않고 기초 설명에 먼저 접근할 수 있게 했다.
- **관련어·입력 진입 보완:** 새 문법은 기존 공유 예문4개 외에는 어휘로 이어지는 명시 참조가 부족했다. 검토된54개 related 관계를 사전 양방향 조회에 포함하고, 실제 입력 문제가 있는 어휘만 기존 ProductionStudyView로 진입시킨다. 별도 채점 엔진·SRS·진도 DB를 만들지 않았다.

관계·태그 변경이므로 후보는 Content24, Schema4/reader7/UserProgress10 유지다. 새 content UUID는 Unit tag6개뿐이다. 변경된 기존107개(Grammar54/어휘35/Lesson18)의 revision·updated_at만 정책대로1 증가시킨다. 새 관계74개(선행20+관련어54)와 Unit membership18개이며 기존 관계·태그·배치를 삭제하지 않는다. [고정 ID/배치/관계 manifest](Content/data09-integration-ids.json), [승인 revision](Content/data09-integration-revised-ids.json), `prepare_data09_integration.py`가 동결23에서 같은24를 재현한다.

기존 질문·정답/choice ID·문법/예문 본문·Vocabulary sort key·Listening order는 유지한다. 진행 중 GrammarSession의 문항 snapshot/선택/페이지/ContentVersion과 기존 어휘 세트 membership을 재작성하지 않는다. 선행 설명·사전 조회만으로 완료나 SRS를 새로 등록하지 않는다. 기존19→24와23→24 교체를 별도 임시 사용자 디스크에서 확인하며 실제 개인DB를 수정하지 않는다.

### 12.4 검사 범위·초기 검사 수정

전용13개 검사에서19/23 fixture 해시 및 두 strict gate·재구성 byte 일치·107개 endpoint revision·신규6개 Unit·모든54개 실제 레슨/카드/질문·220개 예문 placement·Note reader/view·선행 DAG·사전/입력/검색·네트워크 금지·모든 사용자 테이블/설정/통계/어려운 항목·5/10/20 복습·중복 SRS와 rollback을 검사한다. SQL 실행과 Swift 실행을 구분한다.

첫 전용 실행은13검사 중4 failure였다. 두 upgrade subcase의 가상 SRS seed에 Difficult 판정 필드(consecutiveSuccesses/lastResult)가 빠진 것, 코스/단원 SQL 열 번호 오기, 변경된 ANALYZE 통계(sqlite_stat1)를 불변 본문처럼 비교한 검사 문제가 원인이었다. seed와 열 번호를 수정하고 optimizer 통계는 불변 본문 비교에서 제외했다. **strict 재구성은 sqlite_stat1을 포함한 DB 전체 byte 일치를 계속 요구**한다. Production 데이터를 삭제하거나 Validator를 완화하지 않았다. 정정 후 전용 **13/13 PASS(20.361초)**. 초기 로그와 최종 전용 로그를 구분해 보존했다.

고아 문항은 `question_target`/lesson/audio 관계뿐 아니라 `questions.listening_id` 소유 경로도 포함해 검사했다. 이를 빼면 기존 정상 듣기1,849문항을 잘못 고아로 세므로 삭제·재연결하지 않았다. 정의를 명시한 전수 검사에서 Grammar/Lesson, Example/의미·문법·발음, Question/학습 소유, Vocabulary/Meaning, Course/Lesson 고아0이다. [소유 경로·결과](Docs/DATA09_INTEGRATION_ORPHANS.json).

native 회귀2개를 추가했다(전체139정의). 실제54개 카드/6단원/선행·Note·어휘 활용/입력 연결과 初中級 grammar 회독/SRS/cold resume를 대상으로 한다. 재사용 예문에서 연결되는 명사·부사·expression은 활용표가 없으므로, native 회귀의 기대값을 용언/그 외 품사로 구분했다. 이 작성상 정정 후 최종 파일 snapshot으로 전체 portable 검사를 다시 수행한다. **Xcode/Swift가 없어 native 실행0/BLOCKED**다.

전용 upgrade fixture는 이후 실제19/23 DB의 Grammar/Lesson/Question/입력 대상 어휘/Listening ID를 사용하도록 강화했다. 교체 후 같은 ID로 실제 repository 조회가 가능한지도 확인하고 전용13/13을 재실행했다(**22.336초**). JSON은 SQL 보존 검사용 fixture이며 Swift Codable/상태전이 실행으로 인증하지 않는다.

첫 전체 portable 실행은 **359개 실행/실패0/오류4,418.495초,exit1**이었다. Data04 및 A/B/C의 레슨 조회 검사가 기존4열을 고정 unpack해서, 새 코스/단원2열이 추가된6열 결과를 받지 못한 오류다. 레슨 ID/수량 assertion은 유지한 채 실제 행의 첫4열을 사용하도록 고쳤다. 해당4개 회귀는 **4/4 PASS(0.763초)**. 수정 전 재실행은 SUPERSEDED 로그로 분리하고, 최종 파일 전체 snapshot에서 portable를 새로 실행한다. 실패·중간 검사를 PASS로 덮어쓰지 않는다.

수정 전6열 unpack을 고치기 전에 시작한 중간 전체 실행도359개/오류4/실패0(425.021초,exit1)로 종료했다. 이 결과 역시 SUPERSEDED 원시 로그에 실패 상태 그대로 보존하며 최종 PASS에 합산하지 않는다.

설정 검사는 임시 SQLite의 opaque metadata 보존 범위다. 실제 UserDefaults/Keychain의 설정·광고 제거 권한·기기 상태 이전은 별도 native 검증이 필요하며 BLOCKED로 남긴다. 해당 서비스/저장 키 코드는 변경하지 않았다.

### 12.5 최종 자동 검사·실제 Production 반영

- **PASS** 최종 파일 snapshot의 `sh Tools/verify.sh --portable`: **359/359**,420.142초, failures/errors/skipped0,exit0. 기존346+신규13이며 별도 전용/조회 재실행 수는 합산하지 않는다. 전용13/13(22.336초), 조회 형식 회귀4/4(0.763초)도 PASS. 초기 실패/오류 로그는 그대로 보존했다.
- **PASS** 실제19·23 보존 해시와 strict previous-version gate 모두0errors/기존10warnings. A/B/C/최종 검수의20/21/22/23 fixture와 정확한 gate를 유지했다. 변경107개와 신규 Unit6개 이외 모든 기존 payload·관계·배치·ID/kind/created_at을 보존한다.
- **PASS** 검증 전후251개 코드/테스트/입력 SHA를 대조하고 검증 완료24만 Production Source/DB에 반영했다. 실제 Production Source에서19/23을 previous로 각각 다시 빌드해 **두 DB 모두 현재 Resources/content.sqlite와 byte/SHA까지 동일**함을 확인했다. Source25테이블66,094행, DB31테이블, integrity ok/FK0. 원본 JSON·과거 fixture·대용량 원본을 삭제/재작성하지 않았다.
- **PASS** DATA09 계약0errors/0warnings, DATA08 구조 감사0errors/기존5단문warnings. 전체96 Grammar의 선행93간선 DAG 순환0·참조 누락0. 소유 경로를 포함한 Grammar/Example/Question/Vocabulary/Course 고아0. 기존 동형어 경고를 중복 오류라고 삭제/병합하지 않는다.
- **PASS / SQL·디스크 범위**54개/18레슨/6단원·216문제·220예문 placement, 새 Note·선행/관련어·사전/입력/검색,19/23 실제 콘텐츠 ID로 모든 사용자 테이블/snapshot·통계·어려운 항목·Favorites 보존, SRS54개 중복 등록2회 후 기존stage4/due900 유지, 실패 transaction rollback,5/10/20 복습 경계, 네트워크 금지 조회를 실행했다. 실제 개인DB·Swift 상태전이를 실행했다고 주장하지 않는다.
- **PASS / 로컬 warm SQL 성능** 동일 환경30회 측정의24 p95: Home4.6853ms, 넓은 검색4.1834ms, Grammar catalog1.1135ms, 전체 card2.2933ms, Grammar SRS due20 headers1.9652ms,3항목 session commit0.1683ms.23/19 기준 원시값을 함께 보존했다. 작은 레슨·즉시 transaction 저장·bounded 조회/scroll/44pt/선택적 프리뷰 정책을 유지한다. iPhone UI·RAM·3~10분 실측 보증이 아니다.
- **BLOCKED** xcodebuild/swift 없음. iOS Debug/Release·SDK·139 XCTest(실행0), 실제 Resume/비행기 모드/TTS·접근성/큰 글씨/VoiceOver·메모리·중단/3~10분·StoreKit/AdMob/UserDefaults/Keychain 기기 검증은 미실행이다. **NOT TESTED** 독립 원어민·교사/외부 사전 검수. 기존 native P1/B—Conditional·미해결36건을 해결로 바꾸지 않는다.

최종 Content24/Schema4/reader7/UserProgress10, Vocabulary2,287/Meaning2,420/Example4,813(문장4,800+발음13)/Grammar96(入門22/初級20/初中級54)/Question3,553(Grammar300)/Listening1,936/Course8/Lesson103. 신규 수량54/216/216과 목표45~60/180~300/180~300, 장기350~500 유지. content_items15,941·tags103·content_links6,499·grammar_examples389. 단원 태그나 재사용 관계를 신규 문법/예문/문제로 합산하지 않는다.

Source SHA `081ed35c7cd78345af1c1793fc450acaa2931f173cef00aaa960c8ef42318540`, DB SHA `56a7fa8b5358e254eeb324e706860d150d20c8ec013ba0b6f602cf14d93cceff`. [결과](Docs/DATA09_INTEGRATION_RESULTS.json), [전체 로그](Docs/DATA09_INTEGRATION_TEST_LOG.txt), [전용 로그](Docs/DATA09_INTEGRATION_FOCUSED_LOG.txt), [19 기준 실제 재구성](Docs/DATA09_INTEGRATION_RECONSTRUCTION19.json), [23 기준 실제 재구성](Docs/DATA09_INTEGRATION_RECONSTRUCTION23.json), [수량·배치](Docs/DATA09_INTEGRATION_COUNTS.json), [성능](Docs/DATA09_INTEGRATION_PERFORMANCE.json), [범위·미검증](Docs/DATA09_INTEGRATION.md). 상위 상태/콘텐츠/릴리스 문서와 AGENTS를 실제24 및 미완료 gate에 맞췄다. **DATA09-6에서 종료하며 DATA09-7/DATA10은 시작하지 않았다.**


### 12.6 Git 전달

통합/검증 commit `dc3809e04154e30d6e548439f6fe41033fd576dd`를 `data09-6/production-integration`에 정상 push하고 [PR #15](https://github.com/Raccoon26/Project-Hangul-Study/pull/15)를 main 대상으로 생성했다. 최대 신규 blob18,841,600 bytes로 일반 Git push 성공. Content 원본·기존 fixture 보존, force push/이력 재작성/LFS 전환0. 초기 unittest subtest의 행끝 공백1개는 원시 로그 보존을 위해 그대로 두고 해당 원시 로그를 제외한 소스/문서 whitespace 검사를 수행했다. GitHub 등록 check0개이므로 로컬 portable PASS를 GitHub CI/native 실행으로 표현하지 않는다. 최종 전달 문서 commit과 main merge SHA/상태는 해당 PR head/merge 기록 및 최종 응답을 따른다. 이번은 DATA09-6에서 종료한다.


## 13. DATA-09-7 / 요구사항·전체 모듈 회귀 감사

### 13.1 시작·명세·실제 범위

2026-10-20 UTC. fetch 후 main `fcb7897b8bf78ce138e1941d9e678d9c22128aed`와 origin/main 일치·미커밋 변경0을 확인하고 `data09-7/system-audit`에서 작업했다. 기존 DEV01~14/DATA01~08와 DATA09 문서·코드·현재 Production을 대조했다. 원래 DEV01~14/DATA01~07 완전 명세는 현재 tracked 경로 및 접근 가능한 Git history의 SPEC/REQUIREMENT 이름에서 찾지 못했다. 사후 STATUS/REVIEW21개를 원래 전체 요청으로 오인하지 않으며 확인 불가능한 원래 세부 수락조건은 UNVERIFIABLE이다. [요구 대조표](Docs/DATA09_SYSTEM_REVIEW.md), [원문 요청](Docs/DATA09_SYSTEM_REQUEST.md), [경로/해시·실제 SQL 감사](Docs/DATA09_SYSTEM_AUDIT.json).

이번은 상태·연결 회귀 감사다. runtime 코드·Production Source/DB·ID/revision·level·lesson/order 변경0이다. Content24/Schema4/reader7/UserProgress10, 신규54G/216고유E/216Q·기존4예문 재사용·DATA08 신규911V/1,821고유문장 및 장기350~500을 유지한다. 전체 Vocabulary2,287/Meaning2,420/Example4,813/Grammar96/Question3,553/Listening1,936/Course8/Lesson103, Source25테이블66,094행·비활성0. Level 집계는 [COUNTS](Docs/DATA09_SYSTEM_COUNTS.json).

### 13.2 전수 연결·오류·기존 P1 추적

Content→Curriculum→Vocabulary→Grammar→Conjugation/입력→Listening→SRS→Search→Statistics/UserProgress의 실제 repository SQL을 조회했다. 전3,553문제/4,813예문 도달·누락0,300문법 문항의 단일 target/choice/실제 예문 관계,96문법/30레슨의 고유 bounded membership을 확인했다. 어휘2,287한국어 검색·72일본어뜻 표본,96문법의 한일192검색도 PASS다. 이것은 Swift 엔진/UI를 실행한 E2E가 아니다.

96문법/93선행 edge 순환·자기참조·잘못된 target0. 실제 curriculum ordinal 기준 후행 참조12개는 설명 프리뷰로 확인할 수 있다. 기존 snapshot/lesson순서를 재작성하지 않았다. 선행163후보의120해결/7조건부/36미해결·Level검토8미해결은 새 언어 재분류 없이 유지하며 전체 선행 숙달/최적 순서 완료로 주장하지 않는다.

DATA08 P1-01 unavailable 복습 보류: 원SRS/due/review_items/events 유지·완료/보류 구분·cold reopen/rollback·release별 재확인 PASS. P1-02 끝 .!? 생략: 현1,850dictation corpus/현재 source route PASS, DATA08 영향1,821개 유지·일반 입력 정규화 불변. P1-03 listening45due/첫25retire→두번째 page15active 도달·원SRS45보존/나머지5pending SQL PASS. 세 건의 native API/UI/실제 Swift grading 확인은 여전히 BLOCKED다. 전용10/10(0.126초)은 전체 suite와 중복이다.

새 런타임 P0/P1 재현0·수정0이다. 새 portable6개는 전300문항/30레슨, 잘못 선택한 문항 snapshot의 cold reopen/새 콘텐츠 보존, 늦은 저장 실패 시 답안·이벤트·통계·Resume timestamp 동시 rollback, UUID 중복 거부/통계 불변과 native guard 소스 계약을 보강했다. native2개(18신규 레슨 전체 실제 Quiz→회독/SRS→Resume·오답/중복 Progress)는 작성했지만 실행0이다.

부분 구현/위험은 보고서에 유지했다: 일반 Validator 전체 prerequisite cycle gate 없음(현재 DAG 별도 검사), 고정 회독 retire 자동대체 없음, 새54문형 전체 직접입력/듣기 생성 없음,9형 외 활용/ㅎ사전 override·자유작문/상위과정/검증 녹음/혼합 scheduler/원격 update 부분. 실제 Dead Button/crash/audio/기기 메모리·오프라인/3~10분은 미실행이다.

### 13.3 실제 실행 결과·한계

- **PASS** `sh Tools/verify.sh --portable`: **365/365,415.721초,실패0/오류0/skip0,exit0**. Python Unit/SQL Integration/Regression이며 Swift XCTest가 아니다. 전용6/6(0.071초)·기존P1 10/10은 포함된 검사로 중복 가산하지 않는다. [전체 로그](Docs/DATA09_SYSTEM_TEST_LOG.txt), [결과](Docs/DATA09_SYSTEM_RESULTS.json).
- **PASS** 현재19→24/23→24 strict rebuild:0errors/기존10warnings, DB byte 일치. DATA08 구조0errors/5warnings, DATA09 계약0/0, integrity ok/FK0. user1~10 migration·진행중 다종 snapshot/선택·Favorites/Difficult/SRS·통계·Resume·socket 금지 Offline SQL·15k규모 회귀 재실행. 실제 개인진도·Swift Codable·UserDefaults/Keychain은 이 SQL fixture 실행으로 인증하지 않는다.
- **FAIL→수정** 새 전용 초기6개 중1ERROR는 exposed_at 누락 fixture CHECK 위반. 실제 노출 상태로 수정·constraint 유지. 추가 audit 초기 learning_order 조회 오류는 실제 lesson/item ordinal로 수정. 초기 원시 로그 보존, 앱 버그 수정 수에 넣지 않는다.
- **PASS(로컬 SQL 측정)** warm30회 p95 Home7.7807ms/Search넓은검색6.1627ms/Grammar catalog0.9404ms/fullcard2.1516ms/SRS20 headers2.2862ms/3개 session commit0.1770ms. [실측](Docs/DATA09_SYSTEM_PERFORMANCE.json). Python SQLite/공유 Linux이며 iPhone 성능/메모리/학습시간 보장이 아니다.
- **PASS(소스·저장 경계)** 광고/구매/설정4파일은 시작 commit과 byte 동일. remove_ads·Keychain/빈도/preferences key는 Content Version 독립. 기존 monetization checker/회귀 유지. opaque cache SQL 검사를 실제 권한 실행으로 표현하지 않는다.
- **BLOCKED** Linux에 xcodebuild/swift 없음. iOS Debug/Release/SDK resolve·141정의 XCTest(기존139+이번2) 실행0·실기기 Resume/비행기/TTS/Audio interruption·IME/접근성/메모리/3~10분·AdMob/StoreKit/Keychain/UserDefaults 미실행. **NOT TESTED** 독립 원어민·교사/외부 사전. **UNVERIFIABLE** 미확보 옛 전체 원래 명세.

### 13.4 보존·Git·종료

Source SHA `081ed35c7cd78345af1c1793fc450acaa2931f173cef00aaa960c8ef42318540`, bundle SHA `56a7fa8b5358e254eeb324e706860d150d20c8ec013ba0b6f602cf14d93cceff`를 전체 검사 후에도 확인했다. 기존 원본/DB/fixture/ID/미완료 gate를 보존하고 감사만으로 Content/Schema Version을 올리지 않았다. 기존 명시적 위임에 따라 정상 commit/push/PR/merge로 전달하며 최종 SHA/PR/clean main은 Git 및 최종 응답이 기준이다. Force push/이력 재작성0.

이번 범위의 미수정 재현 P0/P1 0과 iOS/native P1 확인 미완료를 구분한다. B—Conditional·선행36건·독립 사람 NOT TESTED를 유지한다. **DATA-09-7에서 종료하며 다음 단계/DATA10은 시작하지 않았다.**

### 13.5 Git 전달 기록

검증된 감사/회귀 commit `4e25c574a5fe019bcb71338a85be9a34cf307f35`를 `data09-7/system-audit`로 정상 push했다. 전달 PR은 [#16](https://github.com/Raccoon26/Project-Hangul-Study/pull/16)이다. GitHub status check 등록은 없으므로 원격 CI PASS로 표현하지 않고 보존한 로컬365 PASS만 근거로 삼는다. 이 기록 추가는 문서만 변경하며 실행 코드/검증 입력은 불변이다. 사용자 위임에 따라 정상 merge로 전달하며 최종 merge SHA·상태·clean main 일치는 해당 PR/Git과 최종 응답이 기준이다.


## 14. DATA-09-8 / 최종 종료·재구성·Git 전달

### 14.1 기준선·Batch·품질·목표 재확인

2026-10-20 UTC, clean main/origin/main `542816ccf1a8ce25a8a4865cbd8f2a7fcb73c03e`에서 fetch 후 `data09-8/final-closeout`으로 작업했다. Content19의 Grammar42부터 A20=60/B21=78/C22=96/교정23=96/통합24=96/시스템24까지 실제 fixture·현재 DB와 당시 수량 보고서를 대조했다. 신규 각18G/72E/72Q, 누적54G/216고유E/216Q로45~60/180~300/180~300 목표를 충족한다. 기존 예문4개 재사용은 신규에서 제외하고 장기350~500 목표를 유지한다.

54개는 생산적인 문법 구조·종결어미다. 별도 고정 Expression0, 신규 Vocabulary0이며 **현재 Vocabulary expression 전체163개 / DATA08 신규104개 / DATA09 추가0**을 구분했다. DATA09-5의 AI 전수54문법/216신규예문/216문제·648선택지, 고위험18문법 및 관련18예문배치·18문제, 무작위9문법/18예문/18문제 검수와25ID/31필드 교정 기록을 현재 본문·회귀와 대조했다. 표본을 중복 가산하거나 독립 사람 승인으로 표현하지 않는다.

6단계의 예문 Note 누락 수정, 단원·선행 preview 및 관련 사전·실제 검수 입력 진입 보완과7단계의 snapshot/오답/중복/rollback 회귀를 보존했다. 이번 runtime 수정0·Production 변경0이다.

### 14.2 전체 수량·선행163건·남은 공백

현재 Content24/Schema4/reader7/UserProgress10. Vocabulary2,287/Meaning2,420/Example4,813(문장4,800+발음13)/Grammar96/Question3,553(Grammar300)/Listening1,936/Course8/Lesson103, Source25테이블66,094행이다. Level별 전수 집계는 [최종표](Docs/DATA09_CLOSEOUT.md)와 [실제 집계](Docs/DATA09_CLOSEOUT.json)에 있다. 入門 V306/M327/E659/G22/Q156/L34, 初級800/847/1,577/20/134/79, 初中級1,181/1,246/2,577/54/3,204/1,823, 한글Question59이며 상위는 각각0이다.

선행163건의 index·원Example 한일 원문·지원Grammar ID를 현재 DB에 재대조했다. 기존120해결/7조건부/36미해결을 유지한다. 원부족147=120/4/23, Level8=0/0/8, 단순검토8=0/3/5다. 해결은 AI 설명 coverage 판단이며 숙달·사람 승인·새 재사용 승인이 아니다. 현재96문법/93선행edge 순환0, 후행참조12개는 선택적 설명 preview로 지원하며 기존 lesson/session 순서를 재작성하지 않는다.

선행 미해결36건(Level8포함), 장기Grammar 부족254~404개, 중급 이상/검증 녹음0, 추가 authored 입력·듣기와 통합 교육 순서·독립 검수 공백을 남긴다.

### 14.3 재구성·보존·대용량 검사

기존 Importer에 Source를 넣고 실제 previous23으로 `/tmp/data09-8-rebuilt.sqlite`를 새로 만들었다. **31테이블의 모든 열·중복 포함 행/파생 검색·sqlite_stat1/schema/index/trigger SQL/table_xinfo/FK/index metadata와 binary SHA가 일치**한다. integrity ok/FK0, strict0errors/기존10warnings,4.0429초다. 원본/Resources/과거 fixture95파일을 baseline Git byte와 대조해 보존했다. 이번 버전/ID/revision/배치 변경·Bundle 교체0이며 다음 실제 콘텐츠 변경은 현재24를 먼저 보존한다.

Source SHA `081ed35c7cd78345af1c1793fc450acaa2931f173cef00aaa960c8ef42318540`, Bundle/재구성 SHA는 모두 `56a7fa8b5358e254eeb324e706860d150d20c8ec013ba0b6f602cf14d93cceff`로 **불일치 없음**. Python3.12.14/SQLite3.53.1/Linux에서 재현했다. 다른 환경에서 SHA가 다르면 논리 행/schema와 별도로 원인을 보고해야 한다. [Importer 결과](Docs/DATA09_CLOSEOUT_BUILD.json), [전체 비교](Docs/DATA09_CLOSEOUT.json).

접근 가능한 전체 Git refs의 blob 중50MiB/100MiB 초과0, 최대18,841,600bytes다. canonical Source17,472,029bytes·Bundle18,841,600bytes와 DDL/Importer/ID·fixture를 계속 추적한다. 새 candidate/빌드 결과만 임시·기존 ignore를 쓴다. LFS 불필요, 기존 파일 삭제·범용 ignore·이력 재작성·force push0. 과거 대용량 오류 원문은 없어 당시 원인을 추측하지 않는다.

### 14.4 최종 실행·호환성·미검증 gate

- **PASS** 이번 `sh Tools/verify.sh --portable`: **365/365,405.161초,failures/errors/skipped0,exit0**. [전체 원시 로그](Docs/DATA09_CLOSEOUT_TEST_LOG.txt). 종료580점검은 unittest와 별개로 합산하지 않는다. [실제 결과](Docs/DATA09_CLOSEOUT_RESULTS.json).
- **PASS** 종료580/580, Source/DB/SHA·fixture 보존·전3,553문제/4,813예문 도달·96문법 한일 검색192건. DATA08 구조0errors/5warnings·DATA09 계약0/0, strict 기존10warnings 유지. 모든 Batch/교정/통합/시스템 회귀를 재실행했다.
- **PASS(임시 SQL·소스 범위)** UserProgress1~10 additive migration·Content19/23→24 디스크 교체, 기존 Progress/Favorites/Difficult/SRS due·다종 snapshot/선택·통계/Resume·socket 금지 Offline·15k규모·광고/구매 저장 독립성 회귀. 개인 진도·Swift Codable·실제 UserDefaults/Keychain·기기 Offline을 이 검사로 인증하지 않는다.
- **BLOCKED** xcodebuild/swift 없음. iOS Debug/Release/device Build·SDK/type-check·XCTest141정의/실행0, 기기3~10분·음성/중단/강제종료·접근성/메모리·StoreKit/AdMob/권한 미실행. **NOT TESTED** 독립 원어민·교사/외부 사전. **UNVERIFIABLE** 미확보 DEV01~14/DATA01~07 원래 완전 명세.
- 이번 FAIL0·새 runtime 수정0·실행 범위에서 미수정으로 재현된 P0/P1=0. DATA08 P1 세 건의 코드수정/SQL·corpus PASS/native BLOCKED와 DATA09 통합 native gate를 유지하며 iOS 전체의 P0/P1 부재를 보장하지 않는다. **Release B—Conditional 유지**.

### 14.5 Git·종료

PROJECT_STATUS/CONTENT_GUIDE/DATA_PROGRESS/RELEASE_CHECKLIST/AGENTS/DATA09_PROGRESS를 실제 상태와 검증 한계로 갱신했다. 수량·품질·재현 명령·버그·다음 공백·원본/대용량 정책은 [최종 보고](Docs/DATA09_CLOSEOUT.md)에 있다. 이번 명시 지시에 따라 정상 commit/push/PR과 검증 후 main merge·원격 동기화를 수행한다. 실제 최종 SHA·PR 상태는 Git/PR과 최종 응답이 기준이다. Force Push 금지. **DATA09-8에서 종료하고 DATA10은 자동 시작하지 않는다.**
