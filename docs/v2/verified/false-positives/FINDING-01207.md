# FINDING-01207: `thyristor_v4_1.Ron` in `ThyristorBehaviourTest`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `divisor-unreachable-under-witness` |
| Original tier | Candidate |
| Sanitizer result | `divisor-unreachable-under-witness` |
| Model | Modelica.Electrical.Analog.Examples.ThyristorBehaviourTest |
| Target | `thyristor_v4_1.Ron` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Semiconductors/Thyristor.mo:59` |
| Original report | [FINDING-thyristorbehaviourtest-thyristor-v4-1-ron-divunreach.md](../../bugs/FINDING-thyristorbehaviourtest-thyristor-v4-1-ron-divunreach.md) |
| Original SHA-256 | `b55c9c836389749175abe2821331d2b3b6d82fe2ca1f842666541179241c6c94` |

## Why this is not a verified bug

The assignment that makes the denominator zero also makes the branch containing the division unreachable. The arithmetic witness is not an executable-path witness.

## Regression action

Keep this as a regression proving the detector suppresses or labels the non-defect correctly.

## Evidence basis

The v2 report's own verdict/proof explicitly declines a defect claim.

## Original claim

The assignment that zeroes the denominator also makes the branch containing the division unreachable, so the division is never evaluated at that value. It does **not** claim that anything is wrong.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
