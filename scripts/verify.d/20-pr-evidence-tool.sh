#!/usr/bin/env bash
# The camera resolves and runs. It lives outside this repo, so it can be missing.
echo "\$ command -v pr-evidence"
p="$(command -v pr-evidence)" || { echo "not on PATH — see README, 'Evidence on a pull request'"; exit 2; }
echo "$p"
echo "\$ pr-evidence --help >/dev/null"
pr-evidence --help >/dev/null 2>&1 || { echo "on PATH but will not run"; exit 1; }
echo "runs"
