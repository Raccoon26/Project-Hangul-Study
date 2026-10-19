# DATA-08-8 최종 검증·전달 보고

**DATA-08의 수량·콘텐츠 통합 목표 달성. B—Conditional 유지: 미실행 native·사람 검수 조건을 완료로 표시하지 않는다. DATA-09는 시작하지 않았다.** 이번 단계는 최종 확인·문서·산출물 보존 정책 작업이며 Production 본문/ID/revision/버전/Runtime/UserProgress 변경0이다.

## 1~7단계 결과 재대조

시작은 clean main/origin/main `4cf64ca3b1ac496193033ee7a04d63ad1ee46379`(PR #8)였다. 각 보존 DB를 read-only로 열어 당시 보고 수량을 대조하고, 현재 ID와 A/B/C registry를 비교했다. 아래 PASS 수는 당시 로그의 결과이며 이번 실행 수로 합산하지 않는다.

| 단계 | 실제 근거 | 검증된 결과 / 당시 portable |
| --- | --- | --- |
| 1 상태 조사 | v14 fixture·BASELINE | V1,376/E2,776, Content14, 추가0; 당시232 PASS |
| 2 Batch A | v15 fixture·A ID registry | 신규 V301(일반261/표현40), E602; 당시243 PASS |
| 3 Batch B | v16 fixture·B ID registry | 신규 V300(일반266/표현34), E600; 당시255 PASS |
| 4 Batch C | v17 fixture·C ID registry | 신규 V310(일반280/표현30), E619, 기존1 재사용; 당시269 PASS |
| 5 전체 품질 감사 | v18 fixture·FINAL_COUNTS/EDITORIAL/SAMPLES | 신규 수량 증감0,34어휘/43필드 교정·40 ID revision; 당시280 PASS |
| 6 Production 통합 | 현재 v19·INTEGRATION_COUNTS | 신규 Course1/Unit tag3/Lesson47, 듣기1,821/활용581/문장입력581; 당시291 PASS |
| 7 요구사항 감사 | 현재 v19·SYSTEM_RESULTS | Content/Schema 변경0, P1 세 건 코드 수정; 당시301 PASS |

최종 신규 **Vocabulary911 = 일반807 + 표현104 / Meaning963 / 고유 문장 Example1,821 / Note314**. A/B/C 모두 어휘270~400 / 예문450~650 가이드 안에 있다. 원래 전체 목표 **800~1,200 / 1,300~2,000**를 유지하며 부족0/0. 표현을 제외한 일반 어휘807도800개 이상이다. 문장 placement1,822 중 기존 문장1개 재사용은 신규에서 제외했다. 전체 v14→19 Vocabulary/Example ID 차집합이 registry의911/1,821와 정확히 같고 신규 Batch 간 ID 교집합0이다.

기존 v14 Stable ID/kind/created_at, vocabulary sort_key, listening learning_order, lesson membership을 모두 보존했다. 현재 비활성 엔티티0. Source 25테이블63,159행과 전체 DB 필드가 일치하며 검색 index 등 파생 테이블도 재구성 비교에 포함했다. 상세 전수 검사 [CLOSEOUT.json](DATA08_CLOSEOUT.json), [ROUTING](DATA08_CLOSEOUT_ROUTING.json).

## 전체 Production·Level

| Level | Vocabulary | Meaning | Example(문장) | Grammar | Listening | Question | Course / Lesson |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 한글 | 0 | 0 | 0(0) | 0 | 0 | 59 | 1 / 12 |
| 入門 / intro | 306 | 327 | 659(646) | 22 | 34 | 156 | 2 / 20 |
| 初級 / beginner | 800 | 847 | 1,577(1,577) | 20 | 79 | 134 | 1 / 6 |
| 初中級 / lower_intermediate | 1,181 | 1,246 | 2,361(2,361) | 0 | 1,823 | 2,988 | 1 / 47 |
| 中級·中上級·上級·マスター·維持学習 각각 | 0 | 0 | 0(0) | 0 | 0 | 0 | 0 / 0 |
| **합계** | **2,287** | **2,420** | **4,597(4,584)** | **42** | **1,936** | **3,337** | **5 / 85** |

추가 실제 DB 수량: content_items15,428 / learner_notes531 / vocabulary_examples4,514 / grammar_examples169 / lesson_items1,137 / vocabulary_search4,707 / sources19 / media_assets0. TTS 듣기1,936이며 녹음 asset 인증은 없다. Level은 내부 콘텐츠 Level이며 TOPIK·공식 일본어 등급이 아니다. 維持学習0은 기록 기반 유지학습 기능 부재를 뜻하지 않는다.

DATA08 신규911어휘는 初中級의 실제1코스·3 Unit tag·47레슨에 각1회 배치되어 모두 도달한다. Unit은 별도 schema 엔티티가 아니라 tag+레슨 제목이다. 기존20개 Set 회독·SRS/검색/사전과 연결한다. 581서술어에 form/sentence 각581문항,1,821고유 예문에 listening/dictation 각1,821항목을 연결했다. 전체3,337문항/4,597예문 중 경로 없는 항목0. 기능별 원본 SQL 경로는 이번 ROUTING으로 재검사했으며 Swift 실행을 대체 인증하지 않는다.

## Production 원본·재생성·대용량 Git

| 구분 | 보존/배포 정책 |
| --- | --- |
| `Content/production.json` (16,638,955 bytes) | canonical UTF-8 Production 원본. 반드시 Git 보존. 임의 삭제·샘플 축소·생성형 대체 금지 |
| `Content/content-schema-v4.sql`, Importer/Validator, ID registry | 원본 재구성 계약과 고정 ID/검수 근거. 함께 보존 |
| `Resources/content.sqlite` (17,932,288 bytes) | 원본에서 재생성 가능한 **실제 앱 번들 DB**. 현재 Xcode가 직접 포함하므로 추적 유지; 생성물이라는 이유만으로 제거하지 않음 |
| `Tests/Fixtures/content-v*-production.sqlite`, `*.json.gz` | strict previous-release 비교/회귀용 불변 snapshot. 현재 원본에서 과거 버전을 대신 생성하지 않음. 모두 보존 |
| `Resources/.content-pcb7fgvn.sqlite` (7,426,048 bytes) | DATA07 import에서 이미 추적된 legacy 임시 DB. 앱 번들 선택 대상이 아님. 이번에 삭제·변경하지 않음; 새 `.content-*`는 ignore |
| 새 후보 SQLite·synthetic·성능 DB·빌드 결과 | `/tmp` 또는 기존 ignored 디렉터리 사용. WAL/SHM·xcresult/xcarchive·새 staging DB는 ignore. Production JSON/배포 DB/fixture를 광범위 ignore하지 않음 |

Importer의 `--production --previous Tests/Fixtures/content-v18-production.sqlite`로 `/tmp/data08-8-rebuilt.sqlite`를 생성했다. **번들·재구성 SHA-256 동일**:

```text
source f97b3bd70d07a3945770b8d6940c4a53e29a9b70b565caf21fb927230c08b4a8
bundle 57aeaf918d5eaaec3bbfaed02f87c5452cca8264540b923a70448b781adbe9e5
rebuilt 57aeaf918d5eaaec3bbfaed02f87c5452cca8264540b923a70448b781adbe9e5
```

DB 전체31테이블(원본·metadata·파생 index·sqlite_stat1)의 모든 열/중복 포함 행, schema/index SQL, integrity/FK 및 binary SHA를 비교해 모두 일치했다. 모든 기존 Content/Resources/fixture 파일을 HEAD byte와 비교해 변경0. 다음 **콘텐츠 변경 배포**의 previous는18이 아니라 실제 현재 Content19 번들이다. 이번은 동일19 재현 검사라18 fixture를 strict 기준으로 사용했으며 버전을 올리지 않았다.

이번 재구성 환경은 Python3.12.14 / SQLite3.53.1 / Linux다. SQLite 버전이 달라 binary가 달라지면 원인을 확인하고 전체 논리 행·schema/index 비교와 별도로 보고해야 하며, SHA 불일치를 조용히 통과 처리하지 않는다.

전체 로컬 Git refs에서 접근 가능한 blob을 `rev-list --objects --all` + `cat-file --batch-check`로 조사했다. 50MiB 초과0 /100MiB 초과0, 최대17,932,288 bytes. 이전 대용량 push 오류의 원문 로그는 현재 근거에 없으므로 원인을 추측하거나 모든 과거 실패를 해결했다고 주장하지 않는다. 현재 도달 가능한 이력과 이번 전달 파일에는 GitHub100MiB 제한 초과가 없다. **Git LFS 불필요**, LFS 도입·이력 재작성·force push·기존 파일 삭제 없음. 향후 커지면 우선 ID 보존 JSONL shard/일반 텍스트 diff 및 생성물 분리를 검토하고, 실제 필요한 대형 원본에 한해 LFS와 checkout/CI/bundle 구성을 함께 검토한다.

## Validator·Build·Test

기존10경고는 짧은 발음 예시의 한일 텍스트5건과 기존 동형 표제어 후보5건이다. 새 중복을 정당화하거나 Validator를 완화하지 않았다.

- **PASS**: strict Importer/Validator 0 errors / 기존10 warnings, 재구성3.2742초, byte-exact SHA·전체31테이블·schema/index 일치, integrity ok/FK0.
- **PASS**: 종료 구조·보존 점검133건, Source25테이블63,159행·기존75개 Content/Resources/fixture 파일 byte 보존, 전체 문항/예문 경로 확인.
- **PASS**: 이번 `sh Tools/verify.sh --portable` **301/301**, 270.967초, failures/errors/skipped/expected failures0, exit0. [이번 원시 로그](DATA08_CLOSEOUT_TEST_LOG.txt). 과거 단계/전용 회귀 수를 중복 합산하지 않는다.
- **BLOCKED**: 이번 `xcodebuild -version` 및 `swift --version` 모두 exit127(command not found). iOS Debug/Release/device-architecture build·SDK link·type-check·native XCTest 정의137개/실행0. UI/오디오/강제 종료/실제 Keychain·StoreKit/AdMob·실기기 성능·메모리/3~10분은 실행0이다.
- **NOT TESTED**: 독립 사람·원어민/교사의 한일 언어·난도 검수. **UNVERIFIABLE**: 원래 DEV/DATA 전체 명세 준수.
- 현재 최종 실행 **FAIL0**. 기존 단계 초기 FAIL/ERROR 로그와 수정 근거는 보존했다. portable 성공을 iOS 빌드나 사람 검수 완료로 바꾸지 않는다.

재현 명령은 프로젝트 루트에서 실행한다(Python3.10+ 표준 라이브러리, 외부 의존성/서비스 불필요). 새 candidate로만 출력하고 기존 번들을 덮어쓰지 않는다.

```sh
python3 Tools/ContentBuilder/build_content.py Content/production.json /tmp/data08-8-rebuilt.sqlite --production --previous Tests/Fixtures/content-v18-production.sqlite --report /tmp/data08-8-build.json
python3 Tools/ContentBuilder/audit_data08_system.py --report /tmp/data08-8-system-audit.json
python3 Tools/ContentBuilder/audit_data08_closeout.py --rebuilt /tmp/data08-8-rebuilt.sqlite --build-report /tmp/data08-8-build.json --system-audit /tmp/data08-8-system-audit.json --report /tmp/data08-8-closeout.json
sh Tools/verify.sh --portable
```

`audit_data08_closeout.py`는 DATA08 고정 보존자료를 재대조하는 종료 감사 도구다.133건은 unittest301개와 다른 구조/보존 점검이며 두 개수를 더해 테스트 수로 보고하지 않는다. setup skill로 확인한 현재 환경에는 Python/SQLite/Git이 이미 있어 추가 설치나 시작 서비스·환경설정 변경이 필요하지 않았다. 새 환경 게시·iOS 준비 완료를 주장하지 않는다.

## 한국어·일본어 품질 범위와 수정 이력

이번 단계는 기존 감사 자료의 payload hash를 재대조했으며 사람 검수를 새로 수행하지 않았다. DATA08-5에서 assistant가 전911어휘/963뜻/1,821고유예문/314 Note를 한국어·일본어 별도 재독했고 Batch/POS/Level 기준84고유 표본을 재감사했다.34어휘43필드를 교정하고40엔티티 revision을 올렸던 기록을 보존한다. 다의어·Collocation·Register·일본인 혼동 Note, 불규칙 분류와 기본형/조사/활용/띄어쓰기·번역·뉘앙스의 실제 검수 근거는 FINAL_REVIEW/EDITORIAL/SAMPLES/RISK_FORMS에 있다. 이는 독립 원어민·교사 검수나 자동 Validator만으로 언어 품질을 보장한다는 뜻이 아니다.163문장의 선행 Grammar/Level/Register 후보는 남아 있다.

수정 버그: (5) 어휘/예문/일본어·불규칙 관련43필드, (6) vocabulary 레슨의 미지원 표시 경로 연결·진단에 初中級 문항 혼입 방지, (7) 비활성 복습 카드 명시적 보류, 받아쓰기 끝 .!? 선택 허용, 듣기 due 퇴역 prefix로 인한 활성 항목 가림. 원래 ID·SRS 일정·session snapshot·통계·구매/설정 저장소를 보존했다. **P1 세 건은 FIXED IN CODE / SQL·corpus PASS / native BLOCKED**다. 이번 단계 새 런타임 버그 수정0. 이전 테스트 seed/기대값 오류와 수정 전 FAIL/ERROR 로그도 삭제하지 않았다.

## 남은 P0/P1·다음 Content Gap

- 실행된 portable/DB 감사에서 **현재 미해결로 재현된 P0/P1은0**. native137개가 미실행이므로 ‘앱에 P0/P1 없음’ 또는 완전한 수정 검증을 뜻하지 않는다. 위 P1 세 건의 실제 ViewModel·판정·기기 회귀는 미완료 gate다.
- 初中級 독립 Grammar0,163문형 선행 학습 확인·Level/Register 보정, 중급 이상 콘텐츠 전부0, 검증 녹음0이 다음 콘텐츠 공백이다. 이번 단계에서 콘텐츠를 생성하지 않았다.
- 파랗다/노랗다 현재·과거 및 빨갛다 과거 dictionary override 부족, mixed Unit 자동 진행/정밀진단/자유작문·직접입력 전용 due queue는 P2/부분 구현으로 유지한다. 고정 회독·레슨의 대량 퇴역은 snapshot을 보존하고 안전 정지하는 기존 제한이 있어 별도 정책 없이 retire하지 않는다.
- 원래 DEV01~14/DATA01~07 전체 사용자 명세 원문은 저장소에서 찾지 못했다.21개 보존 보고서는 확인된 계약의 근거이며 원문 전체 준수 확인을 대신하지 않는다(**UNVERIFIABLE**).
- 다음 행동은 현재137 native XCTest/SDK·Debug/Release build를 Mac에서 실행하고 iPhone의3~10분·한 손·즉시 저장/중단/재개·비행기 모드/TTS/음성중단/접근성/메모리·광고/StoreKit/권한 보존을 검사하며, 독립 사람 언어 검수와163후보를 확인하는 것이다. 이 작업은 **미실행**이다. DATA08의 미완료 조건이 해소되기 전 DATA09를 시작하지 않는다.

## Git 전달

시작 tracked/untracked 변경0을 확인하고 `data08-8/final-closeout` branch에서 작업했다. 기존 모든 Production 원본·DB·회귀 fixture byte와 단계 로그를 보존한다. 최종 diff/크기/테스트 확인 후 일반 commit/push·PR 경로로 전달하며 force push하지 않는다. 이 보고서 자체의 최종 commit/merge SHA·원격 동기화 상태는 Git/PR 및 최종 응답이 기준이다. Git push 실패 시 실제 원인과 필요한 조치를 보고하고 성공으로 표시하지 않는다. App Store 배포·DATA09 착수는 범위 밖이다.
