# FINDING-03817: `rectifier.thyristor_p.idealThyristor[2].Ron` in `ThyristorCenterTap2mPulse_RLV`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `physical-rule-does-not-apply` |
| Original tier | Candidate |
| Sanitizer result | `physical-rule-does-not-apply` |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierCenterTap2mPulse.ThyristorCenterTap2mPulse_RLV |
| Target | `rectifier.thyristor_p.idealThyristor[2].Ron` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Interfaces/IdealSemiconductor.mo:4` |
| Original report | [FINDING-thyristorcentertap2mpulse-rlv-rectifier-thyristor-p-idealthyristor-2-r.md](../../bugs/FINDING-thyristorcentertap2mpulse-rlv-rectifier-thyristor-p-idealthyristor-2-r.md) |
| Original SHA-256 | `8fe354100f0b2ee8e52afd3a5598190b205f21ef6e00954549c12e7d20d9c5d2` |

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
