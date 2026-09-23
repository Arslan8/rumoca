# FINDING-01468: `PID.k` in `DCPM_CurrentControlled`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `divisor-zero-at-declared-values` |
| Original tier | Candidate |
| Sanitizer result | `divisor-zero-at-declared-values` |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_CurrentControlled |
| Target | `PID.k` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Blocks/Continuous.mo:857` |
| Original report | [FINDING-dcpm-currentcontrolled-pid-k-divbaseline.md](../../bugs/FINDING-dcpm-currentcontrolled-pid-k-divbaseline.md) |
| Original SHA-256 | `fe8491d8c776479ed09a5b09abc88e28d83f47244aec948c5f8010dcc11ef45b` |

## What remains unresolved

The static artifact says a denominator is zero at declared values, but these four cases lack an independent clean-baseline execution and may still involve conditional-component or path reconstruction. They remain unresolved rather than being called broken baselines.

## Evidence needed

Resolve the path/aggregate value and obtain a clean baseline before assigning blame.

## Evidence basis

The v2 analysis explicitly reports UNKNOWN or lacks independent baseline evidence.

## Original claim

The denominator is zero at the model's own declared values. It does **not** claim that any parameter can be blamed: nothing was changed, so this is a broken baseline rather than a latent hazard.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
