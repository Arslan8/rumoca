# FINDING-01172: `simpleTriac.thyristor1.Roff` in `SimpleTriacCircuit`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-zero-unresolved` |
| Original tier | Candidate |
| Sanitizer result | `divisor-zero-unresolved` |
| Model | Modelica.Electrical.Analog.Examples.SimpleTriacCircuit |
| Target | `simpleTriac.thyristor1.Roff` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Semiconductors/Thyristor.mo:58` |
| Original report | [FINDING-simpletriaccircuit-simpletriac-thyristor1-roff-divunresolved-2.md](../../bugs/FINDING-simpletriaccircuit-simpletriac-thyristor1-roff-divunresolved-2.md) |
| Original SHA-256 | `320e0a248e00de6a950406297aff48f1ed484e2b7279ae13627cfe7cefde90ae` |

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
