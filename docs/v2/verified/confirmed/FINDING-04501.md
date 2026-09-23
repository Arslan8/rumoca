# FINDING-04501: `world.defaultWidthFraction` in `PointGravityWithPointMasses2`

| Field | Value |
|---|---|
| Verdict | confirmed |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses2 |
| Target | `world.defaultWidthFraction` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Mechanics/MultiBody/Parts/FixedTranslation.mo:44` |
| Original report | [FINDING-pointgravitywithpointmasses2-world-defaultwidthfraction-divzero-23.md](../../bugs/FINDING-pointgravitywithpointmasses2-world-defaultwidthfraction-divzero-23.md) |
| Original SHA-256 | `8a3da546511bb83f06d44fe9c4547e35ccfafda1f6f3e222c2dd71ba4caec8d9` |

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
model V2OMC_0a61b4e5f347df6b
  extends Modelica.Mechanics.MultiBody.Examples.Elementary.PointGravityWithPointMasses2(world.defaultWidthFraction=0);
end V2OMC_0a61b4e5f347df6b;
```

Relevant OMC diagnostic:

```text
messages = "Simulation execution failed for model: V2OMC_0a61b4e5f347df6b
LOG_ASSERT        | debug   | division by zero at time 0, (a=1) / (b=0), where divisor b expression is: world.defaultWidthFraction
LOG_ASSERT        | info    | simulation terminated by an assertion at initialization
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
