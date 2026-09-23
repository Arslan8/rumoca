# FINDING-02316: `aims.spacePhasorR.turnsRatio` in `IMS_Start`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-zero-at-declared-values` |
| Original tier | Candidate |
| Sanitizer result | `divisor-zero-at-declared-values` |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start |
| Target | `aims.spacePhasorR.turnsRatio` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/SpacePhasors/Components/SpacePhasor.mo:26` |
| Original report | [FINDING-ims-start-aims-spacephasorr-turnsratio-divbaseline.md](../../bugs/FINDING-ims-start-aims-spacephasorr-turnsratio-divbaseline.md) |
| Original SHA-256 | `91cbde417deb85cac42ec3169a829d47d682f81ac3bd83a2cd488ca6d1df385f` |

## What remains unresolved

The static artifact says a denominator is zero at declared values, but these four cases lack an independent clean-baseline execution and may still involve conditional-component or path reconstruction. They remain unresolved rather than being called broken baselines.

## Evidence needed

Resolve the path/aggregate value and obtain a clean baseline before assigning blame.

## Evidence basis

The v2 analysis explicitly reports UNKNOWN or lacks independent baseline evidence.

## Original claim

The denominator is zero at the model's own declared values. It does **not** claim that any parameter can be blamed: nothing was changed, so this is a broken baseline rather than a latent hazard.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
