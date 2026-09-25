# MSL: a resistance computed from a voltage in DCPM_Drive

**Status:** new — not in the upstream tracker as of the 2026-09-24 snapshot
**Found:** 2026-09-24 by `QuantitySan`'s `binding-unit-conflict` check, on its
first sweep of the library. No issue-specific code was involved.

## The defect

`Modelica/Electrical/Machines/Examples/DCMachines/DCPM_Drive.mo:81`

```modelica
Analog.Basic.Resistor resistor(R=0.05*dcpmData.VaNominal/1000)
```

`dcpmData.VaNominal` is a voltage. Dividing it by the dimensionless literal
`1000` leaves a voltage, and the result is bound to `R`, declared
`SI.Resistance`:

```
declared   Ohm    kg.m2.s-3.A-2
binding           kg.m2.s-3.A-1      reads VaNominal[V]
```

The `1000` is standing in for a current — almost certainly the nominal
armature current — written as a bare number. Numerically the model runs and
gives the intended answer at the default rating.

## Why it matters

The value is right only by coincidence of the present parameter set. The
declaration says "5% of nominal voltage per 1000 amperes" while the author
meant "5% of nominal impedance". Re-rate the machine — change `VaNominal`
without changing the hidden 1000 — and the resistor no longer represents 5% of
anything. A parameter that silently stops meaning what it says is worse than
one that is visibly wrong.

This is the same mechanism as upstream [#4078] and [#4079], where a capacitance
is bound to the reciprocal of an inductance. In all three the declaration and
its own binding disagree dimensionally, and in all three the equations are
silent because nothing is inconsistent *between* equations.

## Suggested fix

Bind the resistance to a current the model already names, so the dimensions
close and the intent is stated:

```modelica
Analog.Basic.Resistor resistor(R=0.05*dcpmData.VaNominal/dcpmData.IaNominal)
```

## Detection

`QuantitySan.binding-unit-conflict`, severity high. Pinned by
`packages/modelsan/tests/test_quantity.py::
test_a_resistance_bound_to_a_voltage_over_a_bare_number_is_a_conflict`.

The check only claims a conflict when the binding reads at least one variable
carrying a dimensional unit; a bare numeric binding is how every parameter in
the library is written and is never reported. See
[the pattern catalogue](../method/recurring-issue-patterns.md), P1.
