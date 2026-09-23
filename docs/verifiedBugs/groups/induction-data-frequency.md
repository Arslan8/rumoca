# Zero nominal frequency divides induction-machine data

Group `induction-data-frequency` · 41 report instances · confirmed

InductionMachineData leaves fsNominal without a positive bound, while Lssigma divides by 2*pi*fsNominal and multiple loss-reference angular velocities are proportional to it. The direct Lssigma binding is undefined at zero. The report instances share this record defect; tool-blocked full machines are not counted as successful runtime reproductions.

Set a meaningful positive lower bound on fsNominal and validate fsNominal>0 before derived data bindings are evaluated. If DC/zero-frequency machine data are needed, provide a separate formulation rather than evaluating the AC per-unit conversion at zero.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-01565](../confirmed/FINDING-01565.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking | `imcData.fsNominal` |
| [FINDING-01567](../confirmed/FINDING-01567.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking | `imcData.fsNominal` |
| [FINDING-01611](../confirmed/FINDING-01611.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL | `aimcData.fsNominal` |
| [FINDING-01613](../confirmed/FINDING-01613.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL | `aimcData.fsNominal` |
| [FINDING-01647](../confirmed/FINDING-01647.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize | `aimcData.fsNominal` |
| [FINDING-01649](../confirmed/FINDING-01649.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize | `aimcData.fsNominal` |
| [FINDING-01749](../confirmed/FINDING-01749.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive | `aimcData.fsNominal` |
| [FINDING-01751](../confirmed/FINDING-01751.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive | `aimcData.fsNominal` |
| [FINDING-01788](../confirmed/FINDING-01788.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Inverter | `aimcData.fsNominal` |
| [FINDING-01790](../confirmed/FINDING-01790.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Inverter | `aimcData.fsNominal` |
| [FINDING-01833](../confirmed/FINDING-01833.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz | `aimcData.fsNominal` |
| [FINDING-01835](../confirmed/FINDING-01835.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz | `aimcData.fsNominal` |
| [FINDING-01908](../confirmed/FINDING-01908.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer | `aimcData.fsNominal` |
| [FINDING-01912](../confirmed/FINDING-01912.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer | `aimcData.fsNominal` |
| [FINDING-01981](../confirmed/FINDING-01981.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `aimcData.fsNominal` |
| [FINDING-01983](../confirmed/FINDING-01983.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `aimcData.fsNominal` |
| [FINDING-02044](../confirmed/FINDING-02044.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD | `aimcData.fsNominal` |
| [FINDING-02046](../confirmed/FINDING-02046.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD | `aimcData.fsNominal` |
| [FINDING-02105](../confirmed/FINDING-02105.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aimsData.fsNominal` |
| [FINDING-02114](../confirmed/FINDING-02114.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aimsData.fsNominal` |
| [FINDING-02116](../confirmed/FINDING-02116.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aimsData.fsNominal` |
| [FINDING-02310](../confirmed/FINDING-02310.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking | `smpmData.fsNominal` |
| [FINDING-02312](../confirmed/FINDING-02312.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking | `smpmData.fsNominal` |
| [FINDING-02349](../confirmed/FINDING-02349.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_CurrentSource | `smpmData.fsNominal` |
| [FINDING-02355](../confirmed/FINDING-02355.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_CurrentSource | `smpmData.fsNominal` |
| [FINDING-02400](../confirmed/FINDING-02400.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Inverter | `smpmData.fsNominal` |
| [FINDING-02403](../confirmed/FINDING-02403.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Inverter | `smpmData.fsNominal` |
| [FINDING-02440](../confirmed/FINDING-02440.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad | `smpmData.fsNominal` |
| [FINDING-02442](../confirmed/FINDING-02442.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad | `smpmData.fsNominal` |
| [FINDING-02502](../confirmed/FINDING-02502.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking | `smpmData.fsNominal` |
| [FINDING-02504](../confirmed/FINDING-02504.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking | `smpmData.fsNominal` |
| [FINDING-02546](../confirmed/FINDING-02546.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource | `smpmData.fsNominal` |
| [FINDING-02556](../confirmed/FINDING-02556.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource | `smpmData.fsNominal` |
| [FINDING-02607](../confirmed/FINDING-02607.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL | `smrData.fsNominal` |
| [FINDING-02610](../confirmed/FINDING-02610.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL | `smrData.fsNominal` |
| [FINDING-02655](../confirmed/FINDING-02655.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter | `smrData.fsNominal` |
| [FINDING-02658](../confirmed/FINDING-02658.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter | `smrData.fsNominal` |
| [FINDING-02758](../confirmed/FINDING-02758.md) | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer | `aimcData.fsNominal` |
| [FINDING-02762](../confirmed/FINDING-02762.md) | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer | `aimcData.fsNominal` |
| [FINDING-04894](../confirmed/FINDING-04894.md) | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses | `smpmData.fsNominal` |
| [FINDING-04905](../confirmed/FINDING-04905.md) | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses | `smpmData.fsNominal` |
