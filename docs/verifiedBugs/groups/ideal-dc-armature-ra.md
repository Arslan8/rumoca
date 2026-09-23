# Zero armature resistance is an ideal algebraic limit

Group `ideal-dc-armature-ra` · 19 report instances · false-positives

Ra is passed to Basic.Resistor, whose contract explicitly supports zero and signed resistance; zero removes armature copper loss. The partial machine source has no unconditional reciprocal of this parameter. A particular initialization can still be topology-dependent.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0707](../false-positives/DECL-0707.md) | — | `Ra` |
| [FINDING-01138](../false-positives/FINDING-01138.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcpm.Ra` |
| [FINDING-01156](../false-positives/FINDING-01156.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcee.Ra` |
| [FINDING-01174](../false-positives/FINDING-01174.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcse.Ra` |
| [FINDING-01197](../false-positives/FINDING-01197.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCEE_Start | `dcee.Ra` |
| [FINDING-01226](../false-positives/FINDING-01226.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `dcpm.Ra` |
| [FINDING-01274](../false-positives/FINDING-01274.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_CurrentControlled | `dcpm.Ra` |
| [FINDING-01307](../false-positives/FINDING-01307.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpm1.Ra` |
| [FINDING-01316](../false-positives/FINDING-01316.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpm2.Ra` |
| [FINDING-01354](../false-positives/FINDING-01354.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpm1.Ra` |
| [FINDING-01366](../false-positives/FINDING-01366.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpm2.Ra` |
| [FINDING-01385](../false-positives/FINDING-01385.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Start | `dcpm.Ra` |
| [FINDING-01406](../false-positives/FINDING-01406.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Temperature | `dcpm.Ra` |
| [FINDING-01426](../false-positives/FINDING-01426.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpm1.Ra` |
| [FINDING-01436](../false-positives/FINDING-01436.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpm2.Ra` |
| [FINDING-01479](../false-positives/FINDING-01479.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_SinglePhase | `dcse.Ra` |
| [FINDING-01509](../false-positives/FINDING-01509.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_Start | `dcse.Ra` |
| [FINDING-03074](../false-positives/FINDING-03074.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive | `dcpm.Ra` |
| [FINDING-03235](../false-positives/FINDING-03235.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_DC_Drive | `dcpm.Ra` |
