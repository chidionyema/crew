"""crew#701 incident, 2026-08-30: four of five research runs (33307986866..33307990565) researched and
graded on MiniMax, then died in record() because MLflow 3.x raises on the `./mlruns` file store
("in maintenance mode ... migrate to a database backend"). The score was computed and lost.

Guard: the tracking URI record() hands MLflow is a database URI, never a file:// one.
"""

import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _mod():
    spec = importlib.util.spec_from_file_location("research_run", ROOT / "science" / "research_run.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_tracking_uri_is_a_database_not_the_retired_file_store(tmp_path):
    uri = _mod().tracking_uri(tmp_path / "mlruns")
    assert uri.startswith("sqlite:///"), uri
    assert not uri.startswith("file:"), uri
    assert str(tmp_path) in uri


def test_record_never_hands_mlflow_a_file_uri():
    src = (ROOT / "science" / "research_run.py").read_text()
    line = next(ln for ln in src.splitlines() if "mlflow.set_tracking_uri(" in ln)
    assert "tracking_uri(mlruns)" in line and "as_uri" not in line, line


def test_workflow_installs_full_mlflow_because_skinny_has_no_sql_store():
    # mlflow-skinny 3.15.2 answers "Model registry functionality is unavailable; got unsupported
    # URI 'sqlite:///...'" (measured 2026-08-30): the SQL backend ships only in the full package.
    wf = (ROOT / ".github" / "workflows" / "science-research.yml").read_text()
    assert '"mlflow>=3"' in wf and "mlflow-skinny" not in wf
