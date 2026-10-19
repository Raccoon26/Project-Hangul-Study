# DATA-01 검증 기록 — 2026-10-01

## 실제 실행

- 기존 Importer/Validator `--production --validate-only --previous Tests/Fixtures/content-v4-production.sqlite`: 오류 0, 경고 8.
- 동일 source에서 `Resources/content.sqlite` 생성: schema 3 / content 5 / reader 4 / is_fixture 0.
- `python3 -m unittest discover -s Tools/ContentBuilder -v`: **92개 통과, 13.487초**. 최종 문구 교정 후 실행한 출력은 `TEST_RESULTS_DATA01.txt`.
- 신규 12개 테스트: 수/버전/무결성, 기존 225항목 보존, 각 의미 예문 연결, UUID 및 재정렬 안정성, 실제 Swift keyset pagination/intro 조회, 품사, 한국어·일본어·보조 의미 검색, 동형어, 활용 및 추측 메타데이터 금지, notes/tags/중복 문장, 잘못된 실제 배치 입력 거부, 번들 DB/source 일치.
- 기존 80개 회귀: Importer 실패 시 원자성, 사용자 진도 SQL·재개·완료·통계, 콘텐츠/사용자 데이터 분리, 한글·발음·퀴즈·음성 정책, 15,000 어휘/30,000 예문 synthetic 생성·조회 등.
- 경고 8개는 기존 짧은 발음 예시 5개와 신규 차/일/쓰다 동형어 그룹 3개. `DATA01_REVIEW.md`에 판정 근거를 보존했습니다.
- Swift/UI/Audio/Progress·스키마·Importer 등 42개 보호 파일이 DEV-04와 byte-identical임을 비교했습니다.
- 프로젝트의 실제 DB 복사 shell script를 Debug/Release 환경 변수로 실행했고, 복사된 DB가 원본과 같으며 226어휘/content 5임을 확인했습니다.
- Info.plist 및 scheme/workspace XML 파싱. 결과는 `STATIC_CHECKS_DATA01.txt`.

## 실행하지 않은 것

이 환경에는 Swift와 Xcode가 없습니다. **네이티브 빌드·타입 검사·링크, XCTest 29개, 시뮬레이터/실기기 UI, 실제 오디오 출력은 미실행**입니다. 이번 DATA 작업은 Swift 코드를 수정하지 않았으며 구문 파서를 새로 실행했다고 주장하지 않습니다. DEV-04의 검사 기록은 `VALIDATION_DEV04.md`와 `STATIC_CHECKS_DEV04.txt`에 별도로 보존합니다.

Python이 같은 SQL을 실행한 결과는 앱 프로세스에서 Swift 저장소를 실행한 결과가 아닙니다. 음성 policy 회귀 통과는 실제 ko-KR 발음 품질 확인을 의미하지 않습니다.

## Mac에서 수행할 절차

```sh
sh Tools/verify.sh
TEST_DESTINATION='platform=iOS Simulator,id=YOUR_SIMULATOR_ID' sh Tools/verify.sh
```

1. Debug/Release 빌드 및 XCTest 실행.
2. `単語` 탭에서 첫 50개, さらに表示, 226개 전체 접근과 동형어의 서로 다른 의미 표시 확인.
3. 밥·시간·찾다 등의 단어 상세에서 예문 두 개, 북마크 저장·재실행 유지 확인. 현재 대표 의미 하나만 표시하며 전체 의미/학습 노트 UI는 아직입니다.
4. 기존 ハングル入門 / 発音・パッチム의 시작·정오답·완료·재개 회귀와 음성 가용/불가 상황 확인.
5. 이전 content 4에서 content 5로 앱을 교체했을 때 기존 진도/즐겨찾기가 남는지 확인. 진행 중 세션의 재시작 안내는 기존 정책입니다.
6. 작은 화면·최대 Dynamic Type·Light/Dark·VoiceOver로 새 한국어/일본어 문장이 잘리지 않는지 확인.

위 목록은 다음 환경에서 실행할 절차이며 이번에 실행한 UI test 결과가 아닙니다.
