# FINDING-04592: `inertia2.rotorWith3DEffects.J` in `BevelGear1D`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `physical-zero-is-a-supported-limit` |
| Original tier | Candidate |
| Sanitizer result | `physical-zero-is-a-supported-limit` |
| Model | Modelica.Mechanics.MultiBody.Examples.Rotational3DEffects.BevelGear1D |
| Target | `inertia2.rotorWith3DEffects.J` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Mechanics/MultiBody/Parts/Rotor1D.mo:78` |
| Original report | [FINDING-bevelgear1d-inertia2-rotorwith3deffects-j-zerolimit.md](../../bugs/FINDING-bevelgear1d-inertia2-rotorwith3deffects-j-zerolimit.md) |
| Original SHA-256 | `a7c1de61b21786d421debc9386a970016c9db607743f73beaf268bc1794da393` |

## Why this is not a verified bug

The v2 result explicitly records that zero is a supported component limit. It says the positivity rule does not apply and does not claim that the model is defective.

## Regression action

Keep this as a regression proving the detector suppresses or labels the non-defect correctly.

## Evidence basis

The v2 report's own verdict/proof explicitly declines a defect claim.

## Original claim

The positivity rule does **not** apply: this component documents zero as a meaningful limit, so a missing-bound claim would contradict its contract. It does **not** claim that anything is wrong — this records a rule that was considered and correctly declined, with the contract that declined it.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
