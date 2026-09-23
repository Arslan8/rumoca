# FINDING-04249: `pmActuator.g_mLeak2.l` in `ArmatureStroke`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `divisor-introduced-by-translation` |
| Original tier | Candidate |
| Sanitizer result | `divisor-introduced-by-translation` |
| Model | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.ArmatureStroke |
| Target | `pmActuator.g_mLeak2.l` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/BaseClasses/Leakage.mo:12` |
| Original report | [FINDING-armaturestroke-pmactuator-g-mleak2-l-divgenerated.md](../../bugs/FINDING-armaturestroke-pmactuator-g-mleak2-l-divgenerated.md) |
| Original SHA-256 | `93aeb0affaf6ba2df262c6064864a1ecabf1981a56305e5ba27c55c848f4d7c7` |

## Why this is not a verified bug

The quotient is a compiler-solved representation of a source equation whose zero value is an algebraic/feature limit. It does not prove a source-level division contract defect.

## Regression action

Keep this as a regression proving the detector suppresses or labels the non-defect correctly.

## Evidence basis

The v2 report's own verdict/proof explicitly declines a defect claim.

## Original claim

Zero is a supported limit of this component; the quotient the dae shows is the compiler's solved form, not a division in the source. It does **not** claim that the source contract is wrong.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
