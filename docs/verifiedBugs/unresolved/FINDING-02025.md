# FINDING-02025: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD |
| Target | switchYD.idealOpener.Goff |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-yd-switchyd-idealopener-goff-ruleoff.md](../../v2/bugs/FINDING-imc-yd-switchyd-idealopener-goff-ruleoff.md) — reviewed as `FINDING-02025-imc-yd-switchyd-idealopener-goff.md`, which a later run renamed |
| Original SHA-256 | e3a8b58d0edfb624d67b067dfef164015293cdfa3c1023a24bb97de4df881812 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Polyphase/Ideal/IdealOpeningSwitch.mo:6`. Role: `parameter`; binding: `fill(switchYD.Goff, switchYD.m)`; effective min: `zeros(3)`; effective max: `None`. 

[Electrical/Polyphase/Ideal/IdealOpeningSwitch.mo — source snapshot](../evidence/sources/c7ea2135fdcfb834-IdealOpeningSwitch.mo)

```modelica
4:   parameter SI.Resistance Ron[m](final min=zeros(m), start=
5:         fill(1e-5, m)) "Closed switch resistance";
6:   parameter SI.Conductance Goff[m](final min=zeros(m), start=
7:         fill(1e-5, m)) "Opened switch conductance";
8:   extends Polyphase.Interfaces.ConditionalHeatPort(final mh=m, final T=fill(
9:         293.15, m));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f475b935ebf4281d.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
