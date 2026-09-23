# Zero flux-tube length divides by zero

Group `flux-length` · 10 report instances · confirmed

G_m = mu_0*mu_r*A/l is evaluated with l=0. The numerator is nonzero for the nominal positive area/permeability. Baseline passes; the l=0 source-modified and final-evaluated models explicitly report division by zero.

Validate strictly positive l and area at GenericFluxTube and guard reciprocal evaluation. Add meaningful positive parameter bounds for editor feedback, plus assertions for runtime enforcement. If zero geometry is intended, introduce a separate limiting magnetic element with consistent equations instead of evaluating 1/0.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [BUG-011](../confirmed/BUG-011.md) | ModelicaTest.Magnetic.FluxTubes.Sensors | `genericFluxTube.l` |
| [BUG-019](../confirmed/BUG-019.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube1.l` |
| [BUG-021](../confirmed/BUG-021.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube2.l` |
| [BUG-023](../confirmed/BUG-023.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube3.l` |
| [DECL-0469](../confirmed/DECL-0469.md) | — | `l` |
| [FINDING-04974](../confirmed/FINDING-04974.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube.l` |
| [FINDING-04978](../confirmed/FINDING-04978.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube1.l` |
| [FINDING-04984](../confirmed/FINDING-04984.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube2.l` |
| [FINDING-04988](../confirmed/FINDING-04988.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube3.l` |
| [FINDING-04993](../confirmed/FINDING-04993.md) | ModelicaTest.Magnetic.FluxTubes.Sensors | `genericFluxTube.l` |
