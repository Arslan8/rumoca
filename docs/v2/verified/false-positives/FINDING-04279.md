# FINDING-04279: `g_mLeak2.l` in `PermeanceActuator`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `divisor-introduced-by-translation` |
| Original tier | Candidate |
| Sanitizer result | `divisor-introduced-by-translation` |
| Model | Modelica.Magnetic.FluxTubes.Examples.MovingCoilActuator.Components.PermeanceActuator |
| Target | `g_mLeak2.l` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/BaseClasses/Leakage.mo:12` |
| Original report | [FINDING-permeanceactuator-g-mleak2-l-divgenerated.md](../../bugs/FINDING-permeanceactuator-g-mleak2-l-divgenerated.md) |
| Original SHA-256 | `0c3e9727bf5ed42b70bd1c970b86f6eb12d1a37b95030f74e717bfd49b999953` |

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
