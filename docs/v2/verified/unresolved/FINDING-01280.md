# FINDING-01280: `idealDcDc.Ti` in `DcdcInverter`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Machines.Examples.ControlledDCDrives.Utilities.DcdcInverter |
| Target | `idealDcDc.Ti` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Examples/ControlledDCDrives/Utilities/IdealDcDc.mo:31` |
| Original report | [FINDING-dcdcinverter-idealdcdc-ti-divzero.md](../../bugs/FINDING-dcdcinverter-idealdcdc-ti-divzero.md) |
| Original SHA-256 | `0d5881ce619aeb9727e48f4303afafa1cedea7989d63abcddff3c99772c5f124` |

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
model V2OMC_d8182fe6ee6b3ace
  extends Modelica.Electrical.Machines.Examples.ControlledDCDrives.Utilities.DcdcInverter(idealDcDc.Ti=0);
end V2OMC_d8182fe6ee6b3ace;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_d8182fe6ee6b3ace",
"[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Examples/ControlledDCDrives/Utilities/DcdcInverter.mo:4:3-4:50:writable] Error: Parameter fS has neither value nor start value, and is fixed during initialization (fixed=true).
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
