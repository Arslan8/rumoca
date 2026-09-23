# BUG-005: `MultiBody.Parts.Rotor1D` repeats the `min=0` inertia bound

| | |
|---|---|
| **Severity** | Medium — latent, same class as BUG-002 |
| **Component** | Modelica Standard Library 4.1.0, `Modelica.Mechanics.MultiBody.Parts.Rotor1D` |
| **Found by** | `min=0` source census + isolated-shape confirmation, 2026-09-13 |
| **Status** | Reported, not fixed |

## Summary

[BUG-002](BUG-002-msl-zero-mass-within-declared-bound.md) reported `min=0` on
`Translational.Components.Mass` and `Rotational.Components.Inertia`. The same
bound, on the same equation shape, also appears in MultiBody — a different
package, not covered by that report:

```modelica
// Mechanics/MultiBody/Parts/Rotor1D.mo:7  (and again at :78, the inner variant)
parameter SI.Inertia J(min=0,start=1)
...
// :167
w = der(phi);
a = der(w);
if exact then
  J*a = flange_a.tau + flange_b.tau - nJ*der(w_a);
else
  J*a = flange_a.tau + flange_b.tau;      // :174
end if;
```

`J` is the sole coefficient of `a`, and `a = der(w)`. At `J = 0` the equation
states `0 = tau` and no longer determines `a`. `min=0` admits that value.

## Reproducer

Rumoca cannot yet compile MultiBody, so the shape is isolated instead — the
three lines above with the bearing torque dropped:

```modelica
model Rotor1DShape "Rotor1D's equation shape, isolated"
  parameter Real J(min = 0) = 1 "as Modelica.Mechanics.MultiBody.Parts.Rotor1D";
  parameter Real tau = 1;
  Real phi(start = 0, fixed = true);
  Real w(start = 0, fixed = true);
  Real a;
equation
  w = der(phi);
  a = der(w);
  J * a = tau;          // Rotor1D line 174, with no bearing torque
end Rotor1DShape;
```

```console
$ rumoca compile Rotor1DShape.mo --model Rotor1DShape --emit-bitcode r.rbc
$ rumoca compile-bitcode r.rbc --simulate --check --t-end 0.5
[]                                          # J = 1, clean

$ rumoca compile-bitcode r.rbc --simulate --check --t-end 0.5 --param J=0
[
  {
    "kind": "simulation-failure",
    "detail": "solve-IR evaluation failed: non-finite (inf) value computed for `a`",
    "parameters": [ { "name": "J", "value": 0.0 } ]
  }
]
```

## Scope of this report, stated plainly

What is **confirmed**: the declaration exists in MSL at the cited lines, and the
isolated equation shape is singular at `J = 0`.

What is **not**: `Rotor1D` itself was not simulated, because Rumoca does not yet
support MultiBody. A whole-model run could in principle be non-singular if some
other equation determined `a` — but `a` appears only in the `J*a` equation and
in `a = der(w)`, so there is no such equation. This is inspection, not
execution, and is labelled as such.

## Fix

The same one BUG-002 proposes, and the one MSL already applies in
`QuadraticSpeedDependentForce`:

```modelica
parameter SI.Inertia J(min=Modelica.Constants.small, start=1);
```

Both declarations need it — line 7 and line 78.
