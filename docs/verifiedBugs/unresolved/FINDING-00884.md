# FINDING-00884: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Buffer |
| Target | R1 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-buffer-r1-zerolimit.md](../../v2/bugs/FINDING-buffer-r1-zerolimit.md) — reviewed as `FINDING-00884-buffer-r1.md`, which a later run renamed |
| Original SHA-256 | da01c293d55bce47ef27a8c00343392265cfa24970cec8912a57265c075b33da |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Buffer.mo:5`. Role: `parameter`; binding: `1000`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Buffer.mo — source snapshot](../evidence/sources/88331c0e33cc6eb3-Buffer.mo)

```modelica
3:   extends PartialOpAmp;
4:   parameter Real k(final min=0)=1 "Desired amplification";
5:   parameter SI.Resistance R1=1000 "Resistance at negative pin(s)";
6:   parameter SI.Resistance R2=(k - 1)*R1 "Calculated resistance to reach desired amplification k";
7:   Basic.Resistor                            r1(final R=R1)
8:     annotation (Placement(transformation(extent={{-10,-10},{10,10}},
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/16ddacbc190cee1d.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
