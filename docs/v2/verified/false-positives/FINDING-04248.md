# FINDING-04248: `pmActuator.g_mLeak1.l_g` in `ArmatureStroke`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `divisor-unreachable-under-witness` |
| Original tier | Candidate |
| Sanitizer result | `divisor-unreachable-under-witness` |
| Model | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke |
| Target | `pmActuator.g_mLeak1.l_g` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/Shapes/Leakage/CoaxCylindersEndFaces.mo:21` |
| Original report | [FINDING-armaturestroke-pmactuator-g-mleak1-l-g-divunreach.md](../../bugs/FINDING-armaturestroke-pmactuator-g-mleak1-l-g-divunreach.md) |
| Original SHA-256 | `f3a8b375eac0926795629cbead9d1a9f699ab1a5f782e63cadf9ce602fca35fb` |

## Why this is not a verified bug

The assignment that makes the denominator zero also makes the branch containing the division unreachable. The arithmetic witness is not an executable-path witness.

## Regression action

Keep this as a regression proving the detector suppresses or labels the non-defect correctly.

## Evidence basis

The v2 report's own verdict/proof explicitly declines a defect claim.

## Original claim

The assignment that zeroes the denominator also makes the branch containing the division unreachable, so the division is never evaluated at that value. It does **not** claim that anything is wrong.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
