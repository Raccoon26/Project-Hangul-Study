# DEV-14 Requirements Coverage Audit

2026-10-05. 판정은 **코드/DB 존재 및 portable 검증** 기준. 모든 행의 iOS UI 실행 상태는 미검증이다. 전체 과거 요구의 100% 완료 인증이 아니다.

| 영역 | 근거 | 상태/제한 |
| --- | --- | --- |
| Content/User 분리·versions·stable ID | AppContainer, SQLiteContentRepository, UserDatabaseMigration, ContentBuilder | 구현. production byte 보존/SQL migration 검사 |
| 대규모 importer/validator | build_content.py, benchmark.py | 15k/30k 검증, 오류0. 실제 iPhone memory/launch 미검증 |
| 한글 | Content.production hangul55, lesson engine | 현대 자모40 및 조합 포함; authored DB 검사 |
| 받침/발음 | pronunciation36, Audio models | 규칙/비교 lesson. 검증 녹음0, 개별 자모 TTS 금지 |
| 어휘·예문·notes | VocabularyCard/SQLiteVocabularyContent | production926 직접조회, 공개 후 판정 |
| 회독·set·resume | VocabularyPass/SQLiteVocabularyProgress | snapshot IDs, 모르는 항목만 다음회독, revision guard |
| SRS·dates·backlog | StepReviewScheduler/SQLiteReview | calendar_steps, 다중 skill, due index, bounded session; 날짜 SQL 검사 |
| 문법·비교·quiz·회독 | GrammarLearning/SQLiteGrammarProgress | production42, question/relation, SRS/Continue timestamp 수정 |
| 활용·Direct Input | ConjugationEngine/SQLiteProduction | 9form 기반+override, 전체 언어 예외/자유작문 미완성; ㅚ 수정 |
| Listening/Dictation | SQLiteListening/ListeningView | 111개4유형, retry/score 분리/hidden answer 소스검사 |
| Curriculum/Placement/Skip | SQLiteCurriculum/Curriculum views | 전체level 틀,8문항간이진단. 상위실제콘텐츠/정밀진단 부족 |
| Search/details/Favorites/difficult/recent | SQLiteLookup/SQLiteSavedContent | bounded SQL, lookup와 학습판정 분리 |
| Statistics | SQLiteStatistics/RecordsView | 실제events 기반, retry정확도수정. 총학습시간 허위추정 없음 |
| Maintenance/short | Maintenance/Review repositories | 기존 due/practice재사용; adaptive종합순환은 제한적 |
| Settings/Notifications | LearningPreferences/notification service | 로컬설정, 명시적 opt-in. 실제 권한/시간변경 기기검증 필요 |
| Ads | AdService/MonetizationConfiguration | Vocabulary완료 단일위치, micro/resume금지, cap, 실패nonblocking |
| StoreKit2 | PurchaseService/RemoveAdsView | verified entitlement/cache/update/restore, displayPrice. 실제거래 미검증 |
| Offline/resume | local SQLite/transactions | process-exit SQL 실험. iOS lifecycle/기기audio는 미검증 |
| A11y/design | SwiftUI views | 시스템스타일/labels/44pt. 실제 VoiceOver/최대DynamicType gate |
| Release packaging/privacy | Config/Info.plist/privacy manifest/check_monetization | Release IDs없으면off. signed archive/SDK manifest/ASC 확인필요 |

## P0/P1/P2

- P0 재현: 이번 실행 범위에서 남은 confirmed P0 없음. native 실행 부재를 안전 확인으로 해석하지 않는다.
- P1/Major: retired active review 복구, 상급 curriculum/전체 활용/placement 범위, native QA gate.
- P2/Minor: legacy retry 통계, lifetime 집계 비용, 기기 접근성 polish.

## Integration / 실제 검증과 미검증

Python 전체 결과 및 test_dev14_audit.py는 SQL/fixture/production source/정적계약 검사다. 앱 버튼을 누른 UI 테스트가 아니다. 실제 SQLite child process 종료 테스트는 commit된4/20답변 보존과 미commit완료 rollback을 확인한다. 실제 iPhone kill/background/알림/키보드/오디오/광고/구매 상호작용은 RELEASE_CHECKLIST로 이관.

## 종료 전 감사

새로운 dummy content, TODO 화면, no-op 구매버튼, 새로운 별도 progress DB는 추가하지 않았다. Production ID를 추측하지 않았다. 기존 콘텐츠 source/DB는 이전ZIP과 동일하다. 오류를 숨기려고 테스트/validator를 비활성화하지 않았다. 미검증 빌드나 실기기 작동을 완료로 표시하지 않았다.
