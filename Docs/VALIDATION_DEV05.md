# DEV-05 검증 범위와 Mac 확인 절차

## 이 환경에서 실제 수행

Linux Python/SQLite 테스트 104개 통과. 기존 92개와 새 SQL 12개입니다. `TEST_RESULTS_DEV05.txt`는 실행 출력입니다. SQL 테스트는 Swift repository에 쓰인 SQL을 추출하여 실제 SQLite에서 실행합니다. JSON 저장 테스트는 opaque JSON의 보존을 확인하며 Swift Codable/엔진 실행을 흉내 내는 테스트가 아닙니다.

Production validator 오류 0 / 기존 경고 8. Source 및 bundled DB는 DATA-01과 바이트 동일합니다. Swift 구문 parser 38개 파일 오류 없음. 프로젝트 참조·리소스 연결·plist/XML·SQLite integrity를 확인했습니다. Swift type-check/build/XCTest/UI/실제 음성은 실행하지 않았습니다.

## Mac 자동 검증 (미수행)

```sh
python3 Tools/generate_project.py
xcodebuild -showdestinations -project HangulStudy.xcodeproj -scheme HangulStudy
TEST_DESTINATION='platform=iOS Simulator,id=실제_SIMULATOR_ID' sh Tools/verify.sh
```

총 42개 native XCTest(신규 회독 13개 포함)를 실행합니다. 기존 음성 fallback/normal/slow/누락 녹음 11개 테스트도 유지했습니다. Debug/Release 둘 다 production DB와 v4 사용자 migration 리소스를 번들에 포함해야 합니다.

## 수동 확인 (미수행)

1. 새 설치에서 `学ぶ → 入門単語`에 실제 DB의 어휘 수가 표시되는지 확인합니다. 새 세트는 20개이며 ID 중복이 없어야 합니다.
2. 첫 카드에 큰 한국어와 품사만 표시되고 일본어 의미는 VoiceOver로도 노출되지 않는지 확인합니다. `意味を見る` 전에는 판정할 수 없어야 합니다.
3. 의미/예문/notes와 TTS normal/slow/stop을 확인합니다. 한국어 voice가 없는 상태에서도 어휘 회상은 계속 가능해야 합니다.
4. 첫 회독에서 8개만 `覚える`로 표시합니다. 회독 종료 → 8개만 → 다시 3개만 → 마지막 전부 known → 3周/20語 완료를 확인합니다. 모르는 단어가 같은 회독의 바로 다음 카드로 돌아오지 않아야 합니다.
5. 전부 known이면 1周 완료, 전부 learn이면 20개 그대로 다음 회독인지 확인합니다. 마지막 한 단어는 다음 회독 버튼을 눌러야 다시 보입니다.
6. 13번째 카드에서 의미 공개 전/후 각각 닫기 및 앱 강제 종료 후 재실행합니다. `続きから`가 동일 세트·회독·카드·공개 상태를 복원하고 노출을 중복 집계하지 않아야 합니다.
7. 빠른 중복 탭, 화면 닫기 직전 탭, background 이동을 확인합니다. 저장 중 버튼이 잠기고 재개 후 한 단어를 두 번 통과시키지 않아야 합니다.
8. 완료 후 다음 세트와 같은 세트 `もう一度見る`를 각각 확인합니다. 이전 완료 횟수/이력과 기존 한글/발음/즐겨찾기 기록이 남아야 합니다.
9. v3 사용자 DB가 있는 앱에서 업데이트하여 v4 migration/backup 및 한글/발음 세션 재개를 확인합니다. 별도 기기 복원/클라우드 보장은 아닙니다.
10. Light/Dark, 최대 접근성 글자 크기, VoiceOver, 작은 iPhone/iPad, Reduce Motion을 확인합니다. 긴 뜻/설명과 하단 버튼이 잘리지 않아야 합니다.
11. Content DB에 단어 추가/정렬 변경 후 기존 세트의 ID snapshot과 진행 위치가 유지되는지 확인합니다. 누락/비활성 단어는 기록을 지우지 않고 안내해야 합니다.

## 언어·음성 한계

한국어와 일본어 콘텐츠는 DATA-01 그대로입니다. 시스템 TTS의 발음·속도·음성 다운로드 환경은 실제 iPhone에서 들어봐야 합니다. 검증된 녹음이 필요한 개별 자모/비교 콘텐츠에 TTS를 대체 제공하지 않습니다.
