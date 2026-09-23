# FINDING-01260: `Tr.Phie` in `Transistor`

| Field | Value |
|---|---|
| Verdict | confirmed |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Analog.Examples.Utilities.Transistor |
| Target | `Tr.Phie` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Semiconductors/NPN.mo:82` |
| Original report | [FINDING-transistor-tr-phie-divzero.md](../../bugs/FINDING-transistor-tr-phie-divzero.md) |
| Original SHA-256 | `c95742e2f60b2390589a23a8be2dc3801460c931d53d55f58025d7a75820bad2` |

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
model V2OMC_616387f73062b788
  extends Modelica.Electrical.Analog.Examples.Utilities.Transistor(Tr.Phie=0);
end V2OMC_616387f73062b788;
```

Relevant OMC diagnostic:

```text
LOG_ASSERT        | debug   | t_616387f73062b788_functions.c:119: Invalid root: (-nan)^(-0.4)
LOG_ASSERT        | debug   | t_616387f73062b788_functions.c:119: Invalid root: (-nan)^(-0.4)
LOG_ASSERT        | debug   | t_616387f73062b788_functions.c:119: Invalid root: (-nan)^(-0.4)
LOG_ASSERT        | debug   | t_616387f73062b788_functions.c:119: Invalid root: (-nan)^(-0.4)
LOG_ASSERT        | debug   | t_616387f73062b788_functions.c:119: Invalid root: (-nan)^(-0.4)
LOG_ASSERT        | debug   | t_616387f73062b788_functions.c:119: Invalid root: (-nan)^(-0.4)
LOG_ASSERT        | debug   | t_616387f73062b788_functions.c:119: Invalid root: (-nan)^(-0.4)
LOG_ASSERT        | debug   | t_616387f73062b788_functions.c:119: Invalid root: (-nan)^(-0.4)
LOG_STDOUT        | warning | A Modelica assert prevents the integrator to continue. For more information use -lv LOG_SOLVER
LOG_ASSERT        | debug   | t_616387f73062b788_functions.c:119: Invalid root: (-nan)^(-0.4)
LOG_ASSERT        | debug   | t_616387f73062b788_functions.c:119: Invalid root: (-nan)^(-0.4)
"Warning: The initial conditions are not fully specified. For more information set -d=initialization. In OMEdit Tools->Options->Simulation->Show additional information from the initialization process, in OMNotebook call setCommandLineOptions(\"-d=initialization\").
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
