---
name: review-implementation
description: "Flow · Adversarial review of the work a plan produced, in a fresh subagent; appends a numbered review to the plan."
argument-hint: "<plan-file> [since-ref]"
arguments: [plan, since]
context: fork
background: false
model: opus
effort: high
disable-model-invocation: true
---
Plan: $plan
Since ref (empty means none): [$since]

If no plan is named above, stop and reply that a plan path is needed: you run in a separate context and cannot see the conversation.

The plan was implemented by another agent. Please conduct an adversarial review: assume the implementation is wrong until the evidence shows otherwise.

What to review:

- The current uncommitted work trees in the affected projects or, if a since ref is given above, the commits since that ref.
- Only the files touched by the plan's [X] tasks. List any other changed files separately as "unrelated changes", without reviewing them.

Check:

- Was each [X] task really done, as described?
- Does each [X] task's group have an `> Evidence:` note, and does the evidence hold up? Re-run its commands where you can.
- Look for counterexamples against the original requirements, and flag assertions that were weakened or removed.
- Recorded decisions (`> Decision:` notes) and superseded `[-]` tasks: was the evidence enough, and do the objective and acceptance criteria still hold?
- Judge evidence by whether it would catch the work being wrong, not by its volume. Recommend new tests, fixtures or other artifacts only where a claim stays unproven without them.
- Do the tests exist, and do the focused ones pass? Run them.
- Were the plan's contracts respected: Mandatory Reading entries, entry gates, ownership boundaries?
- The commenting standard: file headers, function docs, business-logic conditions and loops.
- File placement and naming: no scripts, fixtures or output in documentation directories, no documents in source directories, and no non-Markdown file starting with the r2 prefix.
- Scope creep, and plan deviations nobody recorded.
- Security.

Output: append the review to the end of the plan, after every other section, as `## Review N — <date>`, where N is 1 for the first review and otherwise one more than the last. Number the findings R1, R2, …, each with a severity (high, medium or low), file:line and the evidence. End with a verdict. Then reply with a short summary of the findings.
