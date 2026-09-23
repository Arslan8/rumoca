# FINDING-05471: `mass` in `QuadrotorSIL`

| Field | Value |
|---|---|
| Verdict | confirmed |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | RigidBody.Examples.QuadrotorSIL |
| Target | `mass` |
| Declaration/site | `target/cmm/CMM-a642c381/RigidBody/package.mo:56` |
| Original report | [FINDING-quadrotorsil-mass-divzero.md](../../bugs/FINDING-quadrotorsil-mass-divzero.md) |
| Original SHA-256 | `78e24fa52a4997b077c57e70ab7c224261d198217765799add6b609e0a50dc7f` |

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
model V2OMC_9c93d17a7d0f947b
  extends RigidBody.Examples.QuadrotorSIL(mass=0);
end V2OMC_9c93d17a7d0f947b;
```

Relevant OMC diagnostic:

```text
messages = "Simulation execution failed for model: V2OMC_9c93d17a7d0f947b
LOG_SUCCESS       | info    | The initialization finished successfully without homotopy method.
LOG_ASSERT        | warning | The following assertion has been violated at time 0.000000
LOG_ASSERT        | debug   | Model error: Argument of sqrt(v_b[1] ^ 2.0 + v_b[2] ^ 2.0 + v_b[3] ^ 2.0 + 1e-12) was nan should be >= 0
LOG_ASSERT        | info    | The following assertion has been violated at time 0.000000
LOG_ASSERT        | info    | The following assertion has been violated at time 0.000000
LOG_ASSERT        | info    | The following assertion has been violated at time 0.000000
LOG_ASSERT        | info    | The following assertion has been violated at time 0.000000
LOG_STDOUT        | warning | The default linear solver fails, the fallback solver with total pivoting is started at time 0.000000. That might raise performance issues, for more information use -lv LOG_LS.
LOG_ASSERT        | info    | The following assertion has been violated at time 0.000000
LOG_ASSERT        | error   | No event found, but assert was triggered. Throwing now!
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
