# Hermes Skills

Hermes Agent에서 쓰는 독립 스킬 모음입니다. Claude Code 플러그인 마켓플레이스가 아니라, Desktop·CLI에서 공통으로 로드하는 Hermes 스킬 저장소입니다.

## 스킬

| 스킬 | 하는 일 |
| --- | --- |
| [`orca-collab`](./orca-collab/) | Orca CLI로 Claude 세션과 작업 트리를 만들거나 재사용하고, 필요할 때만 추적형 감독을 사용해 결과를 검증합니다. |
| [`interview-methodology`](./interview-methodology/) | 요구사항 인터뷰와 설계 스트레스 테스트를 Hermes의 질문 도구로 진행합니다. |
| [`dev-flow`](./dev-flow/) | 목표·이슈에서 구현 위임, 테스트, PR, 리뷰까지 이어 줍니다. |
| [`session-handoff`](./session-handoff/) | Hermes 대화의 결정·완료·실행 상태를 다음 세션에 전달합니다. |

## 설치

Hermes CLI가 있는 환경에서 원하는 것만 설치합니다. Desktop과 CLI가 같은 Hermes 프로필을 사용하면 같은 스킬을 읽습니다.

```bash
hermes skills inspect YoungjaeDev/hermes-skills/orca-collab
hermes skills install YoungjaeDev/hermes-skills/orca-collab
hermes skills install YoungjaeDev/hermes-skills/interview-methodology
hermes skills install YoungjaeDev/hermes-skills/dev-flow
hermes skills install YoungjaeDev/hermes-skills/session-handoff
hermes skills list --enabled-only
```

신규 대화에서 `/orca-collab`, `/interview-methodology`, `/dev-flow`, `/session-handoff`로 불러오거나 자연어로 요청할 수 있습니다. 한 번에 여러 스킬을 불러오는 **로컬 호출 별칭**이 필요하면 `hermes bundles create --skill ...`을 사용하세요. 번들은 이 저장소의 배포 단위가 아닙니다.

`orca-collab`을 실제로 사용하려면 [Orca](https://github.com/stablyai/orca) 앱과 CLI가 필요합니다. 이 스킬은 실행 중인 Orca의 `orca skills get orca-cli`·`orca skills get orchestration`을 읽어 설치 버전에 맞춥니다. Windows/macOS의 기본 명령은 `orca`; Linux에서 Orca 밖의 셸은 GNOME 스크린리더와 충돌하지 않도록 Orca 가이드에 따라 `orca-ide`를 사용할 수 있습니다. Claude Code 로그인과 작업공간 신뢰 확인은 별도로 필요할 수 있습니다.

## 원칙

- 한 가지 거대한 자동화 레시피보다 **상황에 맞는 선택**: 단순 전달은 Orca 터미널, 완료 감독이 필요한 일은 Orca의 추적형 절차.
- 여러 작성자가 동시에 작업하면 서로 다른 작업 트리와 파일 소유권을 부여합니다.
- 작업 범위 안에서 로컬 수정·커밋·푸시·PR 생성은 허용할 수 있으나, 머지·DB 변경·배포는 명시적 승인 대상입니다.
- Orca가 자신의 Run·Task·Dispatch 상태의 정본입니다. 별도 체크포인트는 생기더라도 복구용 색인일 뿐 작업 성공의 증거가 아닙니다.
- 공개 스킬에 사설 프로젝트의 경로, 토큰, 작업 내용이나 실행 상태를 넣지 않습니다.

## 개발 및 검증

스킬은 루트의 `<name>/SKILL.md`에 작성하고 필요하면 같은 폴더의 `references/`, `scripts/`를 추가합니다. 저작 규칙은 [Hermes 공식 스킬 가이드](https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills)와 이 저장소의 [`docs/SPEC.md`](./docs/SPEC.md)를 따릅니다.

```bash
python tests/test_skills.py
```

실제 실행 검증은 읽기 전용 작업부터 시작하고, Orca 터미널·Run·작업 트리 동작을 각각 확인합니다. 스킬 설치만으로 Claude 계정이나 Orca 권한이 자동 설정되지는 않습니다.

## 출처와 라이선스

`interview-methodology`, `dev-flow`, `session-handoff`는 [YoungjaeDev/my-claude-plugins](https://github.com/YoungjaeDev/my-claude-plugins)의 동명·관련 절차에서 아이디어를 가져와 Hermes 도구와 호출 방식에 맞춰 다시 작성합니다. `orca-collab`은 Orca CLI의 설치 버전 가이드를 실행 시 참고합니다. 이 저장소의 저작물은 [MIT](./LICENSE) 라이선스입니다.
