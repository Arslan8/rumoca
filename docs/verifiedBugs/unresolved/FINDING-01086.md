# FINDING-01086: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.Utilities.RealSwitch |
| Target | S.Goff |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-realswitch-s-goff-ruleoff.md](../../v2/bugs/FINDING-realswitch-s-goff-ruleoff.md) — reviewed as `FINDING-01086-realswitch-s-goff.md`, which a later run renamed |
| Original SHA-256 | 8916bca2dd7d3efe528c185ea46343de756f87a1ab4ba9af6fea1d74a504c2cf |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Ideal/ControlledIdealTwoWaySwitch.mo:5`. Role: `parameter`; binding: `1e-05`; effective min: `0`; effective max: `None`. 

[Electrical/Analog/Ideal/ControlledIdealTwoWaySwitch.mo — source snapshot](../evidence/sources/769cbc584a98db7c-ControlledIdealTwoWaySwitch.mo)

```modelica
3:   parameter SI.Voltage level=0.5 "Switch level";
4:   parameter SI.Resistance Ron(final min=0) = 1e-5 "Closed switch resistance";
5:   parameter SI.Conductance Goff(final min=0) = 1e-5
6:     "Opened switch conductance";
7:   extends Modelica.Electrical.Analog.Interfaces.ConditionalHeatPort(final T=
8:         293.15);
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8abdd9e56826c53f.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
