---
name: session-handoff
description: Hand off a Hermes chat session with verified state.
version: 0.1.0
author: YoungjaeDev, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [session, handoff, continuity]
    related_skills: []
---

# Session Handoff

Make a compact **chat-only** context handoff for the next Hermes agent. It records what this conversation established, not a retrospective, filesystem audit, or attempt to resume work. Works in Hermes Desktop and CLI; do not assume either surface exposes a particular tool.

## When to Use

- The user asks for a session handoff, wrap-up before clearing context, 세션 정리, 핸드오프, or 인수인계.
- Do not use this to transfer a live session to another platform. Hermes CLI's `/handoff <platform>` is a different feature; this skill produces text in the current chat only.

## Procedure

1. **Reconstruct this session.** Review the available conversation from the original request through the latest result. If earlier turns are unavailable, use `session_search` only if exposed and narrowly scoped to this conversation; otherwise explicitly mark the missing history. Record decisions and user constraints, completed changes, actual verification, open questions, and the single next action. Do not treat intentions or a plan as shipped work.
2. **Check named evidence, read-only.** Read a plan or task list already referenced in this chat via `read_file` or the available task tool. For files touched this session, use known paths with `read_file` or a narrowly scoped `terminal` check; for a remote artifact, use its exact URL/ID. Use `process_manage` or the available process/status tool to check known background IDs, and a read-only status command for a known repository or server if needed. Do not scan arbitrary directories, export the session, or call mutating tools. An observation from earlier in the chat is historical, not proof that a process is still running.
3. **Handle Orca pointers narrowly.** If this session names an Orca Run or worker, verify its exact Run ID, worker handle, and current status through read-only status/inspection available here. Include an **active** pointer only when the read-back confirms it is active; include the observed status and check time if available. If verification fails or the tool is unavailable, say `미확인 (not verified)` rather than calling it active. Orca job recovery, reconciliation, restart, and worker lifecycle belong to `orca-collab`: never start, restart, stop, or recover a worker during handoff. Do not infer a worker is alive from a stale log, a PID alone, or a prior statement.
4. **Write the handoff in the chat.** Use the template below, pruning empty detail but retaining every heading. Cite concrete evidence inline (command/result, file path, URL, task/process handle); distinguish `검증됨` (verified now), `대화 기록` (reported earlier), and `미확인` (not checked). Do not claim `없음`/`none` unless the relevant scope was actually checked; use `미확인` for incomplete visibility. Never write a handoff file or update memory automatically.

## Chat Template

```markdown
# Session Handoff — <one-line topic>

## Where it started
<user goal and constraints, 1–2 sentences>

## Decisions + completed work
- <decision / completed change> — <reason; evidence or exact artifact>

## Key files
- <absolute path, if verified> — <why next agent should read it>

## Running state
- Background processes / subagents: <verified handle, status, read-only check; or 없음 / 미확인>
- Servers / ports / branches: <verified item; or 없음 / 미확인>
- Orca Run / workers: <only read-only verified active pointers with status; otherwise 없음 / 미확인>

## Verification
- <actual check and observed result; or 검증 미실시>

## Deferred + open questions
- <deferred item / user question; or 없음 / 미확인>

## Pick up here
<one concrete next action for the fresh agent>
```

## Pitfalls

- Prefer **absolute, platform-native paths** resolved from observed context; if a path cannot be confirmed, mark it unverified rather than inventing one. Never leak secrets, private workspace details, or credential-bearing URLs into a shareable handoff.
- A task list, test, branch, server, or background process may have changed since the last turn. State when it was last observed; do not convert an old result into a current claim.
- Do not paste logs or a transcript. Keep the handoff short enough to paste into a new chat; preserve IDs and failure details only when needed to continue.
- Use the user's language for content (Korean when the user is writing Korean), terse and neutral; keep the template headings stable. No emoji or progress celebration.

## Verification

Before sending, check that each claimed completion has a real result, every named file path is absolute and relevant, every running handle has a read-only status check (or is explicitly unverified), every unanswered question is retained, and the final line gives exactly one next action. Sending the chat message is the entire output; do not create any other state.
