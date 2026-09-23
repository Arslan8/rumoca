# Results

> **Verifying this?** Start at [VERIFY.md](VERIFY.md) — prerequisites,
> the command that recomputes each number, and the known weak points.

Everything this project has found, at every strength of evidence, as
individually addressable files. Nothing lives only in a summary table and
nothing lives only in a temp directory.

## The three tiers, and why they are not merged

The single most important number here is **not** the total. Merging these tiers
would turn ~2200 files into "2200 bugs" when 26 have been proven, and that claim
would not survive one reviewer opening one file.

| Tier | Evidence | Count | Where |
|---|---|---|---|
| **Confirmed declaration defect** | fails in **two independent tools**, and the component's contract does not admit the value | **11 instances** | [`v2/bugs/`](v2/bugs/README.md) · [`verified bugs/`](verified%20bugs/INSTANCES.md) |
| **Confirmed topology-specific** | fails in two tools, but the value is one the component documents as a supported limit | **15 instances** | [`runs/data/INSTANCES_CLASSIFIED.json`](runs/data/INSTANCES_CLASSIFIED.json) |
| **Candidate** | static analysis of the canonical DAE reached it | **5503 occurrences**, of which **2371 make a defect claim** | [`v2/bugs/`](v2/bugs/README.md) · [`site-reports/`](site-reports/README.md) |
| **Latent** | a declaration permits a physically impossible value; nothing observed | **911 declarations** over **17 SI types** | [`v2/bugs/`](v2/bugs/README.md) |

**Start at [`v2/bugs/`](v2/bugs/README.md).** It holds one file per instance across
every tier and each one names the sanitizer responsible and carries the
commands to check it.

### The confirmed tier was split, and the headline number changed

This project reported **26 confirmed defects** for most of its life. An external
review established that 15 of them rest on a value the component *documents as
supported*: a massless body, an ideal short, a zero-capacitance open circuit.
The execution evidence is unchanged — those models do fail at those values — but
the claim they support is not "this declaration is wrong". It is "this topology
is singular at this value", which is a fact about the model and its
initialization, and whose fix is in the model or its documentation.

**Quote 11 as the declaration-defect count.** The other 15 are real observations
filed under a weaker and more accurate claim, not withdrawn. See
[TOOLBUG-020](toolbugs/TOOLBUG-020-zero-behaviour-was-decided-three-times.md).

Quote **11** as the declaration-defect count and **17** as the SI type defects.
The 15 topology-specific instances are a separate claim and must not be added
to either. The rest is reach and blast radius.

## The connection graph

[connection-graph.md](method/connection-graph.md) — components, ports and the
nodes that join them, from [`runs/data/NETWORK_CENSUS.json`](runs/data/NETWORK_CENSUS.json).

| | |
|---|---:|
| models with a graph | 312 of 333 |
| nodes / ports | 3,955 / 17,740 |
| components with a complete power expression | 5,630 |

Built because every other analysis here has one declaration or one equation as
its subject, and a passive component's power balance — checkable from its ports
alone, with no contract saying what the component is for — has no form at that
level. The conserved half of every connection had never been exported
([TOOLBUG-025](toolbugs/TOOLBUG-025-the-conserved-half-was-never-exported.md)).

It also corrected a claim on this page. The structural findings were explained
here as sub-circuits whose *unconnected connectors* leave a `flow = 0` without a
matching unknown. Measured against the graph, **20 of the 24** are explained by
a **boundary port** — an interface pin of the model itself, wired inside and
open on the other side, which nothing forces — and only **4** by an unconnected
connector. None is unexplained. The conclusion held; the mechanism named for it
did not.

## Precision

[precision.md](findings/precision.md) — **26.7% population-weighted**
[18.0, 31.5] over the **1733 defect claims** in a run of 5503 findings. The
other 3770 findings make no defect claim: a division proved safe, a question
the analysis could not decide, a component that documents the value it holds,
or — 638 of them — a question put to the author.

**Read the rows, not the total.** The physical claims whose premise a component
contract or a source division establishes are **100%** precise over 224
findings. The consequence claims are **15.9%** over 1509. The aggregate moved
from 44.0% to 26.7% when the [intent
policy](method/physical-intent-policy.md) re-addressed 638 findings as
questions: no detector got worse, the high-precision stratum got smaller, and
an average over two unlike populations follows their sizes.

The independent review of the v2 reports in
[`v2/verified/`](v2/verified/README.md) puts **830** report instances in the
execution-confirmed tier, 3373 as false positives or explicit non-defects and
2193 unresolved — the advisories among them, because an unanswered question is
undecided rather than wrong.

## Three granularities over the same run

| | Answers | Count |
|---|---|---|
| [`declaration-sites/`](declaration-sites/README.md) | a declaration permits an impossible value | 911 |
| [`site-reports/`](site-reports/README.md) | one declaration, one claim — **what you edit** | 1075 |
| [`findings/instances/`](findings/instances/README.md) | one occurrence — **what you reproduce** | 10942 |

The ratio is not padding: the top 10 sites carry 50% of all findings (one
inherited heat port recurs in 156 models), while **608 of 1075 sites are reached
by exactly one model**. And 4174 findings — 38% — are flagged as noise in place:
four heat-port temperature declarations, where "nothing stops this going below
absolute zero" is true of a state nobody parameterises. Filter with
`grep -L 'Probably not worth acting on'`.

## Confirmed — two layers

| | Answers | Example |
|---|---|---|
| fix site, `BUG-002` … `BUG-019` | which declaration to change | `Mass.m` declares `min=0` |
| instance, `BUG-020` … `BUG-045` | which instance failed, where | `Damper.mo:6`, `mass1`, at `m = 0` |

`Damper.mo` instantiates three masses; all three were confirmed separately and
have their own file and line reference.

## Studies — findings that are not a bug list

| | |
|---|---|
| [documented-sign-latitude.md](findings/documented-sign-latitude.md) | MSL states `Basic.Resistor`'s R "is allowed to be positive, zero, or negative". Four of this project's rules asserted otherwise. |
| [sentinel-parameters.md](findings/sentinel-parameters.md) | 74 Spice3 declarations encoding "unset" as `-1e40`, 12 on quantities that cannot be negative. |
| [si-type-bounds.md](findings/si-type-bounds.md) | Where MSL's declared domains come from, and the three ways components inherit a bound they cannot keep. |
| [min0-census.md](findings/min0-census.md) | 326 `min=0` declarations against 147 guarded, and why the text-level check is unusable at 23% precision. |

## Tool defects — not results

[`toolbugs/`](toolbugs/README.md). Defects in Rumoca and in ModelSan itself,
kept strictly out of the counts above. Two of them changed the results:

- [TOOLBUG-010](toolbugs/TOOLBUG-010-divisorsan-misread-non-literal-min.md) — read `min=Modelica.Constants.eps` as no bound, producing **two confirmed findings against correct models**. Both withdrawn.
- [TOOLBUG-011](toolbugs/TOOLBUG-011-bitcode-cannot-encode-unary-plus.md) — unary plus had no encoding, so an artifact failed its own import.

## Raw run data

[`runs/data/`](runs/data/) — the JSONL and JSON outputs every report above is
derived from, committed so a result survives the machine it was produced on.

| File | What |
|---|---|
| `STATIC_FINAL.jsonl` | full-corpus static run, 847 models |
| `FULLEVAL_MERGED.jsonl` | the execution campaign |
| `CONFIRM_EVAL.json` | cross-tool confirmation verdicts |
| `INSTANCES.json` | the confirmed instance list the `BUG-020+` files are generated from |
| `OMCSWEEP.jsonl` | OpenModelica baseline |
| `foldcmp.jsonl` | `--no-fold-parameter-bindings` comparison, 847 models |

## Regenerating every report

```bash
python3 tools/sweep/gen_instance_reports.py    docs/runs/data/INSTANCES.json 20
python3 tools/sweep/gen_site_reports.py        docs/runs/data/STATIC_FINAL.jsonl
python3 tools/sweep/gen_declaration_reports.py
```

## Reading the artifacts

[bitcode-reading.md](bitcode-reading.md) — `rumoca bitcode disasm` renders an
`.rbc` as a readable listing with the expression graph resolved, against `dump`
which prints the serialization. For the same circuit: 11 KB against 256 KB.

## Standing rule

A new finding gets a new file, at the tier its evidence supports, at the time it
is found. A result that exists only in a terminal, a summary line, or a
scratch directory is a result that is already lost.

## Coverage change from the compiler fixes (this pass)

None of these are new findings. They are how much more of each model the
detectors can now see, which is the thing that caps every number above.

| | before | after |
|---|---:|---:|
| Divisor occurrences reachable by the traversal | 2923 | **3689** (+26%) |
| Models where StructureSan reports a matching failure | 166 | **24** |
| Structural findings, corpus-wide | 1324 | **63** |
| `STATE_WITHOUT_DERIVATIVE_CONSTRAINT`, all false | 246 | **0** |

The extra divisor reach comes from array `for` equations and function call
arguments, neither of which was in the artifact at all
([TOOLBUG-014](toolbugs/TOOLBUG-014-structured-equations-not-exported.md),
[TOOLBUG-015](toolbugs/TOOLBUG-015-function-bodies-not-carried.md)). The
structural collapse comes from four separate incidence defects
([TOOLBUG-016](toolbugs/TOOLBUG-016-incidence-edges-lost-and-invented.md)),
every one of which had been producing findings against models the compiler had
already proved balanced.

`Modelica.Electrical.Analog.Examples.Lines.SmoothStep` is the clearest single
case: 115 of its equations were array families that no consumer could see, and
its parameter `N50` went from 100 visible divisor sites to 306.

**The 63 remaining structural findings are not claimed as MSL defects.** 22 of
the 24 models are sub-circuit building blocks (`.OpAmpCircuits.*`,
`.Examples.Utilities.*`, `.Components.*`) compiled standalone, where unconnected
interface connectors make a structurally singular system that still balances by
count — a correct result about how the model was compiled, not about the model.
The other two are clocked examples whose coordinates the schema does not yet
carry, so they are not adjudicable either way.
