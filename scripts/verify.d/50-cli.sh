#!/usr/bin/env bash
# The tool a person actually types resolves and answers.
echo "\$ command -v crew"
p="$(command -v crew)" || { echo "crew is not on PATH — see README, 'Install'"; exit 2; }
echo "$p"
echo "\$ crew --version"
crew --version || exit 1
