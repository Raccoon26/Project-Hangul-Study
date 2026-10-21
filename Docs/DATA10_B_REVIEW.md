# DATA-10-3 / Listening Batch B 검수·통합 보고

2026-10-21 JST. 최신 main `238b6452d9a69d61f9e187c6176cd76bb240b098`(PR19)과 DATA10_PROGRESS를 동기화한 Cloud checkout에서 작업했다. Content25→**26**, Schema4/reader7/UserProgress10 유지. 이번 단계에서만 신규 상황60개·내용이해60/받아쓰기60으로 **문제120개**를 반영한다. DATA10 누적120원문/240문제이며 전체150~250/300~500 목표를 유지한다. 남은 목표30~130원문/60~260문제이고 다음 Batch는 시작하지 않는다.

## 실제 콘텐츠·수량·배치

| 영역 | 신규 원문 | 문제 |
| --- | ---: | ---: |
| 감정 |8|16|
| 의견 |8|16|
| 판단 |7|14|
| 이유 |7|14|
| 결과 |7|14|
| 경험 |8|16|
| 계획 |8|16|
| 의견 차이 |7|14|
| 합계 |60|120|

내용이해의 편집상 초점은 이유9/화자 의도11/핵심8/세부9/변화5/판단2/조건3/근거1/계획5/순서2/결과4/목적1이다. 모두 기존 `comprehension` 엔진으로 채점하며 새 유형 엔진을 만들지 않는다. 받아쓰기는 짧은 연속 발화 전체를 대상으로 한다. 원문당 Example1/Listening2/Question2,180선택지와60개 정확한 accepted, 기존 source 재사용0·같은 신규 source의 추가 참조60이다. 문장/선택지/추가 참조를 새 원문으로 중복 계산하지 않는다.

전체 Example4,873→4,933, Listening2,056→2,176, Question3,673→3,793, content_items16,241→16,541. Vocabulary2,287/Meaning2,420/Grammar96/Course8/Lesson103은 불변이다. 全Listening1,936개였던 DATA10 시작 기준과 Batch A를 모두 포함해 중복 검사했다. 현재全듣기 유형은 의미50/한국어39/받아쓰기1,940/내용147이다. 初中級 Listening1,943→2,063이며 入門34/初級79는 불변이다.

새 learning_order2180~2299(batch109~114, 화면練習110~115), 각20문항·같은 source 두 유형은3구간 차이로 분리했다. 기존 빈칸/부분 batch/세션 순서는 채우거나 재작성하지 않는다. 기존 typed Curriculum/Listening 목록·SQLite 조회로120문항 모두 접근했다. 자동 SRS는 Listening ID별이어서 같은 source의 두 유형을 모을 수 있는 기존 한계가 남는다. 원문별 SRS 병합을 구현했다고 주장하지 않는다.

## 한국어·일본어·정답/오답 Self Review

assistant가 전60한국어/60일본어를 별도로 재독하고,120prompt/해설/정답·180선택지·60accepted를 검토했다. 한국어의 조사/활용·띄어쓰기·존대·지시대상/인용수혜자·시제·가능성/사실·자연스러운 상황과 일본어 의미/문체/뉘앙스를 대조했다. 각 객관식에는 원문 속 정답 근거와 두 오답 각각의 일본어 해설을 넣었다. a/b/c 정답은각20개이며, 듣지 않아도 배제하기 쉬운 주제 밖 오답을 줄였다.

[15필드 교정](DATA10_B_EDITORIAL_CORRECTIONS.json): B20의 의무형을 필요조건 문법으로 잘못 매핑하지 않도록 수정, B40의 부사 대신을 실제 `-는 대신` 역할 선택으로 재작성, B53 간접의문의 자연스러운 회화형, B19 높은 음 결합, B48 큰 물건/큰買い物의 크기·금액 혼동, B43 미수록 `-던` 부담을 줄인 표현, B20/B30/B57/B58의 오답 후보와 일본어 혼입을 교정했다. 교정은 후보 승인 전이며 기존 Production 항목을 바꾸지 않았다. 새 UUID도 재발급하지 않았다. 별도로 받아쓰기 공통안내를 끝 .!? 생략과 정확히 일치하도록1곳/60문항에 명확히 했다.

DATA09 初中級54문법 모두에 대해 자연스럽게 쓰인 형태와 현재 Grammar ID를 [재사용 근거](DATA10_B_GRAMMAR_REUSE.json)에 기록했다. 예: `잡아야`의 필요조건과 `확인해야 해요`의 의무를 구별하고, 인용/수혜자·추측/확정·경험 발견/미래 기대의 기능을 개별 설명했다. 이 표는 편집상 실제 용례 매핑이며 새 prerequisite/grammar_examples/자동 활용 생성 지원을 뜻하지 않는다. 기존 Grammar endpoint/revision·163후보120해결/7조건부/36미해결(Level8포함)은 변경하지 않았다. 모든 부수 문형의 선행 숙달을 인증하지 않는다.

[개별 AI 검수](DATA10_B_SELF_REVIEW.json), [실제 앱 payload60/120](DATA10_B_ITEMS.md), [중복/가까운 후보](DATA10_B_SIMILARITY.json). 기존4,873예문 전체+Batch내 NFC·공백제거/정규화·끝 .!? 제외 한국어 완전 중복0·한일쌍 중복0이다. 여기에는 원래1,936TTS와 A60원문이 포함된다. 가까운 후보는 bigram Jaccard 상위8에서 SequenceMatcher 상위3을 뽑아 재독했다. 교육적 의미 중복/모든 paraphrase 부재를 자동 점수로 보장하지 않는다.

검수 주체는 **AI Self Review**다. 독립 원어민·교사/전수 외부 사전·실제 TTS 검청은 **NOT TESTED**다. Level은 내부 初中級 편집 기준이며 공인 TOPIK/빈도 인증이 아니다. 외부 대본/녹음 복사0, 자체 저작 provenance를 기록했다.

## TTS·Transcript·Dictation

신규120항목은 전부 **단일 화자의 시스템 TTS**, 검증 녹음0이다. 보고된 말/인용이 있어도 동일 음성의 연속 발화이며 다화자 파일·서로 다른 목소리·실제 대화 녹음으로 표시하지 않는다. audio_asset_id/transcript_ko는 null, 실제 원문은 기존 Example ID로 읽는다. 재생 UI/음성 엔진 변경0이다. 기기의 한국어 voice 가용성·실제 발음/억양·오디오 중단은 이번 Cloud에서 실행하지 않았다.

全신규 prompt_ko=null, 정답 전 transcript·번역·해설은 기존 `else if let result = s.result` 아래에서만 View를 생성한다. audio completion의 played gate 뒤 제출하는 기존 정책을 보존했다. 소스/DB 검사는 실제 VoiceOver/UI 정보 누출 검사와 다르다.

Dictation accepted는 원문 그대로1개씩이다. NFC/공백 정규화·띄어쓰기 경고와 오답을 구별하고, `judgeDictation`은 **끝 .!? 생략만** 허용한다. 내부 문장부호·철자/내용 변경을 정답으로 만들지 않으며 일반 ProductionAnswer를 완화하지 않는다. 각 원문은100자 이하의2~3문장으로 입력 부담을 제한한다. 실제 학습 시간3~10분을 측정한 것은 아니다.

새 native1메서드는120문항·60source·정답/모든 오답·Dictation 원문/종결부호/공백/내부부호·played 전 거부/후 저장 완료를 검사하도록 작성했다. 총143정의/이번 실행0, **BLOCKED**다. 기존 Mac의142실행137PASS/5FAIL 및 DATA08 P1다섯 메서드 PASS는 역사 근거로 별도 보존하며 현재 Cloud 실행으로 복사하지 않는다. 활용 P1·Purchase cache 등 기존 실패 gate를 해결로 바꾸지 않는다.

## Stable ID·원본·재구성·검사

실제 직전25 Source/DB를 `Tests/Fixtures/content-v25-production.json.gz`/`.sqlite`에 byte 그대로 보존했다. frozen24·A검수 원고/기록도 불변이다. A 정확한24→25 검사는 frozen25로 고정했고 새25→26 검사가 현재 Production을 검증한다. 신규300UUID(Example60/Listening120/Question120)를 manifest에1회 발급, 기존 revision 승인 목록은 빈 배열이다. 기존16,241개 fingerprint/본문/ID/revision/order/membership과99개 기존 보호 파일을 보존했다. Source25테이블68,586행·integrity ok/FK0이다.

현재 Cloud Python/SQLite3.53.1에서 frozen25의 byte 재현을 먼저 확인했다. 격리 writer 추가 설치 없이 기존 builder로26도 재구성해 전31테이블(파생 검색·sqlite_stat1 포함)의 중복 포함 전행/schema/index·SHA가 일치했다. 통계 행 삭제/재배치·헤더 편집·Validator·assertion 완화0. 정확한 SHA와 명령 결과는 [BUILD](DATA10_B_BUILD.json), [REBUILD](DATA10_B_REBUILD.json), [COUNTS](DATA10_B_COUNTS.json)와 [최종 결과](DATA10_B_TEST_RESULTS.json)를 따른다.

후보 전용 **9/9 PASS,18.647초** 후 Production에 반영했다. 여기에는 strict 재현·기존 전체 행/ID 보존·全source/DB 대조·중복·54용례·오답/정답·bounded Offline 조회·A진행 snapshot/UserProgress·잘못된 accepted/Transcript/참조 거부가 포함된다. 사용자 상태는 임시 디스크/opaque JSON fixture 검사이며 실제 개인 진도·Swift Codable/기기 설정/권한 실행 인증이 아니다.

첫 전체 검사는 live 기대값에 남은 Content25/기존수량으로5FAIL을 관찰하고 중단(exit130)했다. 관찰된 FAIL과 중단 로그는 [초기 로그](DATA10_B_INTERRUPTED_PORTABLE_LOG.txt)에 보존했다. 누적 기대값을 실제26으로 갱신하고 A의 정확한25 기대값은 frozen25에 유지했다. 두번째 전체382개는 누적delta 기대값1FAIL/381PASS였다(514.289초). 누적 회귀1개와 쿼리6개 targeted PASS 후 최종 전체를 재실행해 **382/382 PASS,578.139초,실패/오류/skip0,exit0**를 확인했다. 검사/Validator를 삭제하거나 실패를 PASS로 기록하지 않는다. 전용/targeted 수를 최종 전체 고유 수에 더하지 않는다.

현재 Cloud에는 xcodebuild/swift가 없어 iOS build·143 XCTest·기기/실음성/독립 사람 검수는 완료로 표시하지 않는다. **Release B—Conditional 유지**. 이번 runtime 수정0·기존 native 활용/구매·테스트 cohort 가정 실패는 후속 gate다. 이번은 Batch B에서 종료하며 다음 Batch를 자동 시작하지 않는다.

재현(프로젝트 루트):

```sh
python3 Tools/ContentBuilder/prepare_data10_b.py --output /tmp/data10-b.json --revised /tmp/data10-b-revised.json
python3 Tools/ContentBuilder/build_content.py /tmp/data10-b.json /tmp/data10-b.sqlite --previous Tests/Fixtures/content-v25-production.sqlite --production
python3 Tools/ContentBuilder/audit_data10_b.py --rebuilt /tmp/data10-b.sqlite --report /tmp/data10-b-counts.json --items /tmp/data10-b-items.md
sh Tools/verify.sh --portable
```

writer가 다른 환경은 `Docs/DATA10_WRITER.md`에 따라 frozen25/현재26의 실제 byte 비교를 먼저 수행한다. 버전 문자열만으로 재현 성공을 주장하지 않는다. 다음 실제 콘텐츠 변경은 현재26을 previous로 먼저 보존한다.
