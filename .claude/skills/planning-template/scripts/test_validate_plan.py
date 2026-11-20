"""Tests for validate_plan.py: one valid mini-plan, then one mutation per check.

Rules under test: ../SKILL.md (plan format); delivered by plan
testbed/r2skl-skill-feedback-implementation.md (r2-prompts repo), Group 18.
The plans live inline as strings, so no fixtures folder is needed.
Run: python -m unittest discover .claude/skills/planning-template/scripts
"""

import tempfile
import unittest
from pathlib import Path

import validate_plan as vp

PROTOCOL = "\n".join(vp.Plan(vp.TEMPLATE.read_text(encoding="utf-8")).protocol())

VALID = f"""# r2tst: Test plan

## Global Mandatory Reading

{PROTOCOL}

| File name | Line Ranges | Description |
| --- | --- | --- |
| [notes](r2tst-a-notes.md) | 1-2 | Notes. |

## Objective Contract

- **Objective:** test the validator.

## Open Questions

None.

### Area Mandatory Reading - Core
_Applies to Groups 1-2._

| File name | Line Ranges | Description |
| --- | --- | --- |

### Group 1 — First

**Outcome:** one.
**Verification:** `true`.

{{{{SIMPLE}}}}
- [X] 1.1 `T-r2tst-001` Do one.
  - a sub-bullet, not a task
- [-] 1.2 `T-r2tst-002` Do two. — Superseded: not needed.

> Evidence: ok.

### Group 2 — Second

**Outcome:** two.
**Verification:** `true`.

{{{{HARD}}}} {{{{driver: uncertainty}}}}
- [ ] 2.1 `T-r2tst-003` Investigate.

## Consult on Demand

## Planning Provenance

```text
{{{{HARD}}}}
- [ ] 9.9 an example inside a fence, not a task
```

## Completion Conditions

- Final regression: `true`.
"""

EXTRA_TASKS = "".join(f"- [ ] 1.{n} `T-r2tst-1{n:02d}` More.\n" for n in range(3, 11))

# (code expected, text to replace, replacement); each mutation breaks exactly one rule.
MUTATIONS = [
    ("box", "- [-] 1.2", "- [?] 1.2"),
    ("numbering", "- [ ] 2.1 `T-r2tst-003`", "- [ ] 3.1 `T-r2tst-003`"),
    ("numbering", "- [-] 1.2 `T-r2tst-002`", "- [-] 1.3 `T-r2tst-002`"),
    ("tag", "{{SIMPLE}}\n", ""),
    ("tag", "{{SIMPLE}}\n- [X] 1.1", "{{SIMPLE}}\n\n- [X] 1.1"),
    ("driver", "{{HARD}} {{driver: uncertainty}}\n- [ ]", "{{HARD}}\n- [ ]"),
    ("driver", "{{SIMPLE}}\n", "{{SIMPLE}} {{driver: complexity}}\n"),
    ("size", "- [-] 1.2 `T-r2tst-002` Do two. — Superseded: not needed.\n",
     "- [-] 1.2 `T-r2tst-002` Do two. — Superseded: not needed.\n" + EXTRA_TASKS),
    ("outcome", "**Outcome:** one.\n", ""),
    ("area", "_Applies to Groups 1-2._", "_Applies to Group 1._"),
    ("area", "### Group 2 — Second", "### Area Mandatory Reading - Again\n_Applies to Group 2._\n\n### Group 2 — Second"),
    ("protocol", "before the first task", "before the second task"),
    ("links", "(r2tst-a-notes.md)", "(r2tst-z-missing.md)"),
    ("sections", "- Final regression: `true`.\n", "- Final regression: `true`.\n\n## Afterthoughts\n"),
    ("sections", "## Consult on Demand\n\n## Planning Provenance\n", "## Planning Provenance\n\n## Consult on Demand\n"),
    ("contract", "## Objective Contract\n\n- **Objective:** test the validator.\n\n", ""),
    ("task-id", "- [ ] 2.1 `T-r2tst-003` ", "- [ ] 2.1 "),
    ("task-id", "`T-r2tst-002`", "`T-r2tst-001`"),
]


class ValidatePlanTest(unittest.TestCase):
    """Each check fires on its mutation and stays silent on the valid plan."""

    def run_on(self, text, extra_files=()):
        """Write a plan (and optional extra files) to a temporary folder and validate it.

        Args:
            text: Plan text to validate.
            extra_files: Names of extra files to create next to the plan.

        Returns:
            The set of finding codes.
        """
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            (base / "r2tst-a-notes.md").write_text("notes\n", encoding="utf-8")
            for name in extra_files:
                (base / name).parent.mkdir(parents=True, exist_ok=True)
                (base / name).write_text("x\n", encoding="utf-8")
            plan = base / "r2tst-test-plan.md"
            plan.write_text(text, encoding="utf-8")
            return {code for _, code, _ in vp.validate(plan)}

    def test_valid_plan_is_clean(self):
        self.assertEqual(self.run_on(VALID), set())

    def test_each_mutation_is_caught(self):
        for code, old, new in MUTATIONS:
            with self.subTest(code=code, old=old[:30]):
                self.assertEqual(VALID.count(old), 1, "mutation anchor must be unique")
                self.assertIn(code, self.run_on(VALID.replace(old, new)))

    def test_bold_task_numbers_are_tasks(self):
        self.assertEqual(self.run_on(VALID.replace("- [X] 1.1 ", "- [X] **1.1** ")), set())

    def test_placement_flags_scripts_and_fixture_folders(self):
        self.assertIn("placement", self.run_on(VALID, ["helper.py"]))
        self.assertIn("placement", self.run_on(VALID, ["fixtures/plan.json"]))
        self.assertEqual(self.run_on(VALID, ["diagram.png", "older/notes.md"]), set())

    def test_ignore_option_filters_codes(self):
        with tempfile.TemporaryDirectory() as folder:
            plan = Path(folder) / "r2tst-test-plan.md"
            plan.write_text(VALID.replace("`T-r2tst-003` ", ""), encoding="utf-8")
            (Path(folder) / "r2tst-a-notes.md").write_text("notes\n", encoding="utf-8")
            self.assertEqual(vp.main(["--ignore", "task-id", str(plan)]), 0)
            self.assertEqual(vp.main([str(plan)]), 1)


if __name__ == "__main__":
    unittest.main()
