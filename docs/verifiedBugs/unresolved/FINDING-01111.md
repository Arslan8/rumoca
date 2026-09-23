# FINDING-01111: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.ControlledDCDrives.Utilities.DcdcInverter |
| Target | fS |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-dcdcinverter-fs-divzero-2.md](../../v2/bugs/FINDING-dcdcinverter-fs-divzero-2.md) — reviewed as `FINDING-01111-dcdcinverter-fs.md`, which a later run renamed |
| Original SHA-256 | 3d560dbf6901802ab4caaf088f2aa4fa04b0621664d9dad7b08f7116a6104ae6 |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/ControlledDCDrives/Utilities/DcdcInverter.mo:4`. Role: `parameter`; binding: `None`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/ControlledDCDrives/Utilities/DcdcInverter.mo — source snapshot](../evidence/sources/540ec26d119f3ecf-DcdcInverter.mo)

```modelica
2: model DcdcInverter "DC-DC inverter"
3:   parameter Boolean useIdealInverter=true "Use ideal averaging inverter, otherwise switching inverter";
4:   parameter SI.Frequency fS "Switching frequency";
5:   parameter SI.Time Td=0.5/fS "Dead time";
6:   parameter SI.Time Tmf=2/fS "Measurement filter time constant";
7:   parameter SI.Voltage VMax "Maximum Voltage";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/5c10b98e9c2107be.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
