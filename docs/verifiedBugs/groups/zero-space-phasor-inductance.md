# Zero space-phasor inductance is an algebraic ideal limit

Group `zero-space-phasor-inductance` · 24 report instances · false-positives

Both axis equations are v_[j]=L[j]*der(i_[j]); L is a multiplier and is never divided. A zero entry sets the corresponding voltage drop to zero. The report applies a strictly-positive heuristic where the component equations support an ideal zero-leakage limit.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0130](../false-positives/DECL-0130.md) | — | `L` |
| [FINDING-01549](../false-positives/FINDING-01549.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking | `imc.lssigma.L` |
| [FINDING-01577](../false-positives/FINDING-01577.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL | `aimc.lssigma.L` |
| [FINDING-01622](../false-positives/FINDING-01622.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize | `aimc.lssigma.L` |
| [FINDING-01721](../false-positives/FINDING-01721.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive | `aimc.lssigma.L` |
| [FINDING-01761](../false-positives/FINDING-01761.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Inverter | `aimc.lssigma.L` |
| [FINDING-01801](../false-positives/FINDING-01801.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz | `aimc.lssigma.L` |
| [FINDING-01844](../false-positives/FINDING-01844.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer | `aimc.lssigma.L` |
| [FINDING-01923](../false-positives/FINDING-01923.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `aimc.lssigma.L` |
| [FINDING-01992](../false-positives/FINDING-01992.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD | `aimc.lssigma.L` |
| [FINDING-02059](../false-positives/FINDING-02059.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aims.lssigma.L` |
| [FINDING-02073](../false-positives/FINDING-02073.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aims.lrsigma.L` |
| [FINDING-02123](../false-positives/FINDING-02123.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `smee.lssigma.L` |
| [FINDING-02195](../false-positives/FINDING-02195.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `smee.lssigma.L` |
| [FINDING-02262](../false-positives/FINDING-02262.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking | `smpm.lssigma.L` |
| [FINDING-02321](../false-positives/FINDING-02321.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_CurrentSource | `smpm.lssigma.L` |
| [FINDING-02364](../false-positives/FINDING-02364.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Inverter | `smpm.lssigma.L` |
| [FINDING-02422](../false-positives/FINDING-02422.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad | `smpm.lssigma.L` |
| [FINDING-02465](../false-positives/FINDING-02465.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking | `smpm.lssigma.L` |
| [FINDING-02514](../false-positives/FINDING-02514.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource | `smpm.lssigma.L` |
| [FINDING-02565](../false-positives/FINDING-02565.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL | `smr.lssigma.L` |
| [FINDING-02619](../false-positives/FINDING-02619.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter | `smr.lssigma.L` |
| [FINDING-02694](../false-positives/FINDING-02694.md) | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer | `aimc.lssigma.L` |
| [FINDING-04860](../false-positives/FINDING-04860.md) | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses | `smpm.lssigma.L` |
