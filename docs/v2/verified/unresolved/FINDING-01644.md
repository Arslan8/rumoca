# FINDING-01644: `dcpmData2.frictionParameters.wLinear` in `DCPM_withLosses`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-zero-unresolved` |
| Original tier | Candidate |
| Sanitizer result | `divisor-zero-unresolved` |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses |
| Target | `dcpmData2.frictionParameters.wLinear` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Losses/Friction.mo:15` |
| Original report | [FINDING-dcpm-withlosses-dcpmdata2-frictionparameters-wlinear-divunresolved.md](../../bugs/FINDING-dcpm-withlosses-dcpmdata2-frictionparameters-wlinear-divunresolved.md) |
| Original SHA-256 | `3eb1c2ba16758a3bd8691d49d9f503c413df61659bf038ce3a2c79d1cbcf9a70` |

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
