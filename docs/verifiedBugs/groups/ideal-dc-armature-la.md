# Zero armature inductance is an ideal algebraic limit

Group `ideal-dc-armature-la` · 19 report instances · false-positives

La is passed to InductorDC, whose equation is v=L*der(i) outside quasi-static mode; zero removes the inductive voltage drop. The partial machine source has no unconditional reciprocal of this parameter. A particular initialization can still be topology-dependent.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0151](../false-positives/DECL-0151.md) | — | `La` |
| [FINDING-01139](../false-positives/FINDING-01139.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcpm.La` |
| [FINDING-01157](../false-positives/FINDING-01157.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcee.La` |
| [FINDING-01175](../false-positives/FINDING-01175.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcse.La` |
| [FINDING-01198](../false-positives/FINDING-01198.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCEE_Start | `dcee.La` |
| [FINDING-01227](../false-positives/FINDING-01227.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `dcpm.La` |
| [FINDING-01275](../false-positives/FINDING-01275.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_CurrentControlled | `dcpm.La` |
| [FINDING-01308](../false-positives/FINDING-01308.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpm1.La` |
| [FINDING-01317](../false-positives/FINDING-01317.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpm2.La` |
| [FINDING-01355](../false-positives/FINDING-01355.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpm1.La` |
| [FINDING-01367](../false-positives/FINDING-01367.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpm2.La` |
| [FINDING-01386](../false-positives/FINDING-01386.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Start | `dcpm.La` |
| [FINDING-01407](../false-positives/FINDING-01407.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Temperature | `dcpm.La` |
| [FINDING-01427](../false-positives/FINDING-01427.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpm1.La` |
| [FINDING-01437](../false-positives/FINDING-01437.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpm2.La` |
| [FINDING-01480](../false-positives/FINDING-01480.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_SinglePhase | `dcse.La` |
| [FINDING-01510](../false-positives/FINDING-01510.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_Start | `dcse.La` |
| [FINDING-03075](../false-positives/FINDING-03075.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive | `dcpm.La` |
| [FINDING-03236](../false-positives/FINDING-03236.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_DC_Drive | `dcpm.La` |
