# PROJECT_STATUS — DEV-09

2026-10-02 UTC. DEV-08 프로젝트·문서·production DB를 확인하고 기존 구조에 듣기를 연결했습니다. 10월 2일 10:11–10:44 UTC에 구현·검증·문서화를 진행했고, 중단 후 10월 3일 최종 검토·패키징을 마무리했습니다. 이전 상태는 `Docs/DEV-08_STATUS.md`입니다.

**Linux에서는 Xcode build, Swift type-check, XCTest, iPhone 음성·키보드·VoiceOver를 실행하지 못했습니다. 아래는 구현과 수행한 SQL/구문 검증 결과이며 출시 검증 완료를 의미하지 않습니다.**

## 구현 경로

`学ぶ → リスニング → 入門 / 初級 → 練習 1 → 手動再生 → 意味選択 / 韓国語選択 / 書き取り / 文理解 → 判定 → 次へ → 間違えた問題を一度再確認 → 完了`입니다. 받아쓰기 화면은 한국어 직접입력과 정답/사용자 입력 비교를 제공합니다. 원문은 제출 후에만 View에 생성합니다. 한국어 선택형에서는 당연히 후보 문장들이 보이지만 정답 여부는 공개하지 않습니다.

기존 production examples **24개**를 참조하는 listening_items **24개**, questions **24개**를 추가했습니다. **入門 12 / 初級 12**, 네 유형이 각 레벨에 3개씩입니다. 신규 어휘·문법·예문은 0입니다. 기존 문장/번역을 복사한 별도 source가 없고 앱은 번들 SQLite를 조회합니다. 선택한 문장과 일본어 피드백은 `Docs/DEV09_LISTENING_CATALOG.md`에 있습니다. 외부 전문가 감수·실제 TTS 청취 검수는 미수행입니다.

## Content architecture / version

같은 `Content/production.json → Validator → Resources/content.sqlite` 경로입니다. **Content schema 4 / content 10 / reader 7**입니다. schema 3의 listening_items는 녹음 asset과 복사된 transcript를 필수로 요구하므로 source example 참조/TTS를 올바르게 표현할 수 없어 최소 확장했습니다.

- listening_items에 source_example_id, audio_mode(tts/recorded_required), learning_order 추가. audio_asset_id와 transcript_ko는 nullable입니다. source 참조형에서는 transcript_ko를 null로 유지하고 examples.korean/japanese를 읽습니다.
- TTS는 example의 정식 한국어를 사용합니다. 녹음 전용은 검수된 media_assets를 사용하고 없는 파일을 TTS로 몰래 대체하지 않습니다.
- 기존 questions.listening_choice/listening_input, question_choices, answer_json, rubric_json을 사용합니다. listening_task=meaning/korean/dictation/comprehension. 듣기 항목 하나에 문제 하나를 연결합니다.
- vocabulary/grammar 연결은 source example의 기존 vocabulary_examples/grammar_examples로 추적할 수 있습니다. 별도 단어/문법 목록을 복제하지 않았습니다.
- content_links에 listening→example related 관계를 추가했습니다. 기존 example **24개는 revision만 +1**, ID·본문·번역은 유지했습니다. `Content/dev09-revised-ids.json`이 승인 목록입니다. 기존 v9 DB를 `Tests/Fixtures/content-v9-production.sqlite`에 보존했습니다.
- Content DB는 교체 가능한 read-only 파일이므로 in-place SQL migration을 실행하지 않습니다. reader 7은 schema 2/3도 계속 읽습니다. 구 reader는 v4 package를 거부합니다. 기존 사용자 DB에는 Content FK가 없습니다.

## 세트·문제·입력

레벨별 고정 editorial learning_order를 20개 구간으로 나눕니다. 카탈로그는 30세트씩 keyset 조회, 세션은 최대 20문항입니다. 현재 각 레벨은 12문항 한 세트입니다. 새 자료는 기존 order를 바꾸지 않고 뒤에 붙입니다. 이미 시작한 세트는 저장된 UUID/본문/선택지 snapshot을 계속 쓰므로 새 자료를 중간에 끼워 넣지 않습니다. SRS는 최대 20개 due ID만 읽습니다.

선택형은 기존 ChoiceJudgement, 선택지 순서는 기존 seed 기반 QuizOptions를 재사용합니다. 새 세션에서 seed를 새로 만들고 실제 선택지 순서를 저장합니다. 복원 때 재셔플하지 않습니다.

받아쓰기는 **DEV-08 ProductionAnswer**를 그대로 씁니다. NFC·앞뒤 공백·연속 공백만 정규화합니다. 받침/모음/조사 오류와 의미만 같은 다른 문장은 정답으로 인정하지 않습니다. 현재 accepted는 원문과 마침표 생략형만 명시했습니다. 띄어쓰기만 다르면 spacing으로 독립 피드백하고 완전 정답으로 세지 않습니다. 입력 상한 500자, 빈 입력 제출 금지입니다. 원문/일본어 번역/사용자 입력/설명을 제출 후 보여주며 한글 단순 문자 diff는 넣지 않았습니다.

오답·spacing은 첫 묶음 종료 뒤 **최대 1회** 재시도합니다. 즉시 같은 회독 안에 재삽입하지 않습니다. 짧은 묶음이나 마지막 문항은 재노출 간격이 짧을 수 있습니다. initial correct/wrong과 retry success를 분리하고 retry는 SRS stage를 올리지 않습니다.

## UserProgress / resume / 통계

기존 SQLiteProgressRepository와 같은 UserProgress 파일에 **v8 additive migration**을 적용합니다. 기존 backup/transaction 정책을 유지합니다.

- listening_sessions: scope, session UUID, 최대 20문항 snapshot, content version, position, retry queue, retry 여부, heard 여부, 제출 답안/판정, revision, 시작/최근 시각, correct/wrong/retrySuccess, 재생/slow 횟수, 완료 상태.
- listening_plays: 세션·문제별 **끝까지 완료된 재생**의 normal/slow 횟수와 최근 시각. 재생 시작/실패/중단은 성공 재생으로 세지 않습니다.
- listening_attempts: item/question UUID, 유형, 최초/재시도, 입력/선택, 판정, review 여부, 시각, 실제 변경된 next_due_at.
- 기존 study_events/item_progress/daily_statistics에 listening_<task> 또는 listening_retry로 기록합니다. 통계 SDK는 없습니다.

저장된 revision을 다시 읽어 비교하고 답안/이벤트/SRS/session을 한 transaction에 저장합니다. 중복 제출과 오래된 화면의 전이를 거부합니다. 제출 결과, 현재 문제, 재생 완료 여부, 남은 문제, 오답 queue를 cold reopen으로 복구합니다. **제출 전 입력 초안과 재생 위치는 저장하지 않습니다.** 앱 재진입 후 수동으로 처음부터 다시 들을 수 있습니다. 기록 오류 시 자동 초기화하지 않고 다시 읽기 버튼을 제공합니다.

## SRS 실제 연결

같은 srs_state와 기존 StepReviewScheduler/calendar_steps v1을 사용하며 skill=`listening`, content_id=listening item UUID입니다. Vocabulary/Grammar 일정과 충돌하지 않습니다.

- 첫 제출은 정오답과 무관하게 stage 0, 다음 날 복습으로 등록합니다.
- 일반 연습을 다시 풀어도 이미 있는 SRS 날짜/단계를 덮어쓰지 않습니다.
- 예정일이 되면 홈 今日の復習에 듣기 진입 행을 표시합니다. 듣기 메뉴에서도 전체 due 수와 active review를 확인합니다.
- 복습 세션의 **최초 판정**에서 correct→remembered, spacing→unsure, incorrect→difficult를 기존 스케줄러에 전달합니다. 1/3/7/14/30/60/120일 정책을 복사하지 않았습니다.
- 같은 세션 retry는 SRS를 다시 갱신하지 않습니다. 재시도 성공을 장기기억 성공으로 처리하지 않습니다.
- due_at<=현재 instant 쿼리, 최대 20개, (skill,due_at,content_id) 인덱스. 나머지 backlog는 그대로 남습니다.
- 기존 UTC instant 저장/판정 당시 timezone의 calendar-day 계산을 유지합니다. 다음 날부터 복습하며 시간대를 바꿔도 기존 due instant를 재작성하지 않습니다.

미래 다른 예문에서 같은 어휘/문법을 듣게 할 연결은 source example 관계로 가능합니다. **서로 다른 문장 간 자동 mastery 전파/적응형 선정은 미구현**입니다. 특정 문장을 잘 기억한 것과 듣기 능력 전체를 동일시하지 않습니다.

## Audio / UI / 접근성

기존 KoreanAudioService, AudioPolicy normal/slow/stop과 ko-KR voice 확인, 녹음 파일 경로·checksum 검증을 재사용했습니다. 오디오 서비스 구현은 변경하지 않았고 RecordingAsset에 snapshot용 Codable만 추가했습니다.

자동재생하지 않습니다. 사용자가 재생 버튼을 누르며 시스템 playback/spokenAudio 정책에 따라 무음 스위치 상태에서도 소리가 날 수 있습니다. 실제 완료 callback을 받은 뒤에만 답을 제출할 수 있습니다. 전화/Siri interruption·이어폰 제거는 기존 backend가 중단/실패 처리하고, 새 화면은 inactive/background/화면 이탈 시 stop합니다. background audio mode·마이크 권한을 추가하지 않았습니다.

한국어 voice 부재, 파일 누락, 재생 실패는 안내하고 상태를 보존합니다. 음원이 없는데 제출을 강제로 허용하지 않습니다. 자모 TTS 금지 정책도 그대로입니다.

일본어 native List/ScrollView/TextField, 시스템 배경, 기존 accent, Dynamic Type, 충분한 터치 영역, 하단 제출/다음, 키보드 닫기와 스크롤을 사용합니다. 장식·효과음·애니메이션은 없습니다. 정답 원문/번역은 답 제출 전 accessibility tree에도 생성하지 않습니다. 실제 VoiceOver/TTS 동시 사용과 작은 화면·큰 글꼴은 Mac/iPhone 확인이 필요합니다.

## 검증 결과

- Production Validator **오류 0 / 기존 검토 경고 10**. 기존 5 homograph 후보와 짧은 발음 예시 경고는 그대로입니다.
- 새 검사: listening UUID/FK, active example, source와 level 일치, 레벨 내 order 중복, 오디오 mode/asset/TTS, 문제 1개, 지원 task, 원문 사전 노출, 정답/선택지 중복, Korean 후보의 기존 example 존재, accepted 원문/구두점 변형 제한.
- **Python/SQLite 149개 통과**. 신규 7개 테스트는 각종 잘못된 입력 하위 사례, 원본 payload/24개 승인 revision, 실제 SQL level/ID/batch/due/backlog, v7→v8 비파괴 migration, 저장 후 reopen, 중복 제출 constraint, 기존 다른 skill SRS 보존을 검사합니다. 기존 한글/발음/어휘/문법/활용·입력 SQL 회귀 포함.
- **Swift 62파일 tree-sitter 구문 오류 0**, Xcode 참조/plist/XML/SQLite integrity·FK 확인.
- **Native XCTest 78개 작성, 미실행**. 신규 듣기 6개와 오디오 interruption 계약 1개를 추가했습니다. 정오답/공백/accepted/게이트/유한 retry/재시도 통계/실제 DB snapshot·SRS/native cold resume 등은 Mac 실행 대상입니다.
- **Xcode Debug/Release, Swift type-check, XCTest 실행, 실제 음성 청취/VoiceOver/키보드/강제종료 UI 검증 미수행**. Python SQL 검사를 네이티브 실행으로 표시하지 않습니다.

증거: Docs/DEV09_CONTENT_REPORT.json, TEST_RESULTS_DEV09.txt, TEST_LISTENING_DEV09.txt, STATIC_CHECKS_DEV09.txt. Mac 절차: Docs/VALIDATION_DEV09.md.

## 최종 감사 / 알려진 제한 / DEV-10

새 버튼은 실제 재생·제출·다음·재시도·복습·재개에 연결했고 신규 코드에 TODO/FIXME/placeholder는 없습니다. 임시 Swift 문장 배열·별도 콘텐츠/진도 DB는 없습니다. 오디오 backend·회독/문법/활용 core는 유지했습니다.

미해결 출시 검증: Mac 빌드/type-check/XCTest, 실제 기기 음질/발음·route interruption, VoiceOver가 원문을 미리 읽지 않는지, 한국어 IME·키보드 가림, native 강제 종료/재개. 오디오 없는 기기에서는 해당 듣기를 진행할 수 없으며 다른 학습과 저장 기록은 유지됩니다. 녹음 seed는 0개이고 TTS24개입니다. 외부 교육 감수는 아직 없습니다.

기존 듣기 항목을 비활성화하면 그 SRS 기록은 삭제되지 않습니다. due snapshot을 새로 만들 때 active source를 찾지 못하는 ID는 출제되지 않지만 사용자 DB의 due 수에는 남을 수 있습니다. 많은 항목을 폐기하는 콘텐츠 배포 전에 alias/retired review 정리 정책을 구현해야 합니다. 현재 24개는 모두 active이며 해당 문제는 발생하지 않습니다.

다음 DATA/DEV는 현재 v10을 previous로 먼저 보관하고 content 11 이상을 사용하세요. 기존 UUID/learning_order/started snapshot을 재작성하거나 UserProgress를 재생성하지 마세요. listening_answer variant 확대에는 음성과 철자 일치 검토가 필요합니다. 인식 평가·마이크·서버·자유 AI 받아쓰기·TOPIK 전체는 이번 범위 밖입니다.
