# FINDING-03092: `aimc.fsNominal` in `IMC_Transformer`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer |
| Target | `aimc.fsNominal` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/BasicMachines/InductionMachines/IM_SquirrelCage.mo:26` |
| Original report | [FINDING-imc-transformer-aimc-fsnominal-divzero-5.md](../../bugs/FINDING-imc-transformer-aimc-fsnominal-divzero-5.md) |
| Original SHA-256 | `6f9e56e22ac14cbf079e03d061d4cac003ba4a31cec84582498bd539319030ef` |

## What remains unresolved

The static denominator witness remains arithmetically valid, but independent OpenModelica did not establish the claimed differential failure. The paired execution outcome was `not-reproduced-by-omc`; a clean short run is not enough to prove the path can never execute later.

## Evidence needed

Use the generated wrapper as a regression, extend execution to the model's relevant experiment horizon, and obtain a clean baseline plus an attributed numerical failure before calling this a true positive.

## Evidence basis

Source-resolved Rumoca witness plus a conservative, non-confirming OpenModelica paired result.

## OpenModelica paired execution

- Outcome: `not-reproduced-by-omc`
- Unmodified baseline: `clean`
- Source-instantiated trigger: `clean`

Generated test program:

```modelica
model V2OMC_3b594977a8036362
  extends Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer(aimc.fsNominal=0);
end V2OMC_3b594977a8036362;
```

Relevant OMC diagnostic:

```text
messages = "LOG_SUCCESS       | info    | The initialization finished successfully without homotopy method.
LOG_SUCCESS       | info    | The simulation finished successfully.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
