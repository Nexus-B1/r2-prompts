---
name: execute-easy-stretch
description: "Flow · Run SIMPLE/MEDIUM groups on Sonnet until the first HARD or COMPLEX group, with the full execution rules."
argument-hint: "[plan-file]"
model: sonnet
effort: medium
disable-model-invocation: true
---
Plan: $ARGUMENTS
(If no plan is named above, use the plan we are working on in this conversation.)

Scope: the {{SIMPLE}} and {{MEDIUM}} groups, in order, starting at the first group with unchecked tasks. Stop before the first {{HARD}} or {{COMPLEX}} group, or at the end of the plan, and report where you stopped, for example: "Stopped before Group 7 ({{HARD}}). Run /execute-hard-stretch next." If you re-rate a group into a tier outside this stretch, stop and report instead of attempting it.

## Before you start

- Read the whole scope once, and collect every question that only the user can answer: unanswered entries in the plan's `## Open Questions`, Pending decisions, `ASSUMPTION` notes you can't verify, contradictions, and missing values such as paths, names or credentials.
- Ask them all in one message before executing anything: numbered, each with your recommended answer. Ask only what changes the work; decide everything else yourself, as "Decisions during execution" allows.
- If there are none, say so in one line and start.
- If the user tells you to go ahead without an answer, use your recommended answer and record it as an `ASSUMPTION:` note where it applies.

## How to execute

- Work through the tasks in plan order, top to bottom, sequentially, within the scope given above. Avoid sub-agents unless explicitly requested.
- Mark a task [X] only after its group's verification passes, and mark each task as soon as that is true. A group's verification is its **Verification:** line or, if it has none, the focused tests for its tasks. Never mark a task you did not complete.
- When the code exists but can't be verified, leave the box [ ] and add an indented note directly under the task: `  > Implemented; verification blocked: <reason>`.
- After each group, write a `> Evidence:` note below its tasks: the commands you ran, the revision (`git rev-parse --short HEAD`, plus "+dirty" when there are uncommitted changes) and the results.
- Never weaken acceptance criteria, and never remove or loosen assertions to get a green result. If a check seems wrong, report it instead of changing it.
- Do not commit; committing is `/commit-all-repos`'s job.

## Decisions during execution

The plan's order holds only while it is still the best known route to its objective. Reassess at each group boundary, and whenever new evidence appears: an existing capability, redundant work, an unexpected dependency, a simpler approach. Never execute a task you have shown to be unnecessary, and don't reopen a decision without new evidence. If the plan's Objective Contract sets execution permissions, they take precedence over this table.

| Level | Examples | Your authority |
| --- | --- | --- |
| Tactical | algorithm, naming, test layout | decide |
| Operational | split, merge or reorder independent groups; re-rate a group's difficulty | decide and record |
| Strategic, within the objective | replace an approach; supersede tasks shown to be unnecessary; reuse an existing capability; skip a task that is blocked, needs a human operator, or needs more than 2 groups of new planning | decide with evidence, and record |
| Objective-changing | requirements, acceptance criteria, public contracts, security guarantees, budget; any gate before an irreversible or outward-facing action (migrations, deleting data or files, deploys, publishing, sending anything outside the workspace) | stop and ask |

- Record each operational or strategic decision directly above the affected group's heading, never between a difficulty tag and its tasks: `> Decision: <observation> → <decision>; impact: <what changes>; verified by: <check>`.
- A superseded task becomes `- [-] n.m … — Superseded: <reason>`. Never mark unperformed work [X].
- A skipped task keeps its [ ] box, with `> SKIPPED n.m — <reason>; unblock by: <what is needed>` above its group's heading. Skip the tasks that depend on it too. Never stub or fake skipped work to keep going.
- When you are blocked and the only way forward is objective-changing, stop and report.

## Mandatory reading

- If the plan has a Global Mandatory Reading section, YOU MUST READ IT BEFORE DOING ANYTHING, and follow the Execution protocol inside it.
- Before starting or resuming a group, YOU MUST read its Area Mandatory Reading block: the nearest block ABOVE the group whose `Applies to` label includes it.
- After EVERY CONTEXT COMPACTION, re-check both lists and re-read ONLY the entries relevant to the task at hand. Be frugal: read what is important and relevant, do not read everything again and again.

## Checkpoint

Keep one checkpoint file per plan, so that progress survives compactions and handovers.

- It sits next to the plan, named with the plan's prefix and the next free helper letter: `<prefix>-<letter>-checkpoint.md`. Create it once, then keep reusing it.
- It holds the current state, overwritten each time rather than appended: the active group and task; the revision and any uncommitted changes; verified work, with the commands and results; partial or unverified work; decisions taken and contracts changed; facts you found to be stale; the next concrete action; blockers and pending test runs.
- Update it after meaningful progress, before a handover, and when compaction is near.
- Keep one pointer line directly above the active group's heading, `> Checkpoint: <file name>`, and move it when the active group changes.

## Commenting standard

Applies to source code in any language. JSON, lockfiles, generated files and Markdown are exempt.

- **File headers:** every file starts with a header that relates it to an `archi*.md` architecture document, an `r2*.md` plan, or both. Prefer a link to the specific architecture section that explains how the code works; the plan that delivered the change is the secondary reference. Never invent a reference: find it by searching the architecture docs and plans for the file or its module.
- **Classes and interfaces:** every class and interface has a javaDoc-style header (JSDoc/TSDoc in TypeScript, docstrings in Python) that states its responsibility and the contracts it upholds.
- **Functions:** every function has javaDoc-style docs with clear comments for each argument. An argument comment explains meaning, units and constraints (allowed values, nullability, ownership), not the argument's name and type again. Also document the return value, side effects and thrown errors when there are any.
- **Conditions:** every `if` statement with more than 1 condition is described as business logic: why it exists and what it affects in the bigger picture. Do the same for a single-condition guard that protects an invariant, such as idempotency, authorization or ordering.
- **Loops:** every loop that is not trivial is explained as business logic.
- Comments explain why. Never restate what the syntax already says.

## Tests

- Verify each claim with the cheapest check that would catch it being wrong: a focused test, a type-check, a grep or a read-through. Write a new test, fixture or script only when no existing check can show the result, or when the plan asks for one. Never build a harness just to prove a point.
- While implementing, run only the focused tests for the code you are changing.
- Run integration or regression tests when a change crosses a boundary: a public contract, shared infrastructure, persistence, or several components.
- Run the broader suite once before the plan is complete, or record in the Evidence note why you didn't.
- If tests take more than 2 minutes, find out why (setup, dependencies, test selection, parallelism) before going on. If a test file is simply too big, split it by responsibility.
- Give test commands a timeout of at least 3 minutes. Run anything longer in the background and wait for its completion notice instead of polling it.

## Files and folders

Keep documents and everything else apart. A plan's directory, like any documentation directory, holds Markdown documents only.

| What you create | Where it goes | How to name it |
| --- | --- | --- |
| A document that supports the plan: notes, findings, the checkpoint, a design | the plan's directory | the plan's prefix, the next free letter and a topic: plan `r2bla5-<name>.md` gets `r2bla5-a-<topic>.md`, then `r2bla5-b-<topic>.md`; plan `r2bla5-5-<name>.md` gets `r2bla5-5-a-<topic>.md` |
| Source code, tests, and the fixtures, mock data and tooling that tests need | next to the code or tests they belong to | the project's conventions |
| Scripts, logs, test output, snapshots and other artifacts needed only while the plan runs | `test-cache/` at the root of the affected repo; logs may go in `logs/` if the project keeps them there, and Playwright output stays in its configured folder | short, lowercase and descriptive, such as `verify-claims.py` or `count-run.json` |

- Only Markdown documents may start with the plan prefix (`r2…`). Source, test, script, fixture, JSON and output files never do.
- Never put scripts, fixtures, test output or snapshots in a documentation directory, and never put a Markdown document in a source directory unless the user asks. Markdown used as test data is a fixture, not a document.
- Create as few artifacts as you can. Extend an existing helper document rather than adding another, and delete temporary artifacts once they have served their purpose, unless an Evidence note points to them. If one must be kept for observation, make sure it can be rebuilt, and name its location in the Evidence note.

## When a group is too big

If a task group (of max 8 tasks) takes more than 3 context compactions, YOU MUST ask yourself if you're not chewing more than we can handle :). Heck, plans change! :). In such a case, the way out is to split the group on the spot, in the plan, into more groups, by appending B, C, D as suffixes to those groups (splitting sub-groups themselves is also allowed). When you do this, add Area Mandatory Reading blocks so you can optimize your context only for the ACTUAL task at hand.

## When you finish

Report, in this order:

- the groups and tasks completed;
- the tasks superseded or skipped, and why, and the decisions you recorded;
- the tests run, with their results;
- the next unchecked group and its difficulty tag.
