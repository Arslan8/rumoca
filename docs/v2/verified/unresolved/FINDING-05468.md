# FINDING-05468: `vertical_tau` in `RoverPlant`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | RigidBody.Examples.RoverPlant |
| Target | `vertical_tau` |
| Declaration/site | `target/cmm/CMM-a642c381/RigidBody/Examples/RoverPlant.mo:58` |
| Original report | [FINDING-roverplant-vertical-tau-divzero.md](../../bugs/FINDING-roverplant-vertical-tau-divzero.md) |
| Original SHA-256 | `2ba7e5837bf1feb33c306629f6cdb746a97b87cb234a7f88998640b6a01fbecc` |

## What remains unresolved

The static denominator witness remains arithmetically valid, but independent OpenModelica did not establish the claimed differential failure. The paired execution outcome was `not-reproduced-by-omc`; a clean short run is not enough to prove the path can never execute later.

## Evidence needed

Use the generated wrapper as a regression, extend execution to the model's relevant experiment horizon, and obtain a clean baseline plus an attributed numerical failure before calling this a true positive.

## Evidence basis

Source-resolved Rumoca witness plus a conservative, non-confirming OpenModelica paired result.

## OpenModelica paired execution

- Outcome: `not-reproduced-by-omc`
- Unmodified baseline: `clean`
- Source-instantiated trigger: `clean`

Generated test program:

```modelica
model V2OMC_6b81890282edb6a1
  extends RigidBody.Examples.RoverPlant(vertical_tau=0);
end V2OMC_6b81890282edb6a1;
```

Relevant OMC diagnostic:

```text
messages = "LOG_SUCCESS       | info    | The initialization finished successfully without homotopy method.
LOG_STDOUT        | warning | The default linear solver fails, the fallback solver with total pivoting is started at time 0.000030. That might raise performance issues, for more information use -lv LOG_LS.
LOG_SUCCESS       | info    | The simulation finished successfully.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
