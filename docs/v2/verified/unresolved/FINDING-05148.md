# FINDING-05148: `mass2.C` in `TwoMasses`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `physical-policy-needs-proof` |
| Original tier | Candidate |
| Sanitizer result | `physical-domain-unenforced` |
| Model | Modelica.Thermal.HeatTransfer.Examples.TwoMasses |
| Target | `mass2.C` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Thermal/HeatTransfer/Components/HeatCapacitor.mo:3` |
| Original report | [FINDING-twomasses-mass2-c-unbounded.md](../../bugs/FINDING-twomasses-mass2-c-unbounded.md) |
| Original SHA-256 | `1992acc9956534d64e0cfae84d48bee3bfa1b72139970de7d81186fd18702eb6` |

## What remains unresolved

The quantity/unit heuristic identifies a possible physical-domain gap, but no unique component-specific source proof establishes the intended sign or zero contract.

## Evidence needed

Add or extract a component-scoped contract, then re-run PhysicalSan.

## Evidence basis

No unique prior source-semantic adjudication matched this v2 instance.

## Original claim

Nothing bounds this declaration at all, so it permits values the physical role forbids, including negative ones. It does **not** claim that any model actually sets such a value.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
