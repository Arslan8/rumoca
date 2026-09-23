# FINDING-02334: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_CurrentSource |
| Target | smpm.Lrsigmaq |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smpm-currentsource-smpm-lrsigmaq-intent.md](../../v2/bugs/FINDING-smpm-currentsource-smpm-lrsigmaq-intent.md) — reviewed as `FINDING-02334-smpm-currentsource-smpm-lrsigmaq.md`, which a later run renamed |
| Original SHA-256 | 02fbdcc03ce61da07fe83e425046a2975cd519e201dcce727fb647925865f3de |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo:65`. Role: `parameter`; binding: `smpmData.Lrsigmaq`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo — source snapshot](../evidence/sources/a25907bd0a29e9a2-SM_PermanentMagnet.mo)

```modelica
63:       group="Damper cage",
64:       enable=useDamperCage));
65:   parameter SI.Inductance Lrsigmaq=Lrsigmad
66:     "Damper stray inductance in q-axis" annotation (Dialog(
67:       tab="Nominal resistances and inductances",
68:       group="Damper cage",
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/be4c41c1bbad95dd.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
