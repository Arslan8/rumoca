# FINDING-02993: `transformerData.L2sigma` in `AsymmetricalLoad`

| Field | Value |
|---|---|
| Verdict | advisory |
| Review group | `physical-intent-question` |
| Original tier | Candidate |
| Sanitizer result | `physical-intent-question` |
| Model | Modelica.Electrical.Machines.Examples.Transformers.AsymmetricalLoad |
| Target | `transformerData.L2sigma` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Utilities/TransformerData.mo:48` |
| Original report | [FINDING-asymmetricalload-transformerdata-l2sigma-intent.md](../../bugs/FINDING-asymmetricalload-transformerdata-l2sigma-intent.md) |
| Original SHA-256 | `a5b519ce4c4206911b218b192f34ebc781f55ce1f95534828250912896b4a091` |

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
