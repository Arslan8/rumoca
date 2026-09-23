# FINDING-01946: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc |
| Target | switchYDwithArc.Goff |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-ydarc-switchydwitharc-goff-ruleoff.md](../../v2/bugs/FINDING-imc-ydarc-switchydwitharc-goff-ruleoff.md) — reviewed as `FINDING-01946-imc-ydarc-switchydwitharc-goff.md`, which a later run renamed |
| Original SHA-256 | 103a92ffe8a9357019301a5e8e05b00f52208f356d40c912784f02e1163b1ac7 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/SwitchYDwithArc.mo:5`. Role: `parameter`; binding: `1e-05`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/SwitchYDwithArc.mo — source snapshot](../evidence/sources/c6f3be8455cf5fa8-SwitchYDwithArc.mo)

```modelica
3:   parameter Integer m=3 "Number of phases" annotation(Evaluate=true);
4:   parameter SI.Resistance Ron=1e-5 "Closed switch resistance";
5:   parameter SI.Conductance Goff=1e-5 "Opened switch conductance";
6:   parameter SI.Time delayTime(final min=0)=0 "Time delay";
7:   parameter SI.Voltage V0(start=30) "Initial arc voltage";
8:   parameter SI.VoltageSlope dVdt(start=10E3) "Arc voltage slope";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/a03f73e52ba0cfd4.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
