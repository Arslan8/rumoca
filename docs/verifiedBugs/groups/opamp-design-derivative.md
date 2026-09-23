# Derivative circuit has an unguarded design denominator

Group `opamp-design-derivative` · 5 report instances · confirmed

The source binding is C=T/R1. The reported parameter is an explicit divisor with no zero handling. At the zero witness the nominal design cannot produce finite capacitance. This declaration has a reproduced instance in the evidence; a declaration-only report is linked to that shared proof, not claimed to have its own executable model.

Validate the denominator parameters at OpAmpCircuits.Derivative, before evaluating C. Use positive domain constraints for the intended passive design and a guarded calculation plus clear assertions. If zero gain is supported, implement a dedicated zero-gain branch instead of dividing by it.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0629](../confirmed/DECL-0629.md) | — | `R1` |
| [FINDING-00820](../confirmed/FINDING-00820.md) | Modelica.Electrical.Analog.Examples.OpAmps.HighPass | `derivative.R1` |
| [FINDING-00826](../confirmed/FINDING-00826.md) | Modelica.Electrical.Analog.Examples.OpAmps.HighPass | `derivative.R1` |
| [FINDING-00885](../confirmed/FINDING-00885.md) | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Derivative | `R1` |
| [FINDING-00889](../confirmed/FINDING-00889.md) | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Derivative | `R1` |
