# FINDING-01738: `imcData.fsNominal` in `IMC_DCBraking`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking |
| Target | `imcData.fsNominal` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo:23` |
| Original report | [FINDING-imc-dcbraking-imcdata-fsnominal-divzero.md](../../bugs/FINDING-imc-dcbraking-imcdata-fsnominal-divzero.md) |
| Original SHA-256 | `732e0e4b3e24d236d5cfb11932a0d0463af26da5524d5a766e1539f24d2af176` |

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
model V2OMC_aa734ed3d063e8f2
  extends Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking(imcData.fsNominal=0);
end V2OMC_aa734ed3d063e8f2;
```

Relevant OMC diagnostic:

```text
messages = "Simulation execution failed for model: V2OMC_aa734ed3d063e8f2
LOG_ASSERT        | debug   | division by zero at time 0, (a=0.1017764061411688) / (b=0), where divisor b expression is: 6.283185307179586 * imcData.fsNominal
LOG_ASSERT        | info    | simulation terminated by an assertion at initialization
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
