---
name: break-groups
description: "Plan · Break groups for a cheaper executor, by driver: `complex` takes {{COMPLEX}} to {{HARD}} or lower, `hard` takes {{HARD}} to {{MEDIUM}} or lower."
argument-hint: "<complex|hard> [plan-file]"
arguments: [tier, plan]
allowed-tools: Bash(python *validate_plan.py*)
model: opus
effort: high
disable-model-invocation: true
---
Pass: $tier
Plan: $plan
(If no plan is named above, use the plan we are working on in this conversation. If the pass is neither `complex` nor `hard`, ask which one to run.)

- `complex`, the first pass: break {{COMPLEX}} groups into {{HARD}} or lower difficulty groups by going deeper into each of them and simplifying for an incoming agent. Also, if a {{HARD}} group turns out to be {{COMPLEX}} on either driver (see the Difficulty section of `/planning-template`), break that too.
- `hard`, the second pass, usually after `complex`: break {{HARD}} groups, and any {{COMPLEX}} groups still in the plan, into {{MEDIUM}} or lower groups. The tasks need to be very granular and max medium in difficulty. If a group genuinely needs a large context and can't be split further without becoming artificial, leave it at {{HARD}} with the note "stays {{HARD}}: <reason>".

So this is sort of a deeper dive into planning mode, where you focus on making the complex easier: `complex` is the 1st iteration, and `hard` an EVEN deeper 2nd one. Go as deep as you need in order to do this reliably. You may research code in depth.

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
