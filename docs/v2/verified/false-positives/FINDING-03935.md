# FINDING-03935: `rectifier.thyristor.idealThyristor[1].Ron` in `ThyristorCenterTapmPulse_RLV`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `physical-rule-does-not-apply` |
| Original tier | Candidate |
| Sanitizer result | `physical-rule-does-not-apply` |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierCenterTapmPulse.ThyristorCenterTapmPulse_RLV |
| Target | `rectifier.thyristor.idealThyristor[1].Ron` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Interfaces/IdealSemiconductor.mo:4` |
| Original report | [FINDING-thyristorcentertapmpulse-rlv-rectifier-thyristor-idealthyristor-1-ron-.md](../../bugs/FINDING-thyristorcentertapmpulse-rlv-rectifier-thyristor-idealthyristor-1-ron-.md) |
| Original SHA-256 | `5cf3fc0c0f678c0437ab5f74415e877336a8de481d2d3d79df1fb473ce107acd` |

## Why this is not a verified bug

The component-specific contract refutes the generic physical rule. The v2 record explicitly says no defect is claimed.

## Regression action

Keep this as a regression proving the detector suppresses or labels the non-defect correctly.

## Evidence basis

The v2 report's own verdict/proof explicitly declines a defect claim.

## Original claim

The component documents this quantity as taking the value it holds, so the rule derived from the si quantity alone does not bind it. It does **not** claim that anything is wrong — this records a rule that was considered and correctly declined, with the contract that declined it.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
