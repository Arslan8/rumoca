# FINDING-00951: Zero inductance is an explicitly supported algebraic limit

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-inductor |
| Model | Modelica.Electrical.Analog.Examples.ParallelResonance |
| Target | inductor2.L |
| Student classification | physical-domain-unenforced |
| Original report | [BUG-parallelresonance-inductor2-l.md](../../v2/bugs/BUG-parallelresonance-inductor2-l.md) — reviewed as `FINDING-00951-parallelresonance-inductor2-l.md`, which a later run renamed |
| Original SHA-256 | 6c77c4569af3f6f6056124666ae920e6f008f5b83673e4f9e5e03045e0c3f391 |

## Why this is a false positive

The library documentation explicitly says L may be positive or zero, and the constitutive equation is L*der(i)=v rather than an unconditional division by L. At L=0 the element becomes the algebraic ideal-short constraint v=0. A translator or post-translation state representation that divides by L cannot be used to prove the source declaration wrong; connected topologies and fixed starts may still be inconsistent.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Basic/Inductor.mo:4`. Role: `parameter`; binding: `(0.1 / (2 * (2 * asin(1.0))))`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Basic/Inductor.mo — source snapshot](../evidence/sources/fff3148b5c6bf96b-Inductor.mo)

```modelica
2: model Inductor "Ideal linear electrical inductor"
3:   extends Interfaces.OnePort(i(start=0));
4:   parameter SI.Inductance L(start=1) "Inductance";
5: 
6: equation
7:   L*der(i) = v;
```

[Electrical/Analog/Basic/Inductor.mo — source snapshot](../evidence/sources/fff3148b5c6bf96b-Inductor.mo)

```modelica
2: model Inductor "Ideal linear electrical inductor"
3:   extends Interfaces.OnePort(i(start=0));
4:   parameter SI.Inductance L(start=1) "Inductance";
5: 
6: equation
7:   L*der(i) = v;
8:   annotation (
9:     Documentation(info="<html>
10: <p>The linear inductor connects the branch voltage <em>v</em> with the branch current <em>i</em> by <em>v = L * di/dt</em>. The Inductance <em>L</em> is allowed to be positive, or zero.</p>
11: 
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/0cc25a901687c470.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `inductor2.L=0` | reported-failure |

Diagnostic: solve-IR evaluation failed: non-finite derivative evaluation for state 'sineCurrent.n.v'

[Independent OpenModelica wrappers and complete output](../evidence/omc-0cc25a901687c470.json). Baseline: simulation succeeded.

- `inductor2.L=0` set before translation: LOG_ASSERT        | debug   | division by zero at time 1.949242003084191e-10, (a=1.224744871391589e-06) / (b=0), where divisor b expression is: inductor2.L.
- Same value declared final, with final-parameter evaluation: simulation succeeded.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-inductor.md) · [Index](../README.md)
