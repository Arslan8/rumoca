# FINDING-01675: `dcseData.Re` in `DCSE_SinglePhase`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `baseline-blocked` |
| Original tier | Candidate |
| Sanitizer result | `physical-domain-unenforced` |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_SinglePhase |
| Target | `dcseData.Re` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Utilities/ParameterRecords/DcSeriesExcitedData.mo:5` |
| Original report | [FINDING-dcse-singlephase-dcsedata-re-unbounded.md](../../bugs/FINDING-dcse-singlephase-dcsedata-re-unbounded.md) |
| Original SHA-256 | `3bef9b492b7591a992a70836c510b3fa67832eea5ccfa0b99e65b2c0603e1e30` |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Evidence needed

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Evidence basis

Matched model/target source-semantic review from the first audit.

## Original claim

Nothing bounds this declaration at all, so it permits values the physical role forbids, including negative ones. It does **not** claim that any model actually sets such a value.

## Earlier independent review

[Prior report](../../../verifiedBugs/unresolved/FINDING-01495.md)

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
