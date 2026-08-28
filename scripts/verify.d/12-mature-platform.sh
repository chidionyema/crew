#!/usr/bin/env bash
# A new script on this branch must name the mature platform it rejected.
#
# Standard: crew/docs/STANDARDS.md, review acceptance criterion 6 -- this gate is that
# criterion made mechanical for the two file types the estate actually writes. Rejected:
# pre-commit + a generic "no new files" hook, because the check is not "was a file added",
# it is "does its header declare a rejected alternative", which no off-the-shelf hook
# expresses; and gitleaks/semgrep, which grade content patterns and not a decision record.
#
# WHY THIS EXISTS. Founder, 2026-08-24: "FOR THE LAST TINE WE NEED A NATURE, PLATFRON WE
# HAVE A POTENTIL BUYER AND NEED INDUSTRY AND ENTERPRISE APPROCACH NOT HALF STICHED
# TOGETHER SOLUTIONS THAT BREAK DAILY. HEADLINE FOR CREW ABOVE ALL LAWS."
#
# That was the fifth time. R4 (2026-08-23) said think like an investor buys tomorrow. R6
# said mature proven platforms over hand-rolled bash and python. R7 said unify and
# standardise. R11 said overhaul, do not firefight. All four were recorded as prose in
# rulings.json, injected at every SessionStart, and every one of them was walked past --
# because prose cannot stop a command. LAW 44: a law without a protocol is a wish. This
# is R6's protocol.
#
# WHAT IT CHECKS. Files ADDED on this branch (never files edited -- the debt is not this
# branch's to pay) ending .sh or .py must carry one of three markers in their first 40
# lines:
#
#   Standard:   <row of docs/reference/STANDARDS.md this uses>
#   Deviation:  <the standard row this departs from, and why>
#   Rejected:   <the mature tool considered, and the specific thing it cannot do>
#
# The vocabulary is deliberately the one criterion 6 already uses. A third set of words
# for the same decision would be its own small act of stitching.
#
# WHY A RATCHET, NOT A SWEEP. 15-code-standard.sh learned this the expensive way: a gate
# that fails on every pre-existing file fails every branch, and a red check every session
# learns to ignore enforces nothing. So only additions are graded. Pre-existing scripts
# are counted and printed, never failed.
#
# WHAT IT CANNOT SEE (residual, stated because a guard that hides its blind spot lies).
# It cannot tell a true rejection from the words "Rejected: none". It grades that a
# decision was recorded, not that the decision was good -- that is the reviewer's job, and
# criterion 6 already says the review grades the deviation. It also cannot see a script
# added in another repository; the class spans the estate and this instance guards crew.
#
# exit 0 pass | exit 1 an added script declares nothing | exit 2 CANNOT RUN
set -uo pipefail
cd "${CREW_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null)}" || exit 2

MARKERS='^[[:space:]]*#?[[:space:]]*(Standard|Deviation|Rejected):[[:space:]]*[^[:space:]]'

# Reads a header rather than a whole file: a marker 300 lines down is not a decision
# record anybody reads.
header_declares() {
	head -40 "$1" 2>/dev/null | grep -qE "$MARKERS"
}

selftest() {
	tmp="$(mktemp -d)" || return 2
	trap 'rm -rf "$tmp"' RETURN
	fail=0

	printf '#!/bin/sh\n# Rejected: cron, it cannot see machine load.\necho hi\n' >"$tmp/good.sh"
	if header_declares "$tmp/good.sh"; then
		echo "  ok    a declared script passes"
	else
		echo "  FAIL  a declared script was refused (LAW 38: that is an outage)"; fail=1
	fi

	printf '#!/bin/sh\n# just a helper\necho hi\n' >"$tmp/bare.sh"
	if header_declares "$tmp/bare.sh"; then
		echo "  FAIL  an undeclared script passed"; fail=1
	else
		echo "  ok    an undeclared script is refused"
	fi

	# The marker must carry a value. "Rejected:" alone is the shape of a session
	# satisfying the grep rather than making the decision.
	printf '#!/bin/sh\n# Rejected:\necho hi\n' >"$tmp/empty.sh"
	if header_declares "$tmp/empty.sh"; then
		echo "  FAIL  an empty marker passed"; fail=1
	else
		echo "  ok    an empty marker does not satisfy it"
	fi

	# 41 lines of preamble then the marker: not a header.
	{ printf '#!/bin/sh\n'; i=0; while [ "$i" -lt 45 ]; do echo "# padding"; i=$((i + 1)); done
	  echo '# Rejected: something'; } >"$tmp/late.sh"
	if header_declares "$tmp/late.sh"; then
		echo "  FAIL  a marker below the header passed"; fail=1
	else
		echo "  ok    a marker below the header does not count"
	fi

	printf '# Standard: docs/reference/STANDARDS.md job monitoring row\nx = 1\n' >"$tmp/py_ok.py"
	if header_declares "$tmp/py_ok.py"; then
		echo "  ok    Standard: is accepted as well as Rejected:"
	else
		echo "  FAIL  Standard: was refused"; fail=1
	fi

	[ "$fail" -eq 0 ] && echo "  selftest: 5 arms, 0 failures" || echo "  selftest: FAILURES"
	return "$fail"
}

if [ "${1:-}" = "--selftest" ]; then selftest; exit $?; fi

base=""
for ref in origin/main main; do
	if b="$(git merge-base HEAD "$ref" 2>/dev/null)" && [ -n "$b" ]; then base="$b"; break; fi
done
if [ -z "$base" ]; then
	echo "CANNOT RUN: no merge-base against origin/main or main."
	echo "A gate that cannot reach its evidence reports BLIND, never a pass."
	exit 2
fi

added=""
while IFS= read -r f; do
	case "$f" in
		*.sh | *.py) ;;
		*) continue ;;
	esac
	case "$f" in
		tests/*) continue ;;  # incident tests, rung 4 of the testing law
	esac
	[ -f "$f" ] || continue
	added="$added$f
"
done <<EOF
$(git diff --diff-filter=A --name-only "$base"...HEAD 2>/dev/null)
EOF

bare=""
n_added=0
while IFS= read -r f; do
	[ -n "$f" ] || continue
	n_added=$((n_added + 1))
	header_declares "$f" || bare="$bare  $f
"
done <<EOF
$added
EOF

total=0
while IFS= read -r f; do
	[ -n "$f" ] && total=$((total + 1))
done <<EOF
$(git ls-files '*.sh' '*.py' 2>/dev/null)
EOF

echo "scripts added on this branch: $n_added   (repo total, not graded: $total)"

if [ -n "$bare" ]; then
	echo
	echo "REFUSED. These were added without naming what they replace:"
	printf '%s' "$bare"
	echo
	echo "Put one line in the first 40 lines of each:"
	echo "  # Rejected: <the mature tool you considered> -- <the specific thing it cannot do>"
	echo "  # Standard: <the docs/reference/STANDARDS.md row this uses>"
	echo "  # Deviation: <the row this departs from, and why>"
	echo
	echo "If you cannot name the tool, you have not looked yet, and the headline of"
	echo "$HOME/AGENTS.md says you may not write the file until you have."
	exit 1
fi

echo "pass: every script added on this branch names what it replaces."
exit 0
