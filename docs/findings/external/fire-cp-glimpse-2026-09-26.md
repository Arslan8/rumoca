# ModelSan on FIRE_CP_Glimpse

**Target:** <https://github.com/mhcho1994/FIRE_CP_Glimpse> (shallow clone, 2026-09-26)
**Run:** every static sanitizer over every class the repository declares.

A co-simulation framework for drones and rovers whose README states an
intention to integrate with Rumoca. Nine `.mo` files, three of them legacy
copies, declaring 49 model/block classes between them.

## Coverage first, because it bounds everything else

**6 unique models analyzed; 39 classes could not be compiled.** Whatever the
sanitizers say applies to an eighth of the repository, and the reason is our
compiler, not their models:

| Blocked by | Count | What it is |
|---|---:|---|
| `EF020` | 17 | expandable connector connections — unsupported |
| `ER002` | 9 | unresolved reference, mostly `Constants.PI` from a sibling package |
| `ED020` / `ED018` / `ED019` / `ED013` / `ED010` | 9 | unsupported DAE constructs: `sample` with a non-literal interval, function assertions, sequential algorithm reads |
| other | 4 | |

Expandable connectors alone account for nearly half. This repository is a
reasonable stress case for Rumoca's frontend, and that is worth more to us
than the findings below.

## What was found

### 1. `RoverHighFidelity` is structurally singular — confirmed

`legacy/NGCrover/model/MFRover.mo`, also `models/MFRover.mo`.

`StructureSan` reported an unmatched equation. Rumoca's own structural proof
agrees, independently of any sanitizer:

```
[EL005] DAE structural proof failed: structurally singular system:
        116 matched out of 117 equations and 117 unknowns
```

One equation has nothing left to determine. The model cannot be simulated as
written. This is the strongest finding in the run and it does not depend on
our analysis being right — the compiler reaches it on its own.

### 2. Physical parameters are unbounded and used as divisors

Every physical parameter in the rover models is declared bare:

```modelica
parameter Real l_total = 0.278;   // [m] distance from rear axle to front axle
parameter Real tw      = 0.234;   // [m] rover trackwidth
parameter Real Lrelx   = 0.185;   // [m] longitudinal relaxation length
parameter Real r_tire  = 0.056;   // [m] rover tire radius
parameter Real mass_total = 4.177; // [kg] rover mass
```

No `min`, and each is a divisor:

```modelica
ay       = thr*thr/l_total*tan(-delta);   // MFRover.mo:429
der(psi) = thr/l_total*tan(delta);        // :433
r        = thr/l_total*tan(delta);        // :436
```

`DivisorSan` reports 58 reachable-zero sites across 19 distinct denominators
in the two rover models. A wheelbase, a trackwidth and a tire radius cannot be
zero, and nothing in the declarations says so, so any parameter sweep or
optimiser is free to pick zero. This is the same defect class as
[BUG-002](../../verified%20bugs/BUG-002-msl-zero-mass-within-declared-bound.md)
and BUG-018 in MSL: the value is fine, the *declaration* is wrong.

The fix is one attribute per declaration, e.g.
`parameter Modelica.Units.SI.Length l_total(min=Modelica.Constants.eps) = 0.278;`

### 3. Nothing in the repository declares a unit

`RoverLowFidelity`: **0 of 40 variables** carry a `unit`, a `quantity` or a
`min`. No `Modelica.Units.SI` type appears anywhere in the models. Units are
written in end-of-line comments, where no tool can read them.

This is not a defect that breaks a simulation, and it is why our largest
sanitizer cluster found nothing here: `QuantitySan` and `DimensionSan` check
declared units against each other, and there is nothing declared to check. The
MSL unit work that reproduces five upstream issues is blind on this corpus by
construction.

Adopting SI types would cost little — the comments already carry the
information — and would turn on dimensional checking, bounds checking and the
physical-invariant rules at once.

## What was reported and is not true

`StructureSan` also reported `UNMATCHED_EQUATION` (high) and
`non-square-block` on **`RoverLowFidelity`**, which simulates cleanly:
501 time points, 53 variables. Those two are false positives, recorded in
[TOOLBUG-031](../../toolbugs/TOOLBUG-031-structuresan-unmatched-equation-on-a-model-that-simulates.md).

The contrast is the useful part: the same sanitizer was right about
`RoverHighFidelity` and wrong about `RoverLowFidelity`, so the finding kind
carries no weight on its own and needs the compiler's own proof beside it.

`EMIVulnerability` and `Magnetometer` are components with unconnected inputs
(`EX002`), not standalone models; their findings describe an incomplete
fragment and are not defects.
