# FINDING-00999: Saturating-inductor ordering is already asserted

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | asserted-inductance-order |
| Model | Modelica.Electrical.Analog.Examples.ShowSaturatingInductor |
| Target | SaturatingInductance1.Lzer |
| Student classification | divisor-zero-when-parameters-equal |
| Original report | [FINDING-showsaturatinginductor-saturatinginductance1-lzer-zerolimit.md](../../v2/bugs/FINDING-showsaturatinginductor-saturatinginductance1-lzer-zerolimit.md) — reviewed as `FINDING-00999-showsaturatinginductor-saturatinginductance1-lzer.md`, which a later run renamed |
| Original SHA-256 | 6112b71e471f8c21835aae146a5567a80f08917f6efce01ebe0b710dca0e7081 |

## Why this is a false positive

The source asserts Lzer>Lnom*(1+eps) and Linf<Lnom*(1-eps), and documents the same ordering. The reported positive-nominal equality violates these existing relational constraints; the claim that no assertion excludes it is false. This is not a claim that every compiler schedules diagnostic assertions before evaluating invalid initial equations.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Basic/SaturatingInductor.mo:12`. Role: `parameter`; binding: `Lzer`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Basic/SaturatingInductor.mo — source snapshot](../evidence/sources/e05b77099ac62435-SaturatingInductor.mo)

```modelica
10:   parameter SI.Inductance Lnom(start=1)
11:     "Nominal inductance at Nominal current";
12:   parameter SI.Inductance Lzer(start=2*Lnom)
13:     "Inductance near current=0";
14:   parameter SI.Inductance Linf(start=Lnom/2)
15:     "Inductance at large currents";
```

[Electrical/Analog/Basic/SaturatingInductor.mo — source snapshot](../evidence/sources/e05b77099ac62435-SaturatingInductor.mo)

```modelica
21:   (Lnom - Linf)/(Lzer - Linf)=Ipar/Inom*(pi/2 - atan(Ipar/Inom));
22: equation
23:   assert(Lzer > Lnom*(1 + eps), "Lzer (= " + String(Lzer) +
24:     ") has to be > Lnom (= " + String(Lnom) + ")");
25:   assert(Linf < Lnom*(1 - eps), "Linf (= " + String(Linf) +
26:     ") has to be < Lnom (= " + String(Lnom) + ")");
27:   Lact = Linf + (Lzer - Linf)*(if noEvent(abs(i)/Ipar<small) then 1 else atan(i/Ipar)/(i/Ipar));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/b3892488197c6c55.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/asserted-inductance-order.md) · [Index](../README.md)
