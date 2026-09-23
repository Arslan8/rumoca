# Polyphase resistance/conductance delegates to signed scalar elements

Group `signed-polyphase-element` · 63 report instances · false-positives

This component is an array wrapper that passes each R or G to Basic.Resistor/Conductor. The scalar contract explicitly allows positive, zero and negative values and uses a multiplicative constitutive equation. A universal strictly-positive rule is therefore wrong here; a particular singular network requires topology-specific evidence.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0064](../false-positives/DECL-0064.md) | — | `G` |
| [DECL-0734](../false-positives/DECL-0734.md) | — | `R` |
| [FINDING-01548](../false-positives/FINDING-01548.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking | `imc.rs.R` |
| [FINDING-01576](../false-positives/FINDING-01576.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL | `aimc.rs.R` |
| [FINDING-01621](../false-positives/FINDING-01621.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize | `aimc.rs.R` |
| [FINDING-01657](../false-positives/FINDING-01657.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive | `resistor.R` |
| [FINDING-01720](../false-positives/FINDING-01720.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive | `aimc.rs.R` |
| [FINDING-01760](../false-positives/FINDING-01760.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Inverter | `aimc.rs.R` |
| [FINDING-01800](../false-positives/FINDING-01800.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz | `aimc.rs.R` |
| [FINDING-01843](../false-positives/FINDING-01843.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer | `aimc.rs.R` |
| [FINDING-01870](../false-positives/FINDING-01870.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer | `transformer.r1.R` |
| [FINDING-01875](../false-positives/FINDING-01875.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer | `transformer.r2.R` |
| [FINDING-01922](../false-positives/FINDING-01922.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `aimc.rs.R` |
| [FINDING-01972](../false-positives/FINDING-01972.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `resistor.R` |
| [FINDING-01991](../false-positives/FINDING-01991.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD | `aimc.rs.R` |
| [FINDING-02058](../false-positives/FINDING-02058.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aims.rs.R` |
| [FINDING-02072](../false-positives/FINDING-02072.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aims.rr.R` |
| [FINDING-02093](../false-positives/FINDING-02093.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `switchedRheostat.rheostat.R` |
| [FINDING-02122](../false-positives/FINDING-02122.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `smee.rs.R` |
| [FINDING-02194](../false-positives/FINDING-02194.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `smee.rs.R` |
| [FINDING-02261](../false-positives/FINDING-02261.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking | `smpm.rs.R` |
| [FINDING-02320](../false-positives/FINDING-02320.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_CurrentSource | `smpm.rs.R` |
| [FINDING-02363](../false-positives/FINDING-02363.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Inverter | `smpm.rs.R` |
| [FINDING-02421](../false-positives/FINDING-02421.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad | `smpm.rs.R` |
| [FINDING-02464](../false-positives/FINDING-02464.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking | `smpm.rs.R` |
| [FINDING-02482](../false-positives/FINDING-02482.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking | `resistor1.R` |
| [FINDING-02483](../false-positives/FINDING-02483.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking | `resistor2.R` |
| [FINDING-02484](../false-positives/FINDING-02484.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking | `resistor3.R` |
| [FINDING-02513](../false-positives/FINDING-02513.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource | `smpm.rs.R` |
| [FINDING-02564](../false-positives/FINDING-02564.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL | `smr.rs.R` |
| [FINDING-02618](../false-positives/FINDING-02618.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter | `smr.rs.R` |
| [FINDING-02670](../false-positives/FINDING-02670.md) | Modelica.Electrical.Machines.Examples.Transformers.AsymmetricalLoad | `transformer.r1.R` |
| [FINDING-02675](../false-positives/FINDING-02675.md) | Modelica.Electrical.Machines.Examples.Transformers.AsymmetricalLoad | `transformer.r2.R` |
| [FINDING-02693](../false-positives/FINDING-02693.md) | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer | `aimc.rs.R` |
| [FINDING-02720](../false-positives/FINDING-02720.md) | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer | `transformer.r1.R` |
| [FINDING-02725](../false-positives/FINDING-02725.md) | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer | `transformer.r2.R` |
| [FINDING-02793](../false-positives/FINDING-02793.md) | Modelica.Electrical.Machines.Examples.Transformers.Rectifier12pulse | `transformer1.r1.R` |
| [FINDING-02798](../false-positives/FINDING-02798.md) | Modelica.Electrical.Machines.Examples.Transformers.Rectifier12pulse | `transformer1.r2.R` |
| [FINDING-02823](../false-positives/FINDING-02823.md) | Modelica.Electrical.Machines.Examples.Transformers.Rectifier12pulse | `transformer2.r1.R` |
| [FINDING-02828](../false-positives/FINDING-02828.md) | Modelica.Electrical.Machines.Examples.Transformers.Rectifier12pulse | `transformer2.r2.R` |
| [FINDING-02881](../false-positives/FINDING-02881.md) | Modelica.Electrical.Machines.Examples.Transformers.Rectifier6pulse | `transformer1.r1.R` |
| [FINDING-02886](../false-positives/FINDING-02886.md) | Modelica.Electrical.Machines.Examples.Transformers.Rectifier6pulse | `transformer1.r2.R` |
| [FINDING-02898](../false-positives/FINDING-02898.md) | Modelica.Electrical.Machines.Examples.Transformers.TransformerTestbench | `load.R` |
| [FINDING-02909](../false-positives/FINDING-02909.md) | Modelica.Electrical.Machines.Examples.Transformers.TransformerTestbench | `transformer.r1.R` |
| [FINDING-02914](../false-positives/FINDING-02914.md) | Modelica.Electrical.Machines.Examples.Transformers.TransformerTestbench | `transformer.r2.R` |
| [FINDING-02957](../false-positives/FINDING-02957.md) | Modelica.Electrical.Polyphase.Examples.TestSensors | `resistor.R` |
| [FINDING-02973](../false-positives/FINDING-02973.md) | Modelica.Electrical.Polyphase.Examples.TransformerYD | `transformerR.R` |
| [FINDING-02978](../false-positives/FINDING-02978.md) | Modelica.Electrical.Polyphase.Examples.TransformerYD | `loadR.R` |
| [FINDING-02989](../false-positives/FINDING-02989.md) | Modelica.Electrical.Polyphase.Examples.TransformerYY | `transformerR.R` |
| [FINDING-02994](../false-positives/FINDING-02994.md) | Modelica.Electrical.Polyphase.Examples.TransformerYY | `loadR.R` |
| [FINDING-03024](../false-positives/FINDING-03024.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.DiodeBridge2mPulse | `multiStarResistance.resistor.R` |
| [FINDING-03047](../false-positives/FINDING-03047.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.HalfControlledBridge2mPulse | `multiStarResistance.resistor.R` |
| [FINDING-03087](../false-positives/FINDING-03087.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive | `rMains.R` |
| [FINDING-03093](../false-positives/FINDING-03093.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive | `earthing.resistor.R` |
| [FINDING-03121](../false-positives/FINDING-03121.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_RL | `multiStarResistance.resistor.R` |
| [FINDING-03144](../false-positives/FINDING-03144.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_RLV_Characteristic | `multiStarResistance.resistor.R` |
| [FINDING-03168](../false-positives/FINDING-03168.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_RLV | `multiStarResistance.resistor.R` |
| [FINDING-03191](../false-positives/FINDING-03191.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_R | `multiStarResistance.resistor.R` |
| [FINDING-04859](../false-positives/FINDING-04859.md) | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses | `smpm.rs.R` |
| [FINDING-04929](../false-positives/FINDING-04929.md) | ModelicaTest.Electrical.PowerConverters.HalfControlledBridge2mPulse | `multiStarResistance.resistor.R` |
| [FINDING-04930](../false-positives/FINDING-04930.md) | ModelicaTest.Electrical.PowerConverters.HalfControlledBridge2mPulse | `resistor1.R` |
| [FINDING-04950](../false-positives/FINDING-04950.md) | ModelicaTest.Electrical.PowerConverters.ThyristorBridge2mPulse_R | `multiStarResistance.resistor.R` |
| [FINDING-04951](../false-positives/FINDING-04951.md) | ModelicaTest.Electrical.PowerConverters.ThyristorBridge2mPulse_R | `innerResistor.R` |
