# FINDING-00767: `Nand.TP1.RDS` in `NandGate`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Analog.Examples.NandGate |
| Target | `Nand.TP1.RDS` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Semiconductors/PMOS.mo:42` |
| Original report | [FINDING-nandgate-nand-tp1-rds-divzero.md](../../bugs/FINDING-nandgate-nand-tp1-rds-divzero.md) |
| Original SHA-256 | `2b9bb3723cecee5ed3057a781639b5e7b7ebcc72cce669328e2a17616254c40c` |

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
model V2OMC_f565101757032932
  extends Modelica.Electrical.Analog.Examples.NandGate(Nand.TP1.RDS=0);
end V2OMC_f565101757032932;
```

Relevant OMC diagnostic:

```text
messages = "Simulation execution failed for model: V2OMC_f565101757032932
LOG_SUCCESS       | info    | The initialization finished successfully without homotopy method.
DASKR--  ERROR TEST FAILED REPEATEDLY OR WITH ABS(H)=HMIN
LOG_STDOUT        | warning | DDASSL had repeated error test failures on the last attempted step.
LOG_STDOUT        | info    | model terminate | Integrator failed. | Simulation terminated at time 1.1e-09
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
