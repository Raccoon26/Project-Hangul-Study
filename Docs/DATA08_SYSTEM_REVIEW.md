# DATA-08-7 요구사항·통합 감사

2026-10-19 UTC. 시작 `main`/`origin/main`=`42441768ea3ce39490350ed217021cfad58eae71`, tracked/untracked 변경0. branch=`data08-7/requirements-audit`. 기존 클라우드 체크아웃과 Python 표준 라이브러리 검증 환경을 재사용했다. 추가 환경 설정/설치/서비스는 필요 없었다.

**Content19 / Schema4 / minReader7 / UserProgress10 유지. Production Source/DB byte 변경0.** DATA08 전체 목표911어휘(일반807/표현104)/고유 신규예문1,821 달성 유지. 이번 신규·수정·삭제·비활성·재발급 콘텐츠 ID0, revision 변경0. runtime 오류만 고쳤으며 Content Version을 불필요하게 올리지 않았다. 앱 출시 판정은 **B—Conditional**이다.

## 명세 근거와 확인 불가능한 범위

완전한 **DEV-01~14 / DATA-01~07 원래 작업 명세 원문을 저장소에서 찾지 못했다.** 현재 파일 경로/문서 본문과 전체 Git history의 SPEC/spec/REQUIREMENT 경로를 조사했으며, 해당 이름으로는 DEV12~14 사후 감사 문서만 있었다. `Docs/DEV-xx_STATUS.md`, `Docs/DATA-01~06_STATUS.md`, `Docs/DATA07_REVIEW.md`는 이전 구현/검수 보고서다. 그 안의 요구 설명을 원래 사용자 요청 전체와 동일하다고 가정하지 않는다. 원문 누락 조건·원래 수량/디자인/테스트 수락 기준의 완전한 충족은 **UNVERIFIABLE**이다. 외부 공유 링크/ZIP에만 있을 수 있는 원문을 이번 감사에서 확인했다고 주장하지 않는다.

현재 사용자의 DATA08-1~7 요청, `AGENTS.md`, `CONTENT_GUIDE.md`, `DATA08_PROGRESS.md`, 보존된 DEV/DATA 보고서의 명시적 계약을 실제 코드·DB와 대조했다. 이번7 요청 원문은 [SYSTEM_REQUEST](DATA08_SYSTEM_REQUEST.md)에 보존했다.21개 옛 단계별 근거 경로/해시/보고된 한계는 [SYSTEM_AUDIT](DATA08_SYSTEM_AUDIT.json)의 specification_inventory에 있다. 아래 ‘연결 확인’은 코드+실행된 SQL 범위이며 iOS 실행 PASS를 의미하지 않는다.

## DEV-01~14 대조표

| 단계/계약 | 실제 구현·검사 근거 | 상태·누락·테스트 부족 |
| --- | --- | --- |
| DEV-01 기반·분리·Stable ID·원자 저장 | AppContainer/SQLiteConnection/SQLiteProgressRepository, test_repository_sql·test_learning_sql·test_builder | SQLite 이벤트/통계/FK/롤백/멱등성 PASS. native build/UI는 BLOCKED |
| DEV-02 확장 schema/Importer/Validator/대규모 | content-schema-v4, build_content/validator, test_validation_v2·test_large_content·benchmark | 전63,159행/UUID/PK/FK/source 일치 PASS. 원격 서명 updater/복구·동기화 UI/전체 prerequisite-cycle 검증은 부분·미구현 |
| DEV-03 한글·레슨·재개 | HangulLearning/LessonViewModel/LessonSession, hangul55/문자12레슨59문제, test_hangul_content·test_learning_sql | 콘텐츠/트랜잭션 연결 확인. 실제 발음/조작·음절 엔진 실행은 BLOCKED |
| DEV-04 발음·받침·음원 정책 | pronunciation36/14레슨, AudioPolicy/KoreanAudioService, test_pronunciation_content | 고립 자모/비교 TTS 금지·녹음 없음 안내 유지. 검증 녹음0, 실제 interruption/청취 BLOCKED |
| DEV-05 어휘·뜻공개·회독·Set | VocabularySetCatalog/VocabularyPassEngine/SQLiteVocabularyProgress, card2,287/meaning2,420, test_vocabulary_sql/data tests | 고정 snapshot/20개 할당·전Meaning 예문 조회 PASS. curated mixed set scheduler는 없음. 퇴역 항목이 있는 기존 고정 회독/레슨은 보존 후 안전 정지하는 기존 계약이며 자동 membership 대체/alias 병합은 미구현 |
| DEV-06 SRS·일정·중복 | StepReviewScheduler/SQLiteReviewProgress, UNIQUE(content_id,skill), test_srs_sql·system tests | SRS 중복/기존 due/unsupported algorithm 보존 PASS. P1-01 수정. 최적 interval/적응형 개인화는 부분, native calendar 실행 BLOCKED |
| DEV-07 Grammar·비교·퀴즈·SRS | SQLiteGrammarContent/Progress/GrammarLearning,42개/12레슨84문제, test_grammar_content | 실제 조회/관계 PASS. 初中級 독립 Grammar0·상위 문법 공백, native 채점/회독 BLOCKED |
| DEV-08 Conjugation·Sentence Production | ConjugationEngine/ProductionAnswer/SQLiteProduction,612lemma/1,227문항 | 명시적9형/override/기존 SRS DO NOTHING 연결. 자유작문 채점·직접입력 전용 due queue는 미구현. 아래 불규칙 예외 부족, Swift 실행 BLOCKED |
| DEV-09 Listening/Dictation | SQLiteListening/ListeningSession/ListeningView,1,936항목/104batch, test_listening_content |4유형/재생완료 게이트·retry/기존 snapshot 보존. P1-02/03 수정. 실제 음성·오디오 route/VoiceOver BLOCKED |
| DEV-10 Curriculum/Placement/Resume | SQLiteCurriculum/Curriculum/Placement/Resume views, test_curriculum_sql·test_dev13 |9단계 실제 membership·최신 저장활동·8문항 간이진단 연결. 혼합 Unit 자동진행/정밀·공인 진단/상위 콘텐츠는 부분 |
| DEV-11 Search/Dictionary/Saved/Practice | SQLiteLookup/SQLiteSavedContent/LookupViewModel, test_lookup_sql | 전2,329 typed 상세·어휘2,287 표제어 검색·일본어72뜻 표본 PASS. literal %, quote/injection·중복/누락 저장도 기존 검사. 실제 back stack/IME/빠른 tap BLOCKED |
| DEV-12 Statistics/Maintenance/Settings/짧은 학습 | SQLiteStatistics/LearningPreferences/Learn/Maintenance, test_dev12_sql | 실제 event/5·10·20/부분저장·수동 practice의 SRS 불변 PASS. 전역 adaptive 유지학습·일일 학습 추천은 부분. UserDefaults/알림/실제3~10분 BLOCKED |
| DEV-13 AdMob/StoreKit/광고 제거 | PurchaseService/AdService/MonetizationPolicy/RemoveAdsView, test_dev13_integration·system tests | 학습 저장과 독립·유일 완료 경계·cache key/상품 ID 독립성 소스 검사 PASS. 실제 SDK/Keychain/StoreKit 거래는 BLOCKED |
| DEV-14 출시 감사/패키징 | Config/Info.plist/privacy manifest/verify.sh, test_dev14_audit/check_monetization | portable/설정 안전 검사 PASS. Release Ad IDs 없음→광고 비활성은 안전 동작이다. Xcode/SDK resolve·Debug/Release·서명/ASC/실기기는 BLOCKED/미완료 |

## DATA-01~07 / DATA08 대조

| 단계 | 실제 보존/대조 | 남은 검수 |
| --- | --- | --- |
| DATA-01 | data01 IDs/뜻별 예문/Note/동형어; 원본 fixture·test_data01_content 보존 | 원문 요구 전체·사람 언어 검수 확인 불가 |
| DATA-02 | data02 IDs/POS/규칙·불규칙/다의어/정렬/발음 선택 필드; test_data02_content | 완전 controlled vocabulary·모든 TTS 청취 미확인 |
| DATA-03 | data03 IDs/예문/일본인 Note/fixture6 업데이트; test_data03_content | 이전 보고서의 언어 평가를 독립 감수로 간주하지 않음 |
| DATA-04 | grammar42/관계/비교/혼동/기존 content10→11 snapshot; test_data04_content | 상위 Grammar 확장·native 문법 흐름 미완료 |
| DATA-05 |200어휘/339예문 cohort/직접입력·듣기 연결; test_data05_content | 모든 새 언어 표현/기기 사용성의 독립 평가 미확인 |
| DATA-06 |80듣기4유형/원 Example ID·SRS/질문/순서; test_data06_content | 실제 TTS/받아쓰기/중단·재개 BLOCKED |
| DATA-07 |450어휘/900예문·새 初中級·직접입력·듣기·직전13 보존; test_data07_content | 후속 문법/뉴스·긴 대화/검증 녹음·상위 어휘는 부족 |
| DATA08 A/B/C |301/602 +300/600 +310/619, 고유 합911/1,821, 일반807/표현104. frozen15/16/17 및18 감사 회귀 유지 | 독립 사람 검수·학습 난도 적합성 NOT TESTED |
| DATA08-5/6 |34어휘43필드 교정은18 이력 그대로, 현재911 editorial payload hash 일치.19의47레슨/Unit tag3·듣기1,821·입력1,162 연결 보존 |163개 문형 후보·독립 Level/Register 평가 유지. Unit은 tag/제목 표현이며 별도 entity/혼합 학습 scheduler는 아님 |

## 통합 전수 검사

`audit_data08_system.py`가 현재 번들에 **실제 repository SQL**을 실행했다. Vocabulary2,287 카드/전2,420 Meaning의 예문/typed detail2,329, generic course3·lesson73(한글/발음26+DATA0847), Grammar42·12레슨, Production612어휘/1,227문항, Listening1,936·104batch를 읽었다. generic 레슨의90 + Grammar84 + Production1,227 + Listening1,936 = **전3,337문항**, 미연결0. 전Example4,597개도 실제 단어 상세/문법 예문/발음/듣기 경로의 합집합에서 확인해 도달 불가0이다. 각 경로의 기존 LIMIT/페이지를 지켜 끝까지 조회했다. 이는 질문이 route에서 조회된다는 검사이며 버튼을 누른 iOS E2E 실행이 아니다.

전2,287 한국어 표제어 검색, 일본어 meaning72개 간격 표본, 현재 표제어/종류/상세·뜻별 예문을 대조했다. DATA08 문장 입력581개 모두 실제 선택되는 첫 Meaning과 연결 Example가 일치하고, 전911 lexical payload가18의 감사 SHA와 일치한다. FK/형식/관계 오류0·exact 중복0이라는 구조 결과로 한국어·일본어 의미/번역의 완전한 정확성을 인증하지 않는다.

Content19 재빌드 strict previous18 및 기존 업데이트/1~10 UserProgress migration·WAL commit/프로세스 종료·dataset 불일치 거부·다종 active session/Resume·SRS 중복/멱등성·Favorites/Difficult/Statistics·Settings 저장 경계 검사를 전체 suite에서 실행했다. 실제 사용자 iPhone의 개인 진도 DB는 이 환경에 없으므로 임시 UserProgress fixture 검사다. 설정은 UserDefaults `learning.preferences.v1`이며 SQL metadata 보존 테스트를 실제 설정 실행으로 표현하지 않는다.

## P0/P1 발견·수정·회귀

### P1-01 — 비활성 항목 때문에 Vocabulary/Grammar/Saved Practice 복습 정지

이전 구현은 active session의 첫 ID를 항상 다시 읽고, 없는 카드에서 재조회 버튼만 제공했다. 실제 번들 사본에서 ID를 비활성화하면 card query가0행이고 뒤의 항목을 진행할 수 없다. 새 UI는 카드 누락/Grammar changedContent에서만 **명시적인 보류**를 허용한다. 임의 DB/IO 오류에서는 학습 판정을 대체하지 않는다.

`review.deferred.v1.<session UUID>`에 보류 ID를 기록하고 원래 review_items·순서·기존 답·SRS·즐겨찾기·통계를 남긴다. 완료 수와 보류 수를 따로 표시한다. 마지막 미판정 수에서 보류 수를 제외해 session이 끝나며 보류 항목을 graded/learned로 세지 않는다. `review.unavailable.v1.<skill>.<ID>`는 현재 Content Version에서만 새 due queue/숫자에서 제외하고, `review.content-version.v1`이 바뀌면 원래 SRS due로 다시 확인한다. 따라서 첫20개 퇴역이 다음 queue를 계속 가리는 문제도 막는다. schema/user version을 변경하거나 SRS state_json을 재작성하지 않는다.

보류 중 늦은 DB 실패는 metadata·cursor를 함께 rollback하고, 중복/지연 action은 다음 카드를 건드리지 않는다. vocab/grammar 및 각 practice4종·cold reopen·전체20개 보류·완료 집계0·새 Content Version 재확인·원 SRS 유지 SQL 검사 PASS. native API/실제 ViewModel 회귀3개는 작성했으나 BLOCKED다. 대규모 자동 퇴역/alias merge/기존 고정 회독 membership 변경을 도입한 것은 아니다.

### P1-02 — 받아쓰기 문장부호 생략을 오답 처리

전체 dictation1,850개 중 **DATA081,821개**는 UI의 `句点は不要です` 안내와 달리 문장부호 없는 accepted가 없었다. 기존 judge는 NFC/공백만 정규화하므로 끝마침표를 뺀 올바른 문장이 incorrect가 된다. 현재 `judgeDictation`은 양쪽의 **문장 끝 .!?만** 제외한 뒤 기존 exact/spacing 규칙을 적용한다. 내부 문장부호·철자·내용이 다르면 오답이고, 일반 ProductionAnswer 판정은 그대로다. Source/accepted 배열을 재작성하지 않았다. 전Corpus 계약/Python 검사는 PASS, native 전1,850문항 judge 회귀는 BLOCKED다.

### P1-03 — 듣기 복습의 퇴역 prefix 때문에 후속 활성 항목 누락

임시 번들에서 예정45개 중 첫25개를 비활성화하면 기존 LIMIT20은 매번 빈 출제 결과를 반환한다. 현재는 새 snapshot 생성 전에20개씩 Content 가용성을 읽고, 조회가 정상 성공했는데 반환되지 않은 ID만 버전별로 보류한다. 빈 퇴역 page 다음으로 이동하며 cancellation/yield를 지킨다. 이미 저장된 listening session은 이 과정을 거치지 않고 그대로 복원한다.

45개/첫25퇴역 사례에서2번째 page의15개 활성 항목으로 도달, 나머지5개는 다음 session에 남고 due20을 확인했다. SRS45개 본문/due·기존 snapshot 불변, 새버전에는45개 재확인한다. SQL PASS, native snapshot/가용성 API 회귀는 BLOCKED다.

**실행된 DB/SQL/소스 범위에서 새 P0는 재현되지 않았다.** 이 판단은 native crash가 없다는 인증이 아니다. 상세 ID·전후 코드 근거는 [SYSTEM_REPRO](DATA08_SYSTEM_REPRO.json), 세 발견은 [SYSTEM_RESULTS](DATA08_SYSTEM_RESULTS.json)에 있다.

## 부분 구현·남은 위험

- 불규칙: 전체 predicates metadata는 현재 engine guard 범위 안이고 출제1,227개가 명시 rubric/override를 사용하며 현재 published guard 호환성 검사1,227건에서 오류0이다. 이 검사는 실제 Swift 활용 계산 실행이 아니다. 하다/ㅂ/ㄷ/ㅅ/르 및29개 DATA08 위험형×3 기대형 native 회귀는 그대로 보존했다. **ㅎ 예외의 Dictionary 현재/과거 override가 완전하지 않다**: 파랗다/노랗다는 현재·과거 override가 없고, 빨갛다는 present만 있다. 지원되지 않는 형은 `try?`로 생략하므로 잘못된 형을 출제하는 확인 오류는 없지만 ‘주요 활용’은 부분이다(P2). 자유작문·모든 활용/예외를 구현했다고 주장하지 않는다.
- 기존 고정 어휘 회독·문법 lesson에서 퇴역/누락이 생기는 경우는 snapshot을 보존하고 안전 정지한다. 이번 복습 보류를 해당 회독의 자동 완료/ID 대체로 확대하지 않았다. 실제 대량 retire 배포 전 별도 정책/회귀가 필요한 기존 제한이다. 현재 Production 비활성 행0이며 이번 데이터 삭제/retire0다.
- SOURCE 순서/뜻/참조 검사는 의미상의 모든 오류를 찾는 검사가 아니다.163개 선행 문형 후보, 독립 원어민/교사 검수, 初中級 Grammar0/상위 과정·녹음 부족은 유지한다.
- 실제 Dead Button/Navigation Crash/Audio 중단/VoiceOver/큰 글씨/IME/iPhone 메모리 누수는 **BLOCKED**다. 소스에서 no-op handler·강제 unwrap/fatalError를 신규로 발견하지 않았고 기존 stale ID/revision/generation·배경/이탈 stop 경로를 검토했지만 iOS UI 실행을 대신하지 않는다.
- 대규모 substring 검색은 전체 terms를 훑는다.15k 규모의 넓은 일본어 검색 median78.959ms/max106.634ms는 P2 최적화 관찰점이다. 실제 handset 지연/메모리 gate는 남는다.

## 광고 제거·콘텐츠 버전 독립성

PurchaseService/AdService/MonetizationPolicy/LearningPreferences는 시작 commit과 byte 동일하다. 상품 `remove_ads`·Keychain debug/release 서비스·UserDefaults frequency/preferences key는 Content Version·schema·user_metadata에서 파생하지 않는다. 새 학습 보류 namespace도 구매/광고 상태를 읽거나 수정하지 않는다.18/19/20 버전 metadata 변경과 학습 보류 전후의 **가상 opaque cache 파일 불변** 및 소스 독립성 검사를 했다. 이것을 실제 Keychain/StoreKit 권한 확인으로 표현하지 않는다.

verified/unverified/pending/cancel/revoke/오프라인 보호, restore/currentEntitlements/Transaction.updates와 늦은 광고 load 무효화 소스 및 기존 policy 회귀를 확인했다. 유일한 광고 호출은 성공한 Vocabulary 완료 후이며 Resume/짧은 session·학습 도중·검색·알림에는 없다. 기존12분/60항목/30분 cap과 학습 저장 후 optional side effect를 유지한다. 실제 SDK load/show/consent·기존 구매 기기의 권한·Keychain·StoreKit 거래는 **BLOCKED**다. Release ID가 비어 광고 비활성인 상태는 그대로다.

## 실행 결과 — 상태를 구분

| 검사 | 상태 | 실제 결과 |
| --- | --- | --- |
| Python Unit/SQL Integration/Regression 전체 | **PASS** | 301/301, 296.353초, failures/errors/skipped0, exit0; 신규10 포함 |
| 이번 전용 회귀 | **PASS** |10/10, 0.085초, failures/errors/skipped0, exit0 (전체 suite와 중복이며 추가 고유 테스트 수가 아님) |
| 중간 전체 검사 | **PASS** |300/300,292.344초; 최종 듣기 회귀 추가 전 기록 |
| 첫 전용 harness 검사 | **FAIL → 수정** |9 case 중4 subtest ERROR, exit1. review_items seed의 필수 CHECK 필드를 빠뜨렸고 실제 repository UPDATE로 수정. 초기 로그 보존 |
| 전수 routing/source/DB/검색 감사 | **PASS** | `audit_data08_system.py`, 위 수량/미연결0·FK0·sourceRows63,159 |
| Linux SQL/규모·메모리 측정 | **PASS** | 아래 실제 수치. iPhone 성능 검사 아님 |
| iOS Debug/Release/SDK resolve/type-check | **BLOCKED** | `xcodebuild -version` exit127, command not found; build는 시작하지 못함 |
| Swift XCTest | **BLOCKED** | 정의137개/실행0, 이번5개 추가. 삭제/비활성 테스트0 |
| iPhone UI/오디오/중단·강제종료/Keychain/StoreKit/AdMob | **BLOCKED** |iOS runtime/기기 없음; 실행0 |
| 독립 사람 언어·학습 난도 검수 | **NOT TESTED** |0; assistant 검수/자동 검사로 대체 인증하지 않음 |
| 옛 원본 명세 전체 충족 | **UNVERIFIABLE** |원래 작업 명세 원문 미확보 |

## 성능·메모리 — 로컬 실측

Linux/Python sqlite3, warm connection30회, 실제 repository SQL·별도 임시 UserProgress(SRS2,287행), Python socket 생성 금지. 현재 버전 DB를 현재 SQL로 측정했다. 파일의 before/after는 **같은 현재 SQL을 Content18/19에 적용**한 비교이며 코드 변경 전후나 iPhone UI 시간을 의미하지 않는다. 공유 클라우드 편차가 있다.

| 항목 | median ms | p95 ms |
| --- | ---: | ---: |
| Home refresh/Resume SQL | 6.031 | 13.154 |
| 한국어 검색 | 1.104 | 2.259 |
| 일본어 검색 | 1.030 | 3.364 |
| 넓은 검색30행 | 4.502 | 8.050 |
| SRS20 + 카드 header | 0.846 | 1.213 |
| 20개 membership/session commit SQL | 1.310 | 2.295 |

Synthetic15,000어휘/30,000예문은 `/tmp`에만 생성해 Production에 넣지 않았다. DB50,712,576bytes, build15.5272초, 같은 도구 process peak RSS **68.76MiB**,15,000 ID keyset 전수 조회0.3422초/중복0. 이것은 Python importer/SQL의 peak RSS이며 iOS 앱 heap/leak 검사가 아니다. 별도15k/500grammar 검색도 실행했다. 실제 Source/Bundle hash는 전후 동일하다.

## 재현·Git·종료

```sh
python3 -m unittest discover -s Tools/ContentBuilder -p test_data08_system_audit.py -v
python3 Tools/ContentBuilder/audit_data08_system.py --report /tmp/data08-system-audit.json
sh Tools/verify.sh --portable
python3 Tools/ContentBuilder/benchmark_data08_integration.py --report /tmp/data08-system-performance.json
python3 Tools/ContentBuilder/benchmark.py /tmp/data08-system-scale --count 15000 --report /tmp/data08-system-memory.json
python3 Tools/ContentBuilder/benchmark_lookup.py
```

원시 로그/결과/성능은 `Docs/DATA08_SYSTEM_*`에 보존했다. source SHA `f97b3bd70d07a3945770b8d6940c4a53e29a9b70b565caf21fb927230c08b4a8` / DB SHA `57aeaf918d5eaaec3bbfaed02f87c5452cca8264540b923a70448b781adbe9e5`. 기존 DATA08/DEV/DATA 문서·fixture·137 native 정의를 보존하고 새로운 임시 콘텐츠를 배포하지 않았다.

기존 명시적 커밋·푸시·PR·머지 위임에 따라 검증된 branch를 전달한다. 최종 SHA/PR/clean main 여부는 Git/PR과 최종 응답이 기준이다. **DATA-08-7에서 종료한다. 다음 단계나 App Store 배포는 시작하지 않는다.**
