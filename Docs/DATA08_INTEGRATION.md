# DATA-08-6 Production 통합 검증

2026-10-19 UTC. 시작 `main`/`origin/main`=`556042b5946b3439bb8f4b01ee375cea2a6a8047`, tracked/untracked 변경 없음. 작업 branch `data08-6/production-integration`. cloud-environment-onboarding:setup 절차로 기존 체크아웃·Python 표준 라이브러리·portable 실행 환경을 재사용했다. 추가 설치/서비스/환경 draft 변경은 필요 없었다.

## 반영 결과와 실제 수량

**Content19 / Schema4 / minReader7 / UserProgress10**. DATA-08 신규 어휘911(일반807/표현104), 고유 신규 예문1,821로 목표800~1,200 / 1,300~2,000 달성을 유지한다. 이번 단계 신규 Vocabulary/Meaning/Example/Note/Grammar 본문은0이다. 연습 문항·관계를 별도 추가했으며 이를 어휘나 예문 증가로 세지 않았다.

| 항목 | Content18 → 19 | 初中級 현재 |
| --- | ---: | ---: |
| Vocabulary | 2,287 → 2,287 | 1,181 |
| Meaning | 2,420 → 2,420 | 1,246 |
| Example | 4,597 → 4,597 (문장4,584 + 발음13) | 2,361 |
| Grammar | 42 → 42 | 0 |
| Listening | 115 → 1,936 | 1,823 |
| Question | 354 → 3,337 | 2,988 |
| Course / Lesson | 4 / 38 → 5 / 85 | 1 / 47 |
| content_items | 10,573 → 15,428 | 새 엔티티4,855 |

의미 Level 수량의 원본 집계는 COUNTS와 DB를 기준으로 한다. 어휘 入門306 / 初級800 / 初中級1,181, 문장646 /1,577 /2,361. Question hangul59 / intro156 / beginner134 / lower_intermediate2,988. Listening34 /79 /1,823. 기존 발음13은 intro Example659에 포함되지만 신규 문장에는 포함하지 않는다.

## 실제 배치와 기능 경로

- **Level lower_intermediate → Course「初中級・会話と現代生活」→ Unit A/B/C → Lesson47개 → 기존 20어휘 Set 회독**. Course/lessons/lesson_items를 Production Source에 실제 추가했다. Unit은 현 schema에 별도 테이블이 없어 `curriculum_unit` tag3개 + 레슨의 명시적 Unit 제목으로 배치했다. 새 엔진/가짜 Unit row나 강제 사용자 세트를 만들지 않았다. A16레슨/301어휘, B15/300, C16/310, 각 레슨≤20. 모든911어휘가 정확히 한 신규 레슨에 있고 카드/뜻/예문/Note를 기존 card reader로 읽는다.
- 기존 범용 레슨 runner의 미지원 vocabulary case를 기존 explanation 화면과 공통 카드 로더에 연결했다. `vocabulary_preview` 노출 이벤트는 `.viewed`이며 회독/SRS 완료·숙련으로 올리지 않는다. lesson cursor/판정 저장은 기존 transaction 경로를 사용한다.
- Set은 UserProgress의 기존 `VocabularySetCatalog.createNext`가 level/sort_key/ID 페이지와 이미 할당된 ID를 읽고 할당한다. 전1,181개를 실제 SQL로 할당하면20개×59 +1개=60세트,911신규어휘 모두 도달하며 기존 첫20 ID/순서와 UNIQUE 중복 방지를 확인했다. 실제 이용자의 세트 UUID·분할·순서는 기존 할당 이력에 따르므로 고정 세트 번호를 콘텐츠 ID로 만들지 않는다. 전911의 SRS enrollment를2회 적용해 중복0, 기존 stage4/due900 보존을 확인했다.
- **Listening/Dictation**: 검수된 고유 Example1,821개를 같은 ID로 재사용해 listening1,821/question1,821을 연결했다. 기존 learning_order를 유지하고220부터 추가해 기존 마지막 batch를 확장하지 않았다. 새92개 batch + 기존1개 = 初中級93 batch,30 batch씩4페이지, 문항≤20. transcript 복제0/선택지 생성0, 정답은 원문 그대로, 입력 전 prompt_ko=null. TTS word_sentence 정책을 사용하며 녹음 인증으로 표시하지 않는다. 독립 듣기 목록에 初中級을 노출했다.
- **Conjugation/Sentence Production**: 동사436+형용사145=581개에 각2문항(語幹+-고 581 / 기존 예문 전체 재현581)을 연결했다. -고는 기존 Grammar ID를 prerequisite로 재사용한다. 어간에고를 붙이는 형식이며 불규칙 어간 교체를 새로 추측하지 않는다. 문장 입력의 accepted/일본어는 기존 검수 예문과 일치하고, 문장 전체 재현과 -고 활용 확인을 설명에서 구분했다. 공통 입력 안내도 문제의 지시를 따르도록 수정했다. 명사·부사·표현330개를 활용 대상으로 오분류하지 않고 카드/레슨/듣기/사전 경로에 유지한다. 새 문법 본문이나 모든 문장에 -고가 쓰였다는 주장은 하지 않는다.
- **Grammar/Search/Dictionary**: 기존46개 DATA08 grammar_examples 연결이 실제 LIMIT6 조회에 남아 있고, 전911개는 현재 표제어 검색·상세·예문 조회에서 발견된다. 실마리가 보이다는 수정된 같은 ID다. 검색30·production30·curriculum200·session20 등 기존 페이지 상한을 유지했다.
- **진단 난도 회귀 수정**: 확장된 전 Level production pool의 첫 UUID를 쓰면 진단에 初中級 문항이 섞일 수 있었다. 진단은 기존 入門 문항을 level-filtered query로 고르게 수정했다. 시작 위치 변경은 진도/완료를 재작성하지 않는다.

## ID·Importer·DB 검사

직전 Content18 DB와 source byte를 `Tests/Fixtures/content-v18-production.sqlite` / `content-v18-production.json.gz`에 보존했다. 이전14~17 fixture, A/B/C 색인·한일 감사·43필드 교정 기록은 그대로다. DATA08-5 회귀군은 원본18 fixture에서 엄격한17→18 교정을 재현하고, 새 통합군은18→19의 전체 델타를 검사한다.

- strict `--production --previous content-v18-production.sqlite` **오류0 / 기존 경고10**. 처음 후보는 지원하지 않는 relation명 `example` 때문에2,402오류로 거부되었다. Validator를 바꾸지 않고 기존 허용 관계 `related`로 수정한 후보만 승격했다.
-25개 source table **63,159행** 모두 필드/PK/FK/ID/참조 대조, candidate 재빌드와 번들 모든 SQL 행 일치, `integrity_check=ok` / FK0. 전체 DATA08 구조·중복 lint 오류0. 구조 감사의 row-field 경고5와 strict 총경고10(기존 짧은 발음예시5/동형어5)을 구분한다.
- 기존10,573 ID/kind/created_at/sort_key/learning_order와 모든 기존 상세행·관계·lesson membership을 그대로 보존했다. 삭제·retire·retype0. 새 관계에 참여한 **2,733 ID**만 revision+1/updated_at(어휘911+예문1,821+기존 -고 Grammar1). 정확한 allowlist와 양 끝점 fingerprint를 대조했다. 새로운 UUID4,855개는 한 번 발급해 source/registry에 저장했으며 runtime에서 재생성하지 않는다.
- source SHA `f97b3bd70d07a3945770b8d6940c4a53e29a9b70b565caf21fb927230c08b4a8`; bundle SHA `57aeaf918d5eaaec3bbfaed02f87c5452cca8264540b923a70448b781adbe9e5`. 직전18 DB SHA `3235c21699bb297a4447f0ce2068a2e949db136a2c4e08ca70d7a737a07308e3`. 전체 테이블/Level/델타/해시는 [COUNTS](DATA08_INTEGRATION_COUNTS.json), ID 배치는 `Content/data08-integration-ids.json`이 기준이다.

## 사용자 기록·즉시 저장·오프라인 검사

분리된 on-disk UserProgress10에 기존 어휘20개·부분4/20 및 순서/round/revision, SRS20개, Favorites, Difficult predicate, item_progress, study_events/daily_statistics, opaque metadata/시작위치, 어휘·문법·production·listening·review·lesson active session을 넣고18→19 Content 파일만 교체했다. 교체 직후 사용자 DB SHA와 모든 테이블/행/opaque JSON snapshot이 동일하며 저장된 ID를 새 Content에서 해석할 수 있음을 확인했다. 통계·Difficult 조회도 동일, Continue SQL은 최근순 lesson→review→listening→production→grammar→vocabulary를 유지했다.5/10/20 due queue도 확인했다.

실제 Settings는 UserProgress의 예제 metadata가 아니라 `Services/LearningPreferences.swift`의 UserDefaults `learning.preferences.v1`에 저장된다. 해당 저장소/키/Schema는 변경하지 않았고, native 설정 테스트에 Content19 코스/레슨을 연 뒤 기존 preferences Data/amount/시간을 그대로 읽는 검사를 보강했다. 이 UserDefaults/알림 검사는 미실행이며 Python metadata 보존 검사를 실제 설정 실행으로 표시하지 않는다.

새 어휘 레슨의 실제 repository SQL로 session 시작→`.viewed` 판정 commit→연결 종료/재오픈을 수행해 판정/현재 cursor를 확인했다. 뒤늦은 중복 결과 쓰기 실패는 앞선 event까지 transaction rollback되고 기존 첫 답은 남았다. 기존 회귀군의 stale/중복/재시도·완료/부분완료·엔진 기대형 검사를 유지했다. 이는 Python이 Swift Codable/상태전이를 실행했다는 뜻이 아니다.

Python socket 생성을 금지한 과정에서 Home/Resume·검색·SRS·카드·세션 SQL은 로컬 DB로 실행됐다. 저장소/학습 경로에 로그인·서버·광고/구매 의존성을 추가하지 않았다. 실제 iOS 비행기 모드·미설치 한국어 TTS voice·통화/백그라운드/강제 종료·VoiceOver는 미실행이다. 세션2문항/레슨≤20/회독20/복습5·10·20과 판정마다 commit을 유지하되, 실제3~10분 소요를 보장하거나 측정했다고 기록하지 않는다.

## 실행 결과·성능

- 전용 통합 **11 PASS**(18.993초, failures/errors/skipped0, exit0). 첫 실행은10 PASS/1 ERROR(테스트 seed의 lesson_progress 컬럼 수 오류)였고 명시적 컬럼 repository SQL로 고쳤다. 초기 로그를 별도 보존했다.
- 전체 `sh Tools/verify.sh --portable`: **291 PASS**, 289.839초, failures/errors/skipped0, exit0. production monetization 설정 검사 포함. 최종 전체 suite 실패0. 첫 전체 실행은291개 중289 PASS/2 FAIL(기존4코스 목록 기대값과 첫30개만 읽는 retirement 테스트의 페이지 가정)였으며, 정확한5코스 순서와612→611 전체 페이지/비활성 제외로 검사했다. 초기 전체 로그도 보존했다. 최신 전용11개에는 전911 SRS 보존 assertion과 실제 Settings/UserDefaults·예제 metadata의 구분을 반영해 재실행했다.
- native XCTest 정의 **132개 / 실행0**. 새2개는 실제47레슨/911카드와1823 listening 전체 페이지/정답을 검사하도록 작성했다. 기존 native production 검사도612어휘 pool을 끝까지 읽도록 유지했고 진단 入門 필터 assertion을 보강했다. Swift/Xcode/iOS SDK가 없어 type-check/build/XCTest는 실행하지 못했다.

아래는 Linux sqlite3, warm connection, 각30회, 별도 사용자DB(SRS2,287행)에서 실행한 **SQL/디스크 commit** 시간이다. 같은 환경에서18/19를 비교했으며 공유 클라우드 부하·캐시 영향을 포함한다. 소규모 표본이며 앱 실행/렌더/활용 계산 시간이나 iPhone 성능 기준 통과를 뜻하지 않는다.

| 검사 | 이전 median ms | 현재 median ms | 현재 p95 ms |
| --- | ---: | ---: | ---: |
| Home refresh/Resume SQL | 3.546 | 3.682 | 5.541 |
| 한국어 검색 | 0.746 | 0.584 | 0.874 |
| 일본어 검색 | 0.694 | 0.657 | 0.792 |
| 넓은 검색 30행 | 5.010 | 5.144 | 5.333 |
| SRS20 + 카드 header | 1.160 | 0.613 | 0.759 |
| 20개 세트·session commit SQL | 0.997 | 0.978 | 1.146 |

번들11,685,888→17,932,288 bytes. 새 레슨20 SQL median0.125ms/p950.158ms, 初中級 어휘 첫20 SQL median0.655ms/p950.747ms. 수치는 [PERFORMANCE](DATA08_INTEGRATION_PERFORMANCE.json)에 원시 분포 요약과 재현 환경으로 남겼다.

재현 명령(루트):

```sh
python3 Tools/ContentBuilder/build_content.py Content/production.json /tmp/data08-candidate.sqlite --production --previous Tests/Fixtures/content-v18-production.sqlite --report /tmp/data08-build.json
python3 Tools/ContentBuilder/audit_data08_final.py Content/production.json --database Resources/content.sqlite --report /tmp/data08-structure.json
python3 -m unittest discover -s Tools/ContentBuilder -p test_data08_integration.py -v
python3 Tools/ContentBuilder/benchmark_data08_integration.py --report /tmp/data08-performance.json
sh Tools/verify.sh --portable
```

## 남은 gate·Git

**B—Conditional 유지**. 사람·독립 원어민/교사 검수 미실행, DATA08-5의163개 선행 문형 후보/Level·Register 적합성 의심은 해결했다고 표시하지 않는다. 初中級 독립 Grammar0/상위 Level 공백, 기존 retirement active-review P1도 유지한다. 듣기·문제 공백은 이번 실제 배치 수량으로 갱신했다. native Debug/Release/SDK·iPhone3~10분/한 손·즉시 중단 재개·오프라인/TTS/VoiceOver·광고/StoreKit/알림 gate는 Mac/iPhone에서 별도 실행해야 한다. 이번 결과는 DB/Source 통합과 실행된 portable 범위의 검증이며 출시 승인이 아니다.

사용자의 기존 명시적 커밋·푸시·PR·머지 위임에 따라 검증된 변경을 전달한다. 최종 commit/PR/merge SHA와 clean main 일치는 Git/PR이 기준이다. DATA-08-6에서 종료하며 후속 단계는 시작하지 않는다.
