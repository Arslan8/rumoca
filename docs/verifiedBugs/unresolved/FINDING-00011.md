# FINDING-00011: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Clocked.Examples.Systems.Utilities.ComponentsMixingUnit.CriticalDamping |
| Target | normalized |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-00011-criticaldamping-normalized.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | cc1c8b0a98ee015cf6161e97ac297ea9dbc97a23d8e266699b41c435e2d77d02 |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Clocked/Examples/Systems/Utilities/ComponentsMixingUnit/CriticalDamping.mo:10`. Role: `parameter`; binding: `True`; effective min: `None`; effective max: `None`. 

[Clocked/Examples/Systems/Utilities/ComponentsMixingUnit/CriticalDamping.mo — source snapshot](../evidence/sources/39e253add206d755-CriticalDamping.mo)

```modelica
8:   parameter Integer n=2 "Order of filter";
9:   parameter SI.Frequency f(start=1) "Cut-off frequency";
10:   parameter Boolean normalized = true
11:     "= true, if amplitude at f_cut is 3 dB, otherwise unmodified filter";
12:   output Real x[n](start=zeros(n)) "Filter states";
13: protected
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/20269371d4d94b00.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
