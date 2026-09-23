# FINDING-00244: `idealTransformer.n` in `CompareTransformers`

| Field | Value |
|---|---|
| Verdict | confirmed |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Analog.Examples.CompareTransformers |
| Target | `idealTransformer.n` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Ideal/IdealTransformer.mo:14` |
| Original report | [FINDING-comparetransformers-idealtransformer-n-divzero.md](../../bugs/FINDING-comparetransformers-idealtransformer-n-divzero.md) |
| Original SHA-256 | `2e2b487a6d171badbbcdad4e4096d0e9af340b2cea4b1df84b569d9ae59b7a31` |

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
model V2OMC_28b87bf3a682ed63
  extends Modelica.Electrical.Analog.Examples.CompareTransformers(idealTransformer.n=0);
end V2OMC_28b87bf3a682ed63;
```

Relevant OMC diagnostic:

```text
messages = "Simulation execution failed for model: V2OMC_28b87bf3a682ed63
LOG_STDOUT        | warning | The default linear solver fails, the fallback solver with total pivoting is started at time 0.000000. That might raise performance issues, for more information use -lv LOG_LS.
LOG_SUCCESS       | info    | The initialization finished successfully without homotopy method.
LOG_STDOUT        | warning | The default linear solver fails, the fallback solver with total pivoting is started at time 0.000000. That might raise performance issues, for more information use -lv LOG_LS.
LOG_STDOUT        | warning | The default linear solver fails, the fallback solver with total pivoting is started at time 0.000000. That might raise performance issues, for more information use -lv LOG_LS.
DASKR--  ITERATION MATRIX IS SINGULAR.
LOG_STDOUT        | warning | The matrix of partial derivatives is singular.
LOG_STDOUT        | info    | model terminate | Integrator failed. | Simulation terminated at time 9.2599e-09
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
