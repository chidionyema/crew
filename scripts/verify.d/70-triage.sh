#!/usr/bin/env bash
# The founder's shape: an issue that shows its work, and templates that say the
# same thing in the same order. 0 PASS, 1 FAIL, 2 CANNOT RUN.
set -uo pipefail
cd "${CREW_ROOT:?}" || exit 2
fail=0

for f in FOUNDER.md scripts/crew-triage .github/ISSUE_TEMPLATE/crew_task.md \
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
if grep -q '.github/ISSUE_TEMPLATE/crew_task.md' ISSUE_TEMPLATE.md; then
    echo "  ISSUE_TEMPLATE.md points at the real one"
else
    echo "  FAIL ISSUE_TEMPLATE.md is a second copy"; fail=1
fi

exit $fail
