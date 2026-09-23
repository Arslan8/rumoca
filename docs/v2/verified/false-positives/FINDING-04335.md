# FINDING-04335: `armature.stopper_xMin.c` in `SimpleSolenoid`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `physical-zero-is-a-supported-limit` |
| Original tier | Candidate |
| Sanitizer result | `physical-zero-is-a-supported-limit` |
| Model | Modelica.Magnetic.FluxTubes.Examples.SolenoidActuator.Components.SimpleSolenoid |
| Target | `armature.stopper_xMin.c` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Mechanics/Translational/Components/ElastoGap.mo:4` |
| Original report | [FINDING-simplesolenoid-armature-stopper-xmin-c-zerolimit.md](../../bugs/FINDING-simplesolenoid-armature-stopper-xmin-c-zerolimit.md) |
| Original SHA-256 | `afcd92225c687e30b59fbdb327b63528a43f96fcd514951c9ed071bb4b799633` |

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
