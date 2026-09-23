# FINDING-05302: `rectifier.thyristor_p.Ron` in `ThyristorBridge2mPulse_R`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `physical-rule-does-not-apply` |
| Original tier | Candidate |
| Sanitizer result | `physical-rule-does-not-apply` |
| Model | ModelicaTest.Electrical.PowerConverters.ThyristorBridge2mPulse_R |
| Target | `rectifier.thyristor_p.Ron` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Polyphase/Ideal/IdealThyristor.mo:4` |
| Original report | [FINDING-thyristorbridge2mpulse-r-rectifier-thyristor-p-ron-ruleoff-2.md](../../bugs/FINDING-thyristorbridge2mpulse-r-rectifier-thyristor-p-ron-ruleoff-2.md) |
| Original SHA-256 | `7fe526f66a0f6b95ba8f254a13fd7ab551c5cb50c24bcf134f45af96188c22bf` |

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
