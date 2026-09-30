---
name: interview-methodology
description: Interview users and stress-test consequential plans.
version: 0.1.0
author: YoungjaeDev (YoungjaeDev), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [requirements, interview, clarification, specification, stress-test]
    requires_tools: [clarify]
---

# Interview Methodology

Resolve consequential unknowns before committing to a design. Interview for decisions the user owns; investigate facts you can discover yourself. Match the number of questions and the output to the stakes, rather than turning every request into a questionnaire.

## When to Use

- The user says “interview me,” “ask questions first,” “요구사항을 정리해줘,” or wants a specification before substantial implementation.
- A feature or workflow has multiple plausible interpretations that would materially change its behavior, risk, or cost.
- The user says “grill me,” “poke holes in this plan,” “집요하게 캐물어,” or explicitly requests a rigorous challenge to a plan already on the table.
- An interview should produce a reusable prompt for a later session (including a TCREI-style prompt).

**Do not use a full interview** for an explicit, well-specified request; a typo, test, copy, or mechanical change; or when the user says to proceed without questions. Do the work, stating reversible assumptions if needed. If a single costly ambiguity blocks a request that permits questions, ask one targeted question instead of conducting an interview. If the user forbids questions and no safe assumption exists, name the blocker rather than silently inventing a decision. Explicit stress-test requests are the exception to the quick-interview rule: do not silently downshift them.

## Prerequisites

- Use Hermes `clarify` for questions requiring a user decision. No external CLI, credentials, or OS-specific setup is needed.
- Inspect any supplied plan and available project context first. Use `read_file`, `search_files`, and relevant read-only retrieval to settle facts before asking about them; do not read unrelated private material.

## Procedure

1. **Choose the scope and name it.** Check what is already known, what can be looked up, and which *decisions* remain. Choose **quick** (one to three blockers), **breadth** (several independent requirements), **depth** (one dominant uncertainty with dependent branches), or **grill** (an explicit adversarial stress test). Tell the user the mode in a short sentence only when an actual interview is starting. Done when each proposed question changes a decision or acceptance criterion; otherwise cut it.
2. **Map the decision frontier.** Record what you understand, the assumption you might be making, the consequence if it is wrong, and who can decide. Challenge unspoken premises: “What must be true for this to work?”, “What happens when the dependency fails?”, “Who bears the cost if our assumption is wrong?” Check for conflicting goals, missing stakeholders, scale, security/privacy, and reversibility. Do not ask what the repository, supplied documents, or tools already establish. Done when the next question has a reason to be asked *now*.
3. **Ask through `clarify`, not an invented interaction.** For independent decisions, send a `questions` array of **two to five** questions in one call; for one blocking question, use a single question. A question can offer at most four concrete choices (best defensible default first, labelled Recommended by the UI), an open answer, or `multi_select` for genuinely nonexclusive choices. Explain meaningful trade-offs in concise option wording, preserve an “Other” path, and ask in the user's language (Korean when appropriate). Example: “현재 이해: 외부 API가 간헐적으로 실패합니다. 결정: 실패 시 사용자 경험. 추천: 재시도 후 오류 안내(중복 요청 위험은 별도 처리). 어떤 동작을 원하세요?” Do **not** batch a downstream question whose wording or options depend on an earlier answer; wait, then ask it in the next round. Done when the call has no redundant or leading questions.
4. **Interpret responses precisely.** Read `clarify`'s `responses` in question order and check each `user_response`; some calls also carry a top-level `timed_out` flag and an explanatory notice. Missing or empty answers and a timeout are not consent. Preserve any answered entries in a partial batch; do not repeat those questions. For a low-risk unresolved point, adopt and label a reversible default; for an expensive or irreversible choice, stop that branch and clearly state the blocker. If the user stops the interview, stop immediately. Done when no inferred agreement is attributed to silence.
5. **Follow the chosen mode.**
   - **Quick:** resolve only the implementation-changing unknowns, then act or summarize. Do not extend it just to fill a question quota.
   - **Breadth:** establish objective and success signal, then cover relevant dimensions: technical integration/data/security, users and UX/accessibility, failures and edge cases, constraints/trade-offs, business value/ownership. Prioritize must-haves versus deferrable work, surface contradictions, then validate a synthesized understanding. Skip irrelevant dimensions; batch independent questions in small rounds rather than dropping a long form at once. Continue until every consequential decision has an answer, an explicit open owner, or a safe default.
   - **Depth:** ask the single highest-leverage unknown, use its answer to select the next question, and stop when that uncertainty no longer changes the proposed approach. Move to breadth only if the answer exposes several independent decisions.
   - **Grill:** test the user's existing proposal against its strongest failure cases, counterexamples, dependencies, incentives, and rollback path. Walk prerequisites before dependent branches; independently investigate facts using **read-only** tools, while leaving value judgments to the user. Be firm about contradictions without being hostile. Do not volunteer a shortcut or begin implementation, edits, or a spec write until the user **explicitly confirms shared understanding** after seeing the resolved plan and residual risks. If the user explicitly cancels, stops, or says proceed anyway, honor that instruction and state any unresolved risks; do not hold the user hostage to the mode.
6. **Close at the right weight.** For quick/depth, present **decisions / assumptions / open questions** inline and proceed if authorized. For a substantial breadth interview, present a concise proposed spec and confirm material interpretations with `clarify` before writing a persistent file. Include objective, user stories or actors, prioritized requirements (P0/P1/P2), constraints, error/edge behaviors, acceptance tests, non-goals, and unresolved decisions with owners. Write with `write_file` only when a spec is requested or its destination is agreed; use a project-relative path chosen with the user, not a tool-specific hidden directory. Do not write a speculative spec after a cancelled grill. For a next-session prompt, provide copy-paste-ready **Task / Context / References / Evaluate / Iterate** sections; ask only for missing decisions, and mark missing source materials rather than inventing them. Done when the output can guide the next action without hiding uncertainty.

## Pitfalls

- **Interrogation by default:** “Tell me your stack” wastes time when the code answers it; inspect first and ask only about intent or trade-offs.
- **Batching dependent questions:** an early answer can invalidate later options. Batch only independent forks, then adapt the next round.
- **Recommendations that steer the outcome:** show why an option is recommended and a credible alternative; do not disguise a preference as a fact.
- **Grill without consent to act:** pressure-testing a plan is not permission to implement it. Keep investigation read-only until explicit confirmation (or the user's explicit change of direction).
- **False completion:** a skipped question or vague “looks good” does not close a costly unresolved decision. Name its owner and impact instead.
- **Oversized deliverables:** a two-question clarification does not require a spec file; conversely, a complex interview should not end with an uncaptured chat summary when a persistent spec was requested.

## Verification

Before closing, check that (1) each question addressed a real implementation-changing gap, (2) independent decisions were batched and dependent ones asked in order, (3) every material answer, contradiction, assumption, and unresolved risk appears in the output, (4) user confirmation precedes any requested persistent spec or grill-mode execution, and (5) the proposed next step and its acceptance criteria are explicit. Never claim the user approved an unanswered item.
