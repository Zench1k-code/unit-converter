#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

status=0
out=$(python3 -m unittest discover -s tests 2>&1) || status=$?
echo "$out" >&2

total=$(echo "$out" | sed -n 's/^Ran \([0-9][0-9]*\) test.*/\1/p')
total=${total:-0}
bad=$(echo "$out" | grep -cE '^(FAIL|ERROR):' || true)
passed=$((total - bad))

echo "TESTS: ${passed}/${total}"
exit "$status"
