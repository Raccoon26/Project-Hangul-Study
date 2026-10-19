# PROJECT_STATUS — DATA-04

2026-10-03. DEV-09 프로젝트·문서·실제 production DB를 확인한 뒤, 기존 Grammar/Vocabulary/Conjugation/Listening/회독/SRS 구조에 콘텐츠를 추가했습니다. 중단 전 약 29분 작업했으며 재개 후에는 신규 콘텐츠 생성을 멈추고 검증·문서화·패키징만 진행했습니다. 이전 상태는 `Docs/DEV-09_STATUS.md`에 보존했습니다.

**Xcode build, Swift type-check, XCTest, 실기기 화면·음성 검증은 이 Linux 환경에서 실행하지 못했습니다. 아래 SQLite/구문 검증이 네이티브 실행을 대신하지 않습니다.**

## 실제 추가 결과

- 신규 grammar **30개: 入門 16 / 初級 14**. 누적 **42개: 入門 22 / 初級 20**.
- 신규 example **53개**. 기존 example **7개 재사용**으로 새 문법마다 예문 2개, 총 60개 grammar-example 연결을 추가했습니다.
- 신규 question **63개: 문법 60 + 듣기 3**. 각 새 문법에 단일선택 문제 2개와 정답 이유를 연결했습니다.
- 신규 lesson **8개**, 기존 두 문법 course에 level별 ordinal 2~5로 추가했습니다. 기존 레슨 ID·순서·구성은 그대로입니다.
- similar/contrast 관계 **16행(8쌍 양방향)** 추가. 누적 contrast 22행, similar 4행입니다.
- 기존 문법 본문 보강 **1개**: `-고 싶다`의 기존 note를 보존하면서 `-(으)려고 하다`와 희망/의도 차이를 덧붙였습니다.
- 기존 직접입력 질문 **5개**에 해당 신규 grammar prerequisite를 연결했습니다. 별도 활용·문제 엔진이나 중복 문장은 만들지 않았습니다.
- 신규 listening **3개**가 문법 example을 참조합니다. 재사용 예문의 기존 level을 보존하여 入門 1 / 初級 2입니다. 기존 듣기 learning_order 0~11을 보존하고 새 항목은 다음 구간 20 이상에 넣었습니다.

## 문법 curriculum

| 단계 | 새 레슨 | 항목 |
| --- | --- | --- |
| 入門 | 丁寧な文と存在 | -아요/어요, 있다/없다, 이/가 아니다, -ㅂ니다/습니다 |
| 入門 | 過去と否定 | -았/었어요, 안, -지 않다 |
| 入門 | 人とものをつなぐ | 와/과·하고, 도, 만, 에게/한테 |
| 入門 | 時間・手段・お願い | 부터, 까지, (으)로, -(으)세요, -아/어 주세요 |
| 初級 | 予定と進行 | -(으)려고 하다, -(으)ㄹ 거예요, -고 있다 |
| 初級 | 試す・経験・可能 | -아/어 보다, -(으)ㄴ 적이 있다/없다, -(으)ㄹ 수 있다/없다 |
| 初級 | 義務・許可・禁止 | -아/어야 하다, -아/어도 되다, -(으)면 안 되다, -지 마세요 |
| 初級 | 比べる・推測・前後 | 현재 추측 것 같다, 비교 보다, -기 전에, -(으)ㄴ 후에 |

기존 입문→초급 진행을 권장하고 hard lock은 추가하지 않았습니다. 초기 seed 레슨은 진행 중 사용자 보호를 위해 재정렬하지 않았습니다. prerequisite는 학습 연결 정보이며 자동 잠금이 아닙니다. 문법마다 의미·상세 설명·형태·조건·일본인 note를 작성했습니다. 조사와 일본어를 무조건 1:1 대응시키지 않고, ㄹ 유지/탈락, 요청과 존경, 가능과 허가, 의무와 금지, 동작 전후 등을 구분합니다.

## DB / Stable ID / 진도

**Content schema 4 / content 11 / reader 7 / UserProgress 8**. 새 테이블이나 schema 확장은 없습니다. 원본은 계속 `Content/production.json`, 앱 DB는 `Resources/content.sqlite`입니다. `data04-ids.json`은 편집·테스트용 ID 색인이지 앱의 별도 학습 데이터 source가 아닙니다.

새 ID는 한 번 발급한 UUID이며 row number나 배열 위치가 아닙니다. 기존 모든 ID와 어휘 정렬키를 보존했습니다. 관계/설명 변경에 필요한 기존 항목 **13개**(문법 1, 예문 7, 직접입력 질문 5)의 revision만 정확히 +1 했습니다. 예문 본문·번역과 기존 문제 본문·정답은 변경하지 않았습니다. `Content/data04-revised-ids.json`으로 승인 범위를 검사합니다.

기존 read-only Content Repository와 UserProgress SQLite 분리는 그대로입니다. 회독 membership/문제 snapshot, grammar_sessions, 공통 srs_state를 그대로 사용하며 사용자 DB를 초기화하거나 migration을 추가하지 않았습니다. 새 문법도 기존 레슨 조회→GrammarLearning→완료→grammar SRS 경로를 사용합니다.

## 발견·수정한 DEV-09 DB 헤더 결함

원본 DEV-09 DB는 content_metadata.schema_version=4인데 `PRAGMA user_version=3`이었습니다. 이것은 기존 v4 DDL의 오기이며, 앱 package 검증/듣기 조회와 다음 release의 previous 검증을 막을 수 있는 문제입니다.

- `Content/content-schema-v4.sql`의 헤더를 **4로 정정**했습니다. 구조 변경이나 임의 schema 증가는 아닙니다.
- Importer에 DDL 헤더와 source schema의 일치 검사를 추가했습니다. Validator를 약화하지 않았습니다.
- 원본은 `Tests/Fixtures/content-v10-production.sqlite`에 그대로 보존했습니다.
- `repair_dev09_header.py`는 정확한 원본 SHA256에만 동작하며, 입력을 덮어쓰지 않고 헤더만 정정한 `content-v10-repaired-production.sqlite`을 만듭니다. 전후 의미 fingerprint와 sqlite_master가 동일한지 테스트합니다.
- 최종 v11은 이 정정 스냅샷을 --previous로 사용해 **일반 stable ID/revision/version 검사를 모두 통과**했습니다. 실제 앱에는 올바른 헤더의 v11 DB만 번들됩니다.

## Validator / self review

Validator 오류 **0**, 경고 **10**은 기존 발음용 짧은 예시 5건과 어휘 동형 후보 5건입니다. 신규 grammar 중복 후보 0. 기존 저/차/일/쓰다/적다 후보는 기존 의미·품사 분리가 유지되어 삭제하지 않았습니다.

문법 표현의 공백만 다른 경우에도 중복 후보를 검출하도록 강화했고, grammar_task 질문은 정확히 하나의 active grammar question_target을 요구합니다. ID/FK, level, 필수 일본어, form, 예문/문제 연결, 관계 타입, 선택지와 정답, previous revision, schema 헤더를 검사했습니다.

별도 검수에서 요청 문제의 지정 형태를 명시해 답의 모호성을 줄였고, 빈칸 선택지를 완전한 어절로 수정했습니다. 일본어 설명의 받침 용어를 パッチム으로 통일하고 語幹을 처음에 설명했습니다. 동일 한국어 문장의 일본어 번역만 다른 중복 후보 1건은 기존 example로 합쳤습니다. 임시 문구·TODO·dummy 없이 실제 source에 반영했습니다. 전체 검수 목록은 `Docs/DATA04_REVIEW_CATALOG.md`, 검수 범위·출처는 `Docs/DATA04_REVIEW.md`입니다.

## 검증 결과와 범위

- 전체 Python/SQLite **159개 테스트 통과**(37.194초). `Docs/TEST_RESULTS_DATA04.txt`에 최종 실행 결과를 기록했습니다.
- 실제 Repository SQL로 신규 레슨 pagination, grammar/example/질문/비교 조회, 직접입력 5개 연결, 듣기 3개 source 조회를 검증했습니다.
- 기존 ID/payload/레슨 membership·어휘 정렬 보존, 디스크 재열기, 공통 SRS due 및 기존 schedule 재등록 시 보존을 SQLite로 확인했습니다.
- 모든 새 레슨의 실제 GrammarLearning→완료→SRS→재개 및 실제 ConjugationEngine/ProductionAnswer 연결 XCTest를 추가했습니다. **작성만 했으며 네이티브 실행은 미수행**입니다.
- Swift **62파일** tree-sitter 구문 검사 통과. Native XCTest **80개 작성·미실행**. Swift type-check가 아닙니다.
- 앱 Swift **54파일이 DEV-09와 byte-identical**입니다. UI/Navigation/Audio/학습 엔진을 수정하지 않았습니다.
- SQLite integrity_check=ok, foreign_key_check=0, schema/header=4. Import 보고서 `Docs/DATA04_CONTENT_REPORT.json`.

## 알려진 제한 / 다음 단계

1. Mac에서 `Tools/verify.sh`의 Debug/Release build와 XCTest를 실행해야 합니다. 실기기에서 새 레슨, 진행 중 종료/재개, SRS due, normal/slow 음성, Dynamic Type/VoiceOver를 확인해야 합니다.
2. 실제 TTS 출력과 외부 한국어 교육·일본어 전문가 감수는 미수행입니다. 자체 편집·검수를 전문가 인증으로 표시하지 마세요.
3. ConjugationEngine은 기존 9가지 형태를 지원합니다. 새 문법 30종 전체의 자동 활용을 새로 구현한 것이 아닙니다. 5개 대표 직접입력 연결만 추가했습니다.
4. Grammar 예문은 현재 ID 순으로 최대 6개 표시됩니다. source의 기초→확장 입력 순서가 UI에서 보장되지는 않아 각각 독립적으로 이해할 수 있는 문장으로 작성했습니다.
5. 현재 grammar blank는 단일선택입니다. 여러 자연스러운 정답이 생기는 문맥은 지시문을 제한했습니다. 직접입력은 기존 accepted/normalization 규칙 그대로입니다.
6. 다음 DATA는 정상 v11 DB를 previous로 보관하고 content 12 이상으로 올리세요. 원본 v10의 잘못된 헤더를 다시 배포하지 마세요. 기존 UUID·레슨 구성·사용자 기록은 재생성하지 않습니다.
7. 신규 기능 TODO/FIXME는 없습니다. 전체 문법 350~500개, 심화 활용, 실제 음원 등은 후속 범위입니다.

## 주요 변경 파일

- Content/production.json, Resources/content.sqlite: 실제 production 콘텐츠와 읽기 전용 번들 DB.
- Content/data04-ids.json, data04-revised-ids.json: 영구 ID 색인과 기존 revision 변경 목록.
- Content/content-schema-v4.sql, Tools/ContentBuilder/build_content.py: schema 헤더 정정·불일치 거부.
- Tools/ContentBuilder/validator.py, repair_dev09_header.py, test_data04_content.py: 검증 강화·제한적 과거 artifact 정정·10개 신규 회귀 테스트.
- Tests/GrammarLearningTests.swift, ProductionLearningTests.swift, ListeningTests.swift: 새 curriculum 네이티브 테스트와 실제 데이터 수 반영.
- 기존 Python content 테스트: 최신 count/revision 허용 목록 갱신. v8→v10/v9→v10 이력 테스트는 보존된 v10에 고정하고, v10→v11은 전체 payload 차이를 별도 엄격 검사합니다.
- PROJECT_STATUS.md, CONTENT_GUIDE.md, DATA_PROGRESS.md, README.md, Docs/DATA04_* 및 VALIDATION_DATA04.md: 인계·검수·실행 로그.

새 관계 쌍은 안↔-지 않다, 의도↔미래 예정(similar), 허가↔가능, 허가↔금지, 전↔후, -(으)세요↔-아/어 주세요, -(으)면 안 되다↔-지 마세요, -고 싶다↔-(으)려고 하다(contrast)입니다. 기존 seed 비교 관계는 그대로입니다.
