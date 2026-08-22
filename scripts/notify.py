#!/usr/bin/env python3
"""A desktop notification, for when hermes is not the way to reach the founder.

    notify.py "CP2 is green" --title crew

Standard library only. macOS Notification Center, Linux notify-send, or a
webhook if ~/.crew/config names one. Never raises: a notification that fails is
not a reason to fail the run that sent it.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import urllib.request
from pathlib import Path

CONFIG = Path.home() / ".crew" / "config"


def config() -> dict[str, str]:
    out: dict[str, str] = {}
    try:
        for line in CONFIG.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip()
    except OSError:
        pass
    return out


def desktop(title: str, message: str) -> bool:
    system = platform.system()
    if system == "Darwin":
        # osascript takes an AppleScript string. A quote in the message ends it
        # early and the notification silently never appears.
        esc = message.replace("\\", "\\\\").replace('"', '\\"')
        t = title.replace("\\", "\\\\").replace('"', '\\"')
        r = subprocess.run(["osascript", "-e",
                            f'display notification "{esc}" with title "{t}"'],
                           capture_output=True)
        return r.returncode == 0
    if system == "Linux" and subprocess.run(["which", "notify-send"],
                                            capture_output=True).returncode == 0:
        return subprocess.run(["notify-send", title, message]).returncode == 0
    return False


def webhook(url: str, title: str, message: str) -> bool:
    if not url:
        return False
    req = urllib.request.Request(
        url, data=json.dumps({"title": title, "message": message}).encode(),
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=5):
            return True
    except Exception as e:                      # noqa: BLE001 - never fail the caller
        print(f"notify: webhook failed: {e}", file=sys.stderr)
        return False


def main() -> int:
    ap = argparse.ArgumentParser(prog="notify.py")
    ap.add_argument("message")
    ap.add_argument("--title", default="crew")
    ns = ap.parse_args()
    cfg = config()
    sent = (webhook(cfg.get("WEBHOOK_URL", ""), ns.title, ns.message)
            if cfg.get("NOTIFY_FALLBACK") == "webhook"
            else desktop(ns.title, ns.message))
    # Say it on stdout either way, so a log always carries what was sent even
    # when nothing on this machine can pop a window.
    print(f"[{ns.title}] {ns.message}" + ("" if sent else "   (not delivered)"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
