# Signed resistance is intentional and the divisor is bounded away from zero

Group `switched-capacitor-guard` · 45 report instances · false-positives

The model explicitly represents positive or negative resistance. Its capacitance uses clock/max(eps*oneOhm,abs(R)), where protected constant oneOhm=1. Thus R=0 does not zero the denominator, negative R is handled by abs, and oneOhm is a fixed unit-conversion constant in this model rather than a reported adjustable parameter.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0656](../false-positives/DECL-0656.md) | — | `R` |
| [FINDING-00059](../false-positives/FINDING-00059.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R4.R` |
| [FINDING-00060](../false-positives/FINDING-00060.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R5.R` |
| [FINDING-00061](../false-positives/FINDING-00061.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R8.R` |
| [FINDING-00062](../false-positives/FINDING-00062.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R9.R` |
| [FINDING-00084](../false-positives/FINDING-00084.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R4.oneOhm` |
| [FINDING-00090](../false-positives/FINDING-00090.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R5.oneOhm` |
| [FINDING-00096](../false-positives/FINDING-00096.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R8.oneOhm` |
| [FINDING-00102](../false-positives/FINDING-00102.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R9.oneOhm` |
| [FINDING-00103](../false-positives/FINDING-00103.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R1.R` |
| [FINDING-00109](../false-positives/FINDING-00109.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R1.oneOhm` |
| [FINDING-00110](../false-positives/FINDING-00110.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R2.R` |
| [FINDING-00116](../false-positives/FINDING-00116.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R2.oneOhm` |
| [FINDING-00117](../false-positives/FINDING-00117.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R3.R` |
| [FINDING-00123](../false-positives/FINDING-00123.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R3.oneOhm` |
| [FINDING-00124](../false-positives/FINDING-00124.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `Rp1.R` |
| [FINDING-00130](../false-positives/FINDING-00130.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `Rp1.oneOhm` |
| [FINDING-00131](../false-positives/FINDING-00131.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R7.R` |
| [FINDING-00137](../false-positives/FINDING-00137.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R7.oneOhm` |
| [FINDING-00138](../false-positives/FINDING-00138.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R10.R` |
| [FINDING-00144](../false-positives/FINDING-00144.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R10.oneOhm` |
| [FINDING-00145](../false-positives/FINDING-00145.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R11.R` |
| [FINDING-00151](../false-positives/FINDING-00151.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R11.oneOhm` |
| [FINDING-00154](../false-positives/FINDING-00154.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R4.oneOhm` |
| [FINDING-00155](../false-positives/FINDING-00155.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R4.R` |
| [FINDING-00156](../false-positives/FINDING-00156.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R5.oneOhm` |
| [FINDING-00157](../false-positives/FINDING-00157.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R5.R` |
| [FINDING-00158](../false-positives/FINDING-00158.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R8.oneOhm` |
| [FINDING-00159](../false-positives/FINDING-00159.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R8.R` |
| [FINDING-00160](../false-positives/FINDING-00160.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R9.oneOhm` |
| [FINDING-00161](../false-positives/FINDING-00161.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R9.R` |
| [FINDING-00162](../false-positives/FINDING-00162.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R1.oneOhm` |
| [FINDING-00163](../false-positives/FINDING-00163.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R1.R` |
| [FINDING-00164](../false-positives/FINDING-00164.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R2.oneOhm` |
| [FINDING-00165](../false-positives/FINDING-00165.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R2.R` |
| [FINDING-00166](../false-positives/FINDING-00166.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R3.oneOhm` |
| [FINDING-00167](../false-positives/FINDING-00167.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R3.R` |
| [FINDING-00168](../false-positives/FINDING-00168.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `Rp1.oneOhm` |
| [FINDING-00169](../false-positives/FINDING-00169.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `Rp1.R` |
| [FINDING-00170](../false-positives/FINDING-00170.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R7.oneOhm` |
| [FINDING-00171](../false-positives/FINDING-00171.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R7.R` |
| [FINDING-00172](../false-positives/FINDING-00172.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R10.oneOhm` |
| [FINDING-00173](../false-positives/FINDING-00173.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R10.R` |
| [FINDING-00174](../false-positives/FINDING-00174.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R11.oneOhm` |
| [FINDING-00175](../false-positives/FINDING-00175.md) | Modelica.Electrical.Analog.Examples.CauerLowPassSC | `R11.R` |
