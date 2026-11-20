"""Check a plan against the mechanical rules of /planning-template.

Rules: ../SKILL.md, sections "Difficulty", "Group format", "Global Mandatory Reading",
"Objective Contract", "Open Questions", "Area Mandatory Reading" and "Completion Conditions".
Delivered by plan testbed/r2skl-skill-feedback-implementation.md (r2-prompts repo), Group 18.
The judgment items of "Final validation" (reading-source quality, tight ranges, triggers)
stay with the planning agent; this script covers only what can be checked mechanically.

Usage:
    python validate_plan.py [--ignore CODE[,CODE...]] <plan.md>

Prints one "line: [code] problem" per finding (line 0 means the whole file) and exits
0 when there is none, 1 when there are findings, 2 on a usage error.

Checks, by code:
    box        every checkbox line is "- [ ]", "- [X]", "- [x]" or "- [-]" (superseded)
    numbering  task numbers n.m match their group and run 1, 2, 3...; groups run in order
    tag        exactly one difficulty tag line, directly above each group's tasks
    driver     {{HARD}} and {{COMPLEX}} carry a valid driver tag; {{SIMPLE}} and {{MEDIUM}} carry none
    size       at most 8 top-level tasks per group
    outcome    **Outcome:** and **Verification:** lines between a group's heading and its tag
    area       each group is covered by an Area block before it; no group is claimed twice
    protocol   the Execution protocol is identical to the template's
    links      local Markdown links resolve
    sections   title, then Global Mandatory Reading first; Consult on Demand, Planning
               Provenance and Completion Conditions in that order; only Review N after them
    contract   an Objective Contract and an Open Questions section exist, in that order,
               between Global Mandatory Reading and Consult on Demand
    task-id    every task has a `T-<plan prefix>-NNN` ID, unique within the plan
    placement  the plan's directory, and its direct subdirectories, hold Markdown documents
               (and images) only: no scripts, fixtures, data or output
"""

import argparse
import re
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "SKILL.md"

TIERS = ("SIMPLE", "MEDIUM", "HARD", "COMPLEX")
DRIVERS = {"complexity", "uncertainty", "complexity + uncertainty"}
DOC_SUFFIXES = {".md", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}

HEADING = re.compile(r"^(#{1,6}) +(.*?)\s*$")
TAG_LINE = re.compile(r"^\{\{(\w+)\}\}(?:[ \t]+\{\{driver:\s*([^}]*?)\s*\}\})?[ \t]*$")
BOX = re.compile(r"^([ \t]*)[-*] \[(.?)\]")
# Task numbers may be bold ("- [X] **1.1** …"), as some existing plans write them.
TASK = re.compile(r"^[-*] \[(.)\] (?:\*\*)?(\d+)([A-Z]?)\.(\d+)\b")
TASK_ID = re.compile(r"`(T-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d{3,})`")
GROUP_IN_HEADING = re.compile(r"\bGroup (\d+)([A-Z]?)\b")
AREA_HEADING = re.compile(r"^Area Mandatory Reading\b")
APPLIES = re.compile(r"^_Applies to Groups? (.+?)\._\s*$")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
REVIEW = re.compile(r"^Review \d+\b")


class Plan:
    """A plan parsed into the line-level facts the checks need.

    Contract: code fences are skipped entirely, so examples inside ``` blocks never count
    as tasks, tags or headings. Line numbers are 1-based, as editors show them.
    """

    def __init__(self, text):
        """Parse plan text.

        Args:
            text: The whole plan, any newline style.
        """
        self.lines = text.splitlines()
        self.live = []  # (line number, text) outside code fences
        fenced = False
        for number, line in enumerate(self.lines, start=1):
            if line.lstrip().startswith("```"):
                fenced = not fenced
                continue
            if not fenced:
                self.live.append((number, line))
        self.groups = self._groups()

    def _groups(self):
        """Split the plan into groups: a difficulty tag line plus the top-level tasks after it.

        Returns:
            Dicts with the tag line, its match, the nearest heading above it (number, text)
            and the task lines (number, match), in plan order. Tasks with no tag line above
            them since the last heading form a group whose "tag" is None.
        """
        groups, heading, current = [], (0, ""), None
        for number, line in self.live:
            head = HEADING.match(line)
            if head:
                heading, current = (number, head.group(2)), None
                continue
            tag = TAG_LINE.match(line)
            if line.startswith("{{") and (tag or line.rstrip().endswith("}}")):
                current = {"tag_line": number, "tag": tag, "raw": line, "heading": heading, "tasks": []}
                groups.append(current)
                continue
            task = TASK.match(line)
            if task:
                # Tasks after a heading but before any tag still belong to a group, so the
                # missing tag is reported once for that group instead of once per task.
                if current is None:
                    current = {"tag_line": None, "tag": None, "raw": "", "heading": heading, "tasks": []}
                    groups.append(current)
                current["tasks"].append((number, task))
        return groups

    def h2(self):
        """Return the level-2 headings as (line number, title) pairs."""
        return [(n, m.group(2)) for n, line in self.live if (m := HEADING.match(line)) and len(m.group(1)) == 2]

    def protocol(self):
        """Return the Execution protocol blockquote as a list of right-stripped lines, or None."""
        for index, line in enumerate(self.lines):
            if line.strip() == "> **Execution protocol**":
                block = []
                for following in self.lines[index:]:
                    if not following.startswith(">"):
                        break
                    block.append(following.rstrip())
                return block
        return None


def group_key(number, suffix):
    """Sort key for a group number such as 5 or 5A."""
    return (int(number), suffix)


def parse_applies(label):
    """Expand an Area label such as "6-10", "5A and 5B" or "1, 3-4" into group keys and ranges.

    Args:
        label: The text between "Applies to Group(s) " and the closing "._".

    Returns:
        A predicate that tells whether a group key (number, suffix) is covered.
    """
    singles, ranges = set(), []
    for part in re.split(r",|\band\b", label):
        part = part.strip()
        span = re.fullmatch(r"(\d+)([A-Z]?)\s*[-–]\s*(\d+)([A-Z]?)", part)
        one = re.fullmatch(r"(\d+)([A-Z]?)", part)
        if span:
            ranges.append((int(span.group(1)), int(span.group(3))))
        elif one:
            singles.add((int(one.group(1)), one.group(2)))
    # A plain number also covers its lettered splits (Group 5 covers 5A and 5B).
    return lambda key: key in singles or (key[0], "") in singles or any(lo <= key[0] <= hi for lo, hi in ranges)


def check_boxes(plan):
    """Findings for checkbox lines with an unknown state."""
    return [(n, "box", f"unknown checkbox state [{m.group(2)}]")
            for n, line in plan.live if (m := BOX.match(line)) and m.group(2) not in (" ", "x", "X", "-")]


def check_groups(plan):
    """Findings for tags, drivers, size, Outcome/Verification lines and numbering.

    Args:
        plan: Parsed plan.

    Returns:
        A list of (line, code, message).
    """
    found, previous = [], None
    for group in plan.groups:
        head_line, head_text = group["heading"]
        anchor = group["tag_line"] or (group["tasks"][0][0] if group["tasks"] else head_line)
        if group["tag"] is None:
            found.append((anchor, "tag", "group has no recognized difficulty tag line above its tasks"))
        else:
            tier, driver = group["tag"].group(1), group["tag"].group(2)
            if tier not in TIERS:
                found.append((anchor, "tag", f"unknown difficulty tag {{{{{tier}}}}}"))
            elif tier in ("HARD", "COMPLEX") and driver not in DRIVERS:
                found.append((anchor, "driver", f"{{{{{tier}}}}} needs a driver tag: complexity, uncertainty, or complexity + uncertainty"))
            elif tier in ("SIMPLE", "MEDIUM") and driver is not None:
                found.append((anchor, "driver", f"{{{{{tier}}}}} takes no driver tag"))
            # Only a blank-free adjacency counts: the tag must sit directly above the first task.
            if not group["tasks"] or group["tasks"][0][0] != group["tag_line"] + 1:
                found.append((anchor, "tag", "difficulty tag is not directly above the group's tasks"))
        if len(group["tasks"]) > 8:
            found.append((anchor, "size", f"{len(group['tasks'])} tasks; the maximum is 8"))
        between = [line for n, line in plan.live if head_line < n < anchor]
        for label in ("**Outcome:**", "**Verification:**"):
            if not any(line.startswith(label) for line in between):
                found.append((anchor, "outcome", f"no {label} line between the group heading and its tag"))
        found += check_numbering(group, head_text, previous)
        if group["tasks"]:
            first = group["tasks"][0][1]
            previous = group_key(first.group(2), first.group(3))
    return found


def check_numbering(group, head_text, previous):
    """Findings for one group's task numbers.

    Args:
        group: One parsed group.
        head_text: The heading above it, which may name "Group N".
        previous: The key of the group before it, or None for the first group.

    Returns:
        A list of (line, code, message).
    """
    found = []
    if not group["tasks"]:
        return found
    first = group["tasks"][0][1]
    key = group_key(first.group(2), first.group(3))
    named = GROUP_IN_HEADING.search(head_text)
    if named and group_key(named.group(1), named.group(2)) != key:
        found.append((group["tasks"][0][0], "numbering", f"tasks are numbered {first.group(2)}{first.group(3)}.n under heading \"{head_text}\""))
    if previous is not None and key <= previous:
        found.append((group["tasks"][0][0], "numbering", "group number does not increase"))
    # Task numbers restart at 1 in every group and must run without gaps or repeats,
    # because executors and reviews refer to tasks by these display numbers.
    for expected, (line, task) in enumerate(group["tasks"], start=1):
        if group_key(task.group(2), task.group(3)) != key:
            found.append((line, "numbering", f"task {task.group(2)}{task.group(3)}.{task.group(4)} sits in group {key[0]}{key[1]}"))
        elif int(task.group(4)) != expected:
            found.append((line, "numbering", f"expected task number {key[0]}{key[1]}.{expected}"))
    return found


def check_areas(plan):
    """Findings for Area coverage: gaps and groups claimed by more than one Area block."""
    areas, found = [], []
    for index, (number, line) in enumerate(plan.live):
        head = HEADING.match(line)
        if head and AREA_HEADING.match(head.group(2)):
            label = next((APPLIES.match(text) for _, text in plan.live[index + 1:index + 4] if APPLIES.match(text)), None)
            if label is None:
                found.append((number, "area", "Area block has no `_Applies to Group(s) …._` label"))
            else:
                areas.append((number, parse_applies(label.group(1))))
    for group in plan.groups:
        if not group["tasks"]:
            continue
        first = group["tasks"][0][1]
        key = group_key(first.group(2), first.group(3))
        line = group["tasks"][0][0]
        claims = [n for n, covers in areas if covers(key)]
        if not any(n < line for n in claims):
            found.append((line, "area", f"group {key[0]}{key[1]} is covered by no Area block above it"))
        if len(claims) > 1:
            found.append((line, "area", f"group {key[0]}{key[1]} is claimed by Area blocks on lines {', '.join(map(str, claims))}"))
    return found


def check_protocol(plan, template_text):
    """Findings when the plan's Execution protocol differs from the template's."""
    expected = Plan(template_text).protocol()
    actual = plan.protocol()
    if expected is None:
        return [(0, "protocol", f"no Execution protocol found in the template {TEMPLATE}")]
    if actual is None:
        return [(0, "protocol", "the plan has no Execution protocol")]
    start = next(i for i, line in enumerate(plan.lines, start=1) if line.strip() == "> **Execution protocol**")
    for offset, (want, got) in enumerate(zip(expected, actual)):
        if want != got:
            return [(start + offset, "protocol", f"differs from the template: expected {want!r}")]
    if len(expected) != len(actual):
        return [(start, "protocol", f"has {len(actual)} lines; the template's has {len(expected)}")]
    return []


def check_links(plan, base):
    """Findings for local Markdown links whose target does not exist.

    Args:
        plan: Parsed plan.
        base: The plan's directory; relative links resolve against it.
    """
    found = []
    for number, line in plan.live:
        for target in LINK.findall(line):
            target = target.strip("<>")
            # Web links, mail links and in-page anchors are not files.
            if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("#"):
                continue
            path = target.split("#", 1)[0].replace("%20", " ")
            if path and not (base / path).exists():
                found.append((number, "links", f"link target not found: {target}"))
    return found


def check_sections(plan):
    """Findings for the title, the order of required sections, and the contract sections."""
    found, titles = [], plan.h2()
    first = next((line for _, line in plan.live if line.strip()), "")
    if not first.startswith("# "):
        found.append((1, "sections", "the plan does not start with a `# ` title"))
    names = [title for _, title in titles]
    if not names or names[0] != "Global Mandatory Reading":
        found.append((titles[0][0] if titles else 1, "sections", "the first section must be Global Mandatory Reading"))
    order = ["Consult on Demand", "Planning Provenance", "Completion Conditions"]
    positions = []
    for name in order:
        if name in names:
            positions.append(names.index(name))
        else:
            found.append((0, "sections", f"missing section: {name}"))
    if positions != sorted(positions):
        found.append((0, "sections", "Consult on Demand, Planning Provenance and Completion Conditions are out of order"))
    if "Completion Conditions" in names:
        for number, title in titles[names.index("Completion Conditions") + 1:]:
            if not REVIEW.match(title):
                found.append((number, "sections", f"only Review sections may follow Completion Conditions, found \"{title}\""))
    end = names.index("Consult on Demand") if "Consult on Demand" in names else len(names)
    contract = [names.index(n) if n in names else None for n in ("Objective Contract", "Open Questions")]
    # Both contract sections must exist, follow Global Mandatory Reading, precede the
    # reference sections, and keep their own order; any miss is one finding.
    if None in contract or not 0 < contract[0] < contract[1] < end:
        found.append((0, "contract", "needs `## Objective Contract` then `## Open Questions`, after Global Mandatory Reading and before Consult on Demand"))
    return found


def check_task_ids(plan):
    """Findings for tasks without a stable ID and for duplicate IDs."""
    found, seen = [], {}
    for group in plan.groups:
        for line, _ in group["tasks"]:
            ident = TASK_ID.search(plan.lines[line - 1])
            if ident is None:
                found.append((line, "task-id", "task has no `T-<plan prefix>-NNN` ID"))
            elif ident.group(1) in seen:
                found.append((line, "task-id", f"ID {ident.group(1)} is also used on line {seen[ident.group(1)]}"))
            else:
                seen[ident.group(1)] = line
    return found


def check_placement(base):
    """Findings for non-document files in the plan's directory or its direct subdirectories."""
    found = []
    for entry in sorted(base.iterdir()):
        if entry.is_file() and entry.suffix.lower() not in DOC_SUFFIXES:
            found.append((0, "placement", f"{entry.name} is not a document; scripts, fixtures and output belong elsewhere"))
        elif entry.is_dir() and not entry.name.startswith("."):
            strays = [f for f in entry.iterdir() if f.is_file() and f.suffix.lower() not in DOC_SUFFIXES]
            if strays:
                found.append((0, "placement", f"{entry.name}/ holds {len(strays)} non-document file(s), such as {strays[0].name}"))
    return found


def validate(plan_path, template_path=TEMPLATE):
    """Run every check on one plan.

    Args:
        plan_path: Path of the plan file.
        template_path: The /planning-template SKILL.md that holds the reference protocol.

    Returns:
        Findings as (line, code, message), sorted by line.
    """
    plan_path = Path(plan_path)
    plan = Plan(plan_path.read_text(encoding="utf-8"))
    found = check_boxes(plan) + check_groups(plan) + check_areas(plan)
    found += check_protocol(plan, Path(template_path).read_text(encoding="utf-8"))
    found += check_links(plan, plan_path.parent) + check_sections(plan)
    found += check_task_ids(plan) + check_placement(plan_path.parent)
    return sorted(found, key=lambda item: item[0])


def main(argv=None):
    """Command-line entry point; returns the exit status."""
    parser = argparse.ArgumentParser(description="Check a plan against /planning-template's mechanical rules.")
    parser.add_argument("plan", help="path of the plan file")
    parser.add_argument("--ignore", default="", help="comma-separated check codes to skip, for accepted exceptions")
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if not Path(args.plan).is_file():
        print(f"no such plan file: {args.plan}")
        return 2
    ignored = {code.strip() for code in args.ignore.split(",") if code.strip()}
    findings = [f for f in validate(args.plan) if f[1] not in ignored]
    for line, code, message in findings:
        print(f"{line}: [{code}] {message}")
    print(f"validate_plan: {len(findings)} finding(s)" + (f", ignoring {', '.join(sorted(ignored))}" if ignored else ""))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
