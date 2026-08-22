"""Crew comments carry a machine-readable marker, so the thread is also state."""

from __future__ import annotations

import re
from dataclasses import dataclass

MARKER_RE = re.compile(r"<!--\s*crew\s+(?P<kv>[^>]*?)\s*-->")


def marker(**fields: str) -> str:
    body = " ".join(f"{k}={v}" for k, v in fields.items() if v is not None)
    return f"<!-- crew {body} -->"


@dataclass(frozen=True)
class Entry:
    fields: dict
    body: str
    author: str
    created_at: str

    @property
    def kind(self) -> str:
        return self.fields.get("kind", "")

    @property
    def cp(self) -> str:
        return self.fields.get("cp", "").upper()

    @property
    def role(self) -> str:
        return self.fields.get("role", "")

    @property
    def result(self) -> str:
        return self.fields.get("result", "")


def parse_comments(comments: list[dict]) -> list[Entry]:
    out = []
    for c in comments or []:
        body = c.get("body", "") or ""
        m = MARKER_RE.search(body)
        if not m:
            continue
        fields = {}
        for pair in m.group("kv").split():
            if "=" in pair:
                k, v = pair.split("=", 1)
                fields[k] = v
        author = (c.get("author") or {}).get("login", "?")
        out.append(Entry(fields=fields, body=body, author=author, created_at=c.get("createdAt", "")))
    return out


def latest(entries: list[Entry], *, kind: str, cp: str | None = None) -> Entry | None:
    want = cp.upper() if cp else None
    hits = [e for e in entries if e.kind == kind and (want is None or e.cp == want)]
    return hits[-1] if hits else None
