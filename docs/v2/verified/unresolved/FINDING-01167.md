# FINDING-01167: `simpleTriac.thyristor1.IGT` in `SimpleTriacCircuit`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-zero-unresolved` |
| Original tier | Candidate |
| Sanitizer result | `divisor-zero-unresolved` |
| Model | Modelica.Electrical.Analog.Examples.SimpleTriacCircuit |
| Target | `simpleTriac.thyristor1.IGT` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Semiconductors/Thyristor.mo:51` |
| Original report | [FINDING-simpletriaccircuit-simpletriac-thyristor1-igt-divunresolved.md](../../bugs/FINDING-simpletriaccircuit-simpletriac-thyristor1-igt-divunresolved.md) |
| Original SHA-256 | `fb6de919a9ad0a670e85e97fd30d076046084f0b1efa895dd100f347a1ce43b0` |

## What remains unresolved

The denominator has an arithmetic zero witness, but the current IR cannot decide whether the division executes on that path.

## Evidence needed

Resolve the path/aggregate value and obtain a clean baseline before assigning blame.

## Evidence basis

The v2 analysis explicitly reports UNKNOWN or lacks independent baseline evidence.

## Original claim

An assignment drives the denominator to zero, but whether the division is evaluated there could not be decided from the artifact. It does **not** claim that the model is wrong — this is **unresolved**, not confirmed, and is reported so it is not silently dropped.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
