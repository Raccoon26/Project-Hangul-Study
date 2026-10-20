# DATA-10-1 듣기 분석·제작 설계

2026-10-20 JST, Mac 로컬의 PR #17 병합 main 기준. **분석·환경 설정만 수행**한다. Content24 / Schema4 / minReader7 / UserProgress10, Release **B—Conditional**을 유지한다. 새 원문/문제/UUID/revision/DB 배포0. DATA09의 콘텐츠 수량·통합 종료와 사람/출시 검증 완료를 구분한다. 실행 결과와 Git 전달은 [DATA10_PROGRESS](../DATA10_PROGRESS.md)가 기준이다.

## 조사와 재현

`PROJECT_STATUS.md`, `CONTENT_GUIDE.md`(특히 §3/5/21/24와 DATA08 SYSTEM), `DATA_PROGRESS.md`, `RELEASE_CHECKLIST.md`, `DATA08_PROGRESS.md` §15~16, `DATA09_PROGRESS.md` §13~14, `Docs/DATA09_CLOSEOUT.md`, DEV09/DATA06·DATA08/09 시스템 감사와 실제 구현을 대조했다. 오래된 ‘현재’ 수량은 최신 기준으로 합산하지 않았다.

읽기 전용 [감사 도구](../Tools/ContentBuilder/audit_data10_listening.py)와 [결과 JSON](DATA10_LISTENING_BASELINE.json)은 현재 DB의 모든 듣기/문항과 Source25테이블66,094행을 비교한다. 전체 Example4,813개를 향후 신규 중복 비교 대상으로 사용한다. source/DB 행 multiplicity·metadata, FK/integrity, active/level, 1:1 문제, 순서·batch 등의 **34개 구조 점검**과 문장 통계는 언어·음성 품질 승인과 다르다.

```sh
python3 Tools/ContentBuilder/audit_data10_listening.py --report /tmp/data10-listening-audit.json
sh Tools/verify.sh --portable
# Mac에서는 실제 설치된 iOS17+ destination으로 실행
TEST_DESTINATION='platform=iOS Simulator,id=<installed-uuid>' sh Tools/verify.sh
```

JSON은 Source/Bundle/과거 fixture 등95파일의 SHA를 포함한다. Production source `081ed35c7cd78345af1c1793fc450acaa2931f173cef00aaa960c8ef42318540`, bundle `56a7fa8b5358e254eeb324e706860d150d20c8ec013ba0b6f602cf14d93cceff`를 보존한다. 이번은 재배포 단계가 아니므로 현재24 fixture를 새로 만들지 않는다. 다음 실제 콘텐츠 변경 전에 현재24 원본과 DB를 불변 snapshot으로 보존하고 strict previous로 사용한다.

Mac Python3.11.6/SQLite3.44.0의 validate-only·임시 재구성은 strict23→24 오류0/기존10경고지만 **byte/schema 재현은 불일치**다. [비교 근거](DATA10_REBUILD_COMPARISON.json): 기존31테이블 전행 multiplicity/column/FK/index metadata와 공통 schema SQL은 같고, ENABLE_STAT4 환경이 내부 sqlite_stat4(948행)를 추가해32테이블이 됐다. DB 크기18,841,600→18,972,672bytes, 임시 SHA `b24a216e1e583308d905d67ae1a0d2bc779f19b1004a32583b8f730a022220ab`. header writer도3.53.1→3.44.0으로 다르다. 통계 테이블 삭제/validator 완화·Production 교체로 맞추지 않는다. 다음 실제 배포 전 기존 writer3.53.1 및 compile profile 재현 환경을 확인해야 한다. strict 유효성과 binary/schema 동일성을 별도 gate로 유지한다. frozen Content23의 byte 비교 실패도 [독립 재구성](DATA10_REBUILD_V23_COMPARISON.json)으로 같은 원인/원래31테이블 전행·공통schema 보존을 확인했다.

## 현재 수량·중복·분포

| Level | 의미 선택 | 한국어 선택 | 받아쓰기 | 내용 이해 | 합계 | batch |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 入門 |4|23|3|4|34|4|
| 初級 |28|4|25|22|79|7|
| 初中級 |0|0|1,822|1|1,823|93|
| 전체 |32|27|1,850|27|1,936|104|

전체 Vocabulary2,287 / Meaning2,420 / Example4,813 / Grammar96 / Question3,553은 DATA09 종료와 일치한다. 모든 듣기는 active Example을 참조하는 TTS, 검증 녹음0, transcript 복사0, 문항당 문제1개다. 현재 상위 Level 듣기0을 완성된 상위 과정으로 표시하지 않는다.

듣기1,936개는 source Example ID가 모두 다르고, NFC+연속공백 정규화한 한국어·한일 문장 쌍 중복0, 종결 .!? 생략 비교도0이다. **의미상 유사성/단순 치환 문장까지 없다는 보장은 아니다.** 전체 Example에는 한국어 동일/일본어 다름4쌍이 있다(‘매일 한국어를 공부해요.’, ‘이 정도면 충분해요.’, ‘표를 미리 샀어요.’, ‘한국에 처음 왔어요.’). 완전히 동일한 한일 쌍0. ID는 JSON에 남기며 번역/문맥을 비교하기 전에 자동 병합하지 않는다.

동일 마지막3어절이3회 이상 반복된 것은 ‘대책을 세워야 해요.’3개다(IDs는 JSON). 이는 template 검토 신호일 뿐 중복 확정이 아니다. 향후에는 원문 전체에 대한 exact/종결부호/공백 비교와 함께 유사 어휘·문형·상황·정답 근거를 사람이 재독해야 한다. 이번 표본과 휴리스틱만으로1,936개 전부의 의미 중복·난도 적정성을 승인하지 않는다.

## 난도·교육적 가치와 한계

| Level | 문자수 min / median / p90 / max | 어절수 min / median / p90 / max | difficulty |
| --- | --- | --- | --- |
| 入門 |8 /11 /14 /18|2 /3 /4 /5|전34개 null|
| 初級 |8 /13 /17 /22|2 /3 /4 /6|전79개 null|
| 初中級 |13 /22 /26 /35|3 /6 /7 /11|전1,823개 null|

문자수는 NFC/공백 정규화 후 공백·문장부호 포함, 어절은 공백 분리, median은 정렬된 중앙 상위 값이다. 길이는 입력 부담의 대리 지표이며 실제 청취 시간·공인 TOPIK 난도·음성 속도를 측정한 값이 아니다. 편집 난도1~5를 추정해 DB에 채우지 않는다.

받아쓰기1,850개는 전체95.56%, 初中級 받아쓰기1,822개는 해당 Level99.95%다. DATA08의1,821개 고유 문장을 추가한 연습은 넓은 어휘·띄어쓰기·형태 재인식에 가치가 있지만, 들은 핵심정보를 고르는 능력과 철자 입력 능력이 점수에서 섞인다. 고유 원문 수만으로 듣기 능력 전반/적응형 교육과정을 충분히 제공한다고 보기 어렵다. 多문장 항목은4개뿐이며 단일 사실을 듣는 연습이 중심이다. 이는 문장부호 기준 탐지이며 실제 화자 수/담화 유형을 인증하지 않는다.

현재 Grammar96개 중29개만 공유 Example을 통해 듣기와 연결된다. DATA09 신규54개 중4개는 기존 DATA08 Example4개를 재사용한 덕분에 연결되고, **새로 만든216개 예문에는 듣기 추가0**이다(신규54의 전체 연결 Example220개 중4개만 듣기에 있음). 이 차이를54개 모두의 독립 청취 연습 완료로 표현하지 않는다.

기존 선행 후보163개는 전부 현재 듣기에 있으며 설명 coverage 판정은120해결/7조건부/36미해결 그대로다. 이 중 Level 검토8건도 유지한다. 미해결 문장을 자동 재활용하거나 그 문법을 모두 배운 것으로 전제하지 않는다. 새 원문은 기존96문법의 설명/배치와 필요한 부수 문형을 개별 확인한다.

일본어 피드백이 번역과 같은 문제는1,825개다. 정답 후 의미를 확인할 수 있으나 왜 틀렸는지·들어야 할 단서·발음과 표기 차이를 가르치는 설명은 제한적이다. 이를 잘못된 정답1,825개로 해석하거나 이번에 일괄 수정하지 않는다.

assistant가 level×존재하는 task별 길이 min/median/max의 중복 없는 **28항목**(한일28쌍·28문제·57선택지·해설)을 한국어/일본어·지시문·선택지·정답 근거·해설 관점에서 재독했다. 선택 규칙/전체 ID·본문은 JSON에 있다. 독립 원어민·교사/실제 TTS 청취 검수가 아니다.

| 대표 Listening ID | 관찰 | 후속 설계 판단 |
| --- | --- | --- |
| `15526c68-f89c-4ecc-a004-2fcf63887fec` | 국이 싱거워요. / 味が薄い, 짜요·뜨거워요 대비 | 동일 상황의 의미/소리 구별에 유효. 단순 최소쌍 녹음 품질 인증은 아님 |
| `45933bf3-7516-4e54-b557-9a8bd5191243` | 가족 몰래 선물을 준비했어요. / 비밀 대상 질문 | 가족이라는 실제 근거를 듣게 하는 명확한 정보 선택 |
| `60b86440-9b7a-41dd-95a1-c0dc3e931a51` | 걱정하지 마세요. 저는 괜찮아요. | 두 문장의 기능·상태를 묻는 짧은 담화 확장에 참고 |
| `3284897a-abfa-4140-b09d-18861db615b0` | 여기에 앉아도 돼요? / 許可, intro | 짧아도 결합·기능 설명이 필요. 길이만으로 입문 적합성 확정 금지 |
| `ab5d752f-832d-427e-982a-09151d68349e` | 섣불리 약속하지 말고 일정을 확인하세요. | 부사·부정연결·명령의 부담이 함께 있음. 철자 외 핵심행동 질문 후보가 가치 있음 |
| `f1dff8d0-ad83-437f-af1b-7fd5ae7f60ca` | 작은 회사도…어깨를 나란히 할 수 있어요. /35자11어절 | 비유/양보/범위 이해와 긴 입력을 구분. Level 확정 오류로 단정하지 않고 재검토 대상으로 둠 |
| `ca6e2de8-4257-4f3c-b2f0-de4b475d9642` | 반품 / 返品, 피드백은 번역만 | 새 문제에는 반품·교환을 가르는 청취 근거를 짧게 설명 |

## 기존 엔진에서 가능한 제작 설계

| 경로 | 실제 계약 | 설계에 미치는 영향 |
| --- | --- | --- |
| `SQLiteListening` | active source/question 조회, level 일치, 1 listening : 1 question, limit20; 목록30batch | 같은 원문에2문제를 연결하려면 Example1 + Listening2 + Question2. 한 listening에 문제2개를 넣지 않음 |
| `ListeningSession` | meaning/korean/dictation/comprehension, 처음 듣기 완료 후 제출, 1회 retry, 최대20 | 새 유형/화자 엔진 없이 현4유형에서 확장. 문항수를 학습시간 보장으로 쓰지 않음 |
| `ListeningStudyView` | 수동 normal/slow/stop, 완료 callback으로 heard 저장, 제출 후에만 transcript/번역 View 생성, 화면 이탈/비활성 stop | 선택형의 Korean 후보 노출은 의도한 출제. 정답 원문/번역 별도 표시와 VoiceOver 누출은 방지·기기 검증 |
| `KoreanAudioService` / `AudioPolicy` | word_sentence TTS≤500자, ko-KR 설치 voice 확인, normal0.5/slow0.42, 자모·[]/→+ 금지 | 속도는 AVSpeech 입력값이며 초당 음절수가 아님. 대화는1 TTS 원문으로 읽을 수 있는 짧은 연속 발화/안내로 제한 |
| `SQLiteProgressRepository` | 판정/attempt/event/SRS/snapshot transaction, 오래된 revision·중복 방어, SRS Listening ID별 | 같은 원문 두 유형은 별도 학습항목. 원문 숙달로 합산하거나 mastery 전파를 새로 만들지 않음 |
| Content Version / due | 시작한 snapshot 우선, 확정 unavailable만 버전별 보류, 원SRS 보존 | 기존20문항 구간·순서·고정 session을 새 콘텐츠 때문에 재편성하지 않음 |

현재 화면은1문제씩 원문을 공개한다. 같은 원문의 다른 유형을 바로 이어 놓으면 답 기억을 측정할 수 있으므로 **서로 다른 연습 구간으로 분리**한다. 자동 SRS due가 나중에 같은 원문의 두 Listening ID를 함께 선택할 가능성은 현재 엔진의 한계이며, semantic dedup scheduler/전역 순서 제어를 이번 설계로 구현했다고 하지 않는다. 사람 검수에서는 재생 없이 prompt/선택지만 보고 정답이 드러나는 문항도 확인한다.

## 신규150~250원문 /300~500문제 계획

**기준안200고유 원문·400문제**, 원문당 서로 다른2유형. 최소150/300~최대250/500 범위를 유지한다. 원문1개는 canonical Example1개의 한일 지문1쌍이며 내부에2~3문장이 있어도 원문 수를 늘리지 않는다. 아래는 편집 계획이며 runtime ID·승인 콘텐츠·확정 Level이 아니다. 기존 문장 재사용은 별도 관계 수로 기록하고 신규200에 포함하지 않는다. 본 단계 제작0/승인0.

| Level 기준안 | 고유 신규 원문 | 의미 | 한국어 | 받아쓰기 | 내용이해 | 문제 합계 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 入門 |20|12|12|6|10|40|
| 初級 |60|32|20|20|48|120|
| 初中級 |120|56|28|54|102|240|
| 합계 |200|100|60|80|160|400|

신규 문제의 받아쓰기 비중20%, 내용 이해40%로 기존 편중을 보완한다. 400추가 시 전체2,336 중 받아쓰기1,930(82.62%)이므로 이번 한 단계 확장만으로 전체 균형이 해결되었다고 하지 않는다. 초안 손질로 범위를 조정할 때는 원문/문제 수를 함께 다시 산정하고 실패 행을 조용히 버리지 않는다.

| 검수 가능한 Batch | 신규 원문 /문제 | 잠정 Level | 의미 /한국어 /받아쓰기 /내용 |
| --- | --- | --- | --- |
| A 생활 정보·입문 연결 |50 /100|入門20+初級30|28 /22 /16 /34|
| B 변경·이유·다음 행동 |50 /100|初級30+初中級20|28 /22 /22 /28|
| C 업무·공공/생활 안내 |50 /100|初中級50|22 /8 /21 /49|
| D 관계·의도·담화 정리 |50 /100|初中級50|22 /8 /21 /49|

주제별 고유 원문은 시간/수량/장소·약속30, 쇼핑/음식/서비스30, 이동/주거/공공안내30, 학교/업무/학습35, 건강/안전/생활관리25, 관계/감정/의도25, 이유/변경/순서가 있는 짧은 안내25로 합200을 계획한다. 건강/공공 문장은 실제 의료·법률 조언을 새로 제공하는 자료로 만들지 않고 상황 속 발화 이해를 다룬다. 주제 수는 공인 빈도나 현재 DB의 topic 전수 분류 결과가 아니다.

주제는 편집/검수 원장 기준이며 현 카탈로그 UI는 level별 ‘練習番号’다. topic playlist/다화자 Unit UI를 이미 지원한다고 하지 않는다. 원문별 학습 목표는 기존 active Meaning/Grammar의 실제 ID와 연결 가능성을 조사하고, 부수 문형·낯선 어휘의 설명 필요성을 검수한다. 모든 예문 토큰이 Vocabulary에 등재됐다고 가정하지 않는다. 기준안 그대로 채택되면 Example200+Listening400+Question400의 학습 엔티티1,000개가 필요하나 이는 아직 발급/승인되지 않은 예상량이다. Choice3개 기준 선택형320문제의960선택지는 question 내부 choice ID이며 별도 신규 원문/학습 엔티티로 합산하지 않는다.

入門은 친숙한 어휘·1문장/1정보, 初級은 짧은1~2문장과 시간/부정/이유/요청, 初中級은2~3개의 연결된 짧은 문장과 의도/조건/순서/다음 행동을 목표로 한다. 길이 목표는 각각 대략8~25/15~45/25~90자이나 자연스러움과 지원 문형을 우선하며 수량 채우기용 길이/치환을 강제하지 않는다. 화자 교대·배경음·동시발화·자연 녹음의 억양 대비·음성인식·새 schema/채점기는 별도 범위다. TTS를 실제 대화 녹음으로 표시하지 않는다.

내용 이해는 원문에서 직접 확정 가능한 정보/이유/발화 의도를 묻고 과도한 세상 지식 추론·복수 정답을 피한다. 의미 정답은 source 일본어와 일치, Korean 선택의 모든 후보는 실제 existing Example 문장이어야 한다. distractor를 만들기 위해 의미 없는 Example을 신규로 추가하지 않는다. 자연스러운 기존 후보가 없으면 원문/task 조합을 재설계한다. Dictation accepted는 원문+허용 종결 .!? 생략만, 내부 철자/조사/문장부호·띄어쓰기 판정을 일반 직접입력까지 확대하지 않는다.

## 후속 제작·검수·통합 gate

1. 각 Batch 시작 전 fetch/main/미커밋/최신 원장 확인. 최초 실제 변경 전 Content24 source+DB snapshot을 보존하고 이후 Batch는 실제 직전 배포를 previous로 삼는다. 기존 ID·본문·sort_key·learning_order·membership·snapshot을 유지한다.
2. 후보를 전체 Example4,813개와 Batch 내부의 한국어/NFC/공백/종결부호/한일 쌍, 의미·상황·문형으로 비교한다. 동일 한일 쌍은 기존 Example ID를 재사용하고 새 원문 수에서 뺀다. 동형·다의/다른 번역은 근거를 남기고 자동 병합하지 않는다.
3. 신규 실제 엔티티만 canonical 소문자 UUID를1회 발급해 production source에 저장한다. Example1→Listening2/Question2의 관계 끝점 revision 정책을 적용한다. 기존 끝점 변경은 ID별 승인목록과 before/after로 검증한다. Authoring 문서/계획 key를 runtime 입력으로 삼지 않는다.
4. 한국어 원문·일본어 번역·목표 문형/부수문형·높임·시제·지시대상·prompt·모든 distractor·정답 유일성·설명을 항목별 검수한다. 작성 후 별도 재독→수정→재검증 기록을 남긴다. 기존36미해결·7조건부·Level8과 새 후보는 자동 승인하지 않는다. assistant 자체 검수와 독립 원어민/교사의 승인을 구분한다. 불확실한 사전/뉘앙스는 그때 실제 원자료를 확인·기록한다.
5. 독창적 작성과 작성 주체/권한을 sources/item_sources에 명시한다. 외부 대본·녹음을 허가 없이 복사하지 않는다. TOPIK/빈도/녹음 인증·권한을 추측하지 않고 미확인 선택값은 null. normal/slow를 설치 voice/기기에서 실제 들어보고 한일 의미·억양·숫자·띄어쓰기의 청취 가능성을 확인한다.
6. level별 **다음 새20칸 구간**부터 추가한다. 현재 값은 入門100 /初級220 /初中級2060이지만 실제 제작 시 재집계한다. 기존 빈 칸/부분 batch를 채워 실행중 구성을 바꾸지 않는다. 같은 source의 두 유형은 인접/같은 batch에 넣지 않는 편집 배치를 검증한다. SRS의 전역 순서 제어 보장은 별도다.
7. 임시 candidate로 기존 Importer→strict Validator(`--previous`)→integrity/FK→Source/DB·UUID/중복/고아/정확한 허용 revision·기존 payload/order 보존→통합 회귀 순으로 통과한 DB만 배포한다. 버전은 실제 콘텐츠 변경 시 content만 증가하며 데이터 추가만으로 Schema4/reader7/UserProgress10을 올리지 않는다.
8. 기존 portable와 가능한 native 전체·DATA08 P1 세 건을 재실행한다. 실제 카드/학습/재생완료/stop/오답/retry/SRS/남은due/중단/오프라인·Content교체 snapshot/VoiceOver·IME·3~10분·광고/구매 독립성을 검증하되 미실행 gate를 완료 처리하지 않는다. 단계 원장에 시작/종료/증가/level/경고/실패/skip/검수/수정/미해결과 Git 전달을 누적한다.

DATA10-1은 이 계획과 환경 설정에서 종료한다. 다음 Batch를 자동 시작하지 않는다. Release **B—Conditional**, 독립 사람·사전 **NOT TESTED**, 실제 iPhone QA는 남는다.
