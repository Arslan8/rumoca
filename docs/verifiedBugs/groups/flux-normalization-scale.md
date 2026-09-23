# Zero magnetic normalization scale divides by zero

Group `flux-normalization-scale` · 16 report instances · confirmed

BaseData leaves B_myMax unconstrained. FixedShape unconditionally computes B_N=abs(B/material.B_myMax), so B_myMax=0 is undefined. In nonlinear material mode it is also a genuine normalization scale. The inactive-linear-mode instances are separately grouped because the calculation should be eliminated there entirely.

Require B_myMax>0 for nonlinear permeability and conditionally evaluate B_N only in that branch. Add a checked material-record validation before normalization. Linear mode must not read unused nonlinear material data.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-03713](../confirmed/FINDING-03713.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.QuadraticCoreAirgap | `leftLeg.material.B_myMax` |
| [FINDING-03718](../confirmed/FINDING-03718.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.QuadraticCoreAirgap | `upperYoke.material.B_myMax` |
| [FINDING-03721](../confirmed/FINDING-03721.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.QuadraticCoreAirgap | `rightLeg.material.B_myMax` |
| [FINDING-03725](../confirmed/FINDING-03725.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.QuadraticCoreAirgap | `airGap.material.B_myMax` |
| [FINDING-03728](../confirmed/FINDING-03728.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.QuadraticCoreAirgap | `lowerYoke.material.B_myMax` |
| [FINDING-03732](../confirmed/FINDING-03732.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.SaturatedInductor | `r_mAirPar.material.B_myMax` |
| [FINDING-03736](../confirmed/FINDING-03736.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.SaturatedInductor | `r_mFe.material.B_myMax` |
| [FINDING-03740](../confirmed/FINDING-03740.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.ToroidalCoreAirgap | `core.material.B_myMax` |
| [FINDING-03745](../confirmed/FINDING-03745.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.ToroidalCoreAirgap | `airGap.material.B_myMax` |
| [FINDING-03750](../confirmed/FINDING-03750.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.ToroidalCoreQuadraticCrossSection | `core.material.B_myMax` |
| [FINDING-03756](../confirmed/FINDING-03756.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.ToroidalCoreQuadraticCrossSection | `airGap.material.B_myMax` |
| [FINDING-03837](../confirmed/FINDING-03837.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid | `material.B_myMax` |
| [FINDING-03850](../confirmed/FINDING-03850.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid | `g_mAirPar.material.B_myMax` |
| [FINDING-03853](../confirmed/FINDING-03853.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.AdvancedSolenoid | `G_mLeakRad.material.B_myMax` |
| [FINDING-03868](../confirmed/FINDING-03868.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid | `material.B_myMax` |
| [FINDING-03881](../confirmed/FINDING-03881.md) | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid | `g_mAirPar.material.B_myMax` |
