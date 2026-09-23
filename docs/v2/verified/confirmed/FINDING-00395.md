# FINDING-00395: `T2.Tnom` in `HeatingPNP_NORGate`

| Field | Value |
|---|---|
| Verdict | confirmed |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Analog.Examples.HeatingPNP_NORGate |
| Target | `T2.Tnom` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Semiconductors/PNP.mo:71` |
| Original report | [FINDING-heatingpnp-norgate-t2-tnom-divzero.md](../../bugs/FINDING-heatingpnp-norgate-t2-tnom-divzero.md) |
| Original SHA-256 | `2e2dbfe86875b3d07a8b06d52105e46b6c50228271a88ccf7d2310bc37092a20` |

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
model V2OMC_816db10f9ac5c3fa
  extends Modelica.Electrical.Analog.Examples.HeatingPNP_NORGate(T2.Tnom=0);
end V2OMC_816db10f9ac5c3fa;
```

Relevant OMC diagnostic:

```text
LOG_ASSERT        | debug   | t_816db10f9ac5c3fa_functions.c:119: Invalid root: (inf)^(3)
LOG_ASSERT        | debug   | t_816db10f9ac5c3fa_functions.c:119: Invalid root: (inf)^(3)
LOG_ASSERT        | debug   | t_816db10f9ac5c3fa_functions.c:119: Invalid root: (inf)^(3)
LOG_ASSERT        | debug   | t_816db10f9ac5c3fa_functions.c:119: Invalid root: (inf)^(3)
LOG_ASSERT        | debug   | t_816db10f9ac5c3fa_functions.c:119: Invalid root: (inf)^(3)
LOG_ASSERT        | debug   | t_816db10f9ac5c3fa_functions.c:119: Invalid root: (inf)^(3)
LOG_ASSERT        | debug   | t_816db10f9ac5c3fa_functions.c:119: Invalid root: (inf)^(3)
LOG_ASSERT        | debug   | t_816db10f9ac5c3fa_functions.c:119: Invalid root: (inf)^(3)
LOG_ASSERT        | debug   | t_816db10f9ac5c3fa_functions.c:119: Invalid root: (inf)^(3)
LOG_ASSERT        | debug   | Solving non-linear system 59 failed at time=0.
|                 | |       | For more information please use -lv LOG_NLS.
LOG_ASSERT        | info    | simulation terminated by an assertion at initialization
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
