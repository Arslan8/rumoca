# FINDING-05465: `mass` in `RoverPlant`

| Field | Value |
|---|---|
| Verdict | confirmed |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | RigidBody.Examples.RoverPlant |
| Target | `mass` |
| Declaration/site | `target/cmm/CMM-a642c381/RigidBody/package.mo:56` |
| Original report | [FINDING-roverplant-mass-divzero.md](../../bugs/FINDING-roverplant-mass-divzero.md) |
| Original SHA-256 | `8dd435993ba06def15a3006a6ef5af46eb8767fb6bf0c6bea20999d0070361b0` |

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
model V2OMC_f5c80d65719e0d30
  extends RigidBody.Examples.RoverPlant(mass=0);
end V2OMC_f5c80d65719e0d30;
```

Relevant OMC diagnostic:

```text
messages = "Simulation execution failed for model: V2OMC_f5c80d65719e0d30
LOG_SUCCESS       | info    | The initialization finished successfully without homotopy method.
DASKR--  ITERATION MATRIX IS SINGULAR.
LOG_STDOUT        | warning | The matrix of partial derivatives is singular.
LOG_STDOUT        | info    | model terminate | Integrator failed. | Simulation terminated at time 0
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
