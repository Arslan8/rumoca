# FINDING-04214: `r_i` in `ToroidalCoreQuadraticCrossSection`

| Field | Value |
|---|---|
| Verdict | confirmed |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.ToroidalCoreQuadraticCrossSection |
| Target | `r_i` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/Examples/BasicExamples/ToroidalCoreQuadraticCrossSection.mo:11` |
| Original report | [FINDING-toroidalcorequadraticcrosssection-r-i-divzero.md](../../bugs/FINDING-toroidalcorequadraticcrosssection-r-i-divzero.md) |
| Original SHA-256 | `8bbb0a7a8f0146382513c343ea069bc8b7e9c6d099ac28b1f94b960ba7136535` |

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
model V2OMC_6a527bcae94232d0
  extends Modelica.Magnetic.FluxTubes.Examples.BasicExamples.ToroidalCoreQuadraticCrossSection(r_i=-0.055);
end V2OMC_6a527bcae94232d0;
```

Relevant OMC diagnostic:

```text
messages = "Simulation execution failed for model: V2OMC_6a527bcae94232d0
LOG_ASSERT        | debug   | division by zero at time 0, (a=0.002) / (b=0), where divisor b expression is: 6.283185307179586 * (r_o + r_i)
LOG_ASSERT        | info    | simulation terminated by an assertion at initialization
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
