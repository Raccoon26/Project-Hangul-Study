# DATA-10-7 Mac Native Full Regression

2026-10-23 JST 재개. 상태: **진행 중, 최종 전체 검사 대기**. 이 문서는 실행 근거와 남은 gate를 구분하며 DATA10-8/11을 시작하지 않는다.

## 환경·보존

- 기존 Mac clone, `codex/data10-7-native-regression`, 시작 main/origin/main `59d3bc7636c2b22ce7a0e21899fa1deeb2bbfedb` (PR #23). 시작 미커밋 변경0. 재개 시 변경은 이 단계에서 작성한 코드·검사뿐이며 삭제/stash/reset/force push0.
- origin `https://github.com/Raccoon26/Project-Hangul-Study.git`, Raccoon26 인증/ADMIN/default main. rulesets0/Actions workflows0. CI 없음과 CI PASS는 다르다.
- macOS27 arm64 / Xcode27.1(27A9275), iOS26.0.1 Simulator. 단일 Xcode build jobs, UI 실행은 한 Simulator씩 순차 실행한다. 앱 iOS16 deployment 유지, XCTest target만 iOS17(현재 XCTest SDK 요구)에 맞춘다.
- Content29/Schema4/reader7/UserProgress10 및 모든 Production/fixture 114개 파일의 SHA-256 보존. Source/DB/Stable ID/revision/learning_order/기존 membership 변경0. 새 optional session JSON 필드는 과거 snapshot을 그대로 decode하며 UserProgress schema/migration/사용자 DB를 재작성하지 않는다.
- 시스템 Python3.11.6/SQLite3.44.0 ENABLE_STAT4와 exact writer SQLite3.53.1을 구분한다. `setup_exact_writer.py`로 만든 외부 `/tmp` writer에서 임시 Content29 rebuild, frozen28 strict Validator 오류0/기존 경고10, 번들 전체 byte/SHA 일치. SHA `228d5572391d4c56509f83c57415c9b76b69c82ce2e7e48ebea82af97630b4af`.

## 발견 → 수정 → 검증

| 문제 | 원인·수정 | 회귀 근거 |
| --- | --- | --- |
| P1 되다/뵈다 생성 오류 | Hangul medial index ㅚ→ㅚ 및 ㅙ→ㅚ 오매핑을 ㅚ→ㅙ/ㅙ 유지로 교정. 꿰다의 ㅞ는 그대로 보존 | 기존 ReleaseAudit + 새 NativeRegression의 85개 published -되다 ×3 Dictionary/engine 및 전체1,227 입력 rubric 조회 |
| P2 ㅎ형 사전 현재/과거 누락 | published 어떻다/빨갛다/파랗다/노랗다 네 lexical base만 검수하여 지원. authored override 우선, 미검수 ㅎ형은 기존 안전 오류 유지 | 네 항목 현재/과거/미래 실제 Dictionary 조회 및 unknown/override 검사 |
| P1 구매 cache 실패를 미구매로 취급 | Keychain missing과 OSStatus/decode failure 분리. 오류 시 광고 fail closed, verified StoreKit 권한 유지, 저장 실패 메시지 | 실제 signed Keychain CRUD/cold read/delete + 로컬 StoreKit 구매/복원 + 실패 주입. unsigned -34018은 진단 기록이며 성공으로 계산하지 않음 |
| P2 받아쓰기·활용 미제출 초안 유실 | optional draft/sequence, 매 입력의 actor transaction 저장, 같은 문항·turn/단조 sequence로 늦은 응답 방지. 판정/SRS/event 생성과 분리 | cold repository/legacy JSON/retry/late writes/no grade·event·SRS + 실제 UI 종료/재개/채점 |
| 오디오 observer Swift6 수명 경고 | immutable observer ownership wrapper가 deinit에서 token 해제. actor deinit에서 non-Sendable 배열 접근 제거 | backend weak release 검사 + 기존 중복 재생/중단/late callback 회귀 |
| P2 학습 진입이 긴 레슨 목록 아래 묻힘 | 기존 학습 모듈 Section을 코스 목록 앞에 배치, 기존 학습순서/ID 불변 | 初中級 듣기 진입 hittable/Content29 실제5문항 수료·Resume·사전 연결 |
| P2 홈 안내문 대비 부족 | 기본 안내문의 secondary style 대비 실패를 primary로 교정 | 필터/무시 없는 `performAccessibilityAudit()` 재실행 중 |
| 오래된 native cohort/기대값 실패 | DATA06 원래80개를 고정 registry로 검사하고 후속 문항은 별도 검증. DATA08 원래1,821개와 현재 전체 pagination을 구분. 발음 테스트는 원래 course UUID로 고정. 꿰다 past의 잘못된 기대값을 규범에 맞게 뀄어요로 교정 | 기존 테스트 삭제·skip·assertion 비활성화0. native 전체 재실행 |

규범 참고(국립국어원 한국어기초사전): [되다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=89858), [뵈다](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=65573), [꿰다](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=37786), [파랗다](https://krdict.korean.go.kr/m/eng/searchResultView?ParaWordNo=71306&nation=eng), [노랗다](https://krdict.korean.go.kr/eng/dicSearch/wordLinkViewPopup?ParaWordNo=40101&nation=eng&nationCode=6). AI와 공개 규범의 대조이며 독립 원어민 승인/모든 활용 구현으로 표시하지 않는다.

## 실행 기록·한계

- 수정 전 native148: 142 PASS/6 FAIL/skip0. 오래된 cohort와 실제 활용 오류, unsigned Keychain 실패를 구분했다.
- 첫 전체 `Tools/verify.sh`: portable418 PASS/0 fail/skip0(984.232초), native155 PASS/0 fail, UI11 중7 PASS/4 FAIL. 전체 명령 exit65이며 성공으로 표시하지 않는다. 실제 XCTest는 합166/162 PASS/4 FAIL.
- UI 실패 중 복원된 입력란의 caret/선택, 키보드가 가린 검색 결과, navigation back button 오선택은 잘못된 테스트 조작을 고쳐 동일 검증을 다시 실행한다. 잘못 입력된 답을 앱이 오답 처리한 것은 채점 버그로 집계하지 않는다. 홈 대비 감사 실패는 실제 앱을 수정했다.
- 재현 로그·xcresult는 `/tmp/hangul-data10-7/`에 보존. 최종 봉인 결과와 재현 명령은 검사 종료 후 별도 원장으로 갱신한다.
- 실제 한국어 TTS 재생 완료/정답 공개/정상·느린 속도 UI를 검증하되 TTS를 녹음이나 사람이 검청한 음질로 표현하지 않는다. 검증 녹음0, 독립 사람/교사 및 기존163후보36미해결·신규12계열27원문 언어 gate 유지.
- 사용자 확인(2026-10-22): 케이블이 없어 현재 iPhone 연결 불가, 내일부터 가능. 자동 후속 작업/예약은 만들지 않았다. 실제 iPhone 연결0: 물리 기기의 VoiceOver 발화/통화·이어폰 중단/한 손·배터리·비행기모드/서명 설치는 BLOCKED. 실제 App Store Connect/AdMob 계정과 Production ID 미제공: production 거래/광고 gate BLOCKED. Release 광고 미설정 시 비활성 정책 보존.
- Portable socket 금지 로컬 조회 및 native SQLite 학습·SRS·저장 검증은 물리 기기 비행기모드 실행과 구분한다. 짧은 세션 광고 차단·권한·실패 nonblocking의 policy/로컬 StoreKit 검증을 production 광고 수신으로 표현하지 않는다.
- Release B—Conditional 유지. 최종 검증 전 DATA-10-7 완료/전체 PASS/main 병합을 선언하지 않는다.

## 10월23일 재개 근거

- main/origin/main과 시작 SHA 일치, 같은 작업 브랜치/미커밋 수정 보존. 실제 iPhone 미연결 재확인.
- SmallProduction21: SE3/iOS26.0.1/Dark/AXXXL, UI06 1/1 PASS(163.370초). 걷다3문항의 초안 cold resume/편집/정답/완료 실제 실행. UI 편집 메뉴는 UIKit 표시에 따라 MenuItem 또는 Button으로 찾아 조작하고 최종 입력 문자열을 정확히 확인한다.
- SmallProduction18 build 실패/실행0은 외부 SPM binary artifact Info.plist 유실. 기존 캐시 보존 후 새 Packages20 경로에서 고정13.11.0/3.1.0 재다운로드, 실제 Info.plist 및 후속 build/test로 복구 확인. 원본·lockfile 불변.
- 임시 Production 제출 NSLog 제거. UI 비동기 setup/teardown으로 MainActor 경고 해결. 키보드 전환 invalid frame warning은 조사 중. 전체 UI14 포함 최신 전체 결과는 아직 대기.

## Checkpoint 원장 (완료 아님)

NormalAudits22: 2 UI 실행/2 실패/skip0. Numeric row/긴 문구의 큰 글씨 배치 수정 후 NormalAudits25는 SPM artifact 누락으로 build 실패/실행0, 새 ignored Packages26에서 현재 재검사 중이다. 모든 접근성 이슈를 계속 실패로 기록한다. 최소 SwiftUI 재현도 유사한 실패가 있지만 제품 문제 전체를 SDK 탓으로 확정하지 않는다.

Mac 공간이 약200MB까지 감소했다. 사용자에게 프로젝트 외 파일 정리를 요청했다. 작업의 중복 export만 원본 xcresult와 manifest를 남긴 뒤 정리했으며, 종료된 작업 소유 QA device는 학습 기록을 별도 SHA 일치 복사해 보존했다. 사용자 기기/기존 Production 삭제0. [실행 요약](DATA10_NATIVE_RUNS.json), [원시 로그 archive](DATA10_NATIVE_CHECKPOINT_LOGS.tar.gz). 최신 전체 검사 미완료·접근성 실패가 남아 있으므로 main 병합 금지다.
