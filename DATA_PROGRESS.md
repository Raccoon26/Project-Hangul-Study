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
