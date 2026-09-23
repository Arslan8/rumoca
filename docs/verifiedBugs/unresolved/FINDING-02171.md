# FINDING-02171: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL |
| Target | smeeData.xd |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-smee-dol-smeedata-xd-divequal-2.md](../../v2/bugs/FINDING-smee-dol-smeedata-xd-divequal-2.md) — reviewed as `FINDING-02171-smee-dol-smeedata-xd.md`, which a later run renamed |
| Original SHA-256 | ac25d421a16addfe9035bfa4411397014caf48a911d570cecdff722823ee14e3 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/SynchronousMachineData.mo:25`. Role: `parameter`; binding: `1.6`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/SynchronousMachineData.mo — source snapshot](../evidence/sources/16b4341f9d5ec816-SynchronousMachineData.mo)

```modelica
23:   parameter Real x0(start=0.1)
24:     "Stator stray inductance per phase (approximately zero impedance) [pu]";
25:   parameter Real xd(start=1.6)
26:     "Synchronous reactance per phase, d-axis [pu]";
27:   parameter Real xq(start=1.6)
28:     "Synchronous reactance per phase, q-axis [pu]";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/60c0c577a4240961.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
