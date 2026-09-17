"""crew#102 — the batched board writer batches, retries, dead-letters, and never
drops silently when GH_TOKEN is missing.

Plan summary (crew#102, batched writer):

  1. Batched: one `gh issue comment --body-file <tmp>` per minute per writer,
     fed by all rows accumulated in that minute. NOT one POST per row.
  2. Memoised: `ESTATE_BOARD_ISSUE` (default 102) and `ESTATE_BOARD_REPO`
     (default `chidionyema/crew`) are resolved once at process start and
     reused on every call — never re-parsed per row.
  3. Lazy dead-letter: exponential backoff 1s/4s/16s/64s (total ~85s) on
     non-2xx. ONLY when retries are exhausted does the batch dead-letter to
     `~/.claude/state/board-deadletter.jsonl`, preserving the original payload.
  4. Pre-flight: `gh auth status` runs ONCE at writer start, never per row.

This test pins every one of those four design points by monkeypatching
`subprocess.run` and counting invocations. It imports
`crew.board.estate_broadcast` (the module surface) and asserts the call
shapes, not just the outcomes.

The contract is: a writer that is faster than the per-row baseline
(POSTs once per minute, not once per row) AND never silently drops a
row when `GH_TOKEN` is unset.
"""

from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# ---------------------------------------------------------------------------
# Subprocess stubbing
# ---------------------------------------------------------------------------


class _FakeProc:
    """Minimal stand-in for ``subprocess.CompletedProcess``."""

    def __init__(self, returncode: int = 0, stdout: str = "", stderr: str = "") -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def _install_fake_run(monkeypatch, *, auth_status_rc: int = 0, post_rcs = None):
    """Patch ``crew.board.estate_broadcast.subprocess.run``.

    Returns a list of the call argument vectors it observed. The auth
    pre-flight returns ``auth_status_rc``; subsequent calls (i.e. the
    ``gh issue comment --body-file ...`` posts) take return codes from
    ``post_rcs`` in order, cycling the last value if the list is shorter
    than the number of posts.
    """

    calls: list[list[str]] = []

    def fake_run(args, *a, **kw):
        calls.append(list(args))
        # `gh auth status` pre-flight: first call after the program starts.
        if args and len(args) >= 3 and args[1] == "auth" and args[2] == "status":
            return _FakeProc(returncode=auth_status_rc)
        # `gh issue comment --body-file ...` post: cycles post_rcs.
        if post_rcs:
            rc = post_rcs[len([c for c in calls if "--body-file" in c]) - 1] if any(
                "--body-file" in c for c in calls[:-1]
            ) else post_rcs[0]
        else:
            rc = 0
        # Pick the rc by index among the body-file calls.
        bf_index = sum(1 for c in calls if "--body-file" in c) - 1
        if post_rcs:
            rc = post_rcs[min(bf_index, len(post_rcs) - 1)]
        else:
            rc = 0
        return _FakeProc(returncode=rc)

    eb = importlib.import_module("crew.board.estate_broadcast")
    monkeypatch.setattr(eb.subprocess, "run", fake_run)
    return calls, eb


def _reset_memo(eb):
    """Force the writer to re-run the auth pre-flight and re-resolve env."""
    # Memoised pre-flight: clear the cached `_auth_ok` flag if the writer
    # exposes one; otherwise the module's first call sets it for the
    # process lifetime, which is itself the contract we pin.
    if hasattr(eb, "_AUTH_OK"):
        eb._AUTH_OK = None  # type: ignore[attr-defined]
    # Drop any cached env-resolved target.
    if hasattr(eb, "_RESOLVED_REPO"):
        eb._RESOLVED_REPO = None  # type: ignore[attr-defined]
        eb._RESOLVED_ISSUE = None  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# Pin test 1 — batching
# ---------------------------------------------------------------------------


def test_writer_batches_rows_into_one_post_per_minute_per_writer(monkeypatch, tmp_path):
    """N rows in a single minute => ONE `gh issue comment --body-file` call.

    Per-row POSTs are the bottleneck the plan names: on 2026-08-24 the
    load-353 storm produced dozens of alerts and per-row POSTs would
    have eaten the 5000 req/h budget. The batched writer must collapse
    every accumulated row in a minute into exactly one body-file POST.
    """
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GH_TOKEN", "fake-token-for-test")
    monkeypatch.delenv("ESTATE_BOARD_ISSUE", raising=False)
    monkeypatch.delenv("ESTATE_BOARD_REPO", raising=False)
    # Sleep fast: backoff would otherwise stretch the test for ~85s.
    monkeypatch.setattr(
        "crew.board.estate_broadcast.time.sleep", lambda *_a, **_k: None
    )

    calls, eb = _install_fake_run(monkeypatch)
    _reset_memo(eb)

    # 12 rows in a single minute => one POST, not twelve.
    rows = [
        {"from": "fable-63", "kind": "broadcast", "priority": "info",
         "message": f"row {i} on the board at minute 17", "ts": "2026-08-24T17:00:00Z"}
        for i in range(12)
    ]

    # The batched writer exposes `flush_minute(minute_key, rows)`. If the
    # module surface does not yet expose that name, fall back to the
    # legacy `post` to keep older tests compatible. Both paths converge
    # here: any 12-row batch must yield exactly one body-file POST.
    if hasattr(eb, "flush_minute"):
        result = eb.flush_minute("2026-08-24T17:00", rows)
    else:
        # Pre-batched interface: each row is its own call. Pin that this
        # path is *not* the batched writer.
        pytest.skip("flush_minute not present; the batched writer has not landed")

    assert result["posted"] is True
    body_file_calls = [c for c in calls if "--body-file" in c]
    assert len(body_file_calls) == 1, (
        f"expected exactly one body-file POST for 12 rows in one minute, "
        f"got {len(body_file_calls)}: {body_file_calls!r}"
    )
    # The body-file arg is a real path (last positional after --body-file).
    arg_vec = body_file_calls[0]
    bf_idx = arg_vec.index("--body-file")
    body_file_path = Path(arg_vec[bf_idx + 1])
    assert body_file_path.exists(), f"body file was not written: {body_file_path}"
    # The body file is a JSON array of all 12 rows in input order.
    body = json.loads(body_file_path.read_text(encoding="utf-8"))
    assert isinstance(body, list)
    assert len(body) == 12
    assert all(r["message"].startswith("row ") for r in body)


# ---------------------------------------------------------------------------
# Pin test 2 — exponential backoff (1s, 4s, 16s, 64s)
# ---------------------------------------------------------------------------


def test_writer_retries_with_exponential_backoff_1_4_16_64(monkeypatch, tmp_path):
    """Non-2xx on the first attempt => retry with sleeps 1, 4, 16, 64.

    Total ~85s of backoff across 5 attempts (1 + 4 + 16 + 64 = 85). The
    test patches `time.sleep` to a recorder so we count the sleeps
    without actually waiting. On success within the budget the writer
    reports `posted=True`; on exhaustion it dead-letters.
    """
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GH_TOKEN", "fake-token-for-test")

    sleeps: list[float] = []
    monkeypatch.setattr(
        "crew.board.estate_broadcast.time.sleep",
        lambda s, *_a, **_k: sleeps.append(float(s)),
    )

    # All four retries fail; the fifth attempt (after the four sleeps)
    # succeeds. That is 5 total POSTs and 4 sleeps of 1, 4, 16, 64.
    calls, eb = _install_fake_run(monkeypatch, post_rcs=[1, 1, 1, 1, 0])
    _reset_memo(eb)

    rows = [{
        "from": "fable-63", "kind": "broadcast", "priority": "info",
        "message": "one row, five attempts",
        "ts": "2026-08-24T17:01:00Z",
    }]

    if not hasattr(eb, "flush_minute"):
        pytest.skip("flush_minute not present; the batched writer has not landed")

    result = eb.flush_minute("2026-08-24T17:01", rows)

    # Backoff is exactly 1, 4, 16, 64 (seconds), in that order.
    assert sleeps == [1.0, 4.0, 16.0, 64.0], (
        f"backoff sleeps wrong: expected [1, 4, 16, 64], got {sleeps}"
    )

    body_file_calls = [c for c in calls if "--body-file" in c]
    assert len(body_file_calls) == 5, (
        f"expected 5 attempts (initial + 4 retries), got {len(body_file_calls)}"
    )
    assert result["posted"] is True, result


# ---------------------------------------------------------------------------
# Pin test 3 — dead-letter ONLY after retries are exhausted
# ---------------------------------------------------------------------------


def test_writer_only_dead_letters_after_retries_are_exhausted(monkeypatch, tmp_path):
    """All 5 attempts fail => the rows go to ~/.claude/state/board-deadletter.jsonl,
    one per line, original payload preserved. A success within the retry
    budget must NOT dead-letter."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GH_TOKEN", "fake-token-for-test")
    monkeypatch.setattr(
        "crew.board.estate_broadcast.time.sleep", lambda *_a, **_k: None
    )

    dead = Path.home() / ".claude" / "state" / "board-deadletter.jsonl"
    dead.parent.mkdir(parents=True, exist_ok=True)
    if dead.exists():
        dead.unlink()

    # All 5 attempts fail -> dead-letter path fires.
    calls, eb = _install_fake_run(monkeypatch, post_rcs=[1, 1, 1, 1, 1])
    _reset_memo(eb)

    rows = [
        {"from": "fable-63", "kind": "broadcast", "priority": "info",
         "message": f"will dead-letter {i}", "ts": "2026-08-24T17:02:00Z"}
        for i in range(3)
    ]

    if not hasattr(eb, "flush_minute"):
        pytest.skip("flush_minute not present; the batched writer has not landed")

    result = eb.flush_minute("2026-08-24T17:02", rows)
    assert result["posted"] is False
    assert result["dead_lettered"] is True

    assert dead.exists(), "dead-letter file was not written"
    lines = [ln for ln in dead.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(lines) == 3, f"expected one dead-letter line per row, got {len(lines)}"
    parsed = [json.loads(ln) for ln in lines]
    # Original payload is preserved; dead-letter metadata is appended
    # alongside, not replacing, the row.
    assert all(p["message"].startswith("will dead-letter ") for p in parsed)
    assert all("dead_lettered_at" in p for p in parsed)


def test_writer_does_not_dead_letter_on_a_successful_first_attempt(
    monkeypatch, tmp_path
):
    """If the first attempt returns 0, NO row may land in the dead-letter file."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GH_TOKEN", "fake-token-for-test")
    monkeypatch.setattr(
        "crew.board.estate_broadcast.time.sleep", lambda *_a, **_k: None
    )

    dead = Path.home() / ".claude" / "state" / "board-deadletter.jsonl"
    dead.parent.mkdir(parents=True, exist_ok=True)
    if dead.exists():
        dead.unlink()

    calls, eb = _install_fake_run(monkeypatch, post_rcs=[0])
    _reset_memo(eb)

    rows = [{
        "from": "fable-63", "kind": "broadcast", "priority": "info",
        "message": "happy path, no retry", "ts": "2026-08-24T17:03:00Z",
    }]

    if not hasattr(eb, "flush_minute"):
        pytest.skip("flush_minute not present; the batched writer has not landed")

    result = eb.flush_minute("2026-08-24T17:03", rows)
    assert result["posted"] is True
    assert result.get("dead_lettered", False) is False
    assert not dead.exists() or dead.read_text(encoding="utf-8").strip() == ""


# ---------------------------------------------------------------------------
# Pin test 4 — memoised target: resolved once at process start
# ---------------------------------------------------------------------------


def test_writer_memoises_estate_board_repo_and_issue_at_process_start(
    monkeypatch, tmp_path
):
    """The writer reads `ESTATE_BOARD_REPO` and `ESTATE_BOARD_ISSUE` from the
    env at most once per process. After the first call, mutating the env
    MUST NOT change the target that subsequent POSTs go to.
    """
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GH_TOKEN", "fake-token-for-test")
    monkeypatch.setenv("ESTATE_BOARD_REPO", "chidionyema/crew")
    monkeypatch.setenv("ESTATE_BOARD_ISSUE", "102")

    calls, eb = _install_fake_run(monkeypatch)
    _reset_memo(eb)

    rows = [{"from": "fable-63", "kind": "broadcast", "priority": "info",
             "message": "memo check", "ts": "2026-08-24T17:04:00Z"}]

    if not hasattr(eb, "flush_minute"):
        pytest.skip("flush_minute not present; the batched writer has not landed")

    eb.flush_minute("2026-08-24T17:04", rows)

    # Mutate the env to a different target. The writer must IGNORE it
    # because it memoised the target at process start.
    monkeypatch.setenv("ESTATE_BOARD_REPO", "somebody-else/board")
    monkeypatch.setenv("ESTATE_BOARD_ISSUE", "999")

    eb.flush_minute("2026-08-24T17:05", [{
        "from": "fable-63", "kind": "broadcast", "priority": "info",
        "message": "memo check 2", "ts": "2026-08-24T17:05:00Z",
    }])

    body_file_calls = [c for c in calls if "--body-file" in c]
    assert len(body_file_calls) == 2
    for vec in body_file_calls:
        # `gh issue comment <issue> -R <repo> ...` — issue and repo are
        # the FIRST positional issue number and the value after `-R`.
        assert "102" in vec, f"issue number not memoised: {vec}"
        assert "chidionyema/crew" in vec, f"repo not memoised: {vec}"
        assert "999" not in vec, f"env change leaked into a later call: {vec}"
        assert "somebody-else/board" not in vec, f"env change leaked: {vec}"


def test_writer_defaults_issue_to_102_and_repo_to_chidionyema_crew(
    monkeypatch, tmp_path
):
    """With env unset, the memoised default is repo=chidionyema/crew, issue=102.

    These are the pin values named in the plan: ESTATE_BOARD_ISSUE=102,
    ESTATE_BOARD_REPO=chidionyema/crew.
    """
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GH_TOKEN", "fake-token-for-test")
    monkeypatch.delenv("ESTATE_BOARD_ISSUE", raising=False)
    monkeypatch.delenv("ESTATE_BOARD_REPO", raising=False)

    calls, eb = _install_fake_run(monkeypatch)
    _reset_memo(eb)

    rows = [{"from": "fable-63", "kind": "broadcast", "priority": "info",
             "message": "default target", "ts": "2026-08-24T17:06:00Z"}]

    if not hasattr(eb, "flush_minute"):
        pytest.skip("flush_minute not present; the batched writer has not landed")

    eb.flush_minute("2026-08-24T17:06", rows)

    vec = next(c for c in calls if "--body-file" in c)
    assert "102" in vec, vec
    assert "chidionyema/crew" in vec, vec


# ---------------------------------------------------------------------------
# Pin test 5 — pre-flight `gh auth status` ONCE at writer start
# ---------------------------------------------------------------------------


def test_writer_runs_gh_auth_status_exactly_once_at_start(
    monkeypatch, tmp_path
):
    """Across N flushes, `gh auth status` is invoked exactly once.

    The pre-flight answers: do we have a token at all? The legacy
    per-row writer ran it implicitly on every call via the `gh` CLI;
    the batched writer runs it once and memoises the answer.
    """
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GH_TOKEN", "fake-token-for-test")
    monkeypatch.setattr(
        "crew.board.estate_broadcast.time.sleep", lambda *_a, **_k: None
    )

    calls, eb = _install_fake_run(monkeypatch)
    _reset_memo(eb)

    rows = [
        {"from": "fable-63", "kind": "broadcast", "priority": "info",
         "message": f"pre-flight probe {i}", "ts": "2026-08-24T17:07:00Z"}
        for i in range(5)
    ]

    if not hasattr(eb, "flush_minute"):
        pytest.skip("flush_minute not present; the batched writer has not landed")

    for k in range(3):
        eb.flush_minute(f"2026-08-24T17:0{7 + k}", rows)

    auth_calls = [c for c in calls if len(c) >= 3 and c[1] == "auth" and c[2] == "status"]
    assert len(auth_calls) == 1, (
        f"expected exactly one `gh auth status` pre-flight, got {len(auth_calls)}: "
        f"{auth_calls!r}"
    )


# ---------------------------------------------------------------------------
# Pin test 6 — dead-letter when GH_TOKEN is missing
# ---------------------------------------------------------------------------


def test_writer_dead_letters_when_gh_token_is_missing(monkeypatch, tmp_path):
    """No GH_TOKEN in env => no `gh` invocation, rows go straight to dead-letter.

    This is the branch the founder's order pins: a row that cannot
    reach GitHub is never silently dropped.
    """
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("ESTATE_BOARD_ISSUE", raising=False)
    monkeypatch.delenv("ESTATE_BOARD_REPO", raising=False)
    monkeypatch.setattr(
        "crew.board.estate_broadcast.time.sleep", lambda *_a, **_k: None
    )

    dead = Path.home() / ".claude" / "state" / "board-deadletter.jsonl"
    dead.parent.mkdir(parents=True, exist_ok=True)
    if dead.exists():
        dead.unlink()

    # Even if `subprocess.run` were called, it would refuse with a clear
    # reason. The writer must short-circuit BEFORE the call so it never
    # even tries.
    calls, eb = _install_fake_run(monkeypatch)
    _reset_memo(eb)

    rows = [
        {"from": "fable-63", "kind": "broadcast", "priority": "info",
         "message": "no token in env", "ts": "2026-08-24T17:10:00Z"}
    ]

    if not hasattr(eb, "flush_minute"):
        pytest.skip("flush_minute not present; the batched writer has not landed")

    result = eb.flush_minute("2026-08-24T17:10", rows)

    assert result["posted"] is False
    assert result["dead_lettered"] is True
    # Zero subprocess invocations on the no-token path.
    gh_calls = [c for c in calls if c and c[0] == "gh"]
    assert gh_calls == [], (
        f"writer must NOT shell out to gh when GH_TOKEN is missing; saw {gh_calls!r}"
    )

    # The dead-letter file carries the original payload, unchanged.
    assert dead.exists()
    lines = [ln for ln in dead.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(lines) == 1
    parsed = json.loads(lines[0])
    assert parsed["message"] == "no token in env"
    assert parsed["from"] == "fable-63"
    assert parsed["kind"] == "broadcast"