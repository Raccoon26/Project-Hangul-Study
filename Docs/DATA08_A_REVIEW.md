# DATA-08-2 / Batch A 개별 검수와 통합 결과

2026-10-19 (Asia/Tokyo). Runtime source는 `Content/production.json` 하나이며 아래 보고서는 검수/전달용이다.

## 범위와 실제 수량

목표 初中級 Vocabulary270~400 / Example450~650에 대해 **301개 / 602문장**을 승인·반영했다. 최초 작성 목표300/600에서 맞추다/맞히다 구분을 명확히 하기 위해 맞히다1개/2문장을 추가했다. 품질을 이유로 줄인 수량은 **0**이다. DATA-08 전체800~1,200어휘/1,300~2,000문장 목표도 유지한다. Batch B 이후 작업은 수행하지 않았다.

| 항목 | Batch A 증가 |
| --- | ---: |
| Vocabulary / Meanings | 301 / 318 |
| 신규 문장 Example / vocabulary_examples 관계 | 602 / 602 |
| 두 의미로 분리한 어휘 | 17 |
| 일본인 학습자 Note / 명시적 Collocation 제공 어휘 | 68 / 68 |
| 어휘 관계 | 45 |
| 기존 Grammar에 새 예문 연결 | 14 (기존 문법14개) |
| 신규 Grammar / Listening / Question | 0 / 0 / 0 |
| 새 Stable ID (content_items) | 1,295 |
| 기존 끝점 revision+1 | 23 (어휘9 / 문법14) |
| 기존 본문·sort_key·learning_order 변경 / 삭제·비활성화 | 0 / 0 |

품사: 동사150 / 형용사51 / 부사40 / 표현40 / 명사20. 명사6.64%, 나머지93.36%. 인간관계49 / 감정57 / 부탁·거절36 / 오해·갈등57 / 일상생활44 / 학교·직장58. 각 항목은 위 여섯 편집 주제 중 하나에 속한다. 공식 TOPIK 등급이나 빈도 순위가 아니다.

## 작성 후 별도 재독

검수자는 작성한 **assistant**다. 301개 전체의 기본형·품사·metadata·의미·양쪽 예문과 번역을 다시 읽었고, 필요한68개 Note도 개별 재독했다. 독립된 사람/한국어·일본어 교육 전문가의 승인이나 기기별 음성 감수는 받지 않았다. 자동 Validator만으로 자연스러움을 인증하지 않는다.

1. 기존1,376개 표제어와 비교해 동일 표제어 후보를 먼저 제외했다. 무효한 단어 조각/미검수 후보는 최종 원본에 넣지 않았다.
2. 전301개/602문장의 한국어 문법·자연스러움·조사·활용·띄어쓰기·목표 의미·주제와 初中級 난도를 확인했다.
3. 일본어 번역의 의미·주어/수동태·시제·존대·문체·감정 강도를 원문과 대조했다. 한국어 해요체에 대응하는 일본어 丁寧体를 기본으로 했다.
4. 다의어는17개를318개 meaning으로 분리하고 각 의미에 실제 예문을 연결했다.기존 단어의 단순한 바꿔 쓰기나 활용형을 새 ID로 늘리지 않았다.
5. 기존/신규 한국어 문장을 NFC·공백·casefold로 정규화해 대조하고 한일 문장 쌍도 확인했다. 기존 문장과 중복0 / 신규끼리 중복0. 같은 문장에 목표 단어만 바꾸는 방식으로 채우지 않았다.
6. 최종 모든 카드/의미/예문/Note와14문법 연결/45어휘 관계를 기존 repository SQL로 조회한 뒤 후보를 승인했다. 검수 payload별 SHA-256은 `DATA08_A_EDITORIAL.json`에 보존했다.

전체 원문/번역/의미 ID/Note는 `DATA08_A_REVIEW_CATALOG.md`에서301개 모두 확인할 수 있다. 자기검수 상태와 fingerprint는 콘텐츠의 무오류 보증이 아니라, 어떤 최종 내용을 검수했는지 추적하는 기록이다.

## 개별 교정과 의미 구분

승인 전 **19항목/29필드**를 교정했다. 이전 배포 데이터가 아닌 이번 초안의 수정이다. 전후 값은 `DATA08_A_EDITORIAL_CORRECTIONS.json`에 보존했다.

- **맞추다 / 맞히다**: 초안의 맞추다=「正解する」를 고쳐 「合わせる／照合する」로 분리했다. 예문도 정답을 내는 장면에서 서로 답을 비교하는 장면으로 수정했다. 正解する는 새 맞히다 항목으로 제공하고 혼동 관계/Note로 연결했다.
- **대하다 / 오가다 / 냉정하다 / 풀리다 / 씁쓸하다 / 사정 / 형편 / 따지다 / 물러서다 / 맞추다 / 익히다 / 지원하다 / 조율하다 / 학점 / 말을 돌리다 / 손을 내밀다 / 힘이 빠지다**: 각 두 의미를 별도 meaning과 예문으로 구분했다. 예: 지원하다는「応募する」와「支援する」의 조사/목적어를 나눴다.
- 의존하다의 결정/의존 대상 표현을 `무슨 일이든 부모님께 의존하고 싶지 않아요.`로 명확히 했다. 탓하다의 반복 설명도 상황과 대상을 간단히 바꿨다.
- 감추다의 모호한 마음 표현, 씁쓸하다의 소식 맥락, 불쑥의 질문 주체, 속이 상하다의 중첩 주어를 명확히 하고 일본어도 함께 수정했다.
- 지치다의 불필요한 `-다 보니`, 쑥스럽다의 `-려니`, 고단하다의 `-더니`를 더 단순한 예문으로 바꿨다. 하마터면의 핵심 `-(으)ㄹ 뻔하다`는 학습 포인트와 Note로 설명하되 새 Grammar가 완성됐다고 표시하지 않았다.
- 정이 들다의 `정이 들어 버리기 어려워요`는 보조용언처럼 오독될 수 있어 `정이 들어서 버리기 어려워요`로 고쳤다. 능숙하다의 결합, 준비되다의 `마음의 준비` 명사구, 양해의 조사, 메우다의 빈자리 표현을 다듬었다.
- 평가받다 두 번째 문장은 `높이 평가받았어요`로 바꿔 실제 등록 기본형을 직접 보여 준다. 일본어 Note의 불필요한 한국어 설명어도 일본어로 통일했다.

## Collocation·유사/혼동어·자동사/타동사

`meanings.usage_ja`에68항목의 결합을 명시하고 Note에서 조사·문체·혼동을 설명한다. 그 외 항목도 목표 의미의 두 예문에서 실제 결합을 보여 준다. 사양하다/거절하다, 변명하다/해명하다, 보완하다/보충하다, 친밀하다/친숙하다를 무조건 동의어로 처리하지 않았다.

- 상태/작용 방향: 드러내다/드러나다, 둘러싸다/둘러싸이다, 배정하다/배정되다, 허락하다/허락받다/허락되다, 승인하다/승인되다, 반영하다/반영되다.
- 인계하다/인수하다: 일본어에서 둘 다「引き継ぐ」로 번역되므로 주는 쪽/받는 쪽을 Note로 구분.
- 너그럽다/쑥스럽다/얄밉다 등은ㅂ, 어지르다/서투르다는르, 들르다는으 탈락을 기존 엔진의none 분류로 처리한다. 하다형은other, predicate/expression has_batchim은null, expression irregular_type도null이다.
- 반말하다/존대하다는 연령만으로 말투를 결정하지 않고 관계·상호 합의·상황을 설명한다. 입이 가볍다/눈치가 없다/정이 떨어지다의 직접적인 부정적 평가도 Note에 명시했다.
- 하마터면/자칫, 좀처럼의 부정 결합, 왠지의 표기, 일일이의 일본어「いちいち」와의 문체 차이를 설명한다.

## 확인한 사전 근거

국립국어원 한국어기초사전에서 품사·활용·의미 구분을 직접 확인했다. 사전 예문/뜻풀이를 콘텐츠에 대량 복제하지 않았고, 본 예문/번역/Note는 자체 작성했다. 사전 등급을 앱 level이나 TOPIK 값에 전사하지 않았다.

- 들르다 (들러/들르니): https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=67876
- 서투르다 (형용사, 서툴러): https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=29043
- 무리하다 (여기서는 형용사 의미만): https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=15328
- 하나하나 (여기서는 부사 의미만): https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=84292
- 맞추다 (대상 비교/기준 조정): https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=74127
- 맞히다 (정답): https://krdict.korean.go.kr/kor/dicMarinerSearch/search?mainSearchWord=맞히다

처음 사용한 검색 경로 `/kor/dicSearch/search`는404를 반환해, 실제 검색 경로 `/kor/dicMarinerSearch/search`와 상세 페이지로 정정했다. 잘못된 응답을 사전 확인 성공으로 기록하지 않았다.

## Stable ID·검증·실패 처리

Content14 DB를 `Tests/Fixtures/content-v14-production.sqlite`에 byte 단위로 보존했다. SHA는 DATA-07 납품/기준 기록과 같은 `9293e75ee0161f8fa7688d6ea500f314c8d93fc3f6c9e0284bbf43afec622ac5`다. 이후 실제 직전 배포를 `--previous`로 지정해 후보를 검증했다.

새 UUID는uuid4로 한 번 발급해 `Content/data08-a-ids.json`과 원본에 저장했다. 본문/행 순서에서 ID를 재생성하지 않았다. 새 sort_key는 `힣:data08:a:NNNN`, learning_priority601이며 편집 순서일 뿐 공식 빈도가 아니다. 기존 세트 membership과 모든 기존 sort_key를 보존했다.

후보 strict Validator0errors/기존10warnings, 정규화 중복0, 기존 전체 payload/ID 보존을 확인하고 나서만 Source를 반영했다. 실제 Production Source를 다시 빌드해 승인 후보와 semantic signature가 같은지 확인한 후 Bundle DB를 교체했다. 검사 규칙/SQLite 제약을 완화하지 않았다.

| 발견/실패 | 진단과 처리 |
| --- | --- |
| 후보 assembler의 맞히다 참조 KeyError | 기존 표제어라고 가정한 초안 오류. 실제 DB에 없는 점을 확인하고 정답 의미의 신규 항목/2문장/Note로 검수 후 추가. Source 반영 전에 해결 |
| Grammar 예문 연결15개 초안 중1개가 기존6행을7행으로 증가 | 실제 repository의LIMIT6을 확인. 기존 예문 노출을 유지하려고 해당 연결만 제외. 새 어휘/예문 수는 줄이지 않고 최종14개 연결을 모두 실제 query로 확인 |
| 첫 portable232개 중19실패 | Content14 총수·버전·revision 승인 기대값이 원인. Content15의 정확한 총수와 이번23개 승인 개정을 추가. 이전 cohort/본문/ID 검사를 유지하고 assertion을 끄지 않음 |
| native 신규 테스트 초안의 품사 타입 가정 | Vocabulary.partOfSpeech는 일본어 표시용String임을 코드로 확인. 실제 모델의表示値와 raw POS 기대값을 함께 검사하도록 테스트 작성 단계에서 수정. native 실행 성공을 주장하지 않음 |

최종 `sh Tools/verify.sh --portable`: **243개 PASS** (기존232 + 신규11), 오류/실패/skip/expected failure0. 신규11개 별도 실행도PASS. integrity=ok, FK위반0. 원시 최종/초기/신규 테스트 로그와 Validator/DB build 보고서를 이 디렉터리에 보존했다.

## 통합 범위와 남은 gate

- 모든301카드/318meaning/602example/68Note를 실제 Swift repository에서 추출한SQL로 확인. 한국어 검색·일본어 보조 의미 검색·typed relation·문법 연결 조회를 검사했다.
- 初中級571개를 bounded keyset page로 조회하고 기존270개의 sort prefix를 보존했다.20개 세트 분할,5/10/20개 due 제한, enrollment 반복 시 due 덮어쓰기 방지를 검사했다. 세트/복습 크기를 늘리거나 새 학습 엔진을 만들지 않았다.
- Content14→15 교체 시 사용자DB byte 불변,4/20 부분 session, 기존 membership/순서·vocabulary/grammar/listening SRS·favorite·설정과 schema10을 디스크 재개로 확인했다. 기존 회귀군은 문법/듣기/직접입력 snapshot·통계·유지학습도 계속 검사한다.
- 실제 Swift의 들러요/서툴러요/어질러요/너그러워요/맞춰요/맞혀요 생성과 Production 카드 연결을 확인하는 XCTest1개를 작성했다. **native127개는 미실행**이다. Python으로 Swift 엔진을 복제해 검증하지 않았다.
- 앱 코드·UI·알림·광고·구매 설정은 변경0. 로컬DB 경로·짧은 세션·저장·Resume·선택적TTS와 기존 광고 경계를 유지한다. 실제3~10분 사용/iPhone offline·중단/VoiceOver/TTS/StoreKit은 미실행이다.
- 기존 retirement P1과 native 출시 gate는 해결하지 않았다. 初中級 전용 Grammar0/Listening2/Question5도 그대로다. 전체 DATA-08 목표까지 **신규 어휘499~899 / 신규 문장698~1,398**이 더 필요하다. 이번 Batch A의 완료가 DATA-08 전체나 앱 출시 완료를 뜻하지 않는다.
