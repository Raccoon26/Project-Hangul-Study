# PROJECT_STATUS — DEV-08

2026-10-02 UTC. 기존 DEV-07 프로젝트/Content DB와 PROJECT_STATUS·CONTENT_GUIDE·DATA_PROGRESS를 확인하고 확장했습니다. 이전 문서는 `Docs/DEV-07_STATUS.md`에 보존했습니다.

**구현은 연결했지만 Linux 환경에서는 Xcode 빌드·Swift type-check·실제 iPhone 키보드/음성·XCTest 실행을 검증할 수 없습니다. 출시 검증 완료를 뜻하지 않습니다.**

## 구현한 사용자 경로

`学ぶ → 活用 · 自分で入力する → 실제 동사/형용사 선택 → 기본형/일본어 의미/어간/활용형/설명 → 입력 → 제출 → 정오답·띄어쓰기 피드백 → 다음 문제 → 틀린 문제 한 번 재확인 → 완료`입니다. 기존 예문으로 만든 빈칸·통제된 일본어→한국어 문장 문제를 포함합니다.

현재 **기존 production 어휘 16개 / 직접입력 문제 49개**입니다. 신규 어휘·문법·예문은 0개입니다. 3개 production 예문을 각각 빈칸/문장 입력으로 사용했습니다. 별도 dummy 단어 배열이 없습니다. 어휘 선택 목록은 실제 questions→vocabulary 관계를 조회하며 최대 30개씩 가져옵니다. 한 단어 세션은 최대 20문제입니다.

대상: 가다, 먹다, 보다, 오다, 주다, 마시다, 공부하다, 좋다, 크다, 어렵다, 걷다, 받다, 모르다, 낫다, 살다, 어떻다. UI는 검수된 문제가 존재하는 이 목록만 제공합니다. 미검수 전체 어휘에 자동으로 출제하지 않습니다.

## 활용 엔진

`LearningEngine/ConjugationEngine.swift`는 lemma + 품사 + 기존 irregular_type + target form + optional override를 받아 필요한 형태 하나만 생성하는 순수 서비스입니다. 앱 시작 시 모든 어휘의 활용을 생성하지 않습니다. 미래 단어 상세에서도 같은 API를 사용할 수 있습니다.

지원 target 9종: 현재 아요/어요/해요, 과거 았어요/었어요/했어요, 미래 (으)ㄹ 거예요, 안 부정, 지 않아요, 고 싶어요, 고, 아/어서, (으)면.

- 한글 완성형 음절을 분해/조합하여 받침·모음 조화·축약·과거 ㅆ·(으)/ㄹ을 처리합니다.
- ㅂ/ㄷ/르/ㅅ은 metadata가 지정한 경우에만 변형합니다. 같은 받침의 규칙 동사는 바꾸지 않습니다. ㄹ 받침의 미래/조건, 으 탈락을 처리합니다.
- 하다형은 기존 other metadata와 어간 하를 함께 확인합니다. 다른 other/u/reu_special 등은 추측하지 않고 오류를 반환합니다.
- **ㅎ의 아/어 계열은 lexical override 필수**입니다. 현재 어떻다→어때요/어땠어요의 검수값을 제공합니다. ㅎ 전체에 단일 모음 규칙을 억지 적용하지 않습니다.
- **하다 복합어의 안 부정은 override 없이 생성하지 않습니다.** 공부하다→공부 안 해요처럼 단어 내부 경계가 필요하기 때문입니다. 현재 안 부정 문제는 가다에 한정했습니다. 푸다도 override 없이 일반 ㅜ 축약으로 생성하지 않습니다.
- 희망은 동사만 허용합니다. 형용사에 고 싶다를 붙이지 않습니다. 형용사의 미래 형태는 의지로 단정하지 않고 ‘予定・見込み’로 표시합니다.
- 서비스가 가능한 기본 형태를 생성하더라도 이 배치 밖 모든 lemma의 정확성을 인증한 것은 아닙니다. 새 출제 어휘는 metadata/예외/accepted answers를 검수하고 테스트해야 합니다.

규칙 확인 참고: 국립국어원 [한글 맞춤법/어문 규범](https://www.korean.go.kr/kornorms/m/m_regltn.do), [ㅂ 불규칙 돕다/곱다 설명](https://korean.go.kr/front/mcfaq/mcfaqView.do?mcfaq_seq=8733&mn_id=216&pageIndex=31), [ㅎ 불규칙 설명](https://www.korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=27&pageIndex=1&qna_seq=329865). 내용을 복제한 사전 데이터셋이 아니라 자체 편집 문제입니다. 외부 교육 전문가 감수는 미완료입니다.

## 콘텐츠·문법 연결

기존 questions.text_input, answer_json.accepted, rubric_json, content_links를 사용합니다. 원본은 기존 `Content/production.json`, 런타임은 읽기 전용 `Resources/content.sqlite`입니다. Content schema 3 유지 / **content 9 / reader 6**입니다. 새로운 독립적인 활용 DB는 없습니다.

rubric에는 production=1, form, mode(form/blank/sentence), spacing_warning, overrides를 사용합니다. question_target은 실제 vocabulary UUID입니다. 빈칸/문장 문제는 기존 example과 related 관계, 희망·연결·이유·조건은 기존 grammar와 prerequisite 관계를 가집니다. 학습 화면에서 연결된 문법을 기존 GrammarExplanationView로 펼쳐 보고 전체 문법 과정으로도 이동할 수 있습니다.

이번 단계는 선수 문법 완료 여부로 문제를 잠그지 않습니다. 각 문제 전에 형태를 학습하는 단계를 둡니다. prerequisite 관계는 향후 course progress 기반 pool 선택의 확장 지점입니다. 자동 선수학습 필터가 구현되었다고 주장하지 않습니다.

새 질문/관계 추가로 기존 vocabulary·example·grammar **23개 항목의 revision을 1씩 증가**시켰습니다. 기존 본문/UUID/배포 정렬키는 변경하지 않았습니다. revision 목록은 `Content/dev08-revised-ids.json`, 신규 질문 목록은 `Content/production-drill-ids.json`입니다. 둘은 검수 색인이며 런타임 소스가 아닙니다. 기존 v8 DB는 `Tests/Fixtures/content-v8-production.sqlite`에 보존합니다.

## 입력 판정·학습·재시도

ProductionAnswer는 Unicode NFC, 앞뒤 공백, 연속 whitespace를 정규화합니다. 철자/조사/어순/문장부호를 임의로 삭제하지 않습니다. 빈 답은 제출할 수 없고 입력 상한은 500자입니다. 단순 오탈자를 정답으로 인정하지 않습니다.

accepted에 있는 답만 정답입니다. 봐요/보아요, 마셔요/마시어요 등 이 범위의 자연스러운 대체 활용을 명시했습니다. 문장 문제는 사용할 어휘·순서·종결형·구두점 조건을 안내하는 **통제된 생산**이며 자유번역 채점이 아닙니다. 표현 조건이 다른 자연스러운 문장 전체를 판별하지 않습니다.

spacing_warning=true일 때 띄어쓰기만 다르면 ‘内容は合っています。分かち書きを確認しましょう’로 별도 표시합니다. 정답으로 위장하지 않고 재확인 대상 및 incorrect 이벤트로 저장하며 session result=spacing도 보존합니다. strict 설정이면 그대로 오답입니다.

정답/오답 확인 후 사용자가 次へ를 누릅니다. 틀린 질문은 첫 묶음 뒤 **최대 한 번** 재확인합니다. 재시도 중 다시 틀려도 무한 반복하지 않습니다. 짧은 세션 끝에서는 간격이 짧을 수 있으며 재입력 성공을 영구 습득으로 처리하지 않습니다. 질문별 순서는 저장된 UUID snapshot을 유지합니다. 여러 lemma를 자동 섞는 배치 drill은 이번 범위에 넣지 않았습니다.

## 저장·재개·SRS

같은 UserProgress DB/repository에 additive **schema v7** migration으로 production_sessions만 추가했습니다. 기존 backup/transaction migration을 사용하며 기존 한글·발음·어휘·문법·SRS 테이블을 초기화하지 않습니다.

세션은 vocabulary scope, 질문 snapshot(대상 lemma/form/정답/예외 결과/문법 연결), content version, 현재 위치, 학습/입력 단계, 답안·판정 피드백, 오답 queue, 재시도 여부, revision을 저장합니다. 제출/다음 전환은 revision 검사 및 transaction으로 처리합니다. 앱 재시작과 콘텐츠 재정렬 후 active 세션을 그대로 복구합니다. **제출 전 미완성 입력은 저장하지 않으며 제출된 답은 저장**합니다.

생산 결과는 기존 study_events에 skill=`production_<form>`의 correct/incorrect로 기록하므로 recognition과 구분할 수 있습니다. contentRevision에는 실제 vocabulary revision을 기록합니다. Hint 기능은 이번에 제공하지 않습니다.

입력 결과가 생긴 lemma는 기존 vocabulary SRS에 등록합니다. existing StepReviewScheduler를 그대로 호출하고 ON CONFLICT DO NOTHING으로 기존 일정/단계를 유지합니다. 현재 `今日の復習`에서는 해당 어휘의 의미 회상으로 이어집니다. **직접입력 전용 due queue·오답 기반 기존 SRS 재스케줄링은 미구현**이며 typed events가 다음 확장 지점입니다. 별도 SRS 구현을 복사하지 않았습니다.

## UI·오디오

Native ScrollView/TextField/FocusState, 키보드 submit과 閉じる, 문제 전환 시 입력 초기화, 학습 중 Tab Bar 숨김, 충분한 터치 영역과 일본어 label을 사용합니다. 시스템 배경/Dynamic Type/기존 accent를 유지하고 애니메이션·카드 장식을 추가하지 않았습니다. 키보드가 올라오면 native layout과 스크롤로 답안/버튼을 볼 수 있게 구성했습니다. 실제 기기 레이아웃 검증은 남아 있습니다.

기존 KoreanAudioService normal/slow/stop을 재사용합니다. 생성된 한국어 형태나 accepted 한국어만 전달하고 일본어 설명/기호는 읽지 않습니다. 음성 미설치와 재생 오류 안내를 표시합니다. 화면 전환 시 정지합니다.

## 검증 결과

- Production Validator **오류 0 / 기존 검토 경고 10**. reader/form/대상 품사·ID/metadata 충돌/override/빈 정답/중복 accepted/세션 크기를 추가 검사합니다. 규칙을 끄지 않았습니다.
- 새 관계가 기존 fingerprint에 영향을 주어 초기 검증이 revision 필요 오류 23개를 냈습니다. 해당 항목 revision을 올려 해결했습니다. 기존 보존 테스트는 승인된 23개만 구분하고 신규 테스트가 그 변경 집합·revision·기존 모든 본문 보존을 정확히 검사합니다.
- **Python/SQLite 142개 통과**. 기존 핵심 회귀 포함. 신규 pool/관계/버전/실제 query/이전 payload·ID/비파괴 migration/디스크 snapshot/잘못된 입력 거부를 검증했습니다.
- **Swift 58파일 tree-sitter 구문 오류 0**. 프로젝트 참조·plist/XML·SQLite integrity/FK 통과.
- Native XCTest는 활용/불규칙과 규칙 반례/9 target/예외·범위 거부/입력 정규화·띄어쓰기·복수 정답/production DB→저장·retry·SRS·cold resume 5개를 추가하여 **71개 작성, 미실행**입니다.
- Xcode build, Swift type-check, 실제 Swift 엔진 실행, 키보드·VoiceOver·TTS 청취·iOS 재시작 검증은 **미수행**입니다. Python SQL 통과를 활용 엔진의 실제 실행 통과로 주장하지 않습니다.

로그: Docs/DEV08_CONTENT_REPORT.json, TEST_RESULTS_DEV08.txt, STATIC_CHECKS_DEV08.txt. Mac 절차: Docs/VALIDATION_DEV08.md.

## 주요 파일·미완성 감사·DEV-09

새 코드: LearningEngine/ConjugationEngine.swift, Models/ProductionModels.swift, Repositories/SQLiteProduction.swift, Views/ProductionView.swift, Resources/user-migration-v7.sql, Tests/ProductionLearningTests.swift, Tools/ContentBuilder/test_production_content.py. 기존 protocol/Home/migration/reader/Validator/project/source/DB를 최소 확장했습니다.

이번 신규 코드에 TODO/FIXME/placeholder는 없습니다. 학습 시작/제출/다음/재시도/음성/문법 펼치기/다시 학습은 실제 경로에 연결했습니다. 다만 ‘네이티브 실행 검증 미수행’은 해결되지 않은 출시 전 검증 항목입니다.

DEV-09 시작 전에 Mac에서 71개 XCTest, Debug/Release, v6→v7 업데이트, 한국어 IME 조합 중 제출, 키보드 가림/닫기, 선택·오답·재시도 직후 강제 종료, 기존 grammar/vocabulary SRS를 확인해야 합니다. 실제 활용 engine 테스트 실패가 있다면 신규 기능보다 먼저 수정하세요.

지원하지 않는 범위: 자유 작문/LLM 채점, 문장 배열, Hint, 모든 존댓말·고급 활용, 모든 어휘의 무검수 자동 출제, 생산 전용 SRS 큐, 자동 선수학습 잠금, 멀티 lemma 세션. 현재 seed 밖 불규칙/안 부정/축약 대체형은 DATA 검수와 테스트 후 추가합니다. 다음 콘텐츠 배치는 v9를 previous로 보관하고 content 10 이상으로 올리며 UserProgress를 재생성하지 않습니다.
