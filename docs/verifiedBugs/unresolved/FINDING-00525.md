# FINDING-00525: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.Lines.SmoothStep |
| Target | oLine5.rm |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smoothstep-oline5-rm-zerolimit.md](../../v2/bugs/FINDING-smoothstep-oline5-rm-zerolimit.md) — reviewed as `FINDING-00525-smoothstep-oline5-rm.md`, which a later run renamed |
| Original SHA-256 | fdd0562e347556312d204841625705431741bab5085b882273c1eeb485a716be |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Lines/OLine.mo:72`. Role: `parameter`; binding: `{((oLine5.r * oLine5.length) / (oLine5.N * 2)), (if ((2 == 1) or (2 == (oLine5.N + 1))) then ((oLine5.r * oLine5.length) / (oLine5.N * 2)) else ((oLine5.r * oLine5.length) / oLine5.N)), (if ((3 == 1) or (3 == (oLine5.N + 1))) then ((oLine5.r * oLine5.length) / (oLine5.N * 2)) else ((oLine5.r * oLine5.length) / oLine5.N)), (if ((4 == 1) or (4 == (oLine5.N + 1))) then ((oLine5.r * oLine5.length) / (oLine5.N * 2)) else ((oLine5.r * oLine5.length) / oLine5.N)), (if ((5 == 1) or (5 == (oLine5.N + 1))) then ((oLine5.r * oLine5.length) / (oLine5.N * 2)) else ((oLine5.r * oLine5.length) / oLine5.N)), (if ((6 == 1) or (6 == (oLine5.N + 1))) then ((oLine5.r * oLine5.length) / (oLine5.N * 2)) else ((oLine5.r * oLine5.length) / oLine5.N))}`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Lines/OLine.mo — source snapshot](../evidence/sources/9e7b2c3ed45998ed-OLine.mo)

```modelica
70:     useHeatPort=fill(useHeatPort, N),
71:     T=fill(T, N));
72:   parameter SI.Resistance rm[N + 1]=
73:   {if i==1 or i==N + 1 then r*length/(N*2) else r*length/N for i in 1:N+1};
74:   parameter SI.Inductance lm[N + 1]=
75:   {if i==1 or i==N + 1 then l*length/(N*2) else l*length/N for i in 1:N+1};
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/21f9fcbcb956ec17.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
