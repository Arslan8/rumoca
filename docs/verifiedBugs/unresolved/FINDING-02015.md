# FINDING-02015: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD |
| Target | switchYD.Goff |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-yd-switchyd-goff-ruleoff.md](../../v2/bugs/FINDING-imc-yd-switchyd-goff-ruleoff.md) — reviewed as `FINDING-02015-imc-yd-switchyd-goff.md`, which a later run renamed |
| Original SHA-256 | 26a67ac016ec961353a305584b8944a78cfc8d14eb45bc91c9532cf911a21ad0 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/SwitchYD.mo:5`. Role: `parameter`; binding: `1e-05`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/SwitchYD.mo — source snapshot](../evidence/sources/dee3d978f63daa43-SwitchYD.mo)

```modelica
3:   parameter Integer m=3 "Number of phases" annotation(Evaluate=true);
4:   parameter SI.Resistance Ron=1e-5 "Closed switch resistance";
5:   parameter SI.Conductance Goff=1e-5 "Opened switch conductance";
6:   parameter SI.Time delayTime(final min=0)=0 "Time delay";
7:   Modelica.Electrical.Polyphase.Interfaces.PositivePlug plugSupply(final m=
8:        m) "To grid" annotation (Placement(transformation(extent={{-10,90},{
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f475b935ebf4281d.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
