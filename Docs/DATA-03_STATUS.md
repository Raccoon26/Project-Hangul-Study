# PROJECT_STATUS — DATA-03

**初級 Vocabulary 2차 확장·일상 표현 강화**를 완료했습니다. 2026-10-01 UTC에 기존 DATA-02 프로젝트·문서·production v6 DB를 확인하고 진행했습니다. 이전 상태는 `Docs/DATA-02_STATUS.md`에 보존했습니다.

## 실제 추가·누적 수

아래 수는 현재 `Resources/content.sqlite`와 이전 v6 DB를 조회한 값입니다.

| 항목 | DATA-03 추가 | 현재 누적 |
| --- | ---: | ---: |
| Vocabulary | 250 | 726 |
| 入門 vocabulary | 10 | 306 |
| 初級 vocabulary | 240 | 420 |
| Meanings | 268 | 772 |
| Production 문장 쌍 | 500 | 1,447 |
| examples 테이블 | 500 | 1,460 (기존 발음 단어 예시 13 포함) |
| Vocabulary→example 관계 | 500 | 1,452 |
| Learner notes | 48 | 148 (어휘 연결 145 + 기존 3) |
| 어휘 간 typed 관계 | 15 | 이번 배치 추가분 |

기존 데이터 수정 **0개**입니다. 250개 모두 예문 2개를 연결했고, 다의어 18개는 의미 2개와 의미별 예문으로 분리했습니다. 동일 문장 쌍 중복은 없습니다. 누적 고유 표제어 문자열은 721개입니다.

신규 품사: **동사 109 / 형용사 51 / 부사 30 / 명사 52 / 의존명사 8**. 동사·형용사·부사 190개(76%)에 집중했습니다. 주요 영역은 생각·판단, 부탁·의사소통, 물건 조작, 자동사/타동사, 변화, 감정·성격·신체 상태, 시간·정도·태도, 일상 추상어, 수량·기간, 생활비·학습·통신입니다. 入門 보강 10개는 살/초/개월/달/이틀/사흘/주일/장/병/층입니다.

## 기존 구조·버전·ID

- **Content schema 3 유지 / Content version 6 → 7 / min reader 4 유지 / UserProgress schema 5 유지**.
- 원본은 기존 `Content/production.json` 한 개입니다. Importer / Validator / source reader / schema를 수정하거나 검증 규칙을 완화하지 않았습니다.
- `Tests/Fixtures/content-v6-production.sqlite`는 DATA-02 DB의 바이트 동일 스냅샷이며 이번 `--previous` 기준입니다. production source를 fixture에만 추가한 작업이 아닙니다.
- 기존 **2,288개 content ID·본문·관계 fingerprint**, 기존 어휘/의미/예문 행과 content revision/level/sort_key를 모두 보존했습니다. 사용자 DB 재생성·migration·초기화 없음.
- 신규 ID는 UUIDv4를 한 번 발급해 source에 고정했습니다. 배열 순번/행 번호/단어 해시를 ID로 사용하지 않습니다.
- `Content/data03-ids.json`은 검수 색인, `Docs/DATA03_REVIEW_CATALOG.md`는 원본의 읽기용 추출물입니다. 별도 런타임 vocabulary source가 아닙니다.
- 기존 표에 배치/주제 태그 26개와 출처 3개(자체 편집 + 제한적 국립국어원 확인 2개)를 추가했습니다. 공식 TOPIK·객관적 빈도·추측 발음 필드는 비워 두었습니다.

## 편집 순서와 기존 세트 안정성

기존 repository의 `sort_key,id` keyset 조회와 `VocabularySetCatalog`를 그대로 사용합니다. **새 DATA-03 어휘만** learning_priority 100(동사·부사), 200(형용사), 300(명사·의존명사)을 부여했습니다. 빈도 순위가 아니라 편집 그룹입니다.

새 sort_key는 `힣:data03:100:0000` 형태입니다. 현재 배포된 기존 단어 뒤에 이어 붙인 뒤, 이번 배치 안에서는 일상 활용도가 높은 동작·의사소통·부사부터 학습하도록 했습니다. 끝의 숫자는 편집 순서일 뿐 진도 ID가 아닙니다. **기존 sort_key는 수정하지 않았으며**, 입문 기존 296개/초급 기존 180개의 상대 순서가 그대로 앞부분에 유지되는 것을 테스트했습니다. 향후 배치도 새 키만 배정하고 기존 배포 키를 일괄 재생성하지 마세요.

이미 시작한 세트는 UserProgress의 stable ID membership·현재 회독·공개 상태 그대로 재개합니다. 새 세트만 미배정 ID를 최대 20개 선택합니다. 기존 작은 마지막 세트를 뒤늦게 늘리지 않습니다. DATA-03 전용 회독/SRS를 추가하지 않았습니다. 회독 완료 후 기존 SRS 등록, due 조회, 재등록 시 기존 단계 보존 정책을 사용합니다.

## 자체 검수·의미·일본인 특화

원고 작성 후 production source에서 별도 목록을 추출하여 기본형·품사·불규칙·의미·예문·번역·띄어쓰기·관계·난이도를 다시 읽었습니다. 신규 원고만 교정했으며 이미 배포된 DATA-01/02 레코드는 바꾸지 않았습니다.

- 다의어: 걸리다(시간/질병), 맞다(정답/맞음·적합), 빼다(꺼냄/뺌), 늘다(양 증가/실력 향상), 고치다(수리/수정), 답답하다(감정/공간), 꿈(수면/장래), 뜻(의미/의도) 등 18개. 각 의미에 예문이 있습니다.
- note 48개: 늘다/늘리다, 열리다/열다, 바뀌다/바꾸다, 듣다/들리다, 외우다/기억하다, 잔돈/거스름돈, 괜히·혹시·좀·별로·이미·이따가, 조사 결합과 수사/단위 등을 설명합니다.
- typed 관계 15개: confusable 8, antonym 5, related_word 1, synonym 1. 의미 차이가 있는 자동사/타동사를 무조건 동의어로 만들지 않았습니다. 현재 UI는 관계 목록을 별도 표시하지 않고 설명 note를 사용합니다.
- `적다` 동사「書き留める」는 기존 형용사「少ない」와 다른 항목입니다. 동형 표제어 경고를 유지하고 note로 구분했습니다. 기존 차/일/쓰다/저도 그대로 보존했습니다.
- 하다형은 기존 other(여 불규칙), ㄷ/ㅂ/르는 해당 기본형에만 설정했습니다. ㄹ·으의 규칙적 탈락은 기존 none 정책, 서술어 has_batchim은 null입니다. 졸리다의 상태 형용사 용법과 머무르다의 르 활용은 국립국어원 자료를 확인했습니다.
- 검수 과정에서 걷는 거리 예문의 수식 모호성, 동생 번역의 성별 추정, 개월의 수사, 따라가다 방향, 중복 문장과 불필요한 note를 교정했습니다. 세부 내용·확인 출처는 `Docs/DATA03_REVIEW.md`에 있습니다.

## 실제 검증 결과

- 기존 Production Validator **오류 0 / 경고 10**. 짧은 발음 예시 5 + 동형 표제어 후보 5(차/일/쓰다/저/적다). 규칙을 끄지 않았습니다.
- v6 이전 배포 검사와 SQLite 생성 성공. 검수된 candidate를 `Resources/content.sqlite`에 반영했으며 최종 validate-only 재생성 SHA256도 일치합니다. `Docs/DATA03_BUILD_REPORT.json`, `Docs/DATA03_VALIDATION.json`.
- **Python/SQLite 129개 통과**: 기존 123개 + DATA-03 6개. `Docs/TEST_RESULTS_DATA03.txt`.
- 새 검사: 신규 UUID 전체 조회, 의미별 예문, note/typed 관계, 두 level의 최대 20개 keyset 조회, 편집 순서, 한국어/일본어/제2의미 검색, 품사·불규칙, 기존 v6 전체 payload 보존, 실제 v6→v7 콘텐츠 파일 교체 후 기존 입문/초급 세트·회독·SRS 상태 보존, 새 UUID SRS INSERT/due SQL 호환성.
- 기존 importer/validator·15,000/30,000 synthetic·한글/발음/오디오 정책 SQL·회독·SRS 회귀도 함께 통과했습니다. 테스트 첫 실행에서 신규 배치에 없는 풀다를 지정한 신규 테스트 입력 오류 1개를 바로잡고 전체를 재실행했습니다. Validator를 수정하거나 실패 조건을 완화한 것이 아닙니다.
- **Swift 45파일 tree-sitter 구문 오류 0**. plist/XML·프로젝트 Swift 참조·SQLite integrity/FK 검사 통과. `Docs/STATIC_CHECKS_DATA03.txt`.
- **앱 Swift 40파일 전부 DATA-02와 바이트 동일**. UI/Navigation/Audio/회독/SRS 코드 변경 없음. 파일 삭제 없음.
- Native XCTest는 새 DATA-03 실제 카드→2회독→중단 재개→SRS→due 복습→디스크 재개 테스트 1개를 추가하여 **60개 작성**했습니다. **실행하지 않았습니다.**

**빌드/실행 한계:** Linux에는 Swift compiler/Xcode/iOS simulator가 없습니다. Swift type-check, Debug/Release build, XCTest 실행, UI/VoiceOver/Dynamic Type, 실제 앱 재시작 및 한국어 음성 청취는 미수행입니다. SQLite 통합 검사는 Swift 제어 흐름 실행을 대신하지 않습니다. Mac에서 `TEST_DESTINATION='platform=iOS Simulator,id=실제ID' sh Tools/verify.sh`로 확인해야 합니다.

## 주요 파일

- Content/production.json / Content/data03-ids.json / Resources/content.sqlite
- Tests/Fixtures/content-v6-production.sqlite / Tests/VocabularyPassTests.swift
- Tools/ContentBuilder/test_data03_content.py 및 기존 수치 기대값 테스트 4개
- PROJECT_STATUS.md / DATA_PROGRESS.md / CONTENT_GUIDE.md / README.md
- Docs/DATA03_REVIEW.md / DATA03_REVIEW_CATALOG.md / 검증·테스트·정적검사 로그 / CHANGES_DATA03.md

## 알려진 한계 / 다음 단계

1. 외부 한일 교육 전문가 감수와 실제 TTS 청취는 완료하지 않았습니다. 자체 검수와 Validator 통과가 전문가 인증은 아닙니다.
2. 예문은 일상적인 초급 표현이지만 완전한 controlled vocabulary 문장집은 아닙니다. 모든 등장 어휘/문법이 현 DB의 독립 항목인 것은 아닙니다.
3. 기존 UI는 의미당 예문 한 개를 UUID 순으로 선택합니다. 저장한 두 예문 전체의 표시 순서는 이번 DATA 단계에서 바꾸지 않았습니다.
4. DATA-04 시작 시 **현재 v7 DB를 보관하여 --previous**로 지정하고 content 8 이상으로 올리세요. 새 ID만 추가하며 기존 세트/회독/SRS snapshot을 다시 계산하지 않습니다.
5. 새 동의어/혼동어 관계는 방향을 명시한 source/target 한 행입니다. 자동 역방향 복제나 신규 관계 UI는 추가하지 않았습니다.
6. 기존 과거 문서의 수치는 단계별 이력입니다. 현재 집계는 DATA_PROGRESS.md와 v7 DB를 기준으로 합니다. 새 TODO/FIXME 마커 없음.
