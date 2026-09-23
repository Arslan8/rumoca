# FINDING-00297: `Transistor1.Tr.Phie` in `DifferenceAmplifier`

| Field | Value |
|---|---|
| Verdict | confirmed |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Analog.Examples.DifferenceAmplifier |
| Target | `Transistor1.Tr.Phie` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Semiconductors/NPN.mo:82` |
| Original report | [FINDING-differenceamplifier-transistor1-tr-phie-divzero.md](../../bugs/FINDING-differenceamplifier-transistor1-tr-phie-divzero.md) |
| Original SHA-256 | `b1cd842550802a96208e298d72f1380a54d851c91f2be239adbc24b177731d99` |

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
model V2OMC_9e12479cdc631bbc
  extends Modelica.Electrical.Analog.Examples.DifferenceAmplifier(Transistor1.Tr.Phie=0);
end V2OMC_9e12479cdc631bbc;
```

Relevant OMC diagnostic:

```text
LOG_ASSERT        | debug   | t_9e12479cdc631bbc_functions.c:119: Invalid root: (-nan)^(-0.4)
LOG_ASSERT        | debug   | t_9e12479cdc631bbc_functions.c:119: Invalid root: (-nan)^(-0.4)
LOG_ASSERT        | debug   | t_9e12479cdc631bbc_functions.c:119: Invalid root: (-nan)^(-0.4)
LOG_ASSERT        | debug   | t_9e12479cdc631bbc_functions.c:119: Invalid root: (-nan)^(-0.4)
LOG_ASSERT        | debug   | t_9e12479cdc631bbc_functions.c:119: Invalid root: (-nan)^(-0.4)
LOG_ASSERT        | debug   | t_9e12479cdc631bbc_functions.c:119: Invalid root: (-nan)^(-0.4)
LOG_ASSERT        | debug   | t_9e12479cdc631bbc_functions.c:119: Invalid root: (-nan)^(-0.4)
LOG_ASSERT        | debug   | t_9e12479cdc631bbc_functions.c:119: Invalid root: (-nan)^(-0.4)
LOG_ASSERT        | debug   | t_9e12479cdc631bbc_functions.c:119: Invalid root: (-nan)^(-0.4)
LOG_STDOUT        | warning | A Modelica assert prevents the integrator to continue. For more information use -lv LOG_SOLVER
LOG_ASSERT        | debug   | t_9e12479cdc631bbc_functions.c:119: Invalid root: (-nan)^(-0.4)
LOG_ASSERT        | debug   | t_9e12479cdc631bbc_functions.c:119: Invalid root: (-nan)^(-0.4)
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
