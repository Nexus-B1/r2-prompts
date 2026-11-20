---
name: comment-modified-files
description: "Ops · Bring every git-modified file up to the commenting standard (javaDoc, file headers, business-logic ifs/loops)."
model: sonnet
effort: medium
disable-model-invocation: true
---
I want all files that show up as modified in the current GIT status to be WELL commented, following the commenting standard below.

Which files:

- Every git repository in the workspace, nested ones included.
- Modified, added and untracked files (`git status --porcelain`). Untracked new files usually need comments the most.
- Skip deleted files, generated files, lockfiles, JSON and Markdown.

What to comment: the file header, plus the classes, functions, conditions and loops that the change added or modified (`git diff` shows them; for an untracked file, that is the whole file). Leave the comments of untouched code as they are, even where they fall short of the standard.

Change comments only. Afterwards, review the diff hunk by hunk to confirm that no code changed, then run the repo's type-check or lint if it has one.

## Commenting standard

Applies to source code in any language. JSON, lockfiles, generated files and Markdown are exempt.

- **File headers:** every file starts with a header that relates it to an `archi*.md` architecture document, an `r2*.md` plan, or both. Prefer a link to the specific architecture section that explains how the code works; the plan that delivered the change is the secondary reference. Never invent a reference: find it by searching the architecture docs and plans for the file or its module.
- **Classes and interfaces:** every class and interface has a javaDoc-style header (JSDoc/TSDoc in TypeScript, docstrings in Python) that states its responsibility and the contracts it upholds.
- **Functions:** every function has javaDoc-style docs with clear comments for each argument. An argument comment explains meaning, units and constraints (allowed values, nullability, ownership), not the argument's name and type again. Also document the return value, side effects and thrown errors when there are any.
- **Conditions:** every `if` statement with more than 1 condition is described as business logic: why it exists and what it affects in the bigger picture. Do the same for a single-condition guard that protects an invariant, such as idempotency, authorization or ordering.
- **Loops:** every loop that is not trivial is explained as business logic.
- Comments explain why. Never restate what the syntax already says.
