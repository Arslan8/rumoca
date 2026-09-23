# Converter switch parameters delegate to ideal semiconductor limits

Group `ideal-converter-switch-zero` · 36 report instances · false-positives

These values are forwarded to IdealGTOThyristor/IdealDiode, whose IdealSemiconductor equations multiply by Ron or Goff rather than divide. Zero is the exact closed/open ideal limit. Some bridge topologies can become structurally singular, but that requires circuit-specific evidence and does not justify a blanket source-parameter positivity claim.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0068](../false-positives/DECL-0068.md) | — | `GoffTransistor` |
| [DECL-0069](../false-positives/DECL-0069.md) | — | `GoffDiode` |
| [DECL-0748](../false-positives/DECL-0748.md) | — | `RonTransistor` |
| [DECL-0749](../false-positives/DECL-0749.md) | — | `RonDiode` |
| [FINDING-03514](../false-positives/FINDING-03514.md) | Modelica.Electrical.PowerConverters.Examples.DCAC.SinglePhaseTwoLevel.SinglePhaseTwoLevel_RL | `inverter.RonTransistor` |
| [FINDING-03515](../false-positives/FINDING-03515.md) | Modelica.Electrical.PowerConverters.Examples.DCAC.SinglePhaseTwoLevel.SinglePhaseTwoLevel_RL | `inverter.GoffTransistor` |
| [FINDING-03516](../false-positives/FINDING-03516.md) | Modelica.Electrical.PowerConverters.Examples.DCAC.SinglePhaseTwoLevel.SinglePhaseTwoLevel_RL | `inverter.RonDiode` |
| [FINDING-03517](../false-positives/FINDING-03517.md) | Modelica.Electrical.PowerConverters.Examples.DCAC.SinglePhaseTwoLevel.SinglePhaseTwoLevel_RL | `inverter.GoffDiode` |
| [FINDING-03530](../false-positives/FINDING-03530.md) | Modelica.Electrical.PowerConverters.Examples.DCAC.SinglePhaseTwoLevel.SinglePhaseTwoLevel_R | `inverter.RonTransistor` |
| [FINDING-03531](../false-positives/FINDING-03531.md) | Modelica.Electrical.PowerConverters.Examples.DCAC.SinglePhaseTwoLevel.SinglePhaseTwoLevel_R | `inverter.GoffTransistor` |
| [FINDING-03532](../false-positives/FINDING-03532.md) | Modelica.Electrical.PowerConverters.Examples.DCAC.SinglePhaseTwoLevel.SinglePhaseTwoLevel_R | `inverter.RonDiode` |
| [FINDING-03533](../false-positives/FINDING-03533.md) | Modelica.Electrical.PowerConverters.Examples.DCAC.SinglePhaseTwoLevel.SinglePhaseTwoLevel_R | `inverter.GoffDiode` |
| [FINDING-03622](../false-positives/FINDING-03622.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_RL | `hbridge.inverter_p.RonTransistor` |
| [FINDING-03623](../false-positives/FINDING-03623.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_RL | `hbridge.inverter_p.GoffTransistor` |
| [FINDING-03624](../false-positives/FINDING-03624.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_RL | `hbridge.inverter_p.RonDiode` |
| [FINDING-03625](../false-positives/FINDING-03625.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_RL | `hbridge.inverter_p.GoffDiode` |
| [FINDING-03634](../false-positives/FINDING-03634.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_RL | `hbridge.inverter_n.RonTransistor` |
| [FINDING-03635](../false-positives/FINDING-03635.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_RL | `hbridge.inverter_n.GoffTransistor` |
| [FINDING-03636](../false-positives/FINDING-03636.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_RL | `hbridge.inverter_n.RonDiode` |
| [FINDING-03637](../false-positives/FINDING-03637.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_RL | `hbridge.inverter_n.GoffDiode` |
| [FINDING-03654](../false-positives/FINDING-03654.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_R | `hbridge.inverter_p.RonTransistor` |
| [FINDING-03655](../false-positives/FINDING-03655.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_R | `hbridge.inverter_p.GoffTransistor` |
| [FINDING-03656](../false-positives/FINDING-03656.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_R | `hbridge.inverter_p.RonDiode` |
| [FINDING-03657](../false-positives/FINDING-03657.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_R | `hbridge.inverter_p.GoffDiode` |
| [FINDING-03666](../false-positives/FINDING-03666.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_R | `hbridge.inverter_n.RonTransistor` |
| [FINDING-03667](../false-positives/FINDING-03667.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_R | `hbridge.inverter_n.GoffTransistor` |
| [FINDING-03668](../false-positives/FINDING-03668.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_R | `hbridge.inverter_n.RonDiode` |
| [FINDING-03669](../false-positives/FINDING-03669.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_R | `hbridge.inverter_n.GoffDiode` |
| [FINDING-03684](../false-positives/FINDING-03684.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_TrianglePWM_RL | `hbridge.inverter_p.RonTransistor` |
| [FINDING-03685](../false-positives/FINDING-03685.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_TrianglePWM_RL | `hbridge.inverter_p.GoffTransistor` |
| [FINDING-03686](../false-positives/FINDING-03686.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_TrianglePWM_RL | `hbridge.inverter_p.RonDiode` |
| [FINDING-03687](../false-positives/FINDING-03687.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_TrianglePWM_RL | `hbridge.inverter_p.GoffDiode` |
| [FINDING-03696](../false-positives/FINDING-03696.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_TrianglePWM_RL | `hbridge.inverter_n.RonTransistor` |
| [FINDING-03697](../false-positives/FINDING-03697.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_TrianglePWM_RL | `hbridge.inverter_n.GoffTransistor` |
| [FINDING-03698](../false-positives/FINDING-03698.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_TrianglePWM_RL | `hbridge.inverter_n.RonDiode` |
| [FINDING-03699](../false-positives/FINDING-03699.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_TrianglePWM_RL | `hbridge.inverter_n.GoffDiode` |
