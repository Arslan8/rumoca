# Air-gap inductance is used as a flux multiplier

Group `zero-machine-airgap-inductance` · 60 report instances · false-positives

The air-gap model constructs an inductance matrix and computes psi=L*i. Neither the main inductance nor the protected matrix is divided. Zero removes the corresponding magnetic coupling; a useful machine normally needs coupling, but that engineering expectation is not an intrinsic arithmetic-domain failure.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0123](../false-positives/DECL-0123.md) | — | `Lmd` |
| [DECL-0124](../false-positives/DECL-0124.md) | — | `Lmq` |
| [DECL-0125](../false-positives/DECL-0125.md) | — | `L` |
| [DECL-0126](../false-positives/DECL-0126.md) | — | `Lm` |
| [DECL-0127](../false-positives/DECL-0127.md) | — | `L` |
| [FINDING-01556](../false-positives/FINDING-01556.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking | `imc.airGap.Lm` |
| [FINDING-01557](../false-positives/FINDING-01557.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking | `imc.airGap.L` |
| [FINDING-01584](../false-positives/FINDING-01584.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL | `aimc.airGap.Lm` |
| [FINDING-01585](../false-positives/FINDING-01585.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL | `aimc.airGap.L` |
| [FINDING-01629](../false-positives/FINDING-01629.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize | `aimc.airGap.Lm` |
| [FINDING-01630](../false-positives/FINDING-01630.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize | `aimc.airGap.L` |
| [FINDING-01728](../false-positives/FINDING-01728.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive | `aimc.airGap.Lm` |
| [FINDING-01729](../false-positives/FINDING-01729.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive | `aimc.airGap.L` |
| [FINDING-01768](../false-positives/FINDING-01768.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Inverter | `aimc.airGap.Lm` |
| [FINDING-01769](../false-positives/FINDING-01769.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Inverter | `aimc.airGap.L` |
| [FINDING-01808](../false-positives/FINDING-01808.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz | `aimc.airGap.Lm` |
| [FINDING-01809](../false-positives/FINDING-01809.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz | `aimc.airGap.L` |
| [FINDING-01851](../false-positives/FINDING-01851.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer | `aimc.airGap.Lm` |
| [FINDING-01852](../false-positives/FINDING-01852.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer | `aimc.airGap.L` |
| [FINDING-01930](../false-positives/FINDING-01930.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `aimc.airGap.Lm` |
| [FINDING-01931](../false-positives/FINDING-01931.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `aimc.airGap.L` |
| [FINDING-01999](../false-positives/FINDING-01999.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD | `aimc.airGap.Lm` |
| [FINDING-02000](../false-positives/FINDING-02000.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD | `aimc.airGap.L` |
| [FINDING-02066](../false-positives/FINDING-02066.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aims.airGap.Lm` |
| [FINDING-02067](../false-positives/FINDING-02067.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aims.airGap.L` |
| [FINDING-02130](../false-positives/FINDING-02130.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `smee.airGap.Lmd` |
| [FINDING-02131](../false-positives/FINDING-02131.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `smee.airGap.Lmq` |
| [FINDING-02132](../false-positives/FINDING-02132.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `smee.airGap.L` |
| [FINDING-02202](../false-positives/FINDING-02202.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `smee.airGap.Lmd` |
| [FINDING-02203](../false-positives/FINDING-02203.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `smee.airGap.Lmq` |
| [FINDING-02204](../false-positives/FINDING-02204.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `smee.airGap.L` |
| [FINDING-02269](../false-positives/FINDING-02269.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking | `smpm.airGap.Lmd` |
| [FINDING-02270](../false-positives/FINDING-02270.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking | `smpm.airGap.Lmq` |
| [FINDING-02271](../false-positives/FINDING-02271.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking | `smpm.airGap.L` |
| [FINDING-02328](../false-positives/FINDING-02328.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_CurrentSource | `smpm.airGap.Lmd` |
| [FINDING-02329](../false-positives/FINDING-02329.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_CurrentSource | `smpm.airGap.Lmq` |
| [FINDING-02330](../false-positives/FINDING-02330.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_CurrentSource | `smpm.airGap.L` |
| [FINDING-02371](../false-positives/FINDING-02371.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Inverter | `smpm.airGap.Lmd` |
| [FINDING-02372](../false-positives/FINDING-02372.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Inverter | `smpm.airGap.Lmq` |
| [FINDING-02373](../false-positives/FINDING-02373.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Inverter | `smpm.airGap.L` |
| [FINDING-02429](../false-positives/FINDING-02429.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad | `smpm.airGap.Lmd` |
| [FINDING-02430](../false-positives/FINDING-02430.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad | `smpm.airGap.Lmq` |
| [FINDING-02431](../false-positives/FINDING-02431.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad | `smpm.airGap.L` |
| [FINDING-02472](../false-positives/FINDING-02472.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking | `smpm.airGap.Lmd` |
| [FINDING-02473](../false-positives/FINDING-02473.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking | `smpm.airGap.Lmq` |
| [FINDING-02474](../false-positives/FINDING-02474.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking | `smpm.airGap.L` |
| [FINDING-02521](../false-positives/FINDING-02521.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource | `smpm.airGap.Lmd` |
| [FINDING-02522](../false-positives/FINDING-02522.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource | `smpm.airGap.Lmq` |
| [FINDING-02523](../false-positives/FINDING-02523.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource | `smpm.airGap.L` |
| [FINDING-02572](../false-positives/FINDING-02572.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL | `smr.airGap.Lmd` |
| [FINDING-02573](../false-positives/FINDING-02573.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL | `smr.airGap.Lmq` |
| [FINDING-02574](../false-positives/FINDING-02574.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL | `smr.airGap.L` |
| [FINDING-02626](../false-positives/FINDING-02626.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter | `smr.airGap.Lmd` |
| [FINDING-02627](../false-positives/FINDING-02627.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter | `smr.airGap.Lmq` |
| [FINDING-02628](../false-positives/FINDING-02628.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter | `smr.airGap.L` |
| [FINDING-02701](../false-positives/FINDING-02701.md) | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer | `aimc.airGap.Lm` |
| [FINDING-02702](../false-positives/FINDING-02702.md) | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer | `aimc.airGap.L` |
| [FINDING-04868](../false-positives/FINDING-04868.md) | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses | `smpm.airGap.Lmd` |
| [FINDING-04869](../false-positives/FINDING-04869.md) | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses | `smpm.airGap.Lmq` |
| [FINDING-04870](../false-positives/FINDING-04870.md) | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses | `smpm.airGap.L` |
