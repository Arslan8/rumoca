# FINDING-00326: `H_PMOS.RDS` in `HeatingMOSInverter`

| Field | Value |
|---|---|
| Verdict | confirmed |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Analog.Examples.HeatingMOSInverter |
| Target | `H_PMOS.RDS` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Semiconductors/PMOS.mo:42` |
| Original report | [FINDING-heatingmosinverter-h-pmos-rds-divzero.md](../../bugs/FINDING-heatingmosinverter-h-pmos-rds-divzero.md) |
| Original SHA-256 | `502fba3f4385d796f908f9286e7848fdbdd79898a28053f6e082319850db32d8` |

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
model V2OMC_9188607737989736
  extends Modelica.Electrical.Analog.Examples.HeatingMOSInverter(H_PMOS.RDS=0);
end V2OMC_9188607737989736;
```

Relevant OMC diagnostic:

```text
LOG_ASSERT        | debug   | t_9188607737989736_functions.c:61: Invalid root: (-6.78046)^(-1.5)
LOG_ASSERT        | debug   | t_9188607737989736_functions.c:61: Invalid root: (-6.78046)^(-1.5)
LOG_ASSERT        | debug   | t_9188607737989736_functions.c:61: Invalid root: (-6.78046)^(-1.5)
LOG_ASSERT        | debug   | t_9188607737989736_functions.c:71: Invalid root: (0)^(-1.5)
LOG_ASSERT        | debug   | t_9188607737989736_functions.c:61: Invalid root: (-6.78046)^(-1.5)
LOG_ASSERT        | debug   | t_9188607737989736_functions.c:61: Invalid root: (-6.78046)^(-1.5)
LOG_ASSERT        | debug   | t_9188607737989736_functions.c:61: Invalid root: (-6.78046)^(-1.5)
LOG_ASSERT        | debug   | t_9188607737989736_functions.c:61: Invalid root: (-6.78046)^(-1.5)
LOG_ASSERT        | debug   | Solving non-linear system 81 failed at time=9.765625e-09.
|                 | |       | For more information please use -lv LOG_NLS.
DASKR--  NONLINEAR SOLVER FAILED TO CONVERGE
LOG_STDOUT        | info    | model terminate | Integrator failed. | Simulation terminated at time 0
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
