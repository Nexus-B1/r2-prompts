---
name: count-plan-tasks
description: "Ops · Count a plan's open and done tasks per group, without reading the plan."
argument-hint: "<plan-file>"
arguments: [plan]
allowed-tools: Bash(awk *)
model: haiku
disable-model-invocation: true
---
Do not read the plan $plan. Report its task counts from the numbers computed below; do not open the file.

```!
awk -v f="$plan" '
BEGIN {
  sub(/^@/, "", f)
  if (f == "" || (getline probe < f) < 0) { print "COUNT-ERROR: no plan named, or cannot read plan file [" f "]"; err = 1; exit }
  close(f); ARGV[1] = f; ARGC = 2
}
/^\{\{(SIMPLE|MEDIUM|HARD|COMPLEX)\}\}([ \t]+\{\{driver:[^}]*\}\})?[ \t]*$/ { tag = $(1) }
/^[ \t]*[-*] \[[ xX-]\]/ {
  state = substr($(0), index($(0), "[") + 1, 1)
  g = "?"
  if (match($(0), /\] (\*\*)?[0-9]+[A-Z]?\./)) { g = substr($(0), RSTART + 2, RLENGTH - 3); sub(/^\*\*/, "", g) }
  if (!(g in seen)) { seen[g] = 1; order[++n] = g; tags[g] = tag }
  if (state == "-") { s[g]++; S++ } else if (state == " ") { o[g]++; O++ } else { d[g]++; D++ }
  last = g
}
/^[ \t]*> Implemented; verification blocked/ { b[last]++; B++ }
END {
  if (err) exit 0
  printf "TOTAL open=%d done=%d blocked=%d superseded=%d\n", O, D, B, S
  for (i = 1; i <= n; i++) { g = order[i]; printf "GROUP %s %s open=%d done=%d blocked=%d superseded=%d\n", g, tags[g], o[g], d[g], b[g], s[g] }
}'
```

How to report:

- Only list items are tasks: lines that start, after any indentation, with `- [ ]`, `- [x]`, `- [X]` or `- [-]`. Prose that mentions `[ ]` is not a task. `[x]` and `[X]` both count as done; `[-]` is superseded, neither open nor done.
- Open tasks with a "verification blocked" note are also counted in `blocked`; report them separately.
- Answer with the total open, done, blocked and superseded, a table of groups (group, difficulty tag, open, done, blocked, superseded), and the next unchecked group: the first group with open tasks, with its difficulty tag.
- If the block above shows COUNT-ERROR or has no TOTAL line, count with Grep in count mode using the same rules, still without reading the file. If no plan was named, ask which plan to count.
