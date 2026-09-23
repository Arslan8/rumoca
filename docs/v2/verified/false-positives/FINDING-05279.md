# FINDING-05279: `rectifier.RonDiode` in `HalfControlledBridge2mPulse`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `physical-rule-does-not-apply` |
| Original tier | Candidate |
| Sanitizer result | `physical-rule-does-not-apply` |
| Model | ModelicaTest.Electrical.PowerConverters.HalfControlledBridge2mPulse |
| Target | `rectifier.RonDiode` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/PowerConverters/ACDC/HalfControlledBridge2mPulse.mo:7` |
| Original report | [FINDING-halfcontrolledbridge2mpulse-rectifier-rondiode-ruleoff-2.md](../../bugs/FINDING-halfcontrolledbridge2mpulse-rectifier-rondiode-ruleoff-2.md) |
| Original SHA-256 | `2c26805e6cd6635694619b1c87d74a05a936d06d496e65130f5d9356f6c81fad` |

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
