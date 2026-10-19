# PROJECT_STATUS — DEV-04

DEV-01〜03의 SQLite, actor repository, Importer/Validator, 영구 ID, 학습 UI 및 사용자 기록 구조를 유지한 확장입니다. DEV-03 상태는 `Docs/DEV-03_STATUS.md`에 보존했습니다. 재개된 작업의 기존 변경을 이어서 안정화했으며 새 대규모 어휘/SRS/서버 기능을 추가하지 않았습니다.

## 구현 결과

- `ハングル入門` 뒤에 **発音・パッチム** 과정 추가. 홈에서 바로 선택할 수 있고 이전 과정의 마지막 완료 화면에서도 다음 과정으로 이동합니다. 강제 잠금은 없습니다.
- 신규 14레슨 / 67단계: 발음 학습 페이지 36개, 객관식 31개(듣고 단어 선택 3개 포함), 관련 예시 13개.
- 받침의 위치와 7개 대표 끝소리, 겹받침, 연음·비음화·유음화·구개음화·기초 경음화·ㅎ 관련 변화, 자음/모음 비교, 읽기/듣기 및 종합 확인.
- 정식 철자와 교육용 발음 표기를 구분하는 화면. 기존 큰 한글·조용한 배경·하단 주요 버튼·정오답 피드백·진도 저장 UI를 재사용했습니다.
- 공통 `KoreanAudioService`: 검증된 녹음 경로와 시스템 한국어 TTS를 분리하고 normal/slow/stop 제공.
- TTS는 원래 철자의 검토된 단어/활용형만 읽습니다. 개별 자모·비교 발음·고립된 끝소리에는 TTS를 사용하지 않습니다.
- 레슨 시작/재개/완료, 마지막 위치, 정오답, 반복 시도는 기존 UserProgress에 연결합니다. 신규 이벤트의 skill은 pronunciation입니다.

**소스 구현과 실제 기기 동작 확인은 구분합니다. 이 환경에서 iOS 빌드·앱 실행·실제 음성 청취는 수행하지 못했습니다.**

## 과정 구조

| 순서 | 레슨 | 주요 콘텐츠 |
| --- | --- | --- |
| 1 | パッチムの位置 | 한, 먹 / 초성·중성·종성 조합 |
| 2 | 七つの終わり方① | ㄱ·ㄴ·ㄷ·ㄹ, 국/산/옷/달 |
| 3 | 七つの終わり方② | ㅁ·ㅂ·ㅇ, 밤/앞/방 |
| 4 | 二つ書くパッチム | 읽다[익따], 없다[업따], 앉다[안따] |
| 5 | つなげて読む・連音 | 한국어[한구거], 먹어요[머거요], 옷이[오시] |
| 6 | 鼻へつながる・鼻音化 | 한국말[한궁말], 먹는[멍는], 앞문[암문] |
| 7 | ㄹにつながる・流音化 | 설날[설랄], 난로[날로] |
| 8 | 이の前の変化・口蓋音化 | 같이[가치], 굳이[구지] |
| 9 | 強く構える・濃音化 | 학교[학꾜], 국밥[국빱] |
| 10 | ㅎが関わる変化 | 좋다[조타], 좋아요[조아요], 많다[만타] |
| 11 | 子音を比べる | 가/카/까, 다/타/따, 바/파/빠, 자/차/짜 |
| 12 | 母音を比べる | ㅓ/ㅗ, ㅜ/ㅡ |
| 13 | 単語を読んで聞く | 사과, 바다, 우유 / TTS 선택 문제 |
| 14 | 総合確認 | 발음 표기, 변화 유형, 철자 유지 |

내용은 실제 production 자료입니다. 자음·모음 비교는 모양과 조음 설명을 학습하는 레슨이며, **검증된 비교 녹음이나 듣기 판별 시험이 완성됐다는 뜻은 아닙니다.** 받침 설명에서는 일본어 모음을 덧붙이지 않는 점과 혀/입술/코의 차이를 설명합니다. 겹받침·ㅎ·유음화·구개음화는 적용 환경을 제한하고 예외를 일반화하지 않습니다. 장단음 표시는 이번 입문 표기에서 생략한다고 안내합니다.

일본어 설명은 자체 작성했습니다. 국립국어원 표준 발음법 및 공식 사전/상담 자료로 대표 예를 확인했으나 외부 전문가 감수 또는 TTS 청각 인증이 완료되었다고 주장하지 않습니다.

## Content DB / Importer 결정

기존 content schema v2 전체를 보존하고 **schema v3**에 다음 3개 테이블을 추가했습니다. 철자·발음 표기·음성 선택 정책을 설명 문자열이나 rubric_json에 섞지 않기 위한 확장입니다.

- pronunciation_presentations: rule_id, 정식 철자 spelling_ko, 복수 표기를 지원하는 readings_json, 적용/표기 설명 context_ja, 조합 표시 여부.
- content_audio: 콘텐츠 ID, tts/recorded_required, word_sentence/isolated/comparison 용도, TTS 원문 또는 선택적 녹음 asset, 편집 검토 메모.
- audio_questions: 기존 객관식 question_id와 공통 audio 콘텐츠 ID를 연결. TTS를 가짜 녹음 파일이나 listening_items로 등록하지 않습니다.

기존 pronunciation_rules / pronunciation_examples / examples / questions / lesson_items를 재사용합니다. 한 레슨만 최대 200단계 조회하며, 새 전체 자료를 앱 시작 때 파싱하지 않습니다.

버전은 **content schema=3 / content version=4 / reader=4 / UserProgress schema=3**입니다. dataset `ko-ja-core`와 is_fixture=0을 유지했습니다. Importer는 schema 2와 3을 지원하고 metadata에 맞는 SQL로 생성합니다. 앱도 기존 schema 2를 읽을 수 있습니다. 기존 콘텐츠 v1/v2 SQL은 수정하지 않았습니다. schema 다운그레이드는 거부합니다.

`Content/production.json`이 이제 앱 배포용 전체 원본입니다. DEV-03의 `hangul-production.json`은 당시 원본/회귀 기준으로 보존했습니다. 새 UUID는 한 번 발급해 `pronunciation-ids.json`에 저장했습니다. 재생성하지 마세요. DEV-03의 130개 항목은 ID, revision, 내용 및 관계 fingerprint가 모두 동일합니다.

새 Validator는 자모/비교 TTS, 발음 표기를 TTS 원문으로 대체하는 입력, 잘못된 발음 배열, 누락된 audio 참조, 듣기 질문의 원문 노출, 구형 reader metadata 등을 검사합니다. 구조 검증은 언어적 정답/녹음 품질을 인증하지 않습니다.

전체 DB: 2과정 / 26레슨 / 184단계, content_items 225개. 한글 55행/기존 문제 59개는 그대로입니다. 신규 pronunciation_rules 36행, audio 정책 36행(21 TTS / 15 녹음 필요), 전체 문제 90개입니다.

## Audio Service / TTS 정책

`LearningAudioPlaying` → `KoreanAudioService` → `AudioPlaybackBackend` 경계로 다른 학습 화면에서도 재사용할 수 있습니다. 앱에 하나의 service를 소유시키고 SwiftUI 환경으로 전달합니다. 실제 backend는 AVSpeechSynthesizer와 AVAudioPlayer이며 테스트용 backend를 주입할 수 있습니다.

- 한국어 음성: AVSpeechSynthesisVoice(language: "ko-KR"), 반환 음성의 언어도 확인. 없으면 일본어/기본 voice로 몰래 대체하지 않고 안내합니다.
- TTS normal=0.50, slow=0.42. 녹음 normal=1.00, slow=0.85. 값은 AudioPolicy에 모았습니다. 자연스러움은 기기/voice별 실청취 후 조정해야 합니다.
- 발음 표기의 `[한궁말]`을 합성하지 않습니다. 원래 철자 `한국말`을 전달합니다. 합성음과 검증된 녹음은 UI 레이블도 구분합니다.
- 호환 자모/유니코드 분해 자모/고어 자모 범위, 빈 입력, 발음 기호 표기, 비교 문자열, 500자 초과 등을 TTS 경계에서 거부합니다. 문자 검사만으로 교육적 적합성이 보장되지는 않아 제작자의 usage/review_note 검토도 필요합니다.
- 녹음 정책에는 자동 TTS fallback이 없습니다. asset이 없거나 파일/해시/경로가 잘못되면 재생하지 않습니다.
- 녹음은 번들 Audio/ 아래 상대경로, 제한된 확장자, SHA-256 일치, 10MB 이하 파일을 확인합니다. 현재 검증된 녹음 파일은 0개입니다.
- Content/Audio 폴더가 생기면 프로젝트 생성기가 폴더 리소스로 포함합니다. 실제 학습 음원을 추가할 때 권리와 품질을 먼저 검수해야 합니다.
- 새 재생은 이전 재생을 정지하고 큐를 쌓지 않습니다. callback 세대/대상 확인으로 이전 요청의 늦은 완료가 현재 재생을 끝내지 않게 합니다.
- 닫기, 단계 이동, 레슨 이동, 앱 비활성/백그라운드, 오디오 interruption 시작, 기존 출력 장치 이탈 시 정지합니다. category 변경 알림 자체로 재생을 끊지는 않습니다.
- 재생이 끝나면 audio session을 해제합니다. 마이크 권한·녹음·음성인식·백그라운드 재생 모드·네트워크 엔진은 없습니다.

## UI / Progress 연결

정식 철자가 가장 크고, 발음 표기는 title2 크기의 보조 정보입니다. 본문 뒤에는 문맥/표기 제한과 관련 예시를 표시합니다. 기존 시스템 배경/indigo/SF Symbols/Dynamic Type/VoiceOver/하단 primary action 스타일을 유지합니다. `聞く / ゆっくり / 停止`는 보조 조작이고 큰 글자에서는 세로 배치할 수 있습니다.

듣기 질문에는 정답 원문/발음 표기를 먼저 보여주지 않습니다. 재생 **완료** callback을 받은 뒤 답안 제출을 허용합니다. 재생 실패·중단은 들었다고 처리하지 않습니다. 음성 사용 불가 시 무작위 답안을 채점하거나 레슨을 가짜 완료하지 않으며, 닫았다가 음성이 가능한 환경에서 재개하도록 안내합니다. 재생 완료 여부는 일시 상태라 미제출 문제를 다시 열면 다시 듣습니다. 이미 제출한 답안/피드백은 재생 없이도 재개됩니다.

사용자 schema, 파일 경로, 기존 저장 트랜잭션은 변경하지 않았습니다. 시작/현재 ID/결과/완료 횟수와 study_events/item_progress/daily_statistics를 그대로 사용합니다. content version이 3→4로 바뀌므로 기존 진행 중 세션은 DEV-03의 보수적 정책에 따라 재시작 안내가 나올 수 있습니다. 이전 답안·즐겨찾기·완료 기록은 삭제하지 않습니다. 완료가 발음 숙련 인증을 뜻하지 않습니다.

## 테스트 및 빌드 결과

### 실제 수행

- Python **80개 통과**: DEV-03의 65개 + DEV-04 15개. 15,000 어휘/30,000 예문 synthetic 회귀도 포함.
- Importer: 오류 0, 짧은 예시 경고 5. 꽃/花, 밭/畑, 밥은 의도된 한 글자 어휘이므로 검토 후 유지했습니다. 검증을 끄거나 경고를 숨기지 않았습니다.
- 신규 코스 순서/규칙 범위, 실제 Swift 조회 SQL, 표기-발음 분리, 듣기 정답/숨김, unsafe TTS 거부, v3→v4 배포 시 ID 보존, 복수 발음 저장 구조 확인.
- 기존 사용자 SQLite 저장/재개/정오답/실패 롤백/콘텐츠 교체 독립성 회귀 통과.
- Swift 29파일 구문 분석 오류 노드 0; Xcode 프로젝트 파싱/리소스 참조/생성기 동일 출력/Info.plist/XML 검사 통과.
- Xcode의 실제 DB 복사 shell phase를 Debug/Release 임시 경로에서 실행해 schema 3/content 4 production 패키지 선택 확인.

결과 파일: `Docs/TEST_RESULTS_DEV04.txt`, `Docs/STATIC_CHECKS_DEV04.txt`, `Docs/PRONUNCIATION_CONTENT_REPORT.json`.

### 미실행

XCTest는 기존 18개 + 신규 11개 = **29개**를 작성했습니다. 음성 policy, missing voice, normal/slow/stop, missing recording, 늦은 callback, 실패 재생, 녹음 경로/해시, 발음 규칙 조회, 듣기 제출 gate 및 실제 사용자 repository 재개를 포함합니다. 시스템 음성 조회 테스트도 소리를 내지는 않습니다.

환경에 **Xcode와 Swift 컴파일러가 없어 iOS Debug/Release 빌드, Swift 타입 검사/링크, XCTest 실행, 시뮬레이터 UI, 실제 오디오 출력 검증은 미실행**입니다. 구문/SQL 검사만으로 이들이 통과했다고 주장하지 않습니다.

## 주요 파일

- Content/production.json, pronunciation-ids.json, content-schema-v3.sql
- Resources/content.sqlite, Tests/Fixtures/content-v3-production.sqlite
- Models/AudioModels.swift, PronunciationModels.swift, LessonModels.swift
- Services/KoreanAudioService.swift, App/HangulStudyApp.swift
- Repositories/SQLiteContentRepository.swift, RepositoryProtocols.swift
- Views/LessonSessionView.swift, LearnView.swift, SettingsView.swift
- ViewModels/LessonViewModel.swift
- Tools/ContentBuilder/build_content.py, validator.py, test_pronunciation_content.py
- Tests/PronunciationTests.swift, Tools/generate_project.py, HangulStudy.xcodeproj
- CONTENT_GUIDE.md, README.md, Docs/ARCHITECTURE.md, Docs/VALIDATION.md

## 알려진 제한 / 다음 단계

1. **Mac에서 build와 XCTest를 가장 먼저 실행**하고 실제 학습 경로/큰 글자/VoiceOver/작은 화면을 확인해야 합니다. `Docs/VALIDATION.md`에 절차를 정리했습니다.
2. 한국어 시스템 voice의 품질·설치 여부·음량·출력 장치는 기기에 따라 다릅니다. 합성음은 개별 자모/비교의 교육용 정답 음원이 아닙니다. normal/slow를 실제 한국어 화자와 실청취 검수해야 합니다.
3. 개별 발음 및 6개 비교 항목의 녹음은 미수록입니다. 자모 TTS로 빈자리를 채우지 마세요. 녹음 파일은 권리/발음/속도 검수 후 추가하세요.
4. 한국어 voice가 없으면 3개 듣기 문제가 있는 레슨은 그 위치에서 중단·재개합니다. 다른 레슨은 자유롭게 접근할 수 있습니다. 미청취를 정답/완료로 우회하는 기능은 없습니다.
5. pronunciation 표시 배열은 복수 발음을 수용하지만 이번 예시는 제한된 환경의 대표 표기입니다. 예외·표준 허용 발음·장단음·형태소 경계는 후속 DATA에서 문맥과 함께 보강하세요.
6. 외부 교육 전문가/일본어 편집자의 감수와 실제 초보자 사용성 검증은 아직입니다. 구조 테스트가 언어 품질을 대신하지 않습니다.
7. 무관한 콘텐츠 버전 변경에도 기존 active 세션은 재시작을 요구할 수 있습니다. 이전 기록은 보존됩니다. 더 세밀한 revision 기반 재개는 추후 정책 과제입니다.
8. 음원 resolver는 작은 번들 파일의 해시를 동기 확인합니다. 실제 대량 음원 도입 시 검증 캐시/비동기 처리 정책을 먼저 검토하세요.
9. 다음 DATA는 현재 content v4를 `--previous`로 사용해야 합니다. 예전 hangul-production.json 또는 production-empty.json으로 앱 DB를 덮어쓰지 마세요.
10. 전체 SRS/회독·대규모 어휘·TOPIK·문법 과정·광고/IAP·서버/로그인·발음채점은 미구현입니다. 실제 공부 시간 측정도 없으며 기존 duration_ms=0 정책을 유지합니다.

## TODO

새 TODO/FIXME 마커를 남기지 않았습니다. 위의 미구현/검증 대기 사항을 다음 작업에 인계합니다. 기존 기능을 임시 결과로 대체하지 않았습니다.
