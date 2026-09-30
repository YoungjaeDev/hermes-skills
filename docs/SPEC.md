# Hermes Skills v0.1 — 합의된 범위

## 목적

사용자는 Hermes Desktop 또는 CLI에서 같은 스킬을 호출해 Orca-managed Claude Code에 작업을 맡기고 결과를 회수·검증한다. 여러 Claude 세션/작업 트리도 필요할 때 다루되, 모든 요청을 무거운 작업 상태 머신에 넣지 않는다. 공개 GitHub 저장소는 배포 원본이고, 사용자별 실행 상태나 비공개 프로젝트 데이터는 보관하지 않는다.

## 제공 범위

1. `orca-collab`: 설치된 Orca CLI 가이드에서 명령을 읽는다. 명시적 대상 선택, 단일/여러 Claude 세션, 간단한 terminal send/read/wait와 추적형 Run/Task/worker-start의 선택, 결과 검증, 불확실한 재시도·중단·복구를 다룬다. Desktop과 CLI의 대화 세션이 자동으로 동일하다고 주장하지 않는다.
2. `interview-methodology`: 기존 Claude 플러그인의 breadth/depth/grill 개념을 Hermes `clarify`와 사실 확인 절차로 개작한다. 명확한 소규모 요청에는 불필요한 인터뷰를 강제하지 않는다.
3. `dev-flow`: 목표·이슈 → 범위 합의 → Orca/Claude 위임 → 검증 → PR/리뷰. 기존 Hermes GitHub 스킬과 도구를 재사용한다. 머지, DB 변경, 배포는 별도 승인을 요구한다.
4. `session-handoff`: 다음 Hermes 세션을 위한 대화 요약을 채팅에 출력한다. Orca 작업의 실제 조회·재개는 `orca-collab` 책임이다.

## 배포 경계

- 공개 MIT 저장소 `YoungjaeDev/hermes-skills`; 각 스킬을 `hermes skills install YoungjaeDev/hermes-skills/<skill>`로 개별 설치.
- Claude Code 플러그인, Codex 플러그인, Hermes Desktop UI 플러그인, Python 실행 플러그인은 v0.1에 포함하지 않는다.
- `skill-forge`를 배포 항목으로 이식하지 않지만, Hermes 공식 스킬 저작 가이드와 기존 skill-forge의 저작·감사 원칙을 적용한다.
- 원격 상태 변경은 작업 카드의 명시된 범위 안에서만 수행한다. 로컬 커밋·푸시·PR 생성은 허용된 개발 작업에서 가능하다. 머지·DB 변경·배포는 사용자 확인을 요구한다.
- Orca Run·Task·Dispatch가 정본이다. 앱 밖 Hermes의 Orca coordinator binding은 아직 라이브 검증되지 않았으므로, 추적형 실행이 실제로 성립하는지 확인 전에는 단순 터미널 감독을 추적형 Run이라 표현하지 않는다.

## 수용 기준

- 네 개의 SKILL.md가 Hermes가 읽을 수 있는 frontmatter와 실질적 절차·검증 단계를 가진다.
- README의 네 설치 식별자와 실제 디렉터리가 일치하며, 지원 파일 참조가 끊기지 않는다.
- 로컬 정적 검증과 Hermes `skills inspect`·설치 후 목록 확인을 통과한다.
- Orca 연동은 실제 터미널 목록·전달·대기·읽기를 사용한 읽기 전용 테스트를 통과해야 하며, 원격 배포나 DB 쓰기로 테스트하지 않는다.
- 여러 세션과 추적형 Run의 재개는 Orca CLI의 현재 계약을 실제로 시험한 범위까지만 ‘검증됨’으로 보고한다.

## 다음 버전 후보 (미확정)

Orca 재시작과 Hermes 대화/표면 전환을 넘는 자동 재개, 영구 체크포인트, Orca 이벤트 기반 플러그인, 특정 프로젝트별 승인 정책은 실제 결핍이 확인될 때 별도 설계한다. 상태 파일을 Orca의 정본과 경쟁시키지 않는다.
