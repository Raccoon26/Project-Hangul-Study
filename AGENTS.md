# HangulStudy 작업 규칙

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
