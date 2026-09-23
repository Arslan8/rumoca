# FINDING-01117: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.ControlledDCDrives.Utilities.LimitedPI |
| Target | k |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-limitedpi-k-divzero.md](../../v2/bugs/FINDING-limitedpi-k-divzero.md) — reviewed as `FINDING-01117-limitedpi-k.md`, which a later run renamed |
| Original SHA-256 | c772c54b416b0da37e1343d699e86cf79a5fc66161624a58605f8e9eac5ac555 |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/ControlledDCDrives/Utilities/LimitedPI.mo:40`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/ControlledDCDrives/Utilities/LimitedPI.mo — source snapshot](../evidence/sources/5727ee15805f587e-LimitedPI.mo)

```modelica
38:   output Real controlError = u - u_m
39:     "Control error (set point - measurement)";
40:   parameter Real k=1 "Gain";
41:   parameter Boolean useI=true "PI else P" annotation(Evaluate=true);
42:   parameter SI.Time Ti(min=Modelica.Constants.small)=1
43:     "Integral time constant (T>0 required)" annotation(Dialog(enable=useI));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/c126e98ef779bb0d.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
