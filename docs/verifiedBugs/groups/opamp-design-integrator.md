# Integrator circuit has an unguarded design denominator

Group `opamp-design-integrator` · 8 report instances · confirmed

The source binding is C=1/k/(2*pi*f*R). The reported parameter is an explicit divisor with no zero handling. At the zero witness the nominal design cannot produce finite capacitance. This declaration has a reproduced instance in the evidence; a declaration-only report is linked to that shared proof, not claimed to have its own executable model.

Validate the denominator parameters at OpAmpCircuits.Integrator, before evaluating C. Use positive domain constraints for the intended passive design and a guarded calculation plus clear assertions. If zero gain is supported, implement a dedicated zero-gain branch instead of dividing by it.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0644](../confirmed/DECL-0644.md) | — | `R` |
| [FINDING-00828](../confirmed/FINDING-00828.md) | Modelica.Electrical.Analog.Examples.OpAmps.Integrator | `integrator.R` |
| [FINDING-00832](../confirmed/FINDING-00832.md) | Modelica.Electrical.Analog.Examples.OpAmps.Integrator | `integrator.R` |
| [FINDING-00833](../confirmed/FINDING-00833.md) | Modelica.Electrical.Analog.Examples.OpAmps.Integrator | `integrator.k` |
| [FINDING-00904](../confirmed/FINDING-00904.md) | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Integrator | `R` |
| [FINDING-00907](../confirmed/FINDING-00907.md) | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Integrator | `f` |
| [FINDING-00908](../confirmed/FINDING-00908.md) | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Integrator | `R` |
| [FINDING-00909](../confirmed/FINDING-00909.md) | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Integrator | `k` |
