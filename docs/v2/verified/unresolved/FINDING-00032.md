# FINDING-00032: `tau0` in `MixingUnit`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Clocked.Examples.Systems.Utilities.ComponentsMixingUnit.MixingUnit |
| Target | `tau0` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Clocked/Examples/Systems/Utilities/ComponentsMixingUnit/MixingUnit.mo:26` |
| Original report | [FINDING-mixingunit-tau0-divzero-2.md](../../bugs/FINDING-mixingunit-tau0-divzero-2.md) |
| Original SHA-256 | `e710a7aa1cc31a82654f00a5f333be583218f64b7f7396eb5aae857314094972` |

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
model V2OMC_eead0f7256f0c3cf
  extends Modelica.Clocked.Examples.Systems.Utilities.ComponentsMixingUnit.MixingUnit(tau0=0);
end V2OMC_eead0f7256f0c3cf;
```

Relevant OMC diagnostic:

```text
messages = "Simulation execution failed for model: V2OMC_eead0f7256f0c3cf
LOG_ASSERT        | debug   | division by zero at time 0, (a=1.5476) / (b=0), where divisor b expression is: tau0
LOG_ASSERT        | info    | simulation terminated by an assertion at initialization
"Warning: The initial conditions are not fully specified. For more information set -d=initialization. In OMEdit Tools->Options->Simulation->Show additional information from the initialization process, in OMNotebook call setCommandLineOptions(\"-d=initialization\").
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
