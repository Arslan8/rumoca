# FINDING-05214: `smpm.Rs` in `SMPM_VoltageSourceWithLosses`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `ideal-stator-resistance` |
| Original tier | Candidate |
| Sanitizer result | `physical-domain-unenforced` |
| Model | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses |
| Target | `smpm.Rs` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo:11` |
| Original report | [FINDING-smpm-voltagesourcewithlosses-smpm-rs-unbounded.md](../../bugs/FINDING-smpm-voltagesourcewithlosses-smpm-rs-unbounded.md) |
| Original SHA-256 | `a0f14de560aebc0e08e692aff8a7d49c1d7429e20d4dfe27325e883866681bd9` |

## Why this is not a verified bug

Rs is passed to Polyphase.Basic.Resistor, which delegates to the scalar resistor contract that explicitly allows positive, zero, or negative resistance. Zero removes copper loss; the source does not divide by Rs. A real machine-data recommendation is not a universal equation-domain requirement.

## Regression action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Evidence basis

Matched model/target source-semantic review from the first audit.

## Original claim

Nothing bounds this declaration at all, so it permits values the physical role forbids, including negative ones. It does **not** claim that any model actually sets such a value.

## Earlier independent review

[Prior report](../../../verifiedBugs/false-positives/FINDING-04855.md)

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
