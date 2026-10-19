> DEV-14 (2026-10-05): 현재 상태는 PROJECT_STATUS.md 및 Docs/DEV14_REQUIREMENTS_AUDIT.md가 기준입니다. 아래 이전 단계 기록의 완료 표현은 native 출시 검증을 의미하지 않습니다. Content13/Schema4/UserProgress10 유지.

# 아키텍처 — DEV-06

현재 Content schema 3/content 5/reader 4, UserProgress schema 5입니다. 아래 DEV-01~04/DATA-01 절은 각 단계의 결정을 보존한 설명이며 최신 장기복습 확장은 마지막 DEV-06 절을 참고하세요.

DEV-01의 SQLite + actor repository + SwiftUI 구조를 유지합니다. 한글 production 및 사용자 DB v3 세션 저장을 보존하고 콘텐츠 schema v3/content v4, 발음 페이지, 공통 음성 서비스를 추가했습니다. 이전 단계 기록은 `DEV-01_STATUS.md`에 보존했습니다.

## 런타임 의존 방향

SwiftUI Views → @MainActor AppModel → ContentRepository / ProgressRepository protocol → SQLite repository actor → SQLiteConnection

`AppContainer.open()`이 리소스·경로·의존성을 조립합니다. DB 연결은 소유 actor 안에 머물며 UI에 SQL이나 파일 핸들을 노출하지 않습니다. 앱은 시작할 때 metadata/첫 단어 50개/과정 메타데이터/사용자 요약을 조회합니다. JSON source나 15,000개 단어를 시작 시 전부 메모리에 올리지 않습니다.

## 저장 분리

| 대상 | 위치/권한 | 업데이트 |
| --- | --- | --- |
| 콘텐츠 | 앱 번들 content.sqlite / read-only | 앱 배포 시 완성된 파일로 교체 |
| 사용자 | Application Support/HangulStudy / writable SQLite | 별도 순차 migration, 기존 기록 보존 |
| 콘텐츠 source | 개발 프로젝트의 JSON/JSONL | 앱에 포함하거나 런타임 파싱하지 않음 |
| synthetic | 도구 실행 시 지정한 개발 디렉터리 | 앱 번들 포함 금지 |

Debug/Release 모두 production content.sqlite를 사용합니다. Debug 사용자 파일은 user-production-development.sqlite, Release는 기존 user.sqlite입니다. 기존 Debug fixture 파일 user-development.sqlite는 삭제하지 않고 그대로 두며, 서로 다른 dataset의 기록을 섞지 않습니다. 작은 content-fixture.sqlite는 XCTest 번들에만 포함합니다. 성능 검증용 15,000/30,000 DB는 어느 앱 설정에도 포함하지 않습니다.

사용자 DB는 WAL + synchronous FULL, Application Support 디렉터리 데이터 보호를 사용합니다. 정상 앱 업데이트/재실행 시 유지되지만 앱 삭제·기기 분실까지 보장하는 별도 백업/클라우드 동기화 기능은 아닙니다. 기존 사용자 DB의 v1/v2→v3 migration 이전에는 SQLite backup API로 WAL을 포함한 일관된 스냅샷을 만듭니다. 오류나 미래 버전 발견 시 DB를 삭제/초기화하지 않습니다.

## 콘텐츠 스키마 v3

정확한 SQL: `Content/content-schema-v3.sql`. 모든 필드·필수/선택·FK·enum은 `CONTENT_GUIDE.md`에 수록했습니다.

- content_items: 전역 영구 UUID, kind, revision, active/tombstone, 9단계 level, 선택 difficulty, 생성/수정 시각
- vocabulary / meanings: 표제어·발음·품사, 받침/불규칙/편집 우선순위, 출처가 필요한 선택 TOPIK/빈도 메타데이터, 다의어/뉘앙스/사용 설명
- examples / vocabulary_examples / grammar_examples: 독립 예문, 일본어 번역, 학습 포인트, 여러 의미/문법에 연결
- grammar: 문법 패턴, 의미·형태·사용 조건·혼동 포인트
- hangul / pronunciation_rules / pronunciation_examples: 자모/받침, 발음 규칙, 표기→실제 발음과 예문
- conjugations: 기본 동사/형용사와 활용형/규칙/불규칙/말높임/설명
- media_assets / listening_items: 경로/해시/권리/길이, 대본과 일본어 설명
- questions / question_choices: 6가지 문제 유형, 번역 방향, JSON 정답 계약 버전, 선택지/듣기/TOPIK 급수
- courses / lessons / lesson_items: 과정-레슨-학습 콘텐츠
- tags / item_tags / learner_notes / content_links / content_aliases: 태그, 일본인 설명, 명시적 관계 및 폐기 ID 이력
- sources / item_sources: 확인 가능한 출처와 콘텐츠 연결
- vocabulary_search: importer가 만드는 정규화된 검색 term→어휘의 파생 테이블. source에서 입력 불가

## 조회와 대용량

단어는 `(sort_key,id)` keyset pagination을 유지합니다. 기본 50개, 최대 100개입니다. `VocabularyQuery`는 level과 prefix를 선택적으로 조합합니다. prefix는 표제어/발음/각 일본어 의미의 NFC·trim·소문자 정규화 후 시작 부분 일치입니다. FTS/형태소/퍼지/임의 부분문자열 검색은 아닙니다. 이 API는 아직 UI 검색창에 연결하지 않았습니다.

콘텐츠는 level/kind/active, 어휘 정렬, 검색 term, 예문 관계의 양방향 인덱스를 갖습니다. 빌더가 ANALYZE를 수행합니다. 현재 level·검색 쿼리는 조건에 따라 작은 정렬용 임시 B-tree를 사용합니다. 실측을 기록했으며 무조건 상수 시간이라고 주장하지 않습니다.

예문은 단어별 최대 100개까지 조회합니다. 과정/레슨 메타데이터는 일괄 조회합니다. 향후 레슨이 수만 개 또는 단어당 예문이 100개를 넘어가는 사용 시 저장 구조를 바꾸지 않고 해당 API만 페이지화할 수 있습니다.

## Importer / Validator

`source_reader.py`는 JSON 또는 sharded JSONL을 읽습니다. JSONL은 행 단위 스트리밍이고 전체 corpus를 Python 객체 배열로 로드하지 않습니다. Validator의 일부 전역 검사(중복 표제어, ID/관계 fingerprint)는 항목 수에 비례하는 메모리를 사용합니다. 앱 메모리 사용과 혼동하지 않습니다.

`build_content.py`는 같은 디렉터리 임시 SQLite에 바인딩된 INSERT를 수행합니다. 테이블/컬럼은 whitelist와 SQL 스키마로 검증합니다. 행 오류가 있으면 보고서에 위치를 기록하되 **부분 DB를 성공 결과로 배포하지 않습니다**. 전체 관계/기본 의미/고아 예문/문제 답 구조/미디어 해시/이전 배포 정책 검사를 통과해야 commit·검색 인덱스·ANALYZE·integrity_check 후 원자적으로 결과를 교체합니다.

오류와 경고는 별개입니다. 동형 표제어 후보·한 글자 예문·비-NFC는 검수 경고입니다. 경고 때문에 자동 삭제하지 않습니다. 언어학적 자연스러움, 진짜 출처의 신뢰도, 교육적 정확성은 별도 검수 대상입니다.

## 영구 ID와 버전

실제 source에 한 번 발급해 저장한 UUID를 계속 사용합니다. rowid/정렬 위치는 진도 ID가 아닙니다. 업데이트는 전체 스냅샷 + 이전 배포 DB 비교이며 tombstone을 보존합니다. 기존 ID 삭제/kind 재사용/created_at 변경/revision 하락을 거부합니다. 상세 행뿐 아니라 관계 끝점 fingerprint를 비교하여 바뀐 콘텐츠의 revision 증가를 요구합니다.

schema_version(구조), content_version(dataset 배포), revision(항목), min_reader_version(앱 계약)은 별개입니다. DEV-01 source는 명시적 migration 도구로 ID를 유지하며 v2 source로 변환했습니다. 앱은 v2/v3 콘텐츠를 열고, 구형 v1 파일은 회귀 검증용으로 보존했습니다. 원격 패키지 다운로드/서명/활성 포인터 전환은 구현하지 않았습니다.

미래 런타임 업데이트는 staging 수신→서명·해시·버전·참조 검증→새 read-only 연결 준비→활성 포인터 원자 교체→이전 패키지 보유 방식으로 확장합니다. 열려 있는 SQLite 파일을 덮어쓰지 않습니다.

## 사용자 스키마 v3

v1 생성 SQL과 v2 migration을 보존하고 `Resources/user-migration-v3.sql`까지 순차 적용합니다. 기존 DB는 먼저 SQLite backup API로 원본 버전 스냅샷을 남긴 후 각 migration을 트랜잭션으로 적용합니다. 새 DB는 v1→v2→v3으로 이동합니다.

- item_progress: 최초/최종 학습일, 학습/정오답/회독 수, acquisition_status, perceived_difficulty
- acquisition_status: unassessed / learning / acquired / maintaining. 기본 unassessed이며 과거 횟수만으로 습득 완료를 추정하지 않음
- perceived_difficulty: null 또는 1~5. 콘텐츠의 편집상 difficulty와 별개
- study_events: 당시 콘텐츠 revision/version, UTC 시각, 당시 날짜/시간대, 결과/스킬/소요시간/세션
- srs_state: 콘텐츠×스킬, 알고리즘/버전/JSON 상태, due_at, 최근 복습일
- favorites, learning_passes, pass_items, lesson_progress, daily_statistics, user_metadata는 유지

콘텐츠 DB로 향하는 FK/cascade delete가 없습니다. 콘텐츠가 교체/비활성화돼도 해당 UUID의 사용자 기록은 남습니다. dataset_id는 실수로 다른 corpus와 진도를 섞는 것을 막습니다.

기존 record()는 UUID 멱등성과 이벤트/항목/일별 통계 단일 트랜잭션을 유지합니다. 새 습득/체감 난이도 컬럼은 저장 기반만 추가했고 평가 UI·회독·SRS 알고리즘을 선행 구현하지 않았습니다. 실제 사용자 기록의 alias 병합도 하지 않습니다.

## 제한

Xcode/Swift 컴파일러 없는 Linux에서 작업했습니다. Python/SQLite 및 Swift 구문 검증과 네이티브 빌드 검증은 다릅니다. 현재 결과는 `VALIDATION.md`, 대용량 실측은 `PERFORMANCE.json`, 다음 개발 인계는 `PROJECT_STATUS.md`를 확인합니다.


## DEV-03 학습 세션

Views → @MainActor LessonViewModel → 기존 Content/ProgressRepository → 각 SQLite actor 경계를 유지합니다. content 쿼리는 한 레슨만 최대 200단계 조회합니다. 전체 학습 자료를 시작 시 로드하지 않습니다.

`lesson_sessions`는 시도 UUID, 영구 lesson ID, content version, 순서 섞기 seed, 시작 당시 step ID 목록, 현재 step ID, 상태/시각을 저장합니다. 레슨별 active 세션은 하나입니다. `lesson_step_results`는 (session ID, content ID)마다 한 번만 답안/정오답/event ID를 저장합니다. `lesson_progress.completed_count`는 완료한 시도 횟수입니다. 기존 item_progress/study_events/daily_statistics는 실제 학습 동작에 계속 사용합니다.

답안 확정 트랜잭션은 event + 항목/일별 집계 + step result를 함께 기록합니다. 피드백 확인 전에는 cursor를 이동하지 않습니다. Next는 현재 답안이 있는지 확인하고 cursor 또는 완료 상태/완료 횟수를 트랜잭션으로 갱신합니다. 설명 페이지는 viewed를 먼저 저장한 뒤 cursor를 진행합니다. 두 동작 사이 종료되면 같은 페이지가 다시 보일 수 있으나, 중복 집계 없이 Next로 진행합니다. 완료 처리도 중복 호출에 안전합니다.

새 시도는 새 UUID/seed를 발급하며 예전 결과와 완료 횟수를 지우지 않습니다. content version 또는 step 목록이 달라지면 자동으로 틀린 위치에 연결하지 않고 재시작 안내를 냅니다. 사용자 요청으로 새 시도를 시작하면 이전 세션은 abandoned로 보존됩니다. 현재는 무관한 콘텐츠 추가로 content version이 증가해도 진행 중 레슨을 다시 시작하도록 하는 보수적 정책입니다. 향후 revision-aware 재개 정책을 도입할 수 있습니다.

제출 전 선택지 선택은 임시 UI 상태입니다. `答える`로 확정한 답안과 방문 위치만 저장합니다. 실제 집중 시간을 측정하지 않으므로 duration_ms=0이며, 학습 시간으로 표시하지 않습니다. 완료는 레슨을 끝까지 확인했다는 뜻이지 SRS 습득 판정이 아닙니다.

`QuizOptions`는 세션 seed와 영구 question ID에서 FNV-1a/SplitMix64 기반으로 순서를 재현합니다. `HangulComposition`은 유니코드 현대 한글 음절을 초성/중성/종성으로 분해하여 조합식을 보여줍니다. `UnavailableHangulAudio`는 검증된 음원 URL이 없음을 반환합니다. DEV-04 공통 음성 서비스와 별개로 기존 한글 과정의 개별 자모 TTS 금지 정책을 유지합니다.


## DEV-04 발음·음성 확장

콘텐츠 v3 스키마는 기존 표를 유지하고 pronunciation_presentations / content_audio / audio_questions를 추가합니다. 원래 철자, 복수 교육용 발음 표기, 문맥, 음성 용도를 분리합니다. SQLiteContentRepository는 기존 lessonSteps에 pronunciation을 추가하고 규칙 단건/연결 예시를 필요할 때 조회합니다. schema 2에는 새 테이블을 조회하지 않습니다.

앱이 @StateObject로 소유한 @MainActor KoreanAudioService 하나를 environmentObject로 주입합니다. UI → LearningAudioPlaying → 주입 가능한 AudioPlaybackBackend 및 RecordingResolving 구조입니다. SystemAudioBackend는 AVSpeechSynthesizer/AVAudioPlayer를 소유합니다. ko-KR 음성이 없거나 녹음/해시가 잘못되면 안전한 안내를 내고 재생하지 않습니다. 단어 TTS는 표기를 읽고, 자모/대립 비교는 녹음 전용입니다.

재생 요청 UUID 및 실제 플레이어/utterance identity로 이전 비동기 callback을 무시합니다. 화면 이동·닫기·백그라운드·중단·이어폰 분리 시 정지합니다. 듣기 문항은 성공한 재생 완료 뒤에만 제출 가능하고, 이미 저장된 답안 피드백은 재청취 없이 이어갈 수 있습니다. 사용자의 듣기 완료는 이번 페이지의 UI 상태이며 학습 성취 점수로 별도 저장하지 않습니다.

진도는 기존 schema 3 세션/결과 트랜잭션을 그대로 사용합니다. skill=pronunciation, 새 UUID만 추가하고 사용자 스키마/파일을 교체하지 않습니다. content 3 진행 중 세션은 기존 보수적 버전 정책에 따라 재시작 안내가 나오며 예전 답안·완료 횟수는 보존됩니다. 코스 간 강제 잠금은 없습니다.


## DATA-01 데이터만 추가

현재 production content는 v5입니다. schema 3/reader 4/사용자 schema 3과 런타임 코드는 그대로입니다. vocabulary 226, meanings 244, 새 examples 447과 관계·태그·학습 설명을 기존 테이블에 추가했습니다. 앱은 기존 50개 keyset pagination으로 자료를 읽습니다. 어휘별 전체 의미·학습 노트는 저장되어 있으나 현재 UI는 대표 의미와 예문만 보여줍니다. 새 입문 course/quiz/SRS/UI를 이번 단계에서 선행 구현하지 않았습니다. 전체 DB와 배치 집계의 차이는 DATA_PROGRESS.md에 기록합니다.


## DEV-05 실제 어휘 회독

기존 프로토콜과 SQLite actor에 vocabulary count/card, set allocation/resume/transition API를 추가했습니다. Content DB/source는 DATA-01 그대로이며 스키마를 교체하지 않습니다. `VocabularyPassEngine`은 pure value-state transition, `VocabularySetCatalog`는 최대 100개 단위 content page와 사용자 배정 ID 조회, `VocabularyStudyViewModel`은 저장 성공 후 UI 진행을 담당합니다.

User schema v4의 vocabulary_sets/items는 사용자가 처음 시작할 때 발급한 local UUID와 고정 vocabulary stable ID 멤버십입니다. 세트당 최대 25개이며 기본 20개입니다. 신규 set 배정은 기존 sort_key/id 순서에서 아직 배정하지 않은 단어를 선택합니다. 전체 텍스트를 적재하지 않고 bounded scan하며, content 추가/재정렬로 기존 세트를 다시 계산하지 않습니다.

vocabulary_sessions의 Codable state JSON은 시도 ID, 세트 ID, 영구 어휘 IDs, round/order/position/passed/deferred, exposed/revealed, seed, version, dates, totalExposures, passID, optimistic revision입니다. 의미 공개·판정·회독 전이는 동기 SQLite transaction으로 저장합니다. expectedRevision과 active unique index가 오래된/중복 동작을 막습니다. 콘텐츠 누락은 사용자 기록을 보존한 오류이며 자동 통과나 초기화가 아닙니다.

vocabulary_events는 exposure/learn/known/round_completed/set_completed를 구분합니다. 노출은 기존 study_events의 viewed 및 item_progress/daily_statistics에도 같은 transaction으로 반영합니다. legacy learning_passes/pass_items에는 실제 회독을 기록하며 scope_content_id는 이 경로에서 local set UUID입니다. pass_number는 세트의 누적 회독, session.round는 개별 시도 안의 회독입니다. known은 completed_passes를 증가시키지만 acquisition_status/SRS/정답률을 바꾸지 않습니다.

완료된 시도는 보존하며 다시 보기는 새 UUID/seed로 시작합니다. active 시도는 content version이 달라도 고정 ID snapshot으로 재개합니다. 이 정책은 기존 lesson 세션의 보수적인 version 재시작 정책을 변경하지 않습니다.

UI는 full-screen 회상→공개→자기평가, 회독 경계, 완료 화면입니다. 카드별 첫 의미/그 의미의 예문/첫 note를 우선하며 추가 의미는 disclosure입니다. 기존 공통 Audio Service와 콘텐츠의 명시적 recorded/tts 정책을 재사용합니다. 최신 검증과 한계는 PROJECT_STATUS.md 및 VALIDATION_DEV05.md에 기록합니다.


## DEV-06 SRS 장기복습

기존 srs_state(content_id,skill)가 유일한 SRS 상태 저장소입니다. calendar_steps v1의 Codable SRSState와 indexed due_at/last_review_at을 함께 저장합니다. StepReviewScheduler는 3단계 자기평가에 따라 Gregorian calendar 간격을 계산하며 콘텐츠 타입/본문/DB row order와 독립적입니다. 기존 DEV-01 ReviewScheduling(StudyOutcome) 계약은 유지하지만 3가지 자기평가를 quiz outcome으로 뭉개지 않습니다.

SQLiteVocabularyProgress의 완료 transaction은 SRS 등록도 포함합니다. 이미 존재하는 키는 DO NOTHING이며 회독을 반복해도 기존 장기 단계/날짜를 덮어쓰지 않습니다. 과거 completed 시도는 AppContainer가 50개씩 backfill하고 srs_enrolled_passes 마커를 남깁니다. v5 migration은 원래 상태 표를 다시 만들지 않습니다.

review_sessions는 skill별 active 1개, review_items는 고정 ID/ordinal snapshot 및 노출·공개·결과/다음 예정일 이력을 담습니다. 판정은 SRS row + 결과 + session 완료를 하나의 SQLite transaction으로 저장합니다. session/content ID의 첫 판정이 유지되어 중복 탭/재시도로 다음 카드를 판정하지 않습니다. 회독 상태와 별도의 개념이지만 같은 ProgressRepository/SQLite 파일 안에 있고 콘텐츠에 FK를 걸지 않습니다.

Due는 idx_srs_skill_due로 skill/algorithm/version을 제한해 due_at<=now, ORDER BY due_at/content_id LIMIT 20으로 조회합니다. 전체 count는 별도 SQL입니다. 미판정 backlog는 그대로 유지되며 JSON/전체 progress를 로드해 필터하지 않습니다.

기존 Vocabulary 카드 표시를 VocabularyCardContentView로 추출하여 회독/복습이 같은 production meanings/examples/notes/audio를 사용합니다. ReviewViewModel은 저장 성공 후 진행하며 뜻 공개 전 판정을 거부합니다. 홈은 due 및 active 재개를 표시하고 새 학습을 잠그지 않습니다. 날짜/복귀/시간 변경 알림으로 요약을 갱신하며 상시 polling은 없습니다.

날짜는 UTC instant 저장, 다음 간격은 판정 당시 timezone의 Gregorian calendar-day로 계산합니다. 기존 instant는 여행 시 보존하고, 다음 판정부터 새 zone을 씁니다. 실패는 다음 날이며 같은 날 재학습 queue는 아직 없습니다. 알고리즘/legacy timezone/backfill/미검증 native build 제한은 PROJECT_STATUS.md가 최신 기준입니다.


## DEV-07 — Grammar integration

Content schema 3/content 8/reader 5. Existing grammar/examples/questions/course tables; no new Content database. `SQLiteGrammarContent` bounds lesson/card/search queries. Existing legacy course query excludes grammar courses and `GrammarCatalogView` routes grammar lessons to their runner.

UserProgress v6 adds grammar_sessions (transactional revisioned recall/page/question snapshot) and grammar_review_questions (selected question snapshot tied to existing review_items). Both use the existing SQLiteProgressRepository/DB. Existing srs_state uses skill=grammar; review_sessions/items and StepReviewScheduler are shared. `ChoiceJudgement`, `RecallOrder`, QuizOptions and KoreanAudioService are shared; vocabulary and grammar keep distinct necessary session states.

Every study transition is persisted before advancing UI. Completed grammar sets enroll atomically without overwriting existing SRS. Stable IDs and active snapshots survive content reordering. Review due SQL is indexed and bounded to 20 items, with grammar question rotation by reviewCount. Home offers two queues rather than a new mixed scheduler. Incorrect quiz answers cannot submit remembered. Native execution still requires the DEV-07 Mac checklist.


## DEV-08 — Conjugation / production

Content schema 3/content 9/reader 6. Existing text_input question/accepted/rubric + vocabulary stable target + example/grammar references. ConjugationEngine is a pure on-demand service; reviewed exception maps are currently question-scoped, not a global dictionary override catalog. Production pool is deliberately limited to authored questions.

UserProgress v7 adds production_sessions in the same DB/repository. Submitted answers/results, phase, bounded retry queue and question snapshot persist transactionally with revision checks. Unsubmitted draft text is not saved. Typed study_events skills separate production from recognition. Existing vocabulary SRS enrolls without resetting schedules; no copied scheduler or production-specific due UI. Grammar prerequisite data connects shared explanation UI and can later gate the pool. Current teaching precedes input without hard locks.

## DEV-09 — Listening / dictation

Content schema4/content10/reader7 adds source_example_id/audio_mode/editorial order to the existing listening_items table. No sentence copy and no separate content store. Existing question_choices/accepted/rubric contract supports four tasks. Example relationships preserve vocabulary/grammar provenance. Active practice batches are fixed 20-order ranges; queries load at most20 questions/30 catalog entries.

UserProgress v8 adds listening_sessions, listening_attempts, listening_plays to the same SQLiteProgressRepository. Revision-checked transitions atomically persist answers, local study events, scheduling and snapshots. ProductionAnswer/ChoiceJudgement/QuizOptions/KoreanAudioService/StepReviewScheduler are reused. Snapshot contains only a bounded session, including accepted answers for offline/stable resume. They are not constructed into visible/accessibility UI until feedback.

The shared srs_state uses skill=listening and listening item UUID. First attempts enroll for tomorrow; due review objective results map to remembered/unsure/difficult. Immediate retries never advance SRS. General practice leaves existing schedules unchanged. Due uses a skill/date index and a20-item limit. No new scheduler or network service. Reading missing/retired content preserves all progress, but retired due reconciliation remains a future migration concern.
