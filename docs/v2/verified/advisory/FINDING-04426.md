# FINDING-04426: `spring.c` in `HeatLosses`

| Field | Value |
|---|---|
| Verdict | advisory |
| Review group | `physical-intent-question` |
| Original tier | Candidate |
| Sanitizer result | `physical-intent-question` |
| Model | Modelica.Mechanics.MultiBody.Examples.Elementary.HeatLosses |
| Target | `spring.c` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Mechanics/MultiBody/Forces/Spring.mo:9` |
| Original report | [FINDING-heatlosses-spring-c-intent.md](../../bugs/FINDING-heatlosses-spring-c-intent.md) |
| Original SHA-256 | `b778d69af25b636143a4cf7a0a9c3b36756be8b0d9c04e70dd9dd6b48ea4b9c7` |

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
