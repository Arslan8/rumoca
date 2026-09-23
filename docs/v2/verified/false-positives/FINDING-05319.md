# FINDING-05319: `R` in `ThyristorBridge2mPulse_R`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `physical-zero-is-a-supported-limit` |
| Original tier | Candidate |
| Sanitizer result | `physical-zero-is-a-supported-limit` |
| Model | ModelicaTest.Electrical.PowerConverters.ThyristorBridge2mPulse_R |
| Target | `R` |
| Declaration/site | `target/corpus/ModelicaStandardLibrary-4.1.0/ModelicaTest/Electrical/PowerConverters.mo:131` |
| Original report | [FINDING-thyristorbridge2mpulse-r-r-zerolimit-2.md](../../bugs/FINDING-thyristorbridge2mpulse-r-r-zerolimit-2.md) |
| Original SHA-256 | `89133a7fbfb7a7322c70aba661bef855974b704981ac94c615c667ddbe2fe31d` |

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
