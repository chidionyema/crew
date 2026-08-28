#!/usr/bin/env bash
# The founder's shape: an issue that shows its work, and templates that say the
# same thing in the same order. 0 PASS, 1 FAIL, 2 CANNOT RUN.
set -uo pipefail
# CREW_ROOT is set by the verify harness and by CI, and was required here. That
# made this gate unrunnable by hand: a developer who ran it directly got
# "parameter null or not set" and rc=1, indistinguishable from a real failure.
# So nobody ran it locally, and it could only ever go red in CI -- the same
# class as the home-directory receipt that 85-risk-register.sh now refuses.
# Default it to the repository this script lives in, exactly as the other gates
# do, so running the gate by hand is the cheap thing rather than the confusing
# one (LAW 38: a guard that refuses correct work is an outage).
cd "${CREW_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}" || exit 2
fail=0

for f in FOUNDER.md docs/decisions/DECISIONS.md docs/reference/PREFERENCES.md docs/decisions/CORRECTIONS.md \
         scripts/crew-triage .github/ISSUE_TEMPLATE/crew_task.md \
         .github/pull_request_template.md scripts/install-crew; do
    if [[ -f "$f" ]]; then echo "PASS  $f"; else echo "FAIL  $f is missing"; fail=1; fi
done

echo "\$ bash -n scripts/install-crew"
bash -n scripts/install-crew && echo "  syntax ok" || { echo "  FAIL"; fail=1; }

# The incident: the draft rendered "- [ ] [x] Implementation", a box inside a
# box, which neither GitHub nor a person reads as ticked.
echo "\$ crew-triage --dry-run | grep -c '\- \[.\] \['"
n=$(scripts/crew-triage --title verify --evidence abc --dry-run </dev/null | grep -c '^- \[.\] \[' || true)
if [[ "${n:-0}" -eq 0 ]]; then echo "  0 doubled checkboxes"; else echo "  FAIL ${n} doubled checkboxes"; fail=1; fi

# One template, not two. A copy at the repo root drifts from the one GitHub serves.
echo "\$ diff the root pointer against the real template"
if grep -q '.github/ISSUE_TEMPLATE/crew_task.md' docs/reference/ISSUE_TEMPLATE.md; then
    echo "  docs/reference/ISSUE_TEMPLATE.md points at the real one"
else
    echo "  FAIL docs/reference/ISSUE_TEMPLATE.md is a second copy"; fail=1
fi

exit $fail
