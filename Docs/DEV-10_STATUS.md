# PROJECT_STATUS — DEV-10

2026-10-04. 중단된 DEV-10 구현을 이어 통합·방어 코드·테스트·문서화를 마무리했다. 이전 DATA-06 상태는 `Docs/DATA-06_STATUS.md`에 보존했다.

**Linux에서 Xcode build, Swift type-check, XCTest, 실제 iOS Navigation/VoiceOver/음성 재생을 실행하지 못했다. 아래 SQL 실행·구문 검사 결과와 네이티브 미검증을 구분한다. App Store 배포 검증 완료 상태는 아니다.**

## 구현 내용 / Architecture

- 기존 9단계(ハングル → 入門 → 初級 → 初中級 → 中級 → 中上級 → 上級 → マスター → 維持学習)를 하나의 코스 진입점으로 연결했다. 모두 앱의 editorial level이며 TOPIK 대응표가 아니다.
- Content Repository의 실제 active 콘텐츠와 기존 course/lesson/set을 사용한다. Vocabulary, Grammar, Conjugation/Direct Input, Listening, Review는 기존 엔진/저장소/음성 서비스를 그대로 호출한다.
- 단계별 문자·발음/단어/문법/듣기 확인 수, 다음 미완료 문자·발음 lesson, 모든 기존 lesson 선택, 작은 단어 세트·문법 lesson·듣기 batch 진입을 제공한다.
- 첫 실행 홈에서 시작 위치 선택을 안내한다. 경험 버튼 3개와 전체 단계 Picker, 선택적 production 진단을 제공한다. 기존 학습 사용자도 위치를 변경할 수 있다. 강제 modal이나 hard lock은 없다.
- 홈은 続きから / 今日の復習 / 現在のコース를 중심으로 구성했다. active session → due review → 선택한 단계 순으로 계속하기를 제안한다. 복습을 먼저 끝내도록 강제하지 않는다.
- 維持学習에서도 복습·활용·듣기를 계속 이용한다. 상위 단계에 아직 콘텐츠가 없으면 사실대로 안내하고 수록된 初級 코스로 이동할 수 있다. 완료/졸업으로 영구 제외하지 않는다.

## Profile / Skip / Diagnostic / Resume

Content schema4 / content13 / min reader7 / UserProgress8 유지. DB와 production.json은 DATA-06 ZIP과 byte-for-byte 동일하다. 신규 콘텐츠 및 schema 변경0.

기존 UserProgress.user_metadata에 `curriculum.profile.v1`, `curriculum.diagnostic.v1`을 저장한다. 별도 진도 DB를 만들지 않았다. profile은 선택 level과 한글 skip 여부이며 완료·mastery·SRS 등록의 근거가 아니다. 변경·재진단은 기존 session/SRS/favorite 기록을 수정하지 않는다.

진단은 실제 production에서 한글2, 어휘2, 문법2, 활용 직접입력1, 듣기1, 총8문항을 조회한다. 질문/선택지·stable ID·Content Version을 session snapshot으로 저장하며 선택지 순서도 재개 시 보존한다. 새 진단은 재섞지만 이미 시작한 진단은 Content Version이 바뀌어도 같은 snapshot으로 이어진다. 별도 dummy 문제 배열은 없다.

- 한글 2문항 모두 오답이면 조기 종료하고 ハングル을 권한다.
- 한글 외 평가한 문항이4개 이상이며75% 이상 정답이면 初級, 그 외 入門을 권한다. 한글 평가가 모두 실패한 경우가 우선한다.
- 듣기 skip은 nil(미평가)이며 오답으로 누적하지 않는다. 음성이 없으면 안전하게 건너뛸 수 있다.
- 진단은 입문 시작 위치 참고용이다. 상급 능력, 공인 시험 등급, 전문적으로 보정된 숙련도를 판정하지 않는다. 사용자가 추천과 다른 단계를 선택할 수 있다.
- UUID/revision 검증과 transaction으로 중복 제출을 거부한다. 답변마다 저장하며 cold reopen으로 복원한다. 진단 재시작은 입력/음성 완료 상태도 초기화한다.

기존 학습 Resume는 원본 session을 수정하지 않고 stable target으로 해당 기존 화면을 연다. 여러 미완료 session이면 **단어 → 문법 → 활용 → 듣기 → 문자/발음 → 복습**의 결정론적 모듈 순서를 쓴다. timestamp가 있는 모듈 내부는 최신 우선, 활용/듣기는 stable target 순이다. 모든 모듈의 전역 최신 조작 시각 순이라고 주장하지 않는다. legacy Listening scope도 원문 그대로 전달한다.

## Progress / Level 전이 / SRS 독립성

- 단어 확인 수: completed_count>0인 기존 set의 DISTINCT vocabulary ID.
- 문법 확인 수: 회독 완료 시 등록되는 grammar SRS의 DISTINCT ID.
- 듣기 확인 수: 완료한 session의 최초 attempt itemID를 DISTINCT 계산. retry/반복학습을 더하지 않는다.
- 문자·발음: completed_count>0인 lesson. Grammar lesson은 별도 문법 수와 이중 집계하지 않는다.
- 장기복습 진행 표시: 기존 SRS stage>=4(30일 간격 단계) 수. 영구 습득을 뜻하지 않는다.
- 수록 영역을 모두 확인하면 다음 단계 링크를 제안하지만 자동 level 변경/차단/기존 기록 초기화를 하지 않는다.
- Content ID를 200개씩 keyset 조회해 집계하고 활용 목록은30개씩 조회한다. 전체 vocabulary/example를 메모리에 적재하지 않는다.
- 신규 데이터로 총수가 늘어도 기존 확인 수와 SRS는 유지된다. 진행률은 `확인 수 / 현재 수록 수`로 표시한다. denominator 증가는 콘텐츠 확장임을 UI에서 안내한다.
- Review hub는 단어/문법/듣기 전체 단계 due와 active session을 제공한다. 각 기존20개 제한 session을 사용하고 남은 backlog는 보존한다. 무작위 통합 review scheduler를 새로 만들지 않았다.

## UI 결정

기존 시스템 배경·한 포인트 색·SwiftUI List/NavigationLink·Dynamic Type·44pt 이상 주요 조작·텍스트 상태를 유지했다. 새 장식/애니메이션/게임화 없음. 학습 화면은 기존 엔진 화면을 재사용한다. 진단 듣기에는 원문 한국어 Text를 만들지 않고 재생 완료 후 선택하도록 했다. 실제 VoiceOver tree와 기기 청취는 미검증이다.

## Integration Audit

상세 범위와 기기 검증 절차: `Docs/DEV10_INTEGRATION_AUDIT.md`.

- Python/SQLite 전체 **180개 통과** (`Docs/TEST_RESULTS_DEV10.txt`). 신규6개는 실제 repository SQL을 실행해 level membership/제한조회/시작 위치 비파괴 저장/6종 resume 우선순위/중복 없는 완료 수/완료 전 듣기 제외를 검증한다.
- 기존 vocabulary 회독/SRS, grammar, 직접입력, 듣기 retry/progress, Content update SQL regression도 같은 전체 실행에 포함한다. Swift 실행을 대신하지 않는다.
- Swift68파일 tree-sitter 구문 오류0. 네이티브 XCTest88개 작성(신규4), **미실행**. Xcodeproject 59 app +9 test 소스 포함. `Docs/STATIC_CHECKS_DEV10.txt` 참조.
- 새 XCTest는 진단 조기 종료/정답 추천/미평가 음성/중복 조작/빈 문제 거부/실제8문항 구성/버전 변경 snapshot 재개/기존 favorite 보존을 포함한다.
- production source와 bundle DB 해시가 DATA-06과 동일함을 확인했다. 콘텐츠 변경이 없어 Content Version을 올리지 않았다. Validator를 약화하지 않았다. 전체 테스트에 기존 production validation/regression이 포함된다.

## Bugs Found

1. 새 continue 라우팅에서 legacy Listening scope `practice:intro`를 `practice:intro:0`으로 재구성하면 원래 session을 놓칠 수 있었다.
2. 기존 LessonFlow의 잘못된/빈 course index는 배열 범위를 벗어날 수 있었다.
3. 진단 재시작에서 이전 입력/음성 완료 상태가 남을 수 있었다.
4. profile 저장 중 다른 경험 버튼을 누르면 화면 선택과 저장 완료 표시가 어긋날 수 있었다.

## Bugs Fixed

1. ListeningStudyView에 optional resumeScope를 추가하고 resume은 원래 scope를 정확히 전달한다. 일반 진입은 기존 scope 정책 유지.
2. LessonFlow는 lesson index 범위를 검사하고 안전한 빈 상태를 표시한다.
3. open/restart에서 input/heard/playback revision을 초기화하고 공통 Audio Service를 stop한다.
4. 저장 중 경험 버튼/Picker를 비활성화한다. 저장 action guard와 진단 revision CAS를 적용한다.

위 사항은 소스/SQL 검토에서 확인·수정한 것으로 실제 iOS 재현 및 수정 후 UI 실행 검증을 주장하지 않는다.

## Known Remaining Issues / DEV-11 이후

- Mac에서 build/type-check/XCTest 및 기기별 UI/Audio/VoiceOver 검증 필요. 구문 검사가 컴파일 성공을 보장하지 않는다.
- curriculum은 기존 course/lesson/set의 level별 조합이다. 여러 모듈을 순서대로 자동 실행하는 authored mixed Unit 모델/일일 학습량 최적화는 구현하지 않았다. 현재는 계속하기·복습·단계 내 학습 선택으로 진행한다.
- 진단은 총8문항의 초반 간이 평가이며 고급 수준을 식별하지 않는다. 상위 레벨은 직접 선택 가능하지만 실제 콘텐츠가 아직 없다.
- 전역 최신 session 시각 정렬은 구현하지 않았다. 위 고정 모듈 우선순위로 복원한다.
- level별 집계는 한 번에200 ID씩 메모리를 제한하지만 총수 계산에는 해당 level 페이지 순회가 필요하다. 향후 실제 15,000어휘 DB에서 UI 지연을 측정하고 필요 시 별도 집계 cache를 도입한다.
- 문법 확인 수는 현재 grammar SRS 등록=회독 완료라는 기존 계약에 의존한다. 향후 SRS 수동 등록 기능을 추가하면 완료 근거를 분리해야 한다.
- 입력 연타/빠른 back/VoiceOver 정답 비노출/동적 글자 최대 크기/자정 및 timezone 변경은 네이티브 실기기 gate로 남는다. 순환 navigation이나 fake action을 의도적으로 넣지 않았으나 런타임 무결함을 보증하지 않는다.
- 신규 파일에 TODO/FIXME/임시 콘텐츠 없음. 미구현 사항은 이 절에 명시했다. 기존 기능/데이터를 placeholder로 대체하지 않았다.

## 주요 변경 파일

`Models/CurriculumModels.swift`, `Repositories/SQLiteCurriculum.swift`, `Repositories/RepositoryProtocols.swift`, `Repositories/SQLiteVocabularyProgress.swift`, `Views/CurriculumView.swift`, `Views/PlacementView.swift`, `Views/CurriculumResumeView.swift`, `Views/LearnView.swift`, `Views/GrammarLearningViews.swift`, `Views/ProductionView.swift`, `Views/ListeningView.swift`, `Views/LessonSessionView.swift`, `Models/AudioModels.swift`, `Tests/CurriculumTests.swift`, `Tools/ContentBuilder/test_curriculum_sql.py`, Xcode project 및 문서. 실제 경로/목록은 프로젝트 파일 기준.
