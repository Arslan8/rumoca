# FINDING-00984: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.ResonanceCircuits |
| Target | L |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-resonancecircuits-l-divzero-2.md](../../v2/bugs/FINDING-resonancecircuits-l-divzero-2.md) — reviewed as `FINDING-00984-resonancecircuits-l.md`, which a later run renamed |
| Original SHA-256 | a254526e163545193165edd68f30bad524fd1fe8e8a28139564c84a08be3d956 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/ResonanceCircuits.mo:7`. Role: `parameter`; binding: `0.01`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/ResonanceCircuits.mo — source snapshot](../evidence/sources/882b8e7adf51b485-ResonanceCircuits.mo)

```modelica
5:   extends Modelica.Icons.Example;
6:   parameter SI.Capacitance C=0.01 "Capacitance";
7:   parameter SI.Inductance L=0.01 "Inductance";
8:   final parameter SI.Frequency fRes=1/(2*pi*sqrt(L*C)) "Resonance frequency";
9:   parameter Real res=1 "Source to resonance frequency ratio (f/fRes)";
10:   parameter SI.Frequency f=res*fRes "Source frequency";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/ce2af800c951db46.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
