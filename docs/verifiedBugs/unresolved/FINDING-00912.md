# FINDING-00912: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.PI |
| Target | C |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-pi-c-zerolimit.md](../../v2/bugs/FINDING-pi-c-zerolimit.md) — reviewed as `FINDING-00912-pi-c.md`, which a later run renamed |
| Original SHA-256 | 414c3692e33d3aa3db87eda2bd4e36d9dad7ce2042e0f5b8074eb4c19832e48d |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/PI.mo:9`. Role: `parameter`; binding: `((T / k) / R1)`; effective min: `0`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/PI.mo — source snapshot](../evidence/sources/cf132956ae22e33b-PI.mo)

```modelica
7:   parameter SI.Resistance R2=k*R1 "Calculated resistance to reach k";
8:   parameter SI.Time T "Time constant";
9:   parameter SI.Capacitance C=T/k/R1 "Calculated capacitance to reach T";
10:   Basic.Resistor                            r1(R=R1)
11:     annotation (Placement(transformation(extent={{-50,20},{-30,40}})));
12:   Basic.Resistor                            r2(R=R2)
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/0777e46f4d751889.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
