# FINDING-05262: `dqCurrentController.Rs` in `SMPM_VoltageSourceWithLosses`

| Field | Value |
|---|---|
| Verdict | confirmed |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses |
| Target | `dqCurrentController.Rs` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Utilities/DQCurrentController.mo:60` |
| Original report | [FINDING-smpm-voltagesourcewithlosses-dqcurrentcontroller-rs-divzero.md](../../bugs/FINDING-smpm-voltagesourcewithlosses-dqcurrentcontroller-rs-divzero.md) |
| Original SHA-256 | `22c27cc111222e2ea82617c53e704c6a9272070d7b0b86d6ae44d8799504522e` |

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
model V2OMC_07759e8333d24f5d
  extends ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses(dqCurrentController.Rs=0);
end V2OMC_07759e8333d24f5d;
```

Relevant OMC diagnostic:

```text
messages = "Simulation execution failed for model: V2OMC_07759e8333d24f5d
LOG_ASSERT        | debug   | division by zero at time 0, (a=0.001273239544735163) / (b=0), where divisor b expression is: dqCurrentController.Rs
LOG_ASSERT        | info    | simulation terminated by an assertion at initialization
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
