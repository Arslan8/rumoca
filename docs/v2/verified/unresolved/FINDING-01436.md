# FINDING-01436: `cooling.V_flowNominal` in `DCPM_Cooling`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling |
| Target | `cooling.V_flowNominal` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Thermal/FluidHeatFlow/BaseClasses/SimpleFriction.mo:29` |
| Original report | [FINDING-dcpm-cooling-cooling-v-flownominal-divzero.md](../../bugs/FINDING-dcpm-cooling-cooling-v-flownominal-divzero.md) |
| Original SHA-256 | `ead3d9a97dc843bafee31197c9e38b37339b149e76be9cc81284dbd45389ed03` |

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
model V2OMC_e884f2c9081ed77f
  extends Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling(cooling.V_flowNominal=0.10000000000000001);
end V2OMC_e884f2c9081ed77f;
```

Relevant OMC diagnostic:

```text
messages = "Simulation execution failed for model: V2OMC_e884f2c9081ed77f
LOG_ASSERT        | error   | [/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Thermal/FluidHeatFlow/BaseClasses/SimpleFriction.mo:25:3-26:64:writable]
|                 | |       | The following assertion has been violated during initialization at time 0.000000
LOG_ASSERT        | info    | simulation terminated by an assertion at initialization
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
