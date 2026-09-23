# FINDING-03064: `transformer.l2sigma.inductor[3].L` in `IMC_Transformer`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `physical-zero-is-a-supported-limit` |
| Original tier | Candidate |
| Sanitizer result | `physical-zero-is-a-supported-limit` |
| Model | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer |
| Target | `transformer.l2sigma.inductor[3].L` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Basic/Inductor.mo:4` |
| Original report | [FINDING-imc-transformer-transformer-l2sigma-inductor-3-l-zerolimit-2.md](../../bugs/FINDING-imc-transformer-transformer-l2sigma-inductor-3-l-zerolimit-2.md) |
| Original SHA-256 | `bfd4a38e75aacf0aa814a0ab647744233d5d37b1f1542a9f8b513fdd62a346f6` |

## Why this is not a verified bug

The v2 result explicitly records that zero is a supported component limit. It says the positivity rule does not apply and does not claim that the model is defective.

## Regression action

Keep this as a regression proving the detector suppresses or labels the non-defect correctly.

## Evidence basis

The v2 report's own verdict/proof explicitly declines a defect claim.

## Original claim

The positivity rule does **not** apply: this component documents zero as a meaningful limit, so a missing-bound claim would contradict its contract. It does **not** claim that anything is wrong — this records a rule that was considered and correctly declined, with the contract that declined it.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
