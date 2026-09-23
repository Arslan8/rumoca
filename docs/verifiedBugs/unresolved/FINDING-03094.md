# FINDING-03094: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive |
| Target | pulse2.fCut |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-03094-thyristorbridge2mpulse-dc-drive-pulse2-fcut.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 5d599bd56daaa29b19c72dd56c791ba4a0c90e5efa25376761df0de065f61782 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/ACDC/Control/VoltageBridge2mPulse.mo:17`. Role: `parameter`; binding: `100`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/ACDC/Control/VoltageBridge2mPulse.mo — source snapshot](../evidence/sources/bddcf83d01284ef8-VoltageBridge2mPulse.mo)

```modelica
15:   parameter Boolean useFilter=true "Enable use of filter"
16:     annotation (Dialog(tab="Filter"));
17:   parameter SI.Frequency fCut=2*f
18:     "Cut off frequency of filter"
19:     annotation (Dialog(tab="Filter", enable=useFilter));
20:   parameter SI.Voltage vStart[m]=zeros(m)
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/d8e62ee37d41ac80.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
