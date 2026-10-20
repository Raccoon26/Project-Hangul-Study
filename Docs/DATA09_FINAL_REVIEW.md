# DATA-09-5 최종 품질 감사

이번 단계는 **assistant AI 자체 검수**다. 독립 원어민·교사 검수, 외부 사전 대조는 **NOT TESTED**다. 자동 검사 통과는 언어 정확성·교육 효과의 인증이 아니다. DATA09-6 또는 DATA10은 진행하지 않는다.

## 범위와 방법

clean main/origin/main `b61866a7669bc1bf3fa2211fe45b08457b34cb0e`에서 `data09-5/final-content-audit`로 시작했다. 이전 미커밋 파일은 없었다. PROJECT_STATUS/CONTENT_GUIDE/DATA_PROGRESS/RELEASE_CHECKLIST/AGENTS/DATA08_PROGRESS/DATA08_CLOSEOUT/DATA09_PROGRESS와 실제 Source·DB·Validator·SQLiteGrammarContent/Progress·ProductionAnswer를 대조했다.

A/B/C 각각18개, 총 **54개 Grammar/Expressions의 모든 설명 필드, 고유 신규 Example216개, 기존 DATA08 재사용 Example4개, Grammar Question216개, 선택지648개와 모든 정답·오답 해설**을 실제 Content22 DB에서 재독했다. 한국어 형태/의미/결합/활용/띄어쓰기와 일본어 의미/설명/문체/수혜자/시제의 검토를 구분했다. 전체 문법96개를 이번에 전부 언어 재검수했다고 주장하지 않는다. 기존42개는 관계·비교 대상과 자동 검사 범위이며, 신규54개의 유사 문법 설명에서 필요한 부분을 대조했다.

- 전수 검수의 문법별 ID·예문·문항·유의사항: [EDITORIAL](DATA09_FINAL_EDITORIAL.json).
- 고위험 재감사:18개 Grammar의 form/constraints/confusion, 첫 Example18개, 선택한 Question18개(모든 선택지/해설). ㄷ/ㅂ/ㄹ 활용, 부정 범위, 결과 상태, 인용의 행위자/수혜자, 높임, 시제/조건을 다시 읽었다.
- 별도 무작위:seed20261020095·각 Batch3 Grammar/6 Example/6 Question = **45개**. Content22 registry 순서에서 한 번 추출하고 다시 뽑지 않았다. 교정 후 candidate23을 별도로 재독했다. 선택 목록 [SAMPLES](DATA09_FINAL_SAMPLES.json), 항목별 실제 재검토 메모 [REAUDIT](DATA09_FINAL_REAUDIT.json). 전수/고위험/무작위의 겹침을 독립 검수자나 신규 수량으로 더하지 않는다. 추가 발견0은 표본의 언어 무오류 인증이 아니다.

## 수정한 13개 사항

교정은 **25개 기존 ID의 31필드**다. Stable ID/정답 choice ID/answer_json/관계/수량/Level/배치는 유지하고 소유 엔티티 revision만 각1 증가했다. 본문 변경이므로 **Content22→23**, Schema4/reader7/UserProgress10 유지. 소유 엔티티는 문법9개·예문8개·문제8개다. 선택지3필드의 소유자는 해당 문제다. 카드 Note만으로는 독립 문항의 성별 문맥이 충분하지 않아 F13의 3문항을 추가 교정했고, 첫 후보 검증 로그와 최종 후보 검증 로그를 분리했다. 형태 설명 오류와 문맥 단정·일본어 품질을 교정했다. 런타임 코드는 보존하고 기존 native P1 검증 gate를 유지한다.

| 번호 | 위치 | 교정과 근거 |
| --- | --- | --- |
| F01 | A01 Q3 | 늦게 끝났다는 사실만으로 회의가 길어졌다고 단정한 선택지/해설을 종료 시점 설명으로 수정 |
| F02 | A09 Q2 | `들려면`은 `들다+려면`. `들리다`와의 혼동이라는 잘못된 기본형 설명 수정 |
| F03 | A08 | 이유 `-(으)니까`를 반드시 이미 성립한 사실로 제한하지 않도록 대조 설명 수정 |
| F04 | A17 | `-(으)면`도 일반적·반복 조건에 사용 가능. 일회성으로 제한한 설명 수정 |
| F05 | A18 E3 | 신청 자체가 회원이 되는 것처럼 읽히는 화제 구성을 실제 신청 상황의 부사절로 교정하고 번역 일치 |
| F06 | B01 | 때절의 시간을 주절 시제만으로 판단하지 않고 수식형·시간어·문맥도 함께 보도록 수정 |
| F07 | B06/Q4 | `-고 있다`의 착용·보유 등 결과 유지도 인정. 도어를 지금 여는 장면을 지정해 진행 해석/정답 범위 명확화. `-아/어 있다`만으로 의도적 준비를 보장하지 않음 명시 |
| F08 | B12 E3 | 며칠간 일찍 잔 것을 일본어 `数日間早寝`로 풀어 며칠 앞당겨 잔다는 오독 방지 |
| F09 | B16 Q4 | `자는 것 같아요`도 습관 추측 가능하므로, 지금 자는 장면을 문제에 명시 |
| F10 | B18/Q1 | 김에의 진행·예정 행동/기회를 어색한 일본어 `すでに行う行為` 대신 자연스럽게 설명 |
| F11 | B10/E4 | `으니`가 비문이라는 판정이 아니라 선행 부담 조정. 이미 배운 `으니까`로 교체 |
| F12 | C05 | 학습자 설명에 노출된 내부 계획 키P25/P26 제거 |
| F13 | B03/B11/B16/C11 | `동생`은 동생의 성별을 지정하지 않는다는 Note 추가. 일본어 弟는 이 카드의 남동생 장면임을 명시하며 번역 자체를 비문으로 보지 않음. 독립 표시되는 3문항에도 남동생 장면 명시 |

정확한 before/after·행 키·필드·근거는 [교정 manifest](../Content/data09-final-corrections.json), 소유 ID는 [revision 목록](../Content/data09-final-revised-ids.json). A/B/C authoring·과거 검수 기록·registry를 덮어써 이력을 없애지 않았다. Content22 원본 gzip/DB를 불변 fixture로 보존하고, `prepare_data09_final.py`는22+manifest로 같은23만 재현한다. 앱 canonical Source는 계속 `Content/production.json` 하나다.

## 163건의 재분류

기존 [DATA09_PREREQUISITE_AUDIT](DATA09_PREREQUISITE_AUDIT.json)의163개 ID/원문/기존 분류는 그대로 보존했다. 새 [FINAL_PREREQUISITES](DATA09_FINAL_PREREQUISITES.json)에 한 문장씩 한국어·일본어·검토 이유·실제 지원 Grammar ID·보류 근거를 기록했다.

| 결과 | 수 | 의미 |
| --- | ---: | --- |
| 해결 | 120 | 지적된 문형 기능을 현재 카드 설명으로 지원할 수 있음. 사람 승인·모든 어휘 토큰 학습 완료·문장 자동 배치 완료를 뜻하지 않음 |
| 교육적으로 허용 가능 | 7 | 기존 문법의 합성/오탐/Collocation 등의 조건부 해설로 사용 가능. 조건은 각 record에 기재 |
| 미해결 | 36 | 목표 문형 일부가 생겼어도 추가 구조·기능·부정 범위·난도 검토가 남음. 재사용 승인 안 함 |

원래 Level·배치 재검토8건은 전부 미해결 유지했다. 예: `부모님이라도`의 신분 양보를 B10 차선 선택으로 해결하지 않음; `달라는 요구`/`기다리라는 말투`의 요청·명령 인용 수식을 평서 인용 수식으로 대체하지 않음; `-다고` 이유 일반화 부정, `-고 나니`/`-(으)니` 발견, `-(으)려는`, `-기` 일반 명사화, `-게` 부사화, `-는 게 낫다`, `-아/어하다`, `-아/어 두다`, `-(으)ㄴ 끝에`, `-아/어서는 안 되다` 등의 공백 보존. 기존 보고의 `으니=니까 축약` 설명은 이번에는 확정하지 않고 별도 문형 검토로 남겼다.

163건의 원문/Level/관계를 고치거나 새 카드에 일괄 연결하지 않았다. `reuse_approved=false`, `production_links_added=false`, `human_reviewed=false`를 유지했다. 이는 이번 단계의 추가 승인0이며, Batch B에서 이미 재사용 승인된4개 관계는 보존하고 별도 flag에 표시했다. 해결120건도 별도 문제·학습 순서 설계 없이 곧바로 초반 단원에 투입할 수 있다는 뜻은 아니다.

## 문제·입력 채점 및 반복성

신규216개는 전부 기존 엔진의 단일 객관식으로 각3선택지/정답1개다. 정답과 두 오답을 문맥·지정 형태·발화 의도에 맞춰 재독했다. 다른 문맥에서 문법적인 오답은 해당 문항에서 왜 맞지 않는지 확인했다. F01/F07/F09의 장면 단정은 교정했으며 답 ID와 기존 선택지 순서는 바꾸지 않았다. C17의 `들을 수록`/`들을수록`은 띄어쓰기를 평가하는 의도된 선택지 차이이므로 공백 제거 후 같은 문장이라는 이유로 합치지 않았다.

신규 문법용 직접입력 문항은 **0 / N/A**다. 기존 `text_input`1,227개·`listening_input`1,850개의 nonempty/정규화 중복 없는 accepted 계약은 전수 자동 검사했다. 이 기존3,077개 문제 전체를 언어 재검수했다고 주장하지 않는다. `ProductionAnswer`는 NFC·연속 공백을 정규화하고 exact→spacing(허용 시)→incorrect를 구분한다. 끝 `.!?` 생략은 `judgeDictation`에서만 다루며 일반 입력의 철자/내부 문장부호를 느슨하게 하지 않는다. 기존 regression 및 실제 SQL 경로를 portable로 실행하지만 **Swift 판정 실행·일본어 IME·iOS UI는 BLOCKED**다. 새 문법54개의 모든 활용을 기존9형 ConjugationEngine이 자동 생성한다고 주장하지 않는다.

진행 중 GrammarSession은 문항 본문·해설·선택지를 포함한 bounded snapshot을 보존한다(Models/GrammarModels.swift, GrammarLearning.expose). 따라서 이번 교정은 Content23에서 새로 읽는 문항에 적용되며, 이미 저장된 세션의 과거 문구를 소급 재작성하지 않았다. 정답 ID를 유지해 기존 판정 계약을 보존했지만 실제 iOS Resume 확인은 BLOCKED다.

고유 신규 예문216개는 기존 전체 DB/Batch 간 정규화 중복0. 질문은 task별54개이며 A/B36개 meaning 질문에 기본 의미 선택 프레임이 반복된다. 선택지 문구 재등장은 `〜するつもりだ`3회, 나머지 반복 문구는 각2회 수준이다. 반복이 정답 복수나 비문을 뜻하지는 않지만, 변별도·장기 반복학습의 질은 교사/학습자 검증이 남아 있다.

## 남은 범위·출시 조건

신규54/216/216의 전체 수량 목표는 유지한다. 전체 Production Grammar96(入門22/初級20/初中級54)·Example4,813·Question3,553·Vocabulary2,287. 장기 Grammar/Expressions350~500 목표의 잔여254~404개를 축소하지 않는다.

새로 재현한 P0/P1 런타임 문제는 없다. 기존 DATA08의 native P1 회귀 확인·B—Conditional·독립 사람 언어/난도 검수 gate는 해결 처리하지 않는다. 원어민/교사 재확인이 특히 필요한 사항은 조건·이유 일반화 부정, 결과상·수혜자 관점, Register, 추론/양보 문맥, Level8건과 미해결36건이다. 현재 SQL로 대조한 주선행 DAG는 순환/앞단원 역참조가 없지만 예문 속 모든 부수 문형의 선행 숙달은 별도 문제다. A10의 `대화할 시간` 등 일반 관형형, 교정 A18의 `신청할 때`처럼 공통 기초 C01/B01의 실제 수업 순서보다 앞서 나오는 조합은 교사/후속 통합 단계의 사전 리뷰/도움말 설계가 필요하다. 기존 단원 순서를 임의 변경하지 않았다.

Native iOS Debug/Release·SDK resolve·XCTest137정의/실행0, 실기기 음성/IME/중단·메모리/3~10분 실측, AdMob/StoreKit 거래는 **BLOCKED**, 독립 사람/사전 검수는 **NOT TESTED**. 이 단계에서 새 듣기·직접입력·문형 카드를 제작하거나 후속 통합을 시작하지 않았다.

## 실제 자동 검증 결과

최종 `sh Tools/verify.sh --portable` **346/346 PASS**(380.927초, 실패/오류/skip0, exit0), 추가 전용11/11 PASS(16.794초). 첫 후보345 PASS는 독립 성별 문맥3문항 교정 전 결과이므로 PRELIMINARY 로그로 분리하고 최종 후보를 전부 다시 검사했다. strict22→23는0errors/기존10warnings, DATA09 계약0errors/0warnings, DATA08 구조 감사0errors/기존5warnings다. 기존 homograph/발음 경고를 삭제하지 않았다.

검증한244개 코드·테스트·입력의 SHA를 다시 확인한 후 candidate만 반영했다. 실제 Production Source를 재빌드해 현재 DB와 byte/SHA까지 동일함을 확인했다. Content22 원본/DB, 과거 fixture·Batch 근거·런타임147개 파일도 baseline과 byte 보존을 확인했다. Source25테이블65,983행, DB31테이블, integrity ok/FK0, Grammar96노드/선행73간선 DAG 순환0이다. 실제 결과와 미실행 조건은 [RESULTS](DATA09_FINAL_RESULTS.json), [전체 로그](DATA09_FINAL_TEST_LOG.txt), [Production 재구성](DATA09_FINAL_RECONSTRUCTION.json), [현재 수량](DATA09_FINAL_COUNTS.json)에 기록했다. 문서만으로 미검증 native·사람 검수 gate를 통과시키지 않았다.
