# DATA-08-4 / Batch C 개별 검수와 목표 달성

Runtime 원본은 `Content/production.json` → 기존 ContentBuilder → `Resources/content.sqlite`다. DATA-08 전체 수량 목표와 이번 Batch C를 완료하며 이후 콘텐츠 Batch나 앱 기능 변경은 수행하지 않는다.

## 실제 기준과 전체 수량

시작 main/origin/main=`e7ed775342e261716aa1f7a4afd3eabd965fde78`, tracked/untracked 변경0. 상태·제작·누적·출시 문서와 DATA08_PROGRESS §10~11을 읽고, Content16 DB에서 A301/602·B300/600의 모든 ID와 실제 행을 확인했다. 당시 Vocabulary1,977 / Example3,978(문장3,965) / Grammar42 / Listening115 / Question354였다. 初中級 Grammar0/Listening2/Question5·상위레벨 공백·retirement P1·native gate도 재확인했다.

| Batch | DB Vocabulary 신규 | 일반 어휘 | Phrase | 신규 문장 Example |
| --- | ---: | ---: | ---: | ---: |
| A | 301 | 261 | 40 | 602 |
| B | 300 | 266 | 34 | 600 |
| C | **310** | **280** | **30** | **619** |
| 합계 | **911** | **807** | **104** | **1,821** |

**전체 목표 Vocabulary800~1,200 / 신규 Example1,300~2,000 달성, 부족0/0.** Phrase를 제외한 일반 어휘만도807개다. 기본 가이드에 맞춰 이번 C 일반어휘280+회화표현30, 예문620개를 계획했고, 기존과 같은 문장1개는 기존 ID를 재사용해 실제 신규는619개다. 재사용·관계·Grammar·fixture·고유명사·활용형·미검수 후보를 신규 수량으로 합산하지 않았다. 목표를 줄이거나 새 문장을 보충할 필요가 없다.

C 품사: 동사138 / 형용사45 / 부사44 / 명사53 / expression30. 명사17.10%. 전310항목 Collocation·Register, 의미334(24항목 두 의미/용법), 일본인 Note146. 어휘 관계84 / 기존 Grammar 예문 참조17 / Vocabulary-Example 새 관계620(신규619+재사용1). 신규 Grammar0 / Listening0 / Question0.

Phrase는 기존 schema의 `vocabulary.part_of_speech=expression`으로 제공하고 색인 `lexical_category=phrase`로 분리한다. 일반 어휘는 `lexical_category=vocabulary`, 문법은 기존 grammar 테이블과 그 ID를 유지한다. 회화 표현을 새 Grammar로 세거나 schema를 확장하지 않았다. 복합 명사 `개인 정보`/`이용 약관`은 일상 디지털 용어이며 관용 Phrase와 구분한다.

## 묶음별 Self Review·Duplicate Audit·관계 검사

| 묶음 | 영역 | 일반/표현 | 신규 문장/재사용 | 의미/Note | strict 결과 |
| --- | --- | --- | --- | --- | --- |
| C1 | 현대 생활·디지털·미디어 | 90/10 | 199/1 | 105/42 | 오류0/기존경고10 |
| C2 | 직장·계획·협업 | 90/10 | 200/0 | 102/45 | 오류0/기존경고10 |
| C3 | 사회·추상어·일상 회화 | 100/10 | 220/0 | 127/59 | 오류0/기존경고10 |

검수자는 작성자와 같은 **assistant**다. 전310개 표제어·기본형·품사·활용 metadata·뜻·Collocation·Register, 620문장 쌍(신규619/재사용1), 146 Note를 작성 후 별도 재독했다. 독립 원어민/교육 전문가 승인이나 무오류 인증은 아니다. Validator도 자연스러움을 인증하지 않는다.

각 묶음에서 먼저 기존전체/A/B/앞 묶음과 후보 표제어를 비교하고, 양쪽 언어를 개별 재독한 뒤 관계·UUID·무결성·strict 이전 배포 gate를 실행했다. 실제 카드·뜻·Note·관련어·문법 SQL도 조회했다. 단계별 SHA/누적수는 `DATA08_C1~C3_AUDIT.json`, Validator 원시 보고서는 `DATA08_C1~C3_VALIDATION.json`에 보존한다.

- 한국어: 조사, 주어·목적어, 동사 방향, 시제·높임말·띄어쓰기·추상/비유 용법과 실제 상황을 확인했다. 시간·상황·문장 길이를 섞고 같은 틀의 기계적 단어 치환으로 수량을 채우지 않았다.
- 일본어: 의미 범위·능동/수동·시제·문체·정중함·감정 강도를 대조했다. 해요체는 丁寧体, 조치하다/모쪼록/삼가다의 공식 안내 예문은 해당 문체로 번역했다.
- 난이도: 기본 연결·이유·대조·조건·계획·과거·전후·부탁·허용·가능·금지·추측 문형을 중심으로 初中級에 편집 배정했다. 복잡한 중첩·불필요한 새 숙어는 줄였다. 공식 TOPIK 판정이나 모든 문장의 형태소별 선행 학습 그래프를 증명한 것은 아니다. 공식 등급/빈도/확인되지 않은 읽기·녹음 metadata는 null이다.
- 중복: NFC·casefold·공백 제거 기준 표제어·한국어/일본어 문장·한일 쌍을 대조했다. 같은 뜻의 다른 한국어 단어가 같은 일본어 번역을 갖는 것은 동의/유사어 관계로 검토하며 자동 삭제하지 않는다. 한 어휘 내부의 정규화 의미·ordinal·예문 대응도 검사했다.
- 관용 Phrase는 완결된 의미 단위로 다루고, 조사 결합·임의 활용형·명사+이다를 새 단어로 늘리지 않았다. 기본 후보 중 이미 존재하던 미묘하다와 잘못 분리된 원시 조각은 승인하지 않았다. 고유명사/희귀 전문어 항목0, 기존 초급 표제어를 level만 바꿔 재등록한 항목0이다.

전문/기기별 음성 검수는 미실행이다. 전 항목은 [카탈로그](DATA08_C_REVIEW_CATALOG.md), 검수 payload SHA는 [EDITORIAL.json](DATA08_C_EDITORIAL.json)에 있다.

## 의미·품사·문체 교정

- 로그인/로그아웃은 사전의 명사 기본형으로 제공하고 하다 결합은 예문에서 학습한다. 각각의 명사/하다형을 별도 수량으로 중복 생성하지 않았다. 로그인·가입·탈퇴의 동작 범위도 Note로 분리했다.
- `개인 정보`/`이용 약관`의 띄어쓰기를 통일했다. 부사처럼 보였던 전적으로 후보는 이왕으로 교체했고, 시간 뜻의 한참은 명사로 정정했다. 고작/각기/유독은 이번에 쓰는 부사 뜻을 명시하고 다른 동형 뜻과 구분했다.
- 설치하다(설치/소프트웨어 인스톨), 구독하다(정기 구독/채널 등록), 투명하다(투명/운영에 숨김 없음), 곧장/곧바로(방향/시간), 연기하다(延期/演技), 나란히(공간/나란한 성과), 비추다/비치다, 거북하다, 덜컥, 소박하다 등24항목의 의미/용법을 각 Meaning ID와 예문에 연결했다. 동형 용법을 나눈 경우 같은 어원이라고 주장하지 않는다.
- 노출되다/공개되다, 복구하다/회복하다, 접하다/접속하다, 보안/보완, 출처/근거, 이용료/수수료, 권리/권한, 결재/결제, 채택/채용, 보류/연기, 사직/퇴사/해고, 주관/주도, 상의/상담, 과도/과중, 부실/미흡, 찬찬히/천천히, 고작/겨우/가까스로의 차이를 설명했다.
- 사직하다/퇴사하다의 어색한 목적어 초안, 수립하다의 과도한 일본어 직역, 분산되다의 결합, 마음가짐의 결합과 지탱하다의 중첩 문장을 고쳤다. 간혹의 늦게 열기/늦게까지 열기의 번역 차이, 소박하다/한껏/덜컥 등의 일본어도 다듬었다. 세부 전후 값은 `DATA08_C_CORRECTIONS.json`에 보존한다.
- 삼가다는 삼가요(삼가해요 아님), 껄끄럽다/달갑다/미덥다는ㅂ불규칙. 하다형은 other, 그 외 규칙/으탈락 등은 기존 엔진 계약의 none으로 분류한다. predicate/expression has_batchim=null, expression irregular_type=null이다.
- 격식 차이는 전310항목의 `meanings.nuance_ja`에 기록했다. 무능하다·입을 다물다·고작의 직접 평가/명령, 거부하다·손을 떼다의 강한 어조, 모쪼록·삼가 주시기 바랍니다의 안내 문체는 Note에서 추가 설명했다.

## 실제 중복 재사용과 실패 처리

초기 Duplicate Audit가 `확인하지 않은 소문을 퍼뜨리지 마세요.`의 기존 Example `3fb4a617-a5ef-476b-9f40-0963a3ff9845`를 검출했다. 일본어도 기존 승인문과 같은 의미임을 확인해 기존 문장 쌍/ID를 그대로 재사용했다. 번역의 쉼표 차이로 새 문장을 만들지 않았다. 새 meaning에 연결한 기존 Example 끝점 revision+1을 승인했고 본문·created_at·level은 보존했다. 해당 문장은 신규619개에 포함하지 않는다.

관계 초안은 입력하다·삭제하다·퍼지다·충고하다가 DB에 있을 것으로 가정해 초기 assembler 검사에서 실패했다. 실제 부재를 확인하고 관계4개만 제외했다. 관계를 채우려고 어휘를 추가하지 않았다. 폐기한 관계/없는 끝점은 `DATA08_C_REJECTED_RELATIONS.json`에 기록했다. 최종84관계는 전부 실제 active ID에 연결된다.

초기 후보 오류/교정은 Production 반영 전에 해결했다. Validator나 assertion·FK·제약을 완화하지 않았다. UUID는 승인 전 후보 단계에서 한 번 발급해 저장하고 이후 교정/묶음 확장에서 보존했다.

## 사전 근거·저작 출처

한국어기초사전의 실제 조회로 명사/부사 구분, 동형어·활용을 대조했다. 검색 결과 부재를 단어 자체가 잘못됐다는 증명으로 쓰지 않고, 선택한 기본형의 긍정적 근거를 확인했다. URL/조회 결과는 `DATA08_C_DICTIONARY.json`에 있다.

- 로그인 명사52528 / 로그아웃 명사52530 / 한참 명사72463 / 이왕 부사73476 / 고작 부사18855 / 각기 부사16210 / 유독 부사72448.
- 달갑다 활용: https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=44078
- 미덥다 활용: https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=56245
- 껄끄럽다 활용: https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=39536
- 삼가다 활용: https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=16204
- 찬찬히(본 항목은 꼼꼼하고 차분한 뜻)78003, 지나치다(동사)27760. 부사/형용사의 모든 다른 뜻을 등록했다고 표시하지 않는다.

예문·일본어 번역·Note·Collocation은 자체 작성했다. 사전 예문을 학습 콘텐츠로 복제하지 않았다. 재사용1문장은 기존 출처/ID를 유지한다. 사전 등급이나 저작권/녹음 권한을 임의로 부여하지 않았다.

## 버전·Stable ID·기존 결과 보존

실제 직전 Content16 DB를 `Tests/Fixtures/content-v16-production.sqlite`에 byte 그대로 보존했다(SHA=`112d3662f79a72ca61ad7140a5d937396c0bc9f71180dd5f35a403a040a91f29`). 정확한 source16도 gzip으로 보존했고 복원 SHA=`dcf51d2583ddb7fa7bbbfb7487937546ef30551857d36fecaefc8c3c5ae7b30e`다. A/B 기존 색인·검수 보고서·v14/v15 fixture는 그대로다.

현재 **Content17 / Schema4 / minReader7 / UserProgress10**. 새 content_items1,412개는 UUID4(어휘310+뜻334+문장619+Note146+태그3), 출처1개는 sources에 별도로 기록한다. sort_key=`힣:data08:c:NNNN` / priority603은 편집 순서다. 기존 ID/kind/본문/created_at/정렬/learning_order/lesson membership 삭제·변경·비활성화0. 관계가 추가된 기존 끝점46개(어휘28/문법17/예문1)만 revision+1/updated_at을 갱신했다. 승인 목록=`Content/data08-c-revised-ids.json`.

strict `--previous content-v16-production.sqlite` 통과, integrity=ok/FK0. 기존 경고10은 발음용 짧은 문장5/동형어5로 유지했다. 승인 candidate와 Source 재빌드·Bundle의 SHA/semantic signature를 대조하고 모든 기존 JSON 상세 행과 관계를 보존했다. 문법 참조17개는 실제 LIMIT6에서 이전 예문과 함께 모두 보인다. 의미별 Example 참조는 기존 Listening/Sentence Production 구조에서 재사용 가능하며 신규 듣기/문항 수로 세지 않는다.

## 통합검사·미실행 gate

처음 상태에서 `sh Tools/verify.sh --portable` 기존255개 PASS를 확인했다. B의 정확한300/600 회귀군은 원본 source16 gzip/DB16 fixture에서 모든 기존 assertion을 유지해 재현한다. C는 현재 Bundle에서 A/B 포함 기존 전체 payload/ID와 실제16→17 교체를 검사한다.

C 신규14개는 strict build/수량·UUID/전역 중복/Meaning·Note·카드/검색·typed relation·문법 LIMIT6/활용 metadata/문체/카테고리·20개 세트·5/10/20 due·enrollment 중복 방지/A+B 어휘20개로 구성한4/20 부분session·UserProgress byte/SRS/favorite/설정/schema10 보존/깨진 후보 거부/기존 예문 재사용/세 묶음 gate/전체807+104 및1,821 목표를 확인한다. 최종 `sh Tools/verify.sh --portable`는269개 PASS(failures/errors/skipped0, exit0, 140.179초). 중단 전269PASS 이후 임시 로그가 사라져 재실행했고 `Docs/DATA08_C_TEST_LOG.txt`에 보존한다. 상세는 `DATA08_PROGRESS.md` §12를 따른다.

실제 Swift에서 삼가요·달가워요·미더워요·껄끄러워요·어설퍼요·가라앉아요·가라앉혀요·비춰요·비쳐요·가꿔요·들떠요와 카드 metadata를 확인하는 XCTest1개를 작성했다. 현재 native 정의129개 / 실행0. Swift/Xcode 없음; type-check·Debug/Release build·SDK link·XCTest·iPhone 3~10분/비행기모드·TTS·통화/kill·VoiceOver·광고/StoreKit·알림은 미실행이다.

앱 runtime·학습엔진·UserProgress schema·SRS·로컬 저장/Resume·세션 크기·광고/IAP 코드 변경0. 기존 offline-first·20개 세트·5/10/20 복습·광고 경계는 유지한다. retirement active-review P1, native 출시 gate와 初中級 Grammar0/Listening2/Question5·상위레벨 공백은 후속 별도 범위다. **수량 목표 달성은 앱 출시 승인이나 모든 콘텐츠 연계 부족 해소를 의미하지 않는다.** 이번 Batch C 이후 작업은 수행하지 않았다.
