# FINDING-01171: `simpleTriac.thyristor1.Nbv` in `SimpleTriacCircuit`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-zero-unresolved` |
| Original tier | Candidate |
| Sanitizer result | `divisor-zero-unresolved` |
| Model | Modelica.Electrical.Analog.Examples.SimpleTriacCircuit |
| Target | `simpleTriac.thyristor1.Nbv` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Semiconductors/Thyristor.mo:57` |
| Original report | [FINDING-simpletriaccircuit-simpletriac-thyristor1-nbv-divunresolved.md](../../bugs/FINDING-simpletriaccircuit-simpletriac-thyristor1-nbv-divunresolved.md) |
| Original SHA-256 | `48e41aaef9f6e1d9f26ea9cb23117a60b7d095d18bca70b09c7aa2cf91bde46d` |

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
