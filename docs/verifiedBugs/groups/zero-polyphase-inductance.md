# Polyphase inductance delegates to zero-capable scalar inductors

Group `zero-polyphase-inductance` · 22 report instances · false-positives

The polyphase component passes each L element to Basic.Inductor. That scalar component explicitly documents positive or zero inductance and uses L*der(i)=v. A universal positive-only finding contradicts the delegated contract.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0181](../false-positives/DECL-0181.md) | — | `L` |
| [FINDING-01658](../false-positives/FINDING-01658.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive | `inductor.L` |
| [FINDING-01871](../false-positives/FINDING-01871.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer | `transformer.l1sigma.L` |
| [FINDING-01876](../false-positives/FINDING-01876.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer | `transformer.l2sigma.L` |
| [FINDING-01973](../false-positives/FINDING-01973.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `inductor.L` |
| [FINDING-02671](../false-positives/FINDING-02671.md) | Modelica.Electrical.Machines.Examples.Transformers.AsymmetricalLoad | `transformer.l1sigma.L` |
| [FINDING-02676](../false-positives/FINDING-02676.md) | Modelica.Electrical.Machines.Examples.Transformers.AsymmetricalLoad | `transformer.l2sigma.L` |
| [FINDING-02721](../false-positives/FINDING-02721.md) | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer | `transformer.l1sigma.L` |
| [FINDING-02726](../false-positives/FINDING-02726.md) | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer | `transformer.l2sigma.L` |
| [FINDING-02794](../false-positives/FINDING-02794.md) | Modelica.Electrical.Machines.Examples.Transformers.Rectifier12pulse | `transformer1.l1sigma.L` |
| [FINDING-02799](../false-positives/FINDING-02799.md) | Modelica.Electrical.Machines.Examples.Transformers.Rectifier12pulse | `transformer1.l2sigma.L` |
| [FINDING-02824](../false-positives/FINDING-02824.md) | Modelica.Electrical.Machines.Examples.Transformers.Rectifier12pulse | `transformer2.l1sigma.L` |
| [FINDING-02829](../false-positives/FINDING-02829.md) | Modelica.Electrical.Machines.Examples.Transformers.Rectifier12pulse | `transformer2.l2sigma.L` |
| [FINDING-02882](../false-positives/FINDING-02882.md) | Modelica.Electrical.Machines.Examples.Transformers.Rectifier6pulse | `transformer1.l1sigma.L` |
| [FINDING-02887](../false-positives/FINDING-02887.md) | Modelica.Electrical.Machines.Examples.Transformers.Rectifier6pulse | `transformer1.l2sigma.L` |
| [FINDING-02910](../false-positives/FINDING-02910.md) | Modelica.Electrical.Machines.Examples.Transformers.TransformerTestbench | `transformer.l1sigma.L` |
| [FINDING-02915](../false-positives/FINDING-02915.md) | Modelica.Electrical.Machines.Examples.Transformers.TransformerTestbench | `transformer.l2sigma.L` |
| [FINDING-02931](../false-positives/FINDING-02931.md) | Modelica.Electrical.Polyphase.Examples.Rectifier | `supplyL.L` |
| [FINDING-02958](../false-positives/FINDING-02958.md) | Modelica.Electrical.Polyphase.Examples.TestSensors | `inductor.L` |
| [FINDING-02974](../false-positives/FINDING-02974.md) | Modelica.Electrical.Polyphase.Examples.TransformerYD | `transformerL.L` |
| [FINDING-02990](../false-positives/FINDING-02990.md) | Modelica.Electrical.Polyphase.Examples.TransformerYY | `transformerL.L` |
| [FINDING-03088](../false-positives/FINDING-03088.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive | `lMains.L` |
