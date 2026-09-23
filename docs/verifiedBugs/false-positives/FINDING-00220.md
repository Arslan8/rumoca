# FINDING-00220: Zero capacitance is an explicitly supported algebraic limit

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-capacitor |
| Model | Modelica.Electrical.Analog.Examples.DifferenceAmplifier |
| Target | C5.C |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-differenceamplifier-c5-c-zerolimit.md](../../v2/bugs/FINDING-differenceamplifier-c5-c-zerolimit.md) — reviewed as `FINDING-00220-differenceamplifier-c5-c.md`, which a later run renamed |
| Original SHA-256 | 8efb2a5d810e661d80153f8a0e5263c95e2a2571bb930b32813ef4d11e67c2e8 |

## Why this is a false positive

The library documentation explicitly says C may be positive or zero, and the constitutive equation is i=C*der(v), with no source division by C. At C=0 the component imposes i=0. Several reported runtime-override failures disappear after source-level recompilation and compatible initialization. A particular topology may still be singular, but the blanket strictly-positive rule contradicts the component contract.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Basic/Capacitor.mo:4`. Role: `parameter`; binding: `1e-10`; effective min: `0`; effective max: `None`. 

[Electrical/Analog/Basic/Capacitor.mo — source snapshot](../evidence/sources/441fb6d5cbd9ea34-Capacitor.mo)

```modelica
2: model Capacitor "Ideal linear electrical capacitor"
3:   extends Interfaces.OnePort(v(start=0));
4:   parameter SI.Capacitance C(start=1) "Capacitance";
5: 
6: equation
7:   i = C*der(v);
```

[Electrical/Analog/Basic/Capacitor.mo — source snapshot](../evidence/sources/441fb6d5cbd9ea34-Capacitor.mo)

```modelica
2: model Capacitor "Ideal linear electrical capacitor"
3:   extends Interfaces.OnePort(v(start=0));
4:   parameter SI.Capacitance C(start=1) "Capacitance";
5: 
6: equation
7:   i = C*der(v);
8:   annotation (
9:     Documentation(info="<html>
10: <p>The linear capacitor connects the branch voltage <em>v</em> with the branch current <em>i</em> by <em>i = C * dv/dt</em>. The Capacitance <em>C</em> is allowed to be positive or zero.</p>
11: 
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/a3f2f2f9a1ca72bf.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-capacitor.md) · [Index](../README.md)
