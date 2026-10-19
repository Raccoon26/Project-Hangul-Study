# PROJECT_STATUS — DEV-03

작성: 2026-09-30. DEV-01/02 프로젝트·문서·저장 구조를 먼저 확인하고 이어서 구현했습니다. 이전 상태는 `Docs/DEV-01_STATUS.md`, `Docs/DEV-02_STATUS.md`에 보존했습니다. 이번 작업은 최대 45분 범위로 한글 입문 학습에 한정했습니다.

## 1. 구현한 내용

- 첫 production 과정 **ハングル入門**: 12레슨, 117단계, 59개 확인 문제.
- 현대 자모 40개와 일본어 설명/발음 힌트/예시/혼동점. 개발 fixture가 아닌 실제 교육 콘텐츠입니다.
- 홈의 과정 진행률과 레슨 목록 → 전체 화면 학습 → 선택형 퀴즈 → 정오답 피드백 → 완료/다시 학습/다음 레슨 흐름.
- 실제 ContentRepository에서 레슨별 콘텐츠를 읽고 기존 ProgressRepository/SQLite에 시작·답안·위치·완료·누적 통계를 저장합니다.
- 종료/재실행 후 같은 세션의 위치, 선택지 순서, 확정 답안/피드백을 재개하도록 구현했습니다.
- 단일 정답 판정, 테스트 가능한 선택지 섞기, 유니코드 음절 분해/조합식 표시.
- 검증된 자모 음원이 없을 때 nil을 반환하는 인터페이스. 일반 TTS 연결 없음.
- 기존 단어/예문 조회, 페이지 조회/검색 API, 즐겨찾기, Importer/Validator, schema v2를 보존했습니다.

**구현된 경로와 실제 기기 실행 확인은 구분합니다.** Linux 환경에서 iOS 앱을 실행하지 못했으며 아래 테스트/빌드 절을 확인하세요.

## 2. Hangul 과정과 production 데이터

| Unit | 제목 | 범위 |
| --- | --- | --- |
| 1 | はじめてのハングル | 음절 블록, 초성 ㅇ |
| 2 | 基本母音① | ㅏ ㅓ ㅗ ㅜ ㅣ |
| 3 | 基本母音② | ㅑ ㅕ ㅛ ㅠ ㅡ |
| 4 | 基本子音① | ㄱ ㄴ ㄷ ㄹ ㅁ ㅂ ㅅ |
| 5 | 基本子音② | ㅇ ㅈ ㅊ ㅋ ㅌ ㅍ ㅎ |
| 6 | 文字を組み立てる | ㄱ+ㅏ→가, ㄴ+ㅏ→나, ㅎ+ㅏ+ㄴ→한 |
| 7 | 濃音 | ㄲ ㄸ ㅃ ㅆ ㅉ |
| 8 | 複合母音① | ㅐ ㅔ ㅒ ㅖ |
| 9 | 複合母音② | ㅘ ㅙ ㅚ ㅝ ㅞ ㅟ ㅢ |
| 10 | パッチム入門 | 각/간/갇/갈/감/갑/강의 대표 끝소리 |
| 11 | 読んでみよう | 나/나무/바다/우유/하나 |
| 12 | 総合確認 | 문자·설명·조합·읽기 |

모음을 먼저 익혀 초성 ㅇ과 바로 음절을 만들 수 있도록 했습니다. 복합모음은 학습 분량을 줄이기 위해 두 레슨으로 나누고 별도 종합 확인을 두어 12레슨으로 구성했습니다. 레슨은 잠그지 않아 이미 학습한 사용자는 원하는 위치에서 복습할 수 있습니다.

실제 source는 `Content/hangul-production.json`, 발급 ID 색인은 `Content/hangul-ids.json`입니다. content_items 130개 = course 1 + lesson 12 + hangul 55 + note 3 + question 59. hangul 55개 중 현대 자모는 40개, 나머지는 조합/받침/읽기 페이지입니다. 선택지 225개, content_links 70개를 포함합니다.

일본어 설명은 자체 작성했고 국립국어원의 한글 원리·표준 발음법을 참고했습니다. 가타카나를 동일 발음으로 단정하지 않습니다. ㅐ/ㅔ의 발음 유사성과 철자 구별, 초성 ㅇ, ㄹ, 평음/격음/경음의 구별을 설명합니다. `CONTENT_GUIDE.md`에 참고 링크와 제작 규칙을 추가했습니다. 외부 전문가의 감수 완료나 기관 인증을 주장하지 않습니다.

## 3. 화면 구조와 디자인

기존 일본어 4탭을 유지합니다. `学ぶ`에 과정 설명, `n / 12 レッスン完了`, 간결한 레슨 행을 표시합니다. 진입은 fullScreenCover로 학습 중 탭 바를 숨깁니다.

학습 화면은 닫기/레슨 제목/현재 단계, 얇은 ProgressView, 큰 한글, 이름·분류, 일본어 설명, 하단 주요 버튼 순서입니다. 퀴즈는 선택지 선택→`答える`→피드백→`次へ`입니다. 정답은 체크 표시와 `正解`, 오답은 `もう一度確認しましょう` 및 정답/해설을 표시합니다. 완료 후 점수와 다시 학습/다음 레슨을 제공합니다.

시스템 배경색, 기존 indigo 한 가지 포인트, SF Symbols, semantic fonts와 ScaledMetric을 사용합니다. 중앙 내용 최대 폭 600pt, 충분한 여백, 버튼 44pt 이상의 터치 영역을 적용합니다. 큰 글자에서 본문과 선택지 높이가 늘어나며 스크롤됩니다. 단계가 바뀌면 스크롤 위치를 위로 돌리고, 정답 제출 시 피드백으로 이동합니다. VoiceOver 레이블/선택 상태/피드백 포커스를 제공합니다. 정오답은 색상만으로 구분하지 않습니다. 커스텀 애니메이션·소리·진동·게임화는 없어 Reduce Motion에 의존하는 연출이 없습니다.

## 4. Content DB / Stable ID / 버전

DB 기술은 기존 **SQLite3**입니다. 콘텐츠는 번들 read-only SQLite, 사용자 기록은 Application Support의 별도 writable SQLite입니다. 콘텐츠 schema v2는 바꾸지 않았습니다. 기존 hangul/learner_notes/questions/question_choices/courses/lessons/lesson_items/content_links를 사용합니다.

- dataset: `ko-ja-core`
- schema_version: **2**
- content_version: **3**
- min_reader_version 및 앱 readerVersion: **3**
- is_fixture: **0**
- 사용자 DB 버전: **3** (콘텐츠 schema와 별개)

ID는 한 번 발급해 source에 저장한 UUID이며, 위치·텍스트·rowid에서 재생성하지 않습니다. choice_id도 문제 내에서 영구 유지합니다. 콘텐츠 수정 시 ID를 유지하고 revision/content_version을 올립니다. 제거는 기존 tombstone 정책을 따릅니다.

Debug/Release 모두 `Resources/content.sqlite`를 번들로 복사합니다. 테스트 fixture는 XCTest 번들에만 넣었습니다. Debug 사용자 DB는 `user-production-development.sqlite`로 구분하고 DEV-02의 `user-development.sqlite`는 삭제하지 않습니다. fixture와 production은 dataset이 달라 기록을 섞지 않습니다. Release는 기존 `user.sqlite` 경로를 유지합니다.

## 5. Progress 저장

`user-migration-v3.sql`은 기존 사용자 스키마/데이터를 지우지 않고 다음을 추가합니다.

- lesson_sessions: 시도 UUID, lesson 영구 ID, content version, seed, 단계 ID 목록 snapshot, 현재 content ID, active/completed/abandoned 상태, 시작/갱신/완료 시각.
- lesson_step_results: (session_id, content_id) 유일 키, 확정 선택지, viewed/correct/incorrect, study_event ID.
- lesson_progress.completed_count: 레슨을 끝까지 완료한 횟수. 기존 completed 행은 1회로 보존.

사용자 DB에만 FK를 사용하며 콘텐츠 DB에 연결된 FK/cascade delete는 없습니다. event 저장 시 기존 item_progress와 daily_statistics를 함께 갱신합니다. 학습 횟수/정오답/최초·최종 학습일과 세션 이력이 남습니다. SRS/습득 상태/체감 난이도 필드는 기존 기반만 보존하며 새 알고리즘을 구현하지 않았습니다.

답안 제출과 이벤트/집계는 단일 트랜잭션입니다. 중복 제출은 기존 답안을 유지하고 재집계하지 않습니다. `次へ`는 답안이 있어야 현재 위치를 진행하며, 마지막 단계는 완료 상태와 완료 횟수를 함께 저장합니다. 중복 완료 호출도 재집계하지 않습니다. 설명 페이지의 viewed 저장과 위치 진행 사이에 종료되면 페이지가 한 번 다시 보일 수 있으나 기록은 중복되지 않습니다.

종료 버튼은 저장 중 비활성화됩니다. 미제출 선택지는 임시 UI 상태이며 저장된 답안이 아닙니다. content version 또는 단계 ID 목록이 바뀐 진행 중 세션은 기록을 보존하고 명시적인 재시작을 요청합니다. 새 시도는 과거 답안/통계를 지우지 않습니다. 기존 v1/v2 DB는 migration 전 SQLite backup API로 WAL까지 포함한 스냅샷을 남깁니다. 미래 버전이나 오류 발생 시 DB를 초기화하지 않습니다.

## 6. Quiz / 음원 구조

단일 정답 객관식으로 문자→발음 힌트/이름, 일본어 설명→문자, 조합, 읽기/분해를 표현합니다. 정답은 stable choice_id로 판정합니다. 선택지 순서는 seed + question ID의 FNV-1a/SplitMix64/Fisher–Yates로 섞습니다. 같은 세션 재개는 같은 순서, 새 시도는 새 seed입니다. 새 시도에서도 우연히 동일한 순서가 나올 수 있습니다.

`HangulComposition`은 현대 한글 음절의 초성/중성/종성을 분해하여 조합식을 제공합니다. 일반 자모를 음절처럼 분해하지 않습니다. `HangulAudioProviding` / `UnavailableHangulAudio`는 검증된 음원이 없음을 명시하며 재생 버튼/TTS/가짜 음원은 없습니다. VoiceOver는 접근성 탐색 기능이며 교육용 검증 음원을 대신하지 않습니다.

## 7. 테스트와 빌드

### 실제 수행

- Python 테스트 **65개 통과**: 기존 49개 + 한글 production 8개 + 사용자 학습 SQL 8개.
- production Importer: 오류 0 / 경고 0. DEV-02 production DB 대비 업데이트 검증 통과.
- 자모 전체 40개, 12레슨 순서, 실제 Swift에 쓰인 레슨 조회 SQL, 59개 정답/관계, stable ID 재빌드 일치 확인.
- 사용자 SQLite 재개방 후 위치/seed/답안 보존, 정오답 집계, FK/유일 키, 늦은 저장 오류 롤백, 기존 v2→v3 기록 보존, 콘텐츠 DB 파일 교체와 독립성 확인.
- 기존 synthetic 15,000 어휘/30,000 예문 생성·조회·인덱스 회귀 테스트 포함. 새 대규모 실제 어휘는 만들지 않았습니다. DEV-02 성능 실측은 `Docs/PERFORMANCE.json` 보존.
- Swift 25파일 tree-sitter 구문 분석: 오류 노드 0. 이는 타입 검사/컴파일이 아닙니다.
- Xcode project 파싱, 모든 소스/리소스 참조, 생성기 재실행의 동일 출력, Info.plist/shared scheme/workspace XML 검사.
- 실제 Xcode 콘텐츠 복사 shell phase를 임시 경로에서 실행: Debug/Release 모두 production content v3 확인.

원시 결과: `Docs/TEST_RESULTS_DEV03.txt`, `Docs/STATIC_CHECKS_DEV03.txt`, `Docs/HANGUL_CONTENT_REPORT.json`.

### 작성했지만 실행하지 못한 검증

XCTest **18개**를 프로젝트에 연결했습니다. 기존 10개를 유지/조정하고 자모 조합, 정오답, 선택지 재현/변화, 재개방/피드백, 중복 제출·완료, 미응답 진행 거부, 콘텐츠 변경 시 기록 보존, 실제 코스 로딩 8개를 추가했습니다.

**환경에 Xcode/Swift 컴파일러가 없어 iOS Debug/Release build, Swift 타입 검사·링크, XCTest 실행, 시뮬레이터/실기기 화면 확인은 미실행입니다.** 앱 실행 흐름과 Light/Dark/Dynamic Type/VoiceOver의 실제 작동을 확인했다고 주장하지 않습니다. 다음 Mac 환경에서 `sh Tools/verify.sh`와 `⌘U`를 먼저 실행해야 합니다.

## 8. 주요 파일

- Content/hangul-production.json, hangul-ids.json: 실제 콘텐츠/영구 ID
- Resources/content.sqlite: 미리 생성된 production DB
- Models/LessonModels.swift: 단계/선택지/세션/진도 모델
- LearningEngine/HangulLearning.swift: 조합/선택지 순서/음원 없음 계약
- Repositories/SQLiteContentRepository.swift: 레슨 단계 조회
- Repositories/SQLiteProgressRepository.swift: 세션/답안/진도, 기존 이벤트 저장 재사용
- Resources/user-migration-v3.sql, Persistence/UserDatabaseMigration.swift: 비파괴 사용자 migration
- ViewModels/LessonViewModel.swift, Views/LessonSessionView.swift: 실제 학습 흐름
- Views/LearnView.swift, ViewModels/AppModel.swift: 홈 진행률/재개 연결
- Services/AppContainer.swift, Tools/generate_project.py, HangulStudy.xcodeproj: production 기본 실행과 XCTest fixture 분리
- Tests/HangulLearningTests.swift, Tests/FoundationTests.swift: 네이티브 테스트
- Tools/ContentBuilder/test_hangul_content.py, test_learning_sql.py: 실행 가능한 콘텐츠/SQLite 검증
- Content/ContentPackageValidator.swift, Tools/ContentBuilder/validator.py: reader v3 지원
- Tests/Fixtures/content-v2-production.sqlite: 기존 production 업데이트 검증 기준
- CONTENT_GUIDE.md, README.md, Docs/ARCHITECTURE.md, Docs/VALIDATION.md: 제작/실행/검증 인계

## 9. 알려진 제한과 다음 단계

1. **Mac 빌드/XCTest/시뮬레이터 검증이 최우선**입니다. 특히 최대 Dynamic Type, 작은 iPhone, 가로 화면, VoiceOver 포커스, 배경 전환/강제 종료를 확인하세요.
2. 검증된 자모 음원이 없어 발음 듣기·발음 정확도 평가를 제공하지 않습니다. 일반 TTS로 대체하지 마세요. 음원 시스템은 별도 단계에서 추가하세요.
3. 콘텐츠는 실제 학습용으로 작성했지만 외부 한국어 교육 전문가/일본어 편집자 감수와 초보자 사용성 검증은 아직입니다. 평음/격음/경음·모음 구별은 텍스트만으로 충분한 청각 학습이 될 수 없습니다.
4. 과정은 잠금/선수학습 강제가 없고 완료는 습득 인증이 아닙니다. 전체 SRS·회독/숙련도 판정은 미구현입니다.
5. 무관한 콘텐츠가 추가되어 content_version만 올라가도 진행 중 레슨은 보수적으로 재시작 안내를 합니다. 기록은 남습니다. 세밀한 revision 기반 재개는 이후 정책 과제입니다.
6. 레슨 단계는 최대 200개, 선택형은 정답 1개만 지원합니다. 새로운 유형을 UI에 연결하려면 엔진과 테스트를 함께 확장하세요.
7. duration_ms=0이며 실제 학습 시간을 측정하지 않습니다. 진도는 로컬 기기에 저장하며 동기화/내보내기/계정/서버는 없습니다.
8. 단어 데이터는 아직 production에 없으므로 단어 탭은 빈 상태입니다. 기존 상세·즐겨찾기 코드는 보존했으며 테스트 fixture로 검증합니다.
9. 새로운 DATA 작업은 현재 content v3를 `--previous` 기준으로 삼고 영구 ID를 유지해야 합니다. `production-empty.json`으로 앱 DB를 덮어쓰지 마세요.
10. 고급 발음 변화, 대규모 단어/예문, TOPIK, 문법 과정, 광고/IAP/로그인/게임화는 이번 범위에 포함하지 않았습니다.

## TODO 기록

코드에 새 TODO/FIXME 마커를 남기지 않았습니다. 미구현/검증 대기 사항은 위 9절에 모두 정리했습니다. 기존 기능을 가짜 결과나 임시 코드로 대체하지 않았습니다. 기존 미래 SRS 계약은 그대로 보존했습니다.
