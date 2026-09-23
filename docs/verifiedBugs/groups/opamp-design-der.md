# Der circuit has an unguarded design denominator

Group `opamp-design-der` · 6 report instances · confirmed

The source binding is C=k/(2*pi*f*R). The reported parameter is an explicit divisor with no zero handling. At the zero witness the nominal design cannot produce finite capacitance. This declaration has a reproduced instance in the evidence; a declaration-only report is linked to that shared proof, not claimed to have its own executable model.

Validate the denominator parameters at OpAmpCircuits.Der, before evaluating C. Use positive domain constraints for the intended passive design and a guarded calculation plus clear assertions. If zero gain is supported, implement a dedicated zero-gain branch instead of dividing by it.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0628](../confirmed/DECL-0628.md) | — | `R` |
| [FINDING-00814](../confirmed/FINDING-00814.md) | Modelica.Electrical.Analog.Examples.OpAmps.Differentiator | `der_.R` |
| [FINDING-00819](../confirmed/FINDING-00819.md) | Modelica.Electrical.Analog.Examples.OpAmps.Differentiator | `der_.R` |
| [FINDING-00890](../confirmed/FINDING-00890.md) | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Der | `R` |
| [FINDING-00893](../confirmed/FINDING-00893.md) | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Der | `f` |
| [FINDING-00894](../confirmed/FINDING-00894.md) | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Der | `R` |
