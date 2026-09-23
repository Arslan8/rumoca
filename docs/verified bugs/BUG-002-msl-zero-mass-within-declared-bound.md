# BUG-002: `Translational.Components.Mass.m` declares `min=0`, a value it cannot integrate

| | |
|---|---|
| **Severity** | Medium — latent; bites anyone parameterising a model programmatically |
| **Component** | Modelica Standard Library 4.1.0, not Rumoca |
| **Fix site** | `Mechanics/Translational/Components/Mass.mo`, the `m` declaration |
| **Trigger** | `m = 0` |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev; 17 models in the full sweep |
| **Found by** | ModelSan parameter sweep over 74 MSL example models, 2026-09-13; extended and cross-confirmed against OpenModelica over the full 847-model corpus the same day |
| **Status** | Reported, not fixed |

## Summary

MSL declares

```modelica
// Mechanics/Translational/Components/Mass.mo
parameter SI.Mass m(min=0, start=1) "Mass of the sliding mass";
equation
  m*a = flange_a.f + flange_b.f;
```

The rotational counterpart, `Rotational.Components.Inertia.J`, has the identical
defect and is filed separately as
[BUG-018](BUG-018-rotational-inertia-zero-within-declared-bound.md) — same
cause, different file to edit.

`min=0` is **inclusive**, so `m = 0` is a value the component's own
declaration says is legal. It is not: with `m = 0` the equation
`m * a = f` degenerates to `0 = f`, which no longer determines `a`. The
system loses an unknown and the solve fails with a numerical error rather
than a diagnostic about the parameter.

The bound as written is a promise the component cannot keep.

## Confirmed in two independent tools

| Model | Trigger | Failure |
|---|---|---|
| `Modelica.Mechanics.Translational.Examples.Damper` | `mass1.m = 0` | `algebraic projection did not converge at event boundary: worst scaled residual row=4 target=mass1.a value=2.5e2 ratio=2.5e12` |
| `Modelica.Mechanics.Translational.Examples.SignConvention` | `mass1.m = 0` | same class |
| `Modelica.Mechanics.Translational.Examples.WhyArrows` | `mass1.m = 0` | same class; found by the full-corpus sweep |

Each was re-run in OpenModelica 1.27.0-dev: it passes at its declared values and
**fails** at the trigger, so none is an artifact of Rumoca. The trigger reached
17 models in the full sweep.

`Translational.Examples.CompareBrakingForce` fails in Rumoca at `m = 0` but
**survives in OpenModelica**, so it is excluded from this report.
They are recorded as tool-side gaps, not as findings.

All three simulate cleanly with their declared defaults. The failure appears
only under an override that the declaration permits.

## Not an artifact of exactly zero

```console
$ rumoca compile-bitcode Damper.rbc --simulate --check --param mass1.m=0.001
[]                                          # clean

$ rumoca compile-bitcode Damper.rbc --simulate --check --param mass1.m=1e-12
"detail": "diffsol-bdf advance exhaustion failed: ODE solver error:
           Step size is too small at time = 1.77e-17"
```

`1e-12` also satisfies `min=0`, and collapses the integrator rather than
producing a clean rejection. The usable domain has a lower edge somewhere
above the declared one, and the declaration does not say where.

## MSL knows how to write this bound

The same library gets it right elsewhere:

```modelica
// Modelica.Mechanics.Translational.Sources.QuadraticSpeedDependentForce
parameter SI.Velocity v_nominal(min=Modelica.Constants.eps)
  "Nominal speed";
...
f = -f_nominal*(v/v_nominal)^2;
```

`min=Modelica.Constants.eps` correctly forbids zero for a parameter used as a
divisor. `Mass` uses `min=0` for a coefficient that equally must not vanish. The
asymmetry, within one library, is the finding.

## Suggested fix

Either tighten the bound:

```modelica
parameter SI.Mass m(min=Modelica.Constants.small, start=1);
```

or keep `min=0` and state the degenerate case explicitly, so a user setting it
gets a message naming the parameter instead of a solver error naming `mass1.a`.

Tightening is the smaller change and matches what `QuadraticSpeedDependentForce`
already does.

## Reproducing

```bash
cargo xtask repo modelica-deps ensure
export PYTHONPATH=packages/rumoca-bitcode:packages/modelsan
MSL="target/msl/ModelicaStandardLibrary-4.1.0"

python3 -m modelsan.cli \
  "$MSL/Modelica 4.1.0/Mechanics/Translational/Examples/Damper.mo" \
  --model-name Modelica.Mechanics.Translational.Examples.Damper \
  --source-root "$MSL" --rumoca ./target/debug/rumoca --t-end 0.5
```

## Caveat worth stating

This is a *fragility*, not a crash in correct usage. Nobody simulating a damper
deliberately sets the mass to zero. It matters because parameter sweeps,
optimisers, and calibration loops set parameters programmatically and have only
the declared bounds to go on — and the declared bound here says zero is fine.
