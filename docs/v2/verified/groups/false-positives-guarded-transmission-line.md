# False positives and explicit non-defects: `guarded-transmission-line`

**9 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

TLine explicitly asserts Z0>0 before its port equations divide by Z0. The declaration lacks a min modifier, but the claimed missing domain enforcement is false because an executable assertion supplies it.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0661](../false-positives/DECL-0661.md) | — | `Z0` | Source/semantic review | [DECL-tline-z0-5.md](../../bugs/DECL-tline-z0-5.md) |
| [FINDING-00500](../false-positives/FINDING-00500.md) | Modelica.Electrical.Analog.Examples.Lines.CompareLineTrunks | `tLine1.Z0` | Source/semantic review | [FINDING-comparelinetrunks-tline1-z0-unbounded.md](../../bugs/FINDING-comparelinetrunks-tline1-z0-unbounded.md) |
| [FINDING-00501](../false-positives/FINDING-00501.md) | Modelica.Electrical.Analog.Examples.Lines.CompareLineTrunks | `tLine2.Z0` | Source/semantic review | [FINDING-comparelinetrunks-tline2-z0-unbounded.md](../../bugs/FINDING-comparelinetrunks-tline2-z0-unbounded.md) |
| [FINDING-00502](../false-positives/FINDING-00502.md) | Modelica.Electrical.Analog.Examples.Lines.CompareLineTrunks | `tLine3.Z0` | Source/semantic review | [FINDING-comparelinetrunks-tline3-z0-unbounded.md](../../bugs/FINDING-comparelinetrunks-tline3-z0-unbounded.md) |
| [FINDING-00503](../false-positives/FINDING-00503.md) | Modelica.Electrical.Analog.Examples.Lines.CompareLineTrunks | `tLine4.Z0` | Source/semantic review | [FINDING-comparelinetrunks-tline4-z0-unbounded.md](../../bugs/FINDING-comparelinetrunks-tline4-z0-unbounded.md) |
| [FINDING-00552](../false-positives/FINDING-00552.md) | Modelica.Electrical.Analog.Examples.Lines.CompareLosslessLines | `line1.Z0` | Source/semantic review | [FINDING-comparelosslesslines-line1-z0-unbounded.md](../../bugs/FINDING-comparelosslesslines-line1-z0-unbounded.md) |
| [FINDING-00553](../false-positives/FINDING-00553.md) | Modelica.Electrical.Analog.Examples.Lines.CompareLosslessLines | `line2.Z0` | Source/semantic review | [FINDING-comparelosslesslines-line2-z0-unbounded.md](../../bugs/FINDING-comparelosslesslines-line2-z0-unbounded.md) |
| [FINDING-00554](../false-positives/FINDING-00554.md) | Modelica.Electrical.Analog.Examples.Lines.CompareLosslessLines | `line3.Z0` | Source/semantic review | [FINDING-comparelosslesslines-line3-z0-unbounded.md](../../bugs/FINDING-comparelosslesslines-line3-z0-unbounded.md) |
| [FINDING-00692](../false-positives/FINDING-00692.md) | Modelica.Electrical.Analog.Examples.Lines.SmoothStep | `tLine.Z0` | Source/semantic review | [FINDING-smoothstep-tline-z0-unbounded.md](../../bugs/FINDING-smoothstep-tline-z0-unbounded.md) |
