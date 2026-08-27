"""crew#455, 2026-08-27: `receivers:` printed BLIND on every science-collect run because
`_default_collector_config()` resolved git's relative `../.git` answer against the process cwd:
from ~/dev/code/crew it named ~/dev/idp/..., from ~/dev/code it named ~/idp/....

Rule: the collector config path is the same from any process cwd, and it sits beside this
repo's main checkout. Rung 4, one incident.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAIN = Path(subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
                           cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()).parent
EXPECT = MAIN.parent / "idp" / "observability" / "otel-collector.yaml"


def _path_from(cwd):
    code = f"import sys; sys.path.insert(0, {str(ROOT / 'science')!r}); import collect; print(collect._default_collector_config())"
    return Path(subprocess.run([sys.executable, "-c", code], cwd=cwd, capture_output=True, text=True,
                               check=True).stdout.strip())


def test_incident_crew455_the_path_is_the_same_from_the_repo_its_parent_and_a_temp_dir(tmp_path):
    seen = {_path_from(ROOT), _path_from(ROOT.parent), _path_from(tmp_path)}
    assert seen == {EXPECT}, seen


def test_incident_crew455_the_old_relative_form_is_cwd_dependent(tmp_path):
    # the refusing half: without --path-format=absolute a main checkout answers `../.git`
    # (measured 2026-08-27 08:44Z from science/); resolving that from another cwd names another
    # directory. A linked worktree answers an absolute path, so the measured answer stands in.
    rel = subprocess.run(["git", "rev-parse", "--git-common-dir"], cwd=ROOT / "science",
                         capture_output=True, text=True, check=True).stdout.strip()
    if Path(rel).is_absolute():
        rel = "../.git"
    old_way = (tmp_path / rel).resolve()
    assert old_way != MAIN / ".git" and not old_way.exists(), old_way
