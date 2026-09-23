# FINDING-01513: `dcdcInverter2.idealDcDc.deadTime.T` in `DCPM_Drive`

| Field | Value |
|---|---|
| Verdict | confirmed |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive |
| Target | `dcdcInverter2.idealDcDc.deadTime.T` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Blocks/Continuous.mo:370` |
| Original report | [FINDING-dcpm-drive-dcdcinverter2-idealdcdc-deadtime-t-divzero.md](../../bugs/FINDING-dcpm-drive-dcdcinverter2-idealdcdc-deadtime-t-divzero.md) |
| Original SHA-256 | `24d451e80c25c072b5ecfb612eb5996a8346641b649ce4b3e2cf415a17881ae0` |

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
model V2OMC_0d72ab0666f739b8
  extends Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive(dcdcInverter2.idealDcDc.deadTime.T=0);
end V2OMC_0d72ab0666f739b8;
```

Relevant OMC diagnostic:

```text
messages = "Simulation execution failed for model: V2OMC_0d72ab0666f739b8
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
