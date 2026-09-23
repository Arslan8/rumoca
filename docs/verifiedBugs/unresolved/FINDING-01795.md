# FINDING-01795: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz |
| Target | Cs |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-imc-steinmetz-cs-zerolimit.md](../../v2/bugs/FINDING-imc-steinmetz-cs-zerolimit.md) — reviewed as `FINDING-01795-imc-steinmetz-cs.md`, which a later run renamed |
| Original SHA-256 | 60ebf5e7f1333164a4541674b94a9edbfb71606e14c419a233ae87ce94d85918 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/InductionMachines/IMC_Steinmetz.mo:12`. Role: `parameter`; binding: `(5 * Cr)`; effective min: `0`; effective max: `None`. 

[Electrical/Machines/Examples/InductionMachines/IMC_Steinmetz.mo — source snapshot](../evidence/sources/39e3cc5c9f815c15-IMC_Steinmetz.mo)

```modelica
10:   parameter SI.Capacitance Cr=0.0035
11:     "Motor's running capacitor";
12:   parameter SI.Capacitance Cs=5*Cr
13:     "Motor's (additional) starting capacitor";
14:   parameter SI.AngularVelocity wSwitch(displayUnit="rev/min")=
15:        1350*2*Modelica.Constants.pi/60
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/00227f080db37cf1.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
