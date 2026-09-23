# Bridge parameters explicitly allow the ideal thyristor limit

Group `ideal-thyristor-bridge-zero` · 12 report instances · false-positives

RonThyristor and GoffThyristor have final min=0 and are forwarded to polyphase IdealThyristor, ultimately using IdealSemiconductor multiplicative switching equations. Zero is an intended ideal limit; a specific bridge/network may still require nonzero regularization for numerical structure.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-03055](../false-positives/FINDING-03055.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive | `rectifier.RonThyristor` |
| [FINDING-03056](../false-positives/FINDING-03056.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive | `rectifier.GoffThyristor` |
| [FINDING-03102](../false-positives/FINDING-03102.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_RL | `rectifier.RonThyristor` |
| [FINDING-03103](../false-positives/FINDING-03103.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_RL | `rectifier.GoffThyristor` |
| [FINDING-03125](../false-positives/FINDING-03125.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_RLV_Characteristic | `rectifier.RonThyristor` |
| [FINDING-03126](../false-positives/FINDING-03126.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_RLV_Characteristic | `rectifier.GoffThyristor` |
| [FINDING-03149](../false-positives/FINDING-03149.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_RLV | `rectifier.RonThyristor` |
| [FINDING-03150](../false-positives/FINDING-03150.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_RLV | `rectifier.GoffThyristor` |
| [FINDING-03172](../false-positives/FINDING-03172.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_R | `rectifier.RonThyristor` |
| [FINDING-03173](../false-positives/FINDING-03173.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_R | `rectifier.GoffThyristor` |
| [FINDING-04931](../false-positives/FINDING-04931.md) | ModelicaTest.Electrical.PowerConverters.ThyristorBridge2mPulse_R | `rectifier.RonThyristor` |
| [FINDING-04932](../false-positives/FINDING-04932.md) | ModelicaTest.Electrical.PowerConverters.ThyristorBridge2mPulse_R | `rectifier.GoffThyristor` |
