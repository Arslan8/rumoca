# FINDING-00821: `firstOrder2B.T` in `ControlCircuit`

| Field | Value |
|---|---|
| Verdict | confirmed |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit |
| Target | `firstOrder2B.T` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Blocks/Continuous.mo:370` |
| Original report | [FINDING-controlcircuit-firstorder2b-t-divzero.md](../../bugs/FINDING-controlcircuit-firstorder2b-t-divzero.md) |
| Original SHA-256 | `5dac627f27e40c7f69dbead3b7e95ece859c38e3c655968818be1b3302ea6425` |

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
model V2OMC_b8740c093cead888
  extends Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit(firstOrder2B.T=0);
end V2OMC_b8740c093cead888;
```

Relevant OMC diagnostic:

```text
SSERT        | debug   | division by zero at time 1.5625e-07, (a=0) / (b=0), where divisor b expression is: firstOrder2B.T
LOG_ASSERT        | debug   | division by zero at time 3.90625e-08, (a=0) / (b=0), where divisor b expression is: firstOrder2B.T
LOG_ASSERT        | debug   | division by zero at time 9.765625000000001e-09, (a=0) / (b=0), where divisor b expression is: firstOrder2B.T
LOG_ASSERT        | debug   | division by zero at time 2.44140625e-09, (a=0) / (b=0), where divisor b expression is: firstOrder2B.T
LOG_ASSERT        | debug   | division by zero at time 6.103515625e-10, (a=0) / (b=0), where divisor b expression is: firstOrder2B.T
LOG_ASSERT        | debug   | division by zero at time 1.52587890625e-10, (a=0) / (b=0), where divisor b expression is: firstOrder2B.T
LOG_ASSERT        | debug   | division by zero at time 3.814697265625e-11, (a=0) / (b=0), where divisor b expression is: firstOrder2B.T
LOG_STDOUT        | warning | A Modelica assert prevents the integrator to continue. For more information use -lv LOG_SOLVER
LOG_ASSERT        | debug   | division by zero at time 0, (a=0) / (b=0), where divisor b expression is: firstOrder2B.T
LOG_ASSERT        | debug   | division by zero at time 0, (a=0) / (b=0), where divisor b expression is: firstOrder2B.T
"Warning: There are nonlinear iteration variables with default zero start attribute found in NLSJac88. For more information set -d=initialization. In OMEdit Tools->Options->Simulation->Show additional information from the initialization process, in OMNotebook call setCommandLineOptions(\"-d=initialization\").
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
