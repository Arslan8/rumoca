# FINDING-03378: `m` in `TransformerYD`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Polyphase.Examples.TransformerYD |
| Target | `m` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Polyphase/Examples/TransformerYD.mo:13` |
| Original report | [FINDING-transformeryd-m-divzero-4.md](../../bugs/FINDING-transformeryd-m-divzero-4.md) |
| Original SHA-256 | `b1f4a7e820237df808157234fa03632d8ef646350f460b0fbfc98be2f6f76f33` |

## What remains unresolved

The static denominator witness remains arithmetically valid, but independent OpenModelica did not establish the claimed differential failure. The paired execution outcome was `unresolved-trigger-failed-other`; a clean short run is not enough to prove the path can never execute later.

## Evidence needed

Use the generated wrapper as a regression, extend execution to the model's relevant experiment horizon, and obtain a clean baseline plus an attributed numerical failure before calling this a true positive.

## Evidence basis

Source-resolved Rumoca witness plus a conservative, non-confirming OpenModelica paired result.

## OpenModelica paired execution

- Outcome: `unresolved-trigger-failed-other`
- Unmodified baseline: `clean`
- Source-instantiated trigger: `failed`

Generated test program:

```modelica
model V2OMC_858bd81338a6403a
  extends Modelica.Electrical.Polyphase.Examples.TransformerYD(m=0);
end V2OMC_858bd81338a6403a;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_858bd81338a6403a",
"Error: Too few equations, under-determined system. The model has 11 equation(s) and 12 variable(s).
[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Polyphase/Basic/Delta.mo:13:3-13:40:writable] Error: {}[0] = {}[1] has size 1 but 0 variables ()
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
