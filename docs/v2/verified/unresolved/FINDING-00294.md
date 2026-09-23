# FINDING-00294: `Transistor1.Tr.Tnom` in `DifferenceAmplifier`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-zero-unresolved` |
| Original tier | Candidate |
| Sanitizer result | `divisor-zero-unresolved` |
| Model | Modelica.Electrical.Analog.Examples.DifferenceAmplifier |
| Target | `Transistor1.Tr.Tnom` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Semiconductors/NPN.mo:75` |
| Original report | [FINDING-differenceamplifier-transistor1-tr-tnom-divunresolved-2.md](../../bugs/FINDING-differenceamplifier-transistor1-tr-tnom-divunresolved-2.md) |
| Original SHA-256 | `3af3cad73c0c830dfd2cde725ea8c4a5707535916bad042a073bb6bf44202182` |

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
