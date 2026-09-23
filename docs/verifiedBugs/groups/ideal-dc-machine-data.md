# DC machine-data field has a supported ideal limit

Group `ideal-dc-machine-data` · 68 report instances · false-positives

This field represents zero armature inductance and is forwarded to a component that uses it multiplicatively: torque balance for inertia, v=R*i for resistance, or v=L*der(i) for inductance. None intrinsically requires division by the field. A specific drive train can still be inconsistent; the missing strictly-positive record bound alone is not a bug.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0159](../false-positives/DECL-0159.md) | — | `La` |
| [DECL-0318](../false-positives/DECL-0318.md) | — | `Jr` |
| [DECL-0319](../false-positives/DECL-0319.md) | — | `Js` |
| [DECL-0713](../false-positives/DECL-0713.md) | — | `Ra` |
| [FINDING-01132](../false-positives/FINDING-01132.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcpmData.Jr` |
| [FINDING-01133](../false-positives/FINDING-01133.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcpmData.Js` |
| [FINDING-01134](../false-positives/FINDING-01134.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcpmData.Ra` |
| [FINDING-01135](../false-positives/FINDING-01135.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcpmData.La` |
| [FINDING-01146](../false-positives/FINDING-01146.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dceeData.Jr` |
| [FINDING-01147](../false-positives/FINDING-01147.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dceeData.Js` |
| [FINDING-01148](../false-positives/FINDING-01148.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dceeData.Ra` |
| [FINDING-01149](../false-positives/FINDING-01149.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dceeData.La` |
| [FINDING-01164](../false-positives/FINDING-01164.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcseData.Jr` |
| [FINDING-01165](../false-positives/FINDING-01165.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcseData.Js` |
| [FINDING-01166](../false-positives/FINDING-01166.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcseData.Ra` |
| [FINDING-01167](../false-positives/FINDING-01167.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcseData.La` |
| [FINDING-01209](../false-positives/FINDING-01209.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCEE_Start | `dceeData.Jr` |
| [FINDING-01210](../false-positives/FINDING-01210.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCEE_Start | `dceeData.Js` |
| [FINDING-01211](../false-positives/FINDING-01211.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCEE_Start | `dceeData.Ra` |
| [FINDING-01212](../false-positives/FINDING-01212.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCEE_Start | `dceeData.La` |
| [FINDING-01252](../false-positives/FINDING-01252.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `dcpmData.Jr` |
| [FINDING-01253](../false-positives/FINDING-01253.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `dcpmData.Js` |
| [FINDING-01254](../false-positives/FINDING-01254.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `dcpmData.Ra` |
| [FINDING-01255](../false-positives/FINDING-01255.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `dcpmData.La` |
| [FINDING-01284](../false-positives/FINDING-01284.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_CurrentControlled | `dcpmData.Jr` |
| [FINDING-01285](../false-positives/FINDING-01285.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_CurrentControlled | `dcpmData.Js` |
| [FINDING-01286](../false-positives/FINDING-01286.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_CurrentControlled | `dcpmData.Ra` |
| [FINDING-01287](../false-positives/FINDING-01287.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_CurrentControlled | `dcpmData.La` |
| [FINDING-01303](../false-positives/FINDING-01303.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpmData.Jr` |
| [FINDING-01304](../false-positives/FINDING-01304.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpmData.Js` |
| [FINDING-01305](../false-positives/FINDING-01305.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpmData.Ra` |
| [FINDING-01306](../false-positives/FINDING-01306.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpmData.La` |
| [FINDING-01374](../false-positives/FINDING-01374.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpmData.Jr` |
| [FINDING-01375](../false-positives/FINDING-01375.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpmData.Js` |
| [FINDING-01376](../false-positives/FINDING-01376.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpmData.Ra` |
| [FINDING-01377](../false-positives/FINDING-01377.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpmData.La` |
| [FINDING-01395](../false-positives/FINDING-01395.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Start | `dcpmData.Jr` |
| [FINDING-01396](../false-positives/FINDING-01396.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Start | `dcpmData.Js` |
| [FINDING-01397](../false-positives/FINDING-01397.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Start | `dcpmData.Ra` |
| [FINDING-01398](../false-positives/FINDING-01398.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Start | `dcpmData.La` |
| [FINDING-01416](../false-positives/FINDING-01416.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Temperature | `dcpmData.Jr` |
| [FINDING-01417](../false-positives/FINDING-01417.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Temperature | `dcpmData.Js` |
| [FINDING-01418](../false-positives/FINDING-01418.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Temperature | `dcpmData.Ra` |
| [FINDING-01419](../false-positives/FINDING-01419.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Temperature | `dcpmData.La` |
| [FINDING-01448](../false-positives/FINDING-01448.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpmData1.Jr` |
| [FINDING-01449](../false-positives/FINDING-01449.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpmData1.Js` |
| [FINDING-01450](../false-positives/FINDING-01450.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpmData1.Ra` |
| [FINDING-01451](../false-positives/FINDING-01451.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpmData1.La` |
| [FINDING-01452](../false-positives/FINDING-01452.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpmData2.Jr` |
| [FINDING-01453](../false-positives/FINDING-01453.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpmData2.Js` |
| [FINDING-01454](../false-positives/FINDING-01454.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpmData2.Ra` |
| [FINDING-01455](../false-positives/FINDING-01455.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpmData2.La` |
| [FINDING-01491](../false-positives/FINDING-01491.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_SinglePhase | `dcseData.Jr` |
| [FINDING-01492](../false-positives/FINDING-01492.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_SinglePhase | `dcseData.Js` |
| [FINDING-01493](../false-positives/FINDING-01493.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_SinglePhase | `dcseData.Ra` |
| [FINDING-01494](../false-positives/FINDING-01494.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_SinglePhase | `dcseData.La` |
| [FINDING-01521](../false-positives/FINDING-01521.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_Start | `dcseData.Jr` |
| [FINDING-01522](../false-positives/FINDING-01522.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_Start | `dcseData.Js` |
| [FINDING-01523](../false-positives/FINDING-01523.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_Start | `dcseData.Ra` |
| [FINDING-01524](../false-positives/FINDING-01524.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_Start | `dcseData.La` |
| [FINDING-03083](../false-positives/FINDING-03083.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive | `dcpmData.Jr` |
| [FINDING-03084](../false-positives/FINDING-03084.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive | `dcpmData.Js` |
| [FINDING-03085](../false-positives/FINDING-03085.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive | `dcpmData.Ra` |
| [FINDING-03086](../false-positives/FINDING-03086.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive | `dcpmData.La` |
| [FINDING-03244](../false-positives/FINDING-03244.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_DC_Drive | `dcpmData.Jr` |
| [FINDING-03245](../false-positives/FINDING-03245.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_DC_Drive | `dcpmData.Js` |
| [FINDING-03246](../false-positives/FINDING-03246.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_DC_Drive | `dcpmData.Ra` |
| [FINDING-03247](../false-positives/FINDING-03247.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_DC_Drive | `dcpmData.La` |
