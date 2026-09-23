# FINDING-01300: `dcpmData.Ra` in `DC_CompareCharacteristics`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `ideal-dc-machine-data` |
| Original tier | Candidate |
| Sanitizer result | `physical-domain-unenforced` |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics |
| Target | `dcpmData.Ra` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Utilities/ParameterRecords/DcPermanentMagnetData.mo:19` |
| Original report | [FINDING-dc-comparecharacteristics-dcpmdata-ra-unbounded.md](../../bugs/FINDING-dc-comparecharacteristics-dcpmdata-ra-unbounded.md) |
| Original SHA-256 | `792859115713f1d5845433c0ddef79272f19372a78ee77cf3e41b0764538638a` |

## Why this is not a verified bug

This field represents zero-loss armature resistance and is forwarded to a component that uses it multiplicatively: torque balance for inertia, v=R*i for resistance, or v=L*der(i) for inductance. None intrinsically requires division by the field. A specific drive train can still be inconsistent; the missing strictly-positive record bound alone is not a bug.

## Regression action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Evidence basis

Matched model/target source-semantic review from the first audit.

## Original claim

Nothing bounds this declaration at all, so it permits values the physical role forbids, including negative ones. It does **not** claim that any model actually sets such a value.

## Earlier independent review

[Prior report](../../../verifiedBugs/false-positives/FINDING-01134.md)

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
