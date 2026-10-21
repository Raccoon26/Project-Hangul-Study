# DATA-10-4 / 最終 Listening Batch C

2026-10-21 JST. main/origin/main `a9ec0a450e1c40e0bd3b608ec2059499c27e762e` (PR20) 및 DATA10_PROGRESS §1~3와 실제 Content26을 동기화한 Linux Cloud에서 작업했다. 시작 미커밋0, 브랜치 `codex/data10-4-listening-batch-c`. Content26→**27**, Schema4/minReader7/UserProgress10 유지. 이번 마지막 Batch 이후 다른 단계는 시작하지 않는다.

## 실제 원문·문제와 전체 목표

| 영역 | 신규 원문 | 내용이해 | 받아쓰기 |
| --- | ---: | ---: | ---: |
| 학교 안내 |10|10|10|
| 직장 안내 |10|10|10|
| 설명 |10|10|10|
| 비교·선택 |10|10|10|
| 문제 해결 |10|10|10|
| 화자 의도 |10|10|10|
| 합계 |60|60|60|

A60/120+B60/120+C60/120=**신규 원문180/문제360**. 전체 목표150~250/300~500을 충족한다. [실제 수량](DATA10_C_COUNTS.json)은 Content24 대비 새 Example180/Listening360/Question360의 ID 집합이 A/B/C manifest와 정확히 일치하는지 검사한다. 기존1,936TTS/기존 예문은 신규 수에 더하지 않는다. 원문마다 Example1개를 두 과제에서 참조하며 추가 참조60·내부 문장·180선택지·60accepted를 원문으로 세지 않는다.

전체 Example4,933→4,993, Listening2,176→2,296, Question3,793→3,913, content_items16,541→16,841. Vocabulary2,287/Meaning2,420/Grammar96/Course8/Lesson103 불변. Listening 入門34/初級79/初中級2,183, 전체 유형 의미50/한국어39/받아쓰기2,000/내용이해207. 세부 Level 분포는 COUNTS.entity_levels를 따른다.

learning_order2300~2419 (batch115~120, 화면練習116~121)의6구간 각20문항으로 기존 목록에 연결한다. 동일 원문의 두 유형은3구간 차이, 한 page 안 source 중복0이며 기존 빈칸·부분 batch·session snapshot은 재작성하지 않는다. 원문별 SRS 병합/주제별 새 UI를 구현한 것이 아니다. 기존 SRS는 Listening ID별로 동일 source의 두 유형을 모을 수 있다.

## 별도 언어·문항 AI Self Review

전60한국어·60일본어를 별도로 재독하고120질문/정답/해설,180선택지,60accepted를 대조했다. 조사·활용·띄어쓰기·지시대상·수혜자·높임·부정 범위·시제·의도와 일본어 문체를 확인했다. 안내의 대상/기한, 조작 순서, 비교 조건/장단점, 해결 순서, 반복 요청 범위를 문항별로 구분한다. 각 내용이해 문항에 한국어의 직접 근거와 개별 일본어 오답 이유가 있으며 정답 위치 a/b/c 각20이다. [전수 payload](DATA10_C_ITEMS.md), [항목별 AI 재독](DATA10_C_SELF_REVIEW.json).

[교정 기록](DATA10_C_EDITORIAL_CORRECTIONS.json)은 후보 작성 중 **133편집 이벤트/114고유 필드**다. 133개의 Production 버그라는 뜻은 아니다. C09의 파일명/이름 지시대상, C12/C52/C60의 요청형, 미수록 `-더라도`/`-기보다는`/`-아 두다` 부담을 단순화하고, C05/C23의 의미상 중복 오답 등 선택지의 현실성과 명료성을 보강했다. 기존 Production 텍스트 변경0, 신규 UUID 재발급0.

첫 후보9개는8PASS/1FAIL(17.332초), 수정 스크립트가 쓰기 전 assertion으로 중단되어 두 번째도8PASS/1FAIL(18.016초)이다. 원문 단순화 뒤 정답 인용문이 남은 문제가 원인이며 동일 유형 전수 재검색으로 **C20/C49/C54 세 인용문**을 교정했다. prepare에 원문 내 근거 존재와 선택지 구별 검사를 추가했다. 세 번째9PASS(17.383초) 후 최종 오답 다듬기에 대해 다시 **9/9PASS(18.145초)**. 초기 실패 로그를 삭제하거나 PASS로 바꾸지 않는다. 임시 도구 초기 버전 assertion(26→27 복사 실수), 어휘 조회의 잘못된 컬럼명도 수정했고 후보 승인 전 해소했다. 런타임 코드 수정0.

기존4,933예문(기존 듣기 및 A/B 포함) 전체와 C내 NFC/공백/종결부호 제거 한국어·일본어·문장쌍 완전 중복0. bigram shortlist8→SequenceMatcher 상위3씩 **180근접 후보의 한일 문맥**을 별도 AI 재독했다. C07젖은바닥/C34가방/C38우회/C52반복요청/C56역할분담은 공통어구가 있어도 기존 문장의 상황·명제·문항 근거와 구분했다. [근접 텍스트/판단](DATA10_C_SIMILARITY.json). 자동 점수는 모든 의미상 paraphrase 부재나 언어 품질의 증명이 아니다.

원문은 모두 **2문장/38~63자(평균48.9자)**다. [선행 검토](DATA10_C_PREREQUISITES.json)에 기존 Grammar40개를 참조한60행과 기존 Vocabulary literal receipt를 남겼다. C20/C39는 문형 전체 적용이 아닌 어휘상 시간/비교 참조, C47뒤에/후에 대응, C57권유인용 관형형, C60목적 연결형은 별도 표시했다. future추측·예정·존대 변형 및 열람실/출입증/잠금 등 상황어는 내부 初中級 판단이며 모든 토큰·부수 문형의 선행 숙달/등재를 인증하지 않는다. 학습자 부담을 줄여 작성했고 독립 교사 Level 확인은 남는다. 기존 Grammar ID/revision/관계·선행163건120해결/7조건부/36미해결(Level8포함)은 그대로다. 문법54개를 억지로 모두 끼워 넣지 않았다.

이 검수는 **assistant AI 자체 검수**다. 독립 원어민·교사, 전수 외부 사전, 실제 TTS 검청은 **NOT TESTED**. 외부 대본/녹음 복사0, 자체 저작 provenance를 기록했으며 공식TOPIK/빈도 인증이 아니다.

## TTS·Transcript·Dictation 계약

신규120항목 모두 단일화자 시스템TTS/검증 녹음0, 전Production2,296개도 TTS다. 다화자 녹음/서로 다른 목소리 재생을 가장하지 않는다. audio_asset_id/transcript_ko=null, 실제 원문은 source_example_id의 Example을 읽는다. 질문 prompt_ko=null, transcript/번역/해설은 기존 ListeningView의 result 분기 뒤에 생성된다. 정적 확인은 VoiceOver/UI 실제 검증을 대신하지 않는다.

Dictation accepted는 정확한 원문1개. 안내는 문중 부호를 입력하고 끝 ASCII .!?는 생략할 수 있다고 명시한다. 기존 Swift judgeDictation의 NFC/공백 정규화·spacing warning·종결부호 생략 정책을 유지한다. 문중 부호·철자·단어·내용 오류를 정답으로 확대하지 않고 일반 ProductionAnswer를 바꾸지 않는다. 철자/조사/문장 경계는 각 원문과 직접 대조했다. 숫자 입력 변형을 약속하거나 새 숫자 정규화를 만들지 않았다. 실제 Swift 채점은 신규 native 메서드에 정답/오답/끝부호 생략/spacing/내부부호 변경/played gate를 작성했으나 이 환경에서 실행하지 못했다.

## 무결성·실행 결과·출시 gate

- Content26 원본/DB를 byte 그대로 불변 fixture에 보존했다. 신규 UUID300, 기존16,541엔티티 fingerprint/본문/ID/revision/순서/membership 불변, 기존103보호파일 byte 보존. 승인 기존 revision 목록은 빈 배열이다. canonical Source는 production.json 하나이며 authoring은 편집 색인이다.
- candidate strict previous26 오류0/기존경고10, integrity ok/FK0. Source25테이블69,787행, 재구성31테이블의 중복 포함 전체행/schema/index·SHA 일치. 기존 짧은 한글 음절/동형어 경고를 지우지 않았다. 26도 사전에 writer byte 재현했다. [build](DATA10_C_BUILD.json), [재구성](DATA10_C_REBUILD.json), [보존/수량](DATA10_C_COUNTS.json).
- 최종 portable 결과: **391/391 PASS (466.416초, failures/errors/skipped0, exit0)**. [원시 로그](DATA10_C_PORTABLE_TEST_LOG.txt), [결과](DATA10_C_TEST_RESULTS.json). 후보/targeted 수를 전체 고유 수에 합산하지 않는다. A/B 정확한 gate는25/26 fixture로 고정하고 C가26→27 전체 보존을 검사한다.
- 실제 SQLiteListening warm6page×20반복=120조회/2,400행, median0.294ms/max12.188ms. [측정](DATA10_C_QUERY_MEASUREMENTS.json). Python/SQLite 로컬 수치이며 iPhone cold launch·메모리·음성·3~10분 학습 측정이 아니다. 임시UserProgress의 B active snapshot/SRS due/opaque 사용자 테이블 보존 검사는 실제 개인 기기/Swift Codable 인증이 아니다.
- 현재 Cloud xcodebuild/swift 없음. iOS Build/144 XCTest 정의·실행0 **BLOCKED**. 기존 Mac142실행137PASS/5FAIL은 cohort/course가정3·되다/뵈다활용P1/꿰다 기대값 검토1·cold Purchase cache1로 남는다. 이번에 해결로 바꾸지 않는다. DATA08 P1 세 건의 이전 native 회귀 PASS도 역사 근거로 보존한다.
- 실제 TTS 발음·오디오 중단/기기 Offline·VoiceOver·저장/Resume·3~10분/RAM·AdMob/StoreKit 실제 권한은 미실행 gate다. 광고·구매·사용자 데이터 런타임 코드 변경0. **Release B—Conditional** 유지.

재현은 프로젝트 루트에서 실행한다. Writer가 다른 환경은 DATA10_WRITER.md에 따라 실제 byte 비교를 먼저 한다. SHA 불일치 시 통계 삭제/검사 완화/원본 교체로 숨기지 않는다.

```sh
python3 Tools/ContentBuilder/prepare_data10_c.py --output /tmp/data10-c.json --revised /tmp/data10-c-revised.json
python3 Tools/ContentBuilder/build_content.py /tmp/data10-c.json /tmp/data10-c.sqlite --previous Tests/Fixtures/content-v26-production.sqlite --production
python3 Tools/ContentBuilder/audit_data10_c.py --rebuilt /tmp/data10-c.sqlite --report /tmp/data10-c-counts.json --items /tmp/data10-c-items.md
sh Tools/verify.sh --portable
```

Git은 diff/대용량 blob/필수 checks·mergeability를 확인한 일반 commit/push/PR/server merge로 전달한다. Force Push/기존 원본 삭제/이력 재작성0. 최종 merge SHA와 clean main=origin/main은 실제 Git/PR 및 최종 응답이 기준이며 자기 SHA를 위한 재귀 commit은 하지 않는다. 이 Batch에서 종료한다.
