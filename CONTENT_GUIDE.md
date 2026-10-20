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

**DATA-08-6: Content19 / Schema4 / minReader7 / UserProgress10.** 911어휘/1,821신규예문 목표 유지. 실제 Course1·Unit tag3·Lesson47에911어휘 배치, 듣기/받아쓰기1,821·활용/문장입력1,162문항 연결. Production Vocabulary2,287 / Example4,597 / Grammar42 / Listening1,936 / Question3,337. strict0errors/기존10warnings·integrity ok/FK0·전63,159행 Source/DB 일치. portable **291 PASS**(289.839초, failures/errors/skipped0, exit0), 전용11 PASS. 사용자 기록/active snapshot/5·10·20 복습 SQL 보존. native 정의132/실행0, 실제 iPhone/offline/TTS/3~10분과 사람 검수 미실행. B—Conditional 유지. 상세 [통합 기록](Docs/DATA08_INTEGRATION.md), [DATA08_PROGRESS.md](DATA08_PROGRESS.md) §14. 아래는 단계별 이력이다.

---

> **현재 기준 (DATA-08-5 최종 감사): Content18 / Schema4 / minReader7 / UserProgress10.** A~C 전체 assistant 한일 재독·표본84개 감사 후34어휘43필드 교정. 수량911어휘/1,821신규문장 유지. 현재 규칙은 마지막 DATA-08-FINAL 절과 `DATA08_PROGRESS.md` §13. 사람 검수·완전한 선행 Grammar 검증·native 실행은 미완료이며 아래 단계 내용은 당시 이력이다.

---

> **현재 기준 (DATA-08-4 / Batch C): Schema4 / Content17 / minReader7 / UserProgress10.** C 일반어휘280/표현30·신규문장619·재사용1, 의미334/Note146. DATA-08 누적911어휘(일반807/표현104)/신규문장1,821로 전체 목표 달성. 최신 계약은 마지막 DATA-08-C 절과 `DATA08_PROGRESS.md` §12. 아래 A/B·DEV/DATA 내용은 당시 이력이다.

---

> **현재 기준 (DATA-08-3 / Batch B): Schema4 / Content16 / minReader7 / UserProgress10.** 初中級300어휘/600문장·311의미·100 Note 추가, 전항목 Collocation. 최신 계약은 마지막 DATA-08-B 절과 `DATA08_PROGRESS.md` §11. 이하 Batch A/DEV/DATA 내용은 당시 이력이다.

> **현재 기준 (DATA-08-2 / Batch A, 2026-10-19): Schema4 / Content15 / minReader7 / UserProgress10.** 신규 初中級301어휘/602문장, 의미318/Note68. 아래 DEV/DATA 버전은 당시 이력이며 최신 추가 계약은 마지막 DATA-08-A 절과 `DATA08_PROGRESS.md`를 따릅니다.

> **현재 기준 (DATA-07, 2026-10-06): schema4 / Content14 / reader7 / UserProgress10.** 아래 DEV/DATA별 과거 버전·당시 수량은 이력이며 현재 수량은 DATA_PROGRESS.md를 따른다. 최신 추가 정책은 문서 마지막 DATA-07 절.

> DEV-14 (2026-10-05): 현재 상태는 PROJECT_STATUS.md 및 Docs/DEV14_REQUIREMENTS_AUDIT.md가 기준입니다. 아래 이전 단계 기록의 완료 표현은 native 출시 검증을 의미하지 않습니다. Content13/Schema4/UserProgress10 유지.

# CONTENT_GUIDE — DATA 작업의 입력 계약 (DEV-12)

현재 배포: **DEV-12 / DATA-06 / schema4 / content13 / reader7**. 최신 제작·재현 기준은 §24~27를 보세요. 아래 DEV별 버전 표기는 당시 이력입니다.

이 문서는 일본인용 한국어 학습 앱의 콘텐츠 제작·검수·추가·배포 규칙입니다. 현재 **콘텐츠 schema_version=4, content_version=13, reader_version=7**입니다. 사용자 진도 DB와 독립적입니다. Python 3.10 이상 표준 라이브러리만 사용합니다. 아래 명령은 프로젝트 루트에서 실행합니다.

## 1. 제작 흐름과 파일 형식

**Source JSON/JSONL → Validator → 임시 SQLite → 무결성 확인 → 원자적 출력 → App Bundle** 순서입니다. 앱은 이미 만들어진 SQLite를 read-only로 열며 JSON을 읽거나 전체 DB를 생성하지 않습니다.

현재 배포 원본은 **`Content/production.json`**입니다. `hangul-production.json`은 DEV-03 회귀 검증용 스냅샷입니다. 새 DATA 작업은 production.json 전체를 편집하거나 ID를 보존해 JSONL로 옮깁니다.

작은 수정·예시는 `Content/fixture.json`처럼 단일 UTF-8 JSON을 사용합니다.

```json
{
  "metadata": {
    "schema_version": 2,
    "content_version": 1,
    "min_reader_version": 2,
    "dataset_id": "ko-ja-core",
    "is_fixture": 0,
    "source_locale": "ja",
    "target_locale": "ko"
  },
  "tables": { "content_items": [], "vocabulary": [], "meanings": [] }
}
```

수천~수만 행의 DATA 작업은 **테이블별 JSONL + manifest.json**을 권장합니다. 한 줄에 행 객체 하나이며 빈 줄은 무시합니다. 한 테이블을 여러 shard 파일로 나눌 수 있습니다.

```json
{
  "source_format": "jsonl-v1",
  "metadata": {
    "schema_version": 2,
    "content_version": 3,
    "min_reader_version": 2,
    "dataset_id": "ko-ja-core",
    "is_fixture": 0,
    "source_locale": "ja",
    "target_locale": "ko"
  },
  "tables": {
    "content_items": ["items/data-01.jsonl", "items/data-02.jsonl"],
    "vocabulary": ["words/data-01.jsonl", "words/data-02.jsonl"],
    "meanings": ["meanings/data-01.jsonl", "meanings/data-02.jsonl"],
    "examples": ["examples/data-01.jsonl"],
    "vocabulary_examples": ["relations/word-examples.jsonl"]
  }
}
```

- 경로는 manifest 위치 기준 상대경로입니다. `..`, 절대경로, 바깥으로 나가는 symlink, 동일 shard 중복 등록은 거부합니다.
- 파일/행/테이블 순서는 ID나 의미를 결정하지 않습니다. 부모보다 자식이 먼저 나와도 최종 foreign key 검증을 통과하면 됩니다.
- 단일 JSON의 테이블 값은 행 객체 배열, JSONL manifest의 값은 파일명 배열입니다. 두 방식을 한 manifest 안에서 섞지 않습니다.
- 업데이트 입력은 **전체 스냅샷**입니다. DATA-02의 새 행만 이전 DB에 덧붙이는 patch 형식이 아닙니다. 기존 DATA shard들과 새 shard를 함께 manifest에 등록합니다.
- JSON key 중복, NaN/Infinity, 알 수 없는 테이블·필드는 거부합니다. 선택 필드는 생략하거나 `null`; 빈 문자열로 unknown을 표현하지 않습니다.
- 한국어/일본어는 UTF-8, NFC를 권장합니다. 비-NFC는 검토 경고이며 원문을 몰래 바꾸지 않습니다.

## 2. Stable ID와 개정 규칙

학습 엔티티는 **소문자 canonical UUID**를 사용합니다. 예: `44b3c8d7-8733-4f18-a3f9-9bcb81c209df`. 새 실제 콘텐츠에 UUID를 한 번 발급하고 원본에 저장합니다.

```sh
python3 -c 'import uuid; print(uuid.uuid4())'
```

- 표제어·번역·배열 순번·DB rowid·파일명·정렬 위치에서 ID를 재계산하지 않습니다.
- 단어, 각 의미, 각 예문, 문법, 발음 규칙, 활용, 듣기, 문제, 과정, 레슨, 태그, 자모, 혼동 설명은 각각 `content_items` 행과 종류별 상세 행이 필요합니다.
- `content_items.kind`와 상세 테이블은 아래 스키마 목록의 대응을 따릅니다. 한 ID에 다른 kind의 상세 행을 넣지 않습니다.
- 표현만 수정하면 ID를 유지하고 `revision`을 증가시킵니다. created_at은 유지하고 updated_at은 수정 시각으로 갱신합니다.
- 다른 개념이면 새 ID입니다. 배포했던 항목을 없애려면 **`is_active=0`으로 비활성화하고 상세 행도 보존**합니다. 폐기 ID를 재활용하지 않습니다.
- 관계 추가·삭제·변경도 **관계의 모든 콘텐츠 끝점 revision을 증가**시켜야 합니다. 예: grammar_examples 변경은 해당 grammar와 example, vocabulary_examples 변경은 meaning과 example의 revision 증가입니다.
- 의미 본문 수정은 그 meaning revision을 올립니다. 부모 vocabulary ID를 새로 만들 필요가 없습니다.
- 소스 파일의 행 순서만 바꾸는 경우 revision 증가는 필요 없습니다. 의미적으로 같은 행은 같은 개정입니다.
- `content_aliases`는 비활성 ID에서 동일 kind의 활성 ID로 연결합니다. 순환은 금지하며 사용자 이력을 자동으로 합치지 않습니다.
- 모든 배포 업데이트는 `--previous 이전배포.sqlite` 검증을 사용합니다. 이전 ID 삭제·kind 변경·created_at 변경·revision 하락·본문/관계 변경 후 revision 미증가를 거부합니다.
- synthetic 도구만 전용 namespace의 UUIDv5를 사용합니다. 고정 synthetic entity key에 따른 테스트 재현용이며 실제 콘텐츠 ID 발급 방식으로 사용하지 않습니다.

## 3. 학습 단계, 난이도, 품사

`content_items.level`은 다음 문자열 중 하나입니다. TOPIK 급수와 자동 대응시키지 않습니다.

| level | 표시 의미 |
| --- | --- |
| hangul | ハングル |
| intro | 入門 |
| beginner | 初級 |
| lower_intermediate | 初中級 |
| intermediate | 中級 |
| upper_intermediate | 中上級 |
| advanced | 上級 |
| master | マスター |
| maintenance | 維持学習 |

`difficulty`는 선택적인 **편집상 체감 난이도 1~5**입니다. 단계와 별개이며 모르면 null입니다. `learning_priority`도 선택적 편집 우선순위이며 작은 값부터 우선입니다. 공인 빈도 순위로 표현하지 않습니다.

| part_of_speech | 뜻 |
| --- | --- |
| noun / pronoun / numeral | 명사 / 대명사 / 수사 |
| verb / adjective | 동사 / 형용사 |
| determiner / adverb | 관형사 / 부사 |
| particle / interjection | 조사 / 감탄사 |
| auxiliary_verb / auxiliary_adjective | 보조동사 / 보조형용사 |
| bound_noun | 의존명사 |
| prefix / suffix / ending | 접두사 / 접미사 / 어미 |
| expression | 고정 표현 |

새 품사를 임의 문자열로 추가하지 않습니다. 필요하면 validator·SQL CHECK·Swift `PartOfSpeech`를 함께 개정합니다. 의미별로 품사가 다르면 `meanings.part_of_speech`에 별도 지정할 수 있습니다. 앱의 품사 표시는 일본어로 변환됩니다.

## 4. 어휘·의미 작성

`vocabulary`에는 표제어·품사·sort_key를 넣고 일본어 의미는 `meanings`로 분리합니다. 활성 어휘는 활성 의미를 최소 하나 가져야 합니다. 기본 표시 의미는 가장 낮은 ordinal의 활성 의미입니다.

- `reading`: 선택적 실제 발음 표기. 불확실하면 null. 일본어 가타카나를 한국어 발음의 완전한 대체로 취급하지 않습니다.
- `has_batchim`: 선택적 0/1. 받침 개념이 적용되지 않는 표현 등은 null을 허용합니다. 검증기는 언어학적 정답을 자동 판정하지 않습니다.
- `irregular_type`: null(미분류), `none`(규칙), `d`(ㄷ), `b`(ㅂ), `s`(ㅅ), `h`(ㅎ), `reu`(르), `reu_special`(러), `u`(우), `other`.
- `topik_level`: 선택적 1~6. 지정하면 `topik_source_id`로 **확인 가능한 출처**를 반드시 연결합니다. 공식 목록이라고 검증하지 않은 AI 추정을 넣지 않습니다.
- `frequency_rank`: 선택적 양수. 지정하면 `frequency_source_id` 필수입니다. 출처의 조사 대상·시기·빈도 기준을 citation에 남깁니다.
- `meanings.nuance_ja`, `usage_ja`: 일본인 학습자가 구분할 뉘앙스와 사용 상황. 모르면 null입니다.
- 동형어/다의어는 무조건 합치지 않습니다. 같은 lexical entry의 뜻이면 meaning을 추가하고, 별개 표제어 항목으로 유지해야 하면 새 vocabulary ID와 검수 근거를 남깁니다.
- 태그는 tags + item_tags, 관련어는 content_links로 연결합니다. 유의어·반의어·혼동어를 같은 관계로 섞지 않습니다.

## 5. 예문과 일본어 번역

`examples.korean`, `examples.japanese`는 필수이며 공백뿐인 문장은 오류입니다. 두 필드는 최대 2,000 Unicode 문자입니다. 1문자 문장은 오류로 삭제하지 않고 짧은 문장 검토 경고를 냅니다. 한 글자 한국어 단어(예: 물)는 정상이며 길이 때문에 거부하지 않습니다.

- 한국어 예문은 자연스럽고 목표 의미가 드러나야 합니다. 문법·띄어쓰기·높임말·상황 일관성을 사람이 확인합니다.
- 일본어는 직역의 형태보다 실제 일본인이 문맥에서 사용하는 자연스러운 문장으로 작성합니다. 원문 의미·시제·존대·의도를 임의로 추가/삭제하지 않습니다.
- 필요하면 `learning_point_ja`에 조사/뉘앙스/말높임 설명을 적습니다. 문장 내부에 주석을 섞지 않습니다.
- 어휘 연결은 `vocabulary_examples.meaning_id`로 정확한 의미를 지정합니다. 한 example을 여러 meanings와 연결할 수 있습니다.
- 문법 연결은 `grammar_examples`; 한 example에 여러 grammar를 연결할 수 있습니다.
- 발음 연결은 `pronunciation_examples`: rule_id, example_id, spelling_ko(표기), pronunciation_ko(실제 발음)를 넣습니다.
- 예문이 어휘·문법·발음·레슨·유효 content_links 어디에도 연결되지 않으면 orphan_example 오류입니다. 비활성 tombstone 예문은 이 조건에서 제외합니다.
- 검증기는 한국어/일본어의 자연스러움·사실·교육적 적합성을 증명하지 않습니다. 자동 통과 후에도 원어민/교육 검수가 필요합니다.

## 6. 문법·발음·활용·문제 관계

문법의 필수 pattern/title_ja/explanation_ja 외에 meaning_ja, form_ko, usage_constraints_ja, confusion_ja를 선택적으로 구분합니다. 유사 문법은 `similar_grammar`, 일본인 전용 별도 설명은 learner_notes + `learner_note`로 연결합니다.

발음 rule_type: `batchim`, `liaison`, `nasalization`, `liquidization`, `tensification`, `aspiration`, `palatalization`, `contraction`, `other`. 실제 적용 전/후는 pronunciation_examples에 넣습니다.

활용은 기본 어휘 vocabulary_id, form, form_type, politeness, explanation_ja를 필수로 지정합니다. 규칙/불규칙 구분은 irregular_type, 관련 발음 규칙은 rule_id(선택)입니다. 기본 어휘 품사는 verb/adjective/auxiliary_verb/auxiliary_adjective여야 합니다. 활용 생성은 이후 DEV-08에서 추가한 ConjugationEngine 절을 참고합니다. 모든 사전 예외를 지원하는 것은 아닙니다.

content_links의 허용 관계:

| relation | 끝점 규칙 |
| --- | --- |
| related_word / synonym / antonym / confusable | vocabulary → vocabulary |
| similar_grammar | grammar → grammar |
| learner_note | 콘텐츠 → note |
| pronunciation_example | pronunciation → example |
| question_target | question → 학습 대상 콘텐츠 |
| related / explains / prerequisite | 존재하는 콘텐츠 사이의 명시적 관계 |

자기 자신을 가리키는 관계는 금지합니다. 양방향 탐색 시 source와 target을 모두 조회할 수 있지만 행을 자동으로 반대 방향 복제하지 않습니다. prerequisite 관계 전체 DAG 검증은 현재 구현하지 않았으므로 교육 과정 검수 시 순환 여부를 별도로 확인해야 합니다. lesson_items에는 course/lesson/tag를 넣지 않습니다.

문제 answer_schema_version은 현재 1입니다. `answer_json`은 **JSON 객체를 직렬화한 문자열**입니다. 질문 유형을 추가하려면 SQL·validator·향후 채점 엔진을 함께 변경합니다.

| question_type | answer_json 객체 내용 |
| --- | --- |
| multiple_choice / listening_choice | `{"correct_choice_ids":["a"]}`; question_choices 2개 이상, 실제 존재하는 정답 ID |
| text_input / listening_input | `{"accepted":["물"]}`; 비어 있지 않은 허용 답 문자열 배열 |
| sentence_order | `{"tokens":["물을","마셔요"],"correct_order":[0,1]}`; index 전체를 한 번씩 포함 |
| writing | `{"model_answer":"물을 마셔요"}`; 향후 채점 기준은 선택적 rubric_json 객체 |

`direction`: null 또는 `ko_ja`, `ja_ko`, `ko_ko`. listening_* 유형은 listening_id 필수입니다. listening_items는 실제 media_assets를 참조하고 대본·일본어 설명을 가집니다. 객관식 choice_id는 문제 내부에서 영구적으로 유지하는 문자열입니다. TOPIK 급수(topik_level)는 선택이며 실제 출제/분류 근거를 콘텐츠 출처로 남겨야 합니다. 현재 UI는 단일 정답 multiple_choice를 채점합니다. DEV-04 TTS 듣기 문제는 아래 audio_questions 계약을 사용합니다. 기존 listening_* 녹음 시험 엔진은 아직 UI에 연결하지 않았습니다.

미디어 relative_path는 source 디렉터리 기준 상대경로입니다. 파일 존재와 SHA-256을 검증합니다. license에는 실제 이용 권리를 기록합니다. Importer는 음원 바이트를 복사하지 않습니다. DEV-04의 검증된 녹음 패키징 규칙은 아래 13절을 따릅니다.

## 7. 중복·오류·경고 처리

```sh
python3 Tools/ContentBuilder/build_content.py path/to/source --validate-only --report validation.json
```

오류가 있으면 종료 코드 1, DB는 게시되지 않습니다. 성공은 종료 코드 0입니다. 보고서는 error_count/warning_count와 code/location/message 목록을 포함합니다. 상세 목록은 각각 200개까지이며 총 개수는 모두 셉니다. JSONL은 `파일:줄번호`, 단일 JSON은 `파일:테이블[index]`로 표시합니다. FK 검사처럼 DB 전체 관계를 검사한 결과에는 table/rowid 또는 영구 ID가 표시됩니다. rowid는 오류 위치용일 뿐 사용자 진도 ID가 아닙니다.

- 중복 ID/키, 필수값 누락, 잘못된 타입/enum/관계, 존재하지 않는 참조, 빈 문장/번역, 초과 길이, 고아 예문, schema 불일치는 오류입니다.
- NFC/공백·대소문자 정규화 후 같은 표제어는 `duplicate_headword_candidate` **경고**입니다. 자동 삭제·병합하지 않습니다.
- DATA 검수자는 warning을 확인하고 의도된 동형어/다의어라면 검수 기록에 이유와 ID를 남깁니다. 단순 중복은 학습 개념을 검토한 뒤 병합 정책에 따라 처리합니다.
- 모든 입력 문자열에서 NUL은 거부합니다. 대부분 설명 필드 상한은 20,000자이며 표제어/발음/뜻/정렬키/한국어·일본어 문장은 2,000자입니다. 이 상한은 교육적 길이 권장이 아니라 손상/폭주 방지 한계입니다.
- validator를 끄거나 실패 행을 버리고 나머지 DB를 성공으로 게시하지 않습니다.

## 8. 생성·추가·배포 명령

```sh
# 최초 배포(기존 배포가 정말 없을 때만 --previous 생략)
python3 Tools/ContentBuilder/build_content.py path/to/source build/candidate.sqlite --production --report build/validation.json

# 이후 배포: 이전 배포 DB와 비교
python3 Tools/ContentBuilder/build_content.py path/to/source build/candidate.sqlite --production --previous releases/previous.sqlite --report build/validation.json
```

추가 작업 순서:

1. 최신 source 전체/이전 배포 DB/검수 기록을 확보합니다.
2. 기존 엔티티 수정이면 ID 유지, 새 엔티티면 UUID 발급. source shard에 영구 저장합니다.
3. content_items와 상세 행, 의미·예문·문법 관계를 함께 추가합니다.
4. 변경 엔티티/관계 끝점 revision과 updated_at을 갱신하고 전체 content_version을 증가시킵니다.
5. manifest에 새 shard를 등록하고 기존 shard 및 tombstone을 유지합니다.
6. validate-only와 --previous build를 실행하고 오류를 고칩니다. 경고는 검수합니다.
7. 자동 테스트 및 실제 번들 read-only 조회를 확인합니다.
8. 검수 완료 candidate만 `Resources/content.sqlite`로 복사합니다. Debug/Release 빌드는 이를 번들 `content.sqlite`에 넣습니다. 새 DB 파일을 사용 중인 앱 DB 위에 직접 덮어쓰는 런타임 갱신 방식은 아닙니다.
9. source/DB/보고서와 SHA-256을 같은 배포 버전으로 보관합니다.

DEV-01 source 업그레이드는 다음 도구를 사용합니다. 현재 프로젝트 fixture는 이미 수행했습니다.

```sh
python3 Tools/ContentBuilder/migrate_source_v1.py old-source.json new-source.json
```

이 도구는 기존 ID/created_at을 보존하며 revision/content_version을 증가시키고 DEV-01의 일본어 품사(名詞/表現)를 명시적 enum으로 바꿉니다. 그 외 legacy 품사는 추측하지 않고 거부합니다. v1 DB를 앱에서 제자리 수정하지 않고 v2를 다시 생성하여 교체합니다. v1 SQL과 테스트용 이전 DB를 보존했습니다.

## 9. 버전·사용자 기록 보호

- **schema_version**: 컬럼/제약/관계 구조가 바뀔 때. 현재 3.
- **content_version**: 같은 dataset의 전체 배포마다 증가. 단어 500개 추가도 이 값 증가입니다. 스키마 변경 없이 가능.
- **revision**: 개별 콘텐츠의 의미·본문·메타데이터·관계 변경.
- **min_reader_version**: 이 DB를 읽을 수 있는 앱 코드 계약. 현재 production은 reader 4. schema 2 회귀 패키지도 지원합니다.
- **dataset_id**: 지속적인 콘텐츠 묶음의 정체성. 기존 사용자가 같은 콘텐츠를 이어갈 때 바꾸지 않습니다.

사용자 DB는 콘텐츠 UUID만 참조하며 콘텐츠 DB로 foreign key/cascade delete가 없습니다. 콘텐츠 교체는 user.sqlite를 열거나 재작성하지 않습니다. UserProgress는 별도 schema 5입니다. v1→v2에서 acquisition_status/perceived_difficulty를 추가했고 v2→v3에서 학습 세션/답안 저장을 추가했습니다. DEV-04는 사용자 migration을 추가하지 않았고 DEV-05에서 v3→v4 회독 세션 저장을, DEV-06에서 v4→v5 SRS 복습 세션을 추가했습니다. 이전 학습량만 보고 습득 완료를 추정하지 않으므로 기본 상태는 `unassessed`입니다. 기존 v1은 SQLite backup API로 백업 후 트랜잭션 migration하며 실패하면 rollback합니다. 이 필드의 평가 UI/알고리즘은 아직 없습니다.

## 10. 개발용 성능 데이터

```sh
python3 Tools/ContentBuilder/generate_synthetic.py /tmp/hangul-synthetic --count 15000
python3 Tools/ContentBuilder/benchmark.py /tmp/hangul-benchmark --count 15000 --report benchmark.json
python3 -m unittest discover -s Tools/ContentBuilder -v
```

15,000 어휘/15,000 의미/30,000 예문/50 문법과 관계를 생성합니다. 모든 문장에 `__SYNTHETIC__`, dataset은 synthetic-dev-performance, is_fixture=1입니다. 앱 Debug/Release는 실제 한글 production DB를 사용합니다. 작은 fixture는 XCTest 번들에만 포함하고 성능 DB는 어떤 앱 번들에도 넣지 않습니다. --production은 fixture를 거부하고, flag를 바꿔도 production source의 synthetic marker를 거부합니다.

benchmark는 Swift 저장소에서 실제 SQL을 읽어 DB 생성, 단어 ID/페이지/단계/한국어·일본어 접두어/예문 관계 조회를 측정합니다. prefix는 NFC·trim·소문자 정규화 후 **문자열 시작 부분 일치**이며 임의 부분문자열·형태소·퍼지 검색이 아닙니다. 쿼리 변경 시 cursor를 초기화합니다. 페이지 최대 100개이며 시작 시 전부 로드하지 않습니다. Linux/Python 측정값을 iPhone 성능이라고 표현하지 않습니다.

## 11. 전체 필드 사전

아래는 현재 v2 SQL에서 추출한 필수/선택/참조 계약입니다. 필수는 생략/null 불가, 기본값은 생략 시 SQLite가 적용합니다. `content_items`의 공통 필드는 모든 학습 엔티티에 적용됩니다. Sources/media는 각각 자체 UUID가 있지만 학습 진도의 대상은 아닙니다. `content_metadata`는 manifest metadata로 입력하며 singleton=1은 importer가 만듭니다. `vocabulary_search`는 파생 테이블로 직접 입력 금지입니다.

### conjugations — content_items.kind=conjugation

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| id | TEXT | 필수 | 영구 canonical UUID → content_items.id |
| vocabulary_id | TEXT | 필수 | 기본/부모 어휘 UUID → vocabulary.id |
| form | TEXT | 필수 | 활용 결과 한국어 |
| form_type | TEXT | 필수 | 활용 종류를 나타내는 편집 키 |
| politeness | TEXT | 필수 | 말높임/격식 분류 키 |
| explanation_ja | TEXT | 필수 | 일본어 설명 |
| irregular_type | TEXT | 선택 | 위 규칙/불규칙 분류 |
| rule_id | TEXT | 선택 | 관련 발음 규칙 UUID → pronunciation_rules.id |

### content_aliases

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| old_id | TEXT | 필수 | 보존된 비활성 UUID → content_items.id |
| canonical_id | TEXT | 필수 | 동일 kind의 대표 UUID → content_items.id |

### content_items

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| id | TEXT | 필수 | 영구 canonical UUID |
| kind | TEXT | 필수 | 상세 콘텐츠 종류 |
| revision | INTEGER | 필수 | 개별 콘텐츠 개정 번호 1 이상 |
| is_active | INTEGER | 기본값 1 | 1 활성 / 0 보존된 tombstone |
| level | TEXT | 필수 | 9단계 학습 단계 enum |
| difficulty | INTEGER | 선택 | 선택적인 편집상 난이도 1~5 |
| created_at | TEXT | 필수 | 최초 생성 ISO-8601, 변경 금지 |
| updated_at | TEXT | 필수 | 개정 ISO-8601, 시간대 포함 |

### content_links

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| source_id | TEXT | 필수 | 출발 콘텐츠 또는 출처 UUID(참조 열 확인) → content_items.id |
| target_id | TEXT | 필수 | 도착 콘텐츠 UUID → content_items.id |
| relation | TEXT | 필수 | 위 관계 enum |

### content_metadata

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| singleton | INTEGER | 필수 | 항상 1, importer가 지정 |
| schema_version | INTEGER | 필수 | 콘텐츠 SQL 구조 버전 |
| content_version | INTEGER | 필수 | dataset 전체 배포 번호 |
| min_reader_version | INTEGER | 필수 | 최소 앱 reader 계약 버전 |
| dataset_id | TEXT | 필수 | 변경하지 않는 콘텐츠 묶음 식별자 |
| is_fixture | INTEGER | 필수 | 0 실제 콘텐츠 / 1 개발용 |
| source_locale | TEXT | 필수 | 학습자 언어 ja |
| target_locale | TEXT | 필수 | 목표 언어 ko |

### courses — content_items.kind=course

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| id | TEXT | 필수 | 영구 canonical UUID → content_items.id |
| title_ja | TEXT | 필수 | 일본어 제목 |
| description_ja | TEXT | 필수 | 과정의 일본어 설명 |
| ordinal | INTEGER | 필수 | 부모 안의 0 이상 순서 |

### examples — content_items.kind=example

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| id | TEXT | 필수 | 영구 canonical UUID → content_items.id |
| korean | TEXT | 필수 | 한국어 예문 |
| japanese | TEXT | 필수 | 자연스러운 일본어 번역 |
| learning_point_ja | TEXT | 선택 | 학습 포인트 설명 |
| audio_asset_id | TEXT | 선택 | 음원 asset UUID → media_assets.id |

### grammar — content_items.kind=grammar

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| id | TEXT | 필수 | 영구 canonical UUID → content_items.id |
| pattern | TEXT | 필수 | 한국어 문법/표현 패턴 |
| title_ja | TEXT | 필수 | 일본어 제목 |
| explanation_ja | TEXT | 필수 | 일본어 설명 |
| meaning_ja | TEXT | 선택 | 일본어 의미 |
| form_ko | TEXT | 선택 | 한국어 접속/형태 규칙 |
| usage_constraints_ja | TEXT | 선택 | 사용 조건/제약 |
| confusion_ja | TEXT | 선택 | 일본인이 혼동하는 포인트 |

### grammar_examples

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| grammar_id | TEXT | 필수 | 문법 UUID → grammar.id |
| example_id | TEXT | 필수 | 예문 UUID → examples.id |

### hangul — content_items.kind=hangul

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| id | TEXT | 필수 | 영구 canonical UUID → content_items.id |
| symbol | TEXT | 필수 | 자모/받침/음절 글자 |
| category | TEXT | 필수 | consonant/vowel/final/syllable |
| name_ko | TEXT | 필수 | 글자의 한국어 이름 |
| explanation_ja | TEXT | 필수 | 일본어 설명 |
| audio_asset_id | TEXT | 선택 | 음원 asset UUID → media_assets.id |

### item_sources

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| content_id | TEXT | 필수 | 학습 엔티티 UUID → content_items.id |
| source_id | TEXT | 필수 | 출발 콘텐츠 또는 출처 UUID(참조 열 확인) → sources.id |
| note | TEXT | 선택 | 출처 연결에 대한 검수 메모 |

### item_tags

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| content_id | TEXT | 필수 | 학습 엔티티 UUID → content_items.id |
| tag_id | TEXT | 필수 | 태그 UUID → tags.id |

### learner_notes — content_items.kind=note

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| id | TEXT | 필수 | 영구 canonical UUID → content_items.id |
| title_ja | TEXT | 필수 | 일본어 제목 |
| explanation_ja | TEXT | 필수 | 일본어 설명 |
| confusion_type | TEXT | 필수 | 혼동 포인트 분류 키 |

### lesson_items

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| lesson_id | TEXT | 필수 | 레슨 UUID → lessons.id |
| content_id | TEXT | 필수 | 학습 엔티티 UUID → content_items.id |
| ordinal | INTEGER | 필수 | 부모 안의 0 이상 순서 |

### lessons — content_items.kind=lesson

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| id | TEXT | 필수 | 영구 canonical UUID → content_items.id |
| course_id | TEXT | 필수 | 부모 과정 UUID → courses.id |
| title_ja | TEXT | 필수 | 일본어 제목 |
| ordinal | INTEGER | 필수 | 부모 안의 0 이상 순서 |

### listening_items — content_items.kind=listening

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| id | TEXT | 필수 | 영구 canonical UUID → content_items.id |
| audio_asset_id | TEXT | 필수 | 음원 asset UUID → media_assets.id |
| transcript_ko | TEXT | 필수 | 한국어 듣기 대본 |
| explanation_ja | TEXT | 필수 | 일본어 설명 |

### meanings — content_items.kind=meaning

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| id | TEXT | 필수 | 영구 canonical UUID → content_items.id |
| vocabulary_id | TEXT | 필수 | 기본/부모 어휘 UUID → vocabulary.id |
| meaning_ja | TEXT | 필수 | 일본어 의미 |
| part_of_speech | TEXT | 선택 | 위 품사 enum |
| nuance_ja | TEXT | 선택 | 의미의 뉘앙스 설명 |
| usage_ja | TEXT | 선택 | 의미별 사용 상황/제약 |
| ordinal | INTEGER | 필수 | 부모 안의 0 이상 순서 |

### media_assets

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| id | TEXT | 필수 | 영구 canonical UUID |
| relative_path | TEXT | 필수 | source 디렉터리 기준 미디어 상대경로 |
| sha256 | TEXT | 필수 | 실제 파일 SHA-256 hex |
| media_type | TEXT | 필수 | MIME 유형 |
| duration_ms | INTEGER | 선택 | 선택적 0 이상 길이(ms) |
| license | TEXT | 필수 | 실제 사용 권리/라이선스 |

### pronunciation_examples

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| rule_id | TEXT | 필수 | 관련 발음 규칙 UUID → pronunciation_rules.id |
| example_id | TEXT | 필수 | 예문 UUID → examples.id |
| spelling_ko | TEXT | 필수 | 발음 변화 전 표기 |
| pronunciation_ko | TEXT | 필수 | 규칙이 적용된 발음 |

### pronunciation_rules — content_items.kind=pronunciation

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| id | TEXT | 필수 | 영구 canonical UUID → content_items.id |
| title_ja | TEXT | 필수 | 일본어 제목 |
| rule_type | TEXT | 필수 | 발음 규칙 enum |
| explanation_ja | TEXT | 필수 | 일본어 설명 |

### question_choices

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| question_id | TEXT | 필수 | 문제 UUID → questions.id |
| choice_id | TEXT | 필수 | 해당 문제 안에서 유지할 선택지 ID |
| ordinal | INTEGER | 필수 | 부모 안의 0 이상 순서 |
| text | TEXT | 필수 | 선택지 문구 |

### questions — content_items.kind=question

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| id | TEXT | 필수 | 영구 canonical UUID → content_items.id |
| question_type | TEXT | 필수 | 위 지원 문제 유형 enum |
| direction | TEXT | 선택 | ko_ja/ja_ko/ko_ko |
| answer_schema_version | INTEGER | 기본값 1 | 현재 1 |
| prompt_ja | TEXT | 필수 | 일본어 문제 안내 |
| prompt_ko | TEXT | 선택 | 선택적 한국어 지문 |
| explanation_ja | TEXT | 필수 | 일본어 설명 |
| answer_json | TEXT | 필수 | 유형별 정답 객체의 JSON 문자열 |
| rubric_json | TEXT | 선택 | 선택적 채점 기준 객체의 JSON 문자열 |
| listening_id | TEXT | 선택 | 듣기 항목 UUID → listening_items.id |
| topik_level | INTEGER | 선택 | 선택적 TOPIK 1~6, 근거 필요 |

### sources

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| id | TEXT | 필수 | 영구 canonical UUID |
| title | TEXT | 필수 | 출처 제목 |
| citation | TEXT | 필수 | 찾아 확인할 수 있는 서지/근거 설명 |
| url | TEXT | 선택 | 선택적 출처 URL |
| accessed_at | TEXT | 선택 | 선택적 확인 날짜/시각 |

### tags — content_items.kind=tag

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| id | TEXT | 필수 | 영구 canonical UUID → content_items.id |
| label_ja | TEXT | 필수 | 태그 일본어 표시명 |
| namespace | TEXT | 필수 | 태그 분류 체계 이름 |

### vocabulary — content_items.kind=vocabulary

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| id | TEXT | 필수 | 영구 canonical UUID → content_items.id |
| headword | TEXT | 필수 | 한국어 표제어 |
| reading | TEXT | 선택 | 검수된 발음 표기 |
| part_of_speech | TEXT | 필수 | 위 품사 enum |
| sort_key | TEXT | 필수 | 명시적 목록 정렬키, BINARY 순서 |
| has_batchim | INTEGER | 선택 | 받침 0/1, 모르면 null |
| irregular_type | TEXT | 선택 | 위 규칙/불규칙 분류 |
| learning_priority | INTEGER | 선택 | 0 이상 편집 우선순위, 작은 값 우선 |
| topik_level | INTEGER | 선택 | 선택적 TOPIK 1~6, 근거 필요 |
| topik_source_id | TEXT | 선택 | TOPIK 분류 근거 source → sources.id |
| frequency_rank | INTEGER | 선택 | 선택적 양의 빈도 순위 |
| frequency_source_id | TEXT | 선택 | 빈도 순위 근거 source → sources.id |

### vocabulary_examples

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| meaning_id | TEXT | 필수 | 정확히 해당하는 어휘 의미 UUID → meanings.id |
| example_id | TEXT | 필수 | 예문 UUID → examples.id |

### vocabulary_search

| 필드 | 형식 | 필수/기본값 | 의미·참조 |
| --- | --- | --- | --- |
| term | TEXT | 필수 | 정규화된 파생 접두어 검색 문자열 |
| vocabulary_id | TEXT | 필수 | 기본/부모 어휘 UUID → vocabulary.id |

## 12. DEV-03 한글 입문 production 계약

### 원본과 버전

`Content/hangul-production.json`은 개발 fixture가 아닌 실제 학습 콘텐츠입니다. `Content/hangul-ids.json`은 최초 한 번 발급한 영구 UUID의 편집용 색인입니다. 이 색인을 Importer 입력으로 사용하거나, 텍스트/정렬 순서에서 ID를 재생성하지 않습니다.

이 절은 DEV-03 snapshot(dataset=`ko-ja-core`, schema=2, content=3, min_reader=3, is_fixture=0)의 계약입니다. 현재 배포는 14절의 schema 3/content 5입니다. 기존 schema의 hangul/learner_notes/questions/courses/lessons를 사용하므로 콘텐츠 migration은 필요하지 않습니다. reader v3는 한글 세션과 단일 정답 채점을 지원하는 앱을 뜻합니다. 사용자 DB v3와는 별도 버전입니다.

### 수록 범위

- 현대 자모 40개: 기본 자음 14, 쌍자음 5, 기본 모음 10, 복합 모음 11.
- 조합 3개(`가`, `나`, `한`), 받침 대표 끝소리 7개, 읽기 5개. `hangul` 전체 55행입니다.
- 설명 3개, 단일 정답 객관식 59개/선택지 225개, 12레슨/117단계.
- 연음·비음화·유음화·구개음화·된소리되기·겹받침 상세 규칙은 다루지 않습니다.

| 순서 | 레슨 | 학습 초점 |
| --- | --- | --- |
| 1 | はじめてのハングル | 음절 블록, 초성 ㅇ |
| 2 | 基本母音① | ㅏ ㅓ ㅗ ㅜ ㅣ |
| 3 | 基本母音② | ㅑ ㅕ ㅛ ㅠ ㅡ |
| 4 | 基本子音① | ㄱ ㄴ ㄷ ㄹ ㅁ ㅂ ㅅ |
| 5 | 基本子音② | ㅇ ㅈ ㅊ ㅋ ㅌ ㅍ ㅎ |
| 6 | 文字を組み立てる | 초성+중성(+종성), 가/나/한 |
| 7 | 濃音 | ㄲ ㄸ ㅃ ㅆ ㅉ |
| 8 | 複合母音① | ㅐ ㅔ ㅒ ㅖ |
| 9 | 複合母音② | ㅘ ㅙ ㅚ ㅝ ㅞ ㅟ ㅢ |
| 10 | パッチム入門 | 7가지 대표 끝소리, 모음 덧붙이지 않기 |
| 11 | 読んでみよう | 나/나무/바다/우유/하나 |
| 12 | 総合確認 | 모양·설명·조합·읽기 확인 |

기본 모음을 먼저 가르치는 이유는 발음하지 않는 초성 ㅇ을 배운 뒤 `아` 같은 짧은 음절을 즉시 읽고, 자음과 결합할 수 있기 때문입니다. 복합모음은 한 레슨이 길어지지 않도록 둘로 나눴습니다.

### 필드 매핑

| 학습 정보 | 저장 위치 / 규칙 |
| --- | --- |
| 영구 ID, revision, 활성 상태, level | `content_items`; kind=`hangul`, level=`hangul` |
| 문자 | `hangul.symbol`; 단일 자모 또는 해당 페이지의 음절/짧은 단어 |
| 분류 | `hangul.category`: consonant/vowel/final/syllable; 쌍자음은 consonant, 복합모음은 vowel. 레슨 제목이 세부 분류를 제공 |
| 한국어 이름 | `hangul.name_ko`: 기역, 쌍기역, 아 등. 음절 페이지에서는 해당 음절/단어 |
| 일본어 설명·발음 팁·혼동점·예시 | `hangul.explanation_ja`; 짧은 단락과 `例：아` 형식. 앱은 이 텍스트를 분해/추론하지 않고 그대로 표시 |
| 학습 순서 | `courses.ordinal`, `lessons.ordinal`, `lesson_items.ordinal`의 0부터 시작하는 정수. ID로 사용 금지 |
| 관련 자모 | `content_links`의 source_id/target_id/relation=`related` |
| 음원 | `audio_asset_id`는 현재 전부 null. 검증된 음원/권리/메타데이터가 준비됐을 때만 추가 |
| 설명 페이지 | `content_items.kind=note` + `learner_notes.title_ja/explanation_ja/confusion_type` |
| 퀴즈 페이지 | `content_items.kind=question` + `questions` + `question_choices` + `question_target` 관계 |

앱은 한 레슨의 단계만 조회하며 최대 200개까지 허용합니다. 학습 페이지는 hangul/note/pronunciation, 문제는 multiple_choice를 지원합니다. 다른 종류를 이 과정에 연결하면 앱이 명시적으로 거부합니다. SQL에서 순서가 바뀌어도 영구 ID는 유지되어야 합니다.

### 문제 작성

DEV-03에서 지원하는 네 표현은 모두 기존 `multiple_choice`입니다: 문자→발음 힌트/이름 선택, 일본어 설명→문자 선택, 자모 조합→음절 선택, 짧은 문자 읽기/분해 선택. 음성 문제로 표시하지 않습니다.

`answer_json`은 `{"correct_choice_ids":["answer"]}`처럼 **정확히 한 개**의 정답 choice_id를 가집니다. 선택지는 최소 2개, choice_id와 표시 텍스트는 문제 내에서 중복되지 않도록 작성합니다. 각 문제에 explanation_ja와 학습 대상 `question_target`을 연결합니다. 정답 choice_id는 위치가 아니라 식별자입니다. 앱은 attempt seed + question ID로 순서를 섞으며, 같은 세션을 재개할 때 같은 순서를 유지합니다. 새 학습의 순서는 우연히 이전과 같을 수 있습니다.

문제의 의미/정답을 수정할 때 기존 choice_id의 의미를 바꾸지 말고, 필요한 경우 새 문제 ID를 발급하세요. 일반 문구 수정은 기존 ID와 revision 증가 원칙을 따릅니다. 배포 content_version도 증가시킵니다.

### 일본어와 발음 검수

- 가타카나는 참고에 한정하고 한국어 발음과 동일하다고 단정하지 않습니다.
- ㅓ/ㅗ, ㅜ/ㅡ는 입술·입 모양을 설명합니다. ㅐ/ㅔ 등은 화자에 따른 발음 유사성과 철자 구별을 함께 설명합니다.
- 평음·격음·경음은 일본어 청음/탁음 또는 작은 ッ 하나로 치환하지 않습니다.
- 초성 ㅇ의 무음과 종성 ㅇ을 구분합니다. ㄹ의 위치별 기본 차이를 설명합니다.
- 개별 자모를 일반 한국어 TTS에 전달하지 않습니다. 음원 없음은 의도된 안전한 상태입니다.
- 한국어 예시가 실제 단어인지, 조합 연습용 음절인지 구별합니다. `갇`은 단독 음절 연습이며 단어 뜻을 만들어 붙이지 않습니다.
- 일본어 설명은 자체 작성했습니다. 언어 교육 전문가의 외부 감수나 실제 학습자 검증이 완료됐다고 표시하지 않습니다.

구조·발음 참고: [국립국어원 한글의 원리](https://m.korean.go.kr/hangeul/principle/001.html), [국립국어원 표준 발음법](https://m.korean.go.kr/front/page/pageView.do?mn_id=95&page_id=P000098). 참고 자료의 설명을 장문 복제한 콘텐츠가 아닙니다. 공식 기관이 이 앱을 인증했다는 의미도 아닙니다.

### 추가 및 검증

```sh
# source 계약/참조 무결성 확인
python3 Tools/ContentBuilder/build_content.py Content/hangul-production.json --production --validate-only
# DEV-03 패키지 재현: DEV-02의 빈 production 패키지와 비교
python3 Tools/ContentBuilder/build_content.py Content/hangul-production.json candidate.sqlite --production --previous Tests/Fixtures/content-v2-production.sqlite
# 한글 범위, 실제 runtime 조회 SQL, 문제/ID 검증
python3 -m unittest discover -s Tools/ContentBuilder -p test_hangul_content.py -v
```

위 명령은 DEV-03 회귀 재현용입니다. 새 DATA 작업에서는 `Content/production.json`을 편집하거나 JSONL로 ID를 보존해 옮긴 후, **현재 배포 DB**를 `--previous`로 지정합니다. `Content/production-empty.json`은 과거 호환 테스트용입니다. 이를 앱용 `Resources/content.sqlite`에 다시 빌드하지 마세요. 검수한 candidate만 앱 리소스로 교체합니다. 콘텐츠 버전/학습 단계 ID가 달라진 진행 중 세션은 기존 답안과 완료 기록을 남기고 명시적으로 새 시도를 시작하게 됩니다.


## 13. DEV-04 발음 production 및 공통 음성 계약

### 배포·추가 순서

DEV-04의 배포는 schema 3 / content 4 / min_reader 4 / dataset ko-ja-core / is_fixture 0의 전체 스냅샷이었습니다. 현재 원본은 DATA-01(content 5)을 포함하며 아래 공통 음성 계약을 그대로 유지합니다. DEV-03의 130개 항목을 그대로 포함하고 발음 과정 95개 항목을 추가했습니다. `pronunciation-ids.json`은 한번 발급한 UUID 색인입니다. ID를 재생성하지 마세요. 아래는 공통 생성 명령이며, 현재 DATA-01의 이전 배포 기준은 content-v4-production.sqlite입니다.

```sh
python3 Tools/ContentBuilder/build_content.py Content/production.json --production --validate-only
python3 Tools/ContentBuilder/build_content.py Content/production.json candidate.sqlite --production --previous Tests/Fixtures/content-v4-production.sqlite --report validation.json
python3 -m unittest discover -s Tools/ContentBuilder -v
```

다음 배포에서는 **현재 Resources/content.sqlite를 이전 배포로 보관**하고 --previous에 지정합니다. 새 source의 content_version을 올리고, 수정한 항목과 관계 끝점의 revision을 올린 뒤 candidate를 검수합니다. 통과한 DB만 Resources/content.sqlite로 교체합니다. content-v3-production.sqlite는 DEV-03 비교용이며 이후 배포의 최신 기준으로 계속 사용하지 않습니다.

### 추가 테이블과 필드

기존 모든 표/필드는 유지합니다. 정확한 전체 SQL은 `Content/content-schema-v3.sql`입니다.

| 테이블/필드 | 필수·선택 | 계약 |
| --- | --- | --- |
| pronunciation_presentations.rule_id | 필수 PK/FK | pronunciation_rules.id. content_items.kind=pronunciation |
| spelling_ko | 필수 | 정식 철자 또는 비교 대상. 화면의 가장 큰 표시. 발음대로 고쳐 쓰지 않음 |
| readings_json | 필수 | 서로 다른 비어 있지 않은 문자열의 JSON 배열을 직렬화한 문자열. 예: `["한궁말"]`. 대괄호 장식은 UI에서 붙임 |
| context_ja | 필수 | 적용 조건, 변이·예외, 교육용 표기의 한계. 장음 생략 등도 여기 명시 |
| show_composition | 기본 0 | 0/1. 단일 현대 음절이면 초성/중성/종성 분해 표시 |
| content_audio.content_id | 필수 PK/FK | 음성 정책이 연결된 콘텐츠 영구 UUID |
| mode | 필수 | `tts` 또는 `recorded_required` |
| usage | 필수 | `word_sentence`, `isolated`, `comparison` |
| tts_text | tts에서 필수 | 실제 철자의 한국어 단어/문장. presentation.spelling_ko와 같아야 함. 자모·발음 대괄호·조합식 금지 |
| asset_id | 선택 FK | media_assets.id. verified recording일 때만 지정; 아직 없으면 null |
| review_note | 필수 | 그 용도에 음성이 적합한 이유와 검수 근거. TTS의 교육적 정확성을 자동 보증하지 않음 |
| audio_questions.question_id | 필수 PK/FK | 기존 multiple_choice 문제. prompt_ko=null로 정답 철자 노출 방지 |
| audio_content_id | 필수 FK | word_sentence TTS가 허용된 content_audio.content_id |

`pronunciation_rules.title_ja/explanation_ja/rule_type`은 기존 필수 계약을 사용합니다. 비슷한 예는 `examples` + `pronunciation_examples`로 연결합니다. 하나의 규칙을 보여주는 단어도 실제 단어/뜻이어야 하며 예문의 짧은 길이 경고를 삭제해서 숨기지 않습니다. 현재 13개 연결 예 중 꽃/花, 밭/畑, 밥으로 발생한 5개 short_sentence 경고는 의도된 단어 예시로 검토했습니다.

`readings_json`은 여러 허용 발음에 대응합니다. 어떤 문맥에서 가능한지 context_ja로 설명하고, 퀴즈는 그 문맥을 명확히 제한합니다. 여러 발음이 모두 가능한데 하나만 무조건 오답 처리하는 문제를 만들지 마세요. 현재 단일 정답 엔진에서 이 조건을 만족하지 못하면 설명 페이지로만 제공합니다.

### 과정·퀴즈 연결

14레슨, 36개 설명 페이지, 31개 단일 정답 문제(듣기 3개), 총 67단계입니다. 7대표음/겹받침 → 연음 → 비음화 → 유음화 → 구개음화 → 된소리되기 → ㅎ → 자음/모음 비교 → 단어 듣기 → 종합 확인을 다룹니다. 상세 순서는 PROJECT_STATUS.md에 있습니다.

레슨·단계 순서는 기존 courses/lessons/lesson_items.ordinal을 사용하고 question_target으로 발음 학습 대상을 연결합니다. 정답은 선택지 위치가 아닌 choice_id입니다. 표기→발음, 규칙 이름, 받침 판별은 기존 객관식 구조입니다. TTS 듣기는 audio_questions 연결을 추가합니다. 정상 재생 완료 전에는 답안 제출을 허용하지 않으며, 한국어 음성이 없으면 안내 후 닫고 나중에 재개할 수 있습니다. 재생을 우회해 정답이나 완료를 기록하지 않습니다.

### 음성 정책·녹음 추가 방법

- TTS는 검토한 실제 단어/문장만, **원래 철자**로 전달합니다. `[머거요]` 대신 `먹어요`입니다. 개별 자모, 종성 소리 자체, 가/카/까 같은 최소대립 비교는 반드시 `recorded_required`입니다.
- 현재 21개 word_sentence TTS, 15개 recorded_required(개별 소리 9/비교 6)이며 검증된 녹음 파일은 아직 없습니다. 누락 시 일본어 안내를 표시하며 TTS로 대체하지 않습니다.
- 새 녹음은 원어민·교육 검수 및 이용 권리 확인 후 `Content/Audio/` 아래 m4a/wav/mp3/caf로 추가합니다. media_assets.relative_path=`Audio/파일명`, 실제 SHA-256, license 등 기존 필드를 기입합니다. 임의 경로/외부 URL은 재생하지 않습니다.
- 녹음 asset_id와 content_audio를 연결하고 관련 revision을 올립니다. source가 JSONL이면 상대 경로 기준은 manifest 위치이므로 Audio 폴더 위치도 이에 맞춥니다.
- `python3 Tools/generate_project.py`를 실행하면 존재하는 Content/Audio 폴더를 앱의 Audio 폴더 리소스로 등록합니다. Importer의 파일 존재/해시 검사와 런타임 경로/해시 검사를 모두 통과해야 합니다. 런타임 개별 음원은 최대 10 MB입니다.
- normal/slow는 `AudioPolicy` 한 곳에서 관리합니다(TTS 0.50/0.42, 녹음 1.0/0.85). 기기 음성별 실제 청취 검수 후 조정합니다. 시스템 TTS는 검증된 녹음과 구별하며 교육용 정밀 발음의 보증으로 표현하지 않습니다.
- 음원 제작 전에도 비교 페이지 설명은 학습할 수 있지만, 소리 비교 능력을 검증했다고 기록하지 않습니다.

### 발음 내용 검수

표기, 교육용 발음 표기, 실제 음성을 분리합니다. 일본어 모음이 자동으로 붙는 ク/ト/プ와 종성을 동일시하지 않습니다. ㄴ/ㅁ/ㅇ의 혀·입술 위치 차이, ㄹ의 혀끝 접촉을 설명합니다. 겹받침 읽다/없다/앉다와 활용 시 변화는 해당 문맥에 한정하고 전체 예외로 일반화하지 않습니다. ㅎ의 탈락/거센소리화, 평음·격음·경음, ㅓ/ㅗ 및 ㅜ/ㅡ 설명을 지나치게 단순화하지 않습니다.

출처: 국립국어원 [표준 발음법](https://www.korean.go.kr/kornorms/regltn/regltnView.do?regltn_code=0002), [읽다 발음 상담](https://www.korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=73&pageIndex=1&qna_seq=312133). 일본어 설명은 자체 작성했으며 외부 교육 전문가의 감수 완료를 의미하지 않습니다. Validator는 문법 구조·참조·정책을 검사할 뿐 발음과 일본어의 교육적 품질을 인증하지 않습니다.


## 14. DATA-01 입문 어휘 배치 계약

현재 전체 source는 **Content/production.json**, schema 3 / content 5 / reader 4입니다. 새 source 포맷이나 스키마를 만들지 않았습니다. 226 vocabulary, 244 meanings, 447개 새 문장 쌍, 452 vocabulary_examples 연결, 65 learner_notes를 추가했습니다. 기존 발음의 짧은 예시 13개를 합하면 examples 테이블은 460행입니다.

`Content/data01-ids.json`은 최초 발급한 ID와 의미/예문 연결을 사람이 확인하는 색인입니다. Importer는 production.json만 읽습니다. 색인에서 ID를 다시 생성하거나 순번/표제어로 UUID를 계산하지 마세요. `Docs/DATA01_REVIEW_CATALOG.md`는 읽기 검수용이며 별도 source가 아닙니다.

### 분류·기록 규칙

- level=intro는 앱 편집상 입문 단계입니다. TOPIK/공인 빈도 등급이 아닙니다.
- tags.namespace=data01_theme는 학습 주제, content_batch는 입문 배치 식별입니다. 배치 태그의 영구 ID는 data01-ids.json의 batch_tag_id입니다.
- 기본 의미는 meanings.ordinal=0, 다음 의미는 1입니다. 각 의미에 해당하는 예문을 연결합니다. 뜻만 늘리고 예문 없이 남겨두지 마세요.
- 동형어 차(お茶/車), 일(日/仕事), 쓰다(書く/使う)는 별도 vocabulary UUID입니다. 중복 경고를 자동 병합/삭제하지 않습니다.
- 동일한 한국어/일본어 문장 쌍은 기존 example을 참조할 수 있습니다. 학습 포인트/용도가 달라 무조건 합칠 수 있는지는 검토합니다. 이번에는 같은 쌍 5개를 공유했고 연결 끝점을 모두 명시했습니다.
- 일본인 주의점은 learner_notes와 learner_note 관계로 저장합니다. 의미별 usage_ja, 예문별 learning_point_ja도 기존 계약으로 사용합니다. DEV-05 회독 UI는 기본 의미/연결 예문/첫 note를 표시하며 추가 의미는 펼쳐 볼 수 있습니다.
- 사전형 동사/형용사의 irregular_type은 none/d/b/reu/h/other 등 기존 enum을 사용합니다. 하다형 여 불규칙은 other입니다. 으·ㄹ의 규칙적 탈락은 none이며, none을 ‘변화가 전혀 없음’으로 해석하지 않습니다.
- DATA-01 비서술어 has_batchim은 **표제어 마지막 음절의 철자상 받침**입니다. 서술어는 어간/사전형의 구분을 명확히 할 때까지 null입니다. 활용 엔진의 어간 받침 판정에 이 값을 그대로 쓰지 마세요.
- reading, topik_level, frequency_rank, learning_priority는 이번에 모두 null입니다. 빈 문자열이나 추정 순위를 채우지 않습니다.
- 한국어 예문에 배치 외 기초어/문법이 들어갈 수 있습니다. 이 배치는 어휘 목록이며 완성된 선수학습/레슨 순서를 뜻하지 않습니다.

### 검증·빌드 및 다음 배포

```sh
# DATA-01 재현: DEV-04 배포 DB를 기준으로 검증
python3 Tools/ContentBuilder/build_content.py Content/production.json --production --validate-only --previous Tests/Fixtures/content-v4-production.sqlite --report validation.json
python3 Tools/ContentBuilder/build_content.py Content/production.json candidate.sqlite --production --previous Tests/Fixtures/content-v4-production.sqlite --report build-report.json
python3 -m unittest discover -s Tools/ContentBuilder -v
```

검수한 candidate만 Resources/content.sqlite로 교체합니다. 현재 데이터의 자동 검증 결과는 오류 0/경고 8이고, DATA01_REVIEW.md에 경고 판정 근거가 있습니다.

**DATA-02는 현재 content 5의 Resources/content.sqlite를 이전 배포로 보관한 뒤 이를 --previous로 지정**합니다. 기존 전체 source에 새 자료를 추가하고 content_version을 6 이상으로 올립니다. 배포된 payload/관계 수정은 관련 revision을 올립니다. 스키마가 그대로면 schema 3을 유지합니다. 데이터 추가만을 위해 reader version이나 사용자 DB를 변경하지 않습니다.

통계는 DATA_PROGRESS.md에서 이어갑니다. 어휘는 영구 ID 수, 문장은 고유 문장 쌍 수로 세고, 개발 fixture/짧은 발음 예시/문제 수와 섞어 부풀리지 않습니다.


## 15. DEV-05 어휘 회독 세트와 콘텐츠 업데이트

이번 변경은 런타임 학습 기능이며 production source/DB/schema 3/content 5/reader 4는 바뀌지 않았습니다. UserProgress만 schema 4입니다. DATA source에 새 세트 JSON이나 Swift 단어 배열을 만들지 않습니다.

- `入門単語`는 ContentRepository에서 활성 vocabulary의 level=intro를 조회합니다. 개수는 COUNT이며 DATA-02 추가분도 자연스럽게 포함됩니다.
- 새 세트 생성 시 기존 sort_key/id keyset page에서 아직 사용자 세트에 배정하지 않은 단어 20개를 선택합니다. 마지막 잔여 세트는 더 작을 수 있습니다. local set UUID와 vocabulary UUID 멤버십은 UserProgress에 한 번 저장합니다. sort_key는 최초 선택 순서일 뿐 진도 ID가 아닙니다.
- 배정된 ID는 content version/정렬/level 변경으로 재배정하거나 삭제하지 않습니다. 이미 시작한 세트를 새로운 offset/페이지 결과로 재구성하면 안 됩니다. 앞쪽에 새 단어가 추가되어도 새 세트 생성은 bounded scan으로 찾습니다.
- `VocabularySession`은 시작 시 content version과 ID snapshot을 보존합니다. 콘텐츠 추가만으로 재시작을 강제하지 않습니다. 현재 단어는 ID로 조회하고 이벤트에는 당시 실제 content revision/version을 기록합니다.
- 표시할 의미는 meanings.ordinal 순서입니다. 첫 의미와 해당 meaning_id에 연결된 예문을 우선합니다. 현재 의미별 예문 1개를 example ID 순으로 고릅니다. 편집상 예문 우선순위가 필요하면 기존 관계에 명시적 ordinal 확장을 검토하고 source·validator·SQL·reader를 함께 변경하세요. 임시 Swift 예문을 넣지 마세요.
- 사용 설명/뉘앙스와 learner_note 관계를 그대로 사용합니다. 기본 화면은 사전 전체가 아니라 하나의 회상 목표이므로 나머지 의미는 펼쳐 보며 note는 첫 항목을 표시합니다.
- 실제 단어/문장은 기본적으로 공통 시스템 TTS를 사용할 수 있습니다. content_audio에 명시적 정책이 있으면 그 정책을 우선합니다. 개별 자모/비교/발음 표기를 단어 TTS로 우회하지 않습니다.
- 비활성/누락된 진행 중 vocabulary는 안전하게 멈추고 기록을 보존합니다. DATA 작업에서 ID 삭제/재활용을 하지 마세요. 자동 alias 대체/진도 병합은 아직 없습니다.
- known/learn은 해당 시도 안의 자기평가입니다. 완료를 영구 습득으로 바꾸거나 다음 DATA 배포에서 known 단어를 지우지 마세요. SRS는 별도 사용자 상태와 연결합니다.

현재 세트는 편집자가 설계한 콘텐츠 lesson이 아니라 **사용자별 고정 학습 묶음**입니다. 나중에 authored course/set을 추가할 때도 기존 사용자 묶음과 세션 ID를 유지하고 새 학습부터 적용하는 정책을 사용하세요. 새 어휘 추가를 위해 사용자 DB를 재생성할 필요는 없습니다.


## 16. DEV-06 SRS와 DATA 업데이트

Content schema 3 / content 5 / reader 4는 유지합니다. 사용자 DB만 schema 5이며 SRS는 기존 `srs_state(content_id,skill)`에 저장합니다. 콘텐츠 source에 사용자별 예정일/단계/완료 boolean을 넣지 마세요.

- 회독 완료 시 vocabulary의 **기존 영구 ID**를 skill=vocabulary로 등록합니다. 처음부터 known을 선택한 단어도 stage 0/다음 날부터 복습합니다. 기존 SRS 상태가 있으면 다시 학습해도 초기화하지 않습니다.
- 알고리즘은 calendar_steps v1: 1/3/7/14/30/60/120일. 단계/복습 카운터/자기평가는 콘텐츠 난이도나 TOPIK 등급과 별개입니다.
- DATA 추가/정렬/번역 수정 때문에 srs_state나 진행 중 review_items의 ID 목록을 다시 만들지 마세요. 같은 개념의 표현 수정은 기존 ID/revision 원칙을 따릅니다.
- 예정일은 UTC instant이며 판정 당시 timezone의 Gregorian 달력 날짜로 계산합니다. 시스템 locale이나 임의 날짜 문자열로 저장하지 않습니다. 기존 예정일은 timezone이 바뀌어도 보존합니다.
- 현재 SRS 화면은 기존 vocabularyCard에서 의미/예문/note/음성 정책을 읽습니다. 새 Swift 단어 배열이나 가짜 예문을 추가하지 마세요.
- 콘텐츠 비활성/누락은 기록을 삭제하지 않고 해당 review session을 멈춥니다. DATA는 기존 ID를 삭제/재활용하지 않아야 합니다. retired ID/alias의 자동 복습 대상 대체는 아직 구현하지 않았습니다.
- 미래 grammar/pronunciation/listening/sentence는 같은 content ID + skill 분리를 사용할 수 있습니다. 스케줄러는 vocabulary 본문/DB 정렬에 의존하지 않습니다. 각 콘텐츠의 조회/학습 UI는 별도로 구현해야 합니다.

DEV-06은 콘텐츠를 새로 배포하지 않았습니다. 다음 DATA 배포는 기존 안내대로 현 Content v5를 --previous로 보관하고 새 content version/revision을 증가시키세요. 알고리즘 정책 변경은 별도 algorithm_version 및 사용자 migration 과제입니다.


## 17. DATA-02 및 다음 배포

DATA-02 당시 배포는 **schema 3 / content 6 / reader 4 / UserProgress 5**였습니다. 앞 절의 v5 수치는 각 개발 단계의 이력입니다.

- DATA-02는 기존 production.json에 vocabulary 250(intro 70 / beginner 180), meanings 260, examples 500, learner_notes 32를 추가했습니다. 새 스키마/입력 포맷은 없습니다.
- 현재 누적은 vocabulary 476, meanings 504, 문장 쌍 947(발음 예시 13 포함 examples 960)입니다. 실제 집계는 DATA_PROGRESS.md와 production DB를 기준으로 합니다.
- `Content/data02-ids.json`은 영구 ID 확인용 색인입니다. Importer·앱은 production.json만을 source로 사용합니다. 새 UUID를 다시 발급하거나 이 색인에서 데이터를 별도 생성하지 마세요.
- 신규 저(관형사/あの)는 기존 저(대명사/私)와 구분합니다. 중복 후보 경고가 생겨도 자동 병합하지 않습니다.
- 데이터 배치는 content_batch 태그, 주제는 data02_theme 태그로 표시합니다. editorial level은 intro/beginner입니다. 공식 TOPIK/빈도와 혼동하지 않습니다.
- 기존 의미 ordinal, 의미별 예문, learner_note 관계, 서술어 irregular/has_batchim 정책을 그대로 사용합니다. 기존 ID나 관계를 수정할 때는 기존 revision 계약이 적용됩니다.
- 기존 세트 화면은 level 인자를 받으며 入門/初級 모두 같은 repository·회독·SRS를 사용합니다. 새 세트만 미배정 stable ID를 배정합니다. 기존 세트/진도/SRS는 DATA 배포 때 다시 만들지 않습니다.

DATA-02 재현:

```sh
python3 Tools/ContentBuilder/build_content.py Content/production.json candidate.sqlite --production --previous Tests/Fixtures/content-v5-production.sqlite --report build-report.json
python3 -m unittest discover -s Tools/ContentBuilder -v
```

**DATA-03에서는 현 v6 Resources/content.sqlite를 먼저 보관하고 그것을 --previous로 지정**합니다. 새 content version은 7 이상으로 증가시키며 단순 자료 추가라면 schema/reader/UserProgress를 바꾸지 않습니다. candidate 검수 후에만 bundle DB를 교체합니다.


## 18. DATA-03 — 일상 표현·편집 순서 및 다음 배포

**현재 schema 3 / content 7 / reader 4 / UserProgress 5**. 앞 절의 v5/v6 숫자와 재현 안내는 해당 단계의 이력입니다. 현재 원본은 production.json이며 새 포맷이나 별도 Swift 어휘 배열을 사용하지 않습니다.

- 신규 vocabulary 250(入門 10 / 初級 240), meanings 268, examples 500, notes 48. 상세 실제 누적 수는 DATA_PROGRESS.md를 따릅니다.
- UUIDv4를 발급해 한 번 고정했습니다. data03-ids.json은 검수 색인, DATA03_REVIEW_CATALOG.md는 읽기용 projection입니다. 이 파일로 앱에서 데이터 소스를 중복 생성하지 마세요.
- 각 단어에 예문 2개, 다의어 18개는 meaning.ordinal 0/1과 의미별 예문을 연결했습니다. 예문 관계는 기존 vocabulary_examples(meaning_id,example_id)입니다.
- 일본인 note는 기존 learner_notes와 learner_note 관계를 사용합니다. 신규 어휘 관계는 confusable/antonym/related_word/synonym 기존 enum만 사용하며 방향이 있는 source/target 행입니다. 자동사/타동사는 뜻이 같다는 이유로 synonym 처리하지 않습니다.
- 적다(verb/書く)는 기존 적다(adjective/少ない)와 별개입니다. 자동 중복 삭제를 하지 않습니다. 동형어 판단에는 품사·의미·용례가 필요합니다.
- 불규칙 정책은 기존과 같습니다. 하다 계열 other(여 불규칙), ㄹ·으의 규칙적 탈락 none, 서술어 has_batchim null. 모호한 품사/활용은 검증 가능한 사전·공식 자료로 확인하고 출처를 기록합니다.

### 편집 순서 — 새 항목에만 적용

DATA-03은 **기존 sort_key를 전혀 변경하지 않고** 새 항목을 현재 목록 뒤에 추가했습니다. learning_priority 100=동사/부사, 200=형용사, 300=명사/의존명사입니다. 이는 학습 구성 그룹이며 공식 빈도 순위나 TOPIK 등급이 아닙니다.

새 sort_key는 `힣:data03:100:0000` 형식입니다. `힣:data03:`는 이번 append 배치, 중간 수는 편집 그룹, 마지막 수는 **배포 전 선택한 순서**입니다. UUID나 사용자 진도 ID가 아닙니다. 이 키도 배포 후 배열 순번으로 다시 계산하지 마세요. 기존 레코드의 learning_priority는 null 그대로이며 새 키가 기존 모든 키 뒤에 놓이는 것을 실제 DB 테스트로 확인했습니다.

다음 배치에서는 기존 키를 다시 정렬하지 않고 새 배치 키만 배정합니다. 새 배치의 우선순위/정렬키는 source 작성 시 결정하고, 기존 목록의 상대 순서와 사용자의 membership 보존을 검사하세요. 향후 글로벌 선수학습 순서를 바꾸는 일은 별도 과정 설계로 진행합니다.

이미 시작한 세트는 UserProgress에 고정한 stable IDs를 유지합니다. 새 세트 생성만 기존 최대 20개 keyset scan에서 미배정 ID를 고릅니다. 콘텐츠 추가 시 과거 작은 세트에 단어를 덧붙이거나 SRS를 재등록하여 초기화하지 않습니다.

현재 DATA-03 검증/재생성:

```sh
python3 Tools/ContentBuilder/build_content.py Content/production.json --production --validate-only --previous Tests/Fixtures/content-v6-production.sqlite --report validation.json
python3 Tools/ContentBuilder/build_content.py Content/production.json candidate.sqlite --production --previous Tests/Fixtures/content-v6-production.sqlite --report build-report.json
python3 -m unittest discover -s Tools/ContentBuilder -v
```

검수된 candidate만 Resources/content.sqlite로 반영합니다. **DATA-04는 현재 v7 DB를 먼저 별도 보관하고 그것을 --previous로 사용하며 content 8 이상**으로 올립니다. 단순 자료 추가는 schema/reader/UserProgress version을 올릴 이유가 아닙니다. 배포된 본문·관계 변경 시에는 기존 revision 계약을 따릅니다.


## 19. DEV-07 문법 production 계약 (현재 Content 8 / reader 5)

앞선 DATA-03의 명령·버전은 당시 이력입니다. 현재 실행 예:

```sh
python3 Tools/ContentBuilder/build_content.py Content/production.json --production --validate-only --previous Tests/Fixtures/content-v7-production.sqlite --report validation.json
python3 Tools/ContentBuilder/build_content.py Content/production.json candidate.sqlite --production --previous Tests/Fixtures/content-v7-production.sqlite --report build-report.json
python3 -m unittest discover -s Tools/ContentBuilder -v
```

다음 DATA 배치는 현재 v8 DB를 먼저 보관하여 --previous로 지정하고 content_version을 9 이상으로 올립니다. 테이블 변경 없는 자료 추가는 schema 3 / min_reader_version 5를 유지합니다. UserProgress v6는 콘텐츠 제작 원본과 무관합니다.

### 기존 테이블에 작성하기

- content_items: UUIDv4 한 번 발급, kind=grammar, editorial level, revision. 학습 순서는 lessons.ordinal과 lesson_items.ordinal로 지정합니다. 기존 ID를 재발급하지 않습니다.
- grammar.pattern: 정식 한국어 표현. grammar.meaning_ja: 간결한 핵심 일본어 뜻. explanation_ja: 자연스러운 상세 설명.
- form_ko: `動詞の語幹 + 고 싶다`처럼 한국어 형태와 일본어 결합 안내를 읽기 쉬운 문자열로 작성합니다. 필드명이 _ko여도 이 앱의 형태 안내에는 일본어 보조 설명이 포함됩니다. 원시 기호만 쓰지 않습니다.
- usage_constraints_ja: 결합 조건/상황/뉘앙스/제약을 필요한 것만 간결히 작성합니다. confusion_ja: 일본인 혼동 포인트와 비교. 둘은 optional이며 빈 문자열 대신 null/생략합니다.
- examples는 기존 한국어/일본어 쌍을 재사용하고 grammar_examples로 연결합니다. 같은 example을 vocabulary_examples에도 연결할 수 있습니다. 학습용 문법마다 active 예문 1개 이상이 필요합니다. 현재 화면은 6개까지 ID 순으로 조회하므로 핵심 예문을 소수로 편집하세요.
- similar_grammar / contrast_grammar는 content_links의 grammar→grammar 관계입니다. 필요한 방향만 작성하며 양쪽에서 비교하려면 양방향 행을 만듭니다. 없는 ID/자기 자신/중복 관계는 거부됩니다. 서로 같은 뜻이라고 오해시키지 않는 차이를 confusion_ja 등에 설명하세요. 현재 비교는 6개까지 표시합니다.
- courses/lessons/lesson_items는 기존 형식을 사용합니다. 학습 레슨은 grammar 항목을 직접 연결합니다. 레슨당 1~20항목, 권장 3~5개입니다. **같은 learning level 전체에서 문법 lesson.ordinal은 유일해야 합니다.** 신규 코스에서도 0부터 다시 시작하지 않습니다. 이것은 순서이지 progress ID가 아닙니다.
- 이미 배포한 레슨은 가능한 한 구성·순서를 보존하고 신규 레슨을 뒤에 추가합니다. active UserProgress는 stable ID snapshot으로 재개합니다.

### 문법 문제

questions.question_type=`multiple_choice`, question_choices 2~6개, answer_json의 correct_choice_ids는 정확히 하나입니다. rubric_json에 `{"grammar_task":"meaning"}`를 넣습니다. 지원값은 meaning(뜻), context(문맥), blank(빈칸), form(결합형), contrast(유사 문법 구별)입니다. 모두 단일 선택 UI로 풀며 모든 문법에 5유형을 강제하지 않습니다.

문제의 content_links는 source=question UUID, target=grammar UUID, relation=question_target입니다. 레슨에 연결된 각 grammar는 active 문제 1~20개가 필요합니다. prompt_ja와 explanation_ja는 필수, prompt_ko는 필요할 때 넣습니다. 같은 문법 문제는 ID 순으로 학습하며 SRS는 reviewCount를 이용해 순환 선택합니다. 진행 중 질문은 UserProgress에 snapshot하므로 업데이트가 이미 선택한 문제를 바꾸지 않습니다.

오답 선택지도 문맥을 고려하여 정답이 하나임을 검수하세요. 단순히 다른 조사를 오답으로 넣으면 의도만 다를 뿐 문장이 성립할 수 있습니다. 예를 들어 은/는 대조 문제는 지시문에서 ‘対比’를 명시합니다. 정답/오답 모두 짧은 일본어 이유가 있어야 합니다. SRS는 오답 뒤 ‘覚えた’를 허용하지 않습니다.

### 출처·검수·음성

자체 편집 콘텐츠는 sources와 item_sources로 정확히 표시하고 공식 시험/전문가 감수로 가장하지 않습니다. 일본어 번역의 성별·주어·시간 추정, 불필요한 의미 추가, 기계적인 직역을 검토합니다. 예문만 기존 KoreanAudioService에 wordSentence TTS로 전달합니다. 문법 표기나 자모의 정확한 음원인 것처럼 TTS를 사용하지 않습니다.

Validator는 중복 grammar 표현을 삭제하지 않고 후보로 경고합니다. 학습 grammar의 의미/형태/설명/예문·문제, 문제 유형/선택지/정답, 관계, level, 레슨 크기·ordinal, reader 계약을 자동 검사합니다. 통과 후에도 교육적 정답 유일성과 한일 표현 자연스러움은 사람이 검수해야 합니다.

## 20. DEV-08 — 活用・直接入力 (現在 content 9 / reader 6 / user 7)

既存 questions の `text_input` を使います。新しい独立DBや語彙配列を作りません。現在の production source は production.json です。次回のデータ更新は v9 DB を previous として保存し content 10 以上にします。Content schema は 3 のままです。

- question_target: 実在する verb/adjective vocabulary IDを一つだけ指定。新しい活用形ごとに vocabulary を増やしません。
- answer_json: `{"accepted":["봐요","보아요"]}`。NFC/前後空白/連続空白のみ正規化。自然な別解は編集時に明記します。空文字・同一解の重複は禁止です。
- rubric_json: `{"production":1,"form":"present","mode":"form","spacing_warning":true,"overrides":{}}`。
- form enum: present / past / future / negativeShort / negativeLong / wish / connective / reason / condition。
- mode: form=活用入力、blank=既存例文の空欄、sentence=条件を指定した文の入力。sentenceは語句/順序/文体/句点条件を案内し、自由翻訳の正誤を判定しません。
- direction: ko_ko=lemmaや空欄から韓国語、ja_ko=日本語から韓国語。日本語の指示文があるだけでko_jaにしません。
- prompt_ja/explanation_jaに、使う形と短い理由を書きます。prompt_koは必要な空欄文など。答えを最初から問題文に露出させません。
- spacing_warning=falseなら厳密、trueなら空白だけの違いを独立feedbackにします。spacingを完全正解として記録しません。
- 一つのlemmaにつき出題用production質問は最大20個。必要な範囲を最大30lemmaずつqueryします。ユーザー進行中の質問はsnapshotです。
- blank/sentenceは既存exampleへrelated関係、関連する文法はprerequisiteでgrammarへ接続します。学習画面は同じGrammar説明コンポーネントを使用します。現時点では自動hard lockはありません。

### 活用metadataと例外

vocabulary.irregular_typeを必ず確認します。ㅂなら全語を機械的に不規則と扱うのではなく、既存 none/b/d/s/reu/h/other を尊重します。하다形のotherは対応しますが、その他のother/u/reu_specialは未対応です。으脱落とㄹ条件選択は通常の規則として扱います。

overridesは**その質問のlemma/targetに対する確認済み出力**をキー=上記form enum、値=韓国語として書きます。例：`{"present":"어때요","past":"어땠어요"}`。新しい表ではなく既存rubric JSON内の最小契約です。重複JSONキーは既存readerが拒否します。同じvocabulary UUID/formの複数質問に異なる例外値を書くとValidatorが拒否します。将来辞書の一括活用表示に使う場合は、lemma単位の例外カタログへ集約する必要があります。現段階で全語彙の例外DBが完成しているわけではありません。

ㅎの아/어形、하다複合語の안位置、푸다などはoverrideなしに推測生成しません。wishはverbのみ。form/blankのacceptedにはengineが生成する標準出力を含める必要があり、repositoryでも不一致を拒否します。縮約しない自然な形を併記できる場合はacceptedに追加します。例外で全単語を埋めてルールを迂回しないでください。

### 検証

```sh
python3 Tools/ContentBuilder/build_content.py Content/production.json candidate.sqlite --production --previous Tests/Fixtures/content-v8-production.sqlite --report report.json
python3 -m unittest discover -s Tools/ContentBuilder -v
```

実際のSwift活用実行はMacのProductionLearningTestsで検証します。PythonテストだけでSwift engineの言語的正確性を認証しないでください。新しいlemmaには規則/不規則の反例と各targetの期待形テストを追加します。

## 21. DEV-09 Listening production contract（現在 schema 4 / content 10 / reader 7）

次回は現在の v10 DBをpreviousとして保存し、content 11以上にします。UserProgress v8はこのsourceと独立です。

- `listening_items`: stable UUID / source_example_id（既存active example）/ audio_mode / audio_asset_id / explanation_ja / learning_order。参照型のtranscript_koはnull。本文・訳はexamplesから取得し、同じ文を新しいexamplesに複製しません。
- `audio_mode=tts`: 元のexample韓国語を既存AudioPolicyで発音。assetはnull。個別字母・発音用角括弧・比較表記をTTSに渡しません。`recorded_required`: 検証済みmedia_assetsを指定。検査済み音源がない教材を公開しません。再生時の欠損は安全な案内になり、TTSへ勝手に切り替えません。
- `content_items.level`はsource exampleとquestionにも一致させます。既存のeditorial level enumを使用し、公式TOPIK/頻度と呼びません。
- `learning_order`はレベル内で一意な非負整数。0–19が練習1、20–39が練習2です。既存の値を変更せず、新規は末尾へ追加します。レベル間では0から開始できます。IDではありません。進行中sessionはsnapshotの元の構成を維持します。
- listening→exampleの`content_links.related`を指定します。関係追加でexample revisionも増やします。語彙・文法はsource exampleの既存関係をたどれます。
- listening item一つにつきquestion一つ。`questions.listening_id`を指定。`prompt_ko=null`。答えの原文をprompt_jaにも書かないでください。
- rubric_jsonは `{"listening_task":"meaning"}`。meaning=日本語の意味、korean=聞いた韓国語、dictation=書き取り、comprehension=文内容の質問。
- 選択型はlistening_choiceと既存question_choices/answer_json.correct_choice_ids。正解は一つ、選択肢は2–6。重複、正解と同じdistractorは禁止。koreanの候補は既存examplesの実在文、正解はsource原文と一致。meaningの正解はsource日本語訳と一致させます。comprehensionは文から一意に答えられる質問/回答を人が検査します。
- 書き取りはlistening_input、acceptedに原文を含めます。現在は末尾の句読点の有無だけを追加できます。同義の別文は不可。NFC・空白の正規化は既存ProductionAnswerで実施し、スペル/助詞誤りを消しません。全候補を人が音声と比較してください。
- 日本語解説は正解理由を簡潔に示します。選択肢の長さだけで正解が分かる構成や無関係なdistractorを避けます。TTSは機種/voiceで違い得るため、公開前にnormal/slowを実機で試聴します。
- sourceのフィールド・ID/FK/level/重複/accepted/音声metadataをValidatorで検査します。言語的な正解一意性、原文の自然さ、実際の音声内容は自動認証しません。

```sh
python3 Tools/ContentBuilder/build_content.py Content/production.json candidate.sqlite --production --previous Tests/Fixtures/content-v9-production.sqlite --report report.json
python3 -m unittest discover -s Tools/ContentBuilder -v
```

上はDEV-09再現用です。次回はv10をpreviousとして使用してください。既存学習者のSRSやsessionを削除/再作成しません。廃止コンテンツはtombstoneを保ち、大量廃止前にdue queueのretired項目処理を検討してください。

## 22. DATA-04 — production grammar 확장과 현재 배포 기준

현재 기준은 **schema 4 / content 11 / reader 7 / UserProgress 8**입니다. 위 DEV별 ‘현재’ 표기는 당시 이력입니다. 다음 배포는 정상 v11 DB를 보관해 previous로 사용하고 content 12 이상으로 올립니다.

- 새 문법은 기존 grammar/grammar_examples/questions/lesson_items 형식 그대로 작성합니다. DATA-04는 문법마다 예문 2개와 단일선택 문제 2개를 사용했습니다.
- 기본형의 다를 뺀 ‘語幹’, ‘パッチム’ 등 일본어 설명 용어를 통일합니다. 일반 결합식만으로 불규칙까지 맞는 것처럼 설명하지 마세요. ㄹ 유지/탈락을 개별 문법에 맞춰 확인합니다.
- 한 개념의 형태 변이는 묶되, 진행/결과 상태나 수단/방향 등 범위가 넓은 경우 이번 학습 범위를 표기합니다. 희귀 의미를 모든 항목에 추가할 필요는 없습니다.
- 한국어 원문이 같은 예문은 일본어 번역·문맥을 검토하고 가능한 기존 ID를 재사용합니다. punctuation/공백 차이만으로 중복 문장을 만들지 않습니다. 원래 level은 보존합니다.
- 질문 지시문은 목표 의미·시제·register·형태를 명확히 합니다. 서로 다른 문맥에서는 자연스러운 형태를 무조건 ‘틀린 한국어’라고 설명하지 않습니다.
- grammar_task 질문에는 정확히 하나의 active grammar question_target이 필요합니다. 공백만 다른 grammar pattern도 duplicate 후보로 검출됩니다. 후보 자동삭제는 하지 않습니다.
- 현재 단일선택 grammar runner에 text_input 질문을 question_target으로 연결하지 마세요. 직접입력 question_target은 vocabulary, 관련 grammar는 prerequisite로 연결합니다. 기존 accepted/normalization/override 정책을 그대로 따릅니다.
- Listening은 canonical example을 source_example_id로 참조하고 question/item level을 source에 맞춥니다. beginner grammar가 intro example을 재사용했다면 그 듣기 item은 intro가 될 수 있습니다. grammar level을 억지로 source에 덮어쓰지 마세요.
- 새 레슨은 기존 레슨 구성·ordinal을 유지하고 해당 level 뒤에 추가합니다. DATA-04는 각 level에 ordinal 2~5를 추가했습니다. 신규 듣기는 이미 배포한 첫 20칸 구간을 유지하고 다음 구간에 추가했습니다.
- 관계를 추가한 기존 endpoint도 semantic fingerprint가 바뀌면 revision을 올립니다. DATA-04에서는 기존 문법 1, 예문 7, 직접입력 질문 5개를 +1 했습니다.

### DEV-09 헤더 결함과 재현

원본 v10의 metadata는 schema4지만 SQLite header는3이었습니다. 원본 fixture는 보존하고, hash-locked `repair_dev09_header.py`로 별도 수정본을 만들었습니다. 현재 v4 DDL은 header4이며 Importer가 source schema와 일치하지 않으면 거부합니다. 이 수정은 schema 확장이나 validation 우회가 아닙니다.

```sh
# 정정 스냅샷은 이미 포함되어 있습니다. 새 경로로 재현할 때만 실행합니다.
python3 Tools/ContentBuilder/repair_dev09_header.py Tests/Fixtures/content-v10-production.sqlite /tmp/v10-repaired.sqlite
python3 Tools/ContentBuilder/build_content.py Content/production.json candidate.sqlite --production --previous Tests/Fixtures/content-v10-repaired-production.sqlite --report report.json
python3 -m unittest discover -s Tools/ContentBuilder -v
```

위는 DATA-04 재현용입니다. 다음 배포의 previous는 content11입니다. 데이터 제작 단계에서 UserProgress 파일을 수정하거나 초기화하지 않습니다.


## 23. DATA-05 vocabulary/expression 제작·통합 계약

현재 배포는 content12, schema4, reader7, UserProgress8이다. 다음 DATA 작업은 현재 번들 DB를 previous로 보존하고 content13 이상으로 증가시킨다. `Content/data05-ids.json`은 검수/테스트용 ID 목록이며 앱 콘텐츠 원본은 `production.json` 하나다.

- `expression`은 마음에 들다/발이 넓다 같은 학습 가치가 있는 묶음에 사용한다. 기존 단어의 단순 활용형을 새 동사 표제어로 등록하지 않는다. `번갈아`는 `번갈다`, `차례로`는 `차례`로 등록하고 실제 활용/조사 결합은 예문에서 보여준다.
- predicate 및 expression의 `has_batchim`은 null. expression의 irregular_type은 null이며 Conjugation 대상에 넣지 않는다. predicate의 irregular_type은 검수된 분류만 기록한다.
- 복수 의미는 ordinal과 vocabulary_examples를 통해 의미별 예문을 연결한다. 동일 한국어/일본어 문장 쌍은 기존 Example ID를 재사용한다.
- 새 sort_key는 `힣:data05:400:NNNN`, learning_priority400. 숫자는 편집 순서이며 ID가 아니다. 기존 key/사용자 저장 membership을 재정렬하지 않는다.
- 기존 grammar-example 및 prerequisite 관계 변경은 모든 기존 끝점 revision을 올린다. 이번에는 grammar8개의 revision만+1, 본문 변경0. `data05-revised-ids.json`과 strict previous 검사로 허용 범위를 고정했다.
- 새 직접입력8문제는 기존 question_target/prerequisite와 검토된 accepted를 사용한다. ㅎ 현재형은 override 필수. 듣기4개는 source_example_id와 learning_order40~43으로 기존 batch를 보존한다. dictation question_type은 `listening_input`이며 원문 및 종결부호만 생략한 답을 허용한다.

```sh
python3 Tools/ContentBuilder/build_content.py Content/production.json Resources/content.sqlite --previous Tests/Fixtures/content-v11-production.sqlite --production --report Docs/DATA05_VALIDATION.json
python3 -m unittest discover -s Tools/ContentBuilder -v
```

v11 파일은 DATA-05 업데이트 재현용 이전배포 스냅샷이다. 새 DATA 작업에서는 v12를 previous로 사용한다. Validator 규칙은 변경하지 않았다. native integration과 한계는 `Docs/DATA05_INTEGRATION_AUDIT.md`를 따른다.

## 24. DATA-06 Listening 검수 및 현재 배포 기준

현재 Content13 / schema4 / reader7 / UserProgress8. 다음 작업은 v13 DB를 previous로 보관하고 content14 이상을 사용한다. 위 ‘현재’ 문구는 각 과거 배포 이력이다.

- 원본은 production.json 하나. data06-ids.json은 QA용 UUID 목록이다. 기존 Example을 source_example_id로 연결하고 본문을 복사하지 않는다.
- 기존 listening의 learning_order 및 시작된20개 구간은 변경하지 않는다. DATA06은 각level order60부터 새구간을 사용했다. ID는 편집 순서와 무관한 UUID다.
- 의미 선택은 기존 일본어 번역과 정확히 일치하는 정답1개. Korean 선택의 지시문은 실제 들린 문장 선택이며 다른 선택지도 자연스러운 기존 예문이다.
- Comprehension은 원문에서 답을 하나로 판단할 수 있는 질문을 작성한다. 허용 가능한 해석이 둘이면 질문/선택지를 바꾼다.
- Dictation은 원문 및 terminal punctuation 생략만 accepted에 추가한다. 임의 동의어/문법 변경을 허용하지 않는다. 기존 NFC/whitespace정규화·spacing warning을 변경하지 않는다.
- 제작 시 모두 source/example/question level을 맞춘다. 기존 example level을 문제 편성 때문에 임의로 바꾸지 않는다.
- TTS는 문장용 공통service, 녹음 전환은 itemID 유지. 기기별 voice 청취는 별도 gate이며 Validator 통과만으로 실제 발음 검증을 주장하지 않는다.
- 감사는 실제SQL/네이티브실행/소스검토를 구분하여 기록한다. unrun XCTest를 PASS로 적지 않는다.

```sh
python3 Tools/ContentBuilder/build_content.py Content/production.json Resources/content.sqlite --production --previous Tests/Fixtures/content-v12-production.sqlite --report Docs/DATA06_VALIDATION.json
python3 -m unittest discover -s Tools/ContentBuilder -v
```

위는 DATA06 재현용. 다음 배포 previous는 v13이다. 기존 문장에 새관계를 연결했다면 fingerprint 정책에 따라 endpoint revision을 증가시키고 승인목록으로 정확히 검증한다.

## 25. DEV-10 Curriculum / Placement와 DATA 제작 계약

DEV-10은 production content를 바꾸지 않는다. 현재 content13 / schema4 / reader7 / UserProgress8 유지, 다음 콘텐츠 배포는 v13을 previous로 보존하고 content14 이상 사용한다.

- 새 level별 vocabulary/grammar/listening은 기존 active content_items.level과 기존 course/lesson/set 정책으로 curriculum에 노출된다. 별도 curriculum용 텍스트/어휘 배열을 작성하지 않는다.
- 이미 배포된 UUID, sort_key, learning_order, lesson membership, 진행 중 session snapshot을 재배정하지 않는다. 총수만 늘어도 기존 확인 수·SRS와 skip 선호도는 유지한다.
- grammar lesson을 문자·발음 완료 수에 넣지 않는다. 각 모듈의 완료와 장기복습 진행은 별도 표시한다. level 변경을 mastery 또는 progress reset으로 구현하지 않는다.
- 활용 진입은 active text_input question의 rubric.production=1과 question_target 관계를 사용한다. question 없이 vocabulary만 추가하면 활용 목록에 나타나지 않는 것이 의도된 동작이다.
- 진단은 기존 production quiz/meaning/grammar question/production question/listening question을 조회한 snapshot이다. 현재8문항, 하위3단계 시작 위치만 추천한다. 콘텐츠 수정 시 실제 선별 문항과 distractor/정답 유일성을 다시 검수하고 XCTest의 기대 구성을 검토한다. 학습 예제를 무단으로 진단 정답 데이터와 분리 복제하지 않는다.
- 진단 snapshot은 시작 시 Content Version·stable ID·선택지 순서를 저장한다. 새 DATA가 들어와도 기존 진단 결과를 덮어쓰거나 SRS를 초기화하지 않는다.
- 사용자 위치 preference는 UserProgress.user_metadata 안의 versioned JSON이다. production source에서 사용자 시작 위치/진도를 작성하지 않는다.

## 26. DEV-11 검색·상세·사용자 저장 계약

Content13/schema4/reader7 유지, UserProgress9. 신규 production 본문/ID 변경0. 다음 DATA는 Content13 DB를 previous로 보존한다.

- 검색 대상: vocabulary.headword, 모든 활성 meanings.meaning_ja, grammar.pattern/meaning_ja/explanation_ja. 예문 번역·노트·활용형을 검색어 후보로 무분별하게 추가하지 않는다.
- NFC literal exact/prefix/contains 순서, 페이지30. 같은 항목의 여러 의미가 매치되어도 결과는 한 번만 반환한다. `%`, `_` 등은 일반 문자다.
- 상세의 vocabulary↔grammar는 공유 Example relation, lexical/grammar 관련어는 기존 content_links를 이용한다. 새 데이터 제작 때 링크 endpoint의 기존 stable ID/revision 정책을 유지한다.
- 상세의 활용은 ConjugationEngine과 production rubric.overrides를 재사용한다. 같은 lemma/form에 서로 다른 override를 넣으면 오류다. noun 또는 엔진 미지원 형태를 억지로 생성하지 않는다.
- Favorites에 content_type과 global stable ID를 저장한다. Content 교체/비활성화 때문에 사용자 즐겨찾기나 과거 학습기록을 cascade delete하지 않는다.
- 최근 본 기록은 최대30개이며 학습 완료/SRS와 무관하다. 검색이나 favorite만으로 새 SRS를 생성하지 않는다.
- 수동 연습은 기존 review tables의 *_practice scope. 실제 SRS 예약은 srs_state만 기준으로 한다. practice의 next_due_at은 결과 참조값이며 예정된 복습이 아니다. 정규 회독→SRS 계약은 변경하지 않는다.


## 27. DEV-12 통계·유지학습·짧은 복습 계약

Content schema4 / content13 / reader7 유지. UserProgress는 index-only migration10. 이번 단계에 production 본문/ID 추가·변경은 없다.

- DATA는 이미 배포한 UUID와 기존 세트 membership을 유지한다. 한글/발음 lesson의 stable step 순서가 그대로인 release는 동일 session/results를 재개한다. step list 자체가 달라지면 기존 안전 차단/재시작 정책이다.
- 통계는 user study_events/review_items/listening_attempts/SRS를 집계한다. Content source에 사용자 통계나 설정을 저장하지 않는다. 학습시간을 추측하여 넣지 않는다.
- 새 단어 복습의5/10/20 preference는 due queue만 제한하고 진행중 session의 stable IDs를 재선정하지 않는다. Grammar/Listening은 기존 bounded session/중단 재개를 사용한다.
- Maintenance는 이미 SRS에 있는 항목을 임의로 앞당기지 않는다. 오래된 미예약 단어 후보는 실제 학습 event,30일 cutoff, active round 제외, active Content ID 확인 후 기존 manual review에 연결한다.
- 문법·듣기에서 다양한 문제/예문을 제공하려면 기존 grammar/question/example relation을 확장한다. Maintenance 전용 duplicate sentence나 독립 progress schema를 만들지 않는다.
- 알림·학습량은 UserDefaults 설정이며 curriculum/production Content Version과 별개다. 기기 알림은 일반 학습초대이고 due 확정 문구를 source에 생성하지 않는다.
- 최종 실제 분량과 상급/녹음 공백, 임의 ID 제거 시 미완료 session 차단 한계는 PROJECT_STATUS와 DEV12_REQUIREMENTS_AUDIT에 명시했다.

## 28. DEV-13 수익화 독립성

광고 설정·StoreKit 상품·entitlement·광고 빈도는 Content source/DB에 넣지 않는다. 학습 콘텐츠는 무료 사용자와 구매자가 동일하게 사용한다. 콘텐츠 추가 때 Product ID/remove_ads cache 또는 광고 설정을 변경하지 않는다. Content13/schema4/reader7 유지. 신규 ProductionSession의 optional updatedAt은 UserProgress snapshot용이며 콘텐츠 필드가 아니다. 배포된 stable ID와 기존 membership을 계속 보존한다.

## DATA-07 — production vocabulary extension

- Source는 기존 Content/production.json 한 개. Content/data07-ids.json은 발급 ID/검수·테스트 색인이고 앱은 파싱하지 않습니다. 중간 작성 자료는 production/runtime이나 fixture로 배포하지 않습니다.
- 현재 Content14/schema4/reader7. 다음 업데이트 전에 현재 번들 DB를 보존하고 --previous로 지정합니다. 신규 data만으로 UserProgress10을 변경하지 않습니다.
- 새 vocabulary는 初級(beginner)/初中級(lower_intermediate)에 실제 편성되어 기존 Curriculum/20어휘 set 경로로 조회됩니다. 별도 course vocabulary 배열을 만들지 않습니다.
- sort_key는 힣:data07:01 또는02의 편집순서로 한 번 지정. learning_priority501/502는 편집배치 우선순위이며 공식 빈도 순위가 아닙니다. 배포된 순서/UUID는 재계산하지 않습니다.
- 서술어/expression has_batchim=null, 하다형other, 으·ㄹ 규칙적 탈락none. 일본어 뜻이形容詞처럼 보여도 적극적이다/소극적이다 같은 명사+이다는 expression으로 유지합니다.
- 이루어지다처럼 사전형을 lemma에 쓰고 예문의 자연스러운 축약은 별개로 설명합니다. 의미별 예문 연결을 유지하고 기한/기간 등 확실히 구별되는 관계만 추가합니다.
- source_example_id로 연결한 Listening은 transcript_ko를 복사하지 않습니다. Korean-choice 오답도 검수된 Example의 실제 문장을 사용해야 합니다. Dictation은 원문과 허용된 종결문장부호 변형만 사용합니다.
- 관계 추가로 기존 끝점의 서명까지 변하면 revision을 증가시킵니다. 이번30개 목록은 data07-revised-ids.json. 기존 본문/ID/정렬/사용자상태는 변경하지 않습니다.
- 검수는 Docs/DATA07_REVIEW.md와 전체 카탈로그 참조. 자동 Validator는 한국어/일본어 교육 내용의 정확성을 보증하지 않으므로 별도 재독과 필요시 사전 확인/전문가 검수를 계속합니다.

```sh
python3 Tools/ContentBuilder/build_content.py Content/production.json Resources/content.sqlite --production --previous Tests/Fixtures/content-v13-production.sqlite --report Docs/DATA07_DB_BUILD.json
sh Tools/verify.sh --portable
```

위 명령은 DATA-07 재현용입니다. 다음 DATA에서는 이전DB 경로를현재Content14 snapshot으로 바꾸고 새 ContentVersion을 사용합니다. Mac Release/XCTest 절차는 RELEASE_CHECKLIST.md를 따릅니다.

## DATA-08-A — 初中級 Batch A 제작·검수 계약

- Runtime은 `Content/production.json` → 기존 ContentBuilder → `Resources/content.sqlite` 하나다. `data08-a-ids.json`은 발급 UUID/검수 색인이다. 원본 밖의 초안이나 임시 DB를 앱에서 읽지 않는다.
- Content14 원본 DB를 `Tests/Fixtures/content-v14-production.sqlite`에 보존하고 Content15로 배포했다. 다음 콘텐츠 배포는 실제 직전 Content15를 별도 보존한 후16 이상으로 증가시킨다. 데이터 확장만으로 Schema4/Reader7/UserProgress10을 바꾸지 않는다.
- Stable ID/created_at/기존 본문/sort_key/learning_order/사용자 membership을 유지한다. 새 편집순서는 `힣:data08:a:NNNN`, priority601이며 빈도 순위가 아니다. 변경 관계의 기존 끝점23개 revision+1 목록은 `Content/data08-a-revised-ids.json`이다.
- 의미별 예문을 연결한다. 다의어17개는 각2meaning, 모든 신규 어휘는2문장이다. `meanings.usage_ja`의 Collocation과68개 Note는 검수용 본문과 같다. 이미 같은 문장은 기존 ID를 재사용하며 신규량을 관계 수로 계산하지 않는다.
- 들르다는 none(으 탈락), 서투르다/어지르다는 reu, 너그럽다/얄밉다 등은 b, 하다형은 other다. predicate/expression의 has_batchim은 null이다. 맞추다(合わせる/照合する)와 맞히다(正解する)를 구분한다.
- 기존 Grammar의6예문 조회 한도를 넘기는 연결은 채택하지 않았다. 신규14연결은 기존 예문 노출을 모두 보존하며 실제 SQL로 조회된다. runtime을 바꾸어 콘텐츠 개수를 맞추지 않는다.
- 검수는 작성 assistant의 전 항목 재독이며 독립 전문가 승인이 아니다. `Docs/DATA08_A_REVIEW.md`와 전체 카탈로그를 참고한다. 한국어/일본어 품질과 실기기 음성은 자동 Validator가 보증하지 않는다.

현재 배포 재현 명령(프로젝트 루트, 출력은 임시 경로):

```sh
python3 Tools/ContentBuilder/build_content.py Content/production.json /tmp/data08-a.sqlite --production --previous Tests/Fixtures/content-v14-production.sqlite --report /tmp/data08-a-report.json
sh Tools/verify.sh --portable
```

이 명령은 DATA-08-A/Content15 재현용이다. 다음 배포에 v14를 그대로 previous로 쓰지 않는다. Validator0errors/기존10warnings, portable243PASS. native127개·iOS 빌드·실기기는 미실행이며 기존 release gate를 유지한다.

## DATA-08-B 제작·검수 계약 (Content16)

- 직전 실제 Content15는 `Tests/Fixtures/content-v15-production.sqlite`에 byte 그대로 보존한다. 빌드: `python3 Tools/ContentBuilder/build_content.py Content/production.json /tmp/content16.sqlite --production --previous Tests/Fixtures/content-v15-production.sqlite --report /tmp/content16-report.json`.
- 전체 DATA-08 목표800~1,200어휘/1,300~2,000문장을 유지한다. A+B 누적601/1,202, 잔여199~599/98~798. 이번 B는300/600 승인, 다음 Batch 미실행.
- 세 묶음 각100어휘/200문장에 개별 한일 재독·Duplicate Audit·UUID/이전 payload·strict Validator를 적용했다. `DATA08_B1~B3_AUDIT.json`/`VALIDATION.json`에 실제 누적값을 보존한다. 자동 검사와 assistant 자기검수를 독립 전문가 승인으로 표시하지 않는다.
- 전300항목의 Collocation은 meaning의 `usage_ja`, 100 Note는 기존 learner_note 관계를 이용한다. 미치다/대비하다 등의 의미 범위·조사/동사 방향·유의어 차이를 설명한다. 부사처럼 쓰이는 조사 결합은 기본형을 확인한다(애초/반대/마찬가지).
- `Content/data08-b-ids.json`은 검수 색인이다. 새 UUID4는 한 번 발급해 유지한다. 기존 모든 ID/상세본문/정렬/membership 보존, 관계 끝점28개만 승인 목록대로 revision+1/updated_at. 기존 경고10·제약·validator 유지.
- Grammar 참조15개는 기존 예문과 함께 실제LIMIT6에서 보인다. 의미별 Example ID는 기존 Listening/Sentence Production에서 재사용할 수 있으나 새 듣기/문항 수는0이다. schema4/reader7/UserProgress10 및 실제 활용 엔진·has_batchim/irregular 계약은 유지한다.
- 회귀검사: `sh Tools/verify.sh --portable`. A의 정확한 cohort는 v15 fixture에서, B의15→16과 A 포함 기존 payload/진도 보존은 현재 Bundle에서 확인한다. native128개와 실제3~10분/offline·중단·음성·접근성·광고/IAP gate는 Mac/iPhone에서 별도로 실행한다.

상세·교정·원본/번역 카탈로그·검수 hash: `Docs/DATA08_B_REVIEW.md`, `DATA08_B_REVIEW_CATALOG.md`, `DATA08_B_EDITORIAL.json`, `DATA08_B_COUNTS.json`.


## DATA-08-C 제작·검수 계약 (Content17)

- 실제 직전 Content16 DB/source를 `Tests/Fixtures/content-v16-production.sqlite` / `content-v16-production.json.gz`에 보존한다. gzip은 역사 검사용이며 runtime 입력이 아니다. 다음 배포는 현재 Content17을 보존해 previous로 사용한다.
- C 재현: `python3 Tools/ContentBuilder/build_content.py Content/production.json /tmp/content17.sqlite --production --previous Tests/Fixtures/content-v16-production.sqlite --report /tmp/content17-report.json`. 기존 schema4/reader7/UserProgress10을 유지하며 candidate를 검수한 후에만 Bundle로 반영한다.
- C 신규310 Vocabulary는 일반280/phrase30, 신규 문장619와 기존 예문1 재사용을 별도 집계한다. Phrase는 기존 expression 품사와 색인 lexical_category로 구분한다. 신규 Grammar/Listening/Question0. 전체 DATA-08 누적911/1,821, phrase 제외 일반어휘807, 부족0/0.
- 100/100/110어휘 묶음별 한일 개별 재독·Duplicate Audit·Stable UUID4·Relation·strict gate를 적용했다. 전310 Collocation=`meanings.usage_ja`, Register=`meanings.nuance_ja`, Note146·다의어24항목. 검수 주체는 같은 assistant이며 독립 전문가 승인이 아니다.
- 기존 ID/상세본문/정렬/학습 membership 보존. 관계 끝점46개만 `Content/data08-c-revised-ids.json`대로 revision+1. 기존 예문1개는 ID/본문을 재사용하고 새 관계만 추가한다. 신규 중복0, strict 오류0/기존 경고10·FK0·integrity ok.
- 기존 Grammar 참조17개가 실제 LIMIT6에 보이는지 검사한다. Meaning별 Example 참조를 기존 Listening/Sentence Production에서 재사용 가능하게 유지한다. predicate/expression has_batchim=null, expression irregular_type=null, 하다형 other 및 기존 불규칙 엔진 계약을 따른다.
- `sh Tools/verify.sh --portable`:269 PASS. A/B 정확한 과거 배포 회귀군은 원본 fixture에서 유지하고 C는 현재 Bundle에서 전체 보존/16→17 갱신·부분 session·SRS/UserProgress를 검사한다. native129개는 Mac에서 별도 실행한다. 실제3~10분/offline·음성·중단·접근성·광고/구매 gate는 유지한다.

근거: `Docs/DATA08_C_REVIEW.md`, `DATA08_C_REVIEW_CATALOG.md`, `DATA08_C_EDITORIAL.json`, `DATA08_C_COUNTS.json`, `DATA08_C1~C3_AUDIT.json` / `VALIDATION.json`.


## DATA-08-FINAL — 최종 감사와 Content18 교정 계약

- 실제 직전17 DB/source를 `Tests/Fixtures/content-v17-production.sqlite` / `content-v17-production.json.gz`에 보존한다. 현재 runtime은 기존 Source→ContentBuilder→Bundle 구조다. Content18/schema4/reader7/UserProgress10, 신규 행/ID/관계/Level·정렬·사용자DB 변경0.
- 재현: `python3 Tools/ContentBuilder/build_content.py Content/production.json /tmp/content18.sqlite --production --previous Tests/Fixtures/content-v17-production.sqlite --report /tmp/content18-report.json`.
- 추가 감사: `python3 Tools/ContentBuilder/audit_data08_final.py Content/production.json --database /tmp/content18.sqlite --report /tmp/content18-audit.json`. 전체 필드/참조/중복과 A~C 특정 계약·관찰된 재발 패턴을 검사한다. 정상 결과는 언어 품질이나 사람 검수를 보장하지 않는다. core Validator는 허용 줄바꿈/탭 외 제어문자도 거부한다.
- 34어휘43필드(정확한 전후 값=`Docs/DATA08_FINAL_FINDINGS.json`)만 교정했고40엔티티만 `Content/data08-final-revised-ids.json`대로 revision+1/updated_at. `실마리가 보이다`는 기존 해결 단서 표현의 결합 교정이며 ID/의미/품사·사용자 기록을 유지한다. 과거 A/B/C 색인은 당시 배포의 식별/검수 기록이다. 현재 본문과 표제어는 Source/DB 및 FINAL_EDITORIAL을 따른다.
- 한국어·일본어를 별도 재독하고 다의어52항목의 의미별 예문/Collocation, 조사/활용·Register·번역 방향·혼동어 Note를 재검수한다. 확정 오류와 자연스러움 개선/의심 후보를 구분한다. 같은 유형을 전체 Production에서 다시 검색하며 후보 수를 오류 수로 세지 않는다.
- 무작위 표본은 정렬된 UUID 모집단·seed·구간/Level·추출 수·선택ID를 보존한다. 이번85추출/고유84개는 Batch/POS/실제 Level을 대상으로 했다. 모집단0인 Level의 표본을 꾸미지 않는다.
- 선행Grammar 후보163예문은 `Docs/DATA08_FINAL_GRAMMAR.json`의 제한적 inventory다. 예문과 참조의 존재를 전체 선행 학습 경로의 보장으로 표현하지 않는다. Note의 짧은 설명과 실제 등록 Grammar unit을 구분한다. 공식 Level/빈도나 독립 전문가 승인을 추측하지 않는다.
- `sh Tools/verify.sh --portable`:280 PASS. A/B/C 역사 검사는15/16/17 fixture에서 유지하고 새11개 회귀군은 현재18의 전체 변화·실제 카드/검색·부분session/UserProgress 보존을 검사한다. native130개/실제 iPhone은 Mac에서 별도 검증한다. 사람 검수 미실행·B—Conditional 및 기존 gate 유지.

근거: `Docs/DATA08_FINAL_REVIEW.md`, `DATA08_FINAL_EDITORIAL.json`, `DATA08_FINAL_FINDINGS.json`, `DATA08_FINAL_SAMPLES.json`, `DATA08_FINAL_RESCAN.json`, `DATA08_FINAL_DICTIONARY.json`, `DATA08_FINAL_COUNTS.json`, `DATA08_FINAL_TEST_LOG.txt`.


## DATA-08-INTEGRATION — Content19 / Schema4 / reader7 (2026-10-19)

- DATA08 lexical payload는 Content18 감사본과 동일하다. 추가된 course/47 lessons/3 unit tags,1,821 listening과2,983 question의 실제 ID는 `Content/data08-integration-ids.json`이 기준이다. Unit은 `curriculum_unit` tag와 제목으로 표현하며 별도 Unit schema를 신설하지 않는다.
- vocabulary lesson은 공통 card reader → explanation preview(`vocabulary_preview`,viewed) 경로로 실행하며 회독/SRS 완료와 구분한다. 사용자 Set은 기존 allocator에서20개로 할당하고 재정렬/초기화하지 않는다.
- 듣기는 source_example_id와 related Example ID를 유지한다. 이번 dictation accepted는 기존 Korean 원문, prompt_ko=null이다. 배포된 learning_order는 그대로 두고 신규220~2040을 뒤에 추가했다.
- 동사/형용사581개만 -고 활용형과 기존 문장 재현에 연결한다. `form`/`sentence` mode·prerequisite를 유지하며 문장을 재편집하면 원 Example/accepted/prompt 번역도 함께 검토해야 한다. 명사·부사·표현을 활용 대상으로 바꾸지 않는다.
- 이전18 DB/source를 반드시 strict previous로 사용한다. 기존911어휘+1,821예문+-고 Grammar1의 관계 fingerprint 변경만2,733 allowlist에 따른 revision+1이다. 이전 상세본문/ID/순서/기존 membership과 A~C 검수 이력은 변경하지 않는다.
- 상세 재현·테스트·성능·미실행 gate는 `Docs/DATA08_INTEGRATION.md` / `DATA08_PROGRESS.md` §14. 자동/SQL 통과는 native나 사람 언어 검수 완료가 아니다.


## DATA-08-SYSTEM — 복습 가용성/받아쓰기 계약 (Content19 유지)

- DATA08-7은 runtime 감사/수정이며 Production source/DB/content/schema/minReader/UserProgress version을 바꾸지 않는다.
- unavailable review는 현재 카드 확인 후 명시적으로 보류한다. 원래 review_items ID/순서/판정과 SRS schedule은 남기고 completedCount와 deferredCount를 구분한다. 이번 Content Version의 quarantine metadata만 새 due query/숫자에서 제외한다. 새 Content Version을 configure하면 원래 due로 재시도한다.
- 듣기 due는 새 snapshot 전에20개씩 Content 가용성을 확인한다. 정상 조회에서 누락된 ID만 버전별로 보류하며 DB/decoding 오류를 ‘퇴역’으로 추정하지 않는다. 기존 active listening snapshot은 재조회/재작성하지 않는다.
- dictation은 끝 .!? 생략을 허용하되 내부 부호·어휘·철자 차이를 정답으로 합치지 않는다. 띄어쓰기 피드백을 유지한다. 일반 ProductionAnswer의 exact/spacing 규칙은 변하지 않는다.
- 자동 alias 병합/기존 고정 회독 ID 대체·자동 완료·SRS 초기화를 허용하지 않는다. 원래 명세 미확보/Native137개 BLOCKED/사람 검수 NOT TESTED와 B—Conditional을 보존한다. 상세 DATA08_PROGRESS §15.


## DATA-08-CLOSEOUT — Content19 재구성·원본 보존 계약

현재 runtime은 `Content/production.json` + `content-schema-v4.sql` → 기존 Importer/Validator → `Resources/content.sqlite`이며 Content19/Schema4/reader7이다. 신규911(일반807/표현104)/문장1,821, 전체2,287/4,597(문장4,584). source/ID registry·DDL·과거 snapshot을 반드시 Git 보존한다. 번들 DB는 재생성 가능하지만 현재 Xcode가 포함하는 배포 자산이므로 추적을 유지한다. synthetic/candidate/staging/WAL/SHM/Xcode 출력과 구분한다. `*.sqlite`/`Content/*.json` 전체를 ignore하거나 원본을 지워 대용량 오류를 우회하지 않는다.

동일19 재현에는18 fixture를 `--previous`로 사용해 `/tmp` candidate를 만든다. 위 DATA08_CLOSEOUT 명령으로 전체31테이블·schema/index·SHA까지 일치했다. 다음 콘텐츠 변경은 현재19 DB를 먼저 불변 snapshot으로 보존하고19를 previous로 지정한 strict gate를 통과시킨다. Content Version은 실제 본문/관계 변경 정책대로만 갱신하고 schema 변경이 없으면 Schema4 유지. 이번 문서/검증 변경은 Content19를 유지한다.

원본16,638,955bytes/번들17,932,288bytes, 현재 접근 가능한 Git 이력의50MiB/100MiB 초과 blob0이므로 LFS 도입 불필요. 향후 JSONL shard 또는 필요한 원본에 한한 LFS를 별도 검토한다. 독립 사람 검수·163선행 문형·native gate는 미완료다. 상세·정확한 재현 명령은 [최종 보고](Docs/DATA08_CLOSEOUT.md).


## DATA-09-A — 문법 원본·버전 계약

이번 승인 snapshot은 Content20/Schema4/reader7/UserProgress10이다.18개 문법은 기존42개와 다른 학습 기능이며72개 신규 한일 예문/72개 multiple_choice 문제를 연결한다. grammar_task는 meaning/form/context/contrast 각18개,선택지3개/정답1개/개별 일본어 이유를 사용한다. source/DB/기존19 snapshot·한 번 발급한 UUID와12개 revision allowlist를 보존한다. 텍스트 accepted/free-writing/지원하지 않는 ConjugationForm은 추가하지 않았다.

문법 수는 入門22/初級20/初中級18,현재 Grammar60이다. DATA09 신규18과 장기350~500개 목표를 구분한다.18단위에서 품사·시제 이형태/위해·위한 등을 별도 신규로 세지 않는다. 기존54안의 배치 조정은 DATA09_A_SCOPE.json이 기준이며 과거 계획을 수정해 승인된 것처럼 표시하지 않는다.

다음 실제 콘텐츠 변경은20 DB/source를 먼저 보존하고20을 --previous로 strict 검증한다. 현재20 재현에는19 fixture를 사용한다. authoring/검수 색인은 runtime 입력이 아니며 앱은 production.json에서 생성한 번들 DB만 읽는다. 이번 검증·한계는 DATA09_PROGRESS §8,미검증 native/사람 gate는 유지한다.
