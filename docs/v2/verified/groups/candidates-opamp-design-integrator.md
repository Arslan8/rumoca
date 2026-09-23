# Static/source-supported candidates: `opamp-design-integrator`

**3 report instances**

[Back to Static/source-supported candidates](../candidates.md) · [Overview](../README.md)

## Common decision rule

The source binding is C=1/k/(2*pi*f*R). The reported parameter is an explicit divisor with no zero handling. At the zero witness the nominal design cannot produce finite capacitance. This declaration has a reproduced instance in the evidence; a declaration-only report is linked to that shared proof, not claimed to have its own executable model.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0644](../candidate/DECL-0644.md) | — | `R` | Source/semantic review | [DECL-integrator-r-7.md](../../bugs/DECL-integrator-r-7.md) |
| [FINDING-00876](../candidate/FINDING-00876.md) | Modelica.Electrical.Analog.Examples.OpAmps.Integrator | `integrator.R` | OMC: `witness-admitted-with-warning` | [FINDING-integrator-integrator-r-unbounded.md](../../bugs/FINDING-integrator-integrator-r-unbounded.md) |
| [FINDING-01012](../candidate/FINDING-01012.md) | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Integrator | `R` | OMC: `unresolved-baseline-fails` | [FINDING-integrator-r-unbounded.md](../../bugs/FINDING-integrator-r-unbounded.md) |
