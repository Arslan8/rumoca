# FINDING-02084: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start |
| Target | switchedRheostat.RStart |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-ims-start-switchedrheostat-rstart-ruleoff.md](../../v2/bugs/FINDING-ims-start-switchedrheostat-rstart-ruleoff.md) — reviewed as `FINDING-02084-ims-start-switchedrheostat-rstart.md`, which a later run renamed |
| Original SHA-256 | 7b73da1afe211c00136acd21d375f440022d73419e606a36aa5c3d9da08b3dfb |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/SwitchedRheostat.mo:10`. Role: `parameter`; binding: `Rstart`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/SwitchedRheostat.mo — source snapshot](../evidence/sources/2f414fd8730efa93-SwitchedRheostat.mo)

```modelica
8:     "To negative rotor plug" annotation (Placement(transformation(extent={{
9:             90,-50},{110,-70}})));
10:   parameter SI.Resistance RStart "Starting resistance";
11:   parameter SI.Time tStart
12:     "Duration of switching on the starting resistor";
13:   Modelica.Electrical.Polyphase.Basic.Star star(final m=m) annotation (
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2804e4f64ad6a33e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
