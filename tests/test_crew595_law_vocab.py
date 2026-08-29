"""crew#595 CP1: bin/law-vocab counts from the live files, and a missing file is NOT RUN."""
import json, os, subprocess, sys

BIN = os.path.join(os.path.dirname(__file__), "..", "bin", "law-vocab")


def run(env, *args):
    return subprocess.run([sys.executable, BIN, *args], capture_output=True, text=True,
                          env={**os.environ, **env})


def test_counts_come_from_the_file(tmp_path):
    f = tmp_path / "laws.md"
    f.write_text("never never fail. Thank you, well done.\n")
    r = run({"LAW_FILES": str(f)}, "--json")
    out = json.loads(r.stdout)
    assert out["punish"]["never"] == 2 and out["punish"]["fail"] == 1
    assert out["reward"]["thank"] == 1 and out["reward"]["well done"] == 1
    assert out["missing"] == []


def test_missing_file_is_not_run_not_silent(tmp_path):
    r = run({"LAW_FILES": str(tmp_path / "absent.md")})
    assert "NOT RUN" in r.stdout and "absent.md" in r.stdout


def test_default_files_print_a_table():
    r = run({})
    assert r.returncode == 0 and "punish" in r.stdout and "reward" in r.stdout
