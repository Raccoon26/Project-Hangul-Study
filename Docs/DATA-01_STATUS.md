# PROJECT_STATUS — DATA-01

DEV-01~04의 구조를 유지하고 실제 입문 어휘를 추가했습니다. 이전 상태는 `Docs/DEV-04_STATUS.md`에 보존했습니다. 사용량 제한으로 중단된 뒤 작성된 원본·DB·테스트 결과를 확인하고 이어서 마무리했습니다. 미완성 레코드를 넣거나 목표 개수를 맞추기 위해 fixture를 production으로 바꾸지 않았습니다.

## 이번 결과

| 항목 | DATA-01 추가 | 현재 production 누적 |
| --- | ---: | ---: |
| 어휘 | 226 | 226 |
| 의미 | 244 | 244 |
| 완전한 한국어·일본어 문장 쌍 | 447 | 447 |
| 기존 발음 단어/짧은 예시 | 0 | 13 |
| examples 테이블 전체 | 447 | 460 |
| 어휘→예문 관계 | 452 | 452 |
| 일본인용 learner note | 65 | 68 |
| 문법 항목 | 0 | 0 |

각 어휘에 예문 2개, 모든 의미에 최소 1개를 연결했습니다. 동일한 한국어·일본어 문장 쌍 5개는 하나의 example ID를 공유하므로 452개의 어휘-예문 연결이 447개의 고유 문장을 가리킵니다. 18개 어휘는 두 의미로 분리했습니다. 226개는 동형이의어를 별도 어휘로 센 수이며 고유 표제어 문자열은 223개입니다.

**`Content/production.json` → 기존 Importer/Validator → `Resources/content.sqlite` 반영 완료.** Content version만 **4→5**로 올렸고 **schema=3 / reader=4 / UserProgress schema=3**을 유지했습니다. dataset=ko-ja-core, is_fixture=0입니다.

## 선정·품질 결정

- 사람/관계/자기소개 20, 장소 20, 집/일상 20, 음식/음료 20, 시간/날짜 20, 학교/직장/활동 15, 이동/위치 15, 기본 동사 35, 상태/감정 25, 의문/부사 20, 수량/숫자 10, 기본 동작/상태 보완 6.
- 사람·친구·집·학교·회사·물·밥·오늘·내일·가다·오다·먹다·마시다·좋다·크다·작다·많다·조금 등 일상 입문어 중심입니다. 준비·약속·공부·시간·운동 같은 한자어도 포함합니다.
- 전부 editorial level `intro`입니다. TOPIK 등급, 빈도 순위, 학습 우선순위, 미검증 발음 표기는 null로 두었습니다. 공식 필수어 목록이라고 주장하지 않습니다.
- 밥(炊いた米/食事), 아침(朝/朝食), 저녁(夕方/夕食), 찾다(探す/見つける), 일어나다(起きる/立ち上がる), 좋다(よい/好き), 아프다(痛い/具合が悪い) 등을 의미별로 분리했습니다.
- 일본어는 상황에 맞게 자연스럽게 번역했습니다. 약을 먹다는「薬を飲む」, 집에 가요는 귀가 문맥에서「家に帰ります」입니다. 동생은 성별이 명시되지 않으므로 일부 일본어 예문의「弟」는 문맥 선택임을 note/learning_point에 설명했습니다.
- 한국어 문장 길이는 공백·문장부호 포함 6~19자입니다. 질문·부탁·진술·부정·과거·짧은 이유 표현 등을 섞었으며 모든 예문을「저는 X를 좋아해요」틀로 만들지 않았습니다.
- 품사는 기존 enum 그대로입니다. 어떻게를 독립 부사 기본형으로 등록하지 않고 **어떻다(adjective)**의 활용형으로 다룹니다. 기본형·예문·설명을 함께 수정했습니다. 잘의 예문은 합성 동사 잘하다와 혼동하지 않도록「글씨를 잘 써요」로 교정했습니다.
- 동사/형용사 불규칙: 듣다·걷다=d, 모르다·빠르다=reu, 쉽다·어렵다·덥다·춥다·뜨겁다·차갑다=b, 어떻다=h. 하다 및 -하다 용언은 여 불규칙을 기존 `other`로 기록합니다. 전용 enum/schema를 새로 만들지 않았습니다.
- 닫다·씻다·입다·좋다 등 규칙 활용은 none입니다. 으/ㄹ 탈락처럼 규칙적인 변화도 none이며 활용형이 항상 그대로라는 뜻은 아닙니다.
- 비서술어 has_batchim은 표제어 마지막 음절의 철자상 받침입니다. 동사/형용사는 어간 받침과 사전형 마지막 다를 혼동하지 않도록 null로 두었습니다. 자동 활용 엔진은 이 필드에서 어간 받침을 추측하면 안 됩니다.
- 음원·TTS 정책과 기존 발음 과정은 변경하지 않았습니다. 이번에는 신규 발음 표기나 audio 행을 추측해서 추가하지 않았습니다.

## 중복·자체 검수

DEV-04에 vocabulary는 0개였습니다. 전체 신규 어휘를 이전 production과 비교했으며 기존 과정의 한글/발음 항목을 단어 중복으로 삭제하지 않았습니다.

| 경고 표제어 | 유지한 항목 | 결정 |
| --- | --- | --- |
| 차 | お茶 / 車 | 같은 품사의 동형이의어, 서로 다른 영구 ID |
| 일 | 日(bound_noun) / 仕事(noun) | 다른 품사·의미, 서로 다른 영구 ID |
| 쓰다 | 書く / 使う | 같은 품사의 동형이의어, 서로 다른 영구 ID |

완전히 같은 단어·품사·의미의 불필요한 중복은 0개입니다. 3개 그룹은 confusable 관계와 학습 설명으로 구별합니다. `DATA01_REVIEW_CATALOG.md`에 전체 어휘·의미·예문·설명을 모아 별도 재검수했습니다. 한국어/일본어, 의미별 예문, 날짜 표기, 품사, 활용 분류, 반복 문장과 관계 ID를 확인했습니다. **자체 검수이며 외부 한국어 교육 전문가/일본어 편집자의 감수 완료를 의미하지 않습니다.**

## 영구 ID와 기존 콘텐츠 보호

UUID를 한번 발급해 원본과 `Content/data01-ids.json`에 보존했습니다. 이 파일은 편집 색인이며 새 Importer 포맷이 아닙니다. 텍스트·정렬 순서·rowid에서 ID를 재계산하지 않습니다. 신규 source에 재정렬을 적용해 다시 build해도 의미 fingerprint가 같음을 테스트했습니다.

DEV-04의 225개 기존 콘텐츠는 ID, revision, payload, 관계 fingerprint가 모두 같습니다. 기존 2개 course/26개 lesson/184개 step, 40개 현대 자모, 발음 36페이지, 90개 quiz를 보존했습니다. Swift/UI/Audio/Progress, SQL 스키마, Importer/Validator 코드는 변경하지 않았습니다.

콘텐츠 v5 교체는 사용자 DB를 열거나 수정하지 않습니다. 기존 정책상 content version이 바뀌면 진행 중 lesson은 재시작 안내가 나올 수 있으나, 과거 답안·완료 수·즐겨찾기는 유지됩니다. 이번 DATA 작업에서 이 재개 정책을 변경하지 않았습니다.

## 검증 결과

실제 실행:

- 기존 Validator `--production --validate-only --previous content-v4-production.sqlite`: **오류 0 / 경고 8**.
- 경고 5개는 DEV-04의 의도된 한 글자 발음 예시(꽃/花, 밭/畑, 밥). 신규 3개는 위의 동형어 후보. 검증 규칙을 끄거나 경고를 숨기지 않았습니다.
- 검증한 source로 production DB 생성 및 SQLite integrity_check=ok / foreign_key_check 빈 결과.
- Python **92개 통과(13.487초)**: 기존 80개 회귀 + DATA-01 12개. 최종 문구 수정 후 다시 실행한 결과입니다.
- 실제 Swift repository SQL의 50개 keyset pagination으로 226개를 중복/누락 없이 조회했습니다. intro level, 품사, vocabulary→meanings/examples, UUID 직접 조회, 한국어/일본어/두 번째 의미 접두어 검색도 확인했습니다.
- 잘못된 ID/필수 필드/품사/level/빈 번역/관계/고아 예문 입력 거부를 확인했습니다. 이전 진도 SQL·콘텐츠 분리·한글/발음/TTS 정책 테스트와 15,000 어휘·30,000 예문 synthetic 회귀를 포함합니다.
- DEV-04 대비 42개 런타임/스키마/프로젝트/Importer 파일이 byte-identical. Info.plist/scheme/workspace XML 파싱 확인.
- Xcode 프로젝트의 실제 DB 복사 shell phase만 임시 디렉터리에서 실행: Debug/Release 모두 content 5 / schema 3 / 226어휘 production DB를 복사했습니다.

미실행:

- 환경에 Swift/Xcode가 없어 **iOS 빌드, Swift 타입 검사/링크, XCTest 29개 실행, 시뮬레이터/실기기 UI, 실제 음성 출력은 확인하지 못했습니다**.
- 동일 SQL을 Python에서 실행한 것을 Swift 앱 실행 결과로 표시하지 않습니다. 이번에는 Swift를 수정하지 않았고 새 Swift 구문 검사도 별도로 수행하지 않았습니다.

## 앱에서 보이는 범위·제한

기존 `単語` 탭이 새 production 단어를 50개씩 읽고 상세에서 일본어 대표 의미·품사·예문을 보여주는 구조입니다. UI 수정은 없습니다. 전체 의미 목록, learner_notes/learning_point, 태그·품사 검색 UI는 기존 화면에 아직 연결되지 않았습니다. 데이터는 저장·조회 가능한 상태이며 이 표시 확장은 후속 DEV에서 진행해야 합니다.

입문 어휘 course/단어 quiz/SRS를 이번 데이터 작업에서 새로 만들지 않았습니다. 입문자는 기존 단어 목록/상세로 자료를 볼 수 있습니다. 일부 예문에는 이 배치 밖의 기초어·표현도 등장하며, 226어휘만으로 모든 문장을 해독할 수 있는 폐쇄형 어휘집은 아닙니다. 숫자/요일/계절도 완전한 표가 아니라 첫 배치이므로 DATA-02에서 보강합니다.

## 변경·추가 파일 및 인계

- `Content/production.json`, `Content/data01-ids.json`, `Resources/content.sqlite`
- `Tests/Fixtures/content-v4-production.sqlite`: DEV-04 배포 기준 보존
- `Tools/ContentBuilder/test_data01_content.py`: 새 release gate
- `Tools/ContentBuilder/test_pronunciation_content.py`: 누적 content version/검토된 경고의 기대값만 갱신, 검사 유지
- `DATA_PROGRESS.md`, `CONTENT_GUIDE.md`, `README.md`, `Docs/VALIDATION.md`
- `Docs/DATA01_REVIEW_CATALOG.md`, `Docs/DATA01_REVIEW.md`, `Docs/DATA01_VALIDATION.json`, `Docs/DATA01_BUILD_REPORT.json`, `Docs/TEST_RESULTS_DATA01.txt`, `Docs/STATIC_CHECKS_DATA01.txt`

다음 DATA는 **현재 v5 DB를 이전 배포로 보존**하고 --previous에 지정합니다. 현재 source 전체에 새 자료를 추가하며 기존 ID와 tombstone 원칙을 지킵니다. 신규 DATA 때문에 schema version을 임의로 올리지 마세요. 외부 감수/실기기 표시 확인과 기존 능동 세션의 버전 변경 안내는 후속 확인 사항입니다. 새 TODO/FIXME 코드 마커는 없습니다.
