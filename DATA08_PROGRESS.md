# DATA-08 진행 기록

## 목표·범위

- DATA-08 전체 목표: **신규 Vocabulary 800~1,200개 / 신규 문장 Example 1,300~2,000개**. 이 목표를 임의 축소하지 않는다. 기존 항목·관계 추가·중복·fixture를 신규 수량에 포함하지 않는다.
- 이번 **DATA-08-1은 상태 확인과 기록만** 수행한다. 신규 콘텐츠 0, 기존 콘텐츠 수정/삭제/비활성화 0, Production DB 교체 0, 버전 변경 0, 버그 수정 0.
- 기준일: **2026-10-19 (Asia/Tokyo)**. DEV-01~14 / DATA-01~07 원본·코드·테스트·보고서를 보존한다. 아래 결과는 이번 실행에서 확인한 값이며 과거 보고서의 통과 결과를 전재한 것이 아니다.
- 기계 판독용 집계·ID 검증·SHA 근거: [Docs/DATA08_BASELINE.json](Docs/DATA08_BASELINE.json).

## 1. Git 및 DATA-08 기존 반영 조사

| 항목 | DATA-08-1 조사 시작 상태 |
| --- | --- |
| 저장소 | `Raccoon26/Project-Hangul-Study` |
| checkout | `/workspace/Project-Hangul-Study` |
| branch | `main`, upstream `origin/main` |
| HEAD / origin/main | `3b40fb9a82d942c91bb7bb57190e6fceaae98e82` |
| 로컬/원격 차이 | fetch 후 ahead 0 / behind 0 |
| 직전 작업 | DATA-07 import `233a5d6`, PR #1 머지 `3b40fb9` |
| 시작 시 tracked 변경 / untracked | 없음 / 없음 (`git status --porcelain=v1 --untracked-files=all`) |
| local branches | main, work, import/hangulstudy-data-07 |
| 원격 branch | origin/main (fetch 후 확인) |
| DATA-08 커밋·파일·본문 | 전체 Git refs/커밋 메시지, 저장소 파일/텍스트에서 발견 없음 |
| DATA-08 DB 흔적 | vocabulary sort_key 0행, sources title/citation 0행 |
| DATA-08 기존 반영량 | Vocabulary 0 / 신규 문장 Example 0 |

`Content/dev08-revised-ids.json`은 **DEV-08** 이력이며 DATA-08 반영분이 아니다. 파일명 검색만으로 반영 여부를 판정하지 않았다. 실제 source와 Production DB가 `Docs/DATA07_DELIVERY.json`의 SHA-256과 각각 일치하므로 현재 데이터는 납품된 DATA-07 그대로다. 현재 접근 가능한 저장소 상태의 결론이며 외부에만 존재하는 초안을 조사한 것은 아니다.

## 2. 문서·코드·배포 경로 대조

`PROJECT_STATUS.md`, `CONTENT_GUIDE.md`, `DATA_PROGRESS.md`, `RELEASE_CHECKLIST.md`, DATA07 검수/납품/수량 기록과 DEV14 요구사항 감사를 읽고 실제 구현과 대조했다.

| 계약 | 실제 근거 / 결과 |
| --- | --- |
| Runtime 원본 | `Content/production.json` → `Tools/ContentBuilder/build_content.py` → `Resources/content.sqlite` |
| 실제 앱 DB | `Services/AppContainer.swift`의 Debug/Release 모두 `content.sqlite`, fixture 허용 false |
| DB 열기 | `Repositories/SQLiteContentRepository.swift` → `SQLiteConnection(readOnly: true)` |
| Bundle 복사 | `Tools/generate_project.py`, `HangulStudy.xcodeproj/project.pbxproj`가 `Resources/content.sqlite`만 선택 |
| Content schema / content version | DB metadata 및 PRAGMA: **4 / 14** |
| Dataset / fixture / locale | **ko-ja-core / 0 / ja → ko** |
| min_reader / 앱 reader | DB **7** / `Content/ContentPackageValidator.swift` **7**, supportedSchema **4** |
| UserProgress | `Persistence/UserDatabaseMigration.swift` currentVersion **10**, migration v2~v10 보존 |
| 신규 DATA-08의 첫 배포 | 후속 콘텐츠 작업에서 현재 v14를 previous로 보존하고 Content15 이상 사용; 이번에는 미실행 |

현재 source/DB SHA-256:

```text
Content/production.json
dcc936ba8f31aba0f6bfd0f47e4199568bd27e71a9c23f0a22731fe7175cf065
Resources/content.sqlite
9293e75ee0161f8fa7688d6ea500f314c8d93fc3f6c9e0284bbf43afec622ac5
```

Source에 선언된 모든 테이블의 전체 행을 DB와 비교해 불일치 0개. metadata 일치. 별도 파생 `vocabulary_search` 2,833행도 현재 표제어·reading·활성 meaning의 정규화 검색어 집합과 일치했다.

문서 안의 DEV별 Content13/Schema3/reader4 등은 과거 기록이다. 최신 DATA-07 머리말과 실제 DB를 우선한다. `RELEASE_CHECKLIST.md`의 123 XCTest 표기는 이전 기준이며 현재 Swift 테스트 메서드 정의는 126개(15개 테스트 파일)다. 전체 Swift 파일은 89개(앱74 + 테스트15). 이는 정적 개수이며 이번 native 테스트 실행 수는 **0**이다. 과거 문서는 이번 단계에서 수정하지 않았다.

## 3. 실제 Production 수량 및 level 분포

`Resources/content.sqlite`를 SQLite `mode=ro`로 열어 직접 집계했다. fixture·임시 DB·관계 행을 콘텐츠 신규 수량에 합산하지 않았다. `content_items` **6,552개 전부 active**이므로 아래 전체 수와 활성 수는 같다.

| Level | Vocabulary | Example 전체 | 문장 Example¹ | Grammar | Listening | Question |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| hangul | 0 | 0 | 0 | 0 | 0 | 59 |
| intro / 入門 | 306 | 659 | 646 | 22 | 34 | 156 |
| beginner / 初級 | 800 | 1,577 | 1,577 | 20 | 79 | 134 |
| lower_intermediate / 初中級 | 270 | 540 | 540 | 0 | 2 | 5 |
| intermediate / 中級 | 0 | 0 | 0 | 0 | 0 | 0 |
| upper_intermediate / 中上級 | 0 | 0 | 0 | 0 | 0 | 0 |
| advanced / 上級 | 0 | 0 | 0 | 0 | 0 | 0 |
| master / マスター | 0 | 0 | 0 | 0 | 0 | 0 |
| maintenance / 維持学習 | 0 | 0 | 0 | 0 | 0 | 0 |
| **합계** | **1,376** | **2,776** | **2,763** | **42** | **115** | **354** |

¹ 문장 Example = `pronunciation_examples`에서 참조되는 발음 예시 13개를 제외한 수. 해당 13개는 모두 intro다. level은 각 엔티티 자신의 `content_items.level`이며 일본어 공식 등급/TOPIK 환산이 아니다. hangul Question 59개가 Example 59개를 뜻하지 않는다. maintenance는 별도 신규 콘텐츠가 없어도 기존 기록 기반 유지학습이 동작하므로 0을 기능 부재로 해석하지 않는다.

추가 집계:

| 항목 | 실제 수 / 설명 |
| --- | --- |
| Meanings / Learner notes | 1,457 / 217 |
| Vocabulary-example 관계 / 고유 연결 Example | 2,692 / 2,686; 관계 수와 고유 예문 수를 구분 |
| Grammar-example 관계 | 123 |
| Content links / sources | 806 / 15 |
| Courses / Lessons / Lesson items | 4 / 38 / 226 |
| Hangul / Pronunciation rules | 55(조합 설명 포함; 현대 자모40은 기존 이력) / 36 |
| Question 유형 | multiple_choice 174 / text_input 65 / listening_choice 86 / listening_input 29 |
| 직접입력 mode (text_input 65) | form 59 / blank 3 / sentence 3 |
| Listening task (115) | meaning 32 / korean 27 / dictation 29 / comprehension 27 |
| Listening audio | tts 115 / 녹음 asset 사용 0; media_assets 전체 0 |
| Conjugations 테이블 | 0; 실제 활용은 기존 Swift 엔진과 Question rubric으로 처리하므로 기능 부재와 다름 |
| Vocabulary 품사 | noun462 / verb464 / adjective196 / adverb146 / expression59 / bound_noun19 / pronoun14 / numeral10 / determiner6 |

주요 재현 SQL (table은 위 다섯 상세 테이블 중 하나):

```sql
SELECT i.level, COUNT(*) AS total, SUM(i.is_active) AS active
FROM vocabulary AS x JOIN content_items AS i ON i.id=x.id
GROUP BY i.level;

SELECT i.level, COUNT(*) AS sentences
FROM examples AS e JOIN content_items AS i ON i.id=e.id
WHERE NOT EXISTS (
  SELECT 1 FROM pronunciation_examples AS p WHERE p.example_id=e.id
)
GROUP BY i.level;

SELECT * FROM content_metadata;
PRAGMA user_version;
PRAGMA integrity_check;
PRAGMA foreign_key_check;
```

## 4. Stable ID·기존 데이터 보존·중복 확인

- content_items ID **6,552개/고유 6,552개**, canonical UUID 위반 0. revision 분포: 1=6,387 / 2=155 / 3=8 / 4=1 / 5=1.
- `Content/*ids.json` 18개에서 UUID 참조를 추출해 content_items/sources/media_assets와 대조: 미해결 참조 0. 상세 파일별 결과는 baseline JSON에 기록했다.
- Content13 fixture의 기존 ID 4,663개 중 삭제 0. signature 변경 30개는 `Content/data07-revised-ids.json` 승인 목록과 정확히 일치한다. 기존 payload/관계/버전 정책은 strict previous gate와 기존 DATA07 회귀 테스트로 재확인했다.
- Content13→14 증가는 어휘450 / 의미475 / 예문900 / 문법0 / 듣기4 / 문제12. 이는 **DATA-07 증가분**이며 DATA-08 실적으로 재계산하지 않는다.
- 기존 표제어 중복 후보 5그룹: **저 / 차 / 일 / 쓰다 / 적다**. 기존 동형/의미 구분 기록을 유지하며 자동 병합·삭제하지 않았다.
- 한국어 문장 NFC·앞뒤 공백·casefold 기준 중복은 기존 **4그룹/8행**: `한국에 처음 왔어요.`, `매일 한국어를 공부해요.`, `표를 미리 샀어요.`, `이 정도면 충분해요.`. 각 ID는 모두 Content13에도 존재하며 일본어 번역이 다르다. 새 DATA-08 중복이 아니며 이번에는 보존한다. 후속 제작은 한국어 문자열 후보와 한일 쌍을 모두 비교하고 같은 쌍이면 기존 ID를 재사용한다.
- 기존 Validator 경고 10개 = 발음용 한 글자 예시의 짧은 문장 5건 + 위 표제어 중복 후보 5건. 새 경고를 숨기기 위한 Validator 완화나 데이터 제거는 하지 않았다.

## 5. P0/P1 및 기타 발견 사항

| 구분 | 확인 사실 / 영향 | DATA-08-1 처리 |
| --- | --- | --- |
| P0 확인 범위 | 이번 read-only 무결성·strict validation·portable 232개에서 미해결 데이터 손실/손상 P0를 재현하지 않음 | native 미실행이므로 제품 전체 P0 부재를 보증하지 않음 |
| P1: retirement resume | 기존 vocabulary/grammar active review에 자동 skip/reconcile 없음. 메모리 복제 DB에서 vocabulary ID를 비활성화하면 실제 `SQLiteReviewProgress` due SQL은 ID를 반환하지만 `SQLiteVocabularyContent` active-card SQL은 0행. `ReviewViewModel.loadCard`는 오류 경로로 연결됨. Grammar도 active-card guard 및 오류 처리 확인 | **기존 P1 재확인**, Production 변경 없이 SQL 재현. Swift/UI 실행 재현은 아님. 후속 별도 수정/테스트 필요; 이번 삭제/비활성화 0 |
| P1: native 출시 gate | Xcode/Swift compiler 없음. SDK resolve/link, Debug/Release build, XCTest, UI/TTS/VoiceOver/알림/광고/StoreKit/iPhone offline·중단 재개 미실행 | 기존 **B — Conditional**, 제출 승인 아님. Mac/iPhone에서 RELEASE_CHECKLIST 수행 필요 |
| P1: 콘텐츠 연계 부족 | 初中級 vocabulary270/examples540이나 grammar0/listening2/question5. 중급·중상급·상급·마스터도 위 주요 콘텐츠 0 | 후속 콘텐츠 확대 필요. DATA-08-1에서는 추가하지 않음 |
| 내용 품질 검수 한계 | 외부 한국어/일본어 교육 전문가 감수·기기별 normal/slow 음성 청취 미실행 | 자동 검증을 언어 정확성 인증으로 표현하지 않음 |
| 임시 DB 혼동 위험 | tracked `Resources/.content-pcb7fgvn.sqlite`도 Content14/schema4이나 Production과 다름. ID 집합 동일, 어휘227행의 has_batchim 및 그중92행 irregular_type 차이; shared signature227개 차이 | source/Production이 기준. 앱/generator는 이 파일을 선택하지 않음. 기존 파일은 삭제/교체하지 않으며 DATA-08 반영분으로 계산하지 않음 |
| 문서 버전 혼재 | CONTENT_GUIDE의 과거 버전과 RELEASE_CHECKLIST의 123 native 테스트 수가 최신 코드126개와 다름 | 현재 기준을 이 기록에 분리. 역사 문서와 gate 체크박스는 보존 |
| 기존 P2/운영 gate | legacy retry 통계 역분류, lifetime event scan 비용, 기기 접근성/성능, Bundle ID/Team/Icon/ASC/privacy 설정 | 이번 성능·실기기 검증은 미실행, 해결됐다고 표시하지 않음 |

Production AdMob ID가 비어 광고 비활성인 현재 설정은 기존 정책상 허용된다. 필수 학습을 막는 환경 오류로 취급하거나 임의 ID로 채우지 않았다.

## 6. 부족한 콘텐츠 영역: 실제 데이터와 범위

- 문법은 intro22/beginner20, 初中級 이상 0. 기존42개 pattern에는 **-다 보니 / -느라 / 간접화법**을 설명하는 독립 문법 항목이 없다. 예문에 나온다는 이유로 학습 설명이 갖춰졌다고 계산하지 않는다.
- 初中級 듣기2개는 dictation/comprehension 표본이며 별도 의미선택·한국어선택 확장이 필요하다. 전체115개가 TTS이며 검증 녹음·긴 대화·상위 단계 콘텐츠가 부족하다.
- 직접입력65개 중 단순 form59개, blank3개·sentence3개다. 신규 어휘 전부의 산출/문법/듣기 적용을 커버하지 않는다. 자유작문 채점/전체 활용 예외/상급 진단을 완료 상태로 표시하지 않는다.
- 어휘는 의료·공공서비스·주거/계약·학습활동·취미의 실제 상황 확장이 필요하다. 모든1,376개에 theme/source 관계는 있으나 theme는 DATA별 편집 분류이므로 특정 theme의 부재를 해당 분야 전체0으로 해석하지 않는다.

다음은 DB `vocabulary.headword = ?`의 정확일치 표본 조사다. **후속 후보 검토 근거이며 이번 신규 제작 목록이 아니다.** 해당 표제어가 없더라도 비슷한 표현/의미/예문이 있을 수 있으므로 후속 Batch에서 의미 중복 검토가 필요하다.

| 영역 | 기존 표제어 있음 | 표본 중 정확일치 없음 |
| --- | --- | --- |
| 의료 | 병원·약국·진료·증상 | 처방전·접수·건강보험·알레르기 |
| 공공서비스 | 우체국·은행·신청서 | 주민센터·민원·증명서·발급·신분증 |
| 주거/계약 | 집·보증금·관리비·이사 | 월세·전세·임대차·계약서 |
| 학습/활동 | 공부하다·수업·장학금·동아리·졸업하다 | 전공·자격증·수강하다 |
| 구체적 취미 | 운동하다 | 취미·등산·촬영·악기·전시회·낚시·뜨개질 |

## 7. 이번 실행한 검증

실행 환경: Linux / Python 3.12.14 / 표준 sqlite3. 신규 콘텐츠 제작·Production build 교체 없이 실행했다.

| 검사 | 이번 결과 |
| --- | --- |
| Production `PRAGMA integrity_check` | `ok` |
| Production `PRAGMA foreign_key_check` | 0행 |
| 전체 source metadata/table rows 대조 | 불일치0 |
| 파생 검색어 집합 대조 | 일치 (2,833행) |
| DATA07 source/DB 납품 SHA-256 대조 | 모두 일치 |
| UUID / manifest 참조 / 이전 ID 보존 | 비정상 UUID0 / 미해결0 / 삭제0 |
| strict Validator, Content13 previous | exit0 / errors0 / 기존 warnings10 |
| `sh Tools/verify.sh --portable` | exit0 / **232 tests PASS**, 71.783초, 실패·skip·expected failure 보고 없음 |
| monetization 검사 (portable에 포함) | PASS, production IDs absent → ads disabled |
| 기존 native tests | 정적 정의126개 / **이번 실행0개** |
| Swift syntax/type-check·iOS build·실기기 | 이번 미실행 (과거 DATA07 parse 결과를 이번 실행으로 기록하지 않음) |

프로젝트 루트에서 이번 strict 검증 명령:

```sh
python3 Tools/ContentBuilder/build_content.py Content/production.json \
  --validate-only --production \
  --previous Tests/Fixtures/content-v13-production.sqlite \
  --report /tmp/data08-validation.json
sh Tools/verify.sh --portable
```

위 previous v13 명령은 **현재 DATA-07/v14의 재검증용**이다. 새 DATA-08 배포 때 이를 그대로 이전 버전으로 쓰지 말고 실제 직전 배포(v14 이상)를 사용한다. validate-only는 임시 DB에서 검사하므로 번들 DB를 교체하지 않는다. 임시 원시 로그는 `/tmp/data08-{validation,portable}.log`, 검증 결과 요약은 baseline JSON에 보존한다.

## 8. DATA-08 단계별 누적 원장

| 단계 | 신규 Vocab / 문장 Example | 누적 DATA-08 Vocab / 문장 | 검수·검증 | 버그 | Git 스냅샷 |
| --- | ---: | ---: | --- | --- | --- |
| DATA-08-1 | **0 / 0** | **0 / 0** | 실제 수량·ID·해시·FK·source 대조, strict0errors/10warnings, portable232PASS | 기존 retirement P1 재확인; 신규 수정0; 임시DB 차이 기록 | 시작 main=`3b40fb9`, clean, origin과 일치. 산출물은 AGENTS.md·이 문서·baseline JSON만 |

전체 목표 대비 남은 신규량: **어휘800~1,200 / 문장1,300~2,000**. 목표 범위 달성 시 누적 Vocabulary는2,176~2,576, 문장 Example은4,063~4,763(발음 예시 유지 시 전체 Example4,076~4,776). 후속 배치에서 실제 증가로 재계산하며 이번 단계 달성량으로 표시하지 않는다.

후속 각 단계는 아래 양식을 복사해 누적하고, 위 원장과 실제 DB 수량을 갱신한다.

```text
단계/Batch / 날짜 / 조사 또는 반영 범위:
시작 Git branch·HEAD·upstream 차이·tracked/untracked 상태:
시작 source/DB SHA·dataset·schema/content/minReader/UserProgress:
previous release 경로·버전·SHA (배포 갱신 시):
시작→종료 Vocab/Meanings/전체Examples/문장Examples/Grammar/Listening/Questions:
실제 신규·기존 수정(revision 승인ID)·재사용 관계·비활성화·삭제:
Level별 증가와 누적 DATA-08 목표 대비 잔여량:
Batch 검수 주체·전체 검수 범위·한일 품질 수정·중복 후보와 판단 근거:
ID/FK/source↔DB/previous strict/경고·테스트 실행 수와 exit status:
부분 session·SRS·검색/상세/즐겨찾기·통계·3~10분·offline 통합 결과:
P0/P1 등 버그 재현·수정 여부·재검증·미실행 native/실기기 gate:
종료 Git 변경 파일·commit/PR/merge·upstream 차이·잔여 작업:
```

## 9. 이번 변경 범위와 전달 상태

- 새 `AGENTS.md`: 기존 요구 보존, 고정 DATA-08 목표, Batch 검수, 한일 품질, Stable ID/DB 무결성, 통합검사, 3~10분 학습, Offline-first 규칙을 기록했다.
- 새 `DATA08_PROGRESS.md`와 `Docs/DATA08_BASELINE.json`: 이번 상태 확인과 후속 기록 양식/기준을 저장했다.
- 기존 tracked 파일의 수정·삭제 없음. App/Content/Resources/Tests/Tools, Xcode 프로젝트, 기존 문서와 DB를 보존했다. 신규 단어·예문·ID 발급, v14 fixture 생성, 버그 수정은 하지 않았다.
- 위 Git 원장은 조사 시작/문서 작성 시점 스냅샷이다. 이 단계 산출물의 최종 커밋은 `git log --oneline -- AGENTS.md DATA08_PROGRESS.md Docs/DATA08_BASELINE.json`으로 확인한다. 작업 전달 시 commit/PR/merge 결과와 종료 Git 상태를 함께 보고한다.
