# MultiStarResistance delegates to zero-capable resistor elements

Group `ideal-multistar-resistance` · 10 report instances · false-positives

R is filled into Polyphase.Basic.Resistor, which delegates to scalar Basic.Resistor. That contract permits zero/signed resistance and uses v=R*i. Zero may create an ideal connection with topology consequences, but the parameter itself is not an unguarded divisor.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0733](../false-positives/DECL-0733.md) | — | `R` |
| [FINDING-03023](../false-positives/FINDING-03023.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.DiodeBridge2mPulse | `multiStarResistance.R` |
| [FINDING-03046](../false-positives/FINDING-03046.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.HalfControlledBridge2mPulse | `multiStarResistance.R` |
| [FINDING-03092](../false-positives/FINDING-03092.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive | `earthing.R` |
| [FINDING-03120](../false-positives/FINDING-03120.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_RL | `multiStarResistance.R` |
| [FINDING-03143](../false-positives/FINDING-03143.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_RLV_Characteristic | `multiStarResistance.R` |
| [FINDING-03167](../false-positives/FINDING-03167.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_RLV | `multiStarResistance.R` |
| [FINDING-03190](../false-positives/FINDING-03190.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_R | `multiStarResistance.R` |
| [FINDING-04928](../false-positives/FINDING-04928.md) | ModelicaTest.Electrical.PowerConverters.HalfControlledBridge2mPulse | `multiStarResistance.R` |
| [FINDING-04949](../false-positives/FINDING-04949.md) | ModelicaTest.Electrical.PowerConverters.ThyristorBridge2mPulse_R | `multiStarResistance.R` |
