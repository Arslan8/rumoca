# Precision

Measured on stratified random samples of the full-corpus static run, each drawn
before anything was looked at, every draw adjudicated.

## Current run

`STATIC_INTENT_DEFAULT.jsonl` — 5503 findings, of which **1733 are defect
claims**. Reproduce the table with `tools/sweep/precision_table.py`.

```
stratum                                  pop    n decl  TP  FP   ?  precision      95% CI
physical-zero-is-a-supported-limit      2018    —   —   —   —   —   not a defect claim
divisor-reachable-zero                  1465  266  129  34 201  31    14.5%   [ 10.5,  19.5]
physical-rule-does-not-apply             681    —   —   —   —   —   not a defect claim
physical-intent-question                 638    —   —   —   —   —   not a defect claim
physical-domain-unenforced               201    7    6   7   0   0   100.0%   [ 64.6, 100.0]
divisor-zero-unresolved                  127    —   —   —   —   —   not a defect claim
divisor-guarded-by-assertion             122    —   —   —   —   —   not a defect claim
divisor-unreachable-under-witness        121    —   —   —   —   —   not a defect claim
divisor-zero-when-parameters-equal        44   18    5   8   5   5    61.5%   [ 35.5,  82.3]
divisor-introduced-by-translation         41    —   —   —   —   —   not a defect claim
physical-bound-permits-zero               23    4    4   4   0   0   100.0%   [ 51.0, 100.0]
physical-inertia-tensor-undecided         18    —   —   —   —   —   not a defect claim
divisor-zero-at-declared-values            4    —   —   —   —   —   not a defect claim
WEIGHTED TOTAL                          1733                         26.7%   [ 18.0,  31.5]
```

`decl` is how many **distinct declarations** the draws cover, and it is there
because stratifying by finding *kind* does not stratify by declaration.

### The weighted figure fell from 44.0% and no detector got worse

The [intent policy](../method/physical-intent-policy.md) moved 638 findings
whose premise nobody established out of the two physical defect strata and into
advisories. Both surviving physical strata are still **100%** precise; they are
now 224 findings rather than 862, so the 1465-strong divisor stratum at 14.5%
dominates the average that used to be pulled up by them.

An aggregate over two populations that behave nothing alike moves when their
relative sizes move. **Read the rows, not the total** — that has been the
recommendation on this page since the first measurement, and this is the
clearest illustration of why.

The two surviving physical strata are also down to 7 and 4 surviving draws, so
their intervals are wide; both need a fresh sample drawn from the
established-premise population, which is a different population from the one
they were drawn from.

**Population-weighted precision: 26.7%**, 95% CI [18.0, 31.5].

Nine strata are excluded from the population because they make no defect
claim. `physical-intent-question` is the largest: it asks the author whether an
unusual value was intended, and a question is not a claim. Four say a division is protected, unreachable, already zero, or
introduced by the compiler rather than written by the modeller. Two say a
component documents the value it holds. `physical-inertia-tensor-undecided`
says a tensor could not be assembled. The eighth, `divisor-zero-unresolved`,
says the analysis could not decide — neither a defect claim nor a clean bill of
health, and scoring it either way would be wrong.

### `physical-bound-permits-zero` moved from 2.6% to 72.5%, and nothing improved

The stratum lost its mass-and-inertia members to the aggregate tensor pass
([TOOLBUG-023](../toolbugs/TOOLBUG-023-a-tensor-checked-one-entry-at-a-time.md)),
and **74% of what remains is one declaration**:
`Thermal.FluidHeatFlow.Media.Medium.rho`, whose `SI.Density` type carries
`min=0` while `BaseClasses/TwoPort.mo:34` writes
`V_flow = flowPort_a.m_flow/medium.rho`. Zero density divides by zero, so it is
a true positive — and the stratum is now largely that one true positive counted
154 times.

| | |
|---|---|
| findings that are true positives | **72.5%** [57.2, 83.9], 40 draws |
| *declarations* that are true positives | **4 of 11** sampled |

The first is the right number for "how much of this list is real". The second
is the right number for "how many library declarations does it implicate", and
they are 36 points apart. Quoting either one alone would mislead.

## Two corrections to earlier figures on this page

**Divisor precision was reported as 21.4% and then 21.0%**, on samples of 115
and 116 draws. Extending the sample to **266** puts it at **14.5% [10.5, 19.5]**.
The intervals overlap, so the earlier numbers were not wrong — they were
imprecise, and quoted to three significant figures as though they were not.

**`physical-invariant-violated` was reported as 100% precise on 30 draws.**
That stratum no longer exists, and the figure was wrong when it was published.
Twenty-nine of its thirty draws were `CoreParameters.GcRef`, a `final`
parameter whose binding is

```modelica
final parameter SI.Conductance GcRef = if PRef <= 0 then 0 else PRef/VRef^2/m
```

with `PRef(min=0) = 0`, so the record ships at zero and the model that consumes
it writes `if PRef <= 0 then Gc = 0` beside it. Zero is how this library
*disables core losses*. The draws were marked true positive because the value
was zero and the rule said `> 0`, without asking whether the rule applied to
the component — which is the error the whole contract mechanism exists to
prevent, committed in the adjudication rather than in the detector. See
[TOOLBUG-022](../toolbugs/TOOLBUG-022-a-violated-invariant-never-consulted-the-contract.md).

The four findings that survived the contract were `SwitchedCapacitor.R = -1` in
`CauerLowPassSC` — a component whose first line of documentation is "switched
capacitor which can represent a positive or **negative** resistance". They are
now `physical-rule-does-not-apply`. **The stratum's true precision was near
zero, not 100%.**

## The corpus still splits in two, and more sharply

| | precision | share of defect claims |
|---|---|---|
| "this declaration permits a value its component forbids" | **100.0%** | 224 |
| "this value is impossible, or breaks something" | **15.9%** | 1509 |

A claim about **what the source says** is checkable against the source and is
right. A claim about **physics or consequence** needs the component's contract,
and the quantity alone does not supply it.

The 655 unbounded-declaration findings are the defensible static result. Each
says: this declaration, and the SI type behind it, carry no bound, so a user can
write a value the physical role excludes. Thirty-nine drawn at random were
checked against the declaration and the type; all thirty-nine held.

## Agreement with the external review

`docs/verifiedBugs/` is an independent review of 6079 published reports that
labelled **3304 of them false positives**. Against the current run:

| | |
|---:|---|
| 825 | no longer reported at all |
| 2182 | reported only under a kind that makes no defect claim |
| **3007 (91%)** | **resolved** |
| 297 | still claimed as defects |

The 297 are the work queue, and they cluster:

| count | group |
|---:|---|
| 62 | `ideal-dc-machine-data` |
| 40 | `zero-machine-data-leakage` |
| 38 | `zero-machine-data-inertia` |
| 23 | `zero-space-phasor-inductance` |
| 22 | `ideal-stator-leakage` |
| 19 | `signed-machine-data-resistance` |
| 18 | `armature-zero-mechanical-term` |
| 17 | `ideal-dc-armature-ra` |

`signed-machine-data-resistance` is on that list by design rather than as
unfinished work: the review asked for zero to be permitted and negative values
still reported, so those 19 now claim `Rs >= 0` under
`elec.machine_winding_resistance.non_negative` instead of `Rs > 0`.

Most are machine parameter records, where a stray inductance or a rotor inertia
is declared in a `record` and reaches its equations only through the component
it configures. The contract propagation that carries a component's behaviour
back to the knob feeding it stops at the record boundary.

## What the three-valued divisor classification changed

The detector decides `constraints AND path AND denominator == 0` and answers
three ways rather than reporting whenever it found an assignment:

| Verdict | Divisions | What happens |
|---|---:|---|
| `UNSAT` | 2896 | suppressed, with the proof recorded |
| `SAT` | 1553 | reported, with the witness |
| `UNKNOWN` | 632 | reported as *unresolved*, never as confirmed |

Of 5081 divisions in the corpus, **57% are proved safe** — by an assertion, by
interval propagation, or by a contradictory path. That is recorded per model in
the run under `divisions`, because a suppressed finding leaves no other trace.

**Every defect claim from this detector carries a witness whose residual is
exactly zero, the active path condition, and the constraints consulted.**

## What the adjudication cost and bought

The first measurement returned 30.8%. Finding out why it was wrong is most of
the value here — five defects, four of them in the compiler or the sanitizer
rather than in any model:

| | effect |
|---|---|
| [TOOLBUG-013](../toolbugs/TOOLBUG-013-type-level-bounds-dropped.md) — a type's `min` never reached the DAE | **5643 findings, 52% of the run** |
| `SI.TemperatureDifference` shares `quantity="ThermodynamicTemperature"` with the absolute type and is legitimately negative | 3017 → 0, the kind no longer exists |
| violations reported against a value the declaration explicitly permits (`I_31(min=-C.inf)`) | 318 → 0 |
| array-valued bounds (`min=zeros(m)`) read as absent | 6 of 30 in one stratum |
| [TOOLBUG-020](../toolbugs/TOOLBUG-020-zero-behaviour-was-decided-three-times.md) — three detectors deciding separately what zero meant | **1448 reports across ten families** |
| [TOOLBUG-023](../toolbugs/TOOLBUG-023-a-tensor-checked-one-entry-at-a-time.md) — an inertia tensor checked one entry at a time, and a resistance judged by its SI quantity | **268 reports, and a tensor with a negative eigenvalue it would have passed** |

Findings went 10942 → 5503 and defect claims 10942 → 2371. The count fell by
78% and the result got stronger, which is the point: most of what was removed
was never a finding.

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
    --out docs/runs/data/STATIC_AGGREGATE.jsonl
python3 tools/sweep/sample_for_adjudication.py docs/runs/data/STATIC_AGGREGATE.jsonl 40
python3 tools/sweep/adjudicate_divisors.py docs/runs/data/SAMPLE.json
python3 tools/sweep/precision_table.py
```

`precision_table.py` refuses to score a stratum whose surviving draws are
unadjudicated, and prints which sample each figure came from.

## The honest summary

The confirmed tier is **11 declaration defects** and **15 topology-specific
instances**, split in [RESULTS.md](../RESULTS.md) and recorded per instance in
[`../runs/data/INSTANCES_CLASSIFIED.json`](../runs/data/INSTANCES_CLASSIFIED.json).

The static tier is 5503 findings, of which 1733 are defect claims at **26.7%**,
**224 of them physical claims with an established premise, at 100%**, and 638
advisories that ask the author a question rather than making a claim at all.
Quote 224 as the defensible static number for the physical detector, and say
what it is a statement about: declarations whose component contract or whose
own arithmetic establishes the rule, not failures.
