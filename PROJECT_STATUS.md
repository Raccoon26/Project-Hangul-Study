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

# PROJECT_STATUS — DATA-08-6 / Production 통합 (현재)

**DATA-08-6: Content19 / Schema4 / minReader7 / UserProgress10.** 911어휘/1,821신규예문 목표 유지. 실제 Course1·Unit tag3·Lesson47에911어휘 배치, 듣기/받아쓰기1,821·활용/문장입력1,162문항 연결. Production Vocabulary2,287 / Example4,597 / Grammar42 / Listening1,936 / Question3,337. strict0errors/기존10warnings·integrity ok/FK0·전63,159행 Source/DB 일치. portable **291 PASS**(289.839초, failures/errors/skipped0, exit0), 전용11 PASS. 사용자 기록/active snapshot/5·10·20 복습 SQL 보존. native 정의132/실행0, 실제 iPhone/offline/TTS/3~10분과 사람 검수 미실행. B—Conditional 유지. 상세 [통합 기록](Docs/DATA08_INTEGRATION.md), [DATA08_PROGRESS.md](DATA08_PROGRESS.md) §14. 아래는 단계별 이력이다.

---

# PROJECT_STATUS — DATA-08-5 / 최종 감사 (현재)

**A~C 최종 감사 수행, Release Readiness B—Conditional 유지. 사람 검수는 미실행.** 아래 단계 기록은 당시 이력이다.

- 전911어휘·963뜻·고유 예문1,821개·Note314개를 assistant가 한국어/일본어 별도 재독하고, 무작위 고유84개를 재감사했다.34어휘/43필드를 교정했다. 자동 Validator는 언어 품질을 보증하지 않는다.
- Production Content18 / schema4 / reader7 / UserProgress10. Vocabulary2,287 / Examples4,597(문장4,584) / Grammar42 / Listening115 / Question354. 수량 증감0, 기존 ID·관계·정렬·진도 보존,40엔티티 revision+1. 직전17 DB/source와 A/B/C 이력 보존.
- 전체 목표911어휘(일반807/표현104)/신규 문장1,821 달성 유지. strict 오류0/기존경고10, 전42,909행 Source/DB 일치·integrity ok/FK0. portable **280 PASS**(failures/errors/skipped0, exit0).
- 등록 문법만으로 선행 학습을 입증하기 어려운 문형 후보163예문, 독립 사람 언어 검수/Level 교정은 남아 있다. native 정의130개/실행0, Xcode·SDK·iPhone gate와 기존 retirement P1·初中級 Grammar0/Listening2/Question5·상위 Level 공백 유지.
- runtime/학습 엔진/사용자DB/광고·구매 코드 변경0. DATA-08-5 이후 단계 미실행. 상세 [DATA08_PROGRESS.md](DATA08_PROGRESS.md) §13, [최종 감사](Docs/DATA08_FINAL_REVIEW.md).

---

# PROJECT_STATUS — DATA-08-4 / Batch C (현재)

**DATA-08 콘텐츠 수량 목표 달성. Release Readiness B—Conditional 유지.** 아래 Batch A/B·DEV/DATA 기록은 당시 이력이다.

- Batch C: 初中級310어휘(일반280/표현30), 신규 문장619, 기존 예문1 재사용. 의미334·Note146·전항목 Collocation/Register·다의어24·어휘 관계84·기존 문법 참조17.
- A+B+C 누적 **911어휘(일반807/표현104) / 신규 문장1,821**. 목표800~1,200 / 1,300~2,000 충족, 부족0/0.
- Production Vocabulary2,287 / Examples4,597(문장4,584) / Grammar42 / Listening115 / Question354. Content17 / Schema4 / minReader7 / UserProgress10.
- 세 묶음 한일 재독·중복/UUID/Relation 검사, strict0errors/기존10warnings·integrity ok/FK0. 기존 본문/ID/정렬/진도 보존, 관계 끝점46개만 승인 revision+1. 직전 Content16 DB/source 보존.
- portable **269 PASS (failures/errors/skipped0, exit0)**. native 정의129개/실행0. Xcode·SDK·실기기 QA 미실행. 기존 retirement P1·初中級 Grammar0/Listening2/Question5·상위레벨 공백 유지.
- runtime/학습 엔진/UserProgress/광고·구매 코드 변경0. Batch C 이후 작업은 수행하지 않았다. 상세: [DATA08_PROGRESS.md](DATA08_PROGRESS.md) §12, [수량·해시](Docs/DATA08_C_COUNTS.json), [검수](Docs/DATA08_C_REVIEW.md).

---

# PROJECT_STATUS — DATA-08-3 / Batch B (현재)

**Release Readiness B — Conditional 유지.** 기존 DEV/DATA와 Batch A 결과는 아래 이력으로 보존한다.

- Batch B 승인: **初中級 어휘300 / 신규 문장600 / 의미311 / Note100**, 전300항목 Collocation. 동사148·형용사49·부사36·표현34·명사33. 세 묶음 각100/200에 한일 재독·중복/UUID·strict Validator 적용, 품질로 줄인 수량0.
- 현재 Production: **Vocabulary1,977 / Examples3,978(문장3,965+기존발음13) / Meanings2,086 / Grammar42 / Listening115 / Questions354**. 어휘 入門306 / 初級800 / 初中級871.
- **Content16 / Schema4 / minReader7 / UserProgress10**. 직전 Content15 원본 DB를 fixture로 보존. 기존 ID/상세본문/정렬/learning_order/membership 삭제·비활성화0. 어휘관계72·문법참조15 추가에 참여한 기존 끝점28개 revision만+1.
- strict Validator errors0 / 기존warnings10, integrity/FK 정상, source/Bundle 일치. 최종 portable: **255개 PASS (failures/errors/skip0, exit0)**. 기존243+B 신규12, A 정확한301/602 회귀군도 v15 fixture에서 보존했다.
- native 정의128개 / 실행0. Swift/Xcode·실기기 검증 미실행, runtime/UI/엔진/사용자DB/광고·구매 코드 변경0. 기존 retirement P1, native 출시 gate와 初中級 Grammar0/Listening2/Question5 공백 유지.
- DATA-08 전체800~1,200어휘/1,300~2,000문장 목표 유지. **A+B 누적601/1,202; 잔여199~599/98~798**. Batch B 이후 단계는 실행하지 않았다.

실제 수량·한일 검수·실패/수정·통합/미실행 gate: [DATA08_PROGRESS.md](DATA08_PROGRESS.md) §11, [검수](Docs/DATA08_B_REVIEW.md), [카탈로그](Docs/DATA08_B_REVIEW_CATALOG.md), [기계 집계](Docs/DATA08_B_COUNTS.json).

---

# PROJECT_STATUS — DATA-08-2 / Batch A (현재)

2026-10-19 (Asia/Tokyo). **Release Readiness: B — Conditional 유지, App Store 제출 승인 아님.** 아래 DATA-07 본문은 이력으로 보존한다.

- Batch A: **初中級 어휘301 / 신규 문장602 / 의미318 / 일본인 Note68** 반영. 명사20, 동사150·형용사51·부사40·표현40. 품질로 줄인 수량0.
- 현재 Production: Vocabulary1,677 / Examples3,378(문장3,365 + 발음예시13) / Meanings1,775 / Grammar42 / Listening115 / Questions354. 어휘 入門306 / 初級800 / 初中級571.
- **Content15 / Schema4 / minReader7 / UserProgress10**. Content14는 `Tests/Fixtures/content-v14-production.sqlite`에 원본 byte 그대로 보존.
- 기존 본문·ID·정렬·membership 삭제/변경0. 어휘관계45와 기존문법 예문연결14를 추가하며 승인된 기존끝점23개(어휘9/문법14)의 revision만+1. `Content/data08-a-revised-ids.json` 참조.
- strict Validator **errors0 / 기존warnings10**, integrity/FK 정상. 기존232 + 신규11 = **portable243 tests PASS**. Source/Bundle 일치 및4/20 부분session·SRS·favorite·설정 보존 확인.
- 현재 native 테스트 정의127개(이번1개 추가), **실행0**. Xcode/Swift compiler·iPhone QA 미실행. 앱 runtime/UI/광고/구매 코드 변경0.
- 기존 retirement resume P1과 native 출시 gate 유지. 初中級 전용 Grammar0 / Listening2 / Question5의 연계 부족도 유지. Batch A는 vocabulary 확장 단계이며 후속 Batch는 실행하지 않았다.
- DATA-08 전체 신규800~1,200어휘/1,300~2,000문장 목표 유지. 누적301/602, 잔여499~899/698~1,398. 전체 목표 완료로 표현하지 않는다.

상세: [DATA08_PROGRESS.md](DATA08_PROGRESS.md), [개별 검수](Docs/DATA08_A_REVIEW.md), [전체 카탈로그](Docs/DATA08_A_REVIEW_CATALOG.md), [실제 집계](Docs/DATA08_A_COUNTS.json). 첫 회귀검사19개 실패는 이전 총수/버전/revision 기대값이 원인이며 수정 후243개 모두 통과했다. Validator/제약/기존 cohort 검사는 유지했다.

---

# PROJECT_STATUS — DATA-07

2026-10-06. DEV-14 기준은 `Docs/DEV-14_STATUS.md`에 보존.

**Release Readiness: B — Conditional 유지. App Store 제출 승인 상태가 아니다.** 이번 콘텐츠 반영/portable 검증은 완료했지만 Linux에는 Swift compiler/Xcode가 없어 iOS build·XCTest·SDK 링크·실제 음성/접근성/Navigation은 미실행이다. 콘텐츠 확장은 전체 장기 curriculum 완성을 뜻하지 않는다.

## DATA-07 Summary

| 추가 항목 | 실제 DB 증가 |
| --- | ---: |
| Vocabulary | 450 (初級180 / 初中級270) |
| Meanings | 475 |
| Examples | 900 |
| 일본인 note | 36 |
| 명시적 어휘 관계 | 23 |
| 기존 문법과 새 예문 연결 | 28 (26문법) |
| 직접입력 활용 문제 | 8 |
| Listening / Questions | 4 / 12 (문제12에는 활용8 포함) |

200+250어휘 배치마다 재독/Validator 후 merge. 신규목표 가이드700–1,000개보다 줄여450개를 검수·통합 완료 범위로 확정했다. 추가 생성 없이 안정화를 우선했다. `Docs/DATA07_REVIEW.md`, `DATA07_REVIEW_CATALOG.md`에 검수/사례/전체 목록.

Production totals: vocabulary1,376 / examples2,776(문장2,763+발음예시13) / meanings1,457 / grammar42 / listening115 / questions354. 入門306 / 初級800 / 初中級270. `Docs/DATA07_COUNTS.json`은 실제 SQLite 집계.

## Architecture / Content Version

Content schema4 / **Content14** / minReader7 / UserProgress10. 기존 Content13을 `Tests/Fixtures/content-v13-production.sqlite`에 보존하고 `--previous` strict gate로 검증했다. Runtime source는 `Content/production.json`→기존 ContentBuilder→`Resources/content.sqlite` 하나다. 새 schema/별도 단어 시스템/사용자 migration 없음.

기존926어휘/의미/예문/문법/문제/코스/lesson 본문·ID·sort_key를 모두 유지. 관계가 추가된 기존30개 끝점만 revision+1. 목록 `Content/data07-revised-ids.json`. UUID를 row/order에서 만들지 않았으며 `data07-ids.json`에 발급값 보존.

새 sort_key `힣:data07:01:...`/`02:...`는 이번 편집 순서로 고정. 기존 항목 뒤에 append하고 기존 UserProgress의 set membership은 재배정하지 않는다. Curriculum의 실제 level query와20개 기본 세트 생성 경로로 접근하며 lower_intermediate를 새로 별도 구현하지 않았다.

## Requirements Coverage Audit

기존 DEV14 감사(`Docs/DEV14_REQUIREMENTS_AUDIT.md`)와 실제 source/repository/SQL/test를 대조했다. 문서의 완료 표현을 실기기 검증으로 바꾸지 않았다.

| 범위 | 확인 결과 |
| --- | --- |
| Content/UserProgress 분리, Stable ID, 버전, Importer/Validator | 기존 구조 유지, strict build·232 portable 회귀 |
| 한글/발음/Audio | 기존 본문과 ID 변경0, 기존 회귀 통과; 녹음/기기 음성 품질 미검증 |
| Vocabulary/회독/SRS | 실DB ID/card/meaning/example/query/저장 SQL 통과, native E2E 테스트 추가·미실행 |
| Grammar/Conjugation/Direct Input | 26문법 재노출, 실제문제8추가; native 활용 생성 검증 작성·미실행 |
| Listening/Dictation | 4유형 추가, source/answer/choice/retry 저장 기존 portable 회귀 통과 |
| Curriculum/Search/Detail/Favorites | 初中級 실제 조회/typed relation/기존 favorite 연결 통과 |
| Statistics/Maintenance/Settings | Content 추가로 사용자 DB 불변, 기존 통계/유지학습 SQL 회귀 통과 |
| Micro-session/Resume | bounded queries 및 부분 세션 디스크 재개 확인; iOS interruption 실험 미실행 |
| Ads/IAP/Notification | 코드/설정 변경0, 기존 정책 검사 통과; 실제 결제/권한/광고 gate 유지 |
| 전체 장기 교육과정/상위진단/모든 활용/자유작문 | 부분 구현·콘텐츠 부족, 완료로 표시하지 않음 |

## Integration Audit

- Content→Vocabulary: 신규450개를 실제 Swift repository에서 추출한 SQL로 조회. UUID/품사/meaning ordinal/예문2개/선택 note 확인.
- Curriculum→set: level 전체를200개 이하 페이지로 조회,20개 set 분할, 이전 prefix 순서 동일. 이미 시작된 세트는 저장된 ID 순서를 유지.
- 회독→SRS: 기존 회독 SQL tests 유지. 신규450개 enrollment를 반복해도450행, 기존 due를 덮어쓰지 않음. due5/30개 limit 및 due 이전0개 확인. 실제 Swift 회독→완료→SRS→복습→중복제출 보호 테스트는 작성했으나 미실행.
- Search/Dictionary: 한국어/일본어/보조 의미 조회,23관계와 새 문법예문 연결 확인. 전체 내용을 Swift 메모리로 불러와 필터하는 변경 없음.
- Conjugation: 붓다/가렵다/알아듣다/되묻다/타오르다/잠그다/헹구다/덮다의 metadata와 정답 콘텐츠 검사, 실제 엔진용 XCTest 추가. 엔진을 Python으로 복제해 통과했다고 하지 않음.
- Listening: 기존 Example4개 참조, sentence copy0, 4문제 모두 기존 query로 조회. dictation 정답은 원문 및 끝 마침표 생략만 허용. 소리 재생 자체는 미실행.
- Content update: 실제 User.sqlite에 old set(4/20), 여러 skill SRS, favorites, curriculum/settings를 저장하고 Content13→14 교체. User.sqlite bytes 동일, 재접속 후 ID/active session/순서 유지. 기존 suite는 grammar/listening/production snapshot과 migration도 검사.
- Statistics: total은 actual DB에서 집계하고 learned records를 재작성하지 않음. 기존 통계·maintenance SQL 회귀 통과.

## Micro-session / Commute UX Audit

Home/Continue 및 Curriculum 경로의 기존 UI를 변경하지 않았다. 새 vocabulary는 현재 level의 기존학습 경로로 진입한다. 학습 중 판정마다 transaction 저장, 부분 세션을 완료 처리하지 않는 구조 유지.3–10분 사용을 시간 보장으로 표시하지 않는다. TTS는 Vocabulary/Grammar에서 선택적이고 listening에서만 음성 필요.

SQL 검증은 네트워크 없는 로컬 파일 읽기/저장으로 수행. 실제 iPhone 비행기 모드·전화 interruption·앱 강제 종료·한 손/큰 글씨 사용은 미실행. 기존 하단 action/Dynamic Type/색상 외 feedback 구조 변경0. timer/polling/background task 추가0.

성능: Linux warm SQLite30회 중앙값, 이전→현재 한국어 검색0.2195→0.3140ms, 일본어0.2279→0.3256ms, 넓은検索0.8992→1.4095ms,20개set0.0805→0.0732ms,예문관계0.0092→0.0091ms. 기기 launch 측정이 아니며 앞으로 substring search/event 통계 규모의 실기기 실측은 필요. `Docs/DATA07_PERFORMANCE.json`에 plan/측정조건.

## Bugs Found

1. 신규 초안의 한동안/당장 품사, 챙겨 가다/오다 띄어쓰기·품사, 이루어지다 기본형 정리 필요.
2. 신규 assembler가 서술어 has_batchim을0으로 쓰고 하다형을none으로 쓴 가이드 불일치.
3. Korean listening distractor가 기존 Example을 참조해야 하는 계약 위반.
4. 기존 native 테스트가 production vocabulary 전체를 첫30개 page로 가정했고, DATA05 듣기 cohort를 이후 확장된 batch번호로 찾았음.
5. 기존 portable tests의 이전 총수 기대값, 새 테스트의 set ordinal0 입력 오류. 실제DB의 ordinal>0 제약이 정상 거부.

## Bugs Fixed

위1–3은 출시 전 데이터 수정 후 Validator 재통과. 위4는 native 테스트에서 전체 page 조회 및 기존 stable listening IDs를 사용하도록 수정. 위5는 현재 총수와 승인된 revision 목록을 반영하고 테스트 입력을1로 수정. Validator/제약은 완화하지 않았다. 이번 DATA 작업에서 재현된 별도의 production Swift runtime 버그는 없음. UI/엔진 코드는 불필요하게 변경하지 않았다.

## P0 Remaining

이번에 실행한 portable 범위에서 미수정 데이터 손실/충돌 P0를 재현하지 않았다. native build 미실행이므로 제품 전체P0 없음이라는 보장은 아니다. Release gate는 계속 남아 있다.

## P1 Remaining

- 활성 Vocabulary/Grammar review의 content retirement 시 자동 skip/reconcile 없음. 현재는 안전 오류. DATA07은 삭제/비활성화0으로 직접 충돌하지 않으므로 대규모 리팩터링하지 않음.
- iOS Debug/Release/SDK link/XCTest·실제 UI/VoiceOver/TTS/StoreKit/UMP 검증 미실행. `RELEASE_CHECKLIST.md`를 Mac에서 실행해야 함.
- 初中級 전용 grammar/대량듣기, 고급 전체 curriculum/placement, 모든 활용 예외/자유작문 미완성.

## Known Remaining Issues

외부 교육 전문가의 한국어/일본어 감수 및 실기기 TTS 음질검수는 미실행. 신규450개 전부에 독립 listening/direct-input 문제가 있는 것은 아님. 오래된 retry 통계의 원답변 역분류 불가, lifetime event scan, BundleID/Team/Icon/ASC/privacy owner 설정은 DEV14 gate 그대로. AdMob production ID 미설정은 오류가 아니며 Release 광고 비활성 유지.

## Build / Test Results

- Batch1/Batch2/최종 strict Validator: 오류0, 기존 경고10, 신규 중복 후보0.
- Production DB import: 성공, SQLite integrity 및 foreign keys 정상. Content14/schema4.
- `sh Tools/verify.sh --portable`: **232 tests / PASS**, monetization config 검사 PASS.
- `test_data07_content.py`: 신규11개 PASS. 기존221개도 이번 source와DB로 실행.
- Swift89파일 tree-sitter syntax parse: 오류0. Swift type-check/build가 아님.
- 신규 XCTest3개와 기존 native 테스트 pagination/cohort 수정. XCTest 실행0, Release build 미실행(Xcode/Swift compiler 없음).
- 보고서: `Docs/DATA07_{BATCH1_VALIDATION,BATCH2_VALIDATION,VALIDATION,DB_BUILD,COUNTS,PERFORMANCE,SWIFT_PARSE}.json`, TEST_LOG.txt, NEW_TEST_LOG.txt.

## Content Coverage Gaps

初級의 생활 동작·집안일·음식·상태 표현은 보강. 初中級의 관계/업무/여행/서비스/감정·태도는 진입층270개. 다음 DATA는 의료/공공서비스/주거·계약/학습활동·취미 등의 부족 분야를 기존DB와 비교해 추가한다. 初中級 예문의 새로운 문법(-다 보니/-느라/간접화법 등) 설명, 전용 listening과 활용 문제 확장이 필요하다. 전체 최종량1,376/15,000으로 장기 과정이 완성됐다고 표현하지 않는다.

## Next handoff

현재 Content14를 previous fixture로 보존한 뒤 다음 콘텐츠는15 이상 사용. Schema는 데이터만 추가할 때 올리지 않는다. 원본/ID/사용자 기록을 재생성하지 말고, oldset membership과 SRS/favorite 보존 검사를 계속한다. 먼저 Mac native gate를 실행하고 retirement resume 정책을 보완한다.
