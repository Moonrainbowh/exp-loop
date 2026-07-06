#!/usr/bin/env python3
"""Static maintenance checks for the exp-loop skill."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
REFERENCES = ROOT / "references"
REQUIRED_FILES = [
    SKILL,
    ROOT / "agents" / "openai.yaml",
    REFERENCES / "experiment-records.md",
    REFERENCES / "pressure-scenarios.md",
    REFERENCES / "test-results.md",
]

PRIVATE_PATTERNS = [
    "/" + "mnt" + "/" + "e",
    "260" + "413",
    "10" + "阶段",
    r"\b" + "obs" + "idian" + r"\b",
    r"\b" + "con" + "da" + r"\b",
    "torch" + "_gpu",
    "Windows" + "11",
    "ss" + "cls",
    "科研" + "灵感",
    "管网" + "智能造腔",
    "C:" + r"\\Users",
]

DESCRIPTION_TERMS = [
    "machine-learning experiments",
    "baseline comparison",
    "HPO",
    "ablation",
    "experiment tracking",
    "failed trial diagnosis",
    "model selection",
]

SKILL_REQUIRED_TERMS = [
    "## Preflight Gate",
    "Do not run an experiment until these are known",
    "## Leakage And Reproducibility Gate",
    "## Tool Boundary",
    "## Next-Step Review Gate",
    "Use an extra agent or independent reviewer when available",
    "Do not continue until the review verdict is `approve`, `revise`, or `escalate`",
    "## Decision Contract",
    "references/experiment-records.md",
    "references/pressure-scenarios.md",
    "references/test-results.md",
]

PRESSURE_REQUIRED_TERMS = [
    "## Scenario 6: User Pushes To Expand The Next Step Without Review",
    "next-step reviewer",
    "Failure this catches:",
]

RECORD_REQUIRED_TERMS = [
    "Code state:",
    "Data state:",
    "Environment:",
    "Resource budget:",
    "Validation policy:",
    "Known contamination risks:",
    "Next-step review:",
    "reviewer verdict: approve/revise/escalate",
    "Failure class: environment/data/config/code/resource/metric/unknown",
    "## Contamination Remediation",
    "## HPO Reconstruction Without Writes",
    "## Tiny Gain Rule",
]

TEST_REQUIRED_TERMS = [
    "Status: second cycle complete",
    "Final reviewer verdict: `ready`",
    "Subagent evidence handles:",
    "| 3 | yes, second-cycle pass | none |",
    "| 4 | yes, second-cycle pass | none |",
    "| 5 | yes, second-cycle pass | none |",
    "| 6 | documented maintenance extension; full retest pending | none |",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"missing required file: {path.relative_to(ROOT)}")


def check_required_files() -> None:
    for path in REQUIRED_FILES:
        if not path.exists():
            fail(f"missing required file: {path.relative_to(ROOT)}")


def check_frontmatter(skill_text: str) -> None:
    match = re.match(r"---\n(.*?)\n---\n", skill_text, re.S)
    if not match:
        fail("SKILL.md frontmatter missing")
    frontmatter = match.group(1)
    if "name: exp-loop" not in frontmatter:
        fail("frontmatter name must be exp-loop")
    desc_match = re.search(r"^description:\s*(.+)$", frontmatter, re.M)
    if not desc_match:
        fail("frontmatter description missing")
    description = desc_match.group(1)
    if not description.startswith("Use when "):
        fail("description must start with 'Use when '")
    for term in DESCRIPTION_TERMS:
        if term not in description:
            fail(f"description missing trigger term: {term}")


def check_terms(text: str, terms: list[str], label: str) -> None:
    for term in terms:
        if term not in text:
            fail(f"{label} missing required text: {term}")


def check_private_paths() -> None:
    for path in [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in PRIVATE_PATTERNS:
            if re.search(pattern, text, re.I):
                fail(f"private path or environment marker in {path.relative_to(ROOT)}: {pattern}")


def main() -> int:
    check_required_files()
    skill_text = read(SKILL)
    pressure_text = read(REFERENCES / "pressure-scenarios.md")
    records_text = read(REFERENCES / "experiment-records.md")
    tests_text = read(REFERENCES / "test-results.md")
    check_frontmatter(skill_text)
    check_terms(skill_text, SKILL_REQUIRED_TERMS, "SKILL.md")
    check_terms(pressure_text, PRESSURE_REQUIRED_TERMS, "pressure-scenarios.md")
    check_terms(records_text, RECORD_REQUIRED_TERMS, "experiment-records.md")
    check_terms(tests_text, TEST_REQUIRED_TERMS, "test-results.md")
    check_private_paths()
    print("exp-loop skill checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
