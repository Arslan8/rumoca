# FINDING-02555: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource |
| Target | rotorDisplacementAngle.m |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-02555-smpm-voltagesource-rotordisplacementangle-m.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 3236ee118d84194e79b751f9dd544b1d6aee666071e0814e62f120748ed6b82c |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Sensors/RotorDisplacementAngle.mo:3`. Role: `parameter`; binding: `3`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Sensors/RotorDisplacementAngle.mo — source snapshot](../evidence/sources/0c4c31900d7e280f-RotorDisplacementAngle.mo)

```modelica
1: within Modelica.Electrical.Machines.Sensors;
2: model RotorDisplacementAngle "Rotor lagging angle"
3:   parameter Integer m=3 "Number of phases" annotation(Evaluate=true);
4:   parameter Integer p(min=1) "Number of pole pairs";
5:   parameter Boolean positiveRange=false "Use only positive output range, if true";
6:   parameter Real threshold(final min=0)=0 "Below threshold the voltage is considered as zero";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/d529fc5d98897b6a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
