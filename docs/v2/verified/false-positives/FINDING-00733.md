# FINDING-00733: `oLine50.G[34].alpha` in `SmoothStep`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `divisor-guarded-by-assertion` |
| Original tier | Candidate |
| Sanitizer result | `divisor-guarded-by-assertion` |
| Model | Modelica.Electrical.Analog.Examples.Lines.SmoothStep |
| Target | `oLine50.G[34].alpha` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Basic/Conductor.mo:16` |
| Original report | [FINDING-smoothstep-oline50-g-34-alpha-divguarded.md](../../bugs/FINDING-smoothstep-oline50-g-34-alpha-divguarded.md) |
| Original SHA-256 | `1fcc408823a89509eece02434280be61d6f8c98e73537cb9aca2c5e044f2e2df` |

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
