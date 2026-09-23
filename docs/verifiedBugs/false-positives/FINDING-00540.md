# FINDING-00540: Zero inductance is an explicitly supported algebraic limit

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-inductor |
| Model | Modelica.Electrical.Analog.Examples.Lines.SmoothStep |
| Target | oLine50.L[14].L |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smoothstep-oline50-l-14-l-zerolimit.md](../../v2/bugs/FINDING-smoothstep-oline50-l-14-l-zerolimit.md) — reviewed as `FINDING-00540-smoothstep-oline50-l-14-l.md`, which a later run renamed |
| Original SHA-256 | 4c4b3a0a19a5694c1a1d1ec4e53923fa5aec2182d0bfb96f051251839219b87a |

## Why this is a false positive

The library documentation explicitly says L may be positive or zero, and the constitutive equation is L*der(i)=v rather than an unconditional division by L. At L=0 the element becomes the algebraic ideal-short constraint v=0. A translator or post-translation state representation that divides by L cannot be used to prove the source declaration wrong; connected topologies and fixed starts may still be inconsistent.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Basic/Inductor.mo:4`. Role: `parameter`; binding: `oLine50.lm[14]`; effective min: `None`; effective max: `None`. 

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

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/21f9fcbcb956ec17.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-inductor.md) · [Index](../README.md)
