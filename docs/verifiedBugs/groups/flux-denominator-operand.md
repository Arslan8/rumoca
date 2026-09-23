# Zeroing this operand does not zero the complete denominator

Group `flux-denominator-operand` · 42 report instances · false-positives

The complete denominator is 1+c_b*B_N+B_N^n. The reported parameter is only an operand inside that sum. At c_b=0 the constant and power terms remain; at n=0 the power term is one. The zero-probe rationale therefore does not establish denominator zero. Other negative or relational combinations may deserve a separate range analysis, but they are not this claimed zero witness.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-03714](../false-positives/FINDING-03714.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.QuadraticCoreAirgap | `leftLeg.material.c_b` |
| [FINDING-03715](../false-positives/FINDING-03715.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.QuadraticCoreAirgap | `leftLeg.material.n` |
| [FINDING-03719](../false-positives/FINDING-03719.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.QuadraticCoreAirgap | `upperYoke.material.c_b` |
| [FINDING-03720](../false-positives/FINDING-03720.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.QuadraticCoreAirgap | `upperYoke.material.n` |
| [FINDING-03722](../false-positives/FINDING-03722.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.QuadraticCoreAirgap | `rightLeg.material.c_b` |
| [FINDING-03723](../false-positives/FINDING-03723.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.QuadraticCoreAirgap | `rightLeg.material.n` |
| [FINDING-03726](../false-positives/FINDING-03726.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.QuadraticCoreAirgap | `airGap.material.c_b` |
| [FINDING-03727](../false-positives/FINDING-03727.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.QuadraticCoreAirgap | `airGap.material.n` |
| [FINDING-03729](../false-positives/FINDING-03729.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.QuadraticCoreAirgap | `lowerYoke.material.c_b` |
| [FINDING-03730](../false-positives/FINDING-03730.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.QuadraticCoreAirgap | `lowerYoke.material.n` |
| [FINDING-03733](../false-positives/FINDING-03733.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.SaturatedInductor | `r_mAirPar.material.c_b` |
| [FINDING-03734](../false-positives/FINDING-03734.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.SaturatedInductor | `r_mAirPar.material.n` |
| [FINDING-03737](../false-positives/FINDING-03737.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.SaturatedInductor | `r_mFe.material.c_b` |
| [FINDING-03738](../false-positives/FINDING-03738.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.SaturatedInductor | `r_mFe.material.n` |
| [FINDING-03741](../false-positives/FINDING-03741.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.ToroidalCoreAirgap | `core.material.c_b` |
| [FINDING-03742](../false-positives/FINDING-03742.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.ToroidalCoreAirgap | `core.material.n` |
| [FINDING-03746](../false-positives/FINDING-03746.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.ToroidalCoreAirgap | `airGap.material.c_b` |
| [FINDING-03747](../false-positives/FINDING-03747.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.ToroidalCoreAirgap | `airGap.material.n` |
| [FINDING-03751](../false-positives/FINDING-03751.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.ToroidalCoreQuadraticCrossSection | `core.material.c_b` |
| [FINDING-03752](../false-positives/FINDING-03752.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.ToroidalCoreQuadraticCrossSection | `core.material.n` |
| [FINDING-03757](../false-positives/FINDING-03757.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.ToroidalCoreQuadraticCrossSection | `airGap.material.c_b` |
| [FINDING-03758](../false-positives/FINDING-03758.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.ToroidalCoreQuadraticCrossSection | `airGap.material.n` |
| [FINDING-03838](../false-positives/FINDING-03838.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid | `material.c_b` |
| [FINDING-03839](../false-positives/FINDING-03839.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid | `material.n` |
| [FINDING-03851](../false-positives/FINDING-03851.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid | `g_mAirPar.material.c_b` |
| [FINDING-03852](../false-positives/FINDING-03852.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid | `g_mAirPar.material.n` |
| [FINDING-03854](../false-positives/FINDING-03854.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid | `G_mLeakRad.material.c_b` |
| [FINDING-03855](../false-positives/FINDING-03855.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid | `G_mLeakRad.material.n` |
| [FINDING-03869](../false-positives/FINDING-03869.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid | `material.c_b` |
| [FINDING-03870](../false-positives/FINDING-03870.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid | `material.n` |
| [FINDING-03882](../false-positives/FINDING-03882.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid | `g_mAirPar.material.c_b` |
| [FINDING-03883](../false-positives/FINDING-03883.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid | `g_mAirPar.material.n` |
| [FINDING-04972](../false-positives/FINDING-04972.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube.material.c_b` |
| [FINDING-04973](../false-positives/FINDING-04973.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube.material.n` |
| [FINDING-04976](../false-positives/FINDING-04976.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube1.material.c_b` |
| [FINDING-04977](../false-positives/FINDING-04977.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube1.material.n` |
| [FINDING-04982](../false-positives/FINDING-04982.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube2.material.c_b` |
| [FINDING-04983](../false-positives/FINDING-04983.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube2.material.n` |
| [FINDING-04986](../false-positives/FINDING-04986.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube3.material.c_b` |
| [FINDING-04987](../false-positives/FINDING-04987.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `genericFluxTube3.material.n` |
| [FINDING-04991](../false-positives/FINDING-04991.md) | ModelicaTest.Magnetic.FluxTubes.Sensors | `genericFluxTube.material.c_b` |
| [FINDING-04992](../false-positives/FINDING-04992.md) | ModelicaTest.Magnetic.FluxTubes.Sensors | `genericFluxTube.material.n` |
