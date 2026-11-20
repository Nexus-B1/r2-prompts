---
name: plan-repo-merge
description: "Plan · Plan a merge of a parallel repo location into this one, anticipating conflicts, in the full planning format."
argument-hint: "<other-location> <merge-plan-file>"
arguments: [location, planfile]
allowed-tools: Bash(python *validate_plan.py*)
model: opus
effort: high
disable-model-invocation: true
---
We've done some changes in a parallel location which mimics this repo structure we have here. The other location is $location

The complete changes done in both locations can be found in their plan MD files, in the directory where each location keeps them: sort them by date and check commit times. The plans don't show everything, though, so also compare the code itself: if the two locations share git history, add the other one as a remote and use `git merge-base` and `git log A..B`; otherwise use `git diff --no-index` per repo. Changes that appear in no plan (hotfixes, manual edits, commenting passes) belong in the merge plan too. Default direction: the other location → here. Recommend the reverse only with evidence, such as clearly fewer conflicts or far fewer changes on this side. I want you to study the repos and create a plan for the merge, anticipating conflicts. You will have to solve conflicts based on the features executed in both locations. When having serious doubts, I'm here to help: collect the decisions that need me in an `## Open Questions` section of the merge plan, and ask the blocking ones before writing tasks. Let's plan the merge in: $planfile

The merge plan must also cover:

- Plan prefix collisions: both locations may have created plans with the same r2 code. Detect them, renumber one side following the plan prefix rule, and update every reference, including source-file headers.
- A safety branch in every repo before anything is merged.
- Lockfiles: regenerate them after the merge instead of merging them line by line.
- A final build-and-test phase in the merged repos.

The plan should contain granular tasks, each clearly visible with an empty [ ] checkbox. Order the work by dependency first: a group comes after the groups it depends on, and ends where its work can be verified on its own. Within that order, group tasks by implementation difficulty rather than by topic, so that we may select the right Agent when implementing them. Never merge unrelated tasks, or split tightly coupled ones, just to fit a difficulty.

## Difficulty

Rate every group as a whole on two drivers. Rate the group, not each task on its own: easy tasks can still need hard reasoning when the real problem is how they interact.

- **Complexity:** how much reasoning the work needs once the approach is known: how many contracts, components or files must stay consistent, and how intricate the logic is.
- **Uncertainty:** how much is still unknown: an approach not yet chosen, behaviour of a library, API or legacy code not yet verified, or requirements not yet settled.

| Tag | Complexity at this level | Uncertainty at this level |
| --- | --- | --- |
| {{SIMPLE}} | a local, well-understood change | none: no open design decisions |
| {{MEDIUM}} | an established pattern applied across a bounded area, with clear contracts and checks | small: the answers are in the code or docs at hand |
| {{HARD}} | several contracts to coordinate, or substantial debugging | the approach, or some behaviour, must be investigated within a settled design |
| {{COMPLEX}} | many interacting contracts or a large context, with judgment calls throughout | unresolved architectural, algorithmic or exploratory decisions that need investigation and judgment |

The group's difficulty tag is the higher of its two ratings: either driver alone is enough to make a group {{HARD}} or {{COMPLEX}}. A {{HARD}} or {{COMPLEX}} tag is followed, on the same line, by a driver tag naming the driver or drivers at that level: `{{driver: complexity}}`, `{{driver: uncertainty}}` or `{{driver: complexity + uncertainty}}`. {{SIMPLE}} and {{MEDIUM}} groups have no driver tag. The tag also picks the model: `/execute-easy-stretch` runs {{SIMPLE}} and {{MEDIUM}} groups on a cheaper model, and `/execute-hard-stretch` runs the others on the strongest one.

Making work easier never weakens its verification. When a mistake would be costly whatever the difficulty (security, data loss, a public contract), add a risk line above the tags: `Risk: HIGH — <the extra review or checks required>`.

## Group format

Every group follows this skeleton. `Requires:` and `Risk:` are optional; everything else is required.

```
### Group 5 — <what the group delivers>

Requires: <decisions or groups this group waits for>
**Outcome:** <what becomes possible, or which invariant becomes true, when the group is done>
**Verification:** <the cheapest check that would catch the outcome being wrong: a command, a test or an observable behaviour>
Risk: HIGH — <the extra review or checks required>

{{HARD}} {{driver: uncertainty}}
- [ ] 5.1 `T-r2abc-014` <task>
- [ ] 5.2 `T-r2abc-015` <task>
```

- The tags sit on their own line, immediately above the group's tasks.
- At most 8 tasks per group; 8 is a ceiling, not a target. Every group is numbered, and tasks use hierarchical display numbers such as 1.1, 1.2, 2.1, and so on.
- Every task also carries a stable ID, `` `T-<plan prefix>-NNN` ``, numbered in creation order and never reused. Display numbers change when groups are split or renumbered; IDs never do, so references between tasks use IDs.
- Executors mark a task [X] only after its group's verification passes, and add a `> Evidence:` note below the tasks with the commands run, the revision and the results.
- Plan only the verification the outcome needs: no test harness, fixture or report just to prove a point, and no task that exists only for ceremony.

## Global Mandatory Reading

The plan must begin, immediately after its title, with a `## Global Mandatory Reading` section.

Global Mandatory Reading must contain only the information an implementation agent must know regardless of which task group it is executing. Keep it thin, but substantive. It must not consist solely of barrel/index files, self-references, or planning-governance documents.

Include a small architecture spine using tight ranges from the relevant plan or implementation-handoff documents, together with live public code boundaries where they are globally relevant.

The Global Mandatory Reading table must use exactly these columns:

| File name | Line Ranges | Description |
| --- | --- | --- |

In each Description:

- Name the exact headings, exported symbols, invariants, or ownership boundary being consumed.
- Explain why the source is globally necessary.
- Explain what implementation decision or safety boundary it constrains.
- Do not merely summarize the entire file.

The Global Mandatory Reading section must always contain this exact execution protocol, verbatim, immediately before its table:

> **Execution protocol**
>
> - Read this Global Mandatory Reading section before the first task and again
>   after every context compaction.
> - Before starting or resuming a task group, read the nearest preceding Area
>   Mandatory Reading block whose `Applies to` label includes that group. Area
>   blocks appear immediately before the first group they govern.
> - A referenced heading or exported symbol is authoritative. Global navigation
>   hints and Area line ranges are for navigation only; if they drift, relocate
>   the named section or symbol rather than expanding to the whole file.
> - Mandatory reading is non-transitive. Do not preload a linked file's own
>   Mandatory Reading, Consult on Demand, or Planning Provenance entries unless
>   this plan names them directly for the current area.
> - Do not read Consult on Demand or Planning Provenance merely because those
>   sources are listed. Use a Consult on Demand source only when its trigger
>   occurs.
> - No created source, test, script, fixture or JSON file may start with the same prefix as a planning MD file (such as r2); only Markdown documents can have that prefix. Scripts, fixtures and test output never go in the plan's directory, and no MD file goes in a source directory unless specifically asked.
> - Before the first task, ask the user every unanswered question in Open Questions, all in one message.
> - After EVERY CONTEXT COMPACTION, add or update a single note above the task
>   group which is currently in execution. The note will say: "Context has
>   compacted X times while executing this group.". If the compaction occurs
>   before any meaningful work was done (this can happen when there is a lot
>   of baggage from the previous compaction), then and ONLY then you can skip
>   this step. Otherwise, also update the plan's checkpoint file.
> - When exceeding 3 context compactions, YOU MUST ask yourself if you're not
>   chewing more than we can handle :). Heck, plans change! :). In such a case,
>   the way out is to split the group on the spot, in the plan, into more
>   groups, by appending B, C, D as suffixes to those groups (splitting
>   sub-groups themselves is also allowed). When you do this, add Area
>   Mandatory Reading blocks so you can optimize your context only for the
>   ACTUAL task at hand.

## Objective Contract

Immediately after Global Mandatory Reading, add a `## Objective Contract` section. The objective is fixed; the groups below it are a strategy that executors may revise within their authority. State:

- **Objective:** what the plan must achieve, in one or two sentences.
- **Acceptance criteria:** the checkable conditions that prove it. Completion Conditions turns them into commands.
- **Protected contracts:** the public interfaces, invariants, data and security guarantees that must not change.
- **Execution permissions:** what the executor may change freely, what needs review, and what must stop for approval. A plan that authorizes code changes does not authorize destructive data operations, deploys, or sending anything outside the workspace unless it says so here.

## Open Questions

Immediately after the Objective Contract, add a `## Open Questions` section: every question that only the user can answer and that the plan depends on, numbered, each with your recommended answer and the groups it affects. Once a question is answered, record the answer next to it. If there are none, write "None." When you hand over the plan, ask all unanswered questions together, in one message.

## Area Mandatory Reading

In addition to Global Mandatory Reading, add Area Mandatory Reading blocks at key context transitions inside the implementation task plan.

Do not add an Area Mandatory Reading block before every task group. Add one only when the source of truth, implementation layer, ownership boundary, or required technical context changes enough to justify reloading a different set of contracts.

Example transitions, taken from one epic. They illustrate the rule above; they are not layers every plan must have:

- Legacy characterization to canonical-domain implementation.
- Canonical domain to profile or registry work.
- Profile work to catalog-backed input resolution.
- Input resolution to portable compilation and validation.
- Component implementation to determinism, integration, or acceptance testing.
- Implementation to downstream handoff and plan validation.

Each Area Mandatory Reading block must:

1. Appear immediately before the first task group it governs.
2. Use this heading format:

   `### Area Mandatory Reading - <short area name>`

3. State its coverage immediately below the heading:

   `_Applies to Group 5._`

   or:

   `_Applies to Groups 6-10._`

4. Use exactly these table columns:

| File name | Line Ranges | Description |
| --- | --- | --- |

The Description must name the authoritative headings or exported symbols and explain the exact area-specific contract being consumed.

Every task group must be covered by the nearest preceding Area Mandatory Reading block whose `Applies to` label includes it, so the first group always needs an Area block. Avoid ambiguous or overlapping coverage.

When an Area depends on code produced by earlier groups, reference the live public barrel and the exact exported symbols that should exist by that point. If the file does not exist before those earlier tasks run, the Line Ranges value may say `Live definitions; no fixed range`. The Description must state which earlier groups produce it and which exports are authoritative.

If an Area has a prerequisite that may not yet exist, add an explicit entry gate before its table. State:

- The exact public contract that must exist.
- How the agent verifies it.
- Which tasks must stop if it is absent.
- Which safe, independent work may continue.
- Which internal repositories, stores, files, or fallback paths must not be used to bypass the prerequisite.

## Reading-source selection rules

When composing Global or Area Mandatory Reading:

- Prefer live code, public barrels, exported schemas, interfaces, tests, and implementation handoffs over planning prose when they provide more concrete information with fewer tokens.
- For delivered repository behavior, live public code and executable tests take precedence over historical architecture or predecessor plans.
- For external standards, the current primary official specification is authoritative.
- Use Markdown architecture or predecessor-plan sections only when they provide ownership, rationale, invariants, or handoff information not expressed adequately in code.
- Move historical plans, surveys, product discussions, broad architecture documents, and client guides to Consult on Demand or Planning Provenance unless their exact sections are required for the current implementation area.
- Use tight line ranges. Never use `1-N` merely for convenience.
- Do not cut a range through the middle of a named heading, exported symbol, code block, table, or invariant.
- Named headings and exported symbols are authoritative. Line ranges are navigational and must be verified against the current workspace.
- Mandatory reading is non-transitive. A referenced plan does not make its own reading list mandatory.
- Do not repeat a source in multiple Area blocks unless it is genuinely needed again after context compaction.
- When repeating a source, narrow it to the exact symbols or sections required by that later area.

## Consult on Demand

After the final implementation task group, add a `## Consult on Demand` section.

The plan ends with a `## Completion Conditions` section (see below). Place Consult on Demand and Planning Provenance immediately before it, so that Completion Conditions remains last. The only sections allowed after Completion Conditions are `## Review N` sections, which reviews append, each followed by the post-review task groups that address it.

Consult on Demand contains sources that are not implementation prerequisites but may become useful after a concrete ambiguity, failed test, missing export, ownership dispute, standards mismatch, or unexpected runtime behavior appears.

The Consult on Demand table must use exactly these columns:

| Trigger | File name | Start at | Expand only when | Consultation purpose |
| --- | --- | --- | --- | --- |

Compose each row as follows:

- `Trigger`: State a concrete, observable condition. Do not use vague triggers such as “if useful” or “for more context.”
- `File name`: Link the exact source to consult. Prefer primary or current sources.
- `Start at`: Name the heading, exported symbol, test case, or tight initial line range where consultation begins.
- `Expand only when`: State the condition that justifies reading beyond the starting section.
- `Consultation purpose`: State the precise question the source may answer and its authority limit.

Consult on Demand commonly contains:

- Narrow predecessor-plan sections used only when a live contract is ambiguous.
- Historical architecture consulted only when code and tests do not explain legacy behavior.
- Provider surveys used only as leads for current official evidence.
- Client implementation guides used only for client-consumption problems.
- Adjacent standards used only when two artifact families are being confused.
- Downstream records consulted only during handoff work.
- Candidate APIs that must be inspected before accepting them as substitutes for a missing prerequisite.

A Consult on Demand source must never silently become mandatory. Its trigger must occur before it is read.

## Planning Provenance

Immediately after Consult on Demand, add a `## Planning Provenance` section.

Planning Provenance records material that materially shaped the construction of the plan but is not an implementation reading queue.

The Planning Provenance table must use exactly these columns:

| File name | Sections or Line Ranges used while planning | Planning contribution |
| --- | --- | --- |

Compose each row as follows:

- `File name`: Link the source that materially influenced the plan.
- `Sections or Line Ranges used while planning`: Record the tight sections or ranges actually used during plan construction.
- `Planning contribution`: Explain the decisions, decomposition, vocabulary, risks, sequencing, or ownership boundaries the source helped establish.

Planning Provenance may include:

- Plan-generation governance documents.
- Epic hubs and parent architecture chapters.
- Predecessor plans.
- Historical architecture.
- Product discussions.
- Standards surveys.
- Client guides.
- Adjacent conventions.
- Research used to identify unknowns or risks.

Do not include incidental files that did not materially affect the plan.

A source may appear in Planning Provenance and also in Mandatory Reading or Consult on Demand, but each appearance must describe a distinct role. Its presence in Planning Provenance never makes it an execution prerequisite.

Planning Provenance must include a short statement before the table making clear that:

- It is not an execution reading queue.
- It must not be preloaded after context compaction.
- It is non-transitive.
- Its line ranges record planning use rather than runtime authority.

## Completion Conditions

End the plan with a `## Completion Conditions` section: the concrete, checkable criteria that make the whole plan done, and the final regression command to run. The plan is complete only when every condition holds and the regression passes.

## Final validation

First run the plan validator, and fix every finding:

`python "${CLAUDE_SKILL_DIR}/../planning-template/scripts/validate_plan.py" <plan file>`

If that path doesn't resolve, the script is `planning-template/scripts/validate_plan.py` in the skills folder (`.claude/skills/` in the project, or `~/.claude/skills/`). It checks the mechanical rules: checkbox states and unique task IDs; numbering; difficulty and driver tags directly above the tasks; at most 8 tasks per group; Outcome and Verification lines; Area coverage; the verbatim Execution protocol; section order, including the Objective Contract and Open Questions; local links; and that the plan's directory holds documents only. If it can't run at all, check those rules by hand.

Then verify by reading that:

- Every task's checkbox is still an empty [ ].
- Groups follow dependency order, and each group's tag is the higher of its complexity and uncertainty ratings.
- Each Verification line is the cheapest check that would catch its outcome being wrong.
- Global Mandatory Reading contains only genuinely global contracts and includes substantive architectural context.
- The Objective Contract states the objective, acceptance criteria, protected contracts and execution permissions.
- Every question only the user can answer is in Open Questions, with a recommended answer.
- Area blocks exist only at meaningful context transitions.
- Mandatory sources prefer live code and tests where appropriate.
- Named headings and exported symbols exist.
- Line ranges are current, tight, and do not cut through their named material.
- Mandatory reading is non-transitive.
- Consult on Demand rows have concrete triggers and expansion conditions.
- Planning Provenance records planning influence without becoming mandatory.
- Missing prerequisites have explicit stop boundaries and forbidden fallback paths.
- Completion Conditions include a final regression command.
- Later plans do not duplicate an authority owned by an earlier plan.

Report the validator's result and pass or fail for each item above in your final message. Then ask the unanswered Open Questions, all in one message.
