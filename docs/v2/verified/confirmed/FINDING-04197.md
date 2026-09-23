# FINDING-04197: `r_mFe.l` in `SaturatedInductor`

| Field | Value |
|---|---|
| Verdict | confirmed |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.SaturatedInductor |
| Target | `r_mFe.l` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/Shapes/FixedShape/Cuboid.mo:18` |
| Original report | [FINDING-saturatedinductor-r-mfe-l-divzero.md](../../bugs/FINDING-saturatedinductor-r-mfe-l-divzero.md) |
| Original SHA-256 | `217cb46c3f5803ac3a84570f0f49bb281a1cfdcbed224cbb1ee4a4055a9101d7` |

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
model V2OMC_1fda626557ad0b00
  extends Modelica.Magnetic.FluxTubes.Examples.BasicExamples.SaturatedInductor(r_mFe.l=0);
end V2OMC_1fda626557ad0b00;
```

Relevant OMC diagnostic:

```text
LOG_ASSERT        | debug   | division leads to inf or nan at time 1.25e-06, (a=-nan) / (b=600), where divisor b is: coil.N
LOG_ASSERT        | debug   | division leads to inf or nan at time 3.125e-07, (a=-nan) / (b=600), where divisor b is: coil.N
LOG_ASSERT        | debug   | division leads to inf or nan at time 7.8125e-08, (a=-nan) / (b=600), where divisor b is: coil.N
LOG_ASSERT        | debug   | division leads to inf or nan at time 1.95313e-08, (a=-nan) / (b=600), where divisor b is: coil.N
LOG_ASSERT        | debug   | division leads to inf or nan at time 4.88281e-09, (a=-nan) / (b=600), where divisor b is: coil.N
LOG_ASSERT        | debug   | division leads to inf or nan at time 1.2207e-09, (a=-nan) / (b=600), where divisor b is: coil.N
LOG_ASSERT        | debug   | division leads to inf or nan at time 3.05176e-10, (a=-nan) / (b=600), where divisor b is: coil.N
LOG_ASSERT        | debug   | division leads to inf or nan at time 7.62939e-11, (a=-nan) / (b=600), where divisor b is: coil.N
LOG_ASSERT        | debug   | division leads to inf or nan at time 1.90735e-11, (a=-nan) / (b=600), where divisor b is: coil.N
LOG_STDOUT        | warning | A Modelica assert prevents the integrator to continue. For more information use -lv LOG_SOLVER
LOG_ASSERT        | debug   | division leads to inf or nan at time 0, (a=-nan) / (b=600), where divisor b is: coil.N
LOG_STDOUT        | info    | model terminate | Simulation terminated by an assert at time: 0
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
