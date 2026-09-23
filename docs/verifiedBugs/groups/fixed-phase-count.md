# The alleged zero divisor is constant m=3

Group `fixed-phase-count` · 23 report instances · false-positives

SpacePhasor declares constant Integer m=3. It is not a parameter and cannot be overridden to zero; the transformation matrices therefore divide by the fixed value three. The finding is a variable-role error, not a reachable boundary.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-01568](../false-positives/FINDING-01568.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking | `imc.spacePhasorS.m` |
| [FINDING-01612](../false-positives/FINDING-01612.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL | `aimc.spacePhasorS.m` |
| [FINDING-01648](../false-positives/FINDING-01648.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize | `aimc.spacePhasorS.m` |
| [FINDING-01750](../false-positives/FINDING-01750.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive | `aimc.spacePhasorS.m` |
| [FINDING-01789](../false-positives/FINDING-01789.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Inverter | `aimc.spacePhasorS.m` |
| [FINDING-01834](../false-positives/FINDING-01834.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz | `aimc.spacePhasorS.m` |
| [FINDING-01909](../false-positives/FINDING-01909.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer | `aimc.spacePhasorS.m` |
| [FINDING-01982](../false-positives/FINDING-01982.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `aimc.spacePhasorS.m` |
| [FINDING-02045](../false-positives/FINDING-02045.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD | `aimc.spacePhasorS.m` |
| [FINDING-02111](../false-positives/FINDING-02111.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aims.spacePhasorS.m` |
| [FINDING-02113](../false-positives/FINDING-02113.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aims.spacePhasorR.m` |
| [FINDING-02168](../false-positives/FINDING-02168.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `smee.spacePhasorS.m` |
| [FINDING-02232](../false-positives/FINDING-02232.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `smee.spacePhasorS.m` |
| [FINDING-02311](../false-positives/FINDING-02311.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking | `smpm.spacePhasorS.m` |
| [FINDING-02352](../false-positives/FINDING-02352.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_CurrentSource | `smpm.spacePhasorS.m` |
| [FINDING-02401](../false-positives/FINDING-02401.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Inverter | `smpm.spacePhasorS.m` |
| [FINDING-02443](../false-positives/FINDING-02443.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad | `smpm.spacePhasorS.m` |
| [FINDING-02505](../false-positives/FINDING-02505.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking | `smpm.spacePhasorS.m` |
| [FINDING-02553](../false-positives/FINDING-02553.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource | `smpm.spacePhasorS.m` |
| [FINDING-02608](../false-positives/FINDING-02608.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL | `smr.spacePhasorS.m` |
| [FINDING-02656](../false-positives/FINDING-02656.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter | `smr.spacePhasorS.m` |
| [FINDING-02759](../false-positives/FINDING-02759.md) | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer | `aimc.spacePhasorS.m` |
| [FINDING-04902](../false-positives/FINDING-04902.md) | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses | `smpm.spacePhasorS.m` |
