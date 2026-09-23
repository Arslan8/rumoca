# FINDING-00891: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Der |
| Target | C |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-der-c-zerolimit.md](../../v2/bugs/FINDING-der-c-zerolimit.md) — reviewed as `FINDING-00891-der-c.md`, which a later run renamed |
| Original SHA-256 | 7ca64bc533e749941da131a7d5edb413bb3ea19c719bb0c7ac1ee0c482082414 |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Der.mo:8`. Role: `parameter`; binding: `(k / (((2 * (2 * asin(1.0))) * f) * R))`; effective min: `0`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Der.mo — source snapshot](../evidence/sources/0db365a039713113-Der.mo)

```modelica
6:   parameter SI.Frequency f "Frequency";
7:   parameter SI.Resistance R=1000 "Resistance at output of OpAmp";
8:   parameter SI.Capacitance C=k/(2*pi*f*R) "Calculated capacitance to reach desired amplification k";
9:   SI.Voltage v(start=0)=c.v "Capacitor voltage = state";
10:   Basic.Capacitor                            c(final C=C)
11:     annotation (Placement(transformation(extent={{-50,20},{-30,40}})));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/69a208989c34e9ea.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
