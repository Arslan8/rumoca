# FINDING-05491: `motor[3].tau_down` in `QuadrotorSIL`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | RigidBody.Examples.QuadrotorSIL |
| Target | `motor[3].tau_down` |
| Declaration/site | `target/cmm/CMM-a642c381/RigidBody/Examples/QuadrotorSIL.mo:84` |
| Original report | [FINDING-quadrotorsil-motor-3-tau-down-divzero-2.md](../../bugs/FINDING-quadrotorsil-motor-3-tau-down-divzero-2.md) |
| Original SHA-256 | `6b21b8fb5180a53823c98902d994f540cf11bc58a546dffc6583f3b6c0152a63` |

## What remains unresolved

The static denominator witness remains arithmetically valid, but independent OpenModelica did not establish the claimed differential failure. The paired execution outcome was `not-attempted-array-element-modifier-needs-specialized-wrapper`; a clean short run is not enough to prove the path can never execute later.

## Evidence needed

Use the generated wrapper as a regression, extend execution to the model's relevant experiment horizon, and obtain a clean baseline plus an attributed numerical failure before calling this a true positive.

## Evidence basis

Source-resolved Rumoca witness plus a conservative, non-confirming OpenModelica paired result.

## OpenModelica paired execution

- Outcome: `not-attempted-array-element-modifier-needs-specialized-wrapper`
- Unmodified baseline: `unknown`
- Source-instantiated trigger: `unknown`

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
