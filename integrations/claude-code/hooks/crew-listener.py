#!/usr/bin/env python3
"""Wire A: notice the founder describing work, without him typing a command.

A Claude Code `UserPromptSubmit` hook. It reads the prompt, decides whether it
describes work, and when it does it writes a brief and prints one line back into
the conversation asking for pm-agent. Stdout from this hook is added to Claude's
context, which is the whole mechanism — the hook cannot spawn a subagent itself.

    echo "wire the lease into the test runner" | crew-listener.py --dry-run
    OPEN  an instruction to change something: "wire"

    echo "what should I read first?" | crew-listener.py --dry-run
    SKIP  a question, it is asking rather than asking for

Install it by adding to .claude/settings.json:

    {"hooks": {"UserPromptSubmit": [{"hooks": [{"type": "command",
      "command": "integrations/claude-code/hooks/crew-listener.py"}]}]}}

The rejected design opened an issue on any sentence containing "should" or
"fix". "what should I read first?" and "that fix looks fine" both match it. A
queue full of noise is worse than no queue, and he stops reading it either way,
so the veto list below is longer than the trigger list on purpose.

Wrong in the safe direction. A missed request costs him one command. A false
open costs him an issue he has to close, and his trust in the queue.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

# An instruction to change the world. Present tense, aimed at a deliverable.
DO = r"""
    add|build|wire|write|create|make|implement|set\s+up|hook\s+up|
    fix|patch|repair|correct|
    remove|delete|drop|strip|
    change|update|migrate|move|rename|refactor|rewrite|port|
    deploy|ship|release|publish|push|merge|
    automate|script|generate|
    document|record|track|
    finish|complete|continue|resume|carry\s+on|crack\s+on|
    handle|support|accept|allow|enable|disable|extend|cover|guard|
    install|configure|wire\s+up|connect|integrate|
    get\s+.{0,20}\bdone\b|do\s+(the|all|it|that|this|them)\b
"""
DOING = re.compile(rf"\b({DO})\b", re.X | re.I)

# He is not asking for work; he is asking a question, or reacting to one.
# A wh-word opening is a question whether or not he typed the question mark.
ASKING = re.compile(r"""
    ^\s*(what|why|how|which|where|when|who|whose|should\s+(i|we|it|that))\b
""", re.X | re.I)

# An auxiliary opening is only a question when it ends like one. "do the rest"
# is an instruction; "do you know?" is not, and the mark is what separates them.
AUX = re.compile(r"""
    ^\s*(is|are|was|were|does|do|did|can|could|will|would|has|have|had|
         any|anything|anyone)\b
""", re.X | re.I)

REACTING = re.compile(r"""
    ^\s*(thanks?|thank\s+you|ta|cheers|ok|okay|k|yes|no|nope|yep|sure|
         got\s+it|understood|noted|nice|good|great|perfect|cool|lovely|
         lgtm|looks?\s+(good|fine|right|ok)|that\s+(is|s|'s)\s+(fine|good|right)|
         agreed|correct|right|exactly|indeed)\b
""", re.X | re.I)

# A remark about something that already exists, not a request to change it.
ABOUT = re.compile(r"^\s*(that|this|those|these|it|the)\b.*\b(looks?|seems?|reads?|is|was)\b",
                   re.I)

STATUS = re.compile(r"""
    ^\s*(status|where\s+(are|is)|how\s+many|how\s+much|what\s+is\s+left|
         are\s+we|is\s+it\s+done|show\s+me|list|print|read|open|tell\s+me)\b
""", re.X | re.I)


def decide(text: str) -> tuple[bool, str]:
    """(open an issue, the reason in one line).

    Vetoes run first and every one of them wins. A sentence that both asks a
    question and names a verb is a question — "what should I fix first?" is the
    exact shape the rejected design got wrong.
    """
    t = (text or "").strip()
    if not t:
        return False, "nothing to read"
    first = t.splitlines()[0]

    # An acknowledgement only vetoes when it is the whole message. "ok get all
    # the rest done" is a yes followed by an instruction, and the instruction is
    # the part that matters.
    ack = REACTING.match(first)
    if ack and not DOING.search(first[ack.end():]):
        return False, "an acknowledgement, not a request"
    if ASKING.match(first) or first.rstrip().endswith("?"):
        return False, "a question, it is asking rather than asking for"
    if AUX.match(first) and not DOING.search(first):
        return False, "a question, it is asking rather than asking for"
    if STATUS.match(first):
        return False, "a request to read state, which `crew status` already answers"
    if ABOUT.match(first) and not DOING.match(first):
        return False, "a remark about something that exists, not an instruction"

    m = DOING.search(t)
    if not m:
        return False, "no instruction to change anything"
    if len(t) < 12:
        return False, "too short to be a brief"
    return True, f'an instruction to change something: "{m.group(0).lower()}"'


def read_prompt(raw: str) -> str:
    """Claude Code sends a JSON payload; a person piping a sentence sends text."""
    try:
        payload = json.loads(raw)
    except ValueError:
        return raw
    if isinstance(payload, dict):
        return str(payload.get("prompt") or payload.get("user_prompt") or raw)
    return raw


def write_brief(text: str) -> Path:
    # .crew/ is gitignored: the brief belongs to one checkout, not to the repo.
    d = ROOT / ".crew"
    d.mkdir(exist_ok=True)
    f = d / f"brief-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}.md"
    f.write_text(f"# Brief\n\nIn his words, unedited:\n\n{text.strip()}\n")
    return f


def main() -> int:
    ap = argparse.ArgumentParser(prog="crew-listener.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true",
                    help="print the decision, write nothing")
    ns = ap.parse_args()

    text = read_prompt(sys.stdin.read())
    work, why = decide(text)

    if not work:
        if ns.dry_run:
            print(f"SKIP  {why}")
        return 0

    if ns.dry_run:
        print(f"OPEN  {why}")
        return 0

    brief = write_brief(text)
    # This line lands in Claude's context. It is a request to a person or an
    # agent, not a command being run, because a hook that opened a GitHub issue
    # by itself would open one for every false positive with nobody in the way.
    print(f"crew: that reads as work — {why}. The brief is at "
          f"{brief.relative_to(ROOT)}. Run the pm-agent subagent on it, or "
          f"`crew plan {brief.relative_to(ROOT)} --author chidionyema`.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
