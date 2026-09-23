# FirstOrder circuit has an unguarded design denominator

Group `opamp-design-firstorder` · 9 report instances · confirmed

The source binding is C=T/R2. The reported parameter is an explicit divisor with no zero handling. At the zero witness the nominal design cannot produce finite capacitance. This declaration has a reproduced instance in the evidence; a declaration-only report is linked to that shared proof, not claimed to have its own executable model.

Validate the denominator parameters at OpAmpCircuits.FirstOrder, before evaluating C. Use positive domain constraints for the intended passive design and a guarded calculation plus clear assertions. If zero gain is supported, implement a dedicated zero-gain branch instead of dividing by it.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0641](../confirmed/DECL-0641.md) | — | `R2` |
| [FINDING-00790](../confirmed/FINDING-00790.md) | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit | `firstOrder1A.R2` |
| [FINDING-00797](../confirmed/FINDING-00797.md) | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit | `firstOrder2A.R2` |
| [FINDING-00804](../confirmed/FINDING-00804.md) | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit | `firstOrder1A.R2` |
| [FINDING-00805](../confirmed/FINDING-00805.md) | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit | `firstOrder2A.R2` |
| [FINDING-00859](../confirmed/FINDING-00859.md) | Modelica.Electrical.Analog.Examples.OpAmps.LowPass | `firstOrder.R2` |
| [FINDING-00864](../confirmed/FINDING-00864.md) | Modelica.Electrical.Analog.Examples.OpAmps.LowPass | `firstOrder.R2` |
| [FINDING-00898](../confirmed/FINDING-00898.md) | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.FirstOrder | `R2` |
| [FINDING-00901](../confirmed/FINDING-00901.md) | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.FirstOrder | `R2` |
