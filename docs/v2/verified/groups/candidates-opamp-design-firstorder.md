# Static/source-supported candidates: `opamp-design-firstorder`

**5 report instances**

[Back to Static/source-supported candidates](../candidates.md) · [Overview](../README.md)

## Common decision rule

The source binding is C=T/R2. The reported parameter is an explicit divisor with no zero handling. At the zero witness the nominal design cannot produce finite capacitance. This declaration has a reproduced instance in the evidence; a declaration-only report is linked to that shared proof, not claimed to have its own executable model.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0641](../candidate/DECL-0641.md) | — | `R2` | Source/semantic review | [DECL-firstorder-r2-7.md](../../bugs/DECL-firstorder-r2-7.md) |
| [FINDING-00805](../candidate/FINDING-00805.md) | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit | `firstOrder1A.R2` | OMC: `witness-admitted-with-warning` | [FINDING-controlcircuit-firstorder1a-r2-unbounded.md](../../bugs/FINDING-controlcircuit-firstorder1a-r2-unbounded.md) |
| [FINDING-00812](../candidate/FINDING-00812.md) | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit | `firstOrder2A.R2` | OMC: `witness-admitted-with-warning` | [FINDING-controlcircuit-firstorder2a-r2-unbounded.md](../../bugs/FINDING-controlcircuit-firstorder2a-r2-unbounded.md) |
| [FINDING-00937](../candidate/FINDING-00937.md) | Modelica.Electrical.Analog.Examples.OpAmps.LowPass | `firstOrder.R2` | OMC: `witness-admitted-with-warning` | [FINDING-lowpass-firstorder-r2-unbounded.md](../../bugs/FINDING-lowpass-firstorder-r2-unbounded.md) |
| [FINDING-01003](../candidate/FINDING-01003.md) | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.FirstOrder | `R2` | OMC: `unresolved-baseline-fails` | [FINDING-firstorder-r2-unbounded.md](../../bugs/FINDING-firstorder-r2-unbounded.md) |
