---
name: review-architecture
description: "Plan · Judging architectural review (strengths, risks, coupling, ranked recommendations) with mermaid diagrams."
argument-hint: "[output-file] [\"scope\"]"
arguments: [output, scope]
model: opus
effort: high
disable-model-invocation: true
---
Let's make a thorough architectural review of all this. Use mermaid JS diagrams where applicable. Go deep: for each component, its responsibility, its interfaces and its failure modes, and one mermaid diagram for each non-trivial flow.

"All this": $scope
(If empty: the plan, change or systems discussed in this conversation. If there is nothing to go on, ask.)

Output file: $output
(If empty, give the review in chat instead of writing a file.)

This is a judging review, not documentation (that's `/document-architecture`). Cover:

- strengths worth keeping;
- risks and failure modes;
- coupling and ownership problems;
- recommendations ranked by impact, each with the evidence (file:line) behind it.
