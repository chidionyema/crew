"""crew#629 CP2: the issue template and the pm-agent role tell the writer to paste the
generated Infra facts block, so no ticket is built against guesses (idp#800 met eight
admission refusals after building)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_the_issue_template_asks_for_generated_infra_facts():
    text = (ROOT / ".github" / "ISSUE_TEMPLATE" / "crew_task.md").read_text()
    assert "bin/idp-ticket-facts" in text
    assert "## 0. Infra facts" in text
    assert text.index("## 0. Infra facts") < text.index("## 1. Origin")


def test_the_pm_agent_role_asks_for_generated_infra_facts():
    text = (ROOT / "roles" / "pm-agent.md").read_text()
    assert "bin/idp-ticket-facts" in text
    assert "## Infra facts" in text
