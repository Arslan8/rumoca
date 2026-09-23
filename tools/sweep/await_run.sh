#!/usr/bin/env bash
# Wait for a sweep to finish, then exit. Nothing else.
#
# Written because the obvious spelling is wrong in a way that fails silently:
#
#     until ! pgrep -f "static_eval.py"; do sleep 45; done
#
# `pgrep -f` matches against full command lines, and the waiter's own
# `bash -c '... static_eval.py ...'` is one of them. The pattern always matches,
# `!` is always false, the loop never exits, and the commands chained after it
# never run. Three chained jobs in this project died exactly that way — the
# sweep finished on time and its results sat uncollected, because the step that
# was supposed to pick them up was still spinning.
#
# So: wait on a completion marker the job itself writes, never on a process
# table lookup for a pattern that includes this script's own arguments.
#
#     tools/sweep/await_run.sh results.jsonl 847
set -euo pipefail

output="${1:?usage: await_run.sh <output.jsonl> <expected-rows> [timeout-seconds]}"
expected="${2:?expected row count}"
deadline=$(( $(date +%s) + ${3:-10800} ))

while :; do
    rows=$(wc -l < "$output" 2>/dev/null || echo 0)
    if [ "$rows" -ge "$expected" ]; then
        echo "complete: $rows/$expected rows in $output"
        exit 0
    fi
    if [ "$(date +%s)" -ge "$deadline" ]; then
        # A timeout is reported as a timeout. Exiting 0 here would let a caller
        # chain generation onto a partial file and publish it as a full run.
        echo "TIMED OUT at $rows/$expected rows in $output" >&2
        exit 1
    fi
    sleep 60
done
