---
name: orca-collab
description: Delegate to Claude in Orca and review its work.
version: 0.1.0
author: YoungjaeDev, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Orca, Claude, Delegation, Worktrees, Review]
---

# Orca collaboration from Hermes

Operate Orca-managed Claude sessions from **either Hermes Desktop or Hermes CLI**. Choose the least complicated Orca primitive that gives the requested ownership and feedback loop. This skill adds a Hermes-facing decision and verification layer; the installed Orca executable, not a copied command table, owns CLI syntax and runtime contracts.

## When to use

Load for requests to open or reuse Claude in Orca, delegate work across one or several Orca terminals/worktrees, watch progress, review results, resume an interrupted delegation, or coordinate supervised Orca workers. Use `claude-code` directly instead when the task has no Orca-managed state and a one-shot `claude -p` is sufficient. Do not treat a generic Hermes `delegate_task` worker as an Orca worker.

## Prerequisites

1. Resolve one Orca executable for this session: honor `ORCA_CLI_COMMAND` if set; in a dev checkout with `ORCA_DEV_REPO_ROOT` use `orca-dev`; on Linux outside Orca-managed terminals use `orca-ide` (bare `/usr/bin/orca` may be the GNOME screen reader); otherwise use `orca`. Substitute the selected executable in **every** example below. If it fails, report its exact error; do not silently try another build.
2. Through `terminal`, read `orca skills get orca-cli --json`. Before **tracked supervision**, also read `orca skills get orchestration --json`. These guides come from the installed executable and take precedence over example flags in this skill. Use its `--help` for any missing flag; if `skills get` is unavailable, stop rather than guessing mutations.
3. Check `orca status --json`. If Orca is genuinely not running, `orca open --json` may start it for an authorized Orca task. A `runtime_access_denied` or other sandbox denial is **not** a reason to start/restart Orca: report it and request proper access.
4. Determine the exact registered repo/worktree, whether the checkout has uncommitted work, the user-authorized write/remote scope, and any already-running agents. From Desktop or a non-Orca terminal, never assume `active`/`current` refers to the intended worktree; use an explicit selector and copy the returned IDs/handles.

## Choose the interaction

| Need | Orca route |
| --- | --- |
| Ask an existing agent a bounded question; make a lightweight handoff with no continuing supervisor | `terminal list/read/send`; use `wait` and `read` for a reply **only if** the user asked to monitor it. A full ownership handoff stops monitoring after delivery. |
| Hermes remains responsible for completion, questions, retries and review | Load the **orchestration** guide; use a Run, Task and preferably `worker-start` with `worker_done`/`check --wait`, when a valid coordinator identity is available. |
| Start one or several coding agents in isolated branches | Separate Orca worktrees per concurrent writer; use `worktree create --agent claude` for a simple launch or `worker-start --worktree new-child|new-top-level --agent claude` for supervised launches. |
| Fresh Claude in the same checkout without a new worktree | `terminal create --worktree <exact-selector> --command "claude"`; never mistake this for branch isolation. |

A working terminal exchange is **not** evidence of an Orca Run or Dispatch. Do not invent `taskId`/`dispatchId` for an ad-hoc prompt. A Run is a durable namespace/inbox, not an automatic scheduler.

## Procedure

1. **Scope and route.** Restate the goal, target repo/branch, Claude's read/write paths, completion checks, autonomy limits, and which mode above applies. Independent writers get disjoint file ownership and separate worktrees; review-only agents must not edit. Never infer permission to merge, mutate a database, deploy, or expose secrets from permission to code. Local edits/commits and push/PR are allowed only inside the user's authorized task scope; merge, DB changes and deployment require explicit approval.
2. **Discover before acting.** Use `terminal` with `orca repo list --json`, `orca worktree list --json`, and `orca terminal list --json`; check `git status` in the exact checkout. Capture the target's complete `worktreeId` and current terminal handle; distinguish a currently live agent from a stale tab. `terminal read --screen --terminal <handle> --json` shows the rendered TUI; accumulated output can contain repaint artifacts. Never send a prompt to every terminal matching a title.
3. **Start only what is missing.** In an existing checkout use `terminal create --worktree <exact-selector> --command "claude" --json`. For an isolated writer use `worktree create --repo <exact-repo> --name <task-name> --agent claude --json`; add `--activate` only when the user wants the app to switch view. Do not create both a worktree agent and a second terminal for that same worker. For supervised work prefer the installed guide's `run-create`/`task-create`/`worker-start` loop, which owns readiness and Dispatch provenance. Inspect the receipt before any retry or further mutation.
4. **Handle first-run trust honestly.** `terminal wait --terminal <handle> --for tui-idle --timeout-ms <bounded-ms> --json` confirms readiness/idle, **not** task success. Read the screen for trust, login, permission or question prompts. A new folder may need a human workspace-trust decision; never blindly approve a dialog or switch to a bypass flag. Ask through `clarify` when a decision is needed; passwords and 2FA belong only in approved secure UI paths, never `terminal send`.
5. **Delegate and observe.** For ad-hoc supervision, use an explicit handle: `terminal send --terminal <handle> --text <task-card> --enter --json`, then `terminal wait --terminal <handle> --for tui-idle --timeout-ms <bounded-ms> --json` and `terminal read --terminal <handle> --screen --json` (or `--cursor <previous-nextCursor>` for new stream lines). For tracked work, accept only Orca-injected Dispatch preambles and await `orchestration check --wait --types worker_done,escalation,question --timeout-ms <bounded-ms> --json`; answer real questions and process **every** message before acknowledging the Delivery. A timeout is a checkpoint, not failure. Do not poll with blind sleeps or kill a worker merely because it is quiet.
6. **Verify independently.** Read the worker's changed paths and branch diff from git, run relevant tests and inspect their actual output. Match edits to the agreed owner and acceptance criteria; a worker's prose, TUI idle prompt or `worker_done` is not sufficient proof. Request a review from another agent only when it adds independent signal and cannot write the same files concurrently. Report separately: worker's claim, verified facts, and remaining blockers.
7. **Settle and resume.** For a settled *supervised* Dispatch, follow the installed orchestration guide: reuse the same exact terminal for an immediate next Task or `worker-release` it (or explicitly retain it for user debugging) **before** acknowledging/waiting again. Never release on a timeout or unanswered question. On restart, read `run-list`, `run-show`, `task-list`, `dispatch-show`, `worker-show` and `worker-list` before creating anything; recover a stale terminal handle with `terminal list`. Use `request-show`/`--retry-request` only with the original operation identity when a mutation outcome is unknown. No local checkpoint overrides Orca's live state or authorizes duplicate dispatch.

### Desktop/CLI boundary

Both Hermes surfaces can invoke the same Orca executable and this same skill. They are **not automatically the same Hermes conversation or an Orca coordinator terminal**. `orchestration run-current --json` can return `null` outside a bound Orca terminal. Do not manufacture coordinator authority with `--from` or claim a tracked Run when identity/binding has not been verified in that environment. Fall back to clearly labeled low-level terminal supervision, or establish a real bound coordinator according to the installed guide, before using tracked mutations. Keep the user's original scope across a surface switch; discover live Orca state again rather than replaying a prompt.

## Pitfalls

- Orca may have several repos with the same display name; use returned IDs and explicit selectors. Terminal handles can change when the runtime restarts; rediscover rather than dual-send.
- Starting two writers in one checkout is not isolation. A fresh worktree omits ignored/uncommitted files and may run repo setup hooks; inspect inputs and setup policy before dispatching.
- `orca terminal read` without `--screen` is a stream, not the rendered TUI. A visible `❯` or `tui-idle` is not proof tests passed.
- Use `worker-start` for owned supervised resources. Low-level `dispatch --inject` onto an operator-started terminal creates a tracked context but leaves its terminal **unsupervised**; `worker-release` does not own it.
- Keep Orca Run/Task/Dispatch as source of truth. A future local checkpoint may index IDs and approvals, but must not duplicate task outcomes, store secrets, or trigger automatic worker recreation on uncertain state.
- Do not let this skill's example flags drift ahead of the installed binary. Re-read `skills get` at the start of each new session.

## Verification

For a read-only smoke test: find or launch one Claude terminal, send a request restricted to two non-secret files, wait, read an actual answer, and confirm `git status --short` is unchanged. For a tracked task, verify the exact Run/Task/Dispatch IDs with Orca reads, inspect `worker_done` and git/test evidence, and account for the settled worker resource. Report which mode actually ran; never call a terminal-only test a supervised orchestration test.
