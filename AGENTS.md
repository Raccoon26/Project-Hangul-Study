# HangulStudy 작업 규칙

## Mac 로컬 / Windows에서 시작하는 Codex Cloud 공통 인계 (DATA-10부터)

- 사람의 명시 요청을 받은 DATA 단계만 시작한다. Mac 로컬과 Windows에서 사용하는 Codex Cloud는 같은 `Raccoon26/Project-Hangul-Study`의 서로 다른 checkout이며 로컬 경로·설치 도구·자격증명이 같다고 가정하지 않는다. 기존 checkout을 사용한다.
- 매 작업 시작에 `pwd`, `git status --short --branch`, `git remote -v`, `gh auth status`, 저장소 권한/기본 브랜치, `git fetch origin`, `git rev-parse HEAD origin/main`, ahead/behind를 확인한다. origin이 지정 저장소인지 확인하고 토큰 원문을 기록하지 않는다. 관련 단계 원장·현재 상태·검수/출시 gate를 실제 Source/DB/코드와 대조한다.
- 미커밋 tracked/untracked 변경의 경로·의도를 먼저 조사하고 보존한다. 임의 삭제·stash·덮어쓰기·자동 커밋을 하지 않는다. clean main은 `git switch main` → `git merge --ff-only origin/main`으로 갱신한다. 분기/다른 작업 변경이 있으면 안전하게 분리하거나 충돌을 보고한다. 새 단계는 최신 main에서 `codex/<stage>-<purpose>` 브랜치를 만든다. checkpoint 인계로 같은 단계를 재개할 때는 기록된 기존 브랜치/SHA를 이어가며 새 브랜치를 중복 생성하지 않는다.
- 동시에 두 환경에서 같은 단계/파일을 수정하지 않는다. 작업 중 환경 전환은 현재 브랜치에 검토 가능한 checkpoint commit과 일반 push가 성공한 후 진행한다. 단계 원장에 브랜치/SHA·검사 명령/결과·미완료 항목·다음 행동을 남기고 이전 환경의 수정을 중단한다. push 실패 시 전환 완료로 보고하지 않는다. 다음 환경은 fetch 후 해당 원격 브랜치/commit을 확인하고 이어간다. checkpoint를 main 완료/검증 통과로 간주하지 않는다.
- 단계 종료에는 허용 범위의 diff·데이터/fixture 보존·관련 테스트를 확인하고 Commit → 일반 Push → main 대상 PR → 필수 checks/CI·mergeability 확인 → 정상 merge 순서로 전달한다. 이 요청처럼 병합까지 명시 위임된 작업은 재확인 없이 진행한다. 보호규칙/실패한 필수 CI를 우회하거나 admin 강제 병합하지 않는다. CI/check가 없으면 ‘없음’으로 기록하고 로컬 결과와 구분한다. 인증·권한·CI·충돌 등으로 중단되면 실제 원인과 필요한 조치를 남긴다.
- 병합 후 clean checkout에서 main으로 이동해 fetch/ff-only 갱신하고 `git rev-parse HEAD origin/main`의 전체 SHA 일치와 status를 확인한다. PR URL·merge SHA·검사 결과/남은 gate를 최종 보고한다. 자기 merge SHA를 포함하려고 사후 문서 커밋을 반복하지 않는다. 최종 Git/PR과 응답을 인계 근거로 쓴다. 다음 환경은 로컬의 옛 main을 신뢰하지 않고 다시 fetch한다.
- force push, 파괴적 reset/clean, 이력 재작성, 기존 Production/fixture 삭제, 데이터 축소를 통한 전달 우회를 금지한다. Xcode/Simulator 유무는 환경별로 다시 확인한다. Cloud portable PASS를 Mac native PASS로 바꾸지 않으며 설치되지 않은 native/실기기 gate는 BLOCKED로 유지한다.
- Python/SQLite 버전과 `PRAGMA compile_options`도 확인한다. DATA10-1 당시 배포24는 SQLite3.53.1의31테이블이다. Mac SQLite3.44.0의 ENABLE_STAT4 재구성은 같은31테이블의 행이 일치해도 추가 sqlite_stat4 때문에32테이블·SHA가 다르다(`Docs/DATA10_REBUILD_COMPARISON.json`). 이를 byte-exact PASS로 표시하거나 시스템 통계 테이블을 임의 삭제/검사 완화해 맞추지 않는다. 임시 재구성만 비교하고 Production을 보존하며, 실제 후속 배포 전 동일 writer 버전/compile profile의 재현 환경을 확인한다.

## DATA-10-3 Listening Batch B 현재 기준

- 명시 요청으로 Content26/Schema4/reader7/UserProgress10에 신규 상황60개·내용이해60/받아쓰기60을 반영했다. 감정8/의견8/판단7/이유7/결과7/경험8/계획8/의견차이7이며 DATA10 누적120원문/240문제다. 전체 목표150~250/300~500을 유지한다. 다음 Batch는 자동 시작하지 않는다.
- 실제 직전25 source.gz/DB fixture를 보존했다. A 정확한24→25 gate는 frozen25에 고정하고 B25→26 gate가 기존16,241개 fingerprint·본문/ID/revision/order/membership 불변과 신규300UUID를 검사한다. 기존 revision 승인 목록은 빈 배열이다. 다음 실제 변경은 현재26을 previous로 먼저 보존한다. prepare_data10_b는 고정25→26만 재현하는 도구이며 후속 Production을 덮어쓰는 importer가 아니다.
- 신규 source60/추가 참조60/Listening120/Question120을 구분한다. learning_order2180~2299(batch109~114), source 두유형은3구간 차이다. 기존 번호·부분구간·session snapshot을 재작성하지 않는다. 원문 단위 SRS 병합·새 topic UI를 구현했다고 주장하지 않는다.
- 전단일화자TTS/녹음0이며 인용도 같은 TTS로 읽는다. 다화자 실녹음/목소리·재생을 가장하지 않는다. prompt_ko=null, Transcript는 기존 result 이후 생성한다. Dictation accepted는 정확한 원문1개, 끝 .!? 생략과 내부부호/철자·spacing을 구분하고 일반 입력을 완화하지 않는다.
- 최신 근거는 DATA10_PROGRESS §3 / Docs/DATA10_B_*다. 54문법 재사용은 AI 문맥 용례 매핑이며 기존 Grammar 관계/선행163건의 일괄 해결/재사용 승인으로 해석하지 않는다. 한일/문제 AI 자체 검수와 독립 사람·실제TTS 검청 NOT TESTED를 구분한다.
- 최종 portable382 PASS/Source68,586행/31테이블·SHA 재현은 iOS 실행이 아니다. 현재Cloud Build/XCTest143정의·실행0 BLOCKED, 이전Mac의142실행137PASS/5FAIL은 역사 근거로 유지하며 활용P1·구매cache 등 미해결 gate/Release B—Conditional을 보존한다. 다음 Mac은 최신main과 환경을 동기화하고 실제 native 결과로만 상태를 바꾼다.

## DATA-10-2 Listening Batch A 현재 기준

- 명시 요청으로 初中級 신규 상황60개/문제120개를 Content25에 추가한다. 의미18/한국어12/받아쓰기30/내용이해60, 전TTS이며 녹음0이다. 일상·약속변경·교통·쇼핑·서비스·부탁/거절 각10원문. 기존 원문 source 재사용0, 신규 원문마다 Example1/Listening2/Question2이며 원문 수에 내부 문장/오답/반복 참조를 합산하지 않는다. 전체 DATA10 목표150~250/300~500은 유지한다.
- Content24 원본/DB를 불변 fixture로 보존했다. 기존 모든 payload/ID/revision/created_at/learning_order/membership 변경0이다. 신규300개 UUID는 `data10-a-authoring.json`에 고정하고 기존 승인 revision 목록은 빈 배열이다. 다음 실제 콘텐츠 변경은 현재25를 previous로 먼저 보존한다. 과거 DATA09 정확한 통합 gate는 frozen24에 고정하고 새24→25 gate가 실제 Production 전체 보존을 검사한다.
- 새 구간은 lower_intermediate learning_order2060~2179(batch103~108), 같은 source 두 유형은3구간 떨어진다. 기존 부분 구간을 채우거나 진행 중 snapshot을 재작성하지 않는다. 자동SRS가 같은 source 두 항목을 모을 수 있는 한계는 남는다. 목록은 기존練習番号이며 새 topic/다화자 UI를 구현한 것이 아니다.
- Mac/Cloud byte writer 환경은 `Docs/DATA10_WRITER.md`/`setup_exact_writer.py`를 따른다. SQLite3.53.1만 같아도 allocator/compile profile로 통계 배치가 다를 수 있다. 격리된 profile에서 frozen24/현재25 전체 byte 비교를 확인하고 검사 완화·통계 삭제·원본 덮어쓰기로 우회하지 않는다.
- Batch Self Review는 assistant 자체 검수다. 독립 사람/교사·실기기/TTS 검청·기존 활용/Purchase gate와 Release B—Conditional은 남는다. 최신 결과는 `DATA10_PROGRESS.md` §2 / `Docs/DATA10_A_*`다. 다음 단계는 자동 시작하지 않는다.

## DATA-10-1 분석 범위

- 2026-10-20 명시 요청으로 PR #17 병합 main에서 DATA10 분석·환경 설정을 시작했다. Content24/Schema4/reader7/UserProgress10·Listening1,936(TTS)·DATA09 수량 완료·Release B—Conditional이 기준이다. DATA09의 사람/실기기/native 잔여 gate는 실제 새 실행 결과에 한해 구분해서 갱신한다.
- 이번은 신규 원문150~250개/문제300~500개의 제작 계획까지만 수행한다. 원문·문제 제작/통합, Production 교체, ID/revision·버전 변경, runtime 버그 수정과 다음 Batch는 포함하지 않는다. 최신 근거는 `DATA10_PROGRESS.md`, `Docs/DATA10_LISTENING_ANALYSIS.md`, `Docs/DATA10_LISTENING_BASELINE.json`이다.
- 같은 원문을 다른 유형에 쓰면 Example은 하나만 보존하고 기존 1 listening : 1 question 계약에 따라 별도 Listening/Question을 연결한다. 새 원문 수·재사용 관계 수·문제 수를 분리한다. SRS는 Listening ID별이며 원문 단위 숙달/중복 자동 병합을 추가하지 않는다. 기존 163후보의36미해결/7조건부를 자동 재사용 승인으로 해석하지 않는다.

## 프로젝트와 기존 요구사항 보존

- 일본어 사용자를 위한 한국어 학습 iOS 앱이다. 기존 DEV-01~14 / DATA-01~07의 요구사항, 코드, 콘텐츠, 테스트, 검수 기록과 미완료 출시 조건을 보존한다.
- 작업 시작 시 `PROJECT_STATUS.md`, `CONTENT_GUIDE.md`, `DATA_PROGRESS.md`, `RELEASE_CHECKLIST.md`, `DATA08_PROGRESS.md` 및 관련 DEV/DATA 감사 문서를 읽고 실제 Git·코드·Production DB와 대조한다. 과거 단계의 수량·버전·완료 표현을 현재 상태로 오인하지 않는다.
- 기존 체크아웃을 사용한다. 각 클라우드 작업은 격리되어 있으므로 사용자가 요청하지 않은 Git worktree를 만들지 않는다. 기존 미커밋 변경을 먼저 조사하고 보존한다. 강제 푸시·파괴적 초기화로 문제를 우회하지 않는다.
- Content/UserProgress 분리, 한글·발음, 어휘 회독·SRS, 문법, 활용·직접입력, 듣기·받아쓰기, Curriculum·진단, 검색·저장, 통계·유지학습, 설정·알림, 광고·일회성 광고 제거의 기존 동작을 유지한다. 별도 학습 엔진·진도 DB·새 서비스로 우회하지 않는다.

## DATA-08 범위와 단계 기록

- 전체 목표는 **신규 어휘 800~1,200개, 신규 문장 예문 1,300~2,000개**다. 임의로 축소하거나, 기존 항목·관계 수·fixture·중복·활용형·미검수 초안을 신규 수량으로 계산하지 않는다. 예문 재사용은 관계 증가로 별도 집계한다.
- DATA-08-1은 상태 조사와 기록만 수행한다. 콘텐츠 추가·수정·삭제·DB 교체·버전 증가·버그 수정은 후속 단계의 명시된 범위에서 수행한다.
- 이후 각 단계/Batch의 시작·종료 수량, 실제 증가, level별 분포, 검수, Validator 경고, 테스트의 실행/통과/실패/건너뜀, 버그의 발견/수정/미해결, Git 상태를 `DATA08_PROGRESS.md`에 누적한다. 기존 기록을 지우거나 결과를 덮어쓰지 않는다.
- DATA-08-1 기준은 Content14 / Schema4 / minReader7 / UserProgress10이다. 이후에는 항상 실제 metadata/코드를 다시 확인한다. 데이터 추가만으로 schema/reader/UserProgress 버전을 올리지 않는다.

## Stable ID·원본·DB 무결성

- Runtime 원본은 `Content/production.json` → 기존 ContentBuilder → `Resources/content.sqlite`이다. 앱은 번들 DB를 read-only로 읽는다. `Content/*ids.json`은 검수 색인이며 runtime 원본이 아니다. fixture와 `Resources/.content-*.sqlite` 같은 임시 파일을 Production으로 선택하지 않는다.
- 실제 신규 엔티티는 canonical 소문자 UUID를 한 번 발급해 저장한다. 표제어·번역·배열 순서·rowid·sort_key에서 ID를 다시 만들지 않는다. 기존 ID, kind, created_at, sort_key, learning_order, lesson membership 및 사용자 session snapshot 순서를 보존한다.
- 본문·metadata·관계를 바꾸면 같은 ID의 revision과 updated_at을 갱신한다. 관계에 참여하는 모든 끝점에 기존 fingerprint/revision 정책을 적용하고 변경 승인 ID 목록을 남긴다. kind 변경·ID 재활용·배포 데이터의 물리 삭제는 금지한다.
- 비활성화가 별도로 승인된 경우에도 tombstone/상세 행/사용자 이력을 보존하고 active review의 retirement 복구 정책을 먼저 확인한다. 현재 자동 skip/reconcile 미구현을 알고도 대량 비활성화하지 않는다.
- 콘텐츠 갱신 시 실제 직전 배포 DB를 보존하고 `--previous` strict gate를 통과시킨다. DATA-08 첫 콘텐츠 갱신은 현재 Content14를 보존한 후 Content15 이상을 사용한다. 이번 조사 단계에서 v14 fixture를 만들거나 DB를 다시 배포할 필요는 없다.
- 임시 candidate에 build → Validator → `PRAGMA integrity_check` / `foreign_key_check` → 원본/DB 대조 및 기존 ID 보존 확인 → 통합 검증 → 검수 완료 DB만 배포한다. 입력/직전 배포 DB를 출력으로 덮어쓰지 않는다.
- UserProgress를 콘텐츠 업데이트에 맞춰 재작성·삭제하지 않는다. SRS due, 즐겨찾기, 기존 세트 membership, 진행 중 회독·문법·직접입력·듣기 snapshot, 설정·Curriculum·학습 이력을 보존한다.
- DATA08-7의 복습 가용성 보류는 원래 review_items/SRS/판정을 남기는 versioned metadata다. 현재 카드의 명시적 보류와 새 듣기 due page의 확정 누락만 허용하고, Content Version 변경 시 원래 due로 재확인한다. completedCount/deferredCount를 구분하며 보류를 학습 완료로 세지 않는다. 기존 고정 회독/레슨 ID를 이 정책으로 자동 대체하지 않는다.
- 받아쓰기 끝 .!? 생략과 내부 철자·문장부호·띄어쓰기 차이를 구분한다. 일반 직접입력/문장 생성 판정까지 정규화를 확대하지 않는다.

## Batch 검수·중복 방지·한국어/일본어 품질

- 전체 목표를 유지하면서 검수 가능한 Batch로 나눈다. 각 Batch마다 기존 전체 DB와 신규 Batch 내 후보를 비교하고, 작성 후 별도의 재독·수정·재검증을 거쳐 통합한다. 실패 행을 조용히 버리고 성공으로 보고하지 않는다.
- 어휘/뜻/예문/설명/문제/정답/오답 선택지를 모두 검수한다. 검수 범위·수량·수정 사례·미해결 사항과 검수 주체를 기록한다. assistant 재독을 독립 원어민·교육 전문가 승인으로 표현하지 않는다.
- 한국어는 자연스러운 상황·기본형·품사·띄어쓰기·높임말·시제·의미별 용법·활용 규칙을 확인한다. 일본어는 자연스러운 문장으로 원문의 의미·시제·존대·의도를 보존한다. 사전 확인이 필요한 분류·불규칙·뉘앙스에는 근거를 남긴다.
- 의미별 ordinal과 예문 관계를 정확히 연결한다. 한일 문장 쌍이 같으면 기존 Example ID를 재사용한다. 동형어/다의어는 자동 병합하지 않고 기존 의미와 비교해 판단 근거를 남긴다. 기존 경고를 없애려는 삭제·Validator 완화는 금지한다.
- 한국어/NFC·공백 정규화 표제어, 뜻, 예문·문장 쌍을 중복 조사한다. 단순 활용형·기계적 치환·고유명사·무의미한 짧은 문장으로 수량을 채우지 않는다. 재사용과 신규 문장을 구분한다.
- TOPIK·빈도·발음/녹음·저작권/출처는 추측하지 않는다. 확인되지 않은 선택 필드는 null로 두고 공인 등급·공식 빈도·전문가 인증으로 표시하지 않는다. 데이터 출처와 실제 이용 권한을 기록한다.
- 서술어/expression의 has_batchim은 기존 계약대로 null, expression irregular_type은 null이다. 하다형·불규칙·override는 `CONTENT_GUIDE.md`와 실제 엔진 계약을 따른다. Python 검사로 Swift 활용 실행을 대체 인증하지 않는다.
- 듣기는 기존 active Example ID를 참조하고 문장을 복제하지 않는다. level·learning_order·관련 끝점 revision을 지킨다. 문항당 정답은 명확해야 하며 답 공개 전 transcript가 UI/VoiceOver에 노출되지 않아야 한다.

## 통합 검사와 결과의 한계

- 후속 콘텐츠 Batch마다 strict Validator/이전 배포 비교, 실제 DB count와 level 분포, UUID/FK/중복·고아 참조, source/DB 일치 및 기존 payload/허용 revision 차이를 확인한다. 경고는 건수·내용·검토 근거를 유지한다.
- 프로젝트 루트에서 `sh Tools/verify.sh --portable`을 사용한다. 어휘 카드→세트→회독→SRS→복습, 문법·직접입력·듣기, 검색/상세/즐겨찾기, 통계·유지학습, 이전 Content 교체 후 부분 session/사용자 기록 보존을 관련 기존 테스트로 확인한다. 실패를 숨기려고 assertion/validator를 비활성화하지 않는다.
- Mac에서는 실제 설치된 iOS17+ Simulator의 `TEST_DESTINATION`을 지정해 `sh Tools/verify.sh`로 native build/XCTest를 수행한다. 실기기 음성·접근성·중단 재개·비행기 모드·광고·구매는 `RELEASE_CHECKLIST.md`에 따라 별도 확인한다.
- 검사 결과는 실행 환경·명령·실행 수·종료 상태를 기록한다. portable/SQL/정적 소스 검사는 Swift type-check·Xcode build·UI·StoreKit·실기기 검증이 아니다. 미실행 gate가 있으면 출시 승인/전체 완료로 표현하지 않는다.

## 3~10분 학습·Offline-first

- Home/Continue에서 짧게 시작·중단·재개할 수 있어야 한다. 판정마다 transaction 저장, 부분 완료와 전체 완료 구분, 답 공개 전 자기판정 방지, 중복 제출/등록 방지, 기존 5/10/20개 복습 설정과 bounded query를 유지한다.
- 콘텐츠를 추가했다는 이유로 세트/세션을 강제로 늘리거나 학습시간을 보장한다고 주장하지 않는다. 문장·설명을 작은 화면에서 읽을 수 있게 구성하고 선택적 단어/문법 음성을 필수로 바꾸지 않는다. 듣기에는 재생 완료/stop/화면 종료 정책을 유지한다.
- 콘텐츠·진도·검색·복습은 로컬 SQLite를 기본으로 한다. 로그인·네트워크·광고·결제 성공을 핵심 학습의 전제 조건으로 추가하지 않는다. 검증된 음원/설치된 TTS voice의 가용성을 구분하고 오디오 불가 시 안전하게 안내한다.
- 짧은 학습·재개·시작 위치에 광고를 넣거나 기존 광고 제한을 낮추지 않는다. 학습 저장 후의 기존 완료 경계, 실패 시 nonblocking, verified 광고 제거 권한과 offline cache를 보존한다. 무료/구매 사용자 콘텐츠는 동일하다.
- 실제 iPhone의 3~10분 사용·한 손 조작·큰 글씨·VoiceOver·강제 종료·통화/백그라운드·비행기 모드 검증은 별도 실행 결과가 있어야 완료 처리한다.


## DATA-08-8 종료 기준·대용량 전달

- 현재 검증 기준은 Content19/Schema4/minReader7/UserProgress10, 신규911어휘(일반807/표현104)/고유신규문장1,821, 전체Vocabulary2,287/Example4,597이다. 실제 후속 변경 시 다시 DB를 집계하며 이 숫자를 고정 기대값으로 임의 맞추지 않는다. DATA08 수량·통합 목표와 전체 검수/출시 완료를 구분하고 B—Conditional·native BLOCKED·사람 검수 NOT TESTED를 유지한다. **DATA08 미완료 검증 조건을 해결하기 전 DATA09를 시작하지 않는다.**
- `Content/production.json`·DDL·Importer/Validator·ID registry·검수 근거는 반드시 보존한다. `Resources/content.sqlite`는 재생성 가능한 현재 앱 배포 자산이며 Xcode 계약을 변경하지 않고 추적에서 빼지 않는다. 과거 release fixture는 회귀 계약이다. 새 candidate/synthetic/staging SQLite와 Xcode 빌드 결과는 `/tmp`/ignored 경로에 두고 원본/fixture를 덮어쓰지 않는다. 기존 tracked hidden DB는 이번 작업에서 보존했으며 신규 staging을 배포하지 않는다.
- Git 대용량 오류 전후 tracked 파일과 접근 가능한 history blob 크기를 조사한다. 원본 삭제·데이터 축소·광범위 JSON/SQLite ignore·이력 재작성·force push로 우회하지 않는다. 실제 큰 원본에 필요할 때만 LFS와 checkout/CI/bundle 계약을 함께 검토하고 일반 push의 실제 결과를 확인한다.
- 동일 Content19 재현은18 fixture strict gate와 임시 출력으로 전체31테이블/derived index/schema/index SQL·SHA까지 비교한다. 다음 콘텐츠 변경은 실제 현재19를 previous snapshot으로 보존한다. 문서·감사 도구 변경만으로 Content/Schema Version을 올리지 않는다. 최신 재현/미완료 gate는 `Docs/DATA08_CLOSEOUT.md`와 `DATA08_PROGRESS.md` §16이다.


## DATA-09-1 명시 요청의 분석 범위

- 2026-10-20 사용자가 DATA09-1을 명시 요청했으므로 이번 분석·설계는 앞선 DATA09 착수 보류의 예외다. DATA08의 native BLOCKED/사람 검수 NOT TESTED/B—Conditional을 통과·완료로 바꾸지 않는다. 후속 제작·통합·버전 변경은 이번 분석 요청에 포함하지 않는다.
- 현재 Source/DB는 Content19/Schema4/reader7/UserProgress10·Grammar42/初中級0이다. `DATA09_PROGRESS.md`와 `Docs/DATA09_*`의54단위는 편집 초안이며 Runtime UUID/승인 콘텐츠가 아니다. 장기Grammar/Expressions350~500개를 유지하고 어휘 expression104개나 형태/시제 이형태로 중복 집계하지 않는다.
- 후속 단계는163개 분류(부족147/Level·배치 재검토8/단순검토8)를 해결 수량으로 오인하지 않는다. Level8은 잠정 편집 우려이며 확정 오등급이 아니다. 원문·Example ID·기존42개·기존 Progress/SRS와 DATA08 기록을 보존하고 결과/검증 근거를 DATA09_PROGRESS에 누적한다.


## DATA-09-2 현재 Batch 승인 기준

- 사용자의 DATA09-2 명시 요청에 따라 Batch A18문형/72고유예문/72단일선택 문제를 승인·반영했다. 현재 Content20/Schema4/reader7/UserProgress10, Grammar60/初中級18이다. DATA09-1의54개는 당시 초안이며 이번 영역 조정은12개 선택+6개 추가다. 장기350~500 및 전체 신규45~60 목표를 유지하고 다음 Batch는 자동 시작하지 않는다.
- canonical Source는 production.json 하나다. Content19 source/DB는 불변 fixture에 보존했다. prepare_data09_a.py는19+고정 UUID+검수 authoring으로 동일20만 재현하는 도구이며 후속 데이터를 덮어쓰는 importer로 사용하지 않는다. 다음 실제 콘텐츠 변경은 현재20을 previous로 보존한다.
- 기존12개 관계 끝점 revision 변경은 data09-a-revised-ids.json만 허용한다. 기존 본문/ID/진도/SRS/snapshot/광고·구매 코드를 보존한다. 문형 이형태·고정 표현·질문 재사용으로 수량을 중복 집계하지 않는다.
- 최신 근거는 DATA09_PROGRESS §8 및 Docs/DATA09_A_*다. assistant 한일 재독/portable 통과와 독립 사람·외부사전·Swift/iOS 검증을 구분하고 B—Conditional을 유지한다. 기존163후보를 자동 해결로 집계하지 않는다.


## DATA-09-3 현재 Batch 승인 기준

- 사용자의 명시 요청으로 Batch B18문형/72고유예문/72문제를 반영했다. Content21/Schema4/reader7/UserProgress10, Grammar78/初中級36, DATA09 누적36/144/144이다. DATA08 예문4개 재사용은 신규 수에 넣지 않는다. 전체 신규45~60 및 장기350~500을 유지하고 다음 Batch를 자동 시작하지 않는다.
- Content20 Source/DB fixture와 A 검수 기록은 불변이다. A19→20 정확한 검사는20fixture로 고정하며 B20→21 검사가 모든 구행을 보존한다. prepare_data09_b.py는20+고정UUID+검수 authoring으로 동일21만 재현한다. 다음 실제 변경은 현재21을 previous로 보존한다.
- 기존22개 관계 끝점(Grammar18+Example4) revision+1은 data09-b-revised-ids.json만 허용한다. 기존 본문·ID·배치·Progress/SRS·광고/구매 코드를 보호한다. 새 데이터만으로 Schema/reader/UserProgress를 올리지 않는다.
- 최신 근거는 DATA09_PROGRESS §9 / Docs/DATA09_B_*다. assistant 한일 Self Review와 portable323 PASS는 독립 사람·사전·iOS 검증이 아니다. native BLOCKED/사람 NOT TESTED/B—Conditional을 유지한다. 기존163후보 전체 해결이나 모든 예문 토큰의 Vocabulary 등재를 주장하지 않는다.


## DATA-09-4 현재 Batch 승인 기준

- 명시 요청에 따라 C18문법/72고유예문/72문제를 반영했다. Content22/Schema4/reader7/UserProgress10, Grammar96/初中級54, DATA09 신규54/216/216으로 목표45~60/180~300/180~300 충족. 기존4개 예문 재사용·고정Vocabulary expression104·관계 증가를 신규로 합산하지 않는다. 장기350~500은 유지한다.
- canonicalSource는production.json이다. A/B 정확한 gate는20/21 불변fixture를 사용하고 C가 모든21→22 보존을 확인한다. prepare_data09_c는21+고정ID+검수authoring으로동일22만 재현한다. 다음 실제 변경은현재22를previous로 보존한다.
- 기존 Grammar12개 관계 끝점 revision+1만data09-c-revised-ids.json에따라 허용했다. 기존 본문/ID/배치/Progress/SRS·학습 엔진·광고/구매를 보호한다. 데이터만으로Schema/reader/UserProgress를 올리지 않는다.
- 최신 근거는DATA09_PROGRESS §10/Docs/DATA09_C_*다. 재개 후portable335PASS와assistant 한일 재독은 독립 사람/사전/iOS/출시 완료가 아니다. native BLOCKED/사람 NOT TESTED/B—Conditional·기존P1 gate를 유지하고, 소실된 이전로그나 미완료 검사를PASS로 만들지 않는다. 미승인7개/163후보 전체재연결을 완료로 표시하지 않고 후속단계/DATA10을 자동 시작하지 않는다.


## DATA-09-5 현재 최종 감사 기준

- 명시 요청에 따라 A~C 신규54문법/216고유예문/216문제를 전수 AI 자체 검수하고, 25개 기존 ID/31필드를 교정했다. 현재 Content23/Schema4/reader7/UserProgress10이며 수량·ID·정답 choice ID·관계·배치·진도 정책은 유지한다. 장기350~500 및 DATA09 신규45~60/180~300/180~300 목표를 축소하지 않는다.
- Content22 Source/DB는 불변 fixture다. A/B/C 정확한 gate는20/21/22 fixture로 당시 승인 상태를 검증하며, final gate가22→23의25개 revision/31필드만 허용한다. production.json이 유일한 canonical Source이고 final prepare는22+명시 manifest로 동일23만 재현한다. 다음 실제 본문 변경은 현재23을 previous로 먼저 보존한다.
- 선행163건의 해결120/조건부 허용7/미해결36은 설명 범위 판단이다. 새 재사용·배치 승인으로 해석하지 않고 기존 Batch B 재사용4개는 보존한다. Level 검토8건·부수 문형·인용 수식/양보의 기능 차이와 남은 교육 순서를 자동 완료 처리하지 않는다.
- 최신 근거는 DATA09_PROGRESS §11 및 Docs/DATA09_FINAL_*다. portable346 PASS·AI 전수/고위험/무작위 재독은 독립 원어민/교사·외부 사전·Swift/iOS 검증을 대신하지 않는다. native BLOCKED/사람 NOT TESTED/B—Conditional·기존 native P1 gate를 유지하며 후속 단계/DATA10을 자동 시작하지 않는다.


## DATA-09-6 현재 통합 기준

- 명시 요청으로 현재 Content24/Schema4/reader7/UserProgress10에 통합했다. 신규54문법/216고유예문/216문제, 장기350~500 목표를 유지한다. 기존3Grammar코스/18레슨 ID·membership·ordinal을 보존하고6Unit tag(data09_unit)·선행 복습20참조·관련 어휘54관계를 추가했다. Unit은 레슨당1개, 레슨당3문법의 기존 작은 단위를 유지한다.
- DATA09 시작 전19와 실제 직전23 원본/DB는 별도 불변 fixture다. 현재23을19로 재명명하지 않는다.19→24/23→24 strict와 전체 DB byte 재구성을 유지하며, 다음 실제 콘텐츠 변경은 현재24를 먼저 보존한다. final22→23 정확한 gate는23fixture에 고정했고 새23→24 gate가 Unit6개·기존107endpoint revision을 전부 검증한다. prepare_data09_integration은 동결23+고정 manifest로 같은24만 재현한다.
- 선행 설명 프리뷰/사전 조회를 학습 완료·SRS 등록으로 세지 않는다. GrammarSession 질문 snapshot·선택/페이지/seed/order/ContentVersion과 Vocabulary set membership을 재작성하지 않는다. 예문 learning_point_ja는 reader→비영속 Example→학습/사전 화면까지 전달한다. 입력 연습은 실제 검수 문항이 있는 어휘에서만 노출하고 새54문형 전체 자동 생성으로 표현하지 않는다.
- 최신 근거는 DATA09_PROGRESS §12/Docs/DATA09_INTEGRATION_*다. 최종 portable359 PASS·전용13/조회4와 SQL보존·오프라인/warm 성능 측정은 native 검증이 아니다.139 XCTest 실행0·iOS/접근성/기기 메모리/실제3~10분 BLOCKED, 독립 사람/사전 NOT TESTED, 기존 native P1/B—Conditional/미해결36건 유지. 다음 단계/DATA10은 자동 시작하지 않는다.


## DATA-09-7 현재 시스템 감사 기준

- 명시 요청으로 확인 가능한 DEV/DATA 계약을 감사했다. 현재 Content24/Schema4/reader7/UserProgress10·Source/DB/ID/revision·기존 순서/진도는 불변이다. 감사/테스트 보강만으로 버전을 올리거나 fixture/Production을 다시 배포하지 않는다. 다음 실제 콘텐츠 변경은 현재24를 먼저 보존한다.
- 최신 근거는 DATA09_PROGRESS §13 / Docs/DATA09_SYSTEM_REVIEW.md·RESULTS.json이다. 전체 portable365 PASS와 SQL 전3,553문제/4,813예문 도달은 Swift/UI 실행 증거가 아니다. native141정의/실행0(이번2추가)·Xcode/기기/실제 설정/구매/광고 BLOCKED, 독립 사람/사전 NOT TESTED·B—Conditional 유지.
- DATA08 P1 세 건은 현행 SQL/corpus/source 회귀10개 PASS이나 native 확인 gate는 남는다. 새 런타임 P0/P1 재현/수정0을 전체 앱 crash/grade/UI 무결성 보장으로 표현하지 않는다. 신규6portable·18레슨/오답/중복 native2개 회귀를 보존한다.
- 후행 선행참조12개는 선택적 page0 설명 프리뷰이며 session/lesson 순서를 바꾸거나 숙달로 기록하지 않는다. 후보163건120해결/7조건부/36미해결·Level8미해결 및 확인 불가능한 옛 완전 명세를 자동 완료 처리하지 않는다. 다음 단계/DATA10은 자동 시작하지 않는다.


## DATA-09-8 최종 종료·후속 작업 기준

- 현재 Content24/Schema4/reader7/UserProgress10, 신규 Grammar54·별도 고정Expression0·고유Example216·GrammarQuestion216이다. Vocabulary expression 전체163/DATA08신규104/DATA09추가0을 구분하고 이형태·재사용Example4개를 신규로 더하지 않는다. 장기Grammar/Expressions350~500을 유지한다.
- 최신 근거는 Docs/DATA09_CLOSEOUT.md·RESULTS.json / DATA09_PROGRESS §14다. 이번365 portable PASS·580구조/보존점검·31테이블/스키마/전체행/SHA 재현을 native/사람 승인으로 표현하지 않는다. iOS/XCTest141정의·실행0/기기 BLOCKED, 독립 사람/사전 NOT TESTED, Release B—Conditional과 native P1 gate를 유지한다.
- Source/Bundle/과거fixture95파일 byte를 보존했고 이번 Content/Schema/ID/revision 변경0이다. canonical Source/Bundle/fixture 추적을 유지하며 새 candidate/빌드 결과만 임시·기존 ignore를 쓴다. 현재50/100MiB 초과blob0으로 LFS는 불필요하다. 다음 실제 콘텐츠 변경은 현재24를 previous로 먼저 보존하고 재구성 SHA 불일치 시 원인을 별도 보고한다. 원본 삭제·샘플 축소·이력 재작성·force push는 금지한다.
- 선행163건120해결/7조건부/36미해결(Level8포함)·후행preview12개를 숙달/재사용 일괄 승인으로 바꾸지 않는다. 다음 공백/부분 구현은 현재 종료 보고에서 확인하고 DATA10을 자동 시작하지 않는다.
