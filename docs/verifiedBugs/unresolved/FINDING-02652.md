# FINDING-02652: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter |
| Target | fNominal |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-02652-smr-inverter-fnominal.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | b8b9c70d61d44cbb9f4ba2496eeb67685087968c2eb1893e779e44f8c81ed8e2 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/SynchronousMachines/SMR_Inverter.mo:8`. Role: `parameter`; binding: `50`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/SynchronousMachines/SMR_Inverter.mo — source snapshot](../evidence/sources/e68be21fe7ce0387-SMR_Inverter.mo)

```modelica
6:   parameter SI.Voltage VNominal=100
7:     "Nominal RMS voltage per phase";
8:   parameter SI.Frequency fNominal=50 "Nominal frequency";
9:   parameter SI.Frequency f=50 "Actual frequency";
10:   parameter SI.Time tRamp=1 "Frequency ramp";
11:   parameter SI.Torque TLoad=46 "Nominal load torque";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/cf686768707ef1f9.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
