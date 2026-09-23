# FINDING-00527: `oLine4.G[2].alpha` in `CompareLineTrunks`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `divisor-guarded-by-assertion` |
| Original tier | Candidate |
| Sanitizer result | `divisor-guarded-by-assertion` |
| Model | Modelica.Electrical.Analog.Examples.Lines.CompareLineTrunks |
| Target | `oLine4.G[2].alpha` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Basic/Conductor.mo:16` |
| Original report | [FINDING-comparelinetrunks-oline4-g-2-alpha-divguarded.md](../../bugs/FINDING-comparelinetrunks-oline4-g-2-alpha-divguarded.md) |
| Original SHA-256 | `7c2eb42f2bc409a59c7a7395158ac2716f8f4f248b5c2441b68a695143fcd2e2` |

## Why this is not a verified bug

The complete denominator is protected by an existing assertion. The zero assignment is outside the model's admitted domain, so this is not an unguarded divide-by-zero defect.

## Regression action

Keep this as a regression proving the detector suppresses or labels the non-defect correctly.

## Evidence basis

The v2 report's own verdict/proof explicitly declines a defect claim.

## Original claim

The denominator can be zeroed arithmetically, but the model asserts it is bounded away from zero, so the assignment is one the model already rejects. It does **not** claim that anything is wrong — this is reported so a reader can see the guard was found, and can challenge it if it is insufficient.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
