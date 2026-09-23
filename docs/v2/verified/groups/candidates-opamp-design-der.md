# Static/source-supported candidates: `opamp-design-der`

**3 report instances**

[Back to Static/source-supported candidates](../candidates.md) · [Overview](../README.md)

## Common decision rule

The source binding is C=k/(2*pi*f*R). The reported parameter is an explicit divisor with no zero handling. At the zero witness the nominal design cannot produce finite capacitance. This declaration has a reproduced instance in the evidence; a declaration-only report is linked to that shared proof, not claimed to have its own executable model.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0628](../candidate/DECL-0628.md) | — | `R` | Source/semantic review | [DECL-der-r-7.md](../../bugs/DECL-der-r-7.md) |
| [FINDING-00842](../candidate/FINDING-00842.md) | Modelica.Electrical.Analog.Examples.OpAmps.Differentiator | `der_.R` | OMC: `witness-admitted-with-warning` | [FINDING-differentiator-der-r-unbounded.md](../../bugs/FINDING-differentiator-der-r-unbounded.md) |
| [FINDING-00993](../candidate/FINDING-00993.md) | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Der | `R` | OMC: `unresolved-baseline-fails` | [FINDING-der-r-unbounded.md](../../bugs/FINDING-der-r-unbounded.md) |
