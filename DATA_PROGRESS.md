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
