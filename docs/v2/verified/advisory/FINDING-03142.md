# FINDING-03142: `transformerData1.R2` in `Rectifier12pulse`

| Field | Value |
|---|---|
| Verdict | advisory |
| Review group | `physical-intent-question` |
| Original tier | Candidate |
| Sanitizer result | `physical-intent-question` |
| Model | Modelica.Electrical.Machines.Examples.Transformers.Rectifier12pulse |
| Target | `transformerData1.R2` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Utilities/TransformerData.mo:45` |
| Original report | [FINDING-rectifier12pulse-transformerdata1-r2-intent.md](../../bugs/FINDING-rectifier12pulse-transformerdata1-r2-intent.md) |
| Original SHA-256 | `12319a5a87c0f07891fee7c8e2185b64f7af83a0e02c2c427694535bceed2475` |

## Why this is an advisory

The analyzer observed a value or permissive declaration that is unusual for the quantity, but it has no component contract or user assumption establishing that the generic physical rule applies. It therefore asks the author about intent and deliberately makes no defect claim.

## How to resolve the question

Ask the author whether the value/domain is intended. If it is, add a component contract or user assumption; if it is not, add the appropriate declaration bound. Promote to a violation only after that intent evidence is available.

## Evidence basis

The finding carries premise_state=unknown: quantity/unit evidence raises the question, but does not establish component intent.

## Original claim

The value or the declaration is unusual for the **quantity** it declares, and nothing says what this component is — so this is a question for the author, not a claim about the model. It does **not** claim that the value is wrong. `SI.Resistance` is declared by passive resistors, by negative-impedance converters, by linearised incremental models and by fault-injection inputs alike; without a component contract the analyzer does not know the intent, and this advisory asks rather than asserts.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
