# FINDING-00013: `mixingUnit.c0` in `FilterOrder`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Clocked.Examples.Systems.Utilities.ComponentsMixingUnit.FilterOrder |
| Target | `mixingUnit.c0` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Clocked/Examples/Systems/Utilities/ComponentsMixingUnit/MixingUnit.mo:24` |
| Original report | [FINDING-filterorder-mixingunit-c0-divzero.md](../../bugs/FINDING-filterorder-mixingunit-c0-divzero.md) |
| Original SHA-256 | `42311c456de8a735bfe4a820ecd94f2d32ac015c888a12dfc2a6b1f7aff6e8a4` |

## What remains unresolved

The static denominator witness remains arithmetically valid, but independent OpenModelica did not establish the claimed differential failure. The paired execution outcome was `unresolved-baseline-fails`; a clean short run is not enough to prove the path can never execute later.

## Evidence needed

Use the generated wrapper as a regression, extend execution to the model's relevant experiment horizon, and obtain a clean baseline plus an attributed numerical failure before calling this a true positive.

## Evidence basis

Source-resolved Rumoca witness plus a conservative, non-confirming OpenModelica paired result.

## OpenModelica paired execution

- Outcome: `unresolved-baseline-fails`
- Unmodified baseline: `failed`
- Source-instantiated trigger: `failed`

Generated test program:

```modelica
model V2OMC_ff8ae6d9d56ebd00
  extends Modelica.Clocked.Examples.Systems.Utilities.ComponentsMixingUnit.FilterOrder(mixingUnit.c0=0);
end V2OMC_ff8ae6d9d56ebd00;
```

Relevant OMC diagnostic:

```text
messages = "Simulation execution failed for model: V2OMC_ff8ae6d9d56ebd00
LOG_ASSERT        | debug   | division by zero at time 0, (a=105000000000000) / (b=0), where divisor b expression is: mixingUnit.c0
LOG_ASSERT        | info    | simulation terminated by an assertion at initialization
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
