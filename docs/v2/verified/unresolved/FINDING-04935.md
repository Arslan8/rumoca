# FINDING-04935: `valve.rho0` in `PumpAndValve`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `baseline-blocked` |
| Original tier | Candidate |
| Sanitizer result | `physical-bound-permits-zero` |
| Model | Modelica.Thermal.FluidHeatFlow.Examples.PumpAndValve |
| Target | `valve.rho0` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Thermal/FluidHeatFlow/Components/Valve.mo:19` |
| Original report | [FINDING-pumpandvalve-valve-rho0-bound.md](../../bugs/FINDING-pumpandvalve-valve-rho0-bound.md) |
| Original SHA-256 | `bf605c89f31b46c30709dd4caede89967819206cb600e249a24fb085999dff0d` |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Evidence needed

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Evidence basis

Matched model/target source-semantic review from the first audit.

## Original claim

The declaration carries `min=0`, and the physical role bound to this variable requires strictly greater than zero. It does **not** claim that zero is *reachable* — the bound permits it, which is a property of the declaration, not an observation of a failure.

## Earlier independent review

[Prior report](../../../verifiedBugs/unresolved/FINDING-04615.md)

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
