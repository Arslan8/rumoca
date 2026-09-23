# FINDING-00924: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.SignalGenerator |
| Target | R2 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-signalgenerator-r2-unbounded.md](../../v2/bugs/FINDING-signalgenerator-r2-unbounded.md) — reviewed as `FINDING-00924-signalgenerator-r2.md`, which a later run renamed |
| Original SHA-256 | d618ea9771c11845100627c0610166161f8c00ba1350e2fe53502199a4af8ffd |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/SignalGenerator.mo:9`. Role: `parameter`; binding: `1500`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/SignalGenerator.mo — source snapshot](../evidence/sources/e994e2cdd2e5a217-SignalGenerator.mo)

```modelica
7:   parameter SI.Voltage VAmp=10 "Desired amplitude of output";
8:   parameter SI.Resistance R1=1000 "Arbitrary resistance for Schmitt trigger part";
9:   parameter SI.Resistance R2=R1*Vps/VAmp "Calculated resistance for Schmitt trigger to reach VAmp";
10:   parameter SI.Frequency f=10 "Desired frequency";
11:   parameter SI.Resistance R=1000 "Arbitrary resistance of integrator part";
12:   parameter SI.Capacitance C=Vps/VAmp/(4*f*R) "Calculated capacitance of integrator part to reach f";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/c8b9183ee19e69f8.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
