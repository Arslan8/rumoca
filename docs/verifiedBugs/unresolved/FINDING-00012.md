# FINDING-00012: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Clocked.Examples.Systems.Utilities.ComponentsMixingUnit.FilterOrder |
| Target | mixingUnit.c0 |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-filterorder-mixingunit-c0-divzero-2.md](../../v2/bugs/FINDING-filterorder-mixingunit-c0-divzero-2.md) — reviewed as `FINDING-00012-filterorder-mixingunit-c0.md`, which a later run renamed |
| Original SHA-256 | 375030ecd18b42275b7bfd8a812724a0e3941ba95bb6e7c297dac29912921110 |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Clocked/Examples/Systems/Utilities/ComponentsMixingUnit/MixingUnit.mo:13`. Role: `parameter`; binding: `0.848`; effective min: `None`; effective max: `None`. 

[Clocked/Examples/Systems/Utilities/ComponentsMixingUnit/MixingUnit.mo — source snapshot](../evidence/sources/425e46e253745701-MixingUnit.mo)

```modelica
11:     "Temperature in mixing unit"
12:     annotation (Placement(transformation(extent={{100,-80},{140,-40}})));
13:   parameter Real c0(unit="mol/l") = 0.848 "Nominal concentration";
14:   parameter SI.Temperature T0 = 308.5 "Nominal temperature";
15:   parameter Real a1 = 0.2674 "Process parameter (see references in help)";
16:   parameter Real a21 = 1.815 "Process parameter (see references in help)";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/d5252c4962b43c83.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
