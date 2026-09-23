# BUG-015: `IdealGear.ratio` is an unbounded `Real` that decouples the gear at zero

| | |
|---|---|
| **Severity** | Medium — a core Rotational component |
| **Target** | MSL 4.1.0, `Modelica.Mechanics.Rotational.Components.IdealGear` |
| **Trigger** | `ratio = 0` |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev |
| **Found by** | OMC-backed sweep of 827 models, batch cross-confirmed, 2026-09-14 |
| **Status** | Reported, not fixed |

## Summary

```modelica
// Mechanics/Rotational/Components/IdealGear.mo
parameter Real ratio(start=1) "Transmission ratio (flange_a.phi/flange_b.phi)";
equation
  phi_a = ratio*phi_b;
  0 = ratio*flange_a.tau + flange_b.tau;
```

`ratio` is a plain `Real` with no bound at all — not even a type to inherit one
from. At `ratio = 0` both equations degenerate together:

* `phi_a = 0`, so `phi_b` is no longer related to `phi_a` by anything.
* `flange_b.tau = 0`, so no torque is transmitted either.

The gear stops coupling its two flanges in both the kinematic and the force
sense, and whatever the rest of the drivetrain relied on it to determine is left
undetermined.

A transmission ratio of zero is not a gear. Negative ratios *are* meaningful —
they reverse direction — so the bound wanted here excludes only zero, not the
sign.

## Confirmed

Via `Modelica.Mechanics.Rotational.Examples.ElasticBearing`, which simulates
cleanly at its declared values and fails in both tools at
`idealGear.ratio = 0`.

## Why this one is easy to reach by accident

Unlike a mass or an inductance, a gear ratio is exactly the kind of parameter a
sweep or an optimiser varies — it is a design variable, not a material
constant. A search over ratios that includes or crosses zero is an ordinary
thing to write, and nothing in the declaration says not to.

## Suggested fix

Zero is the only bad value, and `min` cannot express "nonzero" on its own. Two
options:

```modelica
// if the intended use is reduction only
parameter Real ratio(start=1, min=Modelica.Constants.small);

// otherwise state it where a user will see it
assert(abs(ratio) > Modelica.Constants.eps,
       "IdealGear: transmission ratio must be nonzero");
```

The assertion is probably the better fit, since it keeps negative ratios legal.
