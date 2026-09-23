# FINDING-04952: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | ModelicaTest.Electrical.PowerConverters.ThyristorBridge2mPulse_R |
| Target | R |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-thyristorbridge2mpulse-r-r-zerolimit-2.md](../../v2/bugs/FINDING-thyristorbridge2mpulse-r-r-zerolimit-2.md) — reviewed as `FINDING-04952-thyristorbridge2mpulse-r-r.md`, which a later run renamed |
| Original SHA-256 | ba835e5698a022e07d64f13bc472a2f65ccad5af9abf47c1d744de06bb763be4 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `/data/mrumoca/rumoca/target/corpus/ModelicaStandardLibrary-4.1.0/ModelicaTest/Electrical/PowerConverters.mo:131`. Role: `parameter`; binding: `20`; effective min: `None`; effective max: `None`. 

[/data/mrumoca/rumoca/target/corpus/ModelicaStandardLibrary-4.1.0/ModelicaTest/Electrical/PowerConverters.mo — source snapshot](../evidence/sources/d81f06f536e2a0fd-PowerConverters.mo)

```modelica
129:     parameter SI.Angle constantFiringAngle=30*pi/180
130:       "Firing angle";
131:     parameter SI.Resistance R=20 "Load resistance";
132:     Modelica.Electrical.Analog.Basic.Resistor resistor(R=R) annotation (
133:         Placement(transformation(
134:           origin={30,30},
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/3e4bc4f4aebf899e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
