# FINDING-05208: `firstOrder2.T` in `LimPID`

| Field | Value |
|---|---|
| Verdict | confirmed |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | ModelicaTest.Blocks.LimPID |
| Target | `firstOrder2.T` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Blocks/Continuous.mo:370` |
| Original report | [FINDING-limpid-firstorder2-t-divzero.md](../../bugs/FINDING-limpid-firstorder2-t-divzero.md) |
| Original SHA-256 | `eec0f855f1bb914376f37abc458f39bb6dd75bb8d9e61a10dcfdb79bbf8a1efe` |

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
model V2OMC_1ef0b7517a8a8742
  extends ModelicaTest.Blocks.LimPID(firstOrder2.T=0);
end V2OMC_1ef0b7517a8a8742;
```

Relevant OMC diagnostic:

```text
LOG_ASSERT        | debug   | division by zero at time 2.5e-06, (a=0) / (b=0), where divisor b expression is: firstOrder2.T
LOG_ASSERT        | debug   | division by zero at time 6.250000000000001e-07, (a=0) / (b=0), where divisor b expression is: firstOrder2.T
LOG_ASSERT        | debug   | division by zero at time 1.5625e-07, (a=0) / (b=0), where divisor b expression is: firstOrder2.T
LOG_ASSERT        | debug   | division by zero at time 3.90625e-08, (a=0) / (b=0), where divisor b expression is: firstOrder2.T
LOG_ASSERT        | debug   | division by zero at time 9.765625000000001e-09, (a=0) / (b=0), where divisor b expression is: firstOrder2.T
LOG_ASSERT        | debug   | division by zero at time 2.44140625e-09, (a=0) / (b=0), where divisor b expression is: firstOrder2.T
LOG_ASSERT        | debug   | division by zero at time 6.103515625e-10, (a=0) / (b=0), where divisor b expression is: firstOrder2.T
LOG_ASSERT        | debug   | division by zero at time 1.52587890625e-10, (a=0) / (b=0), where divisor b expression is: firstOrder2.T
LOG_ASSERT        | debug   | division by zero at time 3.814697265625e-11, (a=0) / (b=0), where divisor b expression is: firstOrder2.T
LOG_STDOUT        | warning | A Modelica assert prevents the integrator to continue. For more information use -lv LOG_SOLVER
LOG_ASSERT        | debug   | division by zero at time 0, (a=0) / (b=0), where divisor b expression is: firstOrder2.T
LOG_ASSERT        | debug   | division by zero at time 0, (a=0) / (b=0), where divisor b expression is: firstOrder2.T
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
