# FINDING-02314: `aimsData.Rr` in `IMS_Start`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `baseline-blocked` |
| Original tier | Candidate |
| Sanitizer result | `physical-domain-unenforced` |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start |
| Target | `aimsData.Rr` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Utilities/ParameterRecords/IM_SlipRingData.mo:19` |
| Original report | [FINDING-ims-start-aimsdata-rr-unbounded.md](../../bugs/FINDING-ims-start-aimsdata-rr-unbounded.md) |
| Original SHA-256 | `87bb42e8e24e354287bc8f2fe10c0b6a4cc48f162151fe59cc628e0429e5efbe` |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Evidence needed

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Evidence basis

Matched model/target source-semantic review from the first audit.

## Original claim

Nothing bounds this declaration at all, so it permits values the physical role forbids, including negative ones. It does **not** claim that any model actually sets such a value.

## Earlier independent review

[Prior report](../../../verifiedBugs/unresolved/FINDING-02102.md)

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
