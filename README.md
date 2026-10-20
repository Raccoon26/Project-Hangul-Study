# DATA-09-3 / Batch B — 현재 Production

**Content21 / Schema4 / minReader7 / UserProgress10.** 신규 初中級 문법18개·고유 신규 예문72개·단일 선택 문제72개를 한일 Self Review/중복·ID/strict 검증 후 반영했다. DATA08 예문4개는 기존 ID로 재사용하여 신규 수량에서 제외했다. 전체 Grammar78(入門22/初級20/初中級36), Example4,741(문장4,728+발음13), Question3,481, Vocabulary2,287. 새 Grammar 코스1·레슨6(53~58), 기존 본문·ID·배치 보존·관계 끝점22개만 revision+1. Content20 Source/DB 불변 fixture 보존, strict0errors/기존10warnings·Source25테이블65,043행 일치·integrity ok/FK0.

이번 portable **323/323 PASS**(393.788초, 실패/오류/skip0, exit0). DATA09 누적 신규36문법/144고유예문/144문제, 전체 신규45~60 및 장기Grammar/Expressions350~500 목표 유지. 독립 사람·외부 사전 검수 NOT TESTED, Xcode/Swift/iOS build·XCTest137정의/실행0 BLOCKED, **B—Conditional 유지**. [DATA09_PROGRESS §9](DATA09_PROGRESS.md), [한일 검수 범위](Docs/DATA09_B_REVIEW.md), [실제 수량](Docs/DATA09_B_COUNTS.json). Batch B에서 종료하며 다음 단계는 시작하지 않았다. 아래 DATA09-2 이전의 ‘현재’·수량·검사 결과는 당시 이력이다.

---

# DATA-09-2 / Batch A — 현재 Production

**Content20 / Schema4 / minReader7 / UserProgress10.** 신규 初中級 문법18개·고유 예문72개·단일 선택 문제72개를 assistant 한일 Self Review/중복·Stable ID/strict 검증 후 반영했다. 전체 Grammar60(入門22/初級20/初中級18), Example4,669(문장4,656+발음13), Question3,409, Vocabulary2,287. 새 Grammar 코스1·레슨6(47~52), 기존 본문/ID/순서 보존·관계 끝점12개만 revision+1. 기존19 source/DB fixture 보존, strict0errors/기존10warnings·Source25테이블64,099행 일치·integrity ok/FK0.

이번 portable **311/311 PASS**(328.544초, failures/errors/skipped0, exit0). 독립 사람 언어 검수·외부 사전 대조 NOT TESTED, Swift/Xcode/iOS 빌드·XCTest137개/실기기 실행0(BLOCKED), **B—Conditional 유지**. 장기Grammar/Expressions350~500개 및 DATA09 신규45~60개 목표 유지. 이번은 Batch A에서 종료한다. [DATA09_PROGRESS §8](DATA09_PROGRESS.md), [검수·한계](Docs/DATA09_A_REVIEW.md), [실제 수량](Docs/DATA09_A_COUNTS.json). 아래 DATA09-1/DATA08 및 DEV/DATA 내용의 ‘현재’는 당시 이력이다.

---

# DATA-08-8 최종 확인 — Content19 / Schema4 / reader7 / UserProgress10

**수량·Source/DB 통합 목표 달성, 전체 완료 판정은 B—Conditional 유지. DATA-09 미착수.** 신규 Vocabulary **911개(일반 어휘807 + 표현104)** / 고유 신규 문장 Example **1,821개**. 일반 어휘만 세어도 목표800~1,200 범위에 들며, 예문 목표1,300~2,000도 충족한다. 기존 예문1개 재사용은 신규 수에 포함하지 않았다.

Production: Vocabulary **2,287**, Meaning **2,420**, Example **4,597(문장4,584 + 발음13)**, Grammar **42**, Listening **1,936**, Question **3,337**, Course **5**, Lesson **85**. Content19와 모든 기존 ID·원본·DB byte 유지. Importer 재구성 DB는 번들과 SHA-256까지 동일, strict **0 errors / 기존10 warnings**, FK0 / integrity ok, 종료 점검133건 PASS. 이번 portable **301/301 PASS**(270.967초, 실패/오류/skip0, exit0). iOS build/XCTest137개는 **BLOCKED**, 독립 사람 언어 검수는 **NOT TESTED**다.

현재 결과와 미완료 조건은 [DATA08_CLOSEOUT](Docs/DATA08_CLOSEOUT.md), 실제 수량·해시는 [CLOSEOUT.json](Docs/DATA08_CLOSEOUT.json), 단계별 기록은 [DATA08_PROGRESS](DATA08_PROGRESS.md) §16을 따른다. **아래 DATA-08-1~7 및 DEV/DATA 섹션의 ‘현재’·완료 표현·테스트 수는 각 단계 당시 이력이며 최신 상태로 합산하거나 대체하지 않는다.**

---

**DATA-08-7 감사: Content19 / Schema4 / reader7 / UserProgress10 유지, Source/DB 변경0.** P1 세 건(비활성 복습 복구·받아쓰기 문장부호·듣기 due 퇴역 prefix) 코드 수정. 전체 Python/SQL **301 PASS**, native137개/실행0·iOS Build **BLOCKED**. 원래 DEV01~14/DATA01~07 작업 명세 원문은 찾지 못해 전체 원문 준수는 확인 불가. 기존 목표911어휘/1,821예문 유지, B—Conditional. [감사·부분 구현·상태표](Docs/DATA08_SYSTEM_REVIEW.md), [DATA08_PROGRESS.md](DATA08_PROGRESS.md) §15. 아래는 단계별 이력이다.

---

**DATA-08-6: Content19 / Schema4 / minReader7 / UserProgress10.** 911어휘/1,821신규예문 목표 유지. 실제 Course1·Unit tag3·Lesson47에911어휘 배치, 듣기/받아쓰기1,821·활용/문장입력1,162문항 연결. Production Vocabulary2,287 / Example4,597 / Grammar42 / Listening1,936 / Question3,337. strict0errors/기존10warnings·integrity ok/FK0·전63,159행 Source/DB 일치. portable **291 PASS**(289.839초, failures/errors/skipped0, exit0), 전용11 PASS. 사용자 기록/active snapshot/5·10·20 복습 SQL 보존. native 정의132/실행0, 실제 iPhone/offline/TTS/3~10분과 사람 검수 미실행. B—Conditional 유지. 상세 [통합 기록](Docs/DATA08_INTEGRATION.md), [DATA08_PROGRESS.md](DATA08_PROGRESS.md) §14. 아래는 단계별 이력이다.

---

> **현재 DATA-08-5 최종 감사: Content18 / schema4 / reader7.** A~C911어휘·1,821고유예문을 assistant가 한일 별도 재독, 무작위84개 재감사 후34어휘43필드를 교정했습니다. 전체 목표 수량은 유지합니다. portable280 PASS. **사람 검수·native130개 실행은 미완료**이며 선행Grammar 후보163예문 등 남은 사항은 [DATA08_PROGRESS.md](DATA08_PROGRESS.md) §13과 [감사 기록](Docs/DATA08_FINAL_REVIEW.md)에 있습니다. 아래 단계 내용은 당시 이력입니다.

---

> **현재 DATA-08-4 / Batch C: Content17 / schema4 / reader7. Vocabulary2,287 · Examples4,597(문장4,584) · Grammar42 · Listening115.** C 신규310어휘/619문장, 기존 예문1 재사용. DATA-08 전체 **911어휘(일반807/표현104) / 신규 문장1,821**로 목표800~1,200 / 1,300~2,000 달성. portable269 PASS, native129개·실기기 미실행. 상세 [DATA08_PROGRESS.md](DATA08_PROGRESS.md) §12, 출시 조건은 [PROJECT_STATUS.md](PROJECT_STATUS.md). 아래 내용은 당시 이력입니다.

---

> **현재 DATA-08-3 / Batch B: Content16 / schema4 / reader7. Vocabulary1,977 · Examples3,978(문장3,965) · Grammar42 · Listening115.** 初中級300어휘/600문장 추가. 최종 portable **255개 PASS (failures/errors/skip0, exit0)**. native128개·실기기 검증 미실행. 전체 DATA-08 목표/현재 검수 결과는 [DATA08_PROGRESS.md](DATA08_PROGRESS.md) §11, 출시 gate는 [PROJECT_STATUS.md](PROJECT_STATUS.md)를 확인하세요. 아래 Batch A/DATA/DEV 내용은 당시 이력입니다.

> **현재 DATA-08-2 / Batch A (2026-10-19): Content15 / schema4 / reader7. Vocabulary1,677 · Examples3,378(문장3,365) · Grammar42 · Listening115.** 이번 初中級301어휘/602문장 추가, portable243개 통과. Xcode/native127개·실기기 검증은 미실행입니다. DATA-08 전체목표와 단계별 결과는 [DATA08_PROGRESS.md](DATA08_PROGRESS.md), 현재 출시 gate는 [PROJECT_STATUS.md](PROJECT_STATUS.md)를 확인하세요. 아래 DATA/DEV 설명은 당시 이력입니다.

> **DATA-07 (2026-10-06): Content14 · Vocabulary1,376 · Examples2,776 · Grammar42 · Listening115.** 신규어휘450/예문900. 현재검증/남은Release gate는 PROJECT_STATUS.md, 실제누적수는 DATA_PROGRESS.md. 아래 DEV별 설명의 당시 수량은 이력입니다.

## DEV-14 검증 실행

프로젝트 루트에서 `sh Tools/verify.sh --portable`은 Python/SQLite만 실행합니다. Mac에서는 설치된 iOS17+ Simulator의 `TEST_DESTINATION`을 지정해 `sh Tools/verify.sh`를 실행합니다. 기본 모드는 Xcode 또는 destination이 없을 때 실패하며 native test를 생략하지 않습니다. 현재 출시 판정과 미실행 gate는 PROJECT_STATUS.md / RELEASE_CHECKLIST.md를 읽으세요.

> DEV-14 (2026-10-05): 현재 상태는 PROJECT_STATUS.md 및 Docs/DEV14_REQUIREMENTS_AUDIT.md가 기준입니다. 아래 이전 단계 기록의 완료 표현은 native 출시 검증을 의미하지 않습니다. Content13/Schema4/UserProgress10 유지.

# HangulStudy — DEV-12

일본어 사용자를 위한 Swift + SwiftUI 한국어 학습 앱입니다. iOS 16 이상을 대상으로 합니다. 기존 **ハングル入門** 12레슨에 **発音・パッチム** 14레슨을 추가했습니다. 사용자 진도 SQLite와 읽기 전용 콘텐츠 SQLite를 분리합니다.

## 현재 상태 / 실행

Mac Xcode에서 `HangulStudy.xcodeproj` → HangulStudy scheme을 실행하세요. iOS16+, 실기기는 Signing Team 지정이 필요합니다. `Tools/verify.sh`로 Debug/Release build와 Python tests, `TEST_DESTINATION` 지정 시 XCTest를 실행할 수 있습니다.

현재4탭은 学ぶ / 調べる / 記録 / 設定입니다. 学ぶ에서 시작위치·코스·이어하기·今日の復習, due 단어가 있으면 短く復習로 바로 시작합니다. 記録은 실제 통계와 유지학습, 設定은 짧은 복습량/로컬 알림을 제공합니다. 한글/발음/단어/문법/활용/듣기는 기존 production DB와 저장 엔진을 재사용합니다.

**Linux 검증: Python/SQLite203 PASS, Swift80파일 구문오류0. Native XCTest104개는 작성했으나 Xcode build/type-check/기기 UI·TTS·알림 검증은 미실행입니다.** 이 ZIP을 검증 완료된 App Store 배포본으로 간주하지 마세요.

Content schema4/content13/reader7, UserProgress10. Production 어휘926/예문1876/문법42/듣기111. 상급 단계 실제 콘텐츠, 검증된 개별 발음 녹음, 혼합Unit/심화진단은 아직 부족합니다. 전체 현황과 Critical/Major/Minor 감사는 `PROJECT_STATUS.md`, `Docs/DEV12_REQUIREMENTS_AUDIT.md`, 실제 수량은 `DATA_PROGRESS.md`에 있습니다.

## 아래 문서의 DEV/DATA별 이력

이하의 당시 수량·버전·검증 결과는 역사적 기록입니다. 현재 기준은 위 DEV-12 절과 최신 PROJECT_STATUS/DATA_PROGRESS입니다.

## DATA-01 입문 어휘

실제 입문 어휘 **226개**, 일본어 의미 **244개**, 예문 **447개**를 production DB에 추가했습니다. 기존 `単語` 탭에서 50개씩 조회하고 상세에서 대표 의미·품사·예문을 볼 수 있는 구조입니다. DEV-05의 회독 화면에서는 대표 의미와 연결 예문, 일본인용 학습 노트를 표시하고 추가 의미도 펼쳐 볼 수 있습니다.

누적 수는 `DATA_PROGRESS.md`, 전체 검수 목록은 `Docs/DATA01_REVIEW_CATALOG.md`를 확인하세요.

## DEV-05 회독 학습

`学ぶ → 入門単語 → 新しいセットを始める / 続きから`에서 실제 DB의 어휘를 약 20개씩 학습합니다.

- 한국어를 보고 의미를 떠올린 뒤 `意味を見る`를 누릅니다.
- `覚えてる`는 이번 시도에서 통과, `覚える`는 다음 회독으로 남깁니다.
- 한 회독이 끝나면 남은 단어만 순서를 바꿔 다시 확인하고, 모두 통과하면 세트를 완료합니다.
- 현재 카드·회독·뜻 공개 상태를 매 동작마다 로컬 SQLite에 저장합니다. 콘텐츠 순서나 버전이 바뀌어도 저장된 영구 ID 목록으로 재개합니다.
- normal/slow/stop 음성은 기존 KoreanAudioService를 재사용합니다.
- 완료는 영구 습득이 아닙니다. 다시 보기와 미래 SRS 복습을 막지 않습니다.

Content schema 3 / version 5는 유지하며 UserProgress만 비파괴 migration으로 schema 4가 됩니다. 기존 한글/발음 기록은 보존합니다. Native XCTest 42개(신규 회독 13개)는 작성했으며 **이 Linux 환경에서는 실행하지 못했습니다**. 수동 확인 목록은 `Docs/VALIDATION_DEV05.md`입니다.

## DEV-06 장기복습

회독을 완료한 단어는 다음 날부터 홈의 `今日の復習`에 나타납니다. 기본 20개씩 실제 단어를 보고 뜻을 공개한 뒤 `難しい / もう少し / 覚えた`로 판정합니다.

- 1/3/7/14/30/60/120일 단계형 정책이며 최고 단계에서도 계속 복습합니다.
- 처음부터 알고 있던 단어도 등록하고, 같은 세트를 다시 완료해도 기존 SRS를 초기화하지 않습니다.
- 회독 남은 목록과 장기복습 단계는 독립적으로 저장합니다. 복습의 단어 순서/공개 상태/판정 결과는 재실행 후 이어집니다.
- 밀린 복습의 전체 수를 보이며 20개만 시작합니다. 미진행 단어는 남고, 새 학습도 자유롭게 선택할 수 있습니다.
- 기존 UserProgress를 schema 5로 migration하며 DEV-05의 과거 완료 세트도 등록합니다. Content DB는 schema 3/content 5 그대로입니다.
- 현재 SRS는 calendar_steps v1입니다. 자세한 날짜/시간대 정책과 제한은 PROJECT_STATUS.md에 기록했습니다.

**DEV-06의 정책과 이전 검증 이력은 해당 문서에 보존되어 있습니다. 현재 DEV-07 결과는 아래를 확인하세요.** Mac build/실기기 검증은 `Docs/VALIDATION_DEV06.md`를 따라 확인하세요.

## DATA-02 입문 보강·초급

신규 어휘 **250개**, 의미 **260개**, 예문 **500개**, 일본인용 note **32개**를 추가했습니다. DATA-02 당시 누적 어휘 **476개**와 문장 **947개**였습니다. `学ぶ → 初級単語`에서도 기존과 같은 20단어 회독과 SRS를 사용합니다. 기존 세트/기록/ID는 유지합니다. 전체 검수 목록은 `Docs/DATA02_REVIEW_CATALOG.md`입니다.

## DATA-03 초급·일상 표현 강화

신규 어휘 **250개**(입문 10/초급 240), 의미 **268개**, 예문 **500개**, note **48개**를 추가했습니다. 현재 누적 어휘 **726개**, 문장 **1,447개**입니다. 실제 DB의 기존 入門/初級 회독·SRS를 그대로 사용하며 UI나 학습 엔진은 변경하지 않았습니다.

동사·형용사·부사 190개를 중심으로 다의어 18개와 자동사/타동사·혼동어 관계를 보강했습니다. Content version 7, schema 3 유지. Validator 오류 0/검토 경고 10, Python/SQLite 129개 통과입니다. native XCTest 60개는 미실행입니다. 전체 검수 목록은 `Docs/DATA03_REVIEW_CATALOG.md`, 진행 현황과 제한은 `PROJECT_STATUS.md`, `DATA_PROGRESS.md`를 확인하세요.

## DEV-07 문법 학습·회독·복습

`学ぶ → 文法 → 入門/初級`에서 production 문법 **12개**, 예문 **24개**, 문제 **24개**를 4개 작은 레슨으로 학습합니다. 의미→형태→예문/비교→문제→자기판정으로 진행하고 모르는 항목만 다음 회독에 남깁니다. 완료하면 기존 SRS의 grammar 대상으로 등록하며 홈 今日の復習에서 실제 문제를 풀고 다음 날짜를 조정합니다. 진행 단계/현재 문제/선택 피드백은 로컬 SQLite에 저장합니다.

Content schema **3**, content **8**, reader **5**, UserProgress **6**. 누적 vocabulary **726**, 예문 문장 **1,471**(발음 단어 예시 13개 별도), grammar **12**. **Python/SQLite 138개 통과 / Swift 53파일 구문 검사 / Native XCTest 66개 작성·미실행**. Xcode 빌드와 실제 기기 검증은 미수행입니다. `Docs/VALIDATION_DEV07.md`를 따라 Mac에서 확인하세요.

## 콘텐츠 제작·검증

현재 source는 `Content/production.json`이며 schema 4 / content 11 / min_reader 7입니다. DEV-03 source와 ID는 회귀 자료로 보존했습니다.

```sh
python3 Tools/ContentBuilder/build_content.py Content/production.json candidate.sqlite --production --previous Tests/Fixtures/content-v10-repaired-production.sqlite --report validation.json
python3 -m unittest discover -s Tools/ContentBuilder -v
python3 Tools/generate_project.py
```

위 명령은 DATA-04 재현용입니다. DEV-09 DB의 잘못된 SQLite 헤더를 별도 스냅샷에서 정정했으며 원본도 보존했습니다. 다음 배포는 **현재 배포한 DB**를 --previous로 지정하고 revision/content_version을 올립니다. ID를 다시 생성하지 마세요. 검수한 candidate만 Resources/content.sqlite로 교체합니다. 현재 입문 306개·초급 420개를 수록했고 15,000개 전체 구축은 후속 DATA에서 계속합니다.

Mac 검증:

```sh
sh Tools/verify.sh
TEST_DESTINATION='platform=iOS Simulator,id=YOUR_SIMULATOR_ID' sh Tools/verify.sh
```

검증 스크립트는 Python 테스트와 Debug/Release 시뮬레이터 빌드, 지정한 경우 XCTest를 실행합니다. 이 명령은 다음 환경에서 수행할 절차입니다.

## 인계 문서

- `PROJECT_STATUS.md`: DATA-04 결과·제한·다음 단계
- `CONTENT_GUIDE.md`: 데이터·영구 ID·발음·음원 작성 계약
- `Docs/ARCHITECTURE.md`: 데이터/진도/음성 구조
- `Docs/VALIDATION_DATA04.md`: 최신 수행·미수행 검증과 Mac 점검 목록
- `Docs/DATA04_CONTENT_REPORT.json`: 현재 production Importer 보고서
- `Docs/DEV-01_STATUS.md`~`DEV-04_STATUS.md`: 이전 단계 기록

## DEV-08 활용·직접입력

`学ぶ → 活用 · 自分で入力する`에서 기존 production 동사/형용사 16개로 현재/과거/미래·부정·희망·연결·이유·조건을 연습합니다. 직접입력 49문제에는 기존 예문 빈칸과 조건부 일본어→한국어 문장이 포함됩니다. 같은 UserProgress에 답안·판정·오답 queue를 저장하고 기존 vocabulary SRS로 연결합니다. 관련 문법은 기존 설명 UI로 확인합니다.

현재 Content 9 / reader 6 / schema 3 / UserProgress 7. Python/SQLite **142개 통과**, Swift **58파일 구문 검사**, Native XCTest **71개 작성·미실행**입니다. Xcode 빌드·키보드·실제 TTS 확인은 미수행입니다. 지원 범위/예외/생산 전용 SRS 미구현 등 제한은 PROJECT_STATUS.md, Mac 체크리스트는 Docs/VALIDATION_DEV08.md를 확인하세요.

## DEV-09 듣기·받아쓰기

`学ぶ → リスニング → 入門 / 初級 → 練習 1`에서 기존 production 예문24개를 듣고 의미/한국어/문장 이해를 선택하거나 받아쓰기를 합니다. 끝까지 재생해야 제출할 수 있고, 제출 후 원문·일본어·답안을 확인합니다. 오답은 한 번 재확인하며 상태를 같은 UserProgress에 저장합니다. 예정일에는 홈 今日の復習에서 실제 듣기 SRS를 진행합니다.

현재 Content schema4 / content10 / reader7 / UserProgress8. Python/SQLite149개 통과, Swift62파일 구문 확인. **Native XCTest78개·Xcode 빌드·실기기 음성/VoiceOver/키보드 검증은 미수행**입니다. PROJECT_STATUS.md 및 Docs/VALIDATION_DEV09.md를 확인하세요. 앞 단계 설명/버전은 당시 이력입니다.

## DATA-04 문법 확장

신규 문법 **30개**(누적42), 신규 예문 **53개**와 기존 예문7개 재사용, 문법 문제60개와 듣기3개를 반영했습니다. `学ぶ → 文法 → 入門 / 初級`의 기존 코스에 새 레슨8개를 추가했습니다. 문법 회독·SRS·예문 음성은 기존 시스템 그대로입니다. 직접입력5문항은 새 문법 설명에 연결됩니다.

Content11 / schema4 / reader7. DATA-04에서 DEV-09의 SQLite user_version 오기를3→4로 정정했습니다. UI/학습 엔진/사용자 진도 구조는 변경하지 않았습니다. Xcode build와 실기기 검증은 아직 필요합니다. 이전 DEV 절의 버전과 통계는 당시 이력입니다.


## DATA-05 현재 배포

初級 어휘200개·문장339개 추가. 총 어휘926 / 예문1876(문장1863) / 문법42 / 듣기31 / 문제262. schema4 / content12 / reader7 / UserProgress8.

ㄷ 불규칙 조건·미래형, 비활성 어휘의 활용 노출, 활용 화면 background audio, 비동기 문법 오류 경합을 수정했다. 168개 Python/SQLite 테스트 통과. 62개 Swift파일 구문 검사. **Xcode build·XCTest82개·실제 UI/음성은 미실행**. `PROJECT_STATUS.md`, `DATA_PROGRESS.md`, `Docs/DATA05_INTEGRATION_AUDIT.md`를 최신 기준으로 읽는다.
