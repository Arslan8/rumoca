# FINDING-02230: `switchYD.idealCloser.idealClosingSwitch[1].Goff` in `IMC_YD`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `physical-rule-does-not-apply` |
| Original tier | Candidate |
| Sanitizer result | `physical-rule-does-not-apply` |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD |
| Target | `switchYD.idealCloser.idealClosingSwitch[1].Goff` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Interfaces/IdealSwitch.mo:6` |
| Original report | [FINDING-imc-yd-switchyd-idealcloser-idealclosingswitch-1-goff-ruleoff.md](../../bugs/FINDING-imc-yd-switchyd-idealcloser-idealclosingswitch-1-goff-ruleoff.md) |
| Original SHA-256 | `2b54f6da9ef3807784cb33ce3f91cbf11b3421a188c524aced5ca7ae1a3a1c2d` |

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
