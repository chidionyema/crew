"""Incident test, crew#405: foresight labels a PR by the code checks on its first sha, and is BLIND
with no history rather than a model.

Both ways in one run: a red review-gate does not make a PR red (it grades the body, not the
diff); a red qa on the first sha does, even when a later sha went green; a PR whose first run is
still in flight has no label; an empty science/ci/ makes train exit 2 with the word BLIND.
"""
import pathlib
import subprocess
import sys

SCIENCE = pathlib.Path(__file__).resolve().parents[1] / "science"
sys.path.insert(0, str(SCIENCE))
import foresight  # noqa: E402

PR = {"repo": "crew", "number": 1, "headRefName": "feat/x"}


def run(name, sha, conclusion, at, event="pull_request"):
    return {"repo": "crew", "head_branch": "feat/x", "name": name, "sha": sha, "conclusion": conclusion,
            "created_at": at, "event": event}


def test_body_gate_red_is_not_a_red_pr():
    runs = [run("review-gate", "a", "failure", "2026-08-27T00:00:00Z"), run("crew qa", "a", "success", "2026-08-27T00:00:01Z")]
    assert foresight.label(PR, runs) is False


def test_first_sha_red_stays_red_after_a_green_fix():
    runs = [run("crew qa", "a", "failure", "2026-08-27T00:00:00Z"), run("crew qa", "b", "success", "2026-08-27T01:00:00Z")]
    assert foresight.label(PR, runs) is True


def test_in_flight_first_run_has_no_label():
    runs = [run("crew qa", "a", None, "2026-08-27T00:00:00Z")]
    assert foresight.label(PR, runs) is None
    assert foresight.label(PR, []) is None


def test_no_history_is_blind_not_a_model(monkeypatch, tmp_path):
    monkeypatch.setattr(foresight, "CI", tmp_path / "ci")
    assert foresight.cmd_train(None) == 2
    r = subprocess.run([sys.executable, "-c",
                        f"import sys; sys.path.insert(0, {str(SCIENCE)!r}); import foresight as f, pathlib; "
                        f"f.CI = pathlib.Path({str(tmp_path / 'ci')!r}); sys.exit(f.cmd_train(None))"],
                       capture_output=True, text=True, check=False)
    assert r.returncode == 2 and "BLIND" in r.stderr
