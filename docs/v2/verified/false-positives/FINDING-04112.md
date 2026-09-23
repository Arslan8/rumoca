# FINDING-04112: `hbridge.inverter_p.GoffDiode` in `HBridge_R`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `physical-zero-is-a-supported-limit` |
| Original tier | Candidate |
| Sanitizer result | `physical-zero-is-a-supported-limit` |
| Model | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_R |
| Target | `hbridge.inverter_p.GoffDiode` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/PowerConverters/DCAC/SinglePhase2Level.mo:12` |
| Original report | [FINDING-hbridge-r-hbridge-inverter-p-goffdiode-zerolimit.md](../../bugs/FINDING-hbridge-r-hbridge-inverter-p-goffdiode-zerolimit.md) |
| Original SHA-256 | `10dbbf0f5c2d1a6d61e9bbb6b936492a13ab37c7ccbd2ad6cb7bfdd5c32b71d8` |

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
