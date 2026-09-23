# PI circuit has an unguarded design denominator

Group `opamp-design-pi` · 6 report instances · confirmed

The source binding is C=T/k/R1. The reported parameter is an explicit divisor with no zero handling. At the zero witness the nominal design cannot produce finite capacitance. This declaration has a reproduced instance in the evidence; a declaration-only report is linked to that shared proof, not claimed to have its own executable model.

Validate the denominator parameters at OpAmpCircuits.PI, before evaluating C. Use positive domain constraints for the intended passive design and a guarded calculation plus clear assertions. If zero gain is supported, implement a dedicated zero-gain branch instead of dividing by it.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0645](../confirmed/DECL-0645.md) | — | `R1` |
| [FINDING-00785](../confirmed/FINDING-00785.md) | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit | `PIA.R1` |
| [FINDING-00803](../confirmed/FINDING-00803.md) | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit | `PIA.R1` |
| [FINDING-00910](../confirmed/FINDING-00910.md) | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.PI | `R1` |
| [FINDING-00914](../confirmed/FINDING-00914.md) | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.PI | `R1` |
| [FINDING-00915](../confirmed/FINDING-00915.md) | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.PI | `k` |
