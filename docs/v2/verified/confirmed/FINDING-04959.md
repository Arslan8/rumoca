# FINDING-04959: `valve.rho0` in `PumpAndValve`

| Field | Value |
|---|---|
| Verdict | confirmed |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Thermal.FluidHeatFlow.Examples.PumpAndValve |
| Target | `valve.rho0` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Thermal/FluidHeatFlow/Components/Valve.mo:45` |
| Original report | [FINDING-pumpandvalve-valve-rho0-divzero.md](../../bugs/FINDING-pumpandvalve-valve-rho0-divzero.md) |
| Original SHA-256 | `dd05d0a9952e8a513c4bdf813cd53219e9868312fcf1a4f9d5e860ba8fb2d2c6` |

## Verification and root cause

The exact reported witness was placed in a generated Modelica subclass before translation. The unmodified model executed cleanly, while OpenModelica rejected the trigger with a numerical failure such as division by zero, a non-finite result, or a singular system.

## Proposed fix

Constrain or assert the complete denominator away from zero before evaluating the division. If zero has a meaningful limit, implement an explicit algebraic branch; do not hide it with an epsilon.

## Fix validation

Retest nominal values, the exact reported witness, nearby valid boundaries, and any relational equality or conditional branch involved. Preserve the intended ideal/algebraic behavior of delegated components.

## Evidence basis

Rumoca supplied the source-resolved arithmetic witness; independent OpenModelica source translation and execution reproduced the attributed failure against a clean paired baseline.

## OpenModelica paired execution

- Outcome: `confirmed-by-omc`
- Unmodified baseline: `clean`
- Source-instantiated trigger: `failed`

Generated test program:

```modelica
model V2OMC_32e45f55d56c3d71
  extends Modelica.Thermal.FluidHeatFlow.Examples.PumpAndValve(valve.rho0=0);
end V2OMC_32e45f55d56c3d71;
```

Relevant OMC diagnostic:

```text
LOG_NLS           | error   | residualFunc34: Iteration variable `valve.V_flow` is inf or nan.
LOG_ASSERT        | debug   | residualFunc34 failed at time=0.
|                 | |       | For more information please use -lv LOG_NLS.
LOG_NLS           | error   | residualFunc34: Iteration variable `valve.V_flow` is inf or nan.
LOG_ASSERT        | debug   | residualFunc34 failed at time=0.
|                 | |       | For more information please use -lv LOG_NLS.
LOG_NLS           | error   | residualFunc34: Iteration variable `valve.V_flow` is inf or nan.
LOG_ASSERT        | debug   | residualFunc34 failed at time=0.
|                 | |       | For more information please use -lv LOG_NLS.
LOG_ASSERT        | debug   | Solving non-linear system 34 failed at time=0.
|                 | |       | For more information please use -lv LOG_NLS.
LOG_ASSERT        | info    | simulation terminated by an assertion at initialization
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
