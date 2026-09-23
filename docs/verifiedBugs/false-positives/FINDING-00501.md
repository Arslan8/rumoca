# FINDING-00501: TLine already guards its parameter domain

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | guarded-transmission-line |
| Model | Modelica.Electrical.Analog.Examples.Lines.CompareLosslessLines |
| Target | line1.Z0 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-comparelosslesslines-line1-z0-unbounded.md](../../v2/bugs/FINDING-comparelosslesslines-line1-z0-unbounded.md) — reviewed as `FINDING-00501-comparelosslesslines-line1-z0.md`, which a later run renamed |
| Original SHA-256 | be157a25f2cce451a41a0f8115132bf20898e0cd26ce1a789372a0b64c7c2b0b |

## Why this is a false positive

TLine explicitly asserts Z0>0 before its port equations divide by Z0. The declaration lacks a min modifier, but the claimed missing domain enforcement is false because an executable assertion supplies it.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Lines/TLine.mo:5`. Role: `parameter`; binding: `z0`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Lines/TLine.mo — source snapshot](../evidence/sources/0aec4d50d219b4ad-TLine.mo)

```modelica
3:   "Lossless transmission line with characteristic impedance Z0 and transmission delay TD"
4:   extends Modelica.Electrical.Analog.Interfaces.TwoPort;
5:   parameter Modelica.Units.SI.Resistance Z0(start=1) "Characteristic impedance";
6:   parameter Modelica.Units.SI.Time TD=0
7:     "Transmission delay: specify > 0 if F and NL are not given";
8:   parameter Modelica.Units.SI.Frequency F=0
```

[Electrical/Analog/Lines/TLine.mo — source snapshot](../evidence/sources/0aec4d50d219b4ad-TLine.mo)

```modelica
2: model TLine
3:   "Lossless transmission line with characteristic impedance Z0 and transmission delay TD"
4:   extends Modelica.Electrical.Analog.Interfaces.TwoPort;
5:   parameter Modelica.Units.SI.Resistance Z0(start=1) "Characteristic impedance";
6:   parameter Modelica.Units.SI.Time TD=0
7:     "Transmission delay: specify > 0 if F and NL are not given";
8:   parameter Modelica.Units.SI.Frequency F=0
9:     "Frequency: specify > 0 if TD is not given";
10:   parameter Real NL=1/4 "Normalized length: specify if TD is not given";
11:   Modelica.Units.SI.Voltage es(start=0) "Voltage source of forward travelling wave";
12:   Modelica.Units.SI.Voltage er(start=0) "Voltage source of reflected wave";
13: protected
14:   parameter Modelica.Units.SI.Time TDi=if F > 0 then NL/F else TD
15:     "Internally used transmission delay";
16: equation
17:   assert(Z0 > 0, "Z0 has to be positive");
18:   assert((F > 0) or (TD > 0), "F or TD has to be positive");
19:   i1 = (v1 - es)/Z0;
20:   i2 = (v2 - er)/Z0;
21:   es = 2*delay(v2, TDi) - delay(er, TDi);
22:   er = 2*delay(v1, TDi) - delay(es, TDi);
23:   annotation (defaultComponentName="line",
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/7d8ac5a7afc90403.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/guarded-transmission-line.md) · [Index](../README.md)
