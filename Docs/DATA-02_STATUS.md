# PROJECT_STATUS — DATA-02

**入門 보강 + 初級 Production Vocabulary 1차 확장**을 완료했습니다. 2026-10-01에 중단 지점(DEV-06 상태)을 확인하고 이어서 작업했습니다. 기존 DEV-06 문서는 `Docs/DEV-06_STATUS.md`에 보존했습니다.

## 실제 추가·누적 수

모두 `Resources/content.sqlite`와 이전 v5 DB를 조회한 수입니다. 개발 fixture는 포함하지 않습니다.

| 항목 | 이번 추가 | 현재 누적 |
| --- | ---: | ---: |
| Vocabulary | 250 | 476 |
| 入門 vocabulary | 70 | 296 |
| 初級 vocabulary | 180 | 180 |
| Meanings | 260 | 504 |
| Production 문장 쌍 | 500 | 947 |
| examples 테이블 | 500 | 960 (기존 발음 단어 예시 13 포함) |
| Vocabulary→example 관계 | 500 | 952 |
| 일본인용 learner_notes | 32 | 100 (어휘 연결 97 + 기존 3) |

신규 250개 모두 예문이 2개 있습니다. 10개 다의어는 두 의미와 각 의미에 맞는 예문을 분리했습니다. 기존과 새 문장 쌍의 중복은 없습니다. 고유 표제어 문자열은 누적 472개입니다.

주요 영역: 가족·인칭·지시어, 요일·계절·시간·숫자, 날씨·위치, 식사·쇼핑, 집안일·일상 동작, 인간관계·연락, 학교·직장, 교통·여행·숙소, 서비스·계산, 몸·건강, 감정·성질, 부사·예정·이동. 신규 품사는 명사 98 / 동사 81 / 형용사 32 / 부사 22 / 대명사 4 / 관형사 5 / 수사 6 / 의존명사 2입니다.

## 저장·버전 정책

- **Content schema 3 유지 / Content version 5 → 6 / min reader 4 유지**.
- **UserProgress schema 5 유지**. 사용자 DB migration·초기화·재생성 없음.
- 정식 원본은 기존 **Content/production.json 한 개**입니다. Importer와 Validator를 수정하거나 규칙을 완화하지 않았습니다.
- 기존 Resources/content.sqlite를 **Tests/Fixtures/content-v5-production.sqlite**에 바이트 그대로 보관하고 `--previous` 검증에 사용했습니다.
- 신규 콘텐츠는 UUIDv4를 한 번 발급해 production.json에 저장했습니다. 기존 1,220개 콘텐츠 ID/본문/관계 fingerprint와 기존 어휘·의미·예문 행을 모두 보존했습니다. 기존 정렬 키·revision·level을 변경하지 않았습니다.
- `Content/data02-ids.json`은 검수용 ID 색인이고 `Docs/DATA02_REVIEW_CATALOG.md`는 원본에서 추출한 읽기 목록입니다. 앱/Importer는 이 파일들을 별도 콘텐츠 source로 사용하지 않습니다.
- 새로운 25개 주제 태그와 배치 태그, 자체 편집 출처를 기존 표에 추가했습니다. 공식 TOPIK·객관적 빈도·추정 발음·추정 우선순위는 넣지 않았습니다.
- level은 편집상 intro/beginner이며 공식 시험 급수가 아닙니다. 기존 sort_key 기반 새 세트 선택을 유지하고 새 editorial ranking을 꾸며 넣지 않았습니다.

## 검수·중복 판정

- 원고 작성 후 source에서 추출한 별도 목록으로 품사, 기본형/활용, 한일 의미·예문, 높임말·띄어쓰기, 의미별 연결을 재검토했습니다.
- 초안의 기존 기다리다 중복을 제거하고 지키다로 교체했습니다. 기존과 같았던 9개 문장 쌍 및 신규 내부 1개 쌍은 다른 자연스러운 문맥으로 수정한 뒤 반영했습니다.
- 기존 동형어 차/일/쓰다를 보존했습니다. 신규 **저(관형사「あの」)**는 기존 **저(대명사「私」)**와 품사·의미가 다른 의도적 항목이며 note로 구분했습니다. 같은 품사·의미의 중복 어휘를 추가하지 않았습니다.
- 의미별 분리 예: 번(回/番), 살다(住む/生きる), 닦다(拭く/磨く), 보내다(送る/過ごす), 머리(頭/髪), 익다(火が通る/熟す).
- 32개 note는 깨끗하다의 청결/미관 차이, 기분/몸 상태, 빌리다/빌려주다, 잊다/잃어버리다, 다르다/틀리다, 알려주다/가르치다, 방학/휴가, 일찍/빨리, 수사·조사·불규칙 등 실제 혼동 지점을 다룹니다.
- 하다형은 기존 정책대로 other(여 불규칙), ㅂ/ㅅ/르 불규칙을 해당 기본형에 설정했습니다. ㄹ·으의 규칙적 탈락은 none, 서술어 has_batchim은 기존대로 null입니다.
- 외부 교육 전문가의 감수나 기기 음성 검수 완료를 의미하지 않습니다. Validator는 언어 교육 품질을 인증하지 않습니다.

## 회독 / SRS / 접근 연결

기존 `ContentRepository → VocabularySetCatalog → VocabularyPassEngine → SQLiteProgressRepository → SRS`를 그대로 사용합니다. engine/repository/persistence/audio 코드는 바꾸지 않았습니다.

진행 중 세트의 membership과 현재 회독은 UserProgress에 저장한 stable ID snapshot 그대로 재개합니다. 새 세트만 기존 bounded keyset scan에서 미배정 ID 20개를 고릅니다. 새 입문 단어가 가나다순 앞쪽에 들어가도 기존 세트를 재구성하지 않습니다. 초급 세트도 동일한 경로를 사용합니다. 세트 완료 시 기존 SRS 등록 정책이 적용되며 기존 예정일·단계를 초기화하지 않습니다.

**필요한 최소 UI 연결 수정:** DEV-05의 세트 화면이 intro로 고정되어 신규 beginner를 학습할 수 없었습니다. 기존 화면에 level 인자(기본 intro)를 전달하게 하고 홈에 같은 형식의 初級単語 진입 행을 추가했습니다. 실제 DB COUNT와 재개 항목을 표시합니다. 새 디자인·새 학습 엔진·DATA 전용 로직은 추가하지 않았고 기존 입문/한글/발음/복습을 유지했습니다.

## 실제 검증 결과

- Production Validator: **오류 0 / 검토 경고 9**. 기존 짧은 발음 예시 경고 5 + 동형 표제어 후보 4(차/일/쓰다/저). 경고를 끄지 않았습니다.
- `--previous content-v5-production.sqlite`로 candidate 생성 성공, 검수 후 Resources/content.sqlite에 반영했습니다. schema 3 / content 6. 결과 `Docs/DATA02_BUILD_REPORT.json`, 최종 재검증 `Docs/DATA02_VALIDATION.json`.
- **Python/SQLite 123개 통과**(기존 116 + DATA-02 7). `Docs/TEST_RESULTS_DATA02.txt`.
- 신규 검사: 전체 신규 ID·의미·예문·note, 의미별 예문, level별 keyset 20개 조회, 품사 분포, 한국어/일본어/제2의미 검색, 동형어 판정, 문장 중복, 불규칙/메타데이터, 기존 1,220 ID fingerprint 보존, v5→v6 실제 콘텐츠 파일 교체 뒤 user state/세트/즐겨찾기/SRS 보존, 신규 ID의 실제 SRS INSERT/due SQL 호환성 및 재등록 보존.
- 기존 importer/validator/15,000어휘·30,000예문 synthetic/한글·발음·회독·SRS SQL 회귀를 함께 실행했습니다. 과거 고정 수치 기대값은 현재 DB의 정확한 수치로 갱신했고 검증 규칙은 약화하지 않았습니다.
- **Swift 45파일 tree-sitter 구문 오류 0**, plist/XML/프로젝트 참조, SQLite integrity/FK 검사 통과. `Docs/STATIC_CHECKS_DATA02.txt`.
- engine/repository/audio/model/schema/importer/validator **32파일이 DEV-06과 바이트 동일**합니다. 기존 프로젝트 파일 삭제 없음.
- Native XCTest는 초급 실제 ContentRepository → 회독 완료 → SRS → 디스크 재개 통합 테스트 1개 추가하여 **총 59개 작성**했습니다.

**실행하지 못한 검증:** Linux에는 Swift compiler/Xcode/iOS simulator가 없습니다. Swift type-check, Debug/Release build, XCTest 실행, UI/VoiceOver/Dynamic Type 실제 표시, Korean TTS 청취, 실제 앱 종료/재실행은 미수행입니다. Python SQL 테스트는 Swift 제어 흐름 실행을 대신하지 않습니다. 빌드했다고 주장하지 않습니다.

Mac: `TEST_DESTINATION='platform=iOS Simulator,id=실제ID' sh Tools/verify.sh`.

## 주요 변경 파일

- Content/production.json / Content/data02-ids.json / Resources/content.sqlite
- Tests/Fixtures/content-v5-production.sqlite
- Views/VocabularyStudySetsView.swift / Views/LearnView.swift / ViewModels/AppModel.swift — beginner 접근에 필요한 인자·진입·실제 count만
- Tests/VocabularyPassTests.swift — production beginner 통합 테스트
- Tools/ContentBuilder/test_data02_content.py 및 기존 release 수치 기대값 테스트 3파일
- PROJECT_STATUS / CONTENT_GUIDE / DATA_PROGRESS / README
- Docs/DATA02_REVIEW_CATALOG.md / DATA02_REVIEW.md / 검증·테스트·정적검사 로그

## 알려진 한계 / 다음 DEV·DATA

1. Mac native build/59 XCTest와 초급 진입→완료→SRS 실기기 경로를 확인해야 합니다. 테스트 작성과 실행을 혼동하지 마세요.
2. 사용자 세트는 편집 레슨이 아니라 20단어 내외의 고정 ID 묶음입니다. 가나다순과 UUID tie-break를 유지했으며 세밀한 선수학습 순서·편집 우선순위는 후속 과정 설계에서 다룹니다.
3. 외부 한일 언어·교육 감수 및 실제 TTS 청취는 미완료입니다. 신규 부사·동사 예문에는 배치 밖의 일상 기초어도 포함되며 완전한 controlled vocabulary 문장집은 아닙니다.
4. 현재 UI는 의미별 예문 1개를 UUID 순으로 보여줍니다. 저장된 예문 2개가 한 카드에 모두 표시되지는 않습니다. 예문 순서 정책은 기존 제한으로 유지했습니다.
5. DATA-03 시작 시 **현재 v6 DB**를 이전 배포로 보관해 --previous로 지정하고 content 7 이상으로 올리세요. v5 기준을 계속 최신으로 사용하지 마세요. schema/reader/UserProgress는 데이터 추가만으로 올리지 않습니다.
6. 기존 SRS 날짜·재등록·누락 ID 안전 정책은 DEV-06 문서 그대로입니다. 새 단어 추가 때문에 이전 set/review snapshot을 다시 계산하지 마세요.
7. 신규 문법·발음·듣기·TOPIK·음원, 광고/IAP/서버, SRS 알고리즘 변경은 하지 않았습니다. 새 TODO/FIXME 코드 마커 없음.
