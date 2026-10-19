# PROJECT_STATUS — DATA-05

2026-10-03. DATA-04의 프로젝트·제작 문서·실제 production DB를 기준으로 初級 어휘를 확장하고 기능 간 연결/버그 감사를 수행했다. 중단 전 약12분, 재개 후 검증·수정·문서화 작업을 이어 진행했다. 신규 생성은 200개에서 중단하여 통합 검증에 시간을 배정했다. 이전 상태는 `Docs/DATA-04_STATUS.md`에 보존했다.

**Xcode build / Swift type-check / XCTest / 실제 UI·Navigation·음성 출력은 Linux에서 실행하지 못했다. 따라서 iOS end-to-end 정상 동작을 확인한 배포 완료라고 주장하지 않는다. 아래 실행 검증과 네이티브 미검증을 구분한다.**

## 실제 구현·추가 결과

- 신규 vocabulary **200개 모두 初級**. 명사64 / 동사61 / 형용사32 / 부사23 / expression20.
- 신규 meanings210, examples339, learner_notes33. 어휘-예문 관계340개(한 문장을 두 신규 어휘가 공유).
- 신규 직접입력8문제 / 7어휘. 신규 listening4개와 question4개. 총 신규 questions12.
- 기존 grammar6개에 예문11관계 추가, 기존 형태/미래 grammar prerequisite도 사용. 기존 grammar8개만 관계 개정 revision+1. 기존 어휘·의미·예문·문법 본문 수정0, Stable ID 삭제/재배정0.
- 새 vocabulary는 기존 ContentRepository → 初級単語 → 저장된20개 set → 회독 → SRS 경로를 그대로 사용. 기존 sort_key 및 저장된 membership은 보존했다.
- 별도 DB/진도 시스템/앱 데이터 배열/새 학습 framework를 만들지 않았다. UI 변경은 활용 화면 lifecycle 오류 수정으로 제한했다.

## DB / Version

**Content schema4 / content12 / min reader7 / UserProgress8**, 모두 기존 SQLite 구조를 유지했다. 앱이 읽는 번들은 `Resources/content.sqlite`, 유일한 제작 원본은 `Content/production.json`이다. `Content/data05-ids.json`은 QA용 stable ID 목록으로 앱이 읽지 않는다.

실제 DB 집계: vocabulary926(入門306/初級620), meanings982, examples1876(문장1863+발음 예시13), grammar42(入門22/初級20), listening31, questions262, learner_notes181. 전체 count는 `DATA_PROGRESS.md` 참조.

v11 이전배포를 `Tests/Fixtures/content-v11-production.sqlite`에 보존했다. `--previous` 엄격 검증으로 v11→v12 콘텐츠 업데이트를 수행했다. UserProgress DB migration/초기화 코드는 변경하지 않았다. 다음 DATA는 v12를 previous로 사용하고 content13 이상으로 증가시킨다.

## 품질 검수 / Validator

초안 작성 후 별도 검수로 기존 시끄럽다 중복, 번갈아/차례로 원형·품사, 밤새 품사, 의미가 덧붙은 일본어 번역 등을 수정했다. 다의어10개는 각 의미와 예문을 분리했다. 결제/결재, 맡다/맡기다, 자동·타동사, 발이 넓다, 장학금/보증금 등 일본인용 note33개를 작성했다. 자세한 기록은 `Docs/DATA05_REVIEW.md`.

기존 Validator **오류0 / 경고10**: 기존 동형어 후보5(저/차/일/쓰다/적다), 짧은 발음 예시5. 신규 중복 lemma후보0, 동일 한국어/일본어 예문 쌍 중복0. Validator 규칙은 끄거나 약화하지 않았다. 초안의 note kind와 listening_input type 오입력도 데이터에서 수정 후 정상 DB를 원자적으로 생성했다.

## Integration

`Docs/DATA05_INTEGRATION_AUDIT.md`에 A~J 흐름별 실행 범위와 남은 검증을 기록했다.

- **Vocabulary/회독**: 실제 SQL로 신규200개 카드/meaning/example/note 조회. 기존 初級420개 순서 보존, 뒤에200개 추가. 새 set membership과 위치13/회독 상태 디스크 재개, UNIQUE 및 중복 저장 방어 검증.
- **SRS**: 기존 schedule(stage4)와 새 stage0 등록 분리, 재등록이 기존 값을 덮지 않음, due20 제한/인덱스·중복 방어 SQL 검증.
- **Grammar**: 예문11관계가 실제 제한된 repository 조회에서 모두 조회됨. 기존 grammar본문/레슨 구성 보존.
- **Conjugation**: 새8문제의 metadata/accepted/prerequisite 조회. 줍다·기르다·모으다·잠들다·빨갛다·날카롭다·젖다를 연결했다. ㅎ 현재형은 검토한 override 사용. Swift 실제 생성 결과는 XCTest 실행 필요.
- **Listening**: 새4개가 기존 Example ID를 source로 재사용, beginner batch2(order40~43)에 배치. dictation 정답/level/TTS원문 검증, attempt 중복 거부·skill분리·디스크 snapshot재개 검사.
- **Audio/Navigation**: 공통service의 누락음원/ko-KR fallback·stop·세대토큰 경로와 홈→단어/복습/문법/듣기→종료 경로 소스 감사. 실제 화면 탭·back stack·음성 청취는 미실행.
- **Content Version regression**: 기존 모든 content ID·본문·세트 후보순서·lesson구성 유지. 기존 사용자 파일은 제공되지 않아 테스트용 UserProgress로 검증했다.

### Bugs Found

1. ㄷ 불규칙 future/condition 분기가 ㄹ로 바꾼 뒤 으를 잃음(걷다→걸면/걸 거예요 가능).
2. 비활성 vocabulary를 활성 question만 보고 활용 목록/문제에 계속 노출.
3. 활용 화면이 background로 갈 때 onDisappear만으로 TTS 정지가 보장되지 않음.
4. 취소되거나 이전 grammarID에 대한 비동기 로딩 오류가 현재 화면을 덮을 수 있음.

### Bugs Fixed

1. ㄷ→ㄹ 뒤 으를 유지하여 걸으면/걸을 거예요 분기로 수정; 걷다/듣다/묻다 회귀 기대값 추가.
2. SQLiteProduction에서 vocabulary의 is_active도 검사하고 active meaning을 조회. 실제 비활성화 SQL 재현 테스트 통과.
3. ProductionStudyView scenePhase inactive/background에서 audio.stop 및 focus해제.
4. CancellationError를 무시하고 동일 grammarID인 경우에만 로딩 오류 표시.

### Known Remaining Issues

- 위 Swift 수정은 구문검사를 통과했지만 native build/runtime 검증은 아직이다. iOS 실기기/시뮬레이터에서 앱 강제종료 재개, back stack, background 음성 정지를 확인해야 한다.
- 한국어 음성이 없는 기기에서는 듣기 제출을 열지 않는다. 안내 후 뒤로 나갈 수 있으며 음성이 준비되면 재개한다. 무음 상태를 학습 성공으로 처리하지 않는다.
- Conjugation은 지원된9형태/검토된 override 범위만 보장하도록 설계되어 있다. 신규 모든 predicate의 모든 활용 문제가 자동 생성된 것은 아니다.
- 전문 언어 감수·녹음 검수·실제 iOS cold launch/메모리 측정 미수행.
- 새 TODO/FIXME/placeholder는 추가하지 않았다. 기존 자모/발음 비교 녹음 대기 상태는 유지한다.

## Test / Build

- 전체 **Python/SQLite 168개 PASS** (`Docs/TEST_RESULTS_DATA05.txt`). 기존159개+신규9개. 실제 repository SQL, invalid input 거부, 관계/버전/ID, migration·진도·SRS·듣기·대용량 synthetic 회귀 포함.
- **Swift62파일 구문검사 오류0** (`Docs/STATIC_CHECKS_DATA05.txt`). Swift 컴파일/타입검사가 아니다.
- **Native XCTest82개 작성·미실행**. 새 production 단어의 회독→cold resume→SRS→복습과 새 listening source→재개→due 등록 end-to-end 테스트2개를 추가했다. 기존 ㄷ활용 회귀 기대값 및 실제 production pool count를 갱신했다.
- `swift`/`xcodebuild`가 없는 환경이므로 Debug/Release build와 XCTest는 실행하지 않았다. Mac에서 `Tools/verify.sh`와 실제 기기 검증 필요.
- Linux warm SQLite 100회 median: stableID0.0054ms, 初級20개 page0.0782ms, 검색0.0399ms, 예문관계0.0096ms. 앱 실행 성능 수치가 아니다. 원본/실행계획은 `Docs/DATA05_PERFORMANCE.json`.

## 주요 변경 파일 / 다음 단계

`Content/production.json`, `Content/data05-ids.json`, `Content/data05-revised-ids.json`, `Resources/content.sqlite`, `LearningEngine/ConjugationEngine.swift`, `Repositories/SQLiteProduction.swift`, `Views/ProductionView.swift`, `Tests/ProductionLearningTests.swift`, `Tests/ListeningTests.swift`, `Tools/ContentBuilder/test_data05_content.py`, 기존 batch test의 현재 count/허용 revision gate, 제작·진행·검수 문서.

다음 작업은 새 데이터보다 먼저 Mac native build/test 및 `Docs/DATA05_INTEGRATION_AUDIT.md`의 미실행 항목을 확인한다. 이후 콘텐츠만 추가할 때 schema4/UserProgress8을 불필요하게 변경하지 말고 기존 set/SRS ID를 유지한다. DATA04 역사적 v10→v11 정확 비교는 v11 snapshot에 고정했고, 신규 v11→현재 strict gate가 이를 이어받는다.
