# DATA-10-6 Listening / Dictation 통합

2026-10-21, 최신 main `d76f0b89c38c892005de68aef206229234d141c9`를 fetch·대조한 clean checkout에서 시작했다. 이 문서는 DATA10-6의 실제 구현·검사와 미실행 gate를 구분한다. 이전 QA와 native 실패 기록은 덮어쓰지 않는다. Release B—Conditional.

## 실제 배포와 보존

Content28 → **Content29 / Schema4 / minReader7 / UserProgress10**. Content28 source.gz와 SQLite를 그대로 보존했고, 변경 전28도 strict previous27로 재구성해 byte/SHA가 일치했다. clang이 없는 Cloud에서 최초 writer 설치가 실패하여 CC=gcc/LDSHARED='gcc -shared'로 별도 격리 writer를 만들었다. Python·SQLite compile profile은 ENVIRONMENT/PERFORMANCE 기록을 따른다. 시스템 Python·DDL·Validator·통계 테이블은 변경하지 않았다.

고정 UUID manifest에서 Content29 후보를 임시 디렉터리로 만들고 strict `--previous Tests/Fixtures/content-v28-production.sqlite --production` 오류0/기존경고10 후 반영했다. 10경고는 기존 한 글자 발음 예문5개와 동형 표제어 저/차/일/쓰다/적다5개이며 신규 경고가 아니다. 기존 Stable ID/kind/created_at, 모든 payload·정답/선택지·lesson membership·learning_order·과거110개 파일 byte는 보존됐다. `Content/production.json`이 유일한 runtime Source다. prepare 도구는 동결28+manifest에서29만 재현한다.

신규 학습 콘텐츠0: DATA10 신규 원문180개/Listening·Question360개는 그대로다. 배치용 UUID81개(코스3/레슨72/Unit tag6), membership360/참조360만 추가했다. 관계 끝점 **747개**(Listening360/Example180/Grammar77/Vocabulary130)는 명시 승인 목록대로 revision+1/updated_at 갱신했다. 본문 교정·새 원문·문항 추가로 계산하지 않는다. 기존27의 미래 editorial stamp를 보존하며 단조 후행 `2026-10-21T08:00:02Z`를 사용했다. 실제 실행 시각은 `recorded_at_utc`이며 created_at을 현재 시각으로 고치지 않았다.

전체 V2,287/M2,420/E4,993/G96/Q3,913/L2,296, Course11/Lesson175. Source25테이블 **70,823행**, SQLite31테이블. Source SHA `85a6a592256db104bf5e072bef95455cba37e7f1f2ed92f5686e1ef83223e965`, Bundle SHA `228d5572391d4c56509f83c57415c9b76b69c82ce2e7e48ebea82af97630b4af`. 엄격 재구성에서 전체 행(중복 포함)/schema/index SQL/byte를 대조했다. integrity ok/FK0. [전체수량·수준분포·보존](DATA10_INTEGRATION_COUNTS.json), [strict build](DATA10_INTEGRATION_BUILD.json), [변경 전 재현](DATA10_INTEGRATION_PREFLIGHT28.json).

|Level|Vocabulary|Example|Grammar|Question|Listening|
|---|---:|---:|---:|---:|---:|
|Hangul|0|0|0|59|0|
|入門|306|659|22|156|34|
|初級|800|1,577|20|134|79|
|初中級|1,181|2,757|54|3,564|2,183|

## 실제 Curriculum와 재사용 흐름

Listening Catalog 및 初中級 Curriculum의 듣기 목록에 전용3코스를 연결했다. A 일상·약속변경/교통·서비스·부탁, B 감정·의견·판단·이유·경험·계획, C 학교·직장·설명·비교·문제해결이다. 각 코스는 내용이해12레슨 → 별도 기회에 받아쓰기 등12레슨, **레슨당5문항**이다. 같은 원문의 두 과제를 한 레슨에 중복 배치하지 않았다. 실제 재생 시간/학습3~10분은 기기 미측정이며 5문항도 도중 중단할 수 있다.

`listeningCourses` / `listeningLessonIDs`는 기존 Course/Lesson 테이블의 active ID를 읽고, 기존 ListeningQuestion/ListeningSession 엔진을 사용한다. 일반 LessonStep 엔진은 listening/grammar typed 코스를 제외해 지원하지 않는 kind로 진입하지 않는다. 새 코스 순서는 기존0~7 뒤8~10이고 기존 세트·코스·배치103~120 번호와 순서는 불변이다. generic47개 初中級 레슨과 typed72개 듣기 레슨을 중복 집계하지 않는다. 듣기 레슨 확인 표시는 기존 listening_attempts의 completed session/first attempt 기준이고 원문 단위 숙달 인증이 아니다.

원문별 기존 Grammar1개(180관계/77고유)·실제로 등장하는 Vocabulary1개(180관계/130고유)를 AI가 의미·관찰 형태와 대조해 연결했다. `도착한대요/타셔야/샀어요/고마워요/말랐을` 등 활용형도 명시 관찰 문자열로 기록했다. 모든 토큰의 Vocabulary 등재·사전 학습 완료를 뜻하지 않는다. Example learning_point_ja와 기존 Grammar/Vocabulary 사전 링크는 **해답 판정 후에만 생성**한다. 재생 전 선택지 숨김/정답·Transcript·번역 guard를 유지한다. 문법의 기존 학습/퀴즈/SRS, Vocabulary 회독/활용/문장 생성으로 이어지는 기존 사전 화면을 재사용하고 미지원 문항을 생성하지 않는다.

새 scope는 `lesson:lower_intermediate:<stable lesson UUID>`. Home Resume가 scope/lessonID를 복원하며 새 세션은 membership 순서대로5문항 snapshot을 만든다. 기존 active snapshot을 먼저 사용해 ContentVersion·seed/choice order·position·heard·feedback·retry queue를 교체하지 않는다. 재시작은 새 scope의 현재 콘텐츠를 읽고 이전 결과를 지우지 않는다.

기존163 후보 **120해결/7조건부/36미해결(Level8)**, 신규12계열/27원문의 부수·미수록 문형 확인 필요는 유지한다. 이번 참조 배치로 이들을 일괄 해결·선행 숙달·자동 잠금으로 바꾸지 않았다. 선행 문법을 먼저 복습하는 기존 Grammar 화면은 선택 사항이다.

## 저장·SRS·입력·음성 점검의 범위

기존 transactional `beginListening/updateListening`을 사용한다. 성공적 재생완료, 판정, 다음 이동 시 snapshot을 저장하고 중복 제출은 expected revision으로 거부한다. 오답 재도전은 first-pass score/SRS를 다시 졸업시키지 않는다. 같은 Listening ID/skill에는 SRS PK1개이며 연습 재방문은 기존 due를 재설정하지 않는다. 같은 원문의 **서로 다른 두 task ID가 SRS2개가 되는 기존 정책**은 유지한다. 원문 단위 병합을 가장하거나 due를 합치지 않았다.

Cloud 검사는 실제28→29 bundle 교체와 전 사용자 테이블/파일 byte, 활성 session JSON/order/feedback/retry/heard, 기존 SRS due·Favorites·설정·통계·Resume, duplicate PK/rollback을 확인했다. Python의 opaque JSON/SQL은 Swift Codable·state transition 실행이 아니다. 실제 Swift actor/Codable/CAS/오답 재도전/반복 연습·dictation의 새 native3개 메서드를 작성했지만 미실행이다.

Dictation150개 accepted는 정확한 한글원문1개씩이다. 기존 judge의 문말 ASCII .!? 생략 허용/내부부호·철자 오답/spacing warning 구분을 유지하고 일반 ProductionAnswer를 변경하지 않았다. 숫자도 한글 입력 안내는 QA 때 교정한 상태를 보존했다. 판정 전 입력 중인 TextField 문자열은 기존 `@State`로, **화면 종료·프로세스 종료 때 미제출 초안까지 디스크 저장하는 기능은 없다(P2)**. 저장된 판정/위치/재생완료 기록의 손실과 구분하며 초안 보존을 완료로 표시하지 않는다.

정상/느리게 재생 요청, stop/실패·interruption의 완료 미인정, callback generation·question/revision guard, 화면 이탈/백그라운드 audio.stop은 코드와 기존 mock native 테스트 정의로 조사했다. 실제 TTS·iOS 이벤트 실행은 BLOCKED다. VoiceOver/화면 누출은 정적 검사를 통과해도 기기 PASS가 아니다. 모든2,296개 단일화자 시스템 TTS/검증녹음0·실제 검청 NOT TESTED를 유지한다. 중단 후 실제 복귀/IME·통화·오프라인 voice 설치/복구·메모리는 기기에서 확인해야 한다.

검색은 기존 Vocabulary/Grammar 사전의 literal 검색이다. 전180개 관련어의 실제 검색/상세 조회를 확인했고 listening transcript 전용 검색/Favorites를 새로 구현한 것은 아니다. 유지학습의 듣기 진입과 기존 통계 first/retry 분리를 유지한다. Monetization·StoreKit·AdMob·user migration 파일은 byte 불변이며 ContentVersion 변경이 권한을 초기화하는 경로를 추가하지 않았다. 정적 monetization 검사와 사용자 SQLite 보존은 실제 Keychain·구매 복원·광고 SDK 인증을 대신하지 않는다.

## 검사·성능·남은 gate

**INTEGRATION-L01/P2 수정**: A41 머리의 기본 사전 뜻「頭」가 머리카락 문맥에 표시되는 문제를 피하도록 새 related 참조를 기존 `자르다 / 切る`로 교정했다. 관찰형 자르지와 기본 의미를 검사하는 회귀 assertion을 추가했고 본문/기존 어휘 뜻은 바꾸지 않았다.

전용 candidate15개 최종 PASS(21.958초). 초기14PASS/1FAIL(21.829초)은 테스트가 듣기에도 Grammar용 question_target link를 가정한 오류였다. 실제 듣기 FK인 questions.listening_id 검사를 사용하도록 고쳤으며 Production/Validator 계약을 완화하거나 불필요한 관계를 추가하지 않았다. 전체 최초 실행418개는414PASS/1FAIL/3ERROR(552.020초,exit1)였다. 코스 전체 기대값8→11은 기존8개 제목/순서를 보존하면서 승인된3개를 뒤에 추가하도록 갱신했다. 전체 portable 첫 실행의 구검사3개 오류를 수정했다. 2개는 파일 첫 SQL을 듣기 조회라고 가정했고, 1개는 examples 조회를 UserProgress DB로 잘못 분류했다. 실제 SQL prefix와 repository extension으로 query/DB를 선택하고 모든 multiline SQL도 준비 검사하도록 보강했다. 초기 로그와 최종 전체 결과를 별도 보존한다.

최종 전체 portable **418/418 PASS (544.580초, failures/errors/skipped0, exit0)**. strict previous28·전체31테이블/Source70,823행/schema/index/byte 재현 PASS, iOS Build/XCTest/Simulator BLOCKED·독립 사람/TTS 검청 NOT TESTED를 구분한다.

전체 portable 최종 결과는 [실행 원장](DATA10_INTEGRATION_TEST_RESULTS.json)과 [전체 로그](DATA10_INTEGRATION_PORTABLE_TEST_LOG.txt)를 따른다. iOS Debug/Release/unsigned device build·XCTest 정의148개/실행0·Simulator **BLOCKED**(xcodebuild/swift exit127). 이전 Mac의142실행137PASS/5FAIL 이력은 그대로이며 이번3개 native는 authored/unexecuted다. 이전 활용 되다/뵈다 P1, StoreKit cold-cache 원인 미확정, 과거 cohort/course 가정 실패는 native에서 재확인해야 한다. 이번 portable 범위에서 새 runtime P0/P1 재현은 없으며 전체 앱 무결성 보장이 아니다. DATA10-5 재생 전 노출 P1은 코드/정적 PASS·실제 VoiceOver 대기다.

[Warm SQL 측정](DATA10_INTEGRATION_PERFORMANCE.json)은 network socket 금지·40회, 기존28과29의 search/catalog/curriculum 및 현재 Home/SRS/Resume/통계/유지학습/5문항 조회다. 검색p95 0.8127→0.8156ms, 코스 조회p95 1.2672ms·5문항 행 조회0.0577ms·Home0.2965ms·SRS20개0.1704ms다. 소규모 지연 차이는 OS noise를 포함하며 Swift 모델 생성·UI·cold launch·실제 메모리/3~10분 인증이 아니다. DB20,037,632→20,279,296bytes이며 재생성 DB/원본·과거 fixture를 구분해 모두 추적한다.

독립 원어민·교사/외부 사전·실제 TTS 검청 **NOT TESTED**. 기기 비행기모드/백그라운드·콜/VoiceOver·Dynamic Type·키보드·RAM·실제3~10분·실제 광고/구매 권한은 미실행이다. Release B—Conditional을 유지하고 DATA10-7/다음 단계를 시작하지 않는다. Commit/Push/PR/정상 병합 및 최종 main 동기화는 DATA10_PROGRESS §6·Git/PR·최종 응답을 기준으로 한다.

재현(프로젝트 root, 격리 writer PATH 사용):

```sh
CC=gcc LDSHARED='gcc -shared' python3 Tools/ContentBuilder/setup_exact_writer.py /tmp/hangul-writer-new
export PATH="/tmp/hangul-writer-new/bin:$PATH"
python3 Tools/ContentBuilder/prepare_data10_integration.py --output /tmp/content29.json --revised /tmp/revised29.json
python3 Tools/ContentBuilder/build_content.py /tmp/content29.json /tmp/rebuilt29.sqlite --previous Tests/Fixtures/content-v28-production.sqlite --production
cmp /tmp/rebuilt29.sqlite Resources/content.sqlite
python3 Tools/ContentBuilder/audit_data10_integration.py --rebuilt /tmp/rebuilt29.sqlite --report /tmp/audit29.json
sh Tools/verify.sh --portable
python3 Tools/ContentBuilder/benchmark_data10_integration.py
```
