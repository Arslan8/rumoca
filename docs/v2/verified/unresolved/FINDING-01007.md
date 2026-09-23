# FINDING-01007: `R2` in `FirstOrder`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.FirstOrder |
| Target | `R2` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/OpAmps/OpAmpCircuits/FirstOrder.mo:9` |
| Original report | [FINDING-firstorder-r2-divzero.md](../../bugs/FINDING-firstorder-r2-divzero.md) |
| Original SHA-256 | `bbcce37b353e987aacdef4f96148ee3e9463fd6831b871e738c01a74bc49045e` |

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
model V2OMC_1e37393cbe7227c7
  extends Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.FirstOrder(R2=0);
end V2OMC_1e37393cbe7227c7;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_1e37393cbe7227c7",
"[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/OpAmps/OpAmpCircuits/FirstOrder.mo:8:3-8:38:writable] Error: Parameter T has neither value nor start value, and is fixed during initialization (fixed=true).
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
