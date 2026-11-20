---
name: split-fresh-plan
description: "Ops · Split an oversized plan into ~60 KiB parts with incremented prefixes and renamed titles."
argument-hint: "[plan-file]"
allowed-tools: Bash(python *validate_plan.py*)
model: sonnet
effort: high
disable-model-invocation: true
---
Split the plan in as many parts as necessary so that the maximum resulting individual plan size is 60 KiB. This is an already conservative value, it is fine if after a few other post-split adjustments we end up with more, even 80 KiB is fine. Just calculate the initial number of parts by dividing the current size by 60 KiB, rounding up. The first part of the plan stays where it is. The next parts go into new plans whose prefixes follow the plan prefix rule below. The name of each plan should also change to correctly represent what it contains. The name of the first plan should also be updated accordingly.

This skill is for a plan that hasn't started yet. If the plan already has [X] tasks, stop and suggest `/split-executing-plan` instead.

Where to cut:

- Only between groups, preferably where an Area Mandatory Reading block starts. Never inside a group or a reading block.

Every part must work on its own:

- its own title;
- a `## Global Mandatory Reading` section with the Execution protocol copied verbatim from `/planning-template` (`.claude/skills/planning-template/SKILL.md`), plus the global entries that still apply to that part;
- the Area Mandatory Reading block that governs its first group, copied from an earlier part if needed;
- its own Consult on Demand and Planning Provenance rows, keeping only those relevant to its groups.

Numbering and links:

- Group numbers continue across parts (part 2 starts where part 1 ended), so references stay valid. Task IDs (`T-…`) move with their tasks unchanged.
- End each part with "Continues in <next plan>", and start each later part, below its title, with "Continued from <previous plan>".

When you are done, run the plan validator on every resulting plan, `python "${CLAUDE_SKILL_DIR}/../planning-template/scripts/validate_plan.py" <plan file>`, and fix the findings your split caused.

## Plan prefix rule

- If there is a -X- (where X is a number) after the plan prefix, increase X: r2uf1-4- becomes r2uf1-5-.
- Otherwise, add or increase the last number before the first dash: r2csl becomes r2csl2, r2csl1 also becomes r2csl2, r2csl4 becomes r2csl5.
- When you need several new plans, keep counting: r2csl2, r2csl3, r2csl4, and so on.
- If a prefix you need is already taken (there is a r2csl5 already), push the existing plans down by as many numbers as you need. Rename from the highest number downwards so nothing gets overwritten: r2csl6 → r2csl7 first, then r2csl5 → r2csl6.
- After any rename, update every reference to the renamed plans in all repos of the workspace: links in other plans and docs, and source-file headers that reference the plan.
