# Zero stator resistance is a supported ideal-loss limit

Group `ideal-stator-resistance` · 23 report instances · false-positives

Rs is passed to Polyphase.Basic.Resistor, which delegates to the scalar resistor contract that explicitly allows positive, zero, or negative resistance. Zero removes copper loss; the source does not divide by Rs. A real machine-data recommendation is not a universal equation-domain requirement.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0708](../false-positives/DECL-0708.md) | — | `Rs` |
| [FINDING-01545](../false-positives/FINDING-01545.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking | `imc.Rs` |
| [FINDING-01573](../false-positives/FINDING-01573.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL | `aimc.Rs` |
| [FINDING-01618](../false-positives/FINDING-01618.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize | `aimc.Rs` |
| [FINDING-01717](../false-positives/FINDING-01717.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive | `aimc.Rs` |
| [FINDING-01757](../false-positives/FINDING-01757.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Inverter | `aimc.Rs` |
| [FINDING-01797](../false-positives/FINDING-01797.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz | `aimc.Rs` |
| [FINDING-01840](../false-positives/FINDING-01840.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer | `aimc.Rs` |
| [FINDING-01919](../false-positives/FINDING-01919.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `aimc.Rs` |
| [FINDING-01988](../false-positives/FINDING-01988.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD | `aimc.Rs` |
| [FINDING-02055](../false-positives/FINDING-02055.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aims.Rs` |
| [FINDING-02119](../false-positives/FINDING-02119.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `smee.Rs` |
| [FINDING-02191](../false-positives/FINDING-02191.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `smee.Rs` |
| [FINDING-02258](../false-positives/FINDING-02258.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking | `smpm.Rs` |
| [FINDING-02317](../false-positives/FINDING-02317.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_CurrentSource | `smpm.Rs` |
| [FINDING-02360](../false-positives/FINDING-02360.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Inverter | `smpm.Rs` |
| [FINDING-02418](../false-positives/FINDING-02418.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad | `smpm.Rs` |
| [FINDING-02461](../false-positives/FINDING-02461.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking | `smpm.Rs` |
| [FINDING-02510](../false-positives/FINDING-02510.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource | `smpm.Rs` |
| [FINDING-02561](../false-positives/FINDING-02561.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL | `smr.Rs` |
| [FINDING-02615](../false-positives/FINDING-02615.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter | `smr.Rs` |
| [FINDING-02690](../false-positives/FINDING-02690.md) | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer | `aimc.Rs` |
| [FINDING-04855](../false-positives/FINDING-04855.md) | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses | `smpm.Rs` |
