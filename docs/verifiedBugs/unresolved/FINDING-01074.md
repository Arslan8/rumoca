# FINDING-01074: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.Utilities.Nand |
| Target | TP2.L |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-nand-tp2-l-divguarded.md](../../v2/bugs/FINDING-nand-tp2-l-divguarded.md) — reviewed as `FINDING-01074-nand-tp2-l.md`, which a later run renamed |
| Original SHA-256 | f81bba9c2cc3fed9221a3c587c4c77a9a47778075c2544bac8b3c50906392d2c |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Semiconductors/PMOS.mo:13`. Role: `parameter`; binding: `3.1e-06`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Semiconductors/PMOS.mo — source snapshot](../evidence/sources/25ee152809973557-PMOS.mo)

```modelica
11:           annotation (Placement(transformation(extent={{90,-10},{110,10}})));
12:         parameter SI.Length W=20.0e-6 "Width";
13:         parameter SI.Length L=6.0e-6 "Length";
14:         parameter SI.Transconductance Beta=0.0105e-3 "Transconductance parameter";
15:         parameter SI.Voltage Vt=-1.0 "Zero bias threshold voltage";
16:         parameter Real K2=0.41 "Bulk threshold parameter";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/7f9b52945b4eb304.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
