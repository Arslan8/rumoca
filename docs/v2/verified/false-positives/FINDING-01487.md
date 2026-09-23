# FINDING-01487: `dcpm2.Ra` in `DCPM_Drive`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `ideal-dc-armature-ra` |
| Original tier | Candidate |
| Sanitizer result | `physical-domain-unenforced` |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive |
| Target | `dcpm2.Ra` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Interfaces/PartialBasicDCMachine.mo:17` |
| Original report | [FINDING-dcpm-drive-dcpm2-ra-unbounded.md](../../bugs/FINDING-dcpm-drive-dcpm2-ra-unbounded.md) |
| Original SHA-256 | `86f8249e5e1be18a61f46dd336488311034f3eccf0408dce63c858763c7f2936` |

## Why this is not a verified bug

Ra is passed to Basic.Resistor, whose contract explicitly supports zero and signed resistance; zero removes armature copper loss. The partial machine source has no unconditional reciprocal of this parameter. A particular initialization can still be topology-dependent.

## Regression action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Evidence basis

Matched model/target source-semantic review from the first audit.

## Original claim

Nothing bounds this declaration at all, so it permits values the physical role forbids, including negative ones. It does **not** claim that any model actually sets such a value.

## Earlier independent review

[Prior report](../../../verifiedBugs/false-positives/FINDING-01316.md)

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
