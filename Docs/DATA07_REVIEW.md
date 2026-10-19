# DATA-07 Editorial Review — 2026-10-06

## Scope and separate review

두 배치(200어휘/400예문, 250어휘/500예문)를 각각 작성·재독·중복 검사·기존 Validator 검증 후 합쳤다. 전체 목표 가이드 700–1,000개보다 적은 **450개/900예문**으로 범위를 확정했다. 남은 수량을 생성해 채우지 않고, 단어마다 두 예문·관계·기존 학습 경로 검증을 마무리했다. 신규 初級180/初中級270(40%/60%). 入門 추가0.

검수자는 이 작업을 수행한 assistant이며, 별도의 원어민 교육 전문가/인간 편집자가 승인했다고 주장하지 않는다. 학습자에게 노출되는 문장은 모두 실제 한국어/일본어이고 dummy/fixture는 없다. `DATA07_REVIEW_CATALOG.md`에 최종 DB에서 읽은 모든 새 어휘·의미·예문·note를 기록했다. 이 문서는 검수용이며 runtime source는 여전히 `Content/production.json` 하나다.

## Pass 1 — selection and semantics

기존926개 표제어와 비교해 새450개 모두 다른 표제어임을 확인했다. 명사128/동사176/형용사51/부사56/표현39. 고유명사로 수량을 늘리지 않았다. 의미475개, note36개. 공식 빈도·TOPIK·추측 발음은 null 유지.

- `풀다`, `든든하다`, `겨우`, `자신`, `입장` 등은 의미를 분리하고 해당 의미마다 예문 연결.
- `마련하다/준비하다`, `구별하다/구분하다`, `기한/기간`, `답장/회신`, `알아듣다/들리다`는 사용 차이를 note 또는 명시적 관계로 표현. 무조건 synonym으로 묶지 않음.
- `정하다/정해지다`, `식다/식히다`, `속다/속이다`, `망가지다/망가뜨리다`, `포함하다/포함되다` 등의 혼동 관계.
- `말을 놓다`는 상대와의 합의/관계를 설명하고 동갑이면 자동으로 반말해도 된다고 가르치지 않음.
- 수령/분실/회신 등 서비스·업무의 격식 차이를 note로 표시.

## Pass 2 — corrections before publication

- 한동안/당장: 문장에서 부사어로 쓰여도 이번 품사는 명사로 기록.
- 챙겨 가다/챙겨 오다: 띄어쓰기와 expression 분류 수정. 생산적 구를 임의의 단일 동사로 처리하지 않음.
- 이루어지다: 기본형으로 저장. 예문의 이뤄졌어요와 축약 설명은 유지.
- 타오르다/떠오르다/마르다/흐르다: 르 불규칙. 붓다(注ぐ):ㅅ, 알아듣다/되묻다/깨닫다:ㄷ, 가렵다/간지럽다 등:ㅂ.
- 하다형은 기존 가이드대로 other, 으·ㄹ 규칙적 변화는 none. 서술어/표현 has_batchim은 null. 표제어 끝의 다에 받침이 없다는 이유로0을 넣었던 초안을 수정.
- 한자어 일본어 설명, 느끼하다의 번역, 모퉁이 예문의 인위적인 대조, 되묻다의 불필요한 다시를 수정.
- 기존 문장과 동일했던 초안은 더 자연스러운 문맥으로 다시 작성. 최종 신규900문장은 기존 문장 및 서로 간 Korean 문자열 중복0, KO/JA쌍 중복0.
- Listening Korean-choice distractor는 처음에 새 문자열을 썼으나 기존 Validator의 검수된 Example 요구에 맞춰 실제 Example의 문장을 선택. 검증 규칙은 변경하지 않음.

참고한 공식 사전/자료(예문을 복제하지 않고 품사·활용 사실 확인에 사용):
- https://krdict.korean.go.kr/eng/dicMarinerSearch/search?mainSearchWord=동안 (한동안 명사)
- https://www.korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=261&pageIndex=1&qna_seq=333904 (당장 품사)
- https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=53811 (챙겨 가다 띄어쓰기)
- https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=48175 (되묻다)
- https://krdict.korean.go.kr/jpn/dicSearch/SearchView?ParaWordNo=14164 (간지럽다)
- https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=87020 (헹구다)
- https://krdict.korean.go.kr/jpn/dicSearch/SearchView?ParaWordNo=14974 (가렵다)
- https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=62054 (붓다)

## Pass 3 — merged data and integration

최종 DB의 범주별 표본(붓다·시다·한동안·마련하다·기한·건널목·차마·자신·말을 놓다)을 다시 읽고 모든 항목의 의미/예문/선택 note 관계를 SQL로 조회했다. 900문장 중 최대 한국어 길이는27자(공백/문장부호 포함). 긴 문법 설명을 어휘 카드에 쌓지 않았다.

기존42문법 중26개를 새28예문에 연결. 이유 -아/어서에는 순서만 나타내는 예문을 무차별 연결하지 않았다. 자동 문자열 일치로 모든 문법 관계를 추측하지 않는다. 23개 어휘 관계, 실제 활용 문제8개, 듣기4유형 각1개를 연결했다. 듣기 sentence 복사 없음.

두 batch와 최종 strict previous 검증 오류0. 기존 경고10은 발음용 짧은 예시5건, 기존 동형 표제어5그룹(저/차/일/쓰다/적다). 각 의미/품사가 다른 기존 항목이며 신규 duplicate candidate0. 경고를 삭제하거나 Validator를 완화하지 않았다.

## Remaining editorial coverage

- 初級800어휘로 생활 동작·집안일·상태 표현 보강. 의료기관 이용, 공공기관/주거계약, 구체적 취미와 반복 노출은 더 필요.
- 初中級270어휘는 관계/업무/서비스/태도 중심의 진입층. 장기 과정의 완성이나 공식 TOPIK 범위를 의미하지 않음.
- 初中級 전용 문법 course 아직0: 기존42개 문법만 재사용. 일부 자연스러운 예문에 나오는 -다 보니/-느라/간접화법 등은 후속 문법 콘텐츠에서 설명해야 함.
- 신규 직접입력8/듣기4는 통합 표본이며 새450어휘 전부에 독립 문제/듣기 항목이 있지는 않음. 검색 상세의 활용은 지원 가능한 서술어에서 기존 엔진으로 생성.
- 고급 어휘, 뉴스/긴 대화, 검증된 발음 녹음, 전체 문법350–500개는 아직 미완성.
