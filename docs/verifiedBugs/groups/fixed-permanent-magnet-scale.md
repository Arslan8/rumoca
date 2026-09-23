# Lme is an immutable nonzero model constant

Group `fixed-permanent-magnet-scale` · 13 report instances · false-positives

DC_PermanentMagnet declares protected constant SI.Inductance Lme=1. It is a fixed equivalence scale, not a user parameter, and cannot reach the claimed zero witness. The finding lost constant/final role information.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-01137](../false-positives/FINDING-01137.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcpm.Lme` |
| [FINDING-01234](../false-positives/FINDING-01234.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `dcpm.Lme` |
| [FINDING-01282](../false-positives/FINDING-01282.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_CurrentControlled | `dcpm.Lme` |
| [FINDING-01315](../false-positives/FINDING-01315.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpm1.Lme` |
| [FINDING-01324](../false-positives/FINDING-01324.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpm2.Lme` |
| [FINDING-01362](../false-positives/FINDING-01362.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpm1.Lme` |
| [FINDING-01365](../false-positives/FINDING-01365.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpm2.Lme` |
| [FINDING-01393](../false-positives/FINDING-01393.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Start | `dcpm.Lme` |
| [FINDING-01414](../false-positives/FINDING-01414.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Temperature | `dcpm.Lme` |
| [FINDING-01434](../false-positives/FINDING-01434.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpm1.Lme` |
| [FINDING-01446](../false-positives/FINDING-01446.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpm2.Lme` |
| [FINDING-03082](../false-positives/FINDING-03082.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive | `dcpm.Lme` |
| [FINDING-03243](../false-positives/FINDING-03243.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_DC_Drive | `dcpm.Lme` |
