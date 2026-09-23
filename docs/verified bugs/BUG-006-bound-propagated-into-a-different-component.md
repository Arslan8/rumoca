# BUG-006: a `min=0` bound propagates into a *different* component's singular coefficient

| | |
|---|---|
| **Severity** | Medium — the bound and the failure are in different components, so no local check finds it |
| **Component** | MSL 4.1.0, `Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Der` |
| **Found by** | `min=0` source census + isolated-shape confirmation, 2026-09-13 |
| **Status** | Reported, not fixed |

## Why this is not just another BUG-002

BUG-002 and BUG-005 are local: the parameter with the bad bound is the
coefficient that vanishes, in the same equation, in the same component. A
checker that looks at one component at a time finds them.

This one is not local. The parameter carrying the bound is an *amplification
factor*; the coefficient that vanishes is a *capacitance* in a different
component, reached through a derived parameter:

```modelica
// Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Der.mo
parameter Real k(final min=0)=1 "Desired amplification at frequency f";
parameter SI.Frequency f "Frequency";
parameter SI.Resistance R=1000;
parameter SI.Capacitance C=k/(2*pi*f*R)
  "Calculated capacitance to reach desired amplification k";
...
Basic.Capacitor c(final C=C);
```

`Basic.Capacitor` contributes `C*der(v) = i`. At `k = 0` the binding equation
gives `C = 0`, the capacitor equation degenerates to `0 = i`, and `v` is no
longer determined.

`Capacitor` cannot defend against this: its own `C` has no bound to tighten, and
the offending value arrives through a `final` binding. `Der` cannot be caught by
inspecting `Der` alone either — nothing in `Der`'s own equation section divides
by or multiplies `k`.

## Reproducer

`Der` cannot be simulated standalone by *either* tool — it is a circuit
fragment meant to be instantiated inside a larger model, and is underdetermined
on its own:

```console
$ rumoca compile-bitcode der.rbc --simulate --check --t-end 0.5
"DAE structural proof failed: structurally singular system:
 42 matched out of 43 equations and 43 unknowns"

$ omc     # checkModel passes (43 equations, 43 variables) but:
messages = "Failed to build model:
            Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Der"
```

So the propagation path is isolated instead: the `k → C → C*der(v)` chain, with
the OpAmp replaced by a fixed current.

```modelica
model DerAmpShape "OpAmps/Der.mo: min=0 amplification propagated into a capacitance"
  parameter Real k(min = 0) = 1 "Desired amplification at frequency f";
  parameter Real f = 50;
  parameter Real R = 1000;
  parameter Real C = k / (2 * 3.141592653589793 * f * R);  // Der.mo line 8
  Real v(start = 0, fixed = true) "capacitor voltage = state";
  parameter Real i = 1e-3;
equation
  C * der(v) = i;      // Basic.Capacitor
end DerAmpShape;
```

```console
$ rumoca compile-bitcode d.rbc --simulate --check --t-end 0.5
[]                                          # k = 1, clean

$ rumoca compile-bitcode d.rbc --simulate --check --t-end 0.5 --param k=0
[
  {
    "kind": "simulation-failure",
    "detail": "solve-IR evaluation failed: non-finite derivative evaluation for state 'v'",
    "parameters": [ { "name": "k", "value": 0.0 } ]
  }
]
```

## What this says about where the analysis has to run

The chain crosses a component boundary and a parameter binding. It is visible
only after flattening, in a representation that has already resolved `C` to
`k/(2*pi*f*R)` and inlined the capacitor's equation — which is what the DAE is.
A source-level or per-component check cannot see it. That is the argument for
doing this analysis on the DAE rather than on Modelica text; see
[the census note](../findings/min0-census.md) for how badly the text-level version does.

## Scope of this report

**Confirmed**: the declarations and the binding are in MSL as cited; the
isolated propagation chain fails at `k = 0` and is clean at `k = 1`.

**Not confirmed**: `Der` itself was not simulated, because neither Rumoca nor
OpenModelica can simulate it standalone (above). The claim about `Der` is read
off the source. Confirming it end-to-end means instantiating `Der` inside a
complete circuit, which no MSL example does.

## Fix

`k` is an amplification, and zero amplification is not a meaningful request for
this circuit:

```modelica
parameter Real k(final min=Modelica.Constants.small)=1;
```
