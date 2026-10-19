# PROJECT_STATUS — DEV-07

2026-10-01 UTC 구현·검증, 2026-10-02 UTC 중단 후 문서·배포 파일 정리. DATA-03 프로젝트·문서·production v7 DB를 확인하고 기존 구조 위에 문법 학습·회독·SRS 경로를 구현했습니다. 이전 상태는 `Docs/DATA-03_STATUS.md`에 보존했습니다. **Linux에서 Python/SQLite 검증과 Swift 구문 검사를 수행했습니다. Xcode 빌드·Swift type-check·네이티브 실행은 아직 검증하지 못했으므로 App Store 출시 준비가 끝났다는 의미는 아닙니다.**

## 구현한 흐름

`学ぶ → 文法 → 入門/初級 → 레슨 → 의미 → 형태/포인트 → 예문/비교 → 문제/피드백 → 覚える/覚えてる → 남은 문법만 다음 회독 → 완료/SRS 등록`을 연결했습니다. 예정일이 되면 홈 `今日の復習 → 文法`에서 실제 문제를 풀고 `難しい / もう少し / 覚えた`로 기존 SRS 일정을 갱신합니다.

- 실제 콘텐츠: **문법 12 / 예문 24 / 문제 24**, 신규 코스 2 / 레슨 4. 기존 vocabulary 726개는 그대로입니다.
- 입문: 이에요/예요, 은/는, 이/가, 을/를, 에, 에서. 초급: -고 싶다, -고, -지만, -아/어서, -(으)면, -(으)니까.
- `名詞と助詞①`, `場所と目的語`, `希望・つなぐ表現`, `理由と条件`의 3항목씩 작은 레슨입니다. 기존 course/lesson ID 체계를 사용합니다.
- 入門부터 マスター까지 기존 LearningLevel을 지원합니다. 미수록 상위 단계는 사실대로 안내하며 가짜 레슨을 만들지 않습니다.
- 비교 5쌍: 은/는↔이/가, 에↔에서, -고↔-지만, -아/어서↔-(으)니까, -(으)면↔-(으)니까. 유사성을 동의어로 단정하지 않으며 현재/상대 표현의 설명과 실제 예문을 펼쳐 봅니다.

## 아키텍처·DB·호환성

**Content schema 3 유지 / Content 7→8 / reader 4→5 / UserProgress 5→6**.

Content는 기존 read-only 번들 SQLite, 유일한 production 원본은 `Content/production.json`입니다. 기존 grammar, grammar_examples, content_links, questions, question_choices, courses, lessons, lesson_items를 사용합니다. 별도 grammar DB/런타임 배열/새 파일 형식은 없습니다. reader 5는 새 문법 질문 계약과 코스 분기를 알지 못하는 구버전이 새 패키지를 잘못 해석하지 못하게 합니다. 실제 테이블 변경이 없어 Content schema를 올리지 않았습니다.

`SQLiteContentRepository`에 문법 쿼리를 추가했습니다. 레슨은 level/ordinal 기준 최대 30개, 문법 검색은 level/ID keyset 최대 50개, 한 카드의 예문·비교 각 6개, 문제 최대 20개만 가져옵니다. 레슨은 최대 20항목입니다. 이번 seed는 3항목/예문 2개/문제 2개입니다. 모든 문법·예문을 앱 시작 시 적재하지 않습니다. 기존 한글/발음 코스 쿼리는 문법 코스를 제외해 기존 lesson runner와 충돌하지 않습니다.

UserProgress는 **같은 SQLiteProgressRepository와 사용자 DB**입니다. 기존 backup+transaction migration 경로로 v6를 적용합니다.

- `grammar_sessions`: lesson stable ID, 대상 ID snapshot, 현재 회독/순서/위치, 다음 회독 대상, 반복 이력, 현재 설명 page, 현재 문제 snapshot/선택, 노출·정오답 합계, 시작/갱신/완료 시각, revision을 JSON으로 저장합니다. active 시도는 레슨당 하나입니다.
- `grammar_review_questions`: 기존 review_items를 참조하는 현재 문법 복습 문제 snapshot과 선택/정오답입니다. 별도 SRS 상태를 만들지 않습니다.
- 문법의 first/last studied, 정오답, 노출, completed_passes는 기존 item_progress와 study_events에도 기록합니다. exposure·quiz answer·completion 및 해당 content revision/version을 보존합니다.
- SRS는 기존 `srs_state(content_id,skill)`의 **skill=grammar**, review_sessions/review_items를 재사용합니다. vocabulary와 분리되며 ID도 기존 UUID 규칙을 따릅니다. 사용자 DB에서 Content DB로 FK를 걸지 않습니다.

## 회독·저장·재개

문법은 의미/형태/예문 학습과 연결된 문제를 마친 뒤에만 자기판정합니다. `覚えてる`는 이번 시도 통과, `覚える`는 다음 회독 대상입니다. 남은 항목만 회독 종료 후 seeded shuffle합니다. 단어/문법은 각각 필요한 상태 모델을 유지하고 `RecallOrder`와 기존 `QuizOptions`를 함께 씁니다. 정답 판정은 기존 한글/발음 퀴즈와 `ChoiceJudgement`를 공유합니다.

각 동작은 revision 검사와 DB transaction으로 저장합니다. 설명 page, 현재 문제, 선택 직후 피드백까지 재개합니다. 선택 직후 종료해도 정오답이 다시 누적되지 않습니다. 진행 중인 lesson membership과 문제 snapshot은 콘텐츠 업데이트로 다시 계산하지 않습니다. 완료 후 `もう一度学ぶ`만 새 시도를 만들며 active 시도는 항상 이어갑니다. 콘텐츠가 삭제/비활성되어 읽히지 않으면 오류를 보여주고 기록을 보존합니다.

남은 문법이 0개이면 완료를 저장하고 **해당 레슨의 모든 문법**을 SRS에 원자적으로 등록합니다. 첫 회독에서 통과한 항목도 등록하며 `ON CONFLICT DO NOTHING`으로 기존 단계/날짜를 유지합니다. 완료는 영구 습득이 아닙니다. 다시 보기나 향후 복습을 막지 않습니다.

## SRS·날짜·오늘의 복습

기존 calendar_steps v1 스케줄러를 변경하지 않았습니다. 1/3/7/14/30/60/120일 정책, 실패 시 짧은 간격, 보수적 판정, 최고 단계 유지학습을 그대로 사용합니다. Date는 UTC instant로 저장하고 다음 날짜는 사용자 IANA timezone의 Calendar로 계산합니다. 최초 등록 시 반복 필요 여부도 전달합니다.

홈은 今日の復習 아래 単語/文法을 선택하게 했습니다. 두 타입을 강제로 섞는 새 스케줄러는 만들지 않았습니다. 문법 due는 기존 indexed srs_state에서 skill/algorithm/version/due_at 조건으로 집계하고, due_at/ID 순 최대 20개씩 snapshot합니다. 남은 backlog는 사라지지 않습니다. 오늘의 단어 완료 수가 문법을 중복 집계하지 않도록 skill filter를 추가했습니다.

문법 복습은 reviewCount에 따라 연결 문제를 순환 선택합니다. 현재 문제는 로컬에 고정하며 정답 제출 전 SRS 판정은 불가능합니다. 오답이면 `覚えた`를 UI와 repository 양쪽에서 거부하고 `難しい / もう少し`로 조정합니다. 선택 후 의미/형태/예문도 확인할 수 있습니다. 1회 복습에 문제 1개이며 장기적으로 의미·빈칸·문맥·형태·비교를 섞을 수 있습니다. 같은 카드의 즉시 무한 반복은 없습니다.

## Quiz·Validator·콘텐츠 품질

기존 multiple_choice 문제와 단일 정답을 사용하고 rubric_json.grammar_task에 meaning/context/blank/form/contrast를 기록합니다. 다섯 유형 모두 실제 seed에 있습니다. 주관식 입력 엔진은 이번 범위가 아닙니다. 선택지는 seeded shuffle, 정오답과 짧은 일본어 이유를 표시합니다.

Validator에 grammar 중복 표현 후보, 학습용 문법의 의미/형태/설명/active 예문·문제, question_task/단일 정답/선택지 범위, 레슨 크기와 level 내 ordinal 유일성, contrast_grammar 관계를 추가했습니다. 기존 검증 규칙을 끄지 않았습니다. 새 자료를 별도 pass로 읽으며 중복 문장, 일본어 번역의 성별 추정, 은/는 문맥 문제의 모호성을 고쳤습니다. 기존 production 본문 수정은 **0개**입니다. 전문 감수 완료를 주장하지 않습니다.

## UI·접근성

기존 SwiftUI/system background/한 가지 accent를 유지합니다. 큰 한국어, 의미→형태→예문→퀴즈의 순서, 하단 주요 버튼, fullScreen 학습, 간단한 진행 표시입니다. 비교는 필요한 때 펼치며 설명을 한 화면에 몰아넣지 않습니다. 예문 음성은 기존 KoreanAudioService의 normal/slow/stop만 사용합니다. 문법 기호/자모를 TTS에 보내지 않습니다. 음성 미설치는 기존 availability 안내로 처리합니다.

Dynamic Type/ScaledMetric, 44pt 이상 주요 터치 영역, 텍스트·아이콘 피드백, 닫기/음성 VoiceOver label을 적용했고 애니메이션을 추가하지 않았습니다. 실제 화면 크기·VoiceOver/청취 검증은 Mac/iPhone에서 남아 있습니다.

## 실제 검증 결과

- Production Validator **오류 0 / 경고 10**: 기존 짧은 발음 예시 5, 동형어 차/일/쓰다/저/적다 후보 5. 새 문법 중복 후보 없음.
- v7 이전 배포 검사 및 production DB 생성 성공. 기존 **3,380 content ID와 payload/fingerprint 보존**. v7 snapshot은 DATA-03 배포 DB와 바이트 동일합니다.
- **Python/SQLite 138개 통과**: 기존 129개+문법 9개. 실제 query/관계/5문제유형/Validator 거부/중복 후보/v5→v6 보존/grammar SRS due·재등록/선택 snapshot 재개/Swift 내 SQL 준비 검사. 기존 importer·synthetic 15k/30k·한글·발음·오디오 정책·회독·SRS 회귀를 포함합니다.
- **Swift 53파일 tree-sitter 구문 오류 0**, Xcode 파일 참조 61개, plist/XML, SQLite integrity/FK 통과. 기존 핵심 13파일은 DATA-03과 바이트 동일. 삭제 파일 없음.
- Native XCTest는 문법 6개를 추가해 **66개 작성, 미실행**입니다. 문법 회독 축소·전부 통과/보류·판정/저장·잘못된 상태·실제 production repository→회독→SRS→복습→재개·stage 변화를 테스트하도록 작성했습니다.
- **Xcode Debug/Release build, Swift type-check, XCTest 실행, UI/실제 앱 재시작/TTS 청취는 미수행**입니다. Python SQL 검증은 Swift 제어 흐름이나 실제 앱 실행을 대신하지 않습니다.

로그: `Docs/TEST_RESULTS_DEV07.txt`, `STATIC_CHECKS_DEV07.txt`, `DEV07_CONTENT_REPORT.json`. Mac 확인 절차는 `Docs/VALIDATION_DEV07.md`입니다.

## 주요 변경 파일

Models/GrammarModels.swift, LearningEngine/GrammarLearning.swift, Repositories/SQLiteGrammarContent.swift / SQLiteGrammarProgress.swift, ViewModels/GrammarViewModel.swift, Views/GrammarLearningViews.swift / GrammarReviewView.swift, Resources/user-migration-v6.sql, Tests/GrammarLearningTests.swift, Tools/ContentBuilder/test_grammar_content.py.

기존 RepositoryProtocols, SQLiteReviewProgress, VocabularyPassEngine, LessonModels, LearnView/AppModel, UserDatabaseMigration, ContentPackageValidator, Validator와 Xcode generator에 최소 통합 변경을 했습니다. production.json/content.sqlite와 문서를 갱신했습니다. 상세 파일별 목록은 `Docs/CHANGES_DEV07.md`입니다.

## 종료 전 감사·알려진 문제·다음 단계

- 이번 추가 코드에 TODO/FIXME/placeholder, 무동작 버튼, fixture 기반 런타임 콘텐츠는 없습니다. 닫기/재시도/다음/문제 선택/자기판정/다음 회독/다시 학습/복습 결과 모두 실제 경로에 연결했습니다. 네이티브 UI 실행 검증은 남아 있습니다.
- 앱 빌드 가능성을 확정할 수 없는 환경입니다. **DEV-08 시작 전에 Mac에서 Debug/Release와 66 XCTest, v5 업데이트/재개/음성·접근성 회귀를 실행**하세요. 실패가 있으면 기능 추가보다 먼저 수정해야 합니다.
- 문법 콘텐츠는 입문/초급 12개뿐입니다. 외부 한일 교육 전문가 감수는 미완료입니다. DATA-04에서 현재 계약으로 확대하고 문맥상 복수 정답이 가능한 문제를 특히 재검수하세요.
- 비교/예문은 현재 각 6개까지 표시합니다. 더 많이 연결할 경우 교육 우선순위·추가 보기 정책을 먼저 확장하세요. 비교 note는 문법 단위이며 별도 relation별 설명 테이블은 만들지 않았습니다.
- 문법 lesson ordinal은 같은 level 전체에서 유일하게 유지해야 합니다. 배포 후 lesson membership/UUID를 함부로 변경하지 마세요. 이미 시작된 session은 snapshot을 유지합니다.
- Grammar SRS는 매 방문 하나의 문제를 순환합니다. 자유 입력/작문·adaptive mixed scheduling·고급 활용은 미구현 범위입니다.
- DATA-04는 **현재 Content v8 DB를 이전 배포로 보관**, 다음 Content 9 이상/reader 5/schema 3 계약을 사용하세요. 기존 회독/SRS를 재생성하지 마세요.
