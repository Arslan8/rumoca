# FINDING-00203: `R10.IdealCommutingSwitch1.Ron` in `CauerLowPassSC`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `physical-rule-does-not-apply` |
| Original tier | Candidate |
| Sanitizer result | `physical-rule-does-not-apply` |
| Model | Modelica.Electrical.Analog.Examples.CauerLowPassSC |
| Target | `R10.IdealCommutingSwitch1.Ron` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Ideal/IdealTwoWaySwitch.mo:3` |
| Original report | [FINDING-cauerlowpasssc-r10-idealcommutingswitch1-ron-ruleoff.md](../../bugs/FINDING-cauerlowpasssc-r10-idealcommutingswitch1-ron-ruleoff.md) |
| Original SHA-256 | `6b69715652ebaf91cd9e6342903db850500ada191d9ffbccfe7af381a55edde1` |

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
