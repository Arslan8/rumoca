# Zero nominal speed makes DC-machine scaling undefined

Group `dc-data-nominal-speed` · 19 report instances · confirmed

DcPermanentMagnetData leaves wNominal unconstrained and forwards it to the machine/loss records. PartialBasicDCMachine computes turnsRatio=ViNominal/(wNominal*psi_eNominal). The data record therefore admits a value that makes a common consumer divide by zero.

Require and validate a nonzero nominal speed using the documented motor/generator sign convention before turns-ratio and loss-reference calculations. If standstill data are needed, define a different identification input rather than dividing by speed.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-01183](../confirmed/FINDING-01183.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcpmData.wNominal` |
| [FINDING-01185](../confirmed/FINDING-01185.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dceeData.wNominal` |
| [FINDING-01187](../confirmed/FINDING-01187.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcseData.wNominal` |
| [FINDING-01216](../confirmed/FINDING-01216.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCEE_Start | `dceeData.wNominal` |
| [FINDING-01265](../confirmed/FINDING-01265.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `dcpmData.wNominal` |
| [FINDING-01288](../confirmed/FINDING-01288.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_CurrentControlled | `dcpmData.wNominal` |
| [FINDING-01290](../confirmed/FINDING-01290.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_CurrentControlled | `dcpmData.wNominal` |
| [FINDING-01339](../confirmed/FINDING-01339.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpmData.wNominal` |
| [FINDING-01378](../confirmed/FINDING-01378.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpmData.wNominal` |
| [FINDING-01400](../confirmed/FINDING-01400.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Start | `dcpmData.wNominal` |
| [FINDING-01420](../confirmed/FINDING-01420.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Temperature | `dcpmData.wNominal` |
| [FINDING-01460](../confirmed/FINDING-01460.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpmData2.wNominal` |
| [FINDING-01463](../confirmed/FINDING-01463.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpmData1.wNominal` |
| [FINDING-01499](../confirmed/FINDING-01499.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_SinglePhase | `dcseData.wNominal` |
| [FINDING-01529](../confirmed/FINDING-01529.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_Start | `dcseData.wNominal` |
| [FINDING-03099](../confirmed/FINDING-03099.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive | `dcpmData.wNominal` |
| [FINDING-03100](../confirmed/FINDING-03100.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive | `dcpmData.wNominal` |
| [FINDING-03254](../confirmed/FINDING-03254.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_DC_Drive | `dcpmData.wNominal` |
| [FINDING-03255](../confirmed/FINDING-03255.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_DC_Drive | `dcpmData.wNominal` |
