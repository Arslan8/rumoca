# ZsRef is fixed to the nonzero value one

Group `fixed-reference-impedance` · 22 report instances · false-positives

The reported parameter is protected final parameter ZsRef=1, used as a dimensional reference. It cannot be modified to zero in a valid extension, so a zero-domain report against it is unreachable.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-01551](../false-positives/FINDING-01551.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking | `imc.ZsRef` |
| [FINDING-01579](../false-positives/FINDING-01579.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL | `aimc.ZsRef` |
| [FINDING-01624](../false-positives/FINDING-01624.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize | `aimc.ZsRef` |
| [FINDING-01723](../false-positives/FINDING-01723.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive | `aimc.ZsRef` |
| [FINDING-01763](../false-positives/FINDING-01763.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Inverter | `aimc.ZsRef` |
| [FINDING-01803](../false-positives/FINDING-01803.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz | `aimc.ZsRef` |
| [FINDING-01846](../false-positives/FINDING-01846.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer | `aimc.ZsRef` |
| [FINDING-01925](../false-positives/FINDING-01925.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `aimc.ZsRef` |
| [FINDING-01994](../false-positives/FINDING-01994.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD | `aimc.ZsRef` |
| [FINDING-02061](../false-positives/FINDING-02061.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aims.ZsRef` |
| [FINDING-02125](../false-positives/FINDING-02125.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `smee.ZsRef` |
| [FINDING-02197](../false-positives/FINDING-02197.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `smee.ZsRef` |
| [FINDING-02264](../false-positives/FINDING-02264.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking | `smpm.ZsRef` |
| [FINDING-02323](../false-positives/FINDING-02323.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_CurrentSource | `smpm.ZsRef` |
| [FINDING-02366](../false-positives/FINDING-02366.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Inverter | `smpm.ZsRef` |
| [FINDING-02424](../false-positives/FINDING-02424.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad | `smpm.ZsRef` |
| [FINDING-02467](../false-positives/FINDING-02467.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking | `smpm.ZsRef` |
| [FINDING-02516](../false-positives/FINDING-02516.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource | `smpm.ZsRef` |
| [FINDING-02567](../false-positives/FINDING-02567.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL | `smr.ZsRef` |
| [FINDING-02621](../false-positives/FINDING-02621.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter | `smr.ZsRef` |
| [FINDING-02696](../false-positives/FINDING-02696.md) | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer | `aimc.ZsRef` |
| [FINDING-04863](../false-positives/FINDING-04863.md) | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses | `smpm.ZsRef` |
