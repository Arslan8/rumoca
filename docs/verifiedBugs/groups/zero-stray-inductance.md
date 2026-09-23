# Zero optional leakage inductance is intentional

Group `zero-stray-inductance` · 5 report instances · false-positives

The derived stray inductance is Lesigma=Le*sigmae; sigmae=0 represents no stray part. It is passed into InductorDC, whose equation is v=if quasiStatic then 0 else L*der(i). At L=0 the element has zero voltage drop; it is not an unconditional source-level 1/L. A default zero optional leakage term is not an invariant violation.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-01123](../false-positives/FINDING-01123.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcee.Lesigma` |
| [FINDING-01128](../false-positives/FINDING-01128.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcse.Lesigma` |
| [FINDING-01194](../false-positives/FINDING-01194.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCEE_Start | `dcee.Lesigma` |
| [FINDING-01476](../false-positives/FINDING-01476.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_SinglePhase | `dcse.Lesigma` |
| [FINDING-01506](../false-positives/FINDING-01506.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_Start | `dcse.Lesigma` |
