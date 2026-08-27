#!/usr/bin/env bash
# The warehouse's source registry, tested in BOTH directions.
#
# code-84, on the estate's kubernetes work, 2026-08-24: "a store in neither SOURCES nor
# DECLINED failing --check is right. Make sure you have a test that adds a correct new
# store and watches --check say yes." Their own image-pinning gate refused this repo's
# real repoURL on its first run, which is LAW 38: a guard that refuses correct work is
# an outage, and only a control that feeds it correct work would ever have caught it.
#
# So there are six controls here and three of them are the gate saying YES. All of them
# run against scratch files -- collect.py takes its warehouse, its registry and its crawl
# from the environment -- so nothing here touches the real warehouse or the real crawl.
set -u
HERE="$(cd "$(dirname "$0")/../.." && pwd)"
COLLECT="$HERE/science/collect.py"
PY="${PYTHON:-python3}"
[ -f "$COLLECT" ] || { echo "no collector at $COLLECT"; exit 2; }

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
fail=0

# A store that really exists, so the "correct input" controls are feeding the gate a real
# file and not a name. This is the new store an owner would be adding.
mkdir -p "$WORK/store"
printf 'receivers:\n  otlp:\n    protocols: {grpc: {}}\n' > "$WORK/otel-collector.yaml"
printf '{"at":"2026-08-24T00:00:00+00:00","note":"a real row"}\n' > "$WORK/store/new.jsonl"

crawl() {  # $1 = json array of rows
  cat > "$WORK/inventory.json" <<EOF
{"at": "2026-08-24T00:00:00+00:00", "findings": {}, "rows": $1}
EOF
}
registry() { cat > "$WORK/sources.json"; }

run() {  # echoes rc, prints output under a labelled header
  echo "\$ collect.py $*"
  SCIENCE_WAREHOUSE="$WORK/w.db" SCIENCE_REGISTRY="$WORK/sources.json" \
    ESTATE_INVENTORY="$WORK/inventory.json" ESTATE_HOME="$WORK" \
    OTEL_COLLECTOR_CONFIG="${COLLECTOR_CFG:-$WORK/otel-collector.yaml}" \
    "$PY" "$COLLECT" "$@" 2>&1 | sed 's/^/    /'
  return "${PIPESTATUS[0]}"
}

expect() {  # $1 = wanted rc, $2 = label
  local got=$? want=$1 label=$2
  if [ "$got" -eq "$want" ]; then
    echo "  PASS  $label  (rc=$got)"
  else
    echo "  FAIL  $label  (rc=$got, wanted $want)"
    fail=1
  fi
}

declared_only='[{"kind":"ledger","id":"newstore","path":"'"$WORK"'/store/new.jsonl","member_of":null,"rows":1}]'
plus_undeclared='[{"kind":"ledger","id":"newstore","path":"'"$WORK"'/store/new.jsonl","member_of":null,"rows":1},
                  {"kind":"ledger","id":"forgotten","path":"'"$WORK"'/store/forgotten.jsonl","member_of":null,"rows":9}]'

good_registry() {
  registry <<EOF
{"version": 1, "roots": {"home": "~"}, "default_stale_after_hours": 100000,
 "sources": [{"name": "newstore", "root": "home", "path": "store/new.jsonl",
              "kind": "jsonl", "time_field": "at", "receiver": "otlp"}],
 "declined": []}
EOF
}

echo "== A. a correct new store, declared: the gate must say YES =="
good_registry; crawl "$declared_only"
run --check; expect 0 "a fully declared registry passes --check"

echo "== B. the same store, undeclared: the gate must say NO =="
good_registry; crawl "$plus_undeclared"
run --check; expect 1 "an undeclared store fails --check"

echo "== C. the same store, declined with a reason: YES again =="
registry <<EOF
{"version": 1, "roots": {"home": "~"}, "default_stale_after_hours": 100000,
 "sources": [{"name": "newstore", "root": "home", "path": "store/new.jsonl",
              "kind": "jsonl", "time_field": "at", "receiver": "otlp"}],
 "declined": [{"id": "forgotten", "reason": "a scratch file this control wrote, not an estate store"}]}
EOF
run --check; expect 0 "a declined store with a stated reason passes"

echo "== D. declined with no reason: refused, because that is indistinguishable from forgotten =="
registry <<EOF
{"version": 1, "roots": {"home": "~"}, "default_stale_after_hours": 100000,
 "sources": [{"name": "newstore", "root": "home", "path": "store/new.jsonl",
              "kind": "jsonl", "time_field": "at", "receiver": "otlp"}],
 "declined": [{"id": "forgotten", "reason": "   "}]}
EOF
run --check; expect 1 "an exclusion with an empty reason is refused"

echo "== E. no registry at all: refused, never a healthy run over nothing =="
good_registry; crawl "$declared_only"
echo "\$ collect.py --check   # SCIENCE_REGISTRY points at a file that does not exist"
SCIENCE_WAREHOUSE="$WORK/w.db" SCIENCE_REGISTRY="$WORK/absent.json" \
  ESTATE_INVENTORY="$WORK/inventory.json" ESTATE_HOME="$WORK" \
  "$PY" "$COLLECT" --check 2>&1 | sed 's/^/    /'
(exit "${PIPESTATUS[0]}"); expect 1 "a missing registry is refused, not defaulted"

echo "== F. no crawl: refused, because a reconciliation with no oracle reads as proof =="
good_registry; rm -f "$WORK/inventory.json"
run --check; expect 1 "a missing crawl refuses to return a verdict"

echo "== G. a source naming a receiver the collector does not declare: NO =="
registry <<EOF
{"version": 1, "roots": {"home": "~"}, "default_stale_after_hours": 100000,
 "sources": [{"name": "newstore", "root": "home", "path": "store/new.jsonl",
              "kind": "jsonl", "time_field": "at", "receiver": "carrier_pigeon"}],
 "declined": []}
EOF
crawl "$declared_only"
run --check; expect 1 "a source with an undeclared receiver fails --check"

echo "== H. a source with no receiver at all: refused, it has no way into the pipeline =="
registry <<EOF
{"version": 1, "roots": {"home": "~"}, "default_stale_after_hours": 100000,
 "sources": [{"name": "newstore", "root": "home", "path": "store/new.jsonl",
              "kind": "jsonl", "time_field": "at"}],
 "declined": []}
EOF
run --check; expect 1 "a source naming no receiver is refused"

echo "== I. collector config unreadable: BLIND, printed, not a verdict either way =="
good_registry; crawl "$declared_only"
out=$(COLLECTOR_CFG="$WORK/absent-collector.yaml" run --check); rc=$?
echo "$out" | sed 's/^/    /'
echo "$out" | grep -q "receivers: BLIND" && [ "$rc" -eq 0 ]; expect 0 "an unreadable collector config reports BLIND and does not fail correct work"

echo "== J. the real registry against the real crawl =="
# A guard that loses its evidence reports BLIND, never a verdict. The crawl is written
# hourly by com.estate.inventory ON THE LAPTOP; a CI runner has no estate to crawl, and
# grading the real reconcile there fails on absence, not on a defect. Controls A-F above
# are hermetic and still decide this gate everywhere. Same default path as collect.py.
REAL_INVENTORY="${ESTATE_INVENTORY:-$HOME/.estate/state/inventory.json}"
if [ ! -f "$REAL_INVENTORY" ]; then
  echo "  BLIND  no crawl on this host ($REAL_INVENTORY absent); the laptop grades this control"
else
  echo "\$ collect.py --reconcile"
  "$PY" "$COLLECT" --reconcile 2>&1 | sed 's/^/    /'
  (exit "${PIPESTATUS[0]}"); expect 0 "the estate's own registry reconciles clean"
fi

exit $fail
