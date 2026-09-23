# FINDING-05462: `max_speed` in `RoverPlant`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | RigidBody.Examples.RoverPlant |
| Target | `max_speed` |
| Declaration/site | `target/cmm/CMM-a642c381/RigidBody/Examples/RoverPlant.mo:52` |
| Original report | [FINDING-roverplant-max-speed-divzero.md](../../bugs/FINDING-roverplant-max-speed-divzero.md) |
| Original SHA-256 | `e4715b59b481b291199c62af5eb1b12711c03db8f115d390bf140f7fe093f2b4` |

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
model V2OMC_1a37eeaf9fc467fc
  extends RigidBody.Examples.RoverPlant(max_speed=0);
end V2OMC_1a37eeaf9fc467fc;
```

Relevant OMC diagnostic:

```text
messages = "LOG_SUCCESS       | info    | The initialization finished successfully without homotopy method.
LOG_SUCCESS       | info    | The simulation finished successfully.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
