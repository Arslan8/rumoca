# FINDING-00407: `HeatingDiode1.R` in `HeatingRectifier`

| Field | Value |
|---|---|
| Verdict | confirmed |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Analog.Examples.HeatingRectifier |
| Target | `HeatingDiode1.R` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Semiconductors/Diode.mo:28` |
| Original report | [FINDING-heatingrectifier-heatingdiode1-r-divzero.md](../../bugs/FINDING-heatingrectifier-heatingdiode1-r-divzero.md) |
| Original SHA-256 | `fcbcf8c4698c5bf51b16dd607d6dfeb7f78fac830e13b296697a7bf753cd1335` |

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
model V2OMC_5cd70d742c4497bb
  extends Modelica.Electrical.Analog.Examples.HeatingRectifier(HeatingDiode1.R=0);
end V2OMC_5cd70d742c4497bb;
```

Relevant OMC diagnostic:

```text
|                 | |       | For more information please use -lv LOG_NLS.
LOG_NLS           | error   | residualFunc36: Iteration variable `HeatingDiode1.T_heatPort` is inf or nan.
LOG_ASSERT        | debug   | residualFunc36 failed at time=0.
|                 | |       | For more information please use -lv LOG_NLS.
LOG_NLS           | error   | residualFunc36: Iteration variable `HeatingDiode1.T_heatPort` is inf or nan.
LOG_ASSERT        | debug   | residualFunc36 failed at time=0.
|                 | |       | For more information please use -lv LOG_NLS.
LOG_NLS           | error   | residualFunc36: Iteration variable `HeatingDiode1.T_heatPort` is inf or nan.
LOG_ASSERT        | debug   | residualFunc36 failed at time=0.
|                 | |       | For more information please use -lv LOG_NLS.
LOG_ASSERT        | debug   | Solving non-linear system 36 failed at time=0.
|                 | |       | For more information please use -lv LOG_NLS.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
