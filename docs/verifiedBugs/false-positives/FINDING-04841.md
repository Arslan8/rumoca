# FINDING-04841: unitTime is an immutable nonzero unit constant

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | constant-unit-time |
| Model | ModelicaTest.Blocks.UnitDeduction |
| Target | PID.unitTime |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-04841-unitdeduction-pid-unittime.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 6d069bcf106272916fad07e051fb40b7d0b75e0e585b2fb617ecea6d2247a051 |

## Why this is a false positive

unitTime is declared constant SI.Time unitTime=1 and exists only to satisfy unit checking in ratios. It is not a tunable parameter and cannot take the proposed zero witness. Treating it as a reachable divisor is a role-classification false positive.

## Source evidence

Compiler/source-resolved declaration: `Blocks/Continuous.mo:625`. Role: `constant`; binding: `1`; effective min: `None`; effective max: `None`. 

[Blocks/Continuous.mo — source snapshot](../evidence/sources/e0c05b204354b734-Continuous.mo)

```modelica
623:       annotation(Dialog(enable=initType == Init.InitialOutput, group=
624:             "Initialization"));
625:     constant SI.Time unitTime=1 annotation(HideResult=true);
626: 
627:     Blocks.Math.Gain P(k=1) "Proportional part of PID controller"
628:       annotation (Placement(transformation(extent={{-60,60},{-20,100}})));
```

[Blocks/Continuous.mo — source snapshot](../evidence/sources/e0c05b204354b734-Continuous.mo)

```modelica
623:       annotation(Dialog(enable=initType == Init.InitialOutput, group=
624:             "Initialization"));
625:     constant SI.Time unitTime=1 annotation(HideResult=true);
626: 
627:     Blocks.Math.Gain P(k=1) "Proportional part of PID controller"
628:       annotation (Placement(transformation(extent={{-60,60},{-20,100}})));
629:     Blocks.Continuous.Integrator I(k=unitTime/Ti, y_start=xi_start,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/434be1b21277e1f1.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/constant-unit-time.md) · [Index](../README.md)
