# Inactive material data still enter an unguarded division

Group `inactive-flux-normalization` · 9 report instances · confirmed

These instances set nonLinearPermeability=false, so B_myMax is documented as unused. Nevertheless FixedShape unconditionally defines B_N=abs(B/material.B_myMax). At B_myMax=0 this auxiliary equation is undefined. Rumoca and post-translation OpenModelica overrides fail; OpenModelica recompilation succeeds after removing the unused B_N equation. Therefore the original claim of a robust two-tool active-material failure is overstated, but the unconditional inactive-branch calculation is a source-verified defect.

Make B_N conditional: if nonLinearPermeability then abs(B/material.B_myMax) else 0. Validate B_myMax>0 only in the nonlinear branch. Do not reject unused material settings in linear mode. Verify that the compiler preserves lazy conditional evaluation.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [BUG-010](../confirmed/BUG-010.md) | ModelicaTest.Magnetic.FluxTubes.Sensors | `genericFluxTube.material.B_myMax` |
| [BUG-018](../confirmed/BUG-018.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube1.material.B_myMax` |
| [BUG-020](../confirmed/BUG-020.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube2.material.B_myMax` |
| [BUG-022](../confirmed/BUG-022.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube3.material.B_myMax` |
| [FINDING-04971](../confirmed/FINDING-04971.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube.material.B_myMax` |
| [FINDING-04975](../confirmed/FINDING-04975.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube1.material.B_myMax` |
| [FINDING-04981](../confirmed/FINDING-04981.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube2.material.B_myMax` |
| [FINDING-04985](../confirmed/FINDING-04985.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube3.material.B_myMax` |
| [FINDING-04990](../confirmed/FINDING-04990.md) | ModelicaTest.Magnetic.FluxTubes.Sensors | `genericFluxTube.material.B_myMax` |
