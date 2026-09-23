# FINDING-04980: A zero-duration ramp is a supported step

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-duration-ramp |
| Model | ModelicaTest.Magnetic.FluxTubes.Sources |
| Target | ramp1.duration |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-sources-ramp1-duration-divunreach.md](../../v2/bugs/FINDING-sources-ramp1-duration-divunreach.md) — reviewed as `FINDING-04980-sources-ramp1-duration.md`, which a later run renamed |
| Original SHA-256 | b3762400f076b59069352421b33a05c6a8fec9ceb5608de2c0259d6bd5580caa |

## Why this is a false positive

The declaration explicitly says duration=0 gives a Step. Division by duration occurs only after time>=startTime and while time<startTime+duration. For duration=0 those conditions cannot both hold, so that branch is unreachable. The independent Ramp control also runs at zero. A Rumoca projection failure for a step is not evidence of a reachable division in this source.

## Source evidence

Compiler/source-resolved declaration: `Blocks/Sources.mo:247`. Role: `parameter`; binding: `1`; effective min: `0.0`; effective max: `None`. 

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

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8bb9ef7f1f1c7179.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `ramp1.duration=0` | clean |

[Independent controls and actual library-record projections](../evidence/control-initialization.json) include source wrappers, compiler options, and full results.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-duration-ramp.md) · [Index](../README.md)
