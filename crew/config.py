"""Where the crew's brain lives, for the repo you are standing in."""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from .errors import CrewError

CONFIG_NAME = ".crew.json"
STATE_DIR = ".crew"


@dataclass(frozen=True)
class Config:
    root: Path
    repo: str
    features_dir: str = "features"
    specs_dir: str = "docs/reference/specs"
    bdd_command: str = "behave --no-capture --no-skipped -f plain --tags={tag}"
    bdd_cwd: str = "."
    default_role: str = "engineering"
    extra: dict = field(default_factory=dict)

    @property
    def state_file(self) -> Path:
        return self.root / STATE_DIR / "state.json"


def find_root(start: str | None = None) -> Path:
    here = Path(start or os.getcwd()).resolve()
    for d in [here, *here.parents]:
        if (d / CONFIG_NAME).exists():
            return d
    for d in [here, *here.parents]:
        if (d / ".git").exists():
            return d
    raise CrewError(f"no {CONFIG_NAME} and no .git above {here} — run `crew init` inside a repo")


def repo_from_git(root: Path) -> str:
    out = subprocess.run(
        ["git", "-C", str(root), "remote", "get-url", "origin"],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        raise CrewError(
            f"{root} has no git remote 'origin', so there is no repo to hold the issue.\n"
            f"Set one, or put \"repo\": \"owner/name\" in {CONFIG_NAME}."
        )
    url = out.stdout.strip()
    slug = url.removesuffix(".git").removeprefix("git@github.com:")
    slug = slug.replace("https://github.com/", "").replace("ssh://git@github.com/", "")
    if slug.count("/") != 1:
        raise CrewError(f"cannot read an owner/name out of the origin url: {url}")
    return slug


def load(start: str | None = None) -> Config:
    root = find_root(start)
    data: dict = {}
    f = root / CONFIG_NAME
    if f.exists():
        try:
            data = json.loads(f.read_text())
        except json.JSONDecodeError as e:
            raise CrewError(f"{f} is not valid JSON: {e}") from e
    repo = os.environ.get("CREW_REPO") or data.get("repo") or repo_from_git(root)
    known = {"repo", "features_dir", "specs_dir", "bdd_command", "bdd_cwd", "default_role"}
    return Config(
        root=root,
        repo=repo,
        features_dir=data.get("features_dir", "features"),
        specs_dir=data.get("specs_dir", "docs/reference/specs"),
        bdd_command=data.get("bdd_command", Config.bdd_command),
        bdd_cwd=data.get("bdd_cwd", "."),
        default_role=data.get("default_role", "engineering"),
        extra={k: v for k, v in data.items() if k not in known},
    )


def write(root: Path, data: dict) -> Path:
    f = root / CONFIG_NAME
    f.write_text(json.dumps(data, indent=2) + "\n")
    return f


def read_state(cfg: Config) -> dict:
    if cfg.state_file.exists():
        try:
            return json.loads(cfg.state_file.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def write_state(cfg: Config, state: dict) -> None:
    cfg.state_file.parent.mkdir(parents=True, exist_ok=True)
    cfg.state_file.write_text(json.dumps(state, indent=2) + "\n")


def active_issue(cfg: Config, override: int | None = None) -> int:
    if override:
        return int(override)
    env = os.environ.get("CREW_ISSUE")
    if env:
        return int(env)
    n = read_state(cfg).get("issue")
    if not n:
        raise CrewError("no active issue — pass --issue N, or run `crew use N`")
    return int(n)


def role(override: str | None = None, cfg: Config | None = None) -> str:
    return override or os.environ.get("CREW_ROLE") or (cfg.default_role if cfg else "engineering")
