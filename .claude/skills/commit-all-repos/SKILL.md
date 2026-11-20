---
name: commit-all-repos
description: "Ops · Commit all workspace repos with a message listing the plan files that gained [X] tasks."
model: sonnet
effort: low
disable-model-invocation: true
---
Commit all repos in the workspace with a message that includes all plan file names where we completed [X] tasks.

1. Find the repos: every git repository under the workspace root, nested ones included. List them before doing anything else.
2. Find the plans: in each repo, diff the plan files (`git diff -U0 -- '*.md'`) for lines that changed from `[ ]` to `[X]` or `[x]`. Those plans, and the groups their completed tasks belong to, go in the message.
3. Check what would be committed with `git status --porcelain`. Never commit secrets or `.env` files, `test-cache/`, `logs/`, or files that look unrelated to the completed plans. List any such files and ask before going on.
4. Message format: a subject line of at most 72 characters naming the plans (for example `r2skl: groups 1-5 done`), then a body listing each plan file and the groups completed in it. Mark groups without an `> Evidence:` note as unverified.
5. Never push. Never use `--no-verify`. If a commit hook fails, report it and stop.
