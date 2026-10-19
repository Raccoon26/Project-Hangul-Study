# DATA-08 진행 기록

> **현재: DATA-08-5 최종 감사 완료 — A~C911어휘·963뜻·고유 예문1,821개·Note314개를 assistant가 재독, 별도 무작위 표본84개 재감사. 34어휘/43필드 교정, Content18 / Schema4 / Reader7 / UserProgress10. portable280PASS. 사람 검수 미실행.** 전체 목표911어휘(일반807/표현104)/신규예문1,821 달성 유지. 선행 문법 후보163문장·native 검증 등 남은 사항은 §13, §1~12는 당시 이력이다.

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
| DATA-08-2 / Batch A | **301 / 602** | **301 / 602** | 전항목 한일 재독, 다의어17/Note68/관계45/문법연결14, strict0errors/기존10warnings, portable243PASS | 초안19항목 교정; 맞추다/맞히다 구분, 조회한도 보존. 기존 P1 유지 | 시작 main=`57bedcc`, clean, 작업 branch=`data08-2/batch-a`; Content14 fixture 보존, 콘텐츠·검수·테스트만 반영 |
| DATA-08-3 / Batch B | **300 / 600** | **601 / 1,202** | 세 묶음 개별재독·중복/UUID/strict gate, Note100/관계72/문법참조15, portable 최종은 §11 | 기본형·품사·조사·번역 초안교정, 기존 P1 유지 | main=`e3f3350`, clean 시작, branch=`data08-3/batch-b`; Content15 원본보존, Content16 배포 |
| DATA-08-4 / Batch C | **310 / 619** (기존 예문1 재사용 별도) | **911 / 1,821** | 세 묶음 한일 재독·UUID/중복/관계/strict0errors·기존10warnings, portable269PASS | 중복1 재사용·관계초안4 제외·품사/번역 교정; 기존 P1 유지 | main=`e7ed775`, clean 시작, branch=`data08-4/batch-c`; 직전 Content16 보존, Content17 배포 |
| DATA-08-5 / 최종 감사 | **0 / 0** (34어휘/43필드 교정) | **911 / 1,821** | 전체911/963/1,821/314 재독·표본84·strict0errors/기존10warnings·portable280PASS | 수혜자 역전·뜻별 결합·관용/번역/편집노출 교정; 선행Grammar 후보163·사람/native 미검수 | 시작 main=`093b215`, clean, branch=`data08-5/final-audit`; 직전17 원본보존,18 배포 |

DATA-08-1 당시 전체 목표 대비 남은 신규량(이력): **어휘800~1,200 / 문장1,300~2,000**. 목표 범위 달성 시 누적 Vocabulary는2,176~2,576, 문장 Example은4,063~4,763(발음 예시 유지 시 전체 Example4,076~4,776). 후속 배치에서 실제 증가로 재계산하며 이번 단계 달성량으로 표시하지 않는다.

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

## 10. DATA-08-2 / Batch A 완료 기록

2026-10-19 (Asia/Tokyo). 이번 요청 범위는 인간관계·감정·부탁/거절·오해/갈등·일상생활·학교/직장의 **初中級 Production Vocabulary와 Example Batch A**다. Batch A 후속 단계는 실행하지 않았다.

### 목표와 실제 승인량

- Batch A 목표270~400어휘 / 450~650예문에 대해 **301어휘 / 602신규문장**을 승인·반영했다. 목표 범위 충족, 품질을 이유로 축소한 수량0. 신규 의미318, 일본인Note68, 명시적Collocation68, 다의어17개(각2meaning).
- 품사: 동사150 / 형용사51 / 부사40 / 실제 회화표현40 / 명사20. 명사6.64%, 비명사281개. 단순 활용형이나 기존 표제어를 새로운 단어로 계산하지 않았다.
- 영역: 인간관계49 / 감정57 / 부탁·거절36 / 오해·갈등57 / 일상생활44 / 학교·직장58. 전부lower_intermediate, 공식TOPIK/빈도/추측발음은null.
- 기존 학습 경로를 사용하는 어휘관계45개, 기존문법14개와 신규예문14개를 연결했다. 새Grammar·Listening·Question은0이며 어휘 배치를 문법/듣기 완성으로 표시하지 않는다.

### Git·버전·이전 배포 보존

| 항목 | 확인 결과 |
| --- | --- |
| 시작 HEAD / origin/main | `57bedcca04831901f31f01c5097b5d387db001d5`, fetch 후 일치 |
| 시작 미커밋 tracked / untracked | 0 / 0 |
| 작업 브랜치 | `data08-2/batch-a` (기존 checkout 사용) |
| 시작 source SHA | `dcc936ba8f31aba0f6bfd0f47e4199568bd27e71a9c23f0a22731fe7175cf065` |
| previous 배포 | `Tests/Fixtures/content-v14-production.sqlite`, 기존 Bundle byte와동일 |
| previous SHA | `9293e75ee0161f8fa7688d6ea500f314c8d93fc3f6c9e0284bbf43afec622ac5` |
| Content / Schema / minReader / UserProgress | **14→15 / 4→4 / 7→7 / 10→10**, dataset ko-ja-core 유지 |
| 기존 콘텐츠 본문·정렬·ID 삭제/변경 | 0 (관계 끝점 revision/updated_at 개정만 별도) |
| 기존 끝점 revision+1 | 23개 = vocabulary9 + grammar14, 승인 목록과 signature 차이 정확히 일치 |
| 신규 content_items ID | 1,295, canonical UUID / 충돌0 |

새 UUID는 한 번 발급해 `Content/data08-a-ids.json`/Source에 저장했다. 기존 source의 행/본문은 보존하고 새 행만 추가했다. `힣:data08:a:NNNN`/priority601은 새 배치의 편집순서이며 기존 sort_key·lesson membership·learning_order·사용자세트를 재정렬하지 않았다. 기존 임시DB는 선택/수정하지 않았다.

### 실제 Production 수량 (fixture 제외)

| 항목 | 시작 | Batch A 증가 | 종료 |
| --- | ---: | ---: | ---: |
| Vocabulary | 1,376 | 301 | **1,677** |
| Meanings | 1,457 | 318 | **1,775** |
| Example 전체 | 2,776 | 602 | **3,378** |
| 문장 Example (발음13 제외) | 2,763 | 602 | **3,365** |
| Grammar | 42 | 0 | **42** |
| Listening | 115 | 0 | **115** |
| Questions | 354 | 0 | **354** |
| Learner notes | 217 | 68 | **285** |
| Vocabulary-example 관계 | 2,692 | 602 | **3,294** |
| Grammar-example 관계 | 123 | 14 | **137** |
| Content links | 806 | 113 (Note68 + 어휘45) | **919** |
| Content items | 6,552 | 1,295 | **7,847** |

| Level | Vocabulary | Example 전체 | 문장 Example | Grammar | Listening | Question |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| hangul | 0 | 0 | 0 | 0 | 0 | 59 |
| intro | 306 | 659 | 646 | 22 | 34 | 156 |
| beginner | 800 | 1,577 | 1,577 | 20 | 79 | 134 |
| lower_intermediate | **571** | **1,142** | **1,142** | 0 | 2 | 5 |
| intermediate / upper_intermediate / advanced / master / maintenance (각각) | 0 | 0 | 0 | 0 | 0 | 0 |
| 합계 | **1,677** | **3,378** | **3,365** | **42** | **115** | **354** |

위 주요 테이블은 전부active다. maintenance 콘텐츠0을 기존 기록 기반 유지학습 기능 부재로 해석하지 않는다. 전체 테이블별 집계와 해시는 `Docs/DATA08_A_COUNTS.json`에 저장했다.

### 개별 검수·수정·실패 기록

작성 후301개/602문장/68Note를 각각 재독하여 한국어 문법·조사·활용·띄어쓰기·자연스러움·level과 일본어 의미·주체·시제·존대·뉘앙스·문체를 대조했다. 검수자는 작성한assistant이고 독립 교육 전문가 승인/음성 감수는 아니다. 전 항목과 ID는 `Docs/DATA08_A_REVIEW_CATALOG.md`, 최종 검수 fingerprint301개는 `Docs/DATA08_A_EDITORIAL.json`에 보존한다.

| 발견 | 처리 / 재검증 |
| --- | --- |
| 초안의 맞추다=正解する 의미 혼동 | 사전 확인 후 맞추다=合わせる/照合する로 교정하고 맞히다=正解する를1개/2문장 추가. 각각 Note/혼동관계 제공. 최종301/602이며 수량축소 아님 |
| 초안 조사의 모호함·어순·지나친 문형·일본어 대응 | 19항목29필드 교정. 의존하다 대상, 탓하다 반복, 준비되다/능숙하다 결합, 메우다 빈자리, 정이 들다의 오독, 불쑥의 주체, 속이 상하다 주어, 평가받다 기본형 등을 수정. 전후값 별도JSON 보존 |
| 후보 assembler KeyError(맞히다) | 실제로 기존DB에 없음을 확인하고 신규 항목으로 개별 작성·검수. Production 반영 전 수정 |
| Grammar 예문 연결15개 중1개가6행조회한도 초과 | 연결1개만 제외해 최종14개. 어휘/예문은 줄이지 않음. 나머지14개 새예문 및 기존예문이 모두 기존 query로 노출됨을 검사 |
| 첫 portable232개 중19실패 | Content14 버전/총수와 이전 revision 기대값이 원인. Content15 정확한 총수 및 이번23개 승인 개정을 반영. 기존 cohort·본문·관계·ID·저장 검사는 보존. 재실행243개 모두PASS |
| Swift XCTest 초안의 품사 모델 가정 | Vocabulary.partOfSpeech가 일본어 표시String임을 확인해 검사 입력/표시값을 구분. 작성 중 수정이며 native 성공으로 기록하지 않음 |

사전 사실 확인: 국립국어원 한국어기초사전의 들르다/서투르다/무리하다/하나하나/맞추다/맞히다 품사·활용·의미. 정확한 URL과 검색404 경로 정정은 `Docs/DATA08_A_REVIEW.md`에 기록했다. 사전의 등급을 추측 TOPIK값으로 쓰지 않았다.

기존/신규의 정규화 표제어 중복0, 신규602개 한국어 문장과 한일쌍 중복0, 기존문장과의 중복0. 이전부터 있던 동형어5그룹/짧은 발음예시 경고는 보존했다. 기존 데이터를 삭제·병합해서 수량을 맞추지 않았다.

### 이번 검증: 실행과 미실행 구분

| 검증 | 실제 결과 |
| --- | --- |
| 승인 후보 strict Validator, previous=Content14 | **errors0 / 기존warnings10**, exit0 |
| 실제 Production Source 빌드 후 승인 후보 대조 | semantic signatures 동일; 검증된 DB만 Bundle 교체 |
| 원본 metadata/모든 입력 테이블과 Bundle 대조 | 불일치0 (기존 build/회귀로 확인) |
| SQLite integrity / foreign keys | **ok / 0위반** |
| 이전ID·본문·관계 보존 / revision | 삭제0 / 본문변경0 / 승인23개만+1 |
| 신규11개 tests 단독 | **11 PASS**, exit0 |
| 최종 portable 전체 | **243 PASS**, 90.952초, exit0, 실패/오류/skip/expected failure0 |
| 새 native XCTest | 번들metadata→들러요/서툴러요/어질러요/너그러워요/맞춰요/맞혀요 검사1개 작성 |
| native 전체 | 정의127개, **실행0**. Swift type-check/Xcode build·SDK link/실기기 미실행 |
| 신규 runtime/UI/엔진/광고/구매 변경 | **0** |

SQL 통합은 모든 새 카드/meaning/예문/Note, 한국어·일본어 보조의미검색, typed relation, 기존14문법의6예문한도와 노출 보존, 初中級571개 bounded pagination/기존270개 sort prefix,20개 세트, SRS중복등록 방지·due5/10/20개를 검사했다. Content14→15 교체 후 실제 임시 User.sqlite bytes와4/20 session snapshot·순서·SRS3skill·favorite·설정·UserProgress10을 보존했다. 이 검사는 앱 UI/Swift 실행의 대체 인증이 아니다.

로컬SQLite·기존 저장/Resume·짧은세션과 광고 경계는 그대로다. 실제3~10분 학습시간, iPhone 비행기모드/TTS/통화·kill/접근성/광고/IAP/알림은 별도 Mac/실기기 gate로 남긴다. retirement active-review P1, 初中級 Grammar0/Listening2/Question5와 상위레벨 공백도 유지한다. 이번 실행 범위에서 남은 confirmed P0를 재현하지 않았으나 전체제품 무결함 보증은 아니다.

재현(프로젝트 루트):

```sh
python3 Tools/ContentBuilder/build_content.py Content/production.json /tmp/data08-a.sqlite --production --previous Tests/Fixtures/content-v14-production.sqlite --report /tmp/data08-a-report.json
sh Tools/verify.sh --portable
```

최종/초기실패/신규 테스트 원시로그는 각각 `Docs/DATA08_A_TEST_LOG.txt`, `DATA08_A_INITIAL_TEST_LOG.txt`, `DATA08_A_NEW_TEST_LOG.txt`에 보존했다. Validator/DB build/실제counts/검수/교정 보고서는 `Docs/DATA08_A_*`를 참고한다.

### DATA-08 전체 목표와 후속 잔여량

**전체 목표800~1,200어휘 / 1,300~2,000문장을 유지**한다. 현재 누적 **301 / 602**, 남은 신규량 **어휘499~899 / 문장698~1,398**. Batch A에서 줄인 부족분은0이고, 이 잔여량은 원래 전체 DATA-08의 후속 단계 몫이다. Batch B나 전체 DATA-08을 완료했다고 표시하지 않는다.

최종 전달은 이 기록의 콘텐츠·fixture·검수자료·회귀 기대값·신규테스트 및 현재 상태 문서만 커밋·푸시/PR/머지한다. 앱 구현·스키마·기존 과거보고서/fixture는 보존한다. 최종 commit/PR은 전달 메시지와 `git log --oneline -- DATA08_PROGRESS.md Content/data08-a-ids.json`으로 확인하고, 전달 직전 작업트리/upstream 상태를 확인한다.

## 11. DATA-08-3 / Batch B 완료

시작 `main/origin/main=e3f335056b354e292e333ce5a681fe8399caea9e` (Batch A PR #3 merge), tracked/untracked 변경0. `DATA08_PROGRESS.md` §10, 상태/제작/누적/출시 문서와 실제 Content15·Batch A source/DB/색인·Swift repository/활용 코드·Git을 대조했다. 작업 branch=`data08-3/batch-b`. 기존 DEV-01~14 / DATA-01~07 / Batch A 결과를 보존했다.

### 실제 증가와 현재 수량

요청 목표270~400어휘/450~650문장에 대해 **初中級 신규300어휘/600문장** 반영. 품질 때문에 줄인 수량0. 100어휘·200문장씩 세 묶음으로 검수했다. 전체 목표 **800~1,200어휘 / 1,300~2,000문장** 유지, A+B 누적601/1,202, 잔여199~599/98~798. Batch B 뒤 단계는 실행하지 않았다.

| 항목 | Batch A 완료 시 | B 증가 | 현재 Production |
| --- | ---: | ---: | ---: |
| Vocabulary | 1,677 | 300 | **1,977** |
| Meaning | 1,775 | 311 | **2,086** |
| 문장 Example | 3,365 | 600 | **3,965** |
| 전체 Example (기존 발음13 포함) | 3,378 | 600 | **3,978** |
| Grammar | 42 | 0 | 42 |
| Listening | 115 | 0 | 115 |
| Question | 354 | 0 | 354 |
| Learner Note | 285 | 100 | 385 |
| Grammar Example 참조 | 137 | 15 | 152 |
| Vocabulary Example 참조 | 3,294 | 600 | 3,894 |
| content_items | 7,847 | 1,314 | 9,161 |

어휘 level: 入門306 / 初級800 / 初中級871. 문장 level: 入門646 / 初級1,577 / 初中級1,742. Grammar22/20/0, Listening34/79/2, Question入門156/初級134/初中級5/한글59. B는 모두 lower_intermediate다. 공식 TOPIK/빈도는 null. 현재 **Content16 / Schema4 / minReader7 / UserProgress10**.

품사: 동사148 / 형용사49 / 부사36 / 회화 표현34 / 명사33(11%). 전300항목 Collocation, 100항목 일본인 Note, 11항목 두 의미/용법 분리, 어휘관계72. 실제 신규문장은600개이며 예문 재사용/관계 증가로 부풀리지 않았다.

### 묶음별 검수·Duplicate Audit·Stable ID·Validator

| 묶음 | 영역 | 어휘/문장 | 의미/Note | 누적 strict 검증 | Duplicate / FK / UUID |
| --- | --- | --- | --- | --- | --- |
| B1 | 의견·판단·추측 | 100/200 | 104/30 | errors0 / 기존warnings10 | 신규중복0 / 위반0 / UUID4 |
| B2 | 비교·선택·계획·경험 | 100/200 | 102/33 | errors0 / 기존warnings10 | 신규중복0 / 위반0 / UUID4 |
| B3 | 원인·결과·영향·변화·개선·문제 해결 | 100/200 | 105/37 | errors0 / 기존warnings10 | 신규중복0 / 위반0 / UUID4 |

각 묶음마다 작성 후 별도 재독, 한국어 조사/활용/문법/띄어쓰기/상황·난도와 일본어 의미/시제/문체를 개별 대조했다. 검수자는 같은 assistant이며 독립 원어민·전문가 승인이 아니다. 각 누적 candidate를 실제 직전 배포 Content15와 strict 비교하고 통과한 후보만 통합했다. B2/B3의 기본형 추가 보정 후 해당 gate도 재실행했다.

NFC·casefold·공백 제거 표제어/한국어·일본어 문장/한일 쌍을 기존전체/A/B 앞 묶음과 대조, 신규중복0. 기존 경고10(발음5/동형어5)은 보존했다. 그르다(형용사), 모자라다/넘치다(동사), 애초/마찬가지/반대(명사), 뒤늦다(형용사) 등은 기본형·품사를 대조했다. 단정하다/뒷받침하다의 주체·목적어, 본래의 부사 용법, 한일 의미 대응·번역·복잡한 구문을 다듬었다. 미치다·대비하다의 조사, 경험하다/겪다/체험하다, 실행하다/실천하다/실현되다, 확대하다/확장하다, 긴급하다/시급하다 등 차이를 Note로 설명했다.

카탈로그300항목/600문장과 검수 fingerprint를 보존했다. 수정 전후49필드/26표제어는 `Docs/DATA08_B_CORRECTIONS.json`의 실제 값을 따른다. 사전 추가검색의 timeout/503을 성공으로 보고하지 않았다. 원문·번역·Note는 자체 작성했다. 사전/음성/공식등급의 이용 권한이나 인증을 추측하지 않았다.

### DB/참조/학습 통합

직전 Content15 fixture SHA=`b4459a400dae7e7b5572688db928a7b550d865f9cf1b3dfd8cd22a86d5d6f75d`를 원본 byte 그대로 보존했다. 기존 v14 fixture/A 색인·검수 산출물도 유지했다. strict 재빌드 source/승인 DB/Bundle 일치, integrity=ok/FK0. 최종 Source·DB SHA와 전체 수량은 [DATA08_B_COUNTS.json](Docs/DATA08_B_COUNTS.json)에 기록했다.

새 content_items1,314 UUID4, 기존 ID/상세본문/kind/created_at/sort_key/learning_order/lesson membership 삭제·재정렬·비활성화0. 관계 추가 끝점28개(어휘13/문법15)에 한해 revision+1/updated_at 갱신. 승인 목록=`Content/data08-b-revised-ids.json`. 기존1,677어휘와 A 전체 payload를 검사했다.

기존 문법42개를 유지하고 새 예문15개를 참조하며, 실제 LIMIT6 안에서 이전/새 예문 모두 노출을 확인했다. 의미별 Example ID를 기존 Grammar/Listening/Sentence Production이 재사용할 구조는 유지한다. 신규 듣기/문항을 만든 것으로 세지 않는다. 하다형other, ㅂ/르/규칙 metadata와 predicate/expression has_batchim=null, expression irregular_type=null 유지.

### 테스트·발견·수정·미해결

- 첫 portable: **254개 실행 / 251 PASS / 3 FAIL / skip0**. 세 실패는 Note 링크282→382와 전역 품사 총수 기대값 미갱신. 기존 제약·검사 강도를 유지하며 정확한 총수만 갱신했다.
- 중간 재검사255 PASS 후 마지막 기본형 대조에서 반대로→반대(명사+로)를 보정했다. 신규 UUID를 재발급하지 않고 해당 미배포 어휘의 기본형/품사/Note를 바로잡았다. B2/B3 감사/Validator와 전체 검사를 재실행했다.
- 최종 `sh Tools/verify.sh --portable`: **255개 PASS (failures/errors/skip0, exit0)**. 로그=`Docs/DATA08_B_TEST_LOG.txt`. 기존243 + B 신규12, 초기/중간 실패·통과 로그도 보존한다.
- A의 정확한301/602 및14→15 검사는 v15 fixture로 보존, B의15→16 검사는 현재 Bundle에서 A 전체를 포함한 기존 payload/ID 보존을 확인한다. 실제SQL 카드/뜻/Note/검색/문법/관계·20개 세트·5/10/20 due·중복enrollment와 A어휘20개의4/20 부분session/사용자DB byte/SRS/favorite/설정/schema10 보존을 검사했다. 기존 회귀군의 Grammar/Listening/직접입력/통계/유지학습 검사도 유지했다.
- 실제 활용10어휘/카드 연결 XCTest1개 추가. native 정의 **128개, 실행0**. Swift/Xcode 없음; type-check/Debug·Release build/SDK link/XCTest·실기기 검증을 portable 성공으로 대체하지 않는다. 기존 native Data07 전체初中級 기대값270→871도 수정했다.
- 새 runtime 코드/엔진/사용자DB/광고·구매 변경0. 기존 retirement resume P1, native 출시 gate, 初中級 Grammar0/Listening2/Question5와 상위레벨 공백은 유지한다. 이번 범위에서 미해결 데이터 손상 P0를 재현하지 않았으나 앱 전체 결함 부재나 출시 승인으로 표현하지 않는다.

로컬SQLite/저장/Resume·짧은 세션·광고 경계를 유지한다. 실제3~10분·iPhone 비행기모드/TTS/통화·kill/VoiceOver/광고/IAP/알림은 기존 Mac/실기기 gate다. 배포 판정 B—Conditional 유지.

### Git 전달

기존 명시적 커밋·푸시·PR·머지 위임에 따라 검증된 branch를 전달한다. 최종 커밋/PR/merge SHA는 Git/PR 자체가 기준이며 문서 안에 자기 commit SHA를 고정해 순환 변경하지 않는다. 직전 main과 merge 직전 remote 상태, 실제 merge/최종 clean 여부는 최종 응답에서 보고한다.

근거: [개별 검수](Docs/DATA08_B_REVIEW.md), [전체 카탈로그](Docs/DATA08_B_REVIEW_CATALOG.md), [수량·해시](Docs/DATA08_B_COUNTS.json), `Docs/DATA08_B1~B3_AUDIT.json` / `VALIDATION.json` / `EDITORIAL.json` / `DB_BUILD.json`.


## 12. DATA-08-4 / Batch C 완료

2026-10-19 (Asia/Tokyo). 시작 main/origin/main=`e7ed775342e261716aa1f7a4afd3eabd965fde78` (Batch B PR #4 merge), tracked/untracked 변경0. 기존 상태·제작·진행·출시 문서, Batch A/B 색인과 실제 Production Source/DB/Swift repository·활용 엔진을 확인했다. branch=`data08-4/batch-c`. 중단 후 이 branch와 미커밋 산출물을 그대로 이어서 사용했으며 기존 DEV-01~14 / DATA-01~07 / A/B 결과를 보존했다.

### 실제 증가·전체 목표 달성

이번 **初中級 Vocabulary310 / 신규 문장 Example619**를 승인했다. 일반 어휘280 / 회화 Phrase30을 구분한다. 기존 문장1개 재사용으로 Vocabulary-Example 관계는620개 증가했으며 재사용을 신규 문장으로 계산하지 않았다. 기본 가이드270~400 / 450~650 충족. 목표 축소0, 부족0/0이며 Batch C 이후 신규 콘텐츠 작업은 수행하지 않았다.

| Batch | 신규 Vocabulary 행 | 일반 어휘 | Phrase | 신규 문장 |
| --- | ---: | ---: | ---: | ---: |
| A | 301 | 261 | 40 | 602 |
| B | 300 | 266 | 34 | 600 |
| C | 310 | 280 | 30 | 619 |
| 누적 | **911** | **807** | **104** | **1,821** |

**전체 목표 신규 어휘800~1,200 / 예문1,300~2,000 달성.** Phrase를 제외한 일반 어휘만807개로 하한을 충족한다. 관계·fixture·활용형·고유명사·희귀 전문어·기존 초급 단어 재등록으로 수량을 부풀리지 않았다.

| 항목 | 직전 Content16 | C 증가 | 현재 Content17 |
| --- | ---: | ---: | ---: |
| Vocabulary | 1,977 | 310 | **2,287** |
| Meaning | 2,086 | 334 | 2,420 |
| 문장 Example | 3,965 | 619 | **4,584** |
| 전체 Example (기존 발음13 포함) | 3,978 | 619 | 4,597 |
| Grammar | 42 | 0 | 42 |
| Listening | 115 | 0 | 115 |
| Question | 354 | 0 | 354 |
| Learner Note | 385 | 146 | 531 |
| Grammar Example 참조 | 152 | 17 | 169 |
| Vocabulary Example 참조 | 3,894 | 620 | 4,514 |
| content_items | 9,161 | 1,412 | 10,573 |

어휘 level: 入門306 / 初級800 / 初中級1,181. 문장: 入門646 / 初級1,577 / 初中級2,361. Grammar22/20/0, Listening34/79/2, Question入門156/初級134/初中級5/한글59. 신규 C는 전부 lower_intermediate다. **Content17 / Schema4 / minReader7 / UserProgress10**이며 공식 TOPIK·빈도는 추정하지 않았다.

### Batch 검수·품질·오류 처리

| 묶음 | 영역 | 일반/표현 | 신규 문장/재사용 | 의미/Note | strict Validator |
| --- | --- | ---: | ---: | ---: | --- |
| C1 | 현대 생활·디지털·미디어 | 90/10 | 199/1 | 105/42 | 오류0 / 기존 경고10 |
| C2 | 직장·계획·협업 | 90/10 | 200/0 | 102/45 | 오류0 / 기존 경고10 |
| C3 | 사회·추상어·회화 | 100/10 | 220/0 | 127/59 | 오류0 / 기존 경고10 |

동사138·형용사45·부사44·명사53·expression30. 전310항목 Collocation/Register, 다의어·용법24항목, 일본인 Note146, 실제 어휘 관계84. Phrase는 기존 expression 계약으로 제공하고 색인의 lexical_category로 구분한다. 신규 Grammar는0이며 기존 Grammar17개에 예문을 추가 참조한다.

검수자는 작성자와 같은 assistant다. 작성 뒤 전310표제어·뜻334·620문장 쌍(신규619/기존1)·146 Note를 한국어와 일본어로 개별 재독했다. 독립 원어민·전문가 승인이 아니다. 조사·목적어·자동사/타동사·활용·띄어쓰기·상황·난도·시제와 일본어 의미 범위·문체·뉘앙스를 대조했다. 예문은 상황/길이/시제를 섞고 단순 틀 치환을 피했다. 공식 난도 인증이나 모든 선행 형태소의 학습을 보장한 것은 아니다.

- 로그인/로그아웃 명사 기본형, 개인 정보/이용 약관 띄어쓰기, 한참 명사, 이왕·고작·각기·유독의 부사 의미를 사전과 대조했다. 설치하다/구독하다/투명하다/연기하다/비추다·비치다 등은 의미별 Example ID와 연결했다.
- 사직하다/퇴사하다 목적어·수립하다 일본어·분산되다 결합·마음가짐·간혹·지탱하다 등의 초안을 교정했다. 삼가요, 달가워요·미더워요·껄끄러워요와 기존 엔진 metadata 계약을 확인했다. 교정 전후/사전 URL/개별 payload SHA는 아래 근거 파일에 보존한다.
- 중복 Audit가 `확인하지 않은 소문을 퍼뜨리지 마세요.`의 기존 ID `3fb4a617-a5ef-476b-9f40-0963a3ff9845`를 검출해 기존 한일 문장 그대로 재사용했다. 본문은 보존하고 관계 끝점 revision만 갱신했다.
- 초기 assembler에서 실제 부재했던 입력하다·삭제하다·퍼지다·충고하다 관련 관계4개를 제외했다. 수량을 채우는 신규 어휘는 만들지 않았다. 최종84관계는 모두 실제 active ID다.
- 전역 기존 DB/A/B/C 앞 묶음과 NFC·공백·casefold 기준 표제어/양 언어 예문/한일 쌍을 대조했다. 신규 중복0, UUID/FK/Relation 위반0. 기존 경고10(발음5/동형어5)과 기존 중복4그룹은 보존했으며 Validator를 완화하지 않았다.

### Stable ID·Production·사용자 기록 보존

직전 DB16 byte와 source16을 `Tests/Fixtures/content-v16-production.sqlite` / `content-v16-production.json.gz`에 보존했다. source gzip 복원 SHA와 DB SHA는 직전 main 원본과 일치한다. v14/v15 fixture와 A/B 색인·검수 기록도 그대로다.

신규 content_items1,412개 UUID4를 한 번 발급해 유지했다. 기존 ID/kind/상세 본문/created_at/sort_key/learning_order/lesson membership 삭제·재정렬·비활성화0. 관계가 추가된 기존 끝점46개(어휘28/Grammar17/Example1)만 승인 목록대로 revision+1/updated_at. strict 이전 배포 비교0errors/기존10warnings, integrity=ok/FK0, source 재빌드와 승인 candidate/Bundle 일치. 실제 상세 카드·Meaning·Note·검색·관련어·문법 LIMIT6도 확인했다.

### 통합검사·남은 출시 조건

- 시작 baseline portable255개 PASS. 중단 전 최종 portable269개 PASS였으나 임시 로그가 재시작으로 사라져 최종 상태에서 다시 실행하고 로그를 저장했다.
- 최종 `sh Tools/verify.sh --portable`: **269개 PASS, failures/errors/skipped0, exit0**. 원시 로그=`Docs/DATA08_C_TEST_LOG.txt`; 실행 시간 등은 `Docs/DATA08_C_COUNTS.json`에 기록한다. C 신규14개와 기존255개이며 초기 통합검사 실패0. 후보 단계의 중복/관계 오류는 위에 별도 기록했다.
- B의 정확한300/600 회귀군은 직전 source16/DB16 fixture에서 기존 assertion을 유지한다. C 신규 검사에서는 현재 Bundle의 A/B 포함 기존 전체 payload/ID와16→17 교체를 확인한다. UUID·깨진 후보 거부·카드/검색/관계·20개 세트·5/10/20 due·SRS 중복 등록 방지, A/B 혼합20어휘의4/20 부분 session·UserProgress byte·SRS/favorite/설정/schema10 보존을 검사했다. 기존 Grammar/Listening/직접입력/통계/유지학습 회귀군도 유지한다.
- Swift 활용11개/카드 연결 XCTest1개 추가, native 정의129개 / 실행0. Swift/Xcode 부재로 type-check·Debug/Release·SDK link·XCTest와 iPhone 3~10분·비행기모드·TTS·통화/kill·VoiceOver·광고/IAP·알림은 미실행이다.
- runtime/학습 엔진/UserProgress schema/광고·구매 코드 변경0. 로컬SQLite·Resume·짧은 학습·기존 세트/복습 상한·광고 경계를 유지했다. 기존 retirement active-review P1과 初中級 Grammar0/Listening2/Question5·상위레벨 공백은 남아 있다. 이번 검사에서 새로운 데이터 손상 P0를 재현하지 않았다. **Release Readiness B—Conditional 유지**; DATA-08 수량 목표 달성을 앱 출시 승인으로 표현하지 않는다.

### Git 전달

명시적 커밋·푸시·PR·머지 위임에 따라 검증된 `data08-4/batch-c`를 main으로 전달한다. 기존 변경을 강제 초기화하거나 강제 푸시하지 않는다. 최종 commit/PR/merge SHA는 Git/PR 자체가 기준이며, merge 직전 원격 상태와 최종 main 일치·clean 여부는 최종 응답에 기록한다. 이번 Batch C에서 종료한다.

근거: [검수 기록](Docs/DATA08_C_REVIEW.md), [전체 카탈로그](Docs/DATA08_C_REVIEW_CATALOG.md), [수량·해시](Docs/DATA08_C_COUNTS.json), [테스트 로그](Docs/DATA08_C_TEST_LOG.txt), `Docs/DATA08_C1~C3_AUDIT.json` / `VALIDATION.json` / `EDITORIAL.json` / `CORRECTIONS.json` / `DICTIONARY.json` / `DB_BUILD.json`.


## 13. DATA-08-5 / A~C 최종 품질 감사

2026-10-19 (Asia/Tokyo). 시작 `main=origin/main=093b215f4d4d788b11e65febc4338b597cc76f0e`, tracked/untracked 변경0. 상태·제작·진행·출시 문서 및 실제 Content17 Source/DB/기존 학습 SQL·Swift 활용 엔진을 확인했다. branch=`data08-5/final-audit`. 기존 DEV-01~14 / DATA-01~07 / A~C의 ID·테스트·검수 이력을 보존하고 DATA-08-5만 수행했다.

### 실제 검수 범위와 별도 표본

**검수자는 같은 작성 assistant이며, 사람·독립 원어민/교육 전문가 검수는 미실행이다.** Validator 통과나 assistant 재독을 사람 검수·언어 품질 보장으로 표시하지 않는다.

| 범위 | A | B | C | 합계 |
| --- | ---: | ---: | ---: | ---: |
| 어휘 | 301 | 300 | 310 | **911** |
| Meaning | 318 | 311 | 334 | **963** |
| 신규 문장 Example | 602 | 600 | 619 | **1,821** |
| 어휘별 예문 배치 | 602 | 600 | 620 | 1,822 |
| Learner Note | 68 | 100 | 146 | **314** |
| 어휘 관계 / Grammar 참조 | 45 / 14 | 72 / 15 | 84 / 17 | 201 / 46 |

C 재사용1문장은 A의 소문 예문과 같은 ID다. 전체 고유 예문은1,821개다. 일반어휘807 / Phrase104로, 전체 목표800~1,200어휘 / 1,300~2,000예문 달성·부족0/0을 유지한다. 이번 신규 행/ID/콘텐츠 수량 증가는0이다.

한국어와 일본어를 별도 재독했다. 全911개 lemma/POS·뜻963·예문1,822배치·Note314와 존재하는 Collocation/Nuance/Register/learning point를 읽고, 다의어52항목·조사/활용/띄어쓰기·자동사/타동사·일본어 의미/시제/수혜·자연스러움/문체·선행 Grammar/Level·문장 다양성·혼동어 Note를 점검했다. 태그12개·source3개 및201어휘 관계/46문법 참조도 재독했다. null인 선택 필드를 검수 완료 데이터가 존재하는 것처럼 세지 않는다. A/B 독립 Register metadata의 공백과 전체 의미별 난도 인증의 한계는 보존한다.

품사별 동사436 / 형용사145 / 부사120 / 명사106 / 표현104. 신규 어휘/문장 Level은 모두 lower_intermediate다. 별도 seed=`DATA08-5-review-20261019`, Batch별15회 + Batch×POS60회 + 실제 Level10회 =85회 추출/**고유84개** 재감사. 모집단이 없는 다른 Level 표본은 만들지 않았다. 표본6개(서투르다·막연히·개인 정보·나란히·담기다·덜컥)의 교정을 재확인했고 전체 발견량과 중복 합산하지 않았다.

22개ㅂ/르 불규칙 전부와 들르다·모자라다·들뜨다·어설프다·가꾸다·삼가다·옳다7개에 현재/조건/미래 기대형을 기록했다. metadata 오류 발견0. 추상어·부사120개·표현104개의 문맥/의미 범위와 일본어 직역 차이를 강화 확인했다. 사전45개 검색 HTTP200으로 POS/의미를 대조했으며, 잘못된 경로404와 추가 링크 추출503은 별도 실패로 남겼다. 모든 활용형 웹 상세 조회나 사람 인증으로 표현하지 않는다.

### 발견·수정·같은 유형 재검색

**34어휘(A8/B9/C17) / 43필드(A9/B16/C18) 수정**. 정확한 전후 값·ID·분류·근거는 [FINAL_FINDINGS](Docs/DATA08_FINAL_FINDINGS.json)에 있다.

- `상담을 받았어요` → `相談を受けました`의 수혜 방향 역전을 `相談に乗ってもらいました`로 수정했다. 상담·인계/인수·해고와 번역의 주체/수혜를 전체 DB에서 다시 비교했다.
- `胸がわくわく` / `ぽっかりと寂しい` / `するのは不慣れ` 등 어색한 일본어 결합과 빠르게/急に의 속도·돌발성 차이, 시제/공유 표현·직역 반복을 교정했다.
- 내다보다·까다롭다·심지어·야근하다의 의미 범위/Nuance, **13개 Meaning의 해당 뜻과 어긋난 Collocation**(구독하다의 채널/신문, 미치다의 주어/목적어, 담기다의 실제 물건/추상 의미 등)을 보강했다. 같은 두 용법을 모두 올바르게 보여 주는 병기 목록은 유지했다.
- 해결 단서라는 동일 의미의 관용 결합을 `실마리가 풀리다`/`糸口が開ける`에서 `실마리가 보이다`/`糸口が見える`로 명료화했다. 모든 실제 사용을 비표준어로 단정한 것이 아니다. 기존 어휘·뜻·예문·Note ID/품사를 유지했다. 옛 B 색인은 당시 배포 기록이며 현재 본문은 Source/DB가 기준이다.
- 하마터면 Note의 Grammar 제작 여부·로그인의 신규 등록 수량 산정·공감의 계산 문구 등을 학습자 설명으로 바꿨다. 로그인과 단순 접속, 다잡다와 마음을 놓다의 차이도 명료화했다.

동일 유형을 A~C 이전 자료까지 포함한 **전체 Production vocabulary/meanings/examples/notes**에서 검색했다. 교정 전 주체 방향53 / 편집 용어14 / 속도42 / 관용 단서23 / 일본어 결합12 / 활용·철자10필드가 후보였다. 후보 수는 오류 수가 아니다. 오용을 인용해 설명한 Note와 올바른 문맥은 유지했다. 전963 Meaning·다의어52항목104 Meaning 재비교로13개 Collocation 교정을 확정했다. 검색식·매칭 ID·전후 텍스트·판단 범위는 [FINAL_RESCAN](Docs/DATA08_FINAL_RESCAN.json)에 남겼다. 이전 DATA의 상세 본문 수정0, 신규 중복0, 참조 위반0.

### Production·버전·Stable ID 보존

현재 **Content18 / Schema4 / minReader7 / UserProgress10**. Production 실제 수량은 Vocabulary2,287 / Meaning2,420 / Example4,597(문장4,584+발음13) / Note531 / Grammar42 / Listening115 / Question354로 그대로다. 어휘 level入門306/初級800/初中級1,181, 문장646/1,577/2,361. 신규/삭제/비활성화/재발급 ID0, 관계/정렬/created_at/lesson membership 변경0.

직전 Content17 DB·Source를 `Tests/Fixtures/content-v17-production.sqlite` / `content-v17-production.json.gz`에 정확히 보존했다. 기존 v14/v15/v16 fixture 및 A/B/C 색인·검수 보고서는 그대로다.40엔티티(어휘1/의미19/예문12/Note8)만 승인 목록대로 revision+1/updated_at. 전체 Source에서43필드와 metadata/revision을 역적용하면 원본17과 정확히 일치한다. 실제 source/DB SHA·허용 목록은 [FINAL_COUNTS](Docs/DATA08_FINAL_COUNTS.json) / `Content/data08-final-revised-ids.json`에 기록했다.

### 자동 검사·회귀검사 결과와 한계

- 기존 strict `--previous content-v17-production.sqlite`: **오류0 / 기존 경고10**, integrity=ok/FK0. Source 재빌드·승인 candidate/Bundle의 전체 SQL 행을 대조했다.
- 추가 감사 도구로25테이블 **42,909행** 및 A~C 전항목의 ID/PK/FK·필수 필드/형식·중복·Meaning/POS/ordinal·active/level·의미별 예문·Note/typed Relation/Grammar 참조를 검사했다. 초기 관찰 패턴 lint10건 → 교정 후0건. 이 도구의 row-field 경고5개와 strict DB 검사의 총10개 경고를 구분한다. lint 통과는 언어 품질 보장이 아니다.
- core Validator에 허용 줄바꿈/탭 외 숨은 제어문자 검사를 추가했다. **신규11개 집중 검사 PASS**(11.511초, failures/errors/skipped0, exit0).
- 최종 `sh Tools/verify.sh --portable`: **280개 PASS**(186.489초, failures/errors/skipped0, exit0). 기존269개+신규11개. 이번 전체 suite 실패0. 원시 로그=[FINAL_TEST_LOG](Docs/DATA08_FINAL_TEST_LOG.txt). 초기 언어/편집 lint10건과 테스트 실패를 혼동하지 않는다.
- A/B/C의15/16/17 배포 assertion과 SHA는 원본 fixture에서 보존한다. 새 감사 회귀군은 현재18의 전체 보존·43필드 교정·40 revision, 카드/뜻/Note/검색·관계·46 Grammar LIMIT6, 수정 어휘20개 세트4/20 부분 session/SRS due/favorite/설정/UserProgress10 byte 보존 및5/10/20 복습을 확인했다. 검사 제약·assertion 완화0.
- native 정의 **130개 / 실행0**. 신규 XCTest1개는29어휘×현재/조건/미래87기대형을 실제 엔진과 대조하도록 작성했으나 Swift/Xcode 부재로 미실행이다. Xcode/SDK link/Debug·Release/XCTest·iPhone3~10분/비행기모드/TTS/중단/VoiceOver/광고/StoreKit/알림은 기존 별도 gate다.

### 남은 의심·검수 항목과 Git

기존 Grammar42개와46참조의 존재/문맥/조회는 확인했지만 전체 예문의 선행 문법 학습을 입증하지 못했다. 인용·목적/예방·뻔하다·더니·기로·양보 등 **163개 고유 예문의 문형 후보**를 [FINAL_GRAMMAR](Docs/DATA08_FINAL_GRAMMAR.json)에 기록했다. 제한적 regex 후보 목록이며 완전한 형태소 분석·확정 오류 목록이 아니다. 부사 되도록은 -도록 후보에서 제외했다. 일부는 짧은 Note/learning point가 있고, 새로운 Grammar 단원을 제작하지 않았다.

편집 Level lower_intermediate와 Register·관용 결합의 독립 일본인 학습자/한국어 교사 적합성 확인, 사람 언어 검수와 native 실행은 남아 있다. 기존 retirement active-review P1·初中級 Grammar0/Listening2/Question5·상위 Level 공백도 유지한다. **B—Conditional 유지**; 이번 단계에서 새 데이터 손상 P0를 재현하지 않았으나 앱/언어 전체 무결함이나 출시 승인으로 표시하지 않는다. runtime/학습 엔진/사용자DB/광고·구매 코드 변경0.

기존 명시적 커밋·푸시·PR·머지 위임에 따라 검증된 branch를 전달한다. 실제 최종 commit/PR/merge SHA는 Git/PR 자체가 기준이며 원격 상태·최종 main 일치/clean 여부는 최종 응답으로 보고한다. **DATA-08-5에서 종료하고 다음 단계는 시작하지 않았다.**

상세: [전체 감사](Docs/DATA08_FINAL_REVIEW.md), [항목별 재독 SHA](Docs/DATA08_FINAL_EDITORIAL.json), [무작위 표본](Docs/DATA08_FINAL_SAMPLES.json), [사전 근거](Docs/DATA08_FINAL_DICTIONARY.json), [실제 수량·해시](Docs/DATA08_FINAL_COUNTS.json), [구조 검사](Docs/DATA08_FINAL_STRUCTURE.json).
