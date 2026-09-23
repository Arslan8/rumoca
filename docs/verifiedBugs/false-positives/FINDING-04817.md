# FINDING-04817: unitTime is an immutable nonzero unit constant

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | constant-unit-time |
| Model | ModelicaTest.Blocks.StrictLimiters |
| Target | PID2.unitTime |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-04817-strictlimiters-pid2-unittime.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | e4d4723997978239b6593a700ee0e8494d1e2f44905a16a2207748767c588df9 |

## Why this is a false positive

unitTime is declared constant SI.Time unitTime=1 and exists only to satisfy unit checking in ratios. It is not a tunable parameter and cannot take the proposed zero witness. Treating it as a reachable divisor is a role-classification false positive.

## Source evidence

Compiler/source-resolved declaration: `Blocks/Continuous.mo:817`. Role: `constant`; binding: `1`; effective min: `None`; effective max: `None`. 

[Blocks/Continuous.mo — source snapshot](../evidence/sources/e0c05b204354b734-Continuous.mo)

```modelica
815:     parameter Boolean strict=false "= true, if strict limits with noEvent(..)"
816:       annotation (Evaluate=true, choices(checkBox=true), Dialog(tab="Advanced"));
817:     constant SI.Time unitTime=1 annotation (HideResult=true);
818:     Modelica.Blocks.Interfaces.RealInput u_ff if withFeedForward
819:       "Optional connector of feed-forward input signal"
820:      annotation (Placement(
```

[Blocks/Continuous.mo — source snapshot](../evidence/sources/e0c05b204354b734-Continuous.mo)

```modelica
815:     parameter Boolean strict=false "= true, if strict limits with noEvent(..)"
816:       annotation (Evaluate=true, choices(checkBox=true), Dialog(tab="Advanced"));
817:     constant SI.Time unitTime=1 annotation (HideResult=true);
818:     Modelica.Blocks.Interfaces.RealInput u_ff if withFeedForward
819:       "Optional connector of feed-forward input signal"
820:      annotation (Placement(
821:           transformation(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/da5e02db6db34fbd.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/constant-unit-time.md) · [Index](../README.md)
