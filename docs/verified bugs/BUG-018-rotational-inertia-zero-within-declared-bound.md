# BUG-018: `Rotational.Components.Inertia.J` declares `min=0`, a value it cannot integrate

| | |
|---|---|
| **Severity** | Medium — latent; bites anyone parameterising a model programmatically |
| **Component** | Modelica Standard Library 4.1.0, not Rumoca |
| **Fix site** | `Mechanics/Rotational/Components/Inertia.mo`, the `J` declaration |
| **Trigger** | `J = 0` |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev; 29 models in the full sweep |
| **Found by** | OMC-backed sweep of 847 models, cross-confirmed, 2026-09-14 |
| **Status** | Reported, not fixed |

Split from [BUG-002](BUG-002-msl-zero-mass-within-declared-bound.md), which now
covers `Translational.Components.Mass.m` alone. The two share a cause and a
rationale but are **two edits to two files**, so they are filed separately.

## Summary

```modelica
// Mechanics/Rotational/Components/Inertia.mo
parameter SI.Inertia J(min=0, start=1) "Moment of inertia";
equation
  J*a = flange_a.tau + flange_b.tau;
```

`min=0` is **inclusive**, so `J = 0` is a value the component's own declaration
says is legal. It is not: at `J = 0` the equation `J*a = tau` degenerates to
`0 = tau`, which no longer determines `a`. The system loses an unknown and the
solve fails with a numerical error rather than a diagnostic naming the parameter.

The bound as written is a promise the component cannot keep.

## Confirmed

| Model | Trigger | Failure |
|---|---|---|
| `Modelica.Mechanics.Rotational.Examples.ElasticBearing` | `shaft.J = 0` | algebraic projection did not converge at event boundary |
| `Modelica.Mechanics.Rotational.Examples.ElasticBearing` | `housing.J = 0` | same class |
| `Modelica.Clocked.Examples.SimpleControlledDrive.Continuous` | `load.J = 0` | same class |

Each model passes at its declared values and fails at the trigger in **both**
tools, so none is an artifact of Rumoca. The trigger reached 29 models in the
full sweep.

Two models — `Rotational.Examples.CompareBrakingTorque` and its translational
counterpart — fail in Rumoca and **survive** in OpenModelica. They are recorded
as tool-side gaps, not as evidence for this finding.

## Not an artifact of exactly zero

`J = 1e-12` also satisfies `min=0` and collapses the integrator rather than
producing a clean rejection. The usable domain has a lower edge somewhere above
the declared one, and the declaration does not say where.

## MSL knows how to write this bound

```modelica
// Modelica.Mechanics.Translational.Sources.QuadraticSpeedDependentForce
parameter SI.Velocity v_nominal(min=Modelica.Constants.eps) "Nominal speed";
```

`min=Modelica.Constants.eps` correctly forbids zero for a parameter that must
not vanish. `Inertia` uses `min=0` for a coefficient that equally must not
vanish. The asymmetry, within one library, is the finding.

## Suggested fix

```modelica
parameter SI.Inertia J(min=Modelica.Constants.small, start=1) "Moment of inertia";
```

Or keep `min=0` and assert the degenerate case explicitly, so a user setting it
gets a message naming `J` instead of a solver error naming `a`.

## Caveat worth stating

This is a *fragility*, not a crash in correct usage. Nobody simulating a drive
train deliberately sets an inertia to zero. It matters because parameter sweeps,
optimisers and calibration loops set parameters programmatically and have only
the declared bounds to go on — and the declared bound here says zero is fine.
