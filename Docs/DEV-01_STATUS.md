# PROJECT_STATUS — DEV-01

작성: 2026-09-30 (일본 시간). 사용자 지시: 45분 상한, 기반 구축만. 기존 프로젝트를 대체한 것이 아니라 새 프로젝트를 생성했습니다. 다음 단계 기능은 선행 구현하지 않았습니다.

## 이번에 구현한 것

1. 실제 `.xcodeproj`, 공유 Scheme, iOS app target, hosted XCTest target, Info.plist와 리소스 복사 단계
2. SwiftUI 일본어 4탭/NavigationStack, 단어 목록/상세/예문/북마크, 실제 저장 개수 표시
3. 시스템 색상/서체, indigo 포인트 하나, Light/Dark·Dynamic Type 기본 대응
4. 콘텐츠와 사용자 SQLite DB 분리; Debug/Release의 콘텐츠와 진도 파일도 분리
5. 어휘/다의어/예문/문법/자모·받침/발음/활용/음원/듣기/문제/TOPIK 분류/과정/레슨/태그/일본인 설명/관계 스키마
6. 모든 학습 엔티티의 영구 UUID, revision, tombstone, 콘텐츠 별칭 이력 구조
7. 콘텐츠 schema/content/min-reader 버전 검사, 사용자 DB 최초 v0→v1 migration과 미래 버전 거부
8. 사용자 회독/SRS/학습 이벤트/통계/즐겨찾기/레슨 진행 스키마
9. 이벤트 UUID 멱등성, 이벤트와 통계의 원자적 저장, 북마크 저장 API
10. actor 격리 저장소, 프로토콜, AppContainer 조립, 단어 keyset pagination
11. Content Builder: JSON→검증→SQLite 원자적 출력, 이전 배포 ID/버전 비교, FK/무결성/UUID/미디어 해시/alias cycle 검증
12. 개발용 단어 2개·뜻 2개·예문 1개·과정 1개·레슨 1개·자모 1개·일본인 설명 1개. 모두 개발용으로 표시하며 Release에는 포함하지 않음
13. Python 자동 테스트 18개, XCTest 테스트 8개 작성, Mac 검증 스크립트

## 주요 아키텍처 결정

- Core Data/SwiftData 대신 시스템 SQLite3를 사용합니다. 번들 DB 자동 생성과 큰 정규화 콘텐츠를 직접 다루고, 사용자 DB의 버전을 명시적으로 관리하기 위한 선택입니다. 외부 런타임 의존성은 없습니다.
- 콘텐츠는 read-only; 사용자 DB는 Application Support, WAL/FULL synchronous, 데이터 보호 사용. 오류 시 자동 삭제/초기화하지 않습니다.
- 데이터 ID를 단어 문자열·배열 순서·DB rowid에서 만들지 않습니다. 학습 기록은 현재 콘텐츠가 없더라도 보존합니다.
- SRS 알고리즘은 구현하지 않았고 인터페이스와 버전 가능한 저장 구조만 준비했습니다.
- 학습 이벤트는 추가 이력, 누적/일별 통계는 재생성 가능한 집계입니다. 현재 UI는 즐겨찾기만 변경하며 학습 횟수를 가짜로 증가시키지 않습니다.
- Release는 빈 실제 콘텐츠 패키지를 사용합니다. 개발용 데이터가 학습 상품의 실제 데이터로 섞이지 않습니다.

## 파일 구조

```text
HangulStudy/
  HangulStudy.xcodeproj/     프로젝트, workspace, 공유 Scheme
  App/                      @main 진입점
  Models/                   콘텐츠·학습 데이터 모델
  Services/                 AppContainer, 경로·의존성 조립
  Repositories/             프로토콜, 콘텐츠/사용자 SQLite actor
  Views/                    탭, 과정, 단어, 기록, 설정
  ViewModels/               main actor UI 상태
  Persistence/              SQLite 바인딩/트랜잭션, 사용자 migration
  LearningEngine/           ReviewScheduling 계약만
  Content/                  v1 SQL, fixture/빈 production JSON, 패키지 gate
  Utilities/                시간대별 학습일 키
  Resources/                DB 2개, 사용자 SQL, Info.plist, 일본어 strings
  Tests/                    XCTest 8개
  Tools/ContentBuilder/     builder, Python 테스트, 입력 계약
  Tools/generate_project.py 프로젝트 재생성
  Tools/verify.sh            macOS 빌드/테스트
  Docs/                     아키텍처·검증 기록
  README.md                 한국어 실행 안내
  PROJECT_STATUS.md         이 문서
```

## DB 구조

정확한 정의는 `Content/content-schema-v1.sql`, `Resources/user-schema-v1.sql`에 있습니다. 전체 테이블별 역할은 `Docs/ARCHITECTURE.md`에 기록했습니다.

- 콘텐츠: `content_metadata`, `content_items` 중심. 상세 엔티티와 관계 테이블, 영구 ID, 내부 foreign key, 탐색 인덱스
- 사용자: `user_metadata`, `item_progress`, `srs_state`, `favorites`, `study_events`, `learning_passes`, `pass_items`, `lesson_progress`, `daily_statistics`
- 사용자 DB에서 콘텐츠 DB로 cascade delete/FK를 만들지 않습니다.
- 현재 사용자 스키마와 콘텐츠 스키마는 각각 1입니다. fixture와 빈 production의 content_version도 각각 1이며 dataset은 다릅니다.

## 아직 구현하지 않은 것

- 실제 12,000~15,000개 이상 어휘, 20,000~30,000개 예문, 350~500개 문법 및 모든 대규모 콘텐츠
- 전체 자모/받침/발음·활용 교육 내용, 실제 음원·듣기 1,000문제·작문 2,000문제·TOPIK 1,000문제
- 학습 세션/정오답 제출 UI, 코스 진행·회독 기록 갱신 서비스, SRS 상태 갱신 서비스/전체 알고리즘
- 듣기 재생/녹음/발음 평가, 작문 채점, TOPIK 채점/모의시험
- 전문검색/FTS, 즐겨찾기 전용 목록, 학습 알림, 목표/달력/상세 통계 화면
- 콘텐츠 원격 다운로드·서명 검증·런타임 활성 패키지 교체
- 사용자 v1 이후 migration, migration 전 SQLite backup 스냅샷, 복구 UI, 내보내기/가져오기/클라우드 동기화
- alias를 이용한 학습 이력 병합 정책 및 자동 변환
- 언어학적 콘텐츠 검수, 정답 스키마별 검증, 관계 테이블 변경에 대한 revision 자동 비교
- 음원 파일 패키징/다운로더, 저작권 검토 자동화
- 앱 아이콘/최종 브랜드명/스토어 메타데이터/배포 서명/출시 심사 준비
- 광고/IAP/로그인/서버/분석 SDK: 요청에 따라 모두 제외

## 검증 결과

- Python 콘텐츠 빌더 및 실제 Swift 내 SQL 검증 **18개 통과**
- Swift 파일 19개(앱 18 + 테스트 1)를 구문 파서로 확인: syntax error 없음
- `.pbxproj` 독립 파서 로딩, 앱/테스트 target, 공유 scheme/workspace XML, plist 확인
- 모든 Swift 파일의 target 소스 포함과 파일 참조 존재 확인
- 실제 프로젝트 DB 복사 shell phase 실행: Debug fixture=1, Release fixture=0 확인
- DB integrity/FK 확인, 잘못된 입력/ID 삭제/버전 하락 거부, 실패 시 기존 DB 보존, 실제 SQL transaction rollback 확인
- **Xcode/Swift 컴파일러가 없는 Linux 환경이므로 컴파일·링크·XCTest 8개 실행·iOS 화면 확인은 미실행**. 빌드 통과라고 주장하지 않습니다.

## 알려진 문제와 한계

1. 네이티브 빌드 및 실기기/시뮬레이터 확인이 최우선 잔여 검증입니다.
2. Release는 실제 콘텐츠가 없어 빈 상태를 표시합니다. 이는 의도된 DEV-01 상태이며 출시할 수 있는 교육 상품이 아닙니다.
3. 문제 JSON은 문법적 JSON 유효성만 검사합니다. 교육적 정확성·유형별 정답 구조는 검증하지 않습니다.
4. 상세 엔티티 행의 revision 변경은 검사하지만 연결 테이블 변경까지 자동 감지하지는 않습니다. 관계 수정 시 관련 revision을 수동 증가해야 합니다.
5. alias는 저장/순환 검사만 하며 사용자 이력은 자동 병합하지 않습니다.
6. 단어는 페이지 조회, 예문은 단어별 최대 100개, 과정/레슨 메타데이터는 일괄 조회입니다. 대규모 레슨 수요가 생기면 조회 API만 페이지화합니다.
7. app icon은 미포함이며 Xcode의 아이콘 경고/출시 전 설정이 남을 수 있습니다.
8. 영속 저장은 정상 재실행/업데이트를 위한 로컬 DB입니다. 앱 삭제·기기 손실 보호용 별도 백업 기능은 아직 없습니다.
9. 프로젝트 생성기를 재실행하면 수동 Xcode 설정을 덮어씁니다. README 주의사항을 확인하세요.

## TODO 기록

소스에 `TODO`/`FIXME` 마커, `fatalError`, `try!`, `as!`는 없습니다. 이후 작업은 위의 미구현 항목과 알려진 한계에 모두 명시했습니다. 미구현 기능을 동작하는 것처럼 보이는 버튼이나 가짜 결과로 대신하지 않았습니다. `ReviewScheduling`는 명시적인 미래 계약입니다.

## DEV-02 인계

1. 이 ZIP의 전체 프로젝트에서 이어서 작업합니다. DEV-01 저장소/스키마를 임시 JSON 배열이나 UserDefaults 기반 코드로 대체하지 않습니다.
2. 먼저 Mac에서 Debug/Release build와 `⌘U`를 실행합니다. 오류가 있으면 재현 결과를 남기고 우선 수정합니다. OS UI의 Light/Dark·최대 Dynamic Type·VoiceOver도 확인합니다.
3. DEV-02의 실제 범위는 다음 사용자 지시로 확정합니다. 대규모 데이터·SRS·과금을 임의로 한 번에 추가하지 않습니다.
4. 교육 단위를 추가할 때 `content_items` 영구 UUID를 먼저 정의하고, fixture namespace와 production dataset을 혼용하지 않습니다.
5. 학습 완료를 연결할 때 `StudyEvent.id`를 재시도 사이에 유지하고 `record()`를 사용합니다. UI에서 통계를 별도로 증가시키지 않습니다.
6. SRS 알고리즘/스킬/문제 유형을 정할 때 버전을 명시하고 실제 채점·갱신을 원자적으로 묶는 저장 API를 확장합니다. 지금은 SRS가 동작하지 않습니다.
7. 콘텐츠 업데이트는 직전 배포 DB를 `--previous`로 검증합니다. 기존 ID를 지우거나 재활용하지 않습니다.
8. 사용자 migration 추가 시 backup API와 rollback, 실제 과거 DB fixture를 이용한 테스트를 먼저 준비합니다. WAL DB 본체만 복사하거나 파괴적으로 초기화하지 않습니다.
