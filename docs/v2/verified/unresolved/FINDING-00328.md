# FINDING-00328: `H_PMOS.Tnom` in `HeatingMOSInverter`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-zero-unresolved` |
| Original tier | Candidate |
| Sanitizer result | `divisor-zero-unresolved` |
| Model | Modelica.Electrical.Analog.Examples.HeatingMOSInverter |
| Target | `H_PMOS.Tnom` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Semiconductors/PMOS.mo:52` |
| Original report | [FINDING-heatingmosinverter-h-pmos-tnom-divunresolved.md](../../bugs/FINDING-heatingmosinverter-h-pmos-tnom-divunresolved.md) |
| Original SHA-256 | `e6b6edabebae21a7787d7a0ced48d68203103f327b30686c1f7ea1e6ca34a157` |

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
