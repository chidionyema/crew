"""Incident crew#558, 2026-08-28: the one domain that could say what the cluster is RUNNING was
answered by nobody, on every machine an agent works on.

`cluster_live` shelled out to `kubectl --kubeconfig ~/.kube/oke-estate`. That kubeconfig execs
`oci ce cluster generate-token` with no `--profile`; `~/.oci/config` carries no DEFAULT profile,
and both profiles it does carry authenticate with a browser session that expires in hours. So the
domain was BLIND, `verdicts.json` carried a written allowance saying so, and all 233 `cluster`
producers beside it are a yaml walk of what git DECLARES -- never what runs.

The cluster already publishes what it runs: an in-cluster CronJob writes a receipt to Object
Storage every 15 minutes from the node's instance principal, and idp's oke-check workflow prints
that body into its job log. The rule this test holds: the discoverer reads the cluster through
that receipt using a GitHub token and nothing else -- no kubectl, no kubeconfig, no OCI identity --
and every way it can fail names the reason instead of returning an empty list.
"""

from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from science import producers  # noqa: E402


def _stamp(hours_ago: float) -> str:
    at = datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=hours_ago)
    return at.strftime("%Y-%m-%dT%H:%M:%SZ")


def _receipt(hours_ago: float = 1.0) -> dict:
    """The shape idp bin/idp-cluster-state --json actually prints (run 33160603986, 2026-08-28)."""
    return {
        "at": _stamp(hours_ago),
        "flux": [
            {"kind": "HelmRelease", "ns": "monitoring", "name": "k8s-infra", "ready": "True"},
            {"kind": "Kustomization", "ns": "flux-system", "name": "apps", "ready": "False"},
        ],
        "flux_not_ready": 1,
        "daemonsets": [{"ns": "kube-system", "name": "proxymux-client", "ready": 2, "desired": 2}],
        "policy_exceptions": [{"ns": "backstage", "name": "allow-catalogue", "policies": "x"}],
        "nodes": [{"name": "10.0.10.5", "ready": "True", "version": "v1.31.1"}],
        "pods_total": 115,
    }


def _log(body: dict | None, noise: str = "checking flux") -> str:
    """A job log: every line is `<rfc3339> <content>`, and the receipt is one very long line."""
    lines = [f"2026-08-28T09:45:01.0000000Z {noise}"]
    if body is not None:
        lines.append("2026-08-28T09:45:03.0000000Z " + json.dumps(body))
    lines.append("2026-08-28T09:45:04.0000000Z done")
    return "\n".join(lines) + "\n"


class _Fake:
    """A `gh` that answers the three calls the discoverer makes, and records every argv."""

    def __init__(self, logs_by_run: dict[int, str | None]):
        self.logs = logs_by_run
        self.calls: list[list[str]] = []

    def run(self, cmd, capture_output=True, text=True, timeout=None, check=False):
        self.calls.append(list(cmd))
        out, rc = "", 0
        if cmd[:3] == ["gh", "run", "list"]:
            out = json.dumps([{"databaseId": rid, "createdAt": _stamp(1)} for rid in self.logs])
        elif cmd[:2] == ["gh", "api"] and cmd[2].endswith("/jobs"):
            rid = int(cmd[2].split("/runs/")[1].split("/")[0])
            out = json.dumps({"jobs": [{"id": rid * 10, "name": producers.CLUSTER_RECEIPT_JOB}]})
        elif cmd[:2] == ["gh", "api"] and cmd[2].endswith("/logs"):
            rid = int(cmd[2].split("/jobs/")[1].split("/")[0]) // 10
            log = self.logs[rid]
            if log is None:
                rc, out = 1, "gh: Not Found"
            else:
                out = log
        else:
            raise AssertionError(f"the discoverer ran a command it should not: {cmd}")
        return type("R", (), {"returncode": rc, "stdout": out, "stderr": ""})()


def _install(monkeypatch, logs_by_run) -> _Fake:
    fake = _Fake(logs_by_run)
    monkeypatch.setattr(producers.subprocess, "run", fake.run)
    return fake


def test_a_fresh_receipt_becomes_live_cluster_producers(monkeypatch):
    _install(monkeypatch, {900: _log(_receipt())})
    keys = {p["key"]: p for p in producers.cluster_live()}
    assert keys.keys() == {
        "cluster_live/monitoring/HelmRelease/k8s-infra",
        "cluster_live/flux-system/Kustomization/apps",
        "cluster_live/kube-system/DaemonSet/proxymux-client",
        "cluster_live/backstage/PolicyException/allow-catalogue",
        "cluster_live/-/Node/10.0.10.5",
    }
    node = keys["cluster_live/-/Node/10.0.10.5"]
    assert node["measures"], "a Node with no measures is a producer nobody can grade"
    assert "kubelet_version" in node["measures"]
    assert "gh api" in node["evidence"] and "receipt at" in node["evidence"]


def test_no_kubectl_kubeconfig_or_oci_is_on_the_path(monkeypatch):
    """The whole point: this must answer from a machine that has never held an OCI credential."""
    fake = _install(monkeypatch, {900: _log(_receipt())})
    producers.cluster_live()
    assert fake.calls, "nothing ran at all"
    for cmd in fake.calls:
        assert cmd[0] == "gh", f"the discoverer shelled out to {cmd[0]}, not gh"
        joined = " ".join(cmd)
        assert "kubectl" not in joined and "oci" not in joined.split()
        assert str(producers.OKE_KUBECONFIG) not in joined


def test_a_run_whose_log_carries_no_body_is_skipped_and_the_next_is_tried(monkeypatch):
    """`--json` prints the body on two paths only; any other FAIL exits before it. That is a run
    with no receipt, not an error -- the newest run is often exactly this one."""
    fake = _install(monkeypatch, {900: _log(None), 899: _log(None, "FAIL stale receipt"),
                                  898: _log(_receipt())})
    keys = {p["key"] for p in producers.cluster_live()}
    assert "cluster_live/-/Node/10.0.10.5" in keys
    assert any("/jobs/8980/logs" in " ".join(c) for c in fake.calls), "it never reached run 898"


def test_no_readable_body_anywhere_names_the_reason_and_never_returns_empty(monkeypatch):
    _install(monkeypatch, {900: _log(None), 899: _log(None)})
    with pytest.raises(RuntimeError) as e:
        producers.cluster_live()
    msg = str(e.value)
    assert "no receipt body" in msg and producers.CLUSTER_RECEIPT_WORKFLOW in msg


def test_a_stale_receipt_is_refused_rather_than_reported_as_what_runs_now(monkeypatch):
    """A receipt from three days ago lists a world that may not exist. Saying so is the job."""
    old = producers.CLUSTER_RECEIPT_MAX_AGE_H
    _install(monkeypatch, {900: _log(_receipt(hours_ago=old + 12))})
    with pytest.raises(RuntimeError) as e:
        producers.cluster_live()
    assert "old" in str(e.value) and "not what runs now" in str(e.value)


def test_the_written_allowance_that_let_this_domain_stay_blind_is_gone():
    """The deletion is the proof. While `blind_allowed` names cluster_live, datamap --check stays
    GREEN with the domain answering nothing -- which is how it went unnoticed since crew#345."""
    reg = json.loads((ROOT / "science" / "verdicts.json").read_text())
    assert "cluster_live" not in reg.get("blind_allowed", {})
