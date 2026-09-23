# FINDING-01088: `zDiode1.Vt` in `OvervoltageProtection`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-zero-unresolved` |
| Original tier | Candidate |
| Sanitizer result | `divisor-zero-unresolved` |
| Model | Modelica.Electrical.Analog.Examples.OvervoltageProtection |
| Target | `zDiode1.Vt` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Semiconductors/ZDiode.mo:18` |
| Original report | [FINDING-overvoltageprotection-zdiode1-vt-divunresolved-2.md](../../bugs/FINDING-overvoltageprotection-zdiode1-vt-divunresolved-2.md) |
| Original SHA-256 | `9fcefd4f60700a901ead202f9284d1d89bc77a7f225ef461a3985f2399d4f3e3` |

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
