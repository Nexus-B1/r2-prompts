---
name: document-architecture
description: "Plan · Durable, descriptive architecture docs of the involved systems, with mermaid diagrams, in an archi-*.md file."
argument-hint: "[output-file] [\"scope\"]"
arguments: [output, scope]
model: opus
effort: high
disable-model-invocation: true
---
Let's give future us some help by crafting useful architectural documentation of all involved systems.

Scope: $scope
(If empty: the systems involved in the current plan or conversation. If that's unclear too, ask.)

Output file: $output
(If empty: `archi-<topic>.md` next to the plan being worked on, or ask where to put it. The name must start with `archi` so that source-file headers can link to it.)

Describe the systems as they are; don't judge them. Judging belongs to `/review-architecture`. Use mermaid JS diagrams where applicable. Go deep: for each component, its responsibility, its interfaces and its failure modes, and one mermaid diagram for each non-trivial flow.

Use these sections, with stable headings that source-file headers can link to:

1. Purpose and scope
2. Context diagram
3. Components and ownership
4. Key flows
5. Data model
6. Invariants and contracts
7. Extension points
8. Known risks and debt
9. Sources

Back every claim with file:line references, and state the commit or date the document describes ("as of …").

Mermaid: use `flowchart` for context and components, `sequenceDiagram` for key flows, and `classDiagram` or `erDiagram` for the data model. Quote any label that contains `()`, `:` or `/`; unquoted ones are the most common reason a diagram fails to render.
