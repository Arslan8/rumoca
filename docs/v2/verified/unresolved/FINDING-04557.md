# FINDING-04557: `body2.I` in `PlanarFourbar`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `physical-inertia-tensor-undecided` |
| Original tier | Candidate |
| Sanitizer result | `physical-inertia-tensor-undecided` |
| Model | Modelica.Mechanics.MultiBody.Examples.Loops.PlanarFourbar |
| Target | `body2.I` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Mechanics/MultiBody/Parts/BodyBox.mo:111` |
| Original report | [FINDING-planarfourbar-body2-i-tensorunknown.md](../../bugs/FINDING-planarfourbar-body2-i-tensorunknown.md) |
| Original SHA-256 | `daf19ef10be665046d384902976b9fa4757f34c5ded752148b90b56d4d56de40` |

## What remains unresolved

The aggregate inertia tensor cannot be assembled from values currently available to the analysis. Neither validity nor invalidity is proven.

## Evidence needed

Resolve the path/aggregate value and obtain a clean baseline before assigning blame.

## Evidence basis

The v2 analysis explicitly reports UNKNOWN or lacks independent baseline evidence.

## Original claim

This component's inertia tensor could not be assembled from values this analysis can resolve, so **neither its validity nor its invalidity is claimed**. It does **not** claim that anything is wrong. It is recorded because the six scalar declarations are excluded from the positivity rule either way, and a silent exclusion is indistinguishable from a missed defect.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
