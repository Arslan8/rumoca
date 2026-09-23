# FINDING-02290: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking |
| Target | diodeBridge2mPulse.RonDiode |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-smpm-braking-diodebridge2mpulse-rondiode-ruleoff.md](../../v2/bugs/FINDING-smpm-braking-diodebridge2mpulse-rondiode-ruleoff.md) — reviewed as `FINDING-02290-smpm-braking-diodebridge2mpulse-rondiode.md`, which a later run renamed |
| Original SHA-256 | e56853fd25072134d531eca3b6b1ca8a9cff78034c6c85ffc60fae81605afe70 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/ACDC/DiodeBridge2mPulse.mo:6`. Role: `parameter`; binding: `0.0001`; effective min: `0`; effective max: `None`. 

[Electrical/PowerConverters/ACDC/DiodeBridge2mPulse.mo — source snapshot](../evidence/sources/276424e74c4a50cd-DiodeBridge2mPulse.mo)

```modelica
4:   import Modelica.Constants.pi;
5:   parameter Integer m(final min=3) = 3 "Number of phases" annotation(Evaluate=true);
6:   parameter SI.Resistance RonDiode(final min=0) = 1e-05
7:     "Closed diode resistance";
8:   parameter SI.Conductance GoffDiode(final min=0) = 1e-05
9:     "Opened diode conductance";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/aa20b722e1669c45.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
