# DATA-09 진행 기록

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
