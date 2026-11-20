---
name: stop-with-handover
description: "Flow · Stop after the current task and update the plan's checkpoint file (for an IDE refresh)."
model: inherit
disable-model-invocation: true
---
Stop once done with the current task, I want to refresh the IDE :).

Before you stop:

- Mark every task you completed and verified `[X]` now, even if its group isn't finished, so no progress is lost. Completed but unverified tasks stay `[ ]` with an indented `> Implemented; verification blocked: <reason>` note.
- Update the plan's checkpoint file, `<prefix>-<letter>-checkpoint.md` next to the plan (create it with the next free helper letter if there is none yet). Record the current state: the tasks done and in progress, the files touched, the uncommitted state, the test status, the next concrete step, the compaction count for this group, and any open questions.
- Make sure the pointer line `> Checkpoint: <file name>` sits directly above the current group's heading.
