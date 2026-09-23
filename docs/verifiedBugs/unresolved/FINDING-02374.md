# FINDING-02374: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Inverter |
| Target | smpm.Lmd |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smpm-inverter-smpm-lmd-unbounded.md](../../v2/bugs/FINDING-smpm-inverter-smpm-lmd-unbounded.md) — reviewed as `FINDING-02374-smpm-inverter-smpm-lmd.md`, which a later run renamed |
| Original SHA-256 | 5434f613677c063365481fb17166bbb91544ab0f1919a116c1a8f21871f25a14 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo:50`. Role: `parameter`; binding: `smpmData.Lmd`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo — source snapshot](../evidence/sources/a25907bd0a29e9a2-SM_PermanentMagnet.mo)

```modelica
48:   parameter SI.Voltage VsOpenCircuit(start=112.3)
49:     "Open circuit RMS voltage per phase @ fsNominal";
50:   parameter SI.Inductance Lmd(start=0.3*ZsRef/(2*pi*fsNominal))
51:     "Stator main field inductance per phase in d-axis"
52:     annotation (Dialog(tab="Nominal resistances and inductances"));
53:   parameter SI.Inductance Lmq(start=0.3*ZsRef/(2*pi*fsNominal))
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/08f6cfe3d6ca76d9.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
