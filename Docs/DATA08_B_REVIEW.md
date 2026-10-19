# DATA-08-3 / Batch B 검수·통합 기록

Runtime 원본은 `Content/production.json` → 기존 ContentBuilder → `Resources/content.sqlite`이다. 이 문서와 ID 색인은 검수 자료이며 별도 학습 엔진이나 Runtime 입력이 아니다.

## 범위와 승인 수량

기존 Content15 Production과 Batch A 301어휘/602문장을 확인한 뒤, **신규 初中級 Vocabulary300 / 문장 Example600 / Meaning311**을 작성·검수·반영했다. 요청 범위270~400 / 450~650 충족, 품질을 이유로 줄인 수량0. 전체 DATA-08 목표 **800~1,200어휘 / 1,300~2,000문장**은 유지한다. 누적601/1,202, 잔여199~599/98~798이다. Batch C 및 이후 단계는 수행하지 않았다.

| 묶음 | 주제 | 신규 어휘 | 신규 문장 | 의미 | Note | 누적 Validator |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| B1 | 의견·판단·추측 | 100 | 200 | 104 | 30 | 오류0 / 기존경고10 |
| B2 | 비교·선택·계획·경험 | 100 | 200 | 102 | 33 | 오류0 / 기존경고10 |
| B3 | 원인·결과·영향·변화·개선·문제 해결 | 100 | 200 | 105 | 37 | 오류0 / 기존경고10 |
| 합계 | | **300** | **600** | **311** | **100** | 신규 경고0 |

품사: 동사148 / 형용사49 / 부사36 / 회화 표현34 / 명사33. 명사는11%다. 전300항목의 `meanings.usage_ja`에 Collocation을 명시했다. 11항목은 두 의미/용법을 분리하고 각각 별도 Meaning ID와 해당 예문을 연결했다. 비교 대상이나 해석만 다른 기존 문장을 복제하지 않았다. 신규 Grammar0 / Listening0 / Question0, 어휘 관계72 / 기존 Grammar 예문 참조15를 추가했다. 관계 수는 새 어휘·새 문장 수에 합산하지 않는다.

## 각 묶음의 Korean/Japanese Self Review

검수자는 작성자와 같은 **assistant**다. 300항목 전부의 표제어·품사·활용 metadata·뜻·Collocation·양쪽 예문과 번역, 100 Note를 작성 후 별도로 재독했다. 독립된 한국어/일본어 원어민·교육 전문가의 검수 승인을 받은 것은 아니다. Validator는 문장 자연스러움을 인증하지 않는다.

각 묶음마다 다음 과정을 끝낸 후 다음 묶음을 통합했다.

1. 직전 Production1,677개와 Batch A 전체를 포함한 표제어, 먼저 승인된 B 묶음과 후보를 대조했다. NFC·casefold·공백 제거 정규화로 표제어·한국어/일본어 문장·한일 쌍의 중복을 감사했다. 이번 신규와 기존 사이/신규끼리 중복0. 기존 동형어·경고·예문은 삭제하지 않았다.
2. 각 한국어 문장의 조사·주어/목적어·시제·활용·띄어쓰기·높임말·의미와 자연스러운 상황을 재독했다. 일본어는 의미 범위·수동/능동·시제·정중체·강도를 개별 대조했다. 결과·경험의 과거형, 현재 습관/상태, 계획·조건·추측·부탁·금지 등 문형과 가정/학교/직장/대화/여행/문제 해결 상황을 섞었다.
3. 入門/初級의 기본 어휘와 기존 Grammar의 연결·이유·대조·조건·과거·계획·경험·전후·부탁·가능·금지·추측을 중심으로 문장을 구성했다. 부담이 큰 중첩 구문은 더 짧은 문장으로 고쳤다. 추상 어휘의 新規初中級 배정은 편집 판단이며 TOPIK 공식 등급이나 전체 문장의 모든 단어에 대한 완전한 형태소별 선행 학습 증명이 아니다. 현재 schema에 없는 학습 prerequisite 그래프를 완성했다고 주장하지 않는다.
4. 의미별 예문과 Note, 기존 repository SQL의 카드·meaning·예문·Note·문법 참조를 조회했다. 신규 ID는 한 번 발급한 UUID4를 저장·재사용하고 앞 묶음의 ID를 다시 발급하지 않았다.
5. 각100어휘 단위의 누적 candidate DB에 실제 직전 Content15를 `--previous`로 strict build/Validator 실행했다. 무결성/FK·기존 payload/허용 revision·정규화 중복·UUID 감사와 재독을 통과한 후보만 승인했다. `DATA08_B1~B3_VALIDATION.json`, `DATA08_B1~B3_AUDIT.json`에 단계별 실제 결과/해시를 보존했다.

전체300개 원문·번역·뜻/예문 ID·Collocation·Note는 [카탈로그](DATA08_B_REVIEW_CATALOG.md), 최종 검수 payload의 SHA-256은 [EDITORIAL.json](DATA08_B_EDITORIAL.json)에 있다. 이 표시는 재독 대상을 추적하는 기록이며 무오류 보증이 아니다.

## 개별 교정과 의미 범위

승인 전 초안의 필드 교정 전후는 `DATA08_B_CORRECTIONS.json`에 기록했다. 품사·활용 및 후보 기본형도 별도로 대조했다.

- 단정하다: 목적어가 불명확한 문장을 `한 번의 실수로 능력이 없다고 단정하지 마세요.`로, 뒷받침하다: 주체/목적어가 뒤바뀐 초안을 `꾸준한 노력이 좋은 결과를 뒷받침해요.`로 고쳤다.
- 뜻하다는 뜻/예문의 대응을 유지하려고 이번 학습 범위를「意味する」로 한정했다. 되돌아보다는 물리적으로 뒤돌아봄/과거 회고를 별도 의미와 예문으로 나눴다.
- 대비하다는「対比する」의 목적어와「備える」의 `에` 결합을 분리했다. 거르다는 여과/빠뜨리기 두 용법과 `걸러요`를 설명한다. 사전에서 별도 동형 표제어로 나누는 용법도 여기서는 한 어휘의 서로 구분된 Meaning ID로 제공하며, 모든 의미가 같은 어원이라고 주장하지 않는다.
- 본래는 부사 용법이 드러나도록 명사 수식 초안을 `본래 하루만 쉬려고 했어요.`로 변경했다. `애초에` 후보는 명사 **애초**로 등록하고 에/부터 결합을 설명했다. `반대로` 후보도 명사 **반대**로 보정하고 조사 로를 설명했다. `마찬가지로` 후보는 명사 **마찬가지**, `뒤늦게` 후보는 형용사 **뒤늦다**로 기본형을 정리했다. 상대적으로 후보는 제법으로 대체하고 비교적과 제법의 차이를 설명했다. 활용형/조사 결합을 별도 신규어휘로 세지 않았다.
- 모자라다/넘치다는 사전 대조 후 **동사**로 정정했다. 모자라다는 르불규칙이 아니라 `모자라요`, 별다르다/색다르다는 르불규칙으로 `별달라요/색달라요`다. 그르다는 여기서 형용사 뜻만 다루며 `글러요`다.
- 견주다의 의미는 예문과 일치하는「比べる」로 정리하고, 간편하다의 일본어 번역은「使い方が簡単」로 다듬었다. 되풀이하다의 한국어/일본어 문장 주체를 친구로 명시했다.
- 이어지다/미치다/배경은 서로 다른 의미·통사 구조마다 Meaning을 분리했다. 미치다는 영향이 `이/가`로 주어가 되는 경우와 영향을 `을/를`로 목적어로 두는 경우를 구분하고,「正気を失う」의 별도 동형어는 이번 범위에서 제외했다.
- 확대되다의 소문 결합은 문제의 확대 장면으로, 급속히의 꽃 장면은 도로 신설 후 도시 성장 장면으로 자연스럽게 고쳤다. 작용하다의 중첩 사동·변하다의 복잡한 연결 흐름·비로소의 중첩 강조는 더 간단한 문장으로 수정했다.
- 일본어 Note에서 수긍하다/납득하다, 참고하다/참조하다, 실행하다/실천하다/실현되다, 경험하다/겪다/체험하다, 적당하다/알맞다, 긴급하다/시급하다, 급격히/급속히, 대응하다/대처하다 등의 의미·문체 차이와 자연스러운 조사 결합을 설명한다. 완전한 동의어로 일괄 처리하지 않았다.

## 사전 대조와 출처

품사/활용/기본형의 의문은 국립국어원 한국어기초사전의 실제 검색·상세 결과로 대조했다. 표제어 검색에서 결과가 없다는 이유만으로 단어가 잘못됐다고 판정하지 않고, 등록하려는 기본형의 실제 결과를 확인했다. 본래는 명사/부사 중 부사, 이제야·뜻밖에는 실제 부사 항목을 사용한다. 검색 결과와 근거 URL은 `DATA08_B_DICTIONARY.json`에 보존했다. 추가 부사 대조 중11건은 timeout/HTTP503으로 실패한 응답도 그대로 기록했으며, 해당 실패를 사전 확인 성공으로 세지 않았다. 뜻밖에는 그 이전에 성공한 조회 근거가 있다.

- 그르다(형용사, 그른/글러/그르니): https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=36298
- 모자라다(동사): https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=46143
- 넘치다(동사): https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=62327
- 애초(명사): https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=14270
- 마찬가지(명사): https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=28814
- 뒤늦다(형용사): https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=14987
- 본래(부사): https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=59602
- 이제야(부사): https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=24993
- 뜻밖에(부사): https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=15234

학습 예문·일본어 번역·Note·Collocation은 자체 작성했다. 사전 예문을 복제하지 않았다. 공식 TOPIK/빈도·발음 녹음·독립 전문가 인증은 추측하지 않고 해당 선택 metadata는 null이다. 기존 TTS/오디오 선택 정책을 유지했다.

## Stable ID·이전 배포 보존·통합

시작 `main/origin/main=e3f3350`, tracked/untracked 변경0. 기존 Content15를 `Tests/Fixtures/content-v15-production.sqlite`에 **원본 byte 그대로** 보존했다. SHA-256=`b4459a400dae7e7b5572688db928a7b550d865f9cf1b3dfd8cd22a86d5d6f75d`. 기존 Content14 fixture와 Batch A 원본 색인·검수 보고서도 유지했다.

신규 content_items1,314개(어휘300+뜻311+예문600+Note100+태그3)는 canonical UUID4다. 출처1개는 sources에 별도 기록한다. `sort_key=힣:data08:b:NNNN`, learning_priority602는 편집 순서이며 기존 순서 뒤에 추가한다. 표제어나 배열 위치에서 UUID를 파생하지 않는다. 기존 모든 상세 본문·kind·ID·created_at·sort_key·learning_order·lesson membership은 보존했다. 관계 추가에 참여한 기존 끝점28개(어휘13/문법15)는 revision+1/updated_at만 갱신했으며 승인 목록은 `Content/data08-b-revised-ids.json`이다. 삭제·병합·비활성화0.

승인 candidate와 Production Source 재빌드의 DB 해시/semantic signature가 같음을 확인한 뒤 번들 DB를 교체했다. **Content16 / Schema4 / minReader7 / UserProgress10**이며 schema/앱 reader/사용자DB migration 변경0. 기존 DB 테이블의 모든 행을 보존하고 새 관계만 추가했다. strict Validator 오류0 / 기존경고10(짧은 발음예문5 + 기존 동형어5), integrity=ok/FK위반0이다. 기존 경고를 삭제하거나 Validator/SQLite 제약을 완화하지 않았다.

Grammar는 기존42개를 유지하고15개의 새 Example ID를 참조한다. 실제 문법 예문 SQL의 LIMIT6 안에서 이전 예문과 새 연결이 모두 보인다. 의미별 vocabulary_examples와 Stable Example ID는 기존 Listening/Sentence Production 구조에서 재사용할 수 있지만, 이번600문장을 새 듣기/문항으로 배포한 것은 아니다. 활용은 기존 엔진과 metadata 계약을 따른다.

## 회귀검사와 실패 기록

첫 `sh Tools/verify.sh --portable`은 **254개 실행, 3개 실패, 251개 통과**, skip0이었다. 실패3개는 기존 Note 링크282→382와 전역 품사별 총수 기대값의 미갱신이다. 실제 SQL·제약·이전 cohort/ID/payload 검사를 유지하며 정확한 기대값만 갱신했다. 원시 초기 로그는 `DATA08_B_INITIAL_TEST_LOG.txt`에 보존했다.

Batch A의 정확한301/602와 Content14→15 검사는 immutable Content15 fixture에서 그대로 유지했다. 현재 Content16에서 Batch A를 포함한 기존 전체 행/사용자 기록이 보존되는지는 새 Batch B 검사로 추가했다. 기존 테스트를 제거하거나 무조건 참으로 바꾸지 않았다.

신규 B 회귀검사는12개다. strict15→16 재빌드·실제 수량·UUID4·전역/Batch 중복·카드/의미/Note 실제 SQL·활용 metadata·검색/연관어/문법 참조·bounded curriculum/20개 세트·5/10/20 due·enrollment 중복 방지·A 어휘20개로 구성한4/20 부분session 교체/재개·사용자DB byte 불변·세 skill SRS/favorite/설정/schema10 보존·깨진 후보 거부·세 묶음 gate/최종 검수 fingerprint를 확인한다.

기본형 보정 전 중간 재검사는255개 PASS였다. 이 후 마지막 사전 대조에서 반대로→반대(명사+조사)로 보정했고, B2/B3 strict gate·중복/ID 감사를 다시 통과시켰다. 같은 미배포 항목의 기본형을 바로잡으며 UUID는 유지했다. 이 보정본의 전체 검사도 다시 수행했다. 중간 로그는 `DATA08_B_INTERIM_TEST_LOG.txt`에 보존했다.

최종 `sh Tools/verify.sh --portable`: **255개 PASS / 실패0 / 오류0 / skip0 / exit0** (103.423초). 기존243+B 신규12 모두 통과했다.

최종 실행 수/종료 상태는 `DATA08_PROGRESS.md` §11 및 `DATA08_B_TEST_LOG.txt`를 따른다. portable SQL 검사는 Swift 실행이나 iOS UI 검사가 아니다.

## 미실행 gate와 범위 제한

기존 Swift 엔진에서 실제 신규어휘의 글러요/걸러요/별달라요/색달라요/모자라요/넘쳐요/까다로워요/해로워요/이로워요/순조로워요와 카드 metadata를 검증할 XCTest1개를 추가했다. 현재 **native 테스트 정의128개, 실행0**. 기존 Data07IntegrationTests의 초기 初中級270개 기대값도 현재871개로 갱신했다. 이는 테스트 유지보수이며 native 성공을 의미하지 않는다. 이 Linux 환경에 Swift/Xcode가 없어 type-check·Debug/Release build·SDK link·XCTest는 미실행이다.

앱 runtime·UI·학습 엔진·진도DB·SRS·로컬 저장/Resume·세션 크기·광고/IAP 설정 변경0. 기존 offline-first/선택적TTS·5/10/20개 복습·20개 세트·광고 경계를 유지한다. 실제 iPhone 3~10분 사용·비행기모드·통화/강제종료·TTS·VoiceOver·광고·StoreKit·알림은 별도 gate다.

기존 retirement active-review P1과 native 출시 gate를 유지한다. 初中級 Grammar0 / Listening2 / Question5와 상위레벨 공백은 후속 범위로 남았다. 이번 Batch B 범위에서 미해결 데이터 손상 P0를 재현하지 않았으나, 전체 제품의 결함 부재나 출시 승인을 의미하지 않는다.
