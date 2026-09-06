"""crew#85 (2026-08-24, load 255 on 12 cores): the machine was overloaded by concurrent
agent sessions and no session could see the others. The issue's own last comment names the
missing piece: a session-start gate that caps concurrent build/test-heavy sessions.

This test proves the gate both ways (LAW 38): a machine under the ceiling is admitted, and
a machine at the ceiling is refused. The gate reads its inputs from the kernel and `ps`,
never from a hand-typed number, so the test drives the ceiling down to force the refusing
direction rather than fabricating a load reading.
"""
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(REPO_ROOT, "scripts", "session-gate")


def run_gate(*args, env_extra=None):
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable and GATE or GATE, *args],
        env=env,
        capture_output=True,
        text=True,
    )


def test_gate_admits_when_under_the_ceiling():
    # A machine under the ceiling must be admitted. Force a high ceiling so the load
    # reading (whatever it is) is below it, and the heavy-process count is below it.
    result = run_gate(env_extra={"SESSION_GATE_MAX_LOAD_PER_CORE": "1000"})
    assert result.returncode == 0, result.stderr


def test_gate_refuses_when_at_the_ceiling():
    # A machine at the ceiling must be refused. Force the ceiling to zero so no slot can
    # ever be free; the gate must refuse rather than admit.
    result = run_gate(env_extra={"SESSION_GATE_MAX_LOAD_PER_CORE": "0"})
    assert result.returncode == 1, result.stdout
    assert "refusing" in result.stderr


def test_gate_status_prints_the_count_and_ceiling():
    result = run_gate("--status", env_extra={"SESSION_GATE_MAX_LOAD_PER_CORE": "2.0"})
    assert result.returncode == 0, result.stderr
    assert "heavy_sessions=" in result.stdout
    assert "ceiling=" in result.stdout
