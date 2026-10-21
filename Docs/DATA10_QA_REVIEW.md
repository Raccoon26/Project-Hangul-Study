# DATA-10-5 / Listening·Dictation 전체 QA

2026-10-21 JST, Linux Cloud. 시작 main=origin/main `f7d1835a8ce1b073a65e8a21d8b27f6e4eb523a9`(PR21), clean/미커밋0. `codex/data10-5-listening-qa`에서 DATA10_PROGRESS §1~4·상태/가이드/출시/AGENTS와 실제 Source/DB/ListeningView·모델·AudioService·Reader/Validator를 대조했다. 작업은 이번 QA에서 종료한다.

## 검수 범위와 증거의 종류

| 범위 | 실제 수행 | 한계 |
| --- | --- | --- |
| 신규 A/B/C |180한국어·180일본어·360질문/해설/정답·630선택지·150accepted AI 별도 재독|독립 사람·교사 검수 아님|
| 구조 검사 |신규 전항목 및 전체2,296 source/task/ID/참조/정답 형식·기존1,936 분포/완전 중복·전체prompt 원문/번역 포함|기계 검사는 의미·오답 타당성의 증명이 아님|
| 별도 재감사 |batch별6개씩 무작위18원문·고위험 설명/형태에 집중 재독, 기존 Level별4개씩12원문·근접4쌍 AI 표본|별도 재독을 신규 고유 검수 수에 더하지 않음; 기존1,936 언어 전수 검수 아님|
| UI/VoiceOver |실제 소스의 생성 분기·상태/재생완료 경로·접근성 라벨/오류문구 점검, 노출 회귀용 구조 검사|동적 iOS UI/VoiceOver 실행은 BLOCKED|
| 음성·사람 |검증 녹음0 유지|실제 TTS 검청/발음·독립 원어민·교사·전수 외부사전 NOT TESTED|

[실제 전항목 payload](DATA10_QA_ITEMS.md), [항목별 AI 검수·답안](DATA10_QA_EDITORIAL.json), [18표본](DATA10_QA_SAMPLES.json), [구조/보존](DATA10_QA_COUNTS.json), [실제 실행](DATA10_QA_TEST_RESULTS.json). Level은 내부 初中級 판단이며 공인 등급·학습 성과 검증이 아니다.

## 발견·수정

**QA-UI01 / P1, 재생 전 선택지 노출 구조.** 기존 View는 `s.result==nil`에서 선택지 Text를 만들고 버튼만 disabled했다. 의미·한국어 선택에서는 정답 번역/한국어 전체도 선택지로 포함되며 화면에 읽을 수 있었고 접근성 트리에도 노출 가능한 구조였다. 실제 기기에서 VoiceOver로 관찰한 결과라고 주장하지 않는다. 이제 `ListeningSession.revealsChoices`의 heard/result/current/task 조건 아래에서만 ForEach/Label을 생성한다. 듣기 완료 성공이 저장되기 전에는 보기 자체가 없다. 들은 뒤 미채점 Resume는 원래 heard=true를 유지하고, 다음 문제에서는 heard=false로 돌아간다. 새 computed property는 Codable 저장 필드·UserProgress Schema를 추가하지 않는다. Native 전환/Resume1메서드를 추가했으나 미실행이며, 원래 소스/guard 제거 변형을 거부하는 정적 회귀 PASS와 iOS 동적 확인 gate를 구분한다.

**QA-UI02 / P2, 받아쓰기 부호 안내.** 기존 `句点は不要です`는 내부 마침표도 생략 가능한 것처럼 읽혔다. 문중 부호는 입력하고 문말 ASCII .!?만 생략 가능하다는 실제 계약으로 고쳤다. Transcript/번역/정답/설명은 기존 result 분기 뒤 조건부 생성, `.opacity(0)`나 단순 accessibilityHidden으로 숨기지 않는다. TTS error/availability·버튼 라벨은 정답 텍스트를 포함하지 않는다. 전체2,296 prompt의 원문/전체번역 exact 포함0은 기계 확인이며 모든 문맥상 힌트 부재의 증명은 아니다. 질문 자체는 재생 전에 볼 수 있다.

**언어/문항10개 유형**을 [명시 before/after 원장](../Content/data10-final-corrections.json)에 남겼다.

- A13: `-는 대신`의 약속 자체 취소를 피하는 대안과 일본어의 취소 완료 표현을 구별했다. 날짜 변경 제안이라는 설명을 명확히 했다.
- A23: 미수록 `-더라도`를 기존 `-아/어도`로 단순화하고 원문/accepted/해설을 일치시켰다.
- A27: 원문에 없는 두 명이라는 전제를 질문에서 제거했다. 단일화자 TTS 상태를 유지한다.
- B06: 일본어/질문에 있는 부탁받는 사람(형)을 한국어에도 명시했다. 인용 수혜자인 부모님과 전달할 사람인 형을 구별한다.
- B21: 경향 `편이다`를 일본어 추측 `ようだ`로 읽지 않도록 번역/설명을 교정했다.
- B30: 바닥이 마를 때까지 안전 검사를 계속한다는 과한 해석을 정답에서 제거하고, 안전 우선/마를 때까지 기다리는 안내로 좁혔다. 정답 choice ID 불변이다.
- B47: 잠정 의향을 확정 일정처럼 표현한 오답 해설을 교정했다.
- B53: 실제 `하고 싶냐고`와 설명의 잔존 `싶으냐고` 표면을 일치시켰다.
- B56: 미수록 `-기보다는`를 기존 `-는 대신`으로 단순화하고 번역/accepted를 맞췄다.
- B57: 일본어 `私に…言われた`의 수동태 역할 혼동과 원문에 없는 비난 의도 설명을 교정했다.

**숫자/accepted 정책.** 신규150받아쓰기는 정확한 원문1개씩이다. 기존 Validator는 원문 정규형과 끝부호 변형만 허용한다. `두 시/2시` 등 숫자 표기 변형은 현재 미지원이다. 임의 정규화·동의어 허용으로 검사를 완화하지 않고150prompt에 숫자도 한글로 쓰라는 안내를 추가했다. 이 공통 지침 반복은180원문을 반복 템플릿으로 채운 것이 아니다. 문중 부호/철자/단어는 여전히 오답, spacing warning은 정답과 별도이며 일반 ProductionAnswer는 불변이다. 한국어가 달라진3원문의 accepted도 새 원문과 맞췄다. 실제 Swift 판정은 기존 native 코퍼스 메서드에서 실행해야 하며 Python 기대값만으로 실행을 인증하지 않는다.

총 **188본문 필드/175payload 엔티티** 교정, **179기존 ID revision+1**이다. 이 중4 Listening은 바뀐 Example의 음성/번역을 읽는 종속 revision만 전파했고 fingerprint 본문은 불변이다. 단순 instruction150개를150개의 서로 다른 제품 버그로 세지 않는다. 신규/삭제 엔티티0·ID/kind/created_at/학습순서·정답choice ID/순서·관계/배치 불변. 기존 UserProgress·snapshot을 바꾸지 않는다.

## 기존1,936과 선행·학습 경로

[분포/중복/템플릿](DATA10_QA_CORPUS_ANALYSIS.json), [기존12원문·4근접쌍](DATA10_QA_OLD_SAMPLES.json), [실제 목록을 이용한 권고 경로](DATA10_QA_LEARNING_PATH.md).

기존 받아쓰기95.558%/初中級1,823 중1,822받아쓰기, 짧은 단문8~35자로 어휘/표기 연습 편중이다. 합산해도 받아쓰기87.108%다. 기존 구조 중복0이지만 `돌아보며/되돌아보며`의 의미가 매우 가까운 문장쌍은 교육적 중복으로 기록했다. 다른 근접쌍은 장소·형용사·부사 최소대립이며 모두 자동 병합하지 않았다. 신규180원문의 완전 중복/신규 문장조각 반복0, 기존 예문과 겹치는 한 조각 `금방 돌아올게요`는 A51 전체 상황과 구별한다. 단일화자TTS는 실제 방송·다화자·잡음/자연속도 적응을 검증하지 못한다.

신규 전180의 기존 Grammar 선택참조180개/고유77ID, B의 기존54개 용례 관찰을 실제 본문과 다시 대조했다. [선행 검토](DATA10_QA_PREREQUISITES.json)는 원문당1개 문형만으로 전체 숙달을 보장하지 않는다. 미수록/변형12계열·27원문은 사전 설명/교사 확인이 필요하다. C의 종전 lexical-only 참조를 실제 인쇄하세요/높아서 등으로 고쳤지만 Runtime 관계를 새로 만든 것은 아니다. Level을 임의 상향/하향하거나 선행163건을 일괄 승인하지 않았다. 기존 듣기 source에163건이 모두 포함되며120해결/7조건부/36미해결(Level8포함)을 유지한다.

권고는 기존 Grammar96/初中級3코스18레슨6Unit 복습→A103~105/B109~111/C115~117 내용이해→결과 뒤 사전/문법 확인과 기존 단문 보충→다음 학습 기회에 A106~108/B112~114/C118~120의 두 번째 과제다. 실제 목록은練習번호이고 주제/선행 자동 잠금이 없으며 SRS는 Listening ID별로 같은 source 두 유형을 모을 수 있다. 20문항 상한·중단/Resume를 유지하고 실제3~10분 완료 시간은 보장하지 않는다. Favorites는 현행 Vocabulary/Grammar만 지원하며 이번에 듣기 Favorites를 추가했다고 주장하지 않는다.

## 데이터·검증·릴리스

Content27 source/DB를 실제 byte 그대로 동결한 뒤 **Content28/Schema4/reader7/UserProgress10**으로 교정했다. A/B/C exact gate는25/26/27 fixture에 고정, final27→28 gate가 명시 원장과 전체 보존을 확인한다. canonical Source는 production.json 하나이며 과거 원고/validator/fixture를 덮어쓰지 않았다. 기존27의 최대 editorial stamp08:00:00Z가 실제 QA 시각보다 미래인 메타데이터를 보존하고, 이번 revision metadata는 단조 증가08:00:01Z를 사용했다. 실제 QA 실행 UTC는 별도 recorded_at_utc이며 이 metadata를 사람 검수 시각으로 표현하지 않는다.

Source25테이블69,787행·전체31테이블의 중복 포함 행/schema/index/byte SHA 재구성 일치. strict previous27 오류0/기존경고10·integrity ok/FK0. 기존106개 Content/Resources/fixture 파일의 당시 byte를27 snapshot/나머지 실제파일로 보존했다. 전체ID16,841·신규/삭제0, 이전1,936의 Example/Listening/Question 본문 fingerprint 불변이다.

- 최초 후보12개는10PASS/1FAIL/1ERROR(28.969초). 테스트가 내부부호를 마침표만 있다고 가정해 `?`로 이어지는 문장을 놓쳤고, Favorites에 미지원 listening 유형을 넣은 fixture 오류가 있었다. 문중 .!? 경계를 모두 검사하고 실제 지원 Vocabulary favorite를 보존하도록 수정했다. 실제 앱 채점·DB 제약을 완화하지 않았다. [초기 로그](DATA10_QA_CANDIDATE_TEST_LOG.txt).
- 최종 후보 **12/12 PASS,29.605초,exit0**. [로그](DATA10_QA_FINAL_CANDIDATE_TEST_LOG.txt). Source/DB·명시 교정/리비전·179ID·이전1,936·360bounded offline 조회·부호/철자·숫자/동의어/누출/중복/미증가revision 거부·27→28 snapshot/SRS/Favorites/UserProgress byte 보존·UI 생성 분기를 검사했다. SQL의 임시 JSON은 Swift Codable/기기 개인진도 인증이 아니다.
- 최종 전체 portable **403/403 PASS (477.897초, failures/errors/skipped0, exit0)**. [전체 원시 로그](DATA10_QA_PORTABLE_TEST_LOG.txt). 전용/표본 재독·반복 실행을 고유 검사 수에 중복 합산하지 않는다.
- Cloud Xcode/Swift 없음. **iOS Build/145 XCTest 정의·실행0 BLOCKED**, 새 정책1메서드도 미실행. 이전 Mac142실행137PASS/5FAIL(되다/뵈다 활용P1·꿰다 기대값 검토, cold Purchase cache, DATA06 cohort·발음course 가정3)은 미해결이다. 새 노출 P1은 코드수정/정적PASS·native/실기기 확인 보류로 기록한다.
- 실제 VoiceOver/스크린샷·TTS 검청·음성 중단·기기Offline/메모리·IME·3~10분·AdMob/StoreKit 실제 권한은 미실행이다. 독립 사람·교사/전수 외부사전 NOT TESTED, 검증 녹음0, **Release B—Conditional** 유지.

재현:

```sh
python3 Tools/ContentBuilder/prepare_data10_final.py --output /tmp/data10-final.json --revised /tmp/data10-final-revised.json
python3 Tools/ContentBuilder/build_content.py /tmp/data10-final.json /tmp/data10-final.sqlite --previous Tests/Fixtures/content-v27-production.sqlite --production
python3 Tools/ContentBuilder/audit_data10_final.py --rebuilt /tmp/data10-final.sqlite --report /tmp/data10-qa.json --items /tmp/data10-qa-items.md
sh Tools/verify.sh --portable
```

다른 writer 환경은 DATA10_WRITER.md의 실제 byte 비교를 먼저 수행한다. 결과를 일반 Commit/Push/main PR로 전달하며 이전 위임과 AGENTS에 따라 정상 병합·동기화를 확인한다. Force Push·기존원본삭제·이력재작성은 하지 않는다. 최종 PR/merge SHA·clean main 일치는 Git/PR 및 최종 응답이 기준이며 자기 SHA를 위한 사후commit을 반복하지 않는다. 다음 단계는 시작하지 않는다.
