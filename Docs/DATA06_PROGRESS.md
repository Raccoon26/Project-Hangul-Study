# DATA_PROGRESS — DEV-14 / DATA-06 / 2026-10-05

실제 production Resources/content.sqlite 집계. Source=Content/production.json.
**Schema4 / Content13 / Reader7 / UserProgress10**. synthetic/fixture 제외.

| 항목 | 현재 / 목표 | 분포 |
| --- | ---: | --- |
| Vocabulary | 926 / 15,000 | 入門306 / 初級620 |
| Example sentences | 1,863 / 30,000 | 발음예시13 제외 |
| Examples 전체 | 1,876 | 문장1,863 + 발음13 |
| Grammar | 42 / 350~500 | 入門22 / 初級20 |
| Listening | 111 / 1,000+ | 入門34 / 初級77 |
| Dictation | 28 | Listening에 포함 |
| 의미 선택 | 31 | Listening에 포함 |
| 한국어 선택 | 26 | Listening에 포함 |
| 내용 이해 | 26 | Listening에 포함 |
| Questions | 342 | DATA06 신규80 |
| Pronunciation | 36 | 유지 |
| 현대 한글 자모 | 40 / 40 | 기타조합설명 포함 hangul55행 |
| 문장/작문 문제 | 6 / 2,000 | 직접입력 blank3+sentence3, form51 별도 |
| TOPIK 유형 | 0 / 1,000 | 공식 등급 미생성 |

Meanings982, learner_notes181, vocabulary_examples1792, grammar_examples95, content_items4663.

## DATA-06 추가분

Listening80 / Questions80. 4유형 각20, 入門21/初級59. 기존 Example80개 재사용, 신규 Example0. 신규 vocabulary/grammar0. 기존 본문 변경0, source Example80개 관계 revision+1. 새 stable UUID와 기존 learning_order 보존.

Validator 오류0/기존경고10. Python/SQLite174개PASS. Swift62파일 구문 오류0. XCTest84개 작성·미실행. native build/Audio/Navigation 미검증. PROJECT_STATUS.md와 Docs/DATA06_INTEGRATION_AUDIT.md 참조.

다음 DATA는 v13 DB를 previous로 보존하고 content14 이상을 사용한다.

## 누적 배치 이력

| 배치 | 신규 어휘 | 신규 문장 쌍 | 신규 의미 | 신규 note | Content |
| --- | ---: | ---: | ---: | ---: | ---: |
| DEV-01~04 | 0 | 0 | 0 | 3 | 4 |
| DATA-01 | 226 | 447 | 244 | 65 | 5 |
| DATA-02 | 250 | 500 | 260 | 32 | 6 |
| DATA-03 | 250 | 500 | 268 | 48 | 7 |
| DATA-04 | 0 | 53 | 0 | 0 | 11 |
| DATA-05 | 200 | 339 | 210 | 33 | 12 |
| DATA-06 | 0 | 0 | 0 | 0 | 13 |

DEV-05/06은 콘텐츠 수 변경 없이 회독/SRS를 연결했습니다. DATA-03 신규 level은 入門 10 / 初級 240입니다. 기존 어휘/의미/예문 수정 0개, 기존 ID/본문/관계 모두 유지했습니다.

## DATA-03 품사·영역

| 품사 | 신규 수 |
| --- | ---: |
| verb | 109 |
| adjective | 51 |
| adverb | 30 |
| noun | 52 |
| bound_noun | 8 |

동사·형용사·부사 190개(76%). 단어마다 예문 2개, 다의어 18개는 두 의미마다 예문을 연결했습니다.

| 영역 | 신규 수 |
| --- | ---: |
| 考え・判断 | 10 |
| 話す・頼む | 10 |
| 物を動かす | 10 |
| 変化・自動詞 | 10 |
| 変える・整える | 10 |
| 時間がかかる・暮らす | 10 |
| 身近な動作 | 10 |
| 体を動かす | 10 |
| 感情を表す動詞 | 10 |
| 気持ち・体調 | 10 |
| 人・物の性質 | 10 |
| 状態を詳しく言う | 10 |
| 見た目・感覚 | 10 |
| 会話によく出る副詞 | 10 |
| 頻度・時間の副詞 | 10 |
| 程度・やり方 | 10 |
| 毎日の出来事 | 10 |
| 気持ちを話す名詞 | 10 |
| 時間・単位の補強 | 10 |
| 見つける・つながる | 10 |
| 身近な仕事・学習 | 10 |
| 大切な状態 | 10 |
| 量・お金・生活 | 10 |
| 伝えるための言葉 | 10 |
| 学習と日常の道具 | 10 |

## DEV-07 추가

신규 grammar **12**(入門 6 / 初級 6), 문장 **24**, questions **24**, courses **2**, lessons **4**, contrast 관계 **10행(5쌍 양방향)**. 어휘/의미 추가 0, 기존 production 본문 수정 0. 문법 12개에 inline confusion_ja 학습 note가 있으며 learner_notes 148행과 별개입니다. 총 courses 4 / lessons 30 / content_items 3,446입니다.

현재 examples 1,484행 중 실제 문장 1,471개와 기존 발음 단어 예시 13개를 구분했습니다. grammar_examples 24, 의미 772, 기존 vocabulary_examples 1,452는 유지합니다. 수치는 실제 번들 DB에서 조회했습니다.

## DEV-07 당시 검증 / 다음 작업 (이력)

- Validator 오류 0 / 기존 검토 경고 10. 신규 grammar 중복 후보 0. 기존 3,380 content ID/payload/fingerprint 유지.
- Python/SQLite **138개 통과**, Swift **53파일 구문 오류 0**, Native XCTest **66개 작성, 미실행**.
- UserProgress v5→v6 additive migration과 단어/문법 SRS 분리, 문법 due/재등록/문제 snapshot 재개 SQL을 확인했습니다. Swift UI·네이티브 runtime 검증을 대신하지 않습니다.
- 외부 교육 전문가 감수, Mac 빌드, 실제 기기 UI/TTS 청취는 미수행입니다.
- DATA-04는 현재 **content v8**을 보관하여 --previous로 검증하고 content 9 이상으로 올립니다. 기존 UUID/배포 정렬키/세트 snapshot/사용자 기록을 재생성하지 마세요.

## DEV-08 추가 (실제 DB 집계)

신규 vocabulary/grammar/examples **0**. 기존 16 lemma에 production 직접입력 **49문제**(form 43 / blank 3 / sentence 3), level 入門 47 / 初級 2입니다. 기존 예문 3개를 활용하며 23개 기존 항목은 새 관계에 맞춰 revision만 올렸습니다. 본문·UUID·정렬키는 유지했습니다. 누적 content_items 3,495 / questions 163 / vocabulary 726 / grammar 12 / examples 1,484입니다.

Content 9 / reader 6 / schema 3 / UserProgress 7. Validator 오류 0, 기존 경고 10. Python/SQLite 142개 통과, Swift 58파일 구문 검사, Native XCTest 71개 작성·미실행. 앞 DEV-07 검증 절은 당시 이력이며 다음 DATA는 **현재 v9를 previous로 보관하고 content 10 이상**을 사용합니다.

## DEV-09 추가 (production DB 실제 집계)

Vocabulary/Meanings/Examples/Grammar 추가 0. 기존 예문 24개를 참조하는 Listening **24**(入門12/初級12), Questions **24**(meaning6/korean6/dictation6/comprehension6). 녹음0 / 시스템TTS24. 기존 example24개는 관계 추가에 따른 revision만 증가했습니다. 문장 본문·번역·기존ID 유지.

현재 content_items **3,543**, vocabulary **726**, meanings **772**, examples **1,484**(문장1,471+발음단어13), grammar **12**, pronunciation_rules **36**, listening_items **24**, questions **187**, learner_notes **148**입니다. 기존 vocabulary level은 入門306/初級420 그대로입니다.

Schema4 / Content10 / Reader7 / UserProgress8. Validator 오류0/기존 경고10. Python/SQLite149개 통과. Native XCTest78개 작성·미실행, Swift62파일 구문 검사. 실제 음성·교육전문가 감수·Xcode 빌드 미수행. 다음 작업은 v10 DB를 previous로 보관하고 content11 이상 사용.

## DEV-10 / 2026-10-04

신규 vocabulary/example/grammar/listening/question **0**. Content13 / schema4 / reader7 / UserProgress8 유지. production.json과 content.sqlite는 DATA-06 배포본과 byte-for-byte 동일함을 확인했다. 위 최신 DATA-06 실제 DB 총수는 그대로다.

기존 콘텐츠의 level별 진입, 시작 위치·진단 snapshot, 기존 회독/SRS와 독립적인 curriculum 표시를 연결했다. Python/SQLite180개 통과, Swift68파일 구문 오류0, XCTest88개 작성·미실행. native build/UI/audio 미검증. DEV10 PROJECT_STATUS 및 Integration Audit 참조.

## DEV-11 / 2026-10-05

신규 production 콘텐츠0. Vocabulary926 / Examples1876(문장1863) / Grammar42 / Listening111 / Questions342 유지. Content13/schema4/reader7 유지. **UserProgress9**로 typed favorites/recent 추가, 기존 진도·SRS 보존.

검색·상세·즐겨찾기·수동 연습 연결. 15,000어휘/30,000예문/500문법의 synthetic 검색 성능 측정은 temporary fixture이며 위 production 수량에 포함하지 않는다. Python/SQLite191 PASS, native XCTest94 작성·미실행. 실제 build/UI/Audio 미검증. PROJECT_STATUS와 DEV11_INTEGRATION_AUDIT 참조.


## DEV-12 / 2026-10-05

Production vocabulary/example/grammar/listening/question 신규0, 변경0. DEV11 ZIP과 source/DB byte-for-byte 동일. DB 직접집계: Vocabulary926(入門306/初級620), Meanings982, Examples1876(문장1863), Grammar42(入門22/初級20), Listening111/Dictation28, Questions342, Pronunciation36, hangul55(현대자모40). 수량 확대는 하지 않았다.

Content13/schema4/reader7 유지, UserProgress10 index-only migration. strict Validator 오류0/기존검토경고10, integrity ok/FK0, Python·SQLite203 PASS. Statistics/Maintenance/Settings/ShortReview/Reminder를 기존 로컬 학습과 연결했다. Native XCTest104 작성·미실행, Swift80파일 구문검사 오류0. Xcode/실기기 검증 미수행. 실제 production 집계는 Docs/PRODUCTION_COUNTS_DEV12.json, 요구사항 공백은 PROJECT_STATUS 및 Docs/DEV12_REQUIREMENTS_AUDIT.md 참조.

## DEV-13 확인

Production source/DB는 DEV12와 byte-for-byte 동일. 신규 vocabulary/examples/grammar/listening/questions0. Content13/schema4/reader7/UserProgress10 유지. Validator 오류0/기존경고10. 수익화 설정·권한은 Content와 독립이며 기존 stable IDs/세트/SRS를 변경하지 않는다.

## DEV-14 실측 재확인

추가 vocabulary/example/grammar/listening/question 모두0. 실제 DB counts는 Docs/STATIC_AUDIT_DEV14.json 참조. DEV-13 production source/DB와 바이트 동일. integrity_check=ok, foreign_key_check=0. Content13 유지. **Content Expansion Required**: 중상급 이상 전체 curriculum과 목표 규모는 미완성.
