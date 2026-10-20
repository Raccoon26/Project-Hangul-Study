# DATA-09 진행 기록

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
