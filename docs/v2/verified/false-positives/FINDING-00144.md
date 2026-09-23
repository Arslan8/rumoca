# FINDING-00144: `R4.IdealCommutingSwitch1.Goff` in `CauerLowPassSC`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `physical-rule-does-not-apply` |
| Original tier | Candidate |
| Sanitizer result | `physical-rule-does-not-apply` |
| Model | Modelica.Electrical.Analog.Examples.CauerLowPassSC |
| Target | `R4.IdealCommutingSwitch1.Goff` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Ideal/IdealTwoWaySwitch.mo:4` |
| Original report | [FINDING-cauerlowpasssc-r4-idealcommutingswitch1-goff-ruleoff.md](../../bugs/FINDING-cauerlowpasssc-r4-idealcommutingswitch1-goff-ruleoff.md) |
| Original SHA-256 | `00d60fc9ce8c2f7a0e029837f3c26d9f37fdfdd93c1d2884b90f0efcf5714083` |

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
