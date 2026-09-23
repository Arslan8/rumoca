# FINDING-02186: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL |
| Target | smeeData.Td0Subtransient |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-02186-smee-dol-smeedata-td0subtransient.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 71f5da80a6061c3ef6285f5c9ba8692a82f3e90d5506510d6a0fce72020c5c18 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/SynchronousMachineData.mo:39`. Role: `parameter`; binding: `0.006963029`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/SynchronousMachineData.mo — source snapshot](../evidence/sources/16b4341f9d5ec816-SynchronousMachineData.mo)

```modelica
37:   parameter SI.Time Td0Transient(start=0.261177343)
38:     "Open circuit field time constant Td0'";
39:   parameter SI.Time Td0Subtransient(start=0.006963029)
40:     "Open circuit subtransient time constant Td0'', d-axis";
41:   parameter SI.Time Tq0Subtransient(start=0.123345081)
42:     "Open circuit subtransient time constant Tq0'', q-axis";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/60c0c577a4240961.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
