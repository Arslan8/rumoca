# FINDING-01892: `inverter.transistor_n.idealGTOThyristor[3].Goff` in `IMC_InverterDrive`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `physical-zero-is-a-supported-limit` |
| Original tier | Candidate |
| Sanitizer result | `physical-zero-is-a-supported-limit` |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive |
| Target | `inverter.transistor_n.idealGTOThyristor[3].Goff` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Interfaces/IdealSemiconductor.mo:6` |
| Original report | [FINDING-imc-inverterdrive-inverter-transistor-n-idealgtothyristor-3-goff-zerol.md](../../bugs/FINDING-imc-inverterdrive-inverter-transistor-n-idealgtothyristor-3-goff-zerol.md) |
| Original SHA-256 | `350e9ef3c29504e9410048036dacf9665bd515e0eed2aa6bcf28d300e4be2473` |

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
