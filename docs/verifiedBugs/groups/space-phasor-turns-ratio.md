# SpacePhasor permits zero turns ratio then divides by it

Group `space-phasor-turns-ratio` · 22 report instances · confirmed

turnsRatio is an unconstrained parameter and the equation v/turnsRatio=plug_p.pin.v-plug_n.pin.v divides by it directly. Zero is admitted but undefined. This is a declaration/equation defect even when the enclosing machine example is blocked by unrelated runtime limitations.

Require and assert a nonzero turnsRatio before the transformation equation is evaluated. If negative ratios encode winding orientation, enforce abs(turnsRatio)>=small rather than positivity; if only magnitude is supported, document and enforce turnsRatio>0.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-01564](../confirmed/FINDING-01564.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking | `imc.spacePhasorS.turnsRatio` |
| [FINDING-01609](../confirmed/FINDING-01609.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL | `aimc.spacePhasorS.turnsRatio` |
| [FINDING-01645](../confirmed/FINDING-01645.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize | `aimc.spacePhasorS.turnsRatio` |
| [FINDING-01747](../confirmed/FINDING-01747.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive | `aimc.spacePhasorS.turnsRatio` |
| [FINDING-01786](../confirmed/FINDING-01786.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Inverter | `aimc.spacePhasorS.turnsRatio` |
| [FINDING-01831](../confirmed/FINDING-01831.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz | `aimc.spacePhasorS.turnsRatio` |
| [FINDING-01906](../confirmed/FINDING-01906.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer | `aimc.spacePhasorS.turnsRatio` |
| [FINDING-01978](../confirmed/FINDING-01978.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `aimc.spacePhasorS.turnsRatio` |
| [FINDING-02042](../confirmed/FINDING-02042.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD | `aimc.spacePhasorS.turnsRatio` |
| [FINDING-02104](../confirmed/FINDING-02104.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aims.spacePhasorS.turnsRatio` |
| [FINDING-02165](../confirmed/FINDING-02165.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `smee.spacePhasorS.turnsRatio` |
| [FINDING-02229](../confirmed/FINDING-02229.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `smee.spacePhasorS.turnsRatio` |
| [FINDING-02308](../confirmed/FINDING-02308.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking | `smpm.spacePhasorS.turnsRatio` |
| [FINDING-02350](../confirmed/FINDING-02350.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_CurrentSource | `smpm.spacePhasorS.turnsRatio` |
| [FINDING-02398](../confirmed/FINDING-02398.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Inverter | `smpm.spacePhasorS.turnsRatio` |
| [FINDING-02439](../confirmed/FINDING-02439.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad | `smpm.spacePhasorS.turnsRatio` |
| [FINDING-02501](../confirmed/FINDING-02501.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking | `smpm.spacePhasorS.turnsRatio` |
| [FINDING-02551](../confirmed/FINDING-02551.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource | `smpm.spacePhasorS.turnsRatio` |
| [FINDING-02605](../confirmed/FINDING-02605.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL | `smr.spacePhasorS.turnsRatio` |
| [FINDING-02653](../confirmed/FINDING-02653.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter | `smr.spacePhasorS.turnsRatio` |
| [FINDING-02756](../confirmed/FINDING-02756.md) | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer | `aimc.spacePhasorS.turnsRatio` |
| [FINDING-04900](../confirmed/FINDING-04900.md) | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses | `smpm.spacePhasorS.turnsRatio` |
