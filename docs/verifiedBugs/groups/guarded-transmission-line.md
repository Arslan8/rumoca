# TLine already guards its parameter domain

Group `guarded-transmission-line` · 17 report instances · false-positives

TLine explicitly asserts Z0>0 before its port equations divide by Z0. The declaration lacks a min modifier, but the claimed missing domain enforcement is false because an executable assertion supplies it.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0661](../false-positives/DECL-0661.md) | — | `Z0` |
| [FINDING-00434](../false-positives/FINDING-00434.md) | Modelica.Electrical.Analog.Examples.Lines.CompareLineTrunks | `tLine1.Z0` |
| [FINDING-00435](../false-positives/FINDING-00435.md) | Modelica.Electrical.Analog.Examples.Lines.CompareLineTrunks | `tLine2.Z0` |
| [FINDING-00436](../false-positives/FINDING-00436.md) | Modelica.Electrical.Analog.Examples.Lines.CompareLineTrunks | `tLine3.Z0` |
| [FINDING-00437](../false-positives/FINDING-00437.md) | Modelica.Electrical.Analog.Examples.Lines.CompareLineTrunks | `tLine4.Z0` |
| [FINDING-00496](../false-positives/FINDING-00496.md) | Modelica.Electrical.Analog.Examples.Lines.CompareLineTrunks | `tLine1.F` |
| [FINDING-00497](../false-positives/FINDING-00497.md) | Modelica.Electrical.Analog.Examples.Lines.CompareLineTrunks | `tLine2.F` |
| [FINDING-00498](../false-positives/FINDING-00498.md) | Modelica.Electrical.Analog.Examples.Lines.CompareLineTrunks | `tLine3.F` |
| [FINDING-00499](../false-positives/FINDING-00499.md) | Modelica.Electrical.Analog.Examples.Lines.CompareLineTrunks | `tLine4.F` |
| [FINDING-00501](../false-positives/FINDING-00501.md) | Modelica.Electrical.Analog.Examples.Lines.CompareLosslessLines | `line1.Z0` |
| [FINDING-00502](../false-positives/FINDING-00502.md) | Modelica.Electrical.Analog.Examples.Lines.CompareLosslessLines | `line2.Z0` |
| [FINDING-00503](../false-positives/FINDING-00503.md) | Modelica.Electrical.Analog.Examples.Lines.CompareLosslessLines | `line3.Z0` |
| [FINDING-00504](../false-positives/FINDING-00504.md) | Modelica.Electrical.Analog.Examples.Lines.CompareLosslessLines | `line1.F` |
| [FINDING-00505](../false-positives/FINDING-00505.md) | Modelica.Electrical.Analog.Examples.Lines.CompareLosslessLines | `line2.F` |
| [FINDING-00506](../false-positives/FINDING-00506.md) | Modelica.Electrical.Analog.Examples.Lines.CompareLosslessLines | `line3.F` |
| [FINDING-00630](../false-positives/FINDING-00630.md) | Modelica.Electrical.Analog.Examples.Lines.SmoothStep | `tLine.Z0` |
| [FINDING-00747](../false-positives/FINDING-00747.md) | Modelica.Electrical.Analog.Examples.Lines.SmoothStep | `tLine.F` |
