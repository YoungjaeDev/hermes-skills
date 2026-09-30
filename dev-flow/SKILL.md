---
name: dev-flow
description: Deliver scoped changes from goal or issue to reviewed PR.
version: 0.1.0
author: YoungjaeDev, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [development, issues, delegation, testing, pull-requests]
---

# Development Flow

Carry an agreed goal or GitHub issue through implementation, live verification, a PR, and review. Hermes owns scope, integration, evidence, and the final report; delegate bounded coding work to Orca Claude when useful. This is a working procedure, not a rigid state machine or a substitute for the GitHub and Orca skills.

Adapted from [YoungjaeDev/my-claude-plugins `dev:flow` and `dev:resolve-issue`](https://github.com/YoungjaeDev/my-claude-plugins/tree/main/plugins/dev/skills) (MIT). This Hermes version **acts** within an agreed task scope; the source `dev:flow` only recommends next skills.

## When to Use

- The user asks to implement a defined change, resolve an issue, or take work through a PR and review.
- The user asks what remains in an in-flight goal → issue → implementation → PR journey; inspect the actual state first and continue only within authorized scope.
- Don't use for merely mentioning an issue, reviewing someone else's PR without implementation, or an informational question. A question about the flow alone does not authorize writes.

## Boundaries and prerequisites

- Establish the repository, default/base branch, current checkout/worktree, `git status`, project instructions, available tests, and GitHub authentication before changing anything. Preserve existing user edits; do not stash, reset, overwrite, or sweep them into a commit. If the work overlaps dirty files, resolve ownership with the user first.
- Turn the request into a small acceptance contract: desired behavior, non-goals, files/interfaces likely affected, test seam, and the allowed GitHub actions. Ask about decisions that materially change the result; don't invent requirements or expand an issue into unrelated cleanup. Split only when slices have independent acceptance and ownership.
- **Permission boundary:** Local edits, task-scoped commits, pushes, and opening/updating a PR may be autonomous when the user authorized delivery of that task to a PR and the repository permits it. A request to *plan*, *inspect*, or *review* is not delivery authorization. Never merge (including auto-merge or enabling its queue), run mutating DB commands/migrations, deploy, release, or perform destructive cleanup without separate, explicit approval for that exact action and target. Approval for a PR is not approval to merge. Existing project rules may be stricter.
- Load `orca-collab` for the delegation mechanics and current Orca capabilities. Its live `orca skills get orca-cli` and `orca skills get orchestration` instructions determine CLI syntax and whether a simple terminal task or supervised workers fit; do not copy stale commands from this skill. If Orca or that skill is unavailable, report the blocker and ask before changing the agreed delegation method. Never invoke Claude-only `Agent`, `/dev:*`, `Skill`, `AskUserQuestion`, or their state-file conventions as if they were Hermes tools.
- Load Hermes `github` (especially its `references/issue-to-pr.md` for issue delivery and `references/code-review.md` for external PR reviews), `github-pr-workflow` for branch/commit/PR/CI mechanics, and `requesting-code-review` for pre-commit review. Use `skill_view` where available. Follow repository-specific instructions over generic examples, but never relax the explicit-approval boundary above.

## Procedure — choose the next useful move

1. **Ground the work.** For an issue, read its live body **and comments** with Hermes `terminal`/`gh`, check linked plans and current code, and search existing PRs/commits to avoid duplicate work. For a plain goal, inspect the relevant paths using `search_files`/`read_file`. Reproduce a bug or establish the missing behavior and challenge stale/intentional premises. Record acceptance criteria, tests, risks, and exclusions. **Gate:** the change has a finite, current contract and no unresolved decision that blocks coding.
2. **Choose ownership and delegation.** A narrow known edit may be done inline; otherwise use `orca-collab` to send Orca Claude a bounded job card: goal, repository/worktree and owned paths, read-only context, non-goals, acceptance tests, expected output/evidence, and prohibited side effects (merge, DB mutation, deploy, release). Use separate worktrees for concurrent writers; choose a **supervised** Orca Run only when the user wants Hermes to track completion, answer worker questions, and review outcomes *and* the installed Orca guide's coordinator binding is verified. Otherwise use clearly labeled terminal-level delegation. Do not parallelize writers of the same file. Ensure the worker can access only intended inputs; do not copy credentials into prompts or worktrees. Hermes remains responsible for checking the returned diff and running integration verification, regardless of a worker's self-report. **Gate:** each changed path has an owner, and no result is accepted solely on a worker's assertion.
3. **Implement the smallest complete change.** Follow project patterns; for a bug, diagnose the root cause and add a regression test that fails on the old behavior before fixing it when practical. For features, exercise the agreed public behavior and edge cases. Check adjacent call sites for the same defect without broadening scope silently. Inspect `git diff`/`git status` after each integration; reject or quarantine out-of-scope edits instead of committing them. **Gate:** every modified file traces to an acceptance criterion or its necessary test, and the original issue is resolved in the current tree.
4. **Verify locally, then review.** Run the repository's real targeted tests and relevant build/lint/type checks via Hermes `terminal`; execute runnable changes rather than inferring success from files. Keep command, exit status, and decisive output. If a check fails, diagnose and fix, or identify a reproducible baseline/environment blocker; do not call it passing. Compare the diff with the contract, then apply `requesting-code-review` or an independent review when appropriate; address security, logic, and spec gaps and re-run affected checks. **Gate:** acceptance evidence is observed in the integrated tree; unresolved failures are named, not hidden.
5. **Commit, push, and open the PR only within the agreed scope.** Stage explicit task files, inspect the staged diff, and use `github-pr-workflow`/`github` mechanics. In the PR body state the issue/goal, approach, test commands/results, risk, exclusions, and any failing or unrun checks. Read the new PR back: base/head, commit SHA, changed files, body, and URL must match intent. If tests remain blocked, pause or use a clearly labeled draft PR only when delivery scope allows; never present a draft or a pushed branch as a verified fix. **Gate:** the live PR contains only the authorized change and its claims match observed output.
6. **Shepherd review without assuming convergence.** Read live CI results and reviewer threads (including bot comments if present); distinguish pending, failed, and passed checks. Triage each substantive finding as fix, defer with reason, or reject with evidence; fix in scope, rerun affected tests, push, and reread the latest SHA/checks/reviews. Stop on repeated churn, new scope, or a decision requiring user input. Don't require a particular review bot and don't mistake no comments for approval. **Gate:** report the current PR URL, exact tested SHA/check state, addressed versus outstanding findings, and what remains unverified. Stop before merge unless separately approved for that PR and target.

## Pitfalls

- A pre-PR local test pass does not prove the pushed SHA or CI is green; reread the live PR after each push.
- An issue title is not the current specification; later comments and existing PRs can supersede it.
- A worker's “done,” a generated test file, or a review bot's silence is not evidence of behavior.
- Worktrees isolate Git history, not secrets or filesystem access; verify worker path ownership and integration in the tree that will be pushed.
- `github-pr-workflow` includes merge examples; they are **not** permission to merge. Never use an `--auto-merge` path without explicit separate approval.

## Verification / handoff

Finish with: scope delivered; changed paths; actual commands and outcomes (or why unrun); commit/PR URL and fresh remote state if created; review findings still open; explicit blockers and the next human decision. Say **not verified** for any unrun criterion. Do not say “done,” “green,” “merged,” or “deployed” without live evidence of that exact claim. A completed PR is a reviewable artifact, not a merge or release.
