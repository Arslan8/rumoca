# FINDING-00776: `Nand.TN2.RDS` in `NandGate`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Analog.Examples.NandGate |
| Target | `Nand.TN2.RDS` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Semiconductors/NMOS.mo:42` |
| Original report | [FINDING-nandgate-nand-tn2-rds-divzero.md](../../bugs/FINDING-nandgate-nand-tn2-rds-divzero.md) |
| Original SHA-256 | `6fd8cd18b6e027daafd45fb6fae19359e362f01ef67f202fcac74f59c8aa6084` |

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
model V2OMC_cdc38b90487070bd
  extends Modelica.Electrical.Analog.Examples.NandGate(Nand.TN2.RDS=0);
end V2OMC_cdc38b90487070bd;
```

Relevant OMC diagnostic:

```text
messages = "LOG_SUCCESS       | info    | The initialization finished successfully without homotopy method.
LOG_STDOUT        | info    | Chattering detected around time 1.10000000011e-09..5.0010000005e-07 (100 state events in a row with a total time delta less than the step size 0.01). This can be a performance bottleneck. Use -lv LOG_EVENTS for more information. The zero-crossing was: time >= /*Real*/(pre(VIN1.signalSource.count) + 1) * VIN1.signalSource.period + VIN1.signalSource.startTime
LOG_SUCCESS       | info    | The simulation finished successfully.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
