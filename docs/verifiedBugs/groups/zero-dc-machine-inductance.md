# Zero DC-machine inductance is an algebraic ideal limit

Group `zero-dc-machine-inductance` · 24 report instances · false-positives

InductorDC uses v=if quasiStatic then 0 else L*der(i); it never divides by L. At L=0 the dynamic branch also imposes v=0. A missing positive bound is therefore not an intrinsic source defect, although a surrounding machine configuration may have incompatible state selections or constraints.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0131](../false-positives/DECL-0131.md) | — | `L` |
| [FINDING-01122](../false-positives/FINDING-01122.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcee.lesigma.L` |
| [FINDING-01127](../false-positives/FINDING-01127.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcse.lesigma.L` |
| [FINDING-01140](../false-positives/FINDING-01140.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcpm.la.L` |
| [FINDING-01158](../false-positives/FINDING-01158.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcee.la.L` |
| [FINDING-01176](../false-positives/FINDING-01176.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcse.la.L` |
| [FINDING-01193](../false-positives/FINDING-01193.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCEE_Start | `dcee.lesigma.L` |
| [FINDING-01199](../false-positives/FINDING-01199.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCEE_Start | `dcee.la.L` |
| [FINDING-01228](../false-positives/FINDING-01228.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `dcpm.la.L` |
| [FINDING-01276](../false-positives/FINDING-01276.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_CurrentControlled | `dcpm.la.L` |
| [FINDING-01309](../false-positives/FINDING-01309.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpm1.la.L` |
| [FINDING-01318](../false-positives/FINDING-01318.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpm2.la.L` |
| [FINDING-01356](../false-positives/FINDING-01356.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpm1.la.L` |
| [FINDING-01368](../false-positives/FINDING-01368.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpm2.la.L` |
| [FINDING-01387](../false-positives/FINDING-01387.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Start | `dcpm.la.L` |
| [FINDING-01408](../false-positives/FINDING-01408.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Temperature | `dcpm.la.L` |
| [FINDING-01428](../false-positives/FINDING-01428.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpm1.la.L` |
| [FINDING-01439](../false-positives/FINDING-01439.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpm2.la.L` |
| [FINDING-01475](../false-positives/FINDING-01475.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_SinglePhase | `dcse.lesigma.L` |
| [FINDING-01481](../false-positives/FINDING-01481.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_SinglePhase | `dcse.la.L` |
| [FINDING-01505](../false-positives/FINDING-01505.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_Start | `dcse.lesigma.L` |
| [FINDING-01511](../false-positives/FINDING-01511.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_Start | `dcse.la.L` |
| [FINDING-03076](../false-positives/FINDING-03076.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive | `dcpm.la.L` |
| [FINDING-03237](../false-positives/FINDING-03237.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_DC_Drive | `dcpm.la.L` |
