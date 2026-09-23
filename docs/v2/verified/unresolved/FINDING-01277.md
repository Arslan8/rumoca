# FINDING-01277: `fS` in `DcdcInverter`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.Machines.Examples.ControlledDCDrives.Utilities.DcdcInverter |
| Target | `fS` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Examples/ControlledDCDrives/Utilities/DcdcInverter.mo:5` |
| Original report | [FINDING-dcdcinverter-fs-divzero-2.md](../../bugs/FINDING-dcdcinverter-fs-divzero-2.md) |
| Original SHA-256 | `d704235b68c56352bb501625372848b92602224913aeb4bc9125789b3fc2fecd` |

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
model V2OMC_00fbcff7771b4116
  extends Modelica.Electrical.Machines.Examples.ControlledDCDrives.Utilities.DcdcInverter(fS=0);
end V2OMC_00fbcff7771b4116;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_00fbcff7771b4116",
"[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Examples/ControlledDCDrives/Utilities/DcdcInverter.mo:7:3-7:46:writable] Error: Parameter VMax has neither value nor start value, and is fixed during initialization (fixed=true).
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
