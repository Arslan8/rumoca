# LIMITATION-002: no solver-tolerance flag, so small trajectory differences cannot be attributed

| | |
|---|---|
| **Kind** | Capability gap that limits differential testing, not a defect in any model |
| **Component** | `rumoca compile-bitcode --simulate` |
| **Found by** | Building the trajectory-differential detector, 2026-09-13 |
| **Status** | Documented |

## What is missing

`compile-bitcode --simulate` exposes `--t-end` and `--dt` and nothing else:

```console
      --t-end <T_END>       Simulation end time [default: 1]
      --dt <DT>             Fixed output interval. Omitted lets the runtime choose
```

There is no way to set the integrator's relative or absolute tolerance.

## Why it matters for finding bugs

Comparing Rumoca's trajectory against OpenModelica's is the strongest available
soundness check: it tests the answer, not just whether the model was accepted.
But Rumoca's diffsol BDF and OMC's DASSL each run at their own default
tolerance, and two correct integrators at different tolerances disagree.

Measured on models both tools accept, at defaults:

| Model | Variable | Rumoca | OMC | Relative |
|---|---|---|---|---|
| `Rotational.Examples.ElasticBearing` | `housing.flange_a.tau` | 1.9774781e-3 | 1.9845113e-3 | 0.35% |
| `Translational.Examples.Damper` | `damper1.f` | -0.2282128 | -0.22797897 | 0.10% |

Neither is a defect. With a tolerance flag the question is settled directly:
tighten both and see whether the gap shrinks. Without one, a sub-percent
difference cannot be attributed to either tool, so the detector cannot use a
tight threshold and loses sensitivity to genuinely small-but-real errors.

## What the detector does instead

Two compensations, both of which cost sensitivity:

1. **A 5% threshold** rather than the 0.1% a tolerance-matched comparison could
   justify.
2. **Scaling by each signal's own range** over the run rather than its
   instantaneous value. Pointwise relative error reports a finding every time a
   quantity decays through zero — `damper1.f` at 8.3e-4 against 9.4e-4 is a 12%
   relative difference and a 1.1e-4 absolute one, on a force of order 1.

Both are calibrated in `tools/sweep/tests/test_compare_scaled.py`, which pins
that solver noise, a 2% offset and a decaying tail stay quiet while a 20% error,
a sign flip and a NaN all fire.

## What would close it

`--rtol` and `--atol` on `compile-bitcode --simulate`, passed through to the
integrator. The runtime already has them; only the surface is missing.

That would allow the convergence test that makes a divergence a finding: run
both tools at successively tighter tolerances, and report only differences that
do **not** shrink.
