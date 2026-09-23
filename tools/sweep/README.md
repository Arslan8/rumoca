# Sweep tooling

## Run sweeps in parallel

The machine has 32 cores and the jobs are independent — each compiles its own
artifact into its own temp directory and shares nothing. Running a corpus sweep
serially is the single biggest waste in this project's history: a four-minute
job took **seventy-five minutes**, repeatedly, and the results then sat
uncollected because nobody was watching a job that should have finished while
they were still looking at it.

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
    --out results.jsonl --keep-parameter-chains          # parallel by default
python3 tools/sweep/static_eval.py ... --jobs 1          # serial, for debugging
```

`--jobs` defaults to whichever of cores and free memory allows fewer. Each
worker holds a whole compile of MSL at roughly 1.8 GB resident, so memory binds
well before cores do: 24 workers reached 35 GB and got a sibling process killed.
The default now takes half of *available* memory, because the rest of the
machine is doing something too.

**Output is identical to serial.** `executor.map` yields in input order, so two
runs of the same list produce byte-comparable files and a partial file is a
prefix of the whole rather than an arbitrary subset. That property is what makes
a run diffable against the last one, and it is worth the small loss of
throughput against `as_completed`.

A worker that raises records a `harness-error` row for that model. A sweep that
reports 846 of 847 rows without saying which one vanished is worse than one that
records the failure.

### One sweep at a time

The memory-aware default sizes *one* sweep against free memory. Two launched
concurrently each take that share, and the machine runs out — which is how two
waiters were OOM-killed even after the sizing was fixed. Either serialise them,
or pass `--jobs` explicitly to split the budget:

```bash
python3 tools/sweep/static_eval.py ... --jobs 6 &
python3 tools/sweep/other_sweep.py ... --jobs 6 &
```

## Waiting for a sweep

```bash
tools/sweep/await_run.sh results.jsonl 847
```

### Never match your own command line

`pgrep`/`pkill -f` match against *full* command lines, and the shell running
them is one of those command lines. Four background jobs and two shells died to
this in a single day:

```bash
pkill -f "STATIC_V8"      # kills the shell that ran it
pkill -f "STATIC_V[8]"    # matches the job, not the bracketed literal
```

The bracket is the standard trick: `STATIC_V[8]` matches `STATIC_V8` in the
target process, and the pattern as written in this shell's own command line
contains brackets, so it does not match itself.

Do **not** write `until ! pgrep -f "static_eval.py"`. `pgrep -f` matches full
command lines including the waiter's own `bash -c '... static_eval.py ...'`, so
the pattern always matches, the loop never exits, and whatever was chained after
it never runs. Four background jobs died that way in one day, silently, after
the sweep they were waiting on had already finished. `await_run.sh` waits on a
row count and exits non-zero on timeout so a caller cannot chain report
generation onto a partial file.

## The generators

Each reads a completed run and writes one file per item. All are idempotent:

```bash
python3 tools/sweep/gen_instance_reports.py    docs/runs/data/INSTANCES.json 20
python3 tools/sweep/gen_site_reports.py        docs/runs/data/STATIC_FINAL.jsonl
python3 tools/sweep/gen_finding_reports.py     docs/runs/data/STATIC_FINAL.jsonl
python3 tools/sweep/gen_declaration_reports.py
```

## Evaluation

```bash
python3 tools/sweep/adjudicate.py              run.jsonl          # TP/FP/unjudged
python3 tools/sweep/sample_for_adjudication.py run.jsonl 30       # stratified sample
python3 tools/sweep/precision.py               SAMPLE.json        # weighted, Wilson CI
```

`precision.py` refuses to print a figure while any sampled draw is
unadjudicated: dropping the hard ones biases the estimate toward whatever was
easy to decide.
