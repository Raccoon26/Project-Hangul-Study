# DATA-10-5 / Listening·Dictation 전체 QA — Content28

**Content28 / Schema4 / reader7 / UserProgress10**, 기존 수량/ID 불변: DATA10 신규180원문/360문제, 전체 Listening2,296/Example4,993/Question3,913/Vocabulary2,287/Grammar96. A~C 전180한일 원문·360문항·630선택지·150accepted를 AI가 별도 재독했다. 독립 원어민·교사/실제TTS 검청 NOT TESTED, 검증 녹음0 유지.

재생 전 선택지를 disabled만 하던 구조를 재생 완료 후 조건부 생성으로 고치고, 내부 문장부호 안내·언어/문항10유형·신규150문항의 숫자 한글 입력 안내를 교정했다. 기존27 원본/DB fixture 보존·188본문필드/179ID revision+1(종속4포함), 신규/삭제ID0·UserProgress/학습순서/관계 불변. strict previous27 오류0/기존경고10·Source69,787행/전31테이블/schema/index/byte 재현 일치. 후보12/12 PASS, 최종 portable **403/403 PASS (477.897초, failures/errors/skipped0, exit0)**.

기존1,936개 받아쓰기95.558%·합산87.108%, 선행 검토12계열27원문·기존163후보36미해결 유지. UI/VoiceOver는 정적 회귀와 실제 실행을 구분한다. Cloud iOS Build/XCTest145정의·실행0 BLOCKED·이전Mac5FAIL/활용P1·독립 사람/기기 gate가 남아 **Release B—Conditional** 유지. [DATA10_PROGRESS §5](DATA10_PROGRESS.md), [QA보고](Docs/DATA10_QA_REVIEW.md), [학습경로 검토](Docs/DATA10_QA_LEARNING_PATH.md), [검사결과](Docs/DATA10_QA_TEST_RESULTS.json). 다음 단계는 시작하지 않는다. 아래 버전·현재·검사 표현은 각 단계 당시 이력이다.

---

# DATA-10-4 / 最終 Listening Batch C — Content27

**Content27 / Schema4 / reader7 / UserProgress10.** 학교·직장 안내/설명/비교/문제해결/의도 각10개, 신규 원문60·내용이해60/받아쓰기60=120문제를 반영했다. A/B/C 각60/120, DATA10 누적 **신규180원문/360문제**로 전체 목표150~250/300~500 충족. Content24 대비 실제 새ID 집합으로 검증했고 기존 예문/1,936듣기·추가참조·선택지 중복 계산0이다. 전체 Example4,993/Listening2,296/Question3,913, Vocabulary2,287/Meaning2,420/Grammar96 불변.

전60한일/120문제·180선택지·60accepted AI 별도 재독, 완전중복0/근접180쌍 재감사. 후보 인용문3건 등 교정을 기록했다. 기존16,541개 fingerprint/ID/revision/순서·103보호파일 보존, frozen26·strict previous26 오류0/기존경고10·Source69,787행/전31테이블·schema/index·재구성SHA 일치. 최종 portable **391/391 PASS (466.416초, failures/errors/skipped0, exit0)**. 모든신규·전체듣기는 단일화자TTS/검증녹음0, 실제TTS 검청·독립 사람/교사 NOT TESTED.

현재Cloud iOS Build/XCTest144정의·실행0 BLOCKED, 이전Mac의142실행137PASS/기존5FAIL과 실제 활용P1·구매cache gate를 유지한다. **Release B—Conditional**, 기기Offline/VoiceOver/음성중단/3~10분·메모리/실제권한은 미검증이다. [DATA10_PROGRESS §4](DATA10_PROGRESS.md), [검수·한계](Docs/DATA10_C_REVIEW.md), [실제수량](Docs/DATA10_C_COUNTS.json), [실행결과](Docs/DATA10_C_TEST_RESULTS.json). 이 마지막 Batch에서 종료하며 다음 단계는 자동 시작하지 않는다. 아래 버전·‘현재’·검사 표현은 각 단계 당시 이력이다.

---

# DATA-10-3 / 初中級 Listening Batch B — Content26

**Content26 / Schema4 / reader7 / UserProgress10.** 감정·의견·판단·이유·결과·경험·계획·의견차이의 신규 상황60개/문제120개(내용이해60·받아쓰기60)를 반영했다. DATA09 初中級54문법의 실제 자연스러운 용례를 편집상 재사용했고 기존Grammar ID/revision/관계는 바꾸지 않았다. 기존4,873예문 전체와 완전 중복0, 전단일화자TTS·녹음0·다화자 재생 가장0이다. 전체 Example4,933/Listening2,176/Question3,793, Vocabulary2,287/Grammar96 불변.

최종 portable **382/382 PASS**(578.139초,실패/오류/skip0), strict previous25 오류0/기존10경고·Source25테이블68,586행·전31테이블/스키마/행·재구성SHA 일치. 기존16,241개 payload/ID/revision/순서와99보호파일을 frozen25 및 실제파일로 보존했다. AI한일/문항 검수·15원고필드/공통Dictation안내 교정, 미완료/실패 로그도 보존한다. **현재Cloud iOS Build/XCTest143정의·실행0 BLOCKED, 이전Mac142실행의5FAIL은 미해결**, 독립 사람/실제TTS 검청 NOT TESTED·Release B—Conditional 유지.

[DATA10_PROGRESS §3](DATA10_PROGRESS.md), [검수·범위](Docs/DATA10_B_REVIEW.md), [실제 수량/보존](Docs/DATA10_B_COUNTS.json), [실행 결과](Docs/DATA10_B_TEST_RESULTS.json). DATA10 누적120원문/240문제·전체목표150~250/300~500 유지, 이번 Batch B에서 종료한다. 아래 ‘현재’·검사는 당시 이력이다.

---

# DATA-10-2 / 初中級 Listening Batch A — Content25

**Content25 / Schema4 / reader7 / UserProgress10.** 신규 상황60개·문제120개(내용60/받아쓰기30/의미18/한국어12), 6영역 각10원문/20문제. 전체 Example4,873/Listening2,056/Question3,673, Vocabulary2,287/Grammar96 불변. 기존 source 재사용0, 같은 신규 원문당2유형을 별도 구간에 배치했으며 전TTS·검증 녹음0이다. Content24 source/DB 불변 fixture와 기존95파일의 당시 byte·기존15,941개 엔티티 payload/ID/revision/순서/진도를 보존했다.

한국어·일본어·정답/오답·accepted 전수 AI 자체 재독과 NFC/공백 중복·Stable ID/참조·strict previous24 오류0/기존경고10·source25테이블67,385행·DB/byte 재현을 확인했다. 독립 사람·교사/실제 TTS 검청·iPhone/VoiceOver·출시 검증은 남는다. DATA10 전체 목표150~250원문/300~500문제 유지, 이번60/120에서 종료하며 다음 단계는 시작하지 않는다.

최종 `sh Tools/verify.sh`: **portable373/373 PASS**(실패/오류/skip0), Debug/Release Simulator·Release 기기 아키텍처 빌드 PASS. **native142실행·137PASS/기존5FAIL·skip0**, 정상 종료65/봉인 xcresult 보존. 새120문항·DATA08 P1 다섯 메서드는 PASS(전체142에 포함). 전체 native/출시 PASS는 아니다. [실제 결과](Docs/DATA10_A_TEST_RESULTS.json).

최신 [DATA10_PROGRESS §2](DATA10_PROGRESS.md), [검수/한계](Docs/DATA10_A_REVIEW.md), [실제 수량](Docs/DATA10_A_COUNTS.json), [writer 재현](Docs/DATA10_WRITER.md)을 따른다. **Release B—Conditional 유지.** 아래 버전·‘현재’·완료/검사 표현은 각 단계 당시 이력이다.

---

# DATA-10-1 / 듣기 분석·Mac 환경 인계

**Content24 / Schema4 / reader7 / UserProgress10 유지, Production 변경0.** PR #17 병합 main에서 듣기1,936개(전TTS) 전수 구조/중복/분포를 조사했다. 받아쓰기1,850개(95.56%), 初中級1,823개 중1,822개가 받아쓰기다. 신규150~250원문/300~500문제의 기준안200/400·4Batch를 설계했으며 이번 제작/통합0이다. AGENTS에 Mac/Windows Codex Cloud 교대 작업의 fetch·미커밋 보호·checkpoint push·PR/merge·main SHA 대조 규칙을 추가했다.

이번 공통 portable **363/365 PASS·2FAIL**(SQLite byte 재구성), native **141전부 종료·136메서드PASS/5FAIL**(명령은 진단 수집 대기 후143으로 중단)이다. Mac native에서 DATA08 P1 세 건의5회귀는 통과했으나 기존 cohort/course 가정 테스트와 실제 활용 생성 오류가 재현됐다. native 전체 PASS/출시 승인으로 표현하지 않는다. 실행수/중단·재시도/빌드·미완료 gate와 최종 Git 전달은 [DATA10_PROGRESS](DATA10_PROGRESS.md), [분석·계획](Docs/DATA10_LISTENING_ANALYSIS.md), [native 발견](Docs/DATA10_NATIVE_FINDINGS.md)을 따른다. **Release B—Conditional·실기기/독립 사람 gate 유지. 다음 Batch 자동 시작0.** 아래 ‘현재’·버전/검사는 각 단계 당시 이력이다.

---

# DATA-09-8 / 최종 종료 — 현재 Production

**Content24 / Schema4 / reader7 / UserProgress10 유지.** 신규 Grammar54·별도 고정Expression0·고유Example216·GrammarQuestion216(각Batch18/0/72/72), 기존Example4재사용 제외. 전체Vocabulary2,287/Meaning2,420/Example4,813/Grammar96/Question3,553/Listening1,936. Vocabulary expression 전체163개 중 DATA08 신규104개이며 DATA09 추가0이다. 장기Grammar/Expressions350~500 유지.

Source→임시SQLite 재구성: **31테이블 전체 행/스키마/참조·SHA 일치**, Source25테이블66,094행·기존원본/Bundle/fixture95파일 byte 보존, Validator0errors/기존10warnings. 이번 portable **365/365 PASS(405.161초,실패/오류/skip0)**·종료점검580 PASS·전3,553문제/4,813예문 도달. 선행163건120해결/7조건부/36미해결(Level8포함) 유지. **iOS Build/XCTest141정의·실행0/기기 BLOCKED, 독립 사람·사전 NOT TESTED, Release B—Conditional**, native P1 gate 유지. 이번 runtime 수정/데이터변경0·SHA불일치0. [최종보고](Docs/DATA09_CLOSEOUT.md), [실행결과](Docs/DATA09_CLOSEOUT_RESULTS.json), [누적§14](DATA09_PROGRESS.md). DATA10 미착수. 아래 ‘현재’·검사는 당시 이력이다.

---

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

> **DATA-09-1 분석·설계 (2026-10-20 JST):** 현재 Production은 Content19/Schema4/reader7/UserProgress10, Grammar42(入門22/初級20/初中級0)로 동일하다. 기존42개·후보163개를 조사하고 初中級54개 교육 단위를 설계했다. 신규 Production0, DATA08 B—Conditional·native/사람 검수 gate 유지. 현재 요청의 분석 범위만 진행했으며 아래 DATA08 결과는 당시 이력이다. [DATA09_PROGRESS](DATA09_PROGRESS.md), [설계](Docs/DATA09_DESIGN.md).

# DATA-08-8 최종 확인 — Content19 / Schema4 / reader7 / UserProgress10

**수량·Source/DB 통합 목표 달성, 전체 완료 판정은 B—Conditional 유지. DATA-09 미착수.** 신규 Vocabulary **911개(일반 어휘807 + 표현104)** / 고유 신규 문장 Example **1,821개**. 일반 어휘만 세어도 목표800~1,200 범위에 들며, 예문 목표1,300~2,000도 충족한다. 기존 예문1개 재사용은 신규 수에 포함하지 않았다.

Production: Vocabulary **2,287**, Meaning **2,420**, Example **4,597(문장4,584 + 발음13)**, Grammar **42**, Listening **1,936**, Question **3,337**, Course **5**, Lesson **85**. Content19와 모든 기존 ID·원본·DB byte 유지. Importer 재구성 DB는 번들과 SHA-256까지 동일, strict **0 errors / 기존10 warnings**, FK0 / integrity ok, 종료 점검133건 PASS. 이번 portable **301/301 PASS**(270.967초, 실패/오류/skip0, exit0). iOS build/XCTest137개는 **BLOCKED**, 독립 사람 언어 검수는 **NOT TESTED**다.

현재 결과와 미완료 조건은 [DATA08_CLOSEOUT](Docs/DATA08_CLOSEOUT.md), 실제 수량·해시는 [CLOSEOUT.json](Docs/DATA08_CLOSEOUT.json), 단계별 기록은 [DATA08_PROGRESS](DATA08_PROGRESS.md) §16을 따른다. **아래 DATA-08-1~7 및 DEV/DATA 섹션의 ‘현재’·완료 표현·테스트 수는 각 단계 당시 이력이며 최신 상태로 합산하거나 대체하지 않는다.**

---

**DATA-08-7 감사: Content19 / Schema4 / reader7 / UserProgress10 유지, Source/DB 변경0.** P1 세 건(비활성 복습 복구·받아쓰기 문장부호·듣기 due 퇴역 prefix) 코드 수정. 전체 Python/SQL **301 PASS**, native137개/실행0·iOS Build **BLOCKED**. 원래 DEV01~14/DATA01~07 작업 명세 원문은 찾지 못해 전체 원문 준수는 확인 불가. 기존 목표911어휘/1,821예문 유지, B—Conditional. [감사·부분 구현·상태표](Docs/DATA08_SYSTEM_REVIEW.md), [DATA08_PROGRESS.md](DATA08_PROGRESS.md) §15. 아래는 단계별 이력이다.

---

# DATA_PROGRESS — DATA-08-6 / Production 통합 (현재)

**DATA-08-6: Content19 / Schema4 / minReader7 / UserProgress10.** 911어휘/1,821신규예문 목표 유지. 실제 Course1·Unit tag3·Lesson47에911어휘 배치, 듣기/받아쓰기1,821·활용/문장입력1,162문항 연결. Production Vocabulary2,287 / Example4,597 / Grammar42 / Listening1,936 / Question3,337. strict0errors/기존10warnings·integrity ok/FK0·전63,159행 Source/DB 일치. portable **291 PASS**(289.839초, failures/errors/skipped0, exit0), 전용11 PASS. 사용자 기록/active snapshot/5·10·20 복습 SQL 보존. native 정의132/실행0, 실제 iPhone/offline/TTS/3~10분과 사람 검수 미실행. B—Conditional 유지. 상세 [통합 기록](Docs/DATA08_INTEGRATION.md), [DATA08_PROGRESS.md](DATA08_PROGRESS.md) §14. 아래는 단계별 이력이다.

---

# DATA_PROGRESS — DATA-08-5 / 최종 감사 (현재)

**Content18 / Schema4 / Reader7 / UserProgress10.** 이번 신규/삭제 행0,34어휘43필드 교정·40엔티티 revision+1. 이하 A/B/C와 DEV/DATA 기록은 당시 이력이다.

| 항목 | 현재 Production | 이번 증감 | Level/구분 |
| --- | ---: | ---: | --- |
| Vocabulary | 2,287 | 0 | 入門306 / 初級800 / 初中級1,181 |
| Meaning | 2,420 | 0 | A~C 검수963뜻 |
| 문장 Example | 4,584 | 0 | 入門646 / 初級1,577 / 初中級2,361 |
| 전체 Example | 4,597 | 0 | 기존 발음13 포함 |
| Learner Note | 531 | 0 | A~C 검수314개 |
| Grammar / Listening / Question | 42 / 115 / 354 | 0 | 初中級 전용0 / 2 / 5 |
| Vocabulary / Grammar 예문 참조 | 4,514 / 169 | 0 | ID와 관계 보존 |

DATA-08 누적911어휘(일반807/표현104)/신규예문1,821, 전체 목표 달성·부족0/0 유지. 全911어휘·963뜻·1,821고유예문·314 Note의 assistant 별도 한일 재독, 무작위84개 재감사 완료. 사람 검수0. 전Production42,909행 구조/DB 대조·strict 오류0/기존경고10, portable280 PASS. 선행Grammar 후보163예문 및 native130개 미실행은 남은 확인 사항이다. [DATA08_PROGRESS.md](DATA08_PROGRESS.md) §13, [수량·해시](Docs/DATA08_FINAL_COUNTS.json). 다음 단계 미실행.

---

# DATA_PROGRESS — DATA-08-4 / Batch C (현재)

실제 Production 집계. **Schema4 / Content17 / Reader7 / UserProgress10**. 아래 A/B와 DEV/DATA 내용은 당시 이력이다.

| 항목 | 현재 | C 증가 | level/구분 |
| --- | ---: | ---: | --- |
| Vocabulary | **2,287** | **310** | 入門306 / 初級800 / 初中級1,181 |
| 문장 Example | **4,584** | **619** | 入門646 / 初級1,577 / 初中級2,361 |
| 전체 Example | 4,597 | 619 | 기존 발음13 포함 |
| Meaning | 2,420 | 334 | C 다의어24항목 |
| Grammar | 42 | 0 | 入門22 / 初級20 / 初中級0 |
| Listening | 115 | 0 | 入門34 / 初級79 / 初中級2 |
| Question | 354 | 0 | 入門156 / 初級134 / 初中級5 / 한글59 |
| Note | 531 | 146 | C 전310항목 Collocation/Register |
| Grammar Example 참조 | 169 | 17 | 기존 문법 재사용 |
| Vocabulary Example 참조 | 4,514 | 620 | 신규619 / 재사용1 |

A+B+C 누적 **911어휘(일반807/표현104) / 신규 문장1,821**, 전체 목표800~1,200 / 1,300~2,000 달성, 부족0/0. C 일반280/표현30. 세 묶음 strict 오류0/기존경고10·integrity ok/FK0·신규중복0. portable269 PASS, native129개 미실행. 기존 데이터 삭제·비활성화0. 상세 [DATA08_PROGRESS.md](DATA08_PROGRESS.md) §12, [실제 수량·해시](Docs/DATA08_C_COUNTS.json). Batch C 이후 작업은 수행하지 않았다.

---

# DATA_PROGRESS — DATA-08-3 / Batch B (현재)

실제 `Resources/content.sqlite` 집계. **Schema4 / Content16 / Reader7 / UserProgress10**. 이하 Batch A/DATA-07 기록은 당시 이력이다.

| 항목 | 현재 | Batch B 증가 | level/구분 |
| --- | ---: | ---: | --- |
| Vocabulary | **1,977** | **300** | 入門306 / 初級800 / 初中級871 |
| 문장 Example | **3,965** | **600** | 入門646 / 初級1,577 / 初中級1,742 |
| 전체 Example | 3,978 | 600 | 문장3,965 + 기존발음13 |
| Meanings | 2,086 | 311 | 11항목 두 의미/용법 분리 |
| Grammar | 42 | 0 | 入門22 / 初級20 / 初中級0 |
| Listening | 115 | 0 | 入門34 / 初級79 / 初中級2 |
| Question | 354 | 0 | 入門156 / 初級134 / 初中級5 / 한글59 |
| Note | 385 | 100 | 전300어휘 Collocation |
| Grammar Example 참조 | 152 | 15 | 새 문장 ID 참조, 기존 예문 유지 |
| Vocabulary Example 참조 | 3,894 | 600 | 신규 문장과 관계 별도 집계 |

A+B 신규 누적 **601어휘/1,202문장**. 전체 목표800~1,200/1,300~2,000 유지, 잔여199~599/98~798. 세 묶음 각100/200의 Self Review·Duplicate Audit·Stable ID·Validator 완료. strict0errors/기존10warnings, 최종 portable **255개 PASS (failures/errors/skip0, exit0)**, native128개 미실행. 기존 데이터 삭제·비활성화0.

[DATA08_PROGRESS.md](DATA08_PROGRESS.md) §11과 [DATA08_B_COUNTS.json](Docs/DATA08_B_COUNTS.json)에 실제 SHA·증가량·검사·Git 상태를 기록한다. 다음 Batch는 수행하지 않았다.

---

# DATA_PROGRESS — DATA-08-2 / Batch A (현재)

2026-10-19 (Asia/Tokyo). `Resources/content.sqlite` 실제 집계, source=`Content/production.json`. **Schema4 / Content15 / Reader7 / UserProgress10**. 이하 DATA-07 기록은 과거 이력으로 보존한다.

| 항목 | 현재 | Batch A 증가 | 분포/구분 |
| --- | ---: | ---: | --- |
| Vocabulary | 1,677 | 301 | 入門306 / 初級800 / 初中級571 |
| 문장 Example | 3,365 | 602 | 入門646 / 初級1,577 / 初中級1,142 |
| 전체 Example | 3,378 | 602 | 문장3,365 + 기존발음13 |
| Meanings | 1,775 | 318 | 17개 다의어의 의미 구분 포함 |
| Grammar | 42 | 0 | 入門22 / 初級20 / 初中級0 |
| Listening | 115 | 0 | 入門34 / 初級79 / 初中級2; 모두TTS |
| Questions | 354 | 0 | hangul59 / 入門156 / 初級134 / 初中級5 |
| Learner notes | 285 | 68 | 이번68개 어휘에 Collocation/일본인용 설명 |
| Vocabulary-example 관계 | 3,294 | 602 | 고유예문 수와 별도 집계 |
| Grammar-example 관계 | 137 | 14 | 기존문법14개와 신규예문 연결 |
| Content items | 7,847 | 1,295 | 기존ID 삭제0 |

신규 품사: verb150 / adjective51 / adverb40 / expression40 / noun20. 신규는 전부lower_intermediate. 어휘관계45, 기존끝점23개 revision+1 외 기존 본문/정렬/사용자기록 변경0. Validator0errors/기존10warnings, portable243PASS. native127개 작성·미실행.

DATA-08 전체목표 신규어휘800~1,200 / 문장1,300~2,000 유지. 누적301/602, 잔여499~899/698~1,398. Batch A 목표270~400/450~650 충족, 수량축소0. 검수와 잔여문제는 `DATA08_PROGRESS.md`, 실제 SQL 집계는 `Docs/DATA08_A_COUNTS.json`에 기록한다.

---

# DATA_PROGRESS — DATA-07 / 2026-10-06

실제 `Resources/content.sqlite` 집계. Source=`Content/production.json`.
**Schema4 / Content14 / Reader7 / UserProgress10**. fixture 제외.

| 항목 | 현재 / 목표 | 분포 |
| --- | ---: | --- |
| Vocabulary | 1,376 / 15,000 | 入門306 / 初級800 / 初中級270 |
| Example sentences | 2,763 / 30,000 | 발음예시13 제외 |
| Examples 전체 | 2,776 | 문장2,763 + 발음13 |
| Meanings | 1,457 | 의미별 예문 관계 |
| Grammar | 42 / 350–500 | 入門22 / 初級20 / 初中級0 |
| Listening | 115 / 1,000+ | 入門34 / 初級79 / 初中級2 |
| Dictation | 29 | Listening에 포함 |
| 의미 선택 | 32 | Listening에 포함 |
| 한국어 선택 | 27 | Listening에 포함 |
| 내용 이해 | 27 | Listening에 포함 |
| Questions | 354 | 이번12 추가 |
| Pronunciation | 36 | 기존 유지 |
| 현대 한글 자모 | 40 / 40 | 조합설명 포함 hangul55행 |
| 문장/작문 문제 | 6 / 2,000 | 직접입력 blank3+sentence3, form59 별도 |
| TOPIK 유형 | 0 / 1,000 | 공식등급 추측 없음 |

learner_notes217, vocabulary_examples2692, grammar_examples123, content_items6552.

## DATA-07 실제 증가

Vocabulary450 / meanings475 / examples900 / notes36 / grammar0 / listening4 / questions12.
初級180 + 初中級270. 새 문법예문관계28(기존26문법), 어휘관계23. 기존 본문 수정0, 관계 끝점revision증가30. UserProgress schema 변경0.

| 신규 품사 | 수 |
| --- | ---: |
| 동사 | 176 |
| 명사 | 128 |
| 부사 | 56 |
| 형용사 | 51 |
| 표현 | 39 |

한 batch200/400, 다음250/500(어휘/예문). 검수 완료450개로 범위를 확정하여 가이드700–1,000개를 수량 목표로 강제하지 않았다. 최종SQL count와 diff는 `Docs/DATA07_COUNTS.json`, 검수목록은 `Docs/DATA07_REVIEW_CATALOG.md`.

## 누적 배치 이력

| 배치 | 신규 어휘 | 신규 문장 | 신규 의미 | 신규 note | Content |
| --- | ---: | ---: | ---: | ---: | ---: |
| DATA-01 | 226 | 447 | 244 | 65 | 5 |
| DATA-02 | 250 | 500 | 260 | 32 | 6 |
| DATA-03 | 250 | 500 | 268 | 48 | 7 |
| DATA-04 | 0 | 53 | 0 | 0 | 11 |
| DATA-05 | 200 | 339 | 210 | 33 | 12 |
| DATA-06 | 0 | 0 | 0 | 0 | 13 |
| DATA-07 | 450 | 900 | 475 | 36 | 14 |

DEV seed 문장/문법/발음은 DB 전체에 포함. 이전 상세기록은 `Docs/DATA06_PROGRESS.md` 보존.

## Coverage / next DATA

生活動作・家事・状態・調理、関係・気持ち、学校/仕事、旅行/サービス、抽象語・副詞を拡充。初中級はまだ導入層。医療/公共サービス/住居・契約/具体的な趣味、初中級文法・聴解・産出問題を今後補う。全部の語に独立した聴解問題があるわけではない。

Validator0errors/既存10warnings、新規duplicate候補0。Python/SQLite232tests PASS。Swift89ファイル構文parse0errors、XCTest/Release build/実機音声は未実行。次の更新は現在Content14をpreviousとして保存しContent15以上にする。
