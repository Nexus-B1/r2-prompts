---
name: split-executing-plan
description: "Ops · Move a plan's unclosed tasks into a new plan with the next prefix, carrying history and re-assessing mandatory reading."
argument-hint: "[plan-file]"
allowed-tools: Bash(python *validate_plan.py*)
model: opus
effort: high
disable-model-invocation: true
---
The plan has become too large. Move all the unclosed tasks from this plan into a new plan in the same prefix family (the next number, following the plan prefix rule below), with a new name which corresponds to what we do. Only the new plan gets a new name; the name of the first plan stays as it is. Additionally, if there is any new work that has been discovered, add it as new groups in that plan, at the appropriate locations and with the appropriate Area Mandatory Reading. Carry over important historical information and re-assess global mandatory reading. Naturally, the first plan will end up to only contain completed work and we should be able to consider it closed...

How to move the work:

- A group with no [X] tasks moves whole. A partly done group keeps its done tasks in the old plan; its remaining tasks move to the new plan under the same group heading, and the old group gets the note "Continued in <new plan>".
- Group numbers continue: moved groups keep their numbers, so references stay valid. Moved tasks keep their IDs (`T-…`); new tasks get IDs with the new plan's prefix.

Where new work comes from (this session may have been compacted, so don't rely on memory alone):

- the plan's checkpoint file, its ASSUMPTION notes and its `> Decision:` records;
- the latest `## Review N` section and its unresolved findings;
- TODOs this plan added in code.

Historical information to carry over:

- ASSUMPTION notes, compaction notes, `> Decision:` records and superseded `[-]` tasks on the moved groups;
- the checkpoint: the new plan starts its own checkpoint file (its first helper letter) from the current state, and the old file stays with the closed plan;
- unresolved review findings.

Closing:

- The new plan's Planning Provenance lists the old plan as its predecessor.
- The old plan gets a closing note directly below its title: "Closed. Remaining work continues in <new plan>."

When you are done, run the plan validator on every resulting plan, `python "${CLAUDE_SKILL_DIR}/../planning-template/scripts/validate_plan.py" <plan file>`, and fix the findings your split caused.

## Plan prefix rule

- If there is a -X- (where X is a number) after the plan prefix, increase X: r2uf1-4- becomes r2uf1-5-.
- Otherwise, add or increase the last number before the first dash: r2csl becomes r2csl2, r2csl1 also becomes r2csl2, r2csl4 becomes r2csl5.
- When you need several new plans, keep counting: r2csl2, r2csl3, r2csl4, and so on.
- If a prefix you need is already taken (there is a r2csl5 already), push the existing plans down by as many numbers as you need. Rename from the highest number downwards so nothing gets overwritten: r2csl6 → r2csl7 first, then r2csl5 → r2csl6.
- After any rename, update every reference to the renamed plans in all repos of the workspace: links in other plans and docs, and source-file headers that reference the plan.
