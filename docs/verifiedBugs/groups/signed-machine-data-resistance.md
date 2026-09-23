# Zero/signed machine resistance is an ideal electrical limit

Group `signed-machine-data-resistance` · 21 report instances · false-positives

Rs is a stator resistance data field passed to resistor components. The underlying Basic.Resistor contract explicitly permits positive, zero and negative resistance and uses v=R_actual*i. A real machine normally has positive copper resistance, but the ideal zero-loss limit is mathematically supported; a blanket missing-bound finding is not a bug.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0717](../false-positives/DECL-0717.md) | — | `Rs` |
| [FINDING-01539](../false-positives/FINDING-01539.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking | `imcData.Rs` |
| [FINDING-01602](../false-positives/FINDING-01602.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL | `aimcData.Rs` |
| [FINDING-01639](../false-positives/FINDING-01639.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize | `aimcData.Rs` |
| [FINDING-01737](../false-positives/FINDING-01737.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive | `aimcData.Rs` |
| [FINDING-01778](../false-positives/FINDING-01778.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Inverter | `aimcData.Rs` |
| [FINDING-01824](../false-positives/FINDING-01824.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz | `aimcData.Rs` |
| [FINDING-01897](../false-positives/FINDING-01897.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer | `aimcData.Rs` |
| [FINDING-01966](../false-positives/FINDING-01966.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `aimcData.Rs` |
| [FINDING-02035](../false-positives/FINDING-02035.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD | `aimcData.Rs` |
| [FINDING-02096](../false-positives/FINDING-02096.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aimsData.Rs` |
| [FINDING-02287](../false-positives/FINDING-02287.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking | `smpmData.Rs` |
| [FINDING-02346](../false-positives/FINDING-02346.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_CurrentSource | `smpmData.Rs` |
| [FINDING-02393](../false-positives/FINDING-02393.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Inverter | `smpmData.Rs` |
| [FINDING-02415](../false-positives/FINDING-02415.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad | `smpmData.Rs` |
| [FINDING-02458](../false-positives/FINDING-02458.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking | `smpmData.Rs` |
| [FINDING-02543](../false-positives/FINDING-02543.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource | `smpmData.Rs` |
| [FINDING-02588](../false-positives/FINDING-02588.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL | `smrData.Rs` |
| [FINDING-02642](../false-positives/FINDING-02642.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter | `smrData.Rs` |
| [FINDING-02747](../false-positives/FINDING-02747.md) | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer | `aimcData.Rs` |
| [FINDING-04890](../false-positives/FINDING-04890.md) | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses | `smpmData.Rs` |
