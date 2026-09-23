# FINDING-00103: `l2` in `CauerLowPassOPV`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `baseline-blocked` |
| Original tier | Candidate |
| Sanitizer result | `physical-bound-permits-zero` |
| Model | Modelica.Electrical.Analog.Examples.CauerLowPassOPV |
| Target | `l2` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/CauerLowPassOPV.mo:6` |
| Original report | [FINDING-cauerlowpassopv-l2-bound.md](../../bugs/FINDING-cauerlowpassopv-l2-bound.md) |
| Original SHA-256 | `8411584b8cf2b383ae45e1a06e86356a9f8c7c3deeb944b05e31c8e8ec68502d` |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Evidence needed

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Evidence basis

Matched model/target source-semantic review from the first audit.

## Original claim

The declaration carries `min=0`, and the physical role bound to this variable requires strictly greater than zero. It does **not** claim that zero is *reachable* — the bound permits it, which is a property of the declaration, not an observation of a failure.

## Earlier independent review

[Prior report](../../../verifiedBugs/unresolved/FINDING-00042.md)

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
