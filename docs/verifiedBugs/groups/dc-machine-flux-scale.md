# Zero nominal excitation flux divides the turns-ratio calculation

Group `dc-machine-flux-scale` · 15 report instances · confirmed

PartialBasicDCMachine declares psi_eNominal without a positive/nonzero constraint and computes turnsRatio=ViNominal/(wNominal*psi_eNominal). Zero excitation flux therefore makes the machine scaling undefined. This is a direct source denominator even when a full example is blocked by unrelated runtime support.

Define the intended sign convention, then require abs(psi_eNominal)>=small (or psi_eNominal>0) and validate it before computing turnsRatio. A zero-flux motor requires a separate degenerate formulation, not epsilon substitution.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-01184](../confirmed/FINDING-01184.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcpm.psi_eNominal` |
| [FINDING-01186](../confirmed/FINDING-01186.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcee.psi_eNominal` |
| [FINDING-01217](../confirmed/FINDING-01217.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCEE_Start | `dcee.psi_eNominal` |
| [FINDING-01266](../confirmed/FINDING-01266.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `dcpm.psi_eNominal` |
| [FINDING-01296](../confirmed/FINDING-01296.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_CurrentControlled | `dcpm.psi_eNominal` |
| [FINDING-01340](../confirmed/FINDING-01340.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpm1.psi_eNominal` |
| [FINDING-01341](../confirmed/FINDING-01341.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpm2.psi_eNominal` |
| [FINDING-01379](../confirmed/FINDING-01379.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpm1.psi_eNominal` |
| [FINDING-01380](../confirmed/FINDING-01380.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpm2.psi_eNominal` |
| [FINDING-01401](../confirmed/FINDING-01401.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Start | `dcpm.psi_eNominal` |
| [FINDING-01421](../confirmed/FINDING-01421.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Temperature | `dcpm.psi_eNominal` |
| [FINDING-01464](../confirmed/FINDING-01464.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpm1.psi_eNominal` |
| [FINDING-01465](../confirmed/FINDING-01465.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpm2.psi_eNominal` |
| [FINDING-03101](../confirmed/FINDING-03101.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive | `dcpm.psi_eNominal` |
| [FINDING-03256](../confirmed/FINDING-03256.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_DC_Drive | `dcpm.psi_eNominal` |
