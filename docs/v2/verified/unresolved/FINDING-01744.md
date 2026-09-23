# FINDING-01744: `imc.fsNominal` in `IMC_DCBraking`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking |
| Target | `imc.fsNominal` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo:23` |
| Original report | [FINDING-imc-dcbraking-imc-fsnominal-divzero.md](../../bugs/FINDING-imc-dcbraking-imc-fsnominal-divzero.md) |
| Original SHA-256 | `6f9ae7ef20b50e45d11f83a76f9d6d0d6248aeccfa4f7d4813ebfc0ae47243d3` |

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
model V2OMC_b23c9b99845b42bf
  extends Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking(imc.fsNominal=0);
end V2OMC_b23c9b99845b42bf;
```

Relevant OMC diagnostic:

```text
LOG_ASSERT        | debug   | Solving linear system 185 failed at time=6.49247541248603e-10.
|                 | |       | For more information please use -lv LOG_LS.
LOG_STDOUT        | warning | Error solving linear system of equations (no. 185) at time 0.000000.
LOG_STDOUT        | warning | Solving linear system 185 fails at time 6.49239e-10. For more information use -lv LOG_LS.
LOG_ASSERT        | debug   | Solving linear system 185 failed at time=6.49239049912724e-10.
|                 | |       | For more information please use -lv LOG_LS.
LOG_STDOUT        | warning | A Modelica assert prevents the integrator to continue. For more information use -lv LOG_SOLVER
LOG_STDOUT        | warning | Error solving linear system of equations (no. 185) at time 0.000000.
LOG_STDOUT        | warning | Solving linear system 185 fails at time 6.49236e-10. For more information use -lv LOG_LS.
LOG_ASSERT        | debug   | Solving linear system 185 failed at time=6.49236219467432e-10.
|                 | |       | For more information please use -lv LOG_LS.
LOG_STDOUT        | info    | model terminate | Simulation terminated by an assert at time: 6.49236e-10
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
