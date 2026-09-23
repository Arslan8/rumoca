# FINDING-01112: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.ControlledDCDrives.Utilities.DcdcInverter |
| Target | idealDcDc.unitVoltage |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-01112-dcdcinverter-idealdcdc-unitvoltage.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | cb39b47febfaa0a8f2f938ff883776d27c76e86a06873c053e946befe92929fd |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/ControlledDCDrives/Utilities/IdealDcDc.mo:49`. Role: `constant`; binding: `1`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/ControlledDCDrives/Utilities/IdealDcDc.mo — source snapshot](../evidence/sources/ba67317f59e09830-IdealDcDc.mo)

```modelica
47:     annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
48: protected
49:   constant SI.Voltage unitVoltage=1 annotation(HideResult=true);
50: equation
51:   connect(signalCurrent.p, powerBat.nc)
52:     annotation (Line(points={{10,70},{20,70}},         color={0,0,255}));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/5c10b98e9c2107be.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
