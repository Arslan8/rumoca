# FINDING-01176: `simpleTriac.thyristor1.Von` in `SimpleTriacCircuit`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `divisor-unreachable-under-witness` |
| Original tier | Candidate |
| Sanitizer result | `divisor-unreachable-under-witness` |
| Model | Modelica.Electrical.Analog.Examples.SimpleTriacCircuit |
| Target | `simpleTriac.thyristor1.Von` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Semiconductors/Thyristor.mo:59` |
| Original report | [FINDING-simpletriaccircuit-simpletriac-thyristor1-von-divunreach-2.md](../../bugs/FINDING-simpletriaccircuit-simpletriac-thyristor1-von-divunreach-2.md) |
| Original SHA-256 | `8c76cf96ca37ce9f0010def9cd28c63a6b1873cef1c498bdb0dc63ed2864849a` |

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
