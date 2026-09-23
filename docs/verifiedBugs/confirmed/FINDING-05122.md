# FINDING-05122: SwitchedRLC divides directly by unconstrained resistance

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | example-rlc-resistance |
| Model | SwitchedRLC |
| Target | R |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-switchedrlc-r-divzero.md](../../v2/bugs/FINDING-switchedrlc-r-divzero.md) — reviewed as `FINDING-05122-switchedrlc-r.md`, which a later run renamed |
| Original SHA-256 | 511fa2517246cfabb7b85b798442c0743340c619f5ac2e54fd75dee18d011d00 |

## Verification and root cause

The local example declares R without a bound and computes i_R=V/R. R=0 is an immediate divide by zero; unlike the MSL Basic.Resistor formulation, this hand-written example chose explicit reciprocal form.

## Source evidence

Compiler/source-resolved declaration: `/data/mrumoca/rumoca/examples/models/SwitchedRLC.mo:9`. Role: `parameter`; binding: `100`; effective min: `None`; effective max: `None`. 

[/data/mrumoca/rumoca/examples/models/SwitchedRLC.mo — source snapshot](../evidence/sources/20d217108780f0d6-SwitchedRLC.mo)

```modelica
7:   parameter Voltage Vb = 24 "Battery voltage";
8:   parameter Inductance L = 1;
9:   parameter Resistance R = 100;
10:   parameter Capacitance C = 1e-3;
11:   Voltage Vs;
12:   Voltage V;
```

[/data/mrumoca/rumoca/examples/models/SwitchedRLC.mo — source snapshot](../evidence/sources/20d217108780f0d6-SwitchedRLC.mo)

```modelica
7:   parameter Voltage Vb = 24 "Battery voltage";
8:   parameter Inductance L = 1;
9:   parameter Resistance R = 100;
10:   parameter Capacitance C = 1e-3;
11:   Voltage Vs;
12:   Voltage V;
13:   Current i_L;
14:   Current i_R;
15:   Current i_C;
16: equation
17:   Vs = if time > 0.5 then Vb else 0;
18:   i_R = V/R;
19:   i_C = C*der(V);
20:   i_L = i_R + i_C;
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/51a47159af620668.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `R=0` | reported-failure |

Diagnostic: solve-IR evaluation failed: algebraic projection did not converge at event boundary: worst scaled residual row=1 target=i_R value=NaN ratio=NaN norm=inf row_scale=1.000000e0 scaled_tolerance=1.000000e-10

## Proposed fix

Either require/assert abs(R)>0 before i_R evaluation, or reformulate the branch implicitly as R*i_R=V if the ideal zero-resistance limit is meant to be supported. Document whether negative active resistance is valid.

## Fix validation

Test nominal, zero, supported negative resistance, and the switching event at t=0.5 without non-finite current.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/example-rlc-resistance.md) · [Index](../README.md)
