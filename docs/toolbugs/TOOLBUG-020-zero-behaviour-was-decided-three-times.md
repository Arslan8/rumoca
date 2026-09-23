# TOOLBUG-020: three detectors decided what zero means, and disagreed

| | |
|---|---|
| **Component** | `modelsan.sanitizers.{divisor,physical,structure}` |
| **Severity** | High — the largest false-positive class in the project, and a wrong headline number |
| **Found by** | Independent review of the published reports, 2026-09-16 |
| **Status** | Fixed. One shared contract; 16 regression cases in `tests/test_zero_contracts.py`. |

## The defect

`Modelica.Electrical.Analog.Basic.Inductor.L` reaches a denominator in the
*solved* DAE, so DivisorSan called it a divide-by-zero. Its declared quantity
is an inductance, so PhysicalSan called it a missing positivity bound. The
component's own documentation says `L` may be zero, at which point the element
is an ideal short and the constitutive equation `L*der(i) = v` becomes `v = 0`.

Two of the three were wrong about the same parameter for different reasons, and
neither could see the third. **1448 reports across ten component families** came
from that disagreement.

## Zero is not one thing

| Constitutive equation | At zero | Classification |
|---|---|---|
| `L*der(i) = v` | `v = 0`, an ideal short | `ALGEBRAIC_LIMIT` |
| `m*a = f_a + f_b` | a force balance | `ALGEBRAIC_LIMIT` |
| `Q_flow = G*dT` | no heat flows | `FEATURE_DISABLED` |
| `flow = level/R` | undefined | `DIRECT_DIVISOR` |

The first three are supported limits of the physics the component models. Only
the fourth is a defect, and a detector that cannot tell them apart reports all
four or none.

## The fix

One classification, computed once, consulted by all three detectors, with
provenance on every result: `behavior`, `confidence` (proven / declared /
assumed), `source` (equation / bound / class_catalog / user_config), `reason`
and `canonical_declaration`. The design is in
[`../method/zero-behavior-contracts.md`](../method/zero-behavior-contracts.md).

| | before | after |
|---|---:|---:|
| `physical-bound-permits-zero` | 1769 | 295 |
| `physical-domain-unenforced` | 2033 | 664 |
| `physical-invariant-violated` | 134 | 0 |
| `divisor-reachable-zero` | 1506 | 1465 |
| reclassified as a supported limit | 0 | 2973 |
| **defect claims** | **5486** | **2468** |

The last two rows moved again after this was first written:
[TOOLBUG-022](TOOLBUG-022-a-violated-invariant-never-consulted-the-contract.md)
found that the violation path never asked the contract at all.

## The headline number changed

Of the 26 execution-confirmed instances, **15 rest on a value the component
documents as supported** — a massless body, an ideal short, a zero-capacitance
open circuit. The execution evidence is unchanged: those models do fail at those
values. What changed is the claim it supports.

"`Mass.m` should forbid zero" is a claim about
`Mechanics.Translational.Components.Mass`, and it is false — the declaration
carries `min = 0` deliberately and massless bodies are a normal idiom. "This
model is singular with `mass1.m = 0`" is a claim about `Examples.Damper`, and it
is true. The second is weaker, and it is the one the evidence supports.

**11 remain declaration defects** — the flux-tube divisors, `InvertingAmp.f`,
the op-amp supply rails. The other 15 are filed under
`STRUCTURE_DEGENERATES_AT_ZERO`, which names the model rather than the
component, and are recorded in `runs/data/INSTANCES_CLASSIFIED.json`.

This is the second time in this project that removing false positives also
removed true ones and left the result stronger. The first was
[TOOLBUG-013](TOOLBUG-013-type-level-bounds-dropped.md).

## Two defects found while fixing it

**A rate under another name.** `Mass` writes `m*a = f` with `der(v) = a`
alongside, so `m` multiplies an *algebraic* variable and the inference called it
`FEATURE_DISABLED` rather than `ALGEBRAIC_LIMIT`. Both suppress, so the output
was right and the reason was wrong — in a report a reader is meant to check,
that is a defect.

**`min = -Modelica.Constants.inf` read as no bound.** Found by adjudicating a
fresh sample: 6 of 40 `physical-domain-unenforced` draws are off-diagonal
inertia-tensor elements declared `I_21(min=-C.inf)`. That is the author writing
down that the full signed range is intended, and reporting it as "nothing bounds
this declaration" contradicts the declaration being quoted. `Modelica.Constants
.inf` is the largest representable double, not IEEE infinity, so the obvious
test with `math.isinf` finds nothing.

## What the surviving strata look like

`physical-bound-permits-zero` now holds 295 findings at **2.6%** precision (39
surviving draws). The contract removed its true positives along with its false ones,
because its true positives *were* the mass-and-inertia cases now filed as
topology-specific. A stratum at 2.6% is not worth reporting as defects, and that
is a result about the rule rather than about the library.
