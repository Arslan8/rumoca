# FINDING-02241: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator |
| Target | smeeData.IeOpenCircuit |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-02241-smee-generator-smeedata-ieopencircuit.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 493f4e75b133cac085ad62680b6e76bc44680dcddcd849e69d64034820cc3db0 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/SynchronousMachineData.mo:18`. Role: `parameter`; binding: `10`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/SynchronousMachineData.mo — source snapshot](../evidence/sources/16b4341f9d5ec816-SynchronousMachineData.mo)

```modelica
16:   final parameter SI.AngularVelocity omega=2*pi*fsNominal
17:     "Nominal angular frequency";
18:   parameter SI.Current IeOpenCircuit(start=10)
19:     "Open circuit excitation current @ nominal voltage and frequency";
20:   parameter Real effectiveStatorTurns=1 "Effective number of stator turns";
21:   final parameter Real turnsRatio=sqrt(2)*VsNominal/(omega*Lmd*
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/4d376a5cb19be7de.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
