# Static/source-supported candidates: `opamp-design-pi`

**3 report instances**

[Back to Static/source-supported candidates](../candidates.md) · [Overview](../README.md)

## Common decision rule

The source binding is C=T/k/R1. The reported parameter is an explicit divisor with no zero handling. At the zero witness the nominal design cannot produce finite capacitance. This declaration has a reproduced instance in the evidence; a declaration-only report is linked to that shared proof, not claimed to have its own executable model.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0645](../candidate/DECL-0645.md) | — | `R1` | Source/semantic review | [DECL-pi-r1-6.md](../../bugs/DECL-pi-r1-6.md) |
| [FINDING-00800](../candidate/FINDING-00800.md) | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit | `PIA.R1` | OMC: `witness-admitted-with-warning` | [FINDING-controlcircuit-pia-r1-unbounded.md](../../bugs/FINDING-controlcircuit-pia-r1-unbounded.md) |
| [FINDING-01020](../candidate/FINDING-01020.md) | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.PI | `R1` | OMC: `unresolved-baseline-fails` | [FINDING-pi-r1-unbounded.md](../../bugs/FINDING-pi-r1-unbounded.md) |
