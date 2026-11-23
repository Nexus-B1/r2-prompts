# r2tpl — Planning template example

A dummy plan that shows the structure `/planning-template` produces. The tasks are placeholders; `example-architecture-file.md` stands in for a real architecture document and does not exist in this workspace.

## Global Mandatory Reading

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

| File name | Line Ranges | Description |
| --- | --- | --- |
| `example-architecture-file.md` | `## Ownership and boundaries` (placeholder; no fixed range) | The architecture spine: which component owns which data, and the boundaries no task may cross. Every group needs it because it decides where a change is allowed to live. |
| `example-architecture-file.md` | `## Invariants` (placeholder; no fixed range) | The invariants every change must preserve. They constrain every Verification line in this plan: a group is not done if one of them breaks. |

## Objective Contract

- **Objective:** Show every section and convention of the planning template in a plan that can be read in a minute.
- **Acceptance criteria:**
  1. The plan passes `validate_plan.py` with no findings.
  2. It contains three groups covering three difficulty tiers, including one `{{HARD}}` group with a driver tag and a risk line.
- **Protected contracts:** The verbatim Execution protocol, and the section order the template requires.
- **Execution permissions:** The executor may edit this plan freely. Nothing outside `testbed/` may change, nothing may be committed, and nothing may be sent outside the workspace.

## Open Questions

1. Should `example-architecture-file.md` be created as a real placeholder file, so that the reading tables can link to it? **Recommended:** no. It stays a named placeholder, because a dummy architecture file would be read as real guidance. Affects Groups 1-3.

### Area Mandatory Reading - Example foundations

_Applies to Groups 1-2._

| File name | Line Ranges | Description |
| --- | --- | --- |
| `example-architecture-file.md` | `## Component A` (placeholder; no fixed range) | The contract of the component Groups 1 and 2 change: its public interface and the files it owns. Constrains where the example tasks may write. |

### Group 1 — Example foundation

**Outcome:** The first example change exists and the rest of the plan can build on it.
**Verification:** One focused check, for example a single unit test, that would fail if the change were missing.

{{SIMPLE}}
- [ ] 1.1 `T-r2tpl-001` Example task.
- [ ] 1.2 `T-r2tpl-002` Example task.

### Group 2 — Example pattern across a bounded area

Requires: Group 1.
**Outcome:** The pattern from Group 1 is applied across Component A.
**Verification:** The focused tests for Component A pass.

{{MEDIUM}}
- [ ] 2.1 `T-r2tpl-003` Example task.
- [ ] 2.2 `T-r2tpl-004` Example task.
- [ ] 2.3 `T-r2tpl-005` Example task.

### Area Mandatory Reading - Example integration

_Applies to Group 3._

**Entry gate.** Group 3 needs the Component A interface delivered by Group 2.

- **Contract that must exist:** the public interface named in `example-architecture-file.md` § `## Component A`.
- **How to verify it:** Group 2 is marked `[X]` with an Evidence note, and the interface exists in live code.
- **Tasks that stop if it is absent:** 3.1-3.3.
- **Work that may continue:** none in this plan.
- **Forbidden fallbacks:** do not call Component A's internals directly, and do not stub its interface to make Group 3 pass.

| File name | Line Ranges | Description |
| --- | --- | --- |
| `example-architecture-file.md` | `## Integration contract` (placeholder; no fixed range) | How Component A meets Component B: the shared contract Group 3 must keep consistent on both sides. |

### Group 3 — Example integration across two components

Requires: Group 2.
**Outcome:** Components A and B work together through the integration contract.
**Verification:** An integration test that exercises A and B together, plus the focused tests of both components.
Risk: HIGH — the integration contract is public: review every change to it against `## Invariants` before marking the group done.

{{HARD}} {{driver: uncertainty}}
- [ ] 3.1 `T-r2tpl-006` Example task.
- [ ] 3.2 `T-r2tpl-007` Example task.
- [ ] 3.3 `T-r2tpl-008` Example task.

## Consult on Demand

| Trigger | File name | Start at | Expand only when | Consultation purpose |
| --- | --- | --- | --- | --- |
| The Group 3 integration test fails and the integration contract does not explain why. | `example-architecture-file.md` | `## Known failure modes` (placeholder) | The failure matches none of the listed failure modes. | Find out whether the failure is a known behaviour of the integration. Code and tests outrank this section. |

## Planning Provenance

This table records what shaped the plan. It is not an execution reading queue, it must not be preloaded after a context compaction, it is non-transitive, and its line ranges record planning use, not runtime authority.

| File name | Sections or Line Ranges used while planning | Planning contribution |
| --- | --- | --- |
| [SKILL.md](../.claude/skills/planning-template/SKILL.md) | "Group format", "Difficulty", "Area Mandatory Reading" | The section order, group skeleton, tags and table columns this example shows. |

## Completion Conditions

- Every task is `[X]`, with an Evidence note under each group.
- Every acceptance criterion in the Objective Contract holds.
- Final regression: `python .claude/skills/planning-template/scripts/validate_plan.py testbed/r2tpl-planning-template-example.md` reports no findings.
