# FINDING-02310: `aimsData.Lssigma` in `IMS_Start`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `zero-machine-data-leakage` |
| Original tier | Candidate |
| Sanitizer result | `physical-domain-unenforced` |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start |
| Target | `aimsData.Lssigma` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo:23` |
| Original report | [FINDING-ims-start-aimsdata-lssigma-unbounded.md](../../bugs/FINDING-ims-start-aimsdata-lssigma-unbounded.md) |
| Original SHA-256 | `fa42c6c7c4397054a873cabaa2d31b5e3f42a8efc0ed836d0977cbd06dbb7e97` |

## Why this is not a verified bug

Lszero and Lssigma represent zero-sequence/stray inductance. They are forwarded to inductor equations that multiply derivatives by L; zero removes the leakage voltage drop. The Basic.Inductor contract explicitly permits zero. This does not excuse fsNominal=0 in the default formula, which is documented as a separate confirmed frequency bug.

## Regression action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Evidence basis

Matched model/target source-semantic review from the first audit.

## Original claim

Nothing bounds this declaration at all, so it permits values the physical role forbids, including negative ones. It does **not** claim that any model actually sets such a value.

## Earlier independent review

[Prior report](../../../verifiedBugs/false-positives/FINDING-02098.md)

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
