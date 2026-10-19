# DEV-04 검증 기록 — 2026-09-30 UTC

## 수행한 검증

- `python3 -m unittest discover -s Tools/ContentBuilder -v`: **80개 통과**, 10.726초. 원본 출력 `TEST_RESULTS_DEV04.txt`.
- 기존 65개 importer/validator/관계/ID/실패 원자성/진도 SQL/한글 과정/15,000 어휘·30,000 예문 synthetic 회귀를 포함합니다.
- 새 발음 15개: schema/content/reader 버전, 이전 130개 항목의 ID·본문·관계 fingerprint 보존, 14레슨/36페이지/31문제 순서·대상·범위, 실제 Swift repository SQL, 철자→발음, TTS 정책, 자모·비교 녹음 전용, 듣기 문항 철자 비노출, 잘못된 입력 거부, 복수 발음 구조를 검사했습니다.
- DEV-03 production DB를 --previous로 지정한 Importer: **오류 0 / 경고 5**. 꽃/花, 밭/畑, 밥의 짧은 단어 예시 경고이며 의도된 단어를 삭제하거나 validation을 우회하지 않았습니다. `PRONUNCIATION_CONTENT_REPORT.json` 참조.
- tree-sitter-swift: 29 Swift 파일(앱 26/테스트 3) 구문 오류 노드 0.
- pbxproj parser, 생성기 출력 재현, 참조 파일 존재, Info.plist/scheme/workspace 파싱 확인.
- Xcode 생성기의 실제 DB 복사 shell script 실행: Debug/Release 모두 schema 3/content 4/is_fixture 0.
- 요약: `STATIC_CHECKS_DEV04.txt`. 과거 benchmark 수치는 `PERFORMANCE.json`에 보존했으며 새 iPhone 실측값으로 표현하지 않습니다.

## 미수행 및 한계

Linux에 Swift/Xcode가 없어 **Swift 타입 검사·컴파일·링크, Debug/Release iOS 빌드, XCTest, 시뮬레이터/실기기 화면, 실제 오디오 출력은 미실행**입니다. Python에서 실제 SQL을 검증한 것은 Swift actor/ViewModel 실행과 다릅니다. 구문 검사는 SwiftUI/AVFoundation API와 타입 검사를 대신하지 않습니다.

XCTest는 총 **29개**(기존 18 + 신규 11)를 준비했습니다. 새 테스트는 주입형 fake backend의 음성 없음/실패/중단/normal·slow/늦은 callback, 녹음 누락·경로·checksum, 실제 ko-KR voice 가용성 조회 안전성, 발음 repository/순서/퀴즈, SQLite 재개방 및 ViewModel 듣기 제출 조건을 대상으로 합니다. 이 결과를 통과했다고 주장하지 않습니다. Fake backend는 실제 소리 품질을 검증하지 않습니다.

## Mac에서 수행할 확인

```sh
sh Tools/verify.sh
TEST_DESTINATION='platform=iOS Simulator,id=YOUR_SIMULATOR_ID' sh Tools/verify.sh
```

1. Debug/Release 빌드와 XCTest를 실행합니다. 실제 설치된 simulator ID를 사용합니다.
2. 새 설치 → 学ぶ → 発音・パッチム → 첫 레슨 → 정답·오답 → 완료 → 다음 레슨 → 앱 종료/재실행 후 진행을 확인합니다. 기존 ハングル入門 12레슨도 회귀 확인합니다.
3. 받침 조합, 7대표음, 겹받침, 6종 발음 변화, 비교 페이지, 단어 듣기, 종합 확인을 확인합니다. 원래 철자가 보조 발음보다 크게 표시되는지 봅니다.
4. ko-KR 음성 보유/미보유 기기에서 normal/slow/stop, 연속 재생, 페이지 이동, 닫기, 앱 비활성화, 전화 중단, 이어폰 분리를 확인합니다. 다른 언어 voice로 대체하지 않아야 합니다.
5. 듣기 문항에서 재생 전/재생 중에는 제출 불가, 성공 완료 뒤에는 제출 가능해야 합니다. 정지·실패는 성공으로 세지 않습니다. 이미 저장한 피드백은 재생 없이 이어갑니다.
6. 녹음이 없는 개별 자모/최소대립 비교에서 TTS가 실행되지 않아야 합니다. 실제 녹음 추가 후 파일 누락·해시 불일치·손상 파일의 안내를 확인합니다.
7. 원어민이 한국어 단어/문장 실제 음성을 듣고 발음 변화와 slow 자연스러움을 검수합니다. OS/voice 종류에 따라 음질이 달라질 수 있습니다.
8. 설명/미응답/정오답 피드백/완료 직후 종료해 재개 위치·선택지·통계의 중복 없는 보존을 확인합니다. 콘텐츠 v3→v4 업데이트 시 진행 중 세션은 기존 정책대로 재시작 안내가 나오고 이전 기록은 남아야 합니다.
9. 작은 iPhone, 가로 방향, Light/Dark, 최대 Dynamic Type, VoiceOver, Reduce Motion에서 레이아웃·포커스·버튼/피드백 탐색을 확인합니다.
10. 저장 실패/용량 부족 시 학습 위치가 무단 진행하지 않고 재시도 가능한지 확인합니다.

이 목록은 다음 환경에서 수행할 절차이며 이번 작업에서 실행한 UI/오디오 테스트 결과가 아닙니다.
