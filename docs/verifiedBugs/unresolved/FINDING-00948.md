# FINDING-00948: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.OvervoltageProtection |
| Target | zDiode1.Vt |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-overvoltageprotection-zdiode1-vt-divunresolved-2.md](../../v2/bugs/FINDING-overvoltageprotection-zdiode1-vt-divunresolved-2.md) — reviewed as `FINDING-00948-overvoltageprotection-zdiode1-vt.md`, which a later run renamed |
| Original SHA-256 | 82ec5f958184207c7ea0838220cccbdc5a5b19b92b3c0009c184fec0b3ad7ac7 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Semiconductors/ZDiode.mo:5`. Role: `parameter`; binding: `0.04`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Semiconductors/ZDiode.mo — source snapshot](../evidence/sources/0528dc5d485fd8d5-ZDiode.mo)

```modelica
3:   extends Modelica.Electrical.Analog.Interfaces.OnePort;
4:   parameter SI.Current Ids=1e-6 "Saturation current";
5:   parameter SI.Voltage Vt=0.04 "Voltage equivalent of temperature (kT/qn)";
6:   parameter Real Maxexp(final min=Modelica.Constants.small) = 30
7:     "Max. exponent for linear continuation";
8:   parameter SI.Resistance R=1e8 "Parallel ohmic resistance";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/decfc4d4bcc07553.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
