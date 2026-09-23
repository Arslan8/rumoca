# Verifying these results

> **Checking one instance?** Go straight to [`v2/bugs/`](v2/bugs/README.md). Every
> instance has a file, every file names the sanitizer responsible, and every
> file carries the two or three commands that check that one claim. This page
> is for reproducing the *aggregate* numbers.
>
> The reports' own commands are themselves tested, by extracting them from the
> published markdown and running them:
>
> ```console
> $ python3 tools/sweep/verify_bug_reports.py --tier confirmed --all
> $ python3 tools/sweep/verify_bug_reports.py --tier latent --all
> $ python3 tools/sweep/verify_bug_reports.py --tier candidate --sample 400
> ```
>
> Last run: 26/26 confirmed, 911/911 latent, 100/100 sampled candidates — all ok.

Written for someone who did not produce them and should not have to take any of
it on trust. Every number below has a command that recomputes it and a file
that records the input.

If something here does not reproduce, that is a result — say so. Several of the
findings in this project exist because a number was checked and did not hold up.

## 0. Prerequisites

```bash
cargo xtask repo modelica-deps ensure     # fetches MSL 4.1.0 and the corpus into target/
cargo build                               # debug build; every command below uses ./target/debug/rumoca
export PYTHONPATH=packages/rumoca-bitcode:packages/modelsan
```

Cross-tool confirmation additionally needs **OpenModelica** on `PATH`
(`omc --version`, developed against 1.27.0-dev). Two of its quirks cost this
project real time and are worth knowing before you start:

- `omc` must be run with **`CC=gcc`** or `buildModel` fails with a compiler
  error unrelated to the model.
- OMC loads its **bundled MSL 4.0.0** unless 4.1.0 is loaded explicitly with
  `loadFile`. Comparing against the wrong library version produced 12 spurious
  "Rumoca accepts what OMC rejects" findings before it was noticed.

## 1. What the claims are

Four tiers, deliberately not merged. Merging them is the single easiest way to
misread this work.

| Tier | Claim | Count | Evidence |
|---|---|---|---|
| **Confirmed declaration defect** | the component's contract does not admit the value, and the model fails at it | **11** | reproduced in two independent tools |
| **Confirmed topology-specific** | the model fails at a value the component *documents as supported* | **15** | reproduced in two independent tools |
| **Candidate** | static analysis reached it | 5503, of which 1733 make a defect claim and 638 are advisories | 26.7% precise [18.0, 31.5], sampled |
| **Latent** | a declaration permits an impossible value | 911 | source only |

**11 is the declaration-defect count.** The 15 topology-specific instances are
a weaker and more accurate claim about the same 26 execution results, and must
not be added to the 11; see
[TOOLBUG-020](toolbugs/TOOLBUG-020-zero-behaviour-was-decided-three-times.md).
1733 is a candidate list. 911 is blast radius over 17 missing lines in
`Units.mo`.

## 2. Reproducing the 26 confirmed instances

This is the headline result and the one worth attacking first.

```bash
python3 tools/sweep/confirm_eval.py docs/runs/data/FULLEVAL_MERGED.jsonl \
    --out /tmp/confirm.json --max-models 6
```

For each candidate it compiles the model, simulates at its **declared** values,
and only then applies the trigger. A finding is confirmed when the declared
configuration runs cleanly and the trigger fails — in both tools. Anything else
is `single-tool` or `excluded`, which are recorded and *not* counted.

Per-instance reports, one file each with the declaration and line:
[`docs/verified bugs/INSTANCES.md`](verified%20bugs/INSTANCES.md).

**Where to push hardest:** the confirmation asks *does this reproduce in the
other tool*, not *was the trigger legal*. That gap produced two false
confirmations ([TOOLBUG-010](toolbugs/TOOLBUG-010-divisorsan-misread-non-literal-min.md))
which are listed as withdrawn. Check the remaining 26 the same way: open the
declaration and confirm nothing already forbids the trigger value.

## 3. Reproducing the corpus run and its precision

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
    --out run.jsonl --keep-parameter-chains
diff <(sort run.jsonl) <(sort docs/runs/data/STATIC_FINAL.jsonl)   # should be empty
```

~10 minutes on 32 cores. `--jobs N` to bound it; the default is sized by free
memory, because each worker holds a whole MSL compile.

Then the precision figure:

```bash
python3 tools/sweep/sample_for_adjudication.py run.jsonl 30 20260915 /tmp/sample.json
python3 tools/sweep/adjudicate_divisors.py /tmp/sample.json    # execution-decidable strata
python3 tools/sweep/precision.py /tmp/sample.json
```

The seed is fixed, so you get the same draw. `precision.py` refuses to print a
figure while any draw is unadjudicated — filling in a verdict is a judgement,
and the tool will not average over the ones nobody made.

The 60 source-decidable draws were adjudicated by reading the declaration; the
reasoning for each is in `docs/runs/data/SAMPLE.json` under `reason`. **Disagree
with any of them freely** — that is what the field is for.

## 4. The claim most worth checking

> A claim about what the source says is 97–100% precise. A claim about physics
> or consequence is 0–7%.

[precision.md](findings/precision.md). If this is wrong, the whole framing of
the static tier is wrong. The fastest attack is to redraw with a different seed
and adjudicate 30 of `physical-domain-unenforced` yourself:

```bash
python3 tools/sweep/sample_for_adjudication.py run.jsonl 30 1234 /tmp/other.json
```

## 5. The tool defects

[`toolbugs/`](toolbugs/README.md). Four of these were found *by* the
verification work and each changed the results:

| | effect when fixed |
|---|---|
| TOOLBUG-013 — a type's `min` never reached the DAE | removed 5643 findings, 52% of the run |
| TOOLBUG-012 — connection ids numbered before filtering | 31 of 150 models exported artifacts that failed their own validator |
| TOOLBUG-011 — unary plus had no bitcode encoding | a model that simulated stopped simulating under a flag |
| TOOLBUG-010 — a non-literal `min` read as no bound | two false confirmations, now withdrawn |

Each has a regression test named in its file. `cargo test` and
`python3 -m pytest packages/modelsan/tests` should be green; if one is not, the
corresponding claim is suspect.

## 6. Reading the IR while you work

```bash
rumoca compile Model.mo --model M --emit-bitcode m.rbc
rumoca bitcode disasm m.rbc --provenance      # readable listing
rumoca bitcode emit-text m.rbc -o m.rbctxt    # editable textual IR, round-trips
```

Worked examples in [`examples/ir/`](examples/ir/README.md), format in
[bitcode-reading.md](bitcode-reading.md).

## 7. Raw data

[`runs/data/`](runs/data/) — every report is generated from these, so a
disagreement can be traced to a row.

| File | |
|---|---|
| `STATIC_INTENT_DEFAULT.jsonl` | the 848-model static run behind every current site and finding report |
| `STATIC_INTENT_POLICY.jsonl` | the same run with `--keep-parameter-chains`, for the intent-policy review |
| `STATIC_AGGREGATE.jsonl` | the run before the intent policy, kept for tracing |
| `STATIC_SOURCE_PATHS.jsonl` | the run before the aggregate rules, kept for tracing |
| `STATIC_FINAL.jsonl` | an earlier run, kept so any published figure can be traced |
| `FULLEVAL_MERGED.jsonl` | the execution campaign |
| `CONFIRM_EVAL.json` | cross-tool verdicts |
| `INSTANCES.json` | the 26 confirmed instances |
| `INSTANCES_CLASSIFIED.json` | the same 26, split into 11 declaration defects and 15 topology-specific |
| `SAMPLE.json` | the adjudicated sample, with a `reason` per draw |
| `OMCSWEEP.jsonl` | OpenModelica baseline |

Regenerate every report:

```bash
python3 tools/sweep/gen_instance_reports.py    docs/runs/data/INSTANCES.json 20
python3 tools/sweep/gen_site_reports.py        docs/runs/data/STATIC_FINAL.jsonl
python3 tools/sweep/gen_finding_reports.py     docs/runs/data/STATIC_FINAL.jsonl
python3 tools/sweep/gen_declaration_reports.py
```

## 8. Known weak points

Stated so nobody has to find them the hard way.

- **`physical-bound-permits-zero`** (1769 findings, 6.9% precise) — 26 of 30
  sampled draws were undecidable because the tool could not get a clean
  baseline. Its precision is the least well established figure here.
- **Rumoca compiles 332 of 847 models.** Everything static is over that subset,
  and it is not a random one — the models it cannot compile skew toward Fluid
  and external objects.
- **The false-positive taxonomy is not closed.** Four classes exist because
  four were noticed. A fifth would show up exactly where the fourth did: in a
  random draw someone adjudicated honestly.
