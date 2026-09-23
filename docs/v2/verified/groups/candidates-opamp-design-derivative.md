# Static/source-supported candidates: `opamp-design-derivative`

**3 report instances**

[Back to Static/source-supported candidates](../candidates.md) · [Overview](../README.md)

## Common decision rule

The source binding is C=T/R1. The reported parameter is an explicit divisor with no zero handling. At the zero witness the nominal design cannot produce finite capacitance. This declaration has a reproduced instance in the evidence; a declaration-only report is linked to that shared proof, not claimed to have its own executable model.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0629](../candidate/DECL-0629.md) | — | `R1` | Source/semantic review | [DECL-derivative-r1-6.md](../../bugs/DECL-derivative-r1-6.md) |
| [FINDING-00858](../candidate/FINDING-00858.md) | Modelica.Electrical.Analog.Examples.OpAmps.HighPass | `derivative.R1` | OMC: `witness-admitted-with-warning` | [FINDING-highpass-derivative-r1-unbounded.md](../../bugs/FINDING-highpass-derivative-r1-unbounded.md) |
| [FINDING-00986](../candidate/FINDING-00986.md) | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Derivative | `R1` | OMC: `unresolved-baseline-fails` | [FINDING-derivative-r1-unbounded.md](../../bugs/FINDING-derivative-r1-unbounded.md) |
