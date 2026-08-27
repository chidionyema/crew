"""Incident test, crew#405 step 2: a prediction is only a prediction if it predates the outcome.

science-collect runs four times a day; a PR whose first run finished between collects would have
been "predicted" from hindsight, or not at all. The rule: `predict` never writes a row for a PR CI
has already answered, except by copying the comment crew-qa posted before the run finished, and
that row carries the comment's own timestamp, not the collect's.
"""
import json
import pathlib
import sys

SCIENCE = pathlib.Path(__file__).resolve().parents[1] / "science"
sys.path.insert(0, str(SCIENCE))
import foresight  # noqa: E402

PR = {"repo": "crew", "number": 7, "headRefName": "feat/x", "changedFiles": 1, "additions": 1, "deletions": 0,
      "createdAt": "2026-08-27T00:00:00Z", "title": "x", "body": "", "files": [], "mergedAt": None, "closedAt": None}
RUN = {"repo": "crew", "name": "crew qa", "head_branch": "feat/x", "conclusion": "failure",
       "created_at": "2026-08-27T00:05:00Z", "sha": "a", "event": "pull_request"}


def _arm(monkeypatch, tmp_path, comment_body):
    monkeypatch.setattr(foresight, "PREDICTIONS", tmp_path / "predictions.jsonl")
    monkeypatch.setattr(foresight, "_history", lambda: ([RUN], [PR]))
    monkeypatch.setattr(foresight, "dataset", lambda: ([[0.0] * len(foresight.FEATURES)] * foresight.MIN_ROWS,
                                                        [0, 1] * (foresight.MIN_ROWS // 2), None))

    class _M:  # a model that would say RED if anyone asked it after the fact
        named_steps = {"logisticregression": type("c", (), {"coef_": [[0.0] * len(foresight.FEATURES)]})(),
                       "standardscaler": type("s", (), {"mean_": [0.0] * len(foresight.FEATURES),
                                                        "scale_": [1.0] * len(foresight.FEATURES)})()}

        def predict_proba(self, _x):
            return [[0.1, 0.9]]
    monkeypatch.setattr(foresight, "_fit", lambda X, y: _M())
    out = "" if comment_body is None else json.dumps({"body": comment_body, "at": "2026-08-27T00:01:00Z"}) + "\n"
    monkeypatch.setattr(foresight, "_gh", lambda args: out)


def test_hindsight_is_never_written(monkeypatch, tmp_path):
    _arm(monkeypatch, tmp_path, None)
    assert foresight.cmd_predict(None) == 0
    assert not (tmp_path / "predictions.jsonl").exists()


def test_the_pre_run_comment_is_the_row_and_keeps_its_own_time(monkeypatch, tmp_path):
    body = ('<!-- foresight {"step":"first CI run goes GREEN (p_red=0.40)","because":"log_files +0.51",'
            '"p_red":0.402,"predicted_red":false} -->\n**foresight** predicts ...')
    _arm(monkeypatch, tmp_path, body)
    assert foresight.cmd_predict(None) == 0
    rows = foresight._jsonl(tmp_path / "predictions.jsonl")
    assert len(rows) == 1 and rows[0]["source"] == "pr-comment"
    assert rows[0]["at"] == "2026-08-27T00:01:00Z" and rows[0]["predicted_red"] is False
    assert rows[0]["p_red"] == 0.402, "the row is the comment's call, not the model's hindsight (0.9)"
