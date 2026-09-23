# FINDING-04585: `L` in `GasForce2`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Mechanics.MultiBody.Examples.Loops.Utilities.GasForce2 |
| Target | `L` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Mechanics/MultiBody/Examples/Loops/Utilities/GasForce2.mo:26` |
| Original report | [FINDING-gasforce2-l-divzero.md](../../bugs/FINDING-gasforce2-l-divzero.md) |
| Original SHA-256 | `3999e3500dc89efc757b893489a33a9fda19c02edd83c85e9a37866be7ffa7ae` |

## What remains unresolved

The static denominator witness remains arithmetically valid, but independent OpenModelica did not establish the claimed differential failure. The paired execution outcome was `unresolved-baseline-fails`; a clean short run is not enough to prove the path can never execute later.

## Evidence needed

Use the generated wrapper as a regression, extend execution to the model's relevant experiment horizon, and obtain a clean baseline plus an attributed numerical failure before calling this a true positive.

## Evidence basis

Source-resolved Rumoca witness plus a conservative, non-confirming OpenModelica paired result.

## OpenModelica paired execution

- Outcome: `unresolved-baseline-fails`
- Unmodified baseline: `failed`
- Source-instantiated trigger: `failed`

Generated test program:

```modelica
model V2OMC_5866b60812225dca
  extends Modelica.Mechanics.MultiBody.Examples.Loops.Utilities.GasForce2(L=0);
end V2OMC_5866b60812225dca;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_5866b60812225dca",
"[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Mechanics/MultiBody/Examples/Loops/Utilities/GasForce2.mo:7:3-7:47:writable] Error: Parameter d has neither value nor start value, and is fixed during initialization (fixed=true).
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
