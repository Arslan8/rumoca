# FINDING-02272: `aims.Lssigma` in `IMS_Start`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `ideal-stator-leakage` |
| Original tier | Candidate |
| Sanitizer result | `physical-domain-unenforced` |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start |
| Target | `aims.Lssigma` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo:23` |
| Original report | [FINDING-ims-start-aims-lssigma-unbounded.md](../../bugs/FINDING-ims-start-aims-lssigma-unbounded.md) |
| Original SHA-256 | `fe99bd5084fa0476d6a9eb87b2bfc3fe0147c89db7f8cd832756a26e9b867cea` |

## Why this is not a verified bug

Lszero and Lssigma are passed to scalar/space-phasor inductors whose equations multiply current derivatives by L. Zero is the ideal no-leakage voltage-drop limit; there is no intrinsic reciprocal. The separate fsNominal-derived default formula can still require a positive nominal frequency.

## Regression action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Evidence basis

Matched model/target source-semantic review from the first audit.

## Original claim

Nothing bounds this declaration at all, so it permits values the physical role forbids, including negative ones. It does **not** claim that any model actually sets such a value.

## Earlier independent review

[Prior report](../../../verifiedBugs/false-positives/FINDING-02057.md)

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
