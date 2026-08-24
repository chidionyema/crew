#!/usr/bin/env bash
# Every language this repo writes has a checker in front of it, and it runs on the diff.
#
# WHY THIS EXISTS. Founder, 2026-08-24: "almost every python script we write has defects",
# "we burn time fixing and refixing these script issues", "we don't have engineering
# standards at all", "sort it out once so this class of problems never occurs again".
# He is right, and the estate had the receipt: measured on origin/main that morning,
# 34 Python files and 6,173 lines with no linter or type checker ever run over any of
# them. ruff found 121 findings and pyright found 24 errors in its *basic* mode -- 13 of
# those being attribute access on a value that can be None, which is a crash waiting for
# the right input. Nothing failed, because nothing was looking.
#
# WHAT IS CHECKED, AND BY WHAT. Nothing here is hand-rolled; each is the mature tool for
# its language (LAW 43, R6).
#
#   Python  ruff        lint, configured in pyproject.toml
#   Python  pyright     types
#   Shell   shellcheck  the standard shell analyser. 17 files, 1,081 lines, and it was
#                       already clean at `warning` -- the shell here is in better shape
#                       than the Python, which is worth knowing before anyone rewrites it.
#   Actions actionlint  GitHub workflow syntax, expressions, and shellcheck over `run:`
#
# Not covered, and named so nobody assumes otherwise: the single `.rego` file (`opa check`
# is the tool when a second one appears) and Markdown.
#
# WHY IT IS A RATCHET AND NOT A SWEEP. A gate that failed on all 121 pre-existing findings
# would fail every branch in the estate from the moment it merged, including branches that
# touched none of them. Every session would learn within a day to ignore a red check, and
# then nothing is enforced at all -- which is where we already were. So the line is the
# diff: what you wrote or edited on this branch meets the standard, what you did not touch
# is counted and printed. The debt only goes down, and it goes down in the lane that owns
# each file.
#
# exit 0 pass | exit 1 a changed file breaks the standard | exit 2 CANNOT RUN
set -uo pipefail
cd "${CREW_ROOT:-$(git rev-parse --show-toplevel)}" || exit 2

# A worktree has no .venv of its own -- it shares the checkout it was cut from -- and the
# first run of this gate reported BLIND from inside one while ruff sat installed two
# directories away. So the main checkout is searched too, via the common git dir.
MAIN="$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null)"; MAIN="${MAIN%/.git}"
find_tool() {
  for c in "${CREW_VENV:-}/bin/$1" "./.venv/bin/$1" "$MAIN/.venv/bin/$1" "$(command -v "$1" 2>/dev/null)"; do
    [ -n "$c" ] && [ -x "$c" ] && { printf '%s' "$c"; return 0; }
  done
  return 1
}
RUFF="$(find_tool ruff || true)"
PYRIGHT="$(find_tool pyright || true)"
SHELLCHECK="$(find_tool shellcheck || true)"
ACTIONLINT="$(find_tool actionlint || true)"
PY="$(find_tool python || true)"; [ -n "$PY" ] || PY="$(command -v python3)"

[ -f pyproject.toml ] || { echo "BLIND: no pyproject.toml, so no Python standard to check against."; exit 2; }

# The base is where this branch left main, not main's tip: a file somebody else changed
# after I branched is not mine to answer for.
BASE="$(git merge-base HEAD origin/main 2>/dev/null || git merge-base HEAD main 2>/dev/null || true)"
if [ -z "$BASE" ]; then
  # The tempting fallback is "treat every tracked file as changed". That fails every
  # branch on the pre-existing debt the moment a shallow clone hides the base -- a guard
  # refusing correct work, which is an outage (LAW 38). A gate that cannot tell what
  # changed does not get to guess.
  echo "BLIND: no merge base with main. On a runner that means a shallow checkout;"
  echo "set \`fetch-depth: 0\` on actions/checkout. Refusing to guess which files are new."
  exit 2
fi

# Committed on the branch, plus uncommitted work -- otherwise the gate passes on the
# laptop and fails in CI, which teaches people the gate is noise.
changed_files() {
  { git diff --name-only --diff-filter=ACMR "$BASE"...HEAD 2>/dev/null
    git diff --name-only --diff-filter=ACMR HEAD 2>/dev/null
    git ls-files -o --exclude-standard
  } | grep -v '^$' | sort -u | while read -r f; do [ -f "$f" ] && echo "$f"; done
}
ALL="$(changed_files)"
is_shell() {
  case "$1" in *.sh|*.bash) return 0;; esac
  head -c 60 "$1" 2>/dev/null | grep -qE '^#!.*(bash|/sh|zsh)'
}
PY_FILES="$(printf '%s\n' "$ALL" | grep '\.py$' || true)"
SH_FILES="$(printf '%s\n' "$ALL" | while read -r f; do [ -n "$f" ] && is_shell "$f" && echo "$f"; done)"
WF_FILES="$(printf '%s\n' "$ALL" | grep -E '^\.github/workflows/.*\.ya?ml$' || true)"

# The whole-repo number, printed on every run whatever the verdict. A debt nobody prints
# is a debt nobody pays (LAW 28).
if [ -n "$RUFF" ]; then
  DEBT="$("$RUFF" check --no-cache --quiet --output-format concise . 2>/dev/null | grep -c ':' || true)"
  echo "repo-wide ruff findings on all Python: ${DEBT}   (reported, not enforced)"
fi

count() { printf '%s\n' "$1" | grep -c . || true; }
echo "changed on this branch: $(count "$PY_FILES") python, $(count "$SH_FILES") shell, $(count "$WF_FILES") workflow"
if [ -z "$PY_FILES$SH_FILES$WF_FILES" ]; then
  echo "nothing this gate checks was added or changed. Nothing to enforce."
  exit 0
fi
echo

rc=0
# A real failure outranks a blind spot: once something is genuinely broken, a missing tool
# must not soften the verdict to BLIND. The first draft of this gate did exactly that.
note() { if [ "$1" -eq 1 ]; then rc=1; elif [ "$1" -ne 0 ] && [ "$rc" -eq 0 ]; then rc="$1"; fi; }

if [ -n "$PY_FILES" ]; then
  echo "--- ruff, on $(count "$PY_FILES") changed python file(s) ---"
  if [ -z "$RUFF" ]; then
    echo "BLIND: no ruff. \`.venv/bin/pip install ruff pyright\`, or add it to the runner."
    note 2
  elif printf '%s\n' "$PY_FILES" | xargs "$RUFF" check --no-cache --output-format concise; then
    echo "clean."
  else
    note 1
    echo
    echo "Fix, do not silence. \`ruff check --fix\` handles the mechanical ones; a rule that"
    echo "is genuinely wrong for a line takes a \`# noqa: RULE\` with the reason beside it."
  fi
  echo

  echo "--- pyright, on the same file(s) ---"
  if [ -z "$PYRIGHT" ]; then
    echo "BLIND: no pyright, so types went unchecked."
    note 2
  else
    OUT="$(mktemp)"
    printf '%s\n' "$PY_FILES" | xargs "$PYRIGHT" --outputjson --pythonpath "$PY" >"$OUT" 2>/dev/null
    "$PY" - "$OUT" <<'PYEOF'
import json, sys
try:
    d = json.load(open(sys.argv[1]))
except (json.JSONDecodeError, OSError):
    print("pyright produced no readable report; that is BLIND, not clean."); sys.exit(2)
errs = [x for x in d["generalDiagnostics"] if x["severity"] == "error"]
n = d["summary"]["filesAnalyzed"]
if n == 0:
    # It exits 0 having looked at nothing when handed paths it does not accept. Grading
    # that as a pass is the false-green this whole file exists to stop.
    print("pyright analysed 0 files -- it was handed paths it did not accept. BLIND.")
    sys.exit(2)
for x in errs:
    print(f'{x["file"]}:{x["range"]["start"]["line"]+1}: {x["message"].splitlines()[0]}')
print(f'{len(errs)} error(s) over {n} file(s).')
sys.exit(1 if errs else 0)
PYEOF
    note $?
    rm -f "$OUT"
  fi
  echo
fi

if [ -n "$SH_FILES" ]; then
  echo "--- shellcheck, on $(count "$SH_FILES") changed shell file(s) ---"
  if [ -z "$SHELLCHECK" ]; then
    echo "BLIND: no shellcheck. \`brew install shellcheck\`, or apt-get on the runner."
    note 2
  elif printf '%s\n' "$SH_FILES" | xargs "$SHELLCHECK" -f gcc -S warning; then
    echo "clean at severity warning."
  else
    note 1
  fi
  echo
fi

if [ -n "$WF_FILES" ]; then
  # actionlint runs the shell analyser over every `run:` block, and by default exits 1 on
  # its `info` level too. On the first run that failed this repo's own workflow over
  # `tr 'a-z' 'A-Z'` -- correct code, refused (LAW 38). The threshold below is the same
  # `warning` the shell section uses, so one policy covers shell wherever it lives.
  #
  # The comment above deliberately does not start a line with the analyser's own name: a
  # comment that does is read as a directive, and this gate caught exactly that mistake in
  # this file on its first self-run (SC1073).
  echo "--- actionlint, on $(count "$WF_FILES") changed workflow(s) ---"
  if [ -z "$ACTIONLINT" ]; then
    echo "BLIND: no actionlint. \`brew install actionlint\`, or the runner's action."
    note 2
  elif printf '%s\n' "$WF_FILES" | xargs "$ACTIONLINT" -shellcheck='-S warning'; then
    echo "clean."
  else
    note 1
  fi
  echo
fi

if [ "$rc" -eq 0 ]; then
  echo "PASS: every file this branch touched meets the standard."
elif [ "$rc" -eq 2 ]; then
  echo "BLIND: a checker could not run, so this is not a pass. Install it and re-run."
else
  echo "FAIL: this branch adds or edits code that breaks the standard."
fi
exit "$rc"
