# AirGapDC uses excitation inductance only as a multiplier

Group `zero-dc-airgap-inductance` · 19 report instances · false-positives

The complete magnetic relation is psi_e=Le*ie. Le=0 produces zero excitation flux; this source does not divide by Le. Whether such an idealized machine remains useful is separate from the reported claim that the declaration necessarily causes an arithmetic failure.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0122](../false-positives/DECL-0122.md) | — | `Le` |
| [FINDING-01136](../false-positives/FINDING-01136.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcpm.airGapDC.Le` |
| [FINDING-01154](../false-positives/FINDING-01154.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcee.airGapDC.Le` |
| [FINDING-01172](../false-positives/FINDING-01172.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcse.airGapDC.Le` |
| [FINDING-01206](../false-positives/FINDING-01206.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCEE_Start | `dcee.airGapDC.Le` |
| [FINDING-01233](../false-positives/FINDING-01233.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `dcpm.airGapDC.Le` |
| [FINDING-01281](../false-positives/FINDING-01281.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_CurrentControlled | `dcpm.airGapDC.Le` |
| [FINDING-01314](../false-positives/FINDING-01314.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpm1.airGapDC.Le` |
| [FINDING-01323](../false-positives/FINDING-01323.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpm2.airGapDC.Le` |
| [FINDING-01361](../false-positives/FINDING-01361.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpm1.airGapDC.Le` |
| [FINDING-01364](../false-positives/FINDING-01364.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpm2.airGapDC.Le` |
| [FINDING-01392](../false-positives/FINDING-01392.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Start | `dcpm.airGapDC.Le` |
| [FINDING-01413](../false-positives/FINDING-01413.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Temperature | `dcpm.airGapDC.Le` |
| [FINDING-01433](../false-positives/FINDING-01433.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpm1.airGapDC.Le` |
| [FINDING-01445](../false-positives/FINDING-01445.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpm2.airGapDC.Le` |
| [FINDING-01488](../false-positives/FINDING-01488.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_SinglePhase | `dcse.airGapDC.Le` |
| [FINDING-01518](../false-positives/FINDING-01518.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_Start | `dcse.airGapDC.Le` |
| [FINDING-03081](../false-positives/FINDING-03081.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive | `dcpm.airGapDC.Le` |
| [FINDING-03242](../false-positives/FINDING-03242.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_DC_Drive | `dcpm.airGapDC.Le` |
