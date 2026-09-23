# FINDING-00950: Zero capacitance is an explicitly supported algebraic limit

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-capacitor |
| Model | Modelica.Electrical.Analog.Examples.ParallelResonance |
| Target | capacitor1.C |
| Student classification | physical-bound-permits-zero |
| Original report | [BUG-parallelresonance-capacitor1-c.md](../../v2/bugs/BUG-parallelresonance-capacitor1-c.md) — reviewed as `FINDING-00950-parallelresonance-capacitor1-c.md`, which a later run renamed |
| Original SHA-256 | a19cb08f706164501c997392f94fcf1cff36e03ec156f1c89731ec3a7c7fe74c |

## Why this is a false positive

The library documentation explicitly says C may be positive or zero, and the constitutive equation is i=C*der(v), with no source division by C. At C=0 the component imposes i=0. Several reported runtime-override failures disappear after source-level recompilation and compatible initialization. A particular topology may still be singular, but the blanket strictly-positive rule contradicts the component contract.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Basic/Capacitor.mo:4`. Role: `parameter`; binding: `(0.001 / (2 * (2 * asin(1.0))))`; effective min: `0`; effective max: `None`. 

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

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/0cc25a901687c470.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `capacitor1.C=0` | reported-failure |

Diagnostic: solve-IR evaluation failed: non-finite derivative evaluation for state 'sineCurrent.p.v'

[Independent OpenModelica wrappers and complete output](../evidence/omc-0cc25a901687c470.json). Baseline: simulation succeeded.

- `capacitor1.C=0` set before translation: LOG_ASSERT        | debug   | division by zero at time 1.949242003084191e-10, (a=0) / (b=0), where divisor b expression is: capacitor1.C.
- Same value declared final, with final-parameter evaluation: simulation succeeded.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-capacitor.md) · [Index](../README.md)
