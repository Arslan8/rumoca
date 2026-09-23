# Zero leakage inductance is a supported ideal limit

Group `zero-machine-data-leakage` · 42 report instances · false-positives

Lszero and Lssigma represent zero-sequence/stray inductance. They are forwarded to inductor equations that multiply derivatives by L; zero removes the leakage voltage drop. The Basic.Inductor contract explicitly permits zero. This does not excuse fsNominal=0 in the default formula, which is documented as a separate confirmed frequency bug.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0166](../false-positives/DECL-0166.md) | — | `Lszero` |
| [DECL-0167](../false-positives/DECL-0167.md) | — | `Lssigma` |
| [FINDING-01540](../false-positives/FINDING-01540.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking | `imcData.Lszero` |
| [FINDING-01541](../false-positives/FINDING-01541.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking | `imcData.Lssigma` |
| [FINDING-01603](../false-positives/FINDING-01603.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL | `aimcData.Lszero` |
| [FINDING-01604](../false-positives/FINDING-01604.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL | `aimcData.Lssigma` |
| [FINDING-01640](../false-positives/FINDING-01640.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize | `aimcData.Lszero` |
| [FINDING-01641](../false-positives/FINDING-01641.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize | `aimcData.Lssigma` |
| [FINDING-01738](../false-positives/FINDING-01738.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive | `aimcData.Lszero` |
| [FINDING-01739](../false-positives/FINDING-01739.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive | `aimcData.Lssigma` |
| [FINDING-01779](../false-positives/FINDING-01779.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Inverter | `aimcData.Lszero` |
| [FINDING-01780](../false-positives/FINDING-01780.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Inverter | `aimcData.Lssigma` |
| [FINDING-01825](../false-positives/FINDING-01825.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz | `aimcData.Lszero` |
| [FINDING-01826](../false-positives/FINDING-01826.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz | `aimcData.Lssigma` |
| [FINDING-01898](../false-positives/FINDING-01898.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer | `aimcData.Lszero` |
| [FINDING-01899](../false-positives/FINDING-01899.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer | `aimcData.Lssigma` |
| [FINDING-01967](../false-positives/FINDING-01967.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `aimcData.Lszero` |
| [FINDING-01968](../false-positives/FINDING-01968.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `aimcData.Lssigma` |
| [FINDING-02036](../false-positives/FINDING-02036.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD | `aimcData.Lszero` |
| [FINDING-02037](../false-positives/FINDING-02037.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD | `aimcData.Lssigma` |
| [FINDING-02097](../false-positives/FINDING-02097.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aimsData.Lszero` |
| [FINDING-02098](../false-positives/FINDING-02098.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aimsData.Lssigma` |
| [FINDING-02288](../false-positives/FINDING-02288.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking | `smpmData.Lszero` |
| [FINDING-02289](../false-positives/FINDING-02289.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking | `smpmData.Lssigma` |
| [FINDING-02347](../false-positives/FINDING-02347.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_CurrentSource | `smpmData.Lszero` |
| [FINDING-02348](../false-positives/FINDING-02348.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_CurrentSource | `smpmData.Lssigma` |
| [FINDING-02394](../false-positives/FINDING-02394.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Inverter | `smpmData.Lszero` |
| [FINDING-02395](../false-positives/FINDING-02395.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Inverter | `smpmData.Lssigma` |
| [FINDING-02416](../false-positives/FINDING-02416.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad | `smpmData.Lszero` |
| [FINDING-02417](../false-positives/FINDING-02417.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad | `smpmData.Lssigma` |
| [FINDING-02459](../false-positives/FINDING-02459.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking | `smpmData.Lszero` |
| [FINDING-02460](../false-positives/FINDING-02460.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking | `smpmData.Lssigma` |
| [FINDING-02544](../false-positives/FINDING-02544.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource | `smpmData.Lszero` |
| [FINDING-02545](../false-positives/FINDING-02545.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource | `smpmData.Lssigma` |
| [FINDING-02589](../false-positives/FINDING-02589.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL | `smrData.Lszero` |
| [FINDING-02590](../false-positives/FINDING-02590.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL | `smrData.Lssigma` |
| [FINDING-02643](../false-positives/FINDING-02643.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter | `smrData.Lszero` |
| [FINDING-02644](../false-positives/FINDING-02644.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter | `smrData.Lssigma` |
| [FINDING-02748](../false-positives/FINDING-02748.md) | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer | `aimcData.Lszero` |
| [FINDING-02749](../false-positives/FINDING-02749.md) | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer | `aimcData.Lssigma` |
| [FINDING-04891](../false-positives/FINDING-04891.md) | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses | `smpmData.Lszero` |
| [FINDING-04892](../false-positives/FINDING-04892.md) | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses | `smpmData.Lssigma` |
