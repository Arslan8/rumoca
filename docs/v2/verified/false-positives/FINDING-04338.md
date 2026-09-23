# FINDING-04338: `g_mFeYokeSide.alpha` in `SimpleSolenoid`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `divisor-introduced-by-translation` |
| Original tier | Candidate |
| Sanitizer result | `divisor-introduced-by-translation` |
| Model | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid |
| Target | `g_mFeYokeSide.alpha` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/BaseClasses/FixedShape.mo:37` |
| Original report | [FINDING-simplesolenoid-g-mfeyokeside-alpha-divgenerated.md](../../bugs/FINDING-simplesolenoid-g-mfeyokeside-alpha-divgenerated.md) |
| Original SHA-256 | `0518deaae4a63305440b44eb731e7e2f37e8af4b1d1617eed92d1f9fd0b6330c` |

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
