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
# A file is what its shebang says it is. The extension is a hint, and on this estate the
# scripts a person types the name of -- `bin/crew`, `scripts/estate-snapshot` -- do not
# carry one, because a user-facing command should not make anyone type `.py`.
#
# INCIDENT, 2026-08-24. This gate sniffed the shebang for shell and matched `\.py$` for
# Python, so four tracked Python programs were invisible to it. It was found when a PR
# that rewrote `scripts/estate-snapshot`'s commit path introduced 16 new percent-format
# findings in its own new lines and this gate printed PASS over them:
#
#     scripts/estate-snapshot on origin/main   64 ruff findings
#     the same file on that branch             77
#     inside the lines that branch added       16
#     $ bash scripts/verify.d/15-code-standard.sh
#     PASS: every file this branch touched meets the standard.
#
# The gate graded correctly every file it opened. It opened the wrong set of files.
is_shell() {
  case "$1" in *.sh|*.bash) return 0;; esac
  head -c 60 "$1" 2>/dev/null | grep -qE '^#!.*(bash|/sh|zsh)'
}
is_python() {
  case "$1" in *.py) return 0;; esac
  head -c 60 "$1" 2>/dev/null | grep -qE '^#!.*python'
}
PY_FILES="$(printf '%s\n' "$ALL" | grep '\.py$' || true)"
SH_FILES="$(printf '%s\n' "$ALL" | while read -r f; do [ -n "$f" ] && is_shell "$f" && echo "$f"; done)"
# Newly visible, and reported rather than enforced for now -- see REPORT-ONLY below.
#
# Two things about the loop below, and both comments are up HERE on purpose.
#
# 1. The leading paren on the case pattern is load-bearing. bash 3.2 -- which is /bin/bash on
#    every Mac in this estate -- cannot parse a case pattern's closing paren inside a command
#    substitution, so the whole gate died and then ran on with the loop variable unbound.
# 2. A comment INSIDE the substitution is a trap. bash 3.2 lexes quotes inside a command
#    substitution even in a comment, so a single apostrophe there opens a string that never
#    closes and the file stops parsing. The word "pattern's" in this very comment did it.
#
# bash 5 on ubuntu-latest accepts both, which is why CI was green while the gate was dead on
# every Mac. R14 makes the laptop the substrate, so green on the runner is not the question.
PY_NEW="$(printf '%s\n' "$ALL" | while read -r f; do
  [ -n "$f" ] || continue
  case "$f" in (*.py) continue;; esac
  is_python "$f" && echo "$f"
done)"
WF_FILES="$(printf '%s\n' "$ALL" | grep -E '^\.github/workflows/.*\.ya?ml$' || true)"

# The whole-repo number, printed on every run whatever the verdict. A debt nobody prints
# is a debt nobody pays (LAW 28).
if [ -n "$RUFF" ]; then
  DEBT="$("$RUFF" check --no-cache --quiet --output-format concise . 2>/dev/null | grep -c ':' || true)"
  echo "repo-wide ruff findings on all Python: ${DEBT}   (reported, not enforced)"
fi

count() { printf '%s\n' "$1" | grep -c . || true; }
echo "changed on this branch: $(count "$PY_FILES") python, $(count "$SH_FILES") shell, $(count "$WF_FILES") workflow"
[ -n "$PY_NEW" ] && echo "                      + $(count "$PY_NEW") python by shebang, report-only (see the tail of this run)"
if [ -z "$PY_FILES$SH_FILES$WF_FILES$PY_NEW" ]; then
  echo "nothing this gate checks was added or changed. Nothing to enforce."
  exit 0
fi
echo

rc=0
# A real failure outranks a blind spot: once something is genuinely broken, a missing tool
# must not soften the verdict to BLIND. The first draft of this gate did exactly that.
note() { if [ "$1" -eq 1 ]; then rc=1; elif [ "$1" -ne 0 ] && [ "$rc" -eq 0 ]; then rc="$1"; fi; }

# Both checkers, over a newline-separated file list. Returns the same 0/1/2 the gate uses,
# and is called twice: once for the files this gate enforces, once for the report-only set.
# One implementation, so the report says exactly what the enforced run would say -- a
# report produced by a second, simpler code path is a report about the second code path.
python_standard() {
  local _r=0 _p=0 OUT
  echo "--- ruff, on $(count "$1") python file(s) ---"
  if [ -z "$RUFF" ]; then
    echo "BLIND: no ruff. \`.venv/bin/pip install ruff pyright\`, or add it to the runner."
    _r=2
  elif printf '%s\n' "$1" | xargs "$RUFF" check --no-cache --output-format concise; then
    echo "clean."
    _r=0
  else
    _r=1
    echo
    echo "Fix, do not silence. \`ruff check --fix\` handles the mechanical ones; a rule that"
    echo "is genuinely wrong for a line takes a \`# noqa: RULE\` with the reason beside it."
  fi
  echo

  echo "--- pyright, on the same file(s) ---"
  if [ -z "$PYRIGHT" ]; then
    echo "BLIND: no pyright, so types went unchecked."
    [ "$_r" -eq 1 ] || _r=2
  else
    OUT="$(mktemp)"
    printf '%s\n' "$1" | xargs "$PYRIGHT" --outputjson --pythonpath "$PY" >"$OUT" 2>/dev/null
    "$PY" - "$OUT" <<'PYEOF'
import importlib.util, json, pathlib, re, sys
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

# A dependency this repo declares has to be visible to the type checker. When it is not,
# every verdict on a file that imports it sits downstream of something pyright itself
# said it could not read -- and `reportMissingImports = "warning"` in pyproject.toml
# makes that admission a warning while its consequences arrive as errors. Until this
# block existed the admission was dropped on the floor: `errs` below filters to
# severity == "error", so nothing ever printed it.
#
# Measured on PR #166, 2026-08-24. Its new test file takes a `str | None` from
# `shutil.which` and guards it with `pytest.skip()`, which is typed `NoReturn`, so the
# value is `str` at every later use. Same file, same pyright 1.1.411, only the
# interpreter handed to --pythonpath changing:
#
#     resolving against a venv holding the deps    0 errors, 0 warnings
#     resolving against a bare 3.11 venv           5 errors, 1 warning
#                                                  warning: Import "pytest" could not be resolved
#                                                  errors on lines 117, 139, 151, 179
#
# CI reported exactly those five lines. The author's code was correct and this gate
# spent a review cycle saying it was not, without once mentioning that it was reading
# the file with pytest invisible. crew#164: a check that cannot reach its evidence
# returns BLIND, and this one returned a verdict.
#
# Two signals, either of which puts the fault in the environment and not the code:
#
#   1. this interpreter can import the module, and pyright -- pointed at THIS
#      interpreter by --pythonpath -- could not. They disagree, so the search is broken.
#   2. requirements-dev.txt declares the module. Then it was meant to be installed where
#      pyright looked, whether or not this process happens to import it.
#
# Neither fires for the imports that are legitimately unresolvable here. `datamap` and
# `founder_board` are local modules reached through sys.path at run time; this
# interpreter cannot import them either and no requirements file names them. Measured on
# main the day this was written, with the deps visible: 3 unresolved diagnostics, 0
# BLIND. A guard that refuses correct work is an outage (LAW 38), so that case is the
# one this was checked against first.
#
# Residual, stated because it is real: signal 2 compares an import name to a
# distribution name and the two differ for some packages -- PyYAML imports as `yaml`.
# `dbt-duckdb` is the one such entry in this repo and it imports as `dbt`, so an
# invisible dbt-duckdb is caught by signal 1 alone, which needs this interpreter to have
# it installed. Signal 2 does not see it.
unresolved = sorted({x["message"].split('"')[1].split(".")[0]
                     for x in d["generalDiagnostics"]
                     if x.get("rule") == "reportMissingImports"})
declared = set()
try:
    for line in pathlib.Path("requirements-dev.txt").read_text().splitlines():
        name = re.split(r"[<>=!;\[\s#]", line.strip(), maxsplit=1)[0]
        if name:
            declared.add(name.lower().replace("-", "_"))
except OSError:
    pass          # no requirements file: signal 1 still stands on its own
blind = []
for mod in unresolved:
    try:
        importable = importlib.util.find_spec(mod) is not None
    except (ImportError, ValueError):
        importable = False
    if importable:
        blind.append(f"{mod}: this interpreter imports it, pyright pointed at the same "
                     f"interpreter could not. Its import search is broken, not your code.")
    elif mod.lower() in declared:
        blind.append(f"{mod}: requirements-dev.txt declares it and it is not installed "
                     f"where pyright looked. Install the deps into that environment.")
if blind:
    print(f"pyright could not resolve {len(blind)} of this repo's own dependencies, so it "
          f"graded files whose imports it cannot read. BLIND, not clean.")
    print(f"  interpreter handed to --pythonpath: {sys.executable}")
    for b in blind:
        print(f"  {b}")
    sys.exit(2)
for x in errs:
    print(f'{x["file"]}:{x["range"]["start"]["line"]+1}: {x["message"].splitlines()[0]}')
print(f'{len(errs)} error(s) over {n} file(s).')
sys.exit(1 if errs else 0)
PYEOF
    _p=$?
    rm -f "$OUT"
    if [ "$_p" -eq 1 ]; then _r=1; elif [ "$_p" -ne 0 ] && [ "$_r" -eq 0 ]; then _r="$_p"; fi
  fi
  echo
  return "$_r"
}

if [ -n "$PY_FILES" ]; then
  python_standard "$PY_FILES"
  note $?
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

  # Does it parse under the OLDEST bash this estate runs on?
  #
  # A linter is not bash. ShellCheck implements its own parser, so it reads a script that
  # bash 3.2 cannot parse at all and reports it clean. Twice on 2026-08-24 this file itself
  # carried a construct bash 5 accepts and bash 3.2 refuses: a case pattern closing paren
  # inside a command substitution, and an apostrophe in a comment inside a command
  # substitution. Both were invisible. CI runs bash 5 on ubuntu-latest and went green while
  # the gate was dead on every Mac, and R14 makes the laptop the substrate.
  #
  # BLIND, never a pass, where no old bash exists -- which is the case on the runner. This
  # is live exactly where the failure occurs.
  echo "--- bash 3.2 parse, on the same file(s) ---"
  OLDBASH=""
  OLDBASH_V=""
  if [ -x /bin/bash ] && /bin/bash --version 2>/dev/null | head -1 | grep -q 'version 3\.'; then
    OLDBASH=/bin/bash
    OLDBASH_V="bash $(/bin/bash --version | head -1 | sed 's/.*version \([0-9.]*\).*/\1/')"
  fi
  if [ -z "$OLDBASH" ]; then
    echo "BLIND: no bash 3.x here, so a Mac-only parse failure would not be seen."
    note 2
  else
    bad_parse=0
    while IFS= read -r f; do
      [ -n "$f" ] && [ -f "$f" ] || continue
      if ! err=$("$OLDBASH" -n "$f" 2>&1); then
        bad_parse=$((bad_parse + 1))
        echo "$f:"
        printf '%s\n' "$err" | head -2 | sed 's/^/    /'
      fi
    done <<EOF
$SH_FILES
EOF
    if [ "$bad_parse" -eq 0 ]; then
      echo "all $(count "$SH_FILES") parse under $OLDBASH_V."
    else
      echo "$bad_parse file(s) bash 3.2 cannot parse. bash 5 accepting it is not the test."
      note 1
    fi
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

# REPORT-ONLY. New coverage lands visible before it lands blocking (docs/STANDARDS.md,
# "Widening a gate"). Widening the selection above and enforcing it in the same change
# would turn branches red on findings their authors did not write and could not have seen
# coming, and the estate already knows what happens then: a red check everyone learns to
# ignore, which is no gate at all (LAW 38). So this section prints the verdict it WOULD
# reach and leaves `rc` alone. Flipping it to blocking is its own PR, and that PR quotes
# the WOULD-FAIL count printed here.
WOULD=""
if [ -n "$PY_NEW" ]; then
  echo "=== REPORT-ONLY: $(count "$PY_NEW") python file(s) found by shebang, not by extension ==="
  printf '%s\n' "$PY_NEW" | sed 's/^/  /'
  echo
  python_standard "$PY_NEW"
  case $? in
    0) WOULD="";;
    1) WOULD="WOULD-FAIL";;
    *) WOULD="WOULD-BE-BLIND";;
  esac
  echo "verdict on the files above: ${WOULD:-would pass}. Reported, not enforced."
  echo
fi

if [ "$rc" -eq 0 ]; then
  echo "PASS: every file this branch touched meets the standard."
elif [ "$rc" -eq 2 ]; then
  echo "BLIND: a checker could not run, so this is not a pass. Install it and re-run."
else
  echo "FAIL: this branch adds or edits code that breaks the standard."
fi
if [ -n "$WOULD" ]; then
  # The count is hoisted out of the echo on purpose. bash 3.2 -- /bin/bash on every Mac
  # in this estate -- cannot parse a nested double quote inside `$( )` inside a double
  # quoted string when it sits in an `&&` list, and refused to parse this whole FILE for
  # it. bash 5 accepts it, so CI never saw it. Same class as the case-pattern paren above.
  n_new=$(count "$PY_NEW")
  echo "  ($WOULD on $n_new shebang-python file(s), reported above and not yet enforced)"
fi
exit "$rc"
