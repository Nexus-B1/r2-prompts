---
name: plan-review-fixes
description: "Flow · After a review: turn every finding into post-review tasks, with their own Area Mandatory Reading, broken down for the executor."
argument-hint: "[plan-file]"
allowed-tools: Bash(python *validate_plan.py*)
model: opus
effort: high
disable-model-invocation: true
---
Plan: $ARGUMENTS
(If no plan is named above, use the plan we are working on in this conversation.)

Another agent has reviewed the implementation of this plan. Now append tasks to the plan in continuation of the review, with the purpose of addressing all issues found, and prepare them for a fresh agent that will run `/execute-plan <plan> post-review`.

1. Read the latest `## Review N` section at the end of the plan; don't rely on the conversation, which may have been compacted since the review.
2. Write one task per finding, with its stable ID and the finding's ID, for example ``- [ ] 23.1 `T-r2abc-120` (R3) Fix …``. A finding may instead get `won't fix: <reason>`, written under the review. Follow the plan's format: groups of at most 8 tasks, each with its Outcome and Verification lines and its tags on their own line directly above its tasks, numbering continued after the plan's last group, and `[ ]` boxes. Put the new groups directly after that review section.
3. Create a new Area Mandatory Reading block for this iteration, headed `### Area Mandatory Reading - Review fixes`, with an `_Applies to Groups …_` label. It includes exactly what is needed for this iteration, borrowing heavily from the Global Mandatory Reading at the top of the file. Insert it directly above the new groups.
4. Check whether the Global Mandatory Reading at the top still holds now that the implementation changed the code: fix stale line ranges, and renamed or removed symbols.
5. Break the new {{COMPLEX}} groups into {{HARD}} or lower difficulty groups by going deeper into each of them and simplifying for an incoming agent, following the rules below.

## How to break groups down

- Leave completed [X] groups untouched.
- Before breaking down a group, read the Area Mandatory Reading block that governs it, so that you break it down well and keep the reading blocks correct for the new groups.
- Refine for the target executor: keep refining a group until the decisions left in it are ones an agent of the target tier reliably makes. A refinement must make the work more executable, not merely longer. Never lower a tag just by adding prose.
- Break each group according to its driver tag (rate it first if it has none, as the Difficulty section of `/planning-template` describes):
  - **Uncertainty.** Don't write detailed steps for an approach nobody has verified: detail makes a guess look authoritative. First add a bounded investigation or prototype task, in its own earlier group, with a limit (such as 3 attempts) and an output (the decision it settles, the facts it confirms). Then detail only the work its answer can't change, and keep the rest at contract level: what must hold, not how.
  - **Complexity.** The approach is known but laborious. Detail each task, preferably with code snippets and even mermaid js diagrams, and split along dependency and verification boundaries.
  - **Both.** Resolve the uncertainty first, then split the complex part.
- Label every snippet as **Observed** (existing code, verified now), **Required contract** (an interface or invariant the work must preserve) or **Illustrative** (one possible approach, to check before using it).
- Research the code as deeply as you need to make that detail reliable, and no deeper.
- Refine the next area that is ready to start. Keep later groups at contract level until earlier groups have established the facts they depend on.
- Preserve the original requirements, acceptance criteria, invariants and ownership boundaries. Splitting "perform an atomic update" into easy steps must not lose the atomicity, and no group's Verification line may get weaker.
- You may assume that things built earlier in the plan are already built. When you do, YOU MUST add the note: "ASSUMPTION: this was already built previously. If not, re-assess at runtime". When a group depends on a contract that earlier groups must deliver, give its Area block an entry gate, so that the executor stops rather than inventing a substitute.
- Re-run grouping after you've done this: dependency order first, max 8 tasks per group, and each group with its Outcome and Verification lines, re-rated on both drivers, with its tags on their own line immediately above its tasks.
- Tasks keep their stable IDs when you split or move them; new tasks get new IDs. Update group numbering if necessary, but keep references valid: prefer splitting a group with suffixes (5 → 5A, 5B, 5C) over renumbering the groups after it. If you do renumber, update every `_Applies to_` label and every reference to the moved groups. Never renumber completed groups.
- Questions only the user can answer go to the plan's `## Open Questions`, each with your recommended answer. Don't stop to ask them one by one.
- There is NO limit on the number of groups per plan file. Create as many new groups as necessary, and no more.
- When you are done, run the plan validator, `python "${CLAUDE_SKILL_DIR}/../planning-template/scripts/validate_plan.py" <plan file>`, and fix every finding in the groups you changed. Report the rest without fixing them.
