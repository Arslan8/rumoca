# Zero stator leakage inductance is supported

Group `ideal-stator-leakage` · 46 report instances · false-positives

Lszero and Lssigma are passed to scalar/space-phasor inductors whose equations multiply current derivatives by L. Zero is the ideal no-leakage voltage-drop limit; there is no intrinsic reciprocal. The separate fsNominal-derived default formula can still require a positive nominal frequency.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0152](../false-positives/DECL-0152.md) | — | `Lszero` |
| [DECL-0153](../false-positives/DECL-0153.md) | — | `Lssigma` |
| [FINDING-01546](../false-positives/FINDING-01546.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking | `imc.Lszero` |
| [FINDING-01547](../false-positives/FINDING-01547.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking | `imc.Lssigma` |
| [FINDING-01574](../false-positives/FINDING-01574.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL | `aimc.Lszero` |
| [FINDING-01575](../false-positives/FINDING-01575.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL | `aimc.Lssigma` |
| [FINDING-01619](../false-positives/FINDING-01619.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize | `aimc.Lszero` |
| [FINDING-01620](../false-positives/FINDING-01620.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize | `aimc.Lssigma` |
| [FINDING-01718](../false-positives/FINDING-01718.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive | `aimc.Lszero` |
| [FINDING-01719](../false-positives/FINDING-01719.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive | `aimc.Lssigma` |
| [FINDING-01758](../false-positives/FINDING-01758.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Inverter | `aimc.Lszero` |
| [FINDING-01759](../false-positives/FINDING-01759.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Inverter | `aimc.Lssigma` |
| [FINDING-01798](../false-positives/FINDING-01798.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz | `aimc.Lszero` |
| [FINDING-01799](../false-positives/FINDING-01799.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz | `aimc.Lssigma` |
| [FINDING-01841](../false-positives/FINDING-01841.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer | `aimc.Lszero` |
| [FINDING-01842](../false-positives/FINDING-01842.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer | `aimc.Lssigma` |
| [FINDING-01920](../false-positives/FINDING-01920.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `aimc.Lszero` |
| [FINDING-01921](../false-positives/FINDING-01921.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `aimc.Lssigma` |
| [FINDING-01989](../false-positives/FINDING-01989.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD | `aimc.Lszero` |
| [FINDING-01990](../false-positives/FINDING-01990.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD | `aimc.Lssigma` |
| [FINDING-02056](../false-positives/FINDING-02056.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aims.Lszero` |
| [FINDING-02057](../false-positives/FINDING-02057.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aims.Lssigma` |
| [FINDING-02120](../false-positives/FINDING-02120.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `smee.Lszero` |
| [FINDING-02121](../false-positives/FINDING-02121.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `smee.Lssigma` |
| [FINDING-02192](../false-positives/FINDING-02192.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `smee.Lszero` |
| [FINDING-02193](../false-positives/FINDING-02193.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `smee.Lssigma` |
| [FINDING-02259](../false-positives/FINDING-02259.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking | `smpm.Lszero` |
| [FINDING-02260](../false-positives/FINDING-02260.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking | `smpm.Lssigma` |
| [FINDING-02318](../false-positives/FINDING-02318.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_CurrentSource | `smpm.Lszero` |
| [FINDING-02319](../false-positives/FINDING-02319.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_CurrentSource | `smpm.Lssigma` |
| [FINDING-02361](../false-positives/FINDING-02361.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Inverter | `smpm.Lszero` |
| [FINDING-02362](../false-positives/FINDING-02362.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Inverter | `smpm.Lssigma` |
| [FINDING-02419](../false-positives/FINDING-02419.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad | `smpm.Lszero` |
| [FINDING-02420](../false-positives/FINDING-02420.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad | `smpm.Lssigma` |
| [FINDING-02462](../false-positives/FINDING-02462.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking | `smpm.Lszero` |
| [FINDING-02463](../false-positives/FINDING-02463.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking | `smpm.Lssigma` |
| [FINDING-02511](../false-positives/FINDING-02511.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource | `smpm.Lszero` |
| [FINDING-02512](../false-positives/FINDING-02512.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource | `smpm.Lssigma` |
| [FINDING-02562](../false-positives/FINDING-02562.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL | `smr.Lszero` |
| [FINDING-02563](../false-positives/FINDING-02563.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL | `smr.Lssigma` |
| [FINDING-02616](../false-positives/FINDING-02616.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter | `smr.Lszero` |
| [FINDING-02617](../false-positives/FINDING-02617.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter | `smr.Lssigma` |
| [FINDING-02691](../false-positives/FINDING-02691.md) | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer | `aimc.Lszero` |
| [FINDING-02692](../false-positives/FINDING-02692.md) | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer | `aimc.Lssigma` |
| [FINDING-04856](../false-positives/FINDING-04856.md) | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses | `smpm.Lszero` |
| [FINDING-04857](../false-positives/FINDING-04857.md) | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses | `smpm.Lssigma` |
