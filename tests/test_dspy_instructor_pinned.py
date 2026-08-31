"""The DSPy + Instructor rollout (founder order 2026-08-31) stays pinned, documented and portable.

Mistake class guarded: a tool installed by hand on one Mac and named nowhere in git dies with
the machine. And the smoke must never hardcode where the estate lives (no zone literal).
"""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_both_packages_are_pinned_in_the_requirements_file():
    text = (ROOT / "requirements-dev.txt").read_text()
    assert "dspy>=" in text, "dspy is not pinned; the install dies with the machine"
    assert "instructor>=" in text, "instructor is not pinned; the install dies with the machine"


def test_the_docs_page_names_the_proof_and_the_key_convention():
    page = (ROOT / "docs" / "tools" / "dspy-instructor.md").read_text()
    assert "scripts/dspy-instructor-smoke.py" in page
    assert "ROUTER_KEY" in page and "ROUTER_URL" in page


def test_the_smoke_names_no_zone_and_no_vendor_address():
    smoke = (ROOT / "scripts" / "dspy-instructor-smoke.py").read_text()
    for literal in ("mumchimp", "api.openai.com", "api.anthropic.com", "api.groq.com"):
        assert literal not in smoke, (
            f"the smoke hardcodes {literal}; it must come from the environment"
        )
