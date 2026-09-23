# FINDING-02217: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator |
| Target | smee.Lesigma |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smee-generator-smee-lesigma-zerolimit.md](../../v2/bugs/FINDING-smee-generator-smee-lesigma-zerolimit.md) — reviewed as `FINDING-02217-smee-generator-smee-lesigma.md`, which a later run renamed |
| Original SHA-256 | 30b492d6ee6c19106d39a31cfd76100167eddc954f941a37cf295a5e78cab7f1 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo:161`. Role: `parameter`; binding: `(((((smee.Lmd * (smee.turnsRatio ^ 2)) * 3) / 2) * smee.sigmae) / (1 - smee.sigmae))`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo — source snapshot](../evidence/sources/3bf26424ac9fce16-SM_ElectricalExcited.mo)

```modelica
159:   final parameter Real turnsRatio=sqrt(2)*VsNominal/(2*pi*fsNominal*Lmd*
160:       IeOpenCircuit) "Stator current / excitation current";
161:   final parameter SI.Inductance Lesigma=Lmd*turnsRatio^2*3/
162:       2*sigmae/(1 - sigmae);
163:   Modelica.Blocks.Interfaces.RealOutput damperCageLossPower(final
164:       quantity="Power", final unit="W") "Damper losses";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/4d376a5cb19be7de.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
