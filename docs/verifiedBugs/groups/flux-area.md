# Zero flux-tube area makes the model undefined

Group `flux-area` · 6 report instances · confirmed

A=area; G_m=mu_0*mu_r*A/l; the inherited equations use R_m=1/G_m and B=Phi/A. area=0 makes both reciprocals undefined. Runtime overrides report division by zero; final-evaluated translation is structurally singular. This is not merely dividing a storage equation while selecting a state.

Validate strictly positive l and area at GenericFluxTube and guard reciprocal evaluation. Add meaningful positive parameter bounds for editor feedback, plus assertions for runtime enforcement. If zero geometry is intended, introduce a separate limiting magnetic element with consistent equations instead of evaluating 1/0.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [BUG-025](../confirmed/BUG-025.md) | ModelicaTest.Magnetic.FluxTubes.Sensors | `genericFluxTube.area` |
| [FINDING-04967](../confirmed/FINDING-04967.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube.area` |
| [FINDING-04968](../confirmed/FINDING-04968.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube1.area` |
| [FINDING-04969](../confirmed/FINDING-04969.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube2.area` |
| [FINDING-04970](../confirmed/FINDING-04970.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube3.area` |
| [FINDING-04989](../confirmed/FINDING-04989.md) | ModelicaTest.Magnetic.FluxTubes.Sensors | `genericFluxTube.area` |
