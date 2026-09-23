# The alleged divisor is the mathematical constant pi

Group `immutable-pi` · 24 report instances · false-positives

This declaration is protected constant Real pi=Modelica.Constants.pi. It is immutable and nonzero, so the proposed zero witness is unreachable. The detector lost constant-role information while following derived parameter expressions.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-01566](../false-positives/FINDING-01566.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking | `imc.pi` |
| [FINDING-01610](../false-positives/FINDING-01610.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL | `aimc.pi` |
| [FINDING-01646](../false-positives/FINDING-01646.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize | `aimc.pi` |
| [FINDING-01748](../false-positives/FINDING-01748.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive | `aimc.pi` |
| [FINDING-01787](../false-positives/FINDING-01787.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Inverter | `aimc.pi` |
| [FINDING-01832](../false-positives/FINDING-01832.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz | `aimc.pi` |
| [FINDING-01907](../false-positives/FINDING-01907.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer | `aimc.pi` |
| [FINDING-01980](../false-positives/FINDING-01980.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `aimc.pi` |
| [FINDING-02043](../false-positives/FINDING-02043.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD | `aimc.pi` |
| [FINDING-02109](../false-positives/FINDING-02109.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aims.pi` |
| [FINDING-02110](../false-positives/FINDING-02110.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aims.pi` |
| [FINDING-02112](../false-positives/FINDING-02112.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aims.pi` |
| [FINDING-02166](../false-positives/FINDING-02166.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `smee.pi` |
| [FINDING-02230](../false-positives/FINDING-02230.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `smee.pi` |
| [FINDING-02309](../false-positives/FINDING-02309.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking | `smpm.pi` |
| [FINDING-02351](../false-positives/FINDING-02351.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_CurrentSource | `smpm.pi` |
| [FINDING-02399](../false-positives/FINDING-02399.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Inverter | `smpm.pi` |
| [FINDING-02441](../false-positives/FINDING-02441.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad | `smpm.pi` |
| [FINDING-02503](../false-positives/FINDING-02503.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking | `smpm.pi` |
| [FINDING-02552](../false-positives/FINDING-02552.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource | `smpm.pi` |
| [FINDING-02606](../false-positives/FINDING-02606.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL | `smr.pi` |
| [FINDING-02654](../false-positives/FINDING-02654.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter | `smr.pi` |
| [FINDING-02757](../false-positives/FINDING-02757.md) | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer | `aimc.pi` |
| [FINDING-04901](../false-positives/FINDING-04901.md) | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses | `smpm.pi` |
