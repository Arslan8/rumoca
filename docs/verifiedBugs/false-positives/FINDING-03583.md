# FINDING-03583: A zero-duration ramp is a supported step

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-duration-ramp |
| Model | Modelica.Electrical.PowerConverters.Examples.DCDC.ChopperStepDown.ChopperStepDown_RL |
| Target | vRef.duration |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-chopperstepdown-rl-vref-duration-divunreach.md](../../v2/bugs/FINDING-chopperstepdown-rl-vref-duration-divunreach.md) — reviewed as `FINDING-03583-chopperstepdown-rl-vref-duration.md`, which a later run renamed |
| Original SHA-256 | 60a59fea6eba1dca571cfab95a8b09f143e48bdddccd7a93d6cc3de9aeb5fffa |

## Why this is a false positive

The declaration explicitly says duration=0 gives a Step. Division by duration occurs only after time>=startTime and while time<startTime+duration. For duration=0 those conditions cannot both hold, so that branch is unreachable. The independent Ramp control also runs at zero. A Rumoca projection failure for a step is not evidence of a reachable division in this source.

## Source evidence

Compiler/source-resolved declaration: `Blocks/Sources.mo:247`. Role: `parameter`; binding: `0.05`; effective min: `0.0`; effective max: `None`. 

[Blocks/Sources.mo — source snapshot](../evidence/sources/565331012685bd19-Sources.mo)

```modelica
245:     parameter Real height=1 "Height of ramp"
246:       annotation(Dialog(groupImage="modelica://Modelica/Resources/Images/Blocks/Sources/Ramp.png"));
247:     parameter SI.Time duration(min=0.0, start=2)
248:       "Duration of ramp (= 0.0 gives a Step)";
249:     extends Interfaces.SignalSource;
250: 
```

[Blocks/Sources.mo — source snapshot](../evidence/sources/565331012685bd19-Sources.mo)

```modelica
244:   block Ramp "Generate ramp signal"
245:     parameter Real height=1 "Height of ramp"
246:       annotation(Dialog(groupImage="modelica://Modelica/Resources/Images/Blocks/Sources/Ramp.png"));
247:     parameter SI.Time duration(min=0.0, start=2)
248:       "Duration of ramp (= 0.0 gives a Step)";
249:     extends Interfaces.SignalSource;
250: 
251:   equation
252:     y = offset + (if time < startTime then 0 else if time < (startTime +
253:       duration) then (time - startTime)*height/duration else height);
254:     annotation (
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/93f2abf6f300aa3e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

[Independent controls and actual library-record projections](../evidence/control-initialization.json) include source wrappers, compiler options, and full results.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-duration-ramp.md) · [Index](../README.md)
