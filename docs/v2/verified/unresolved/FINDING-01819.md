# FINDING-01819: `aimcData.Rs` in `IMC_Initialize`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `machine-resistance-policy` |
| Original tier | Candidate |
| Sanitizer result | `physical-domain-unenforced` |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize |
| Target | `aimcData.Rs` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo:10` |
| Original report | [FINDING-imc-initialize-aimcdata-rs-unbounded.md](../../bugs/FINDING-imc-initialize-aimcdata-rs-unbounded.md) |
| Original SHA-256 | `55af35cd45c692e2f297fa8f1459d43a5c2d12b31639db8003d9fb44e301489c` |

## What remains unresolved

Zero is a supported ideal lossless winding, while negative machine copper resistance is ordinarily unphysical. The old blanket-positive and blanket-signed readings are both too broad; this needs a component-scoped nonnegative contract.

## Evidence needed

Bind this declaration to a machine-winding role and enforce R >= 0; then regenerate the finding.

## Evidence basis

Re-review prompted by the distinction between generic signed Basic.Resistor and machine winding data.

## Original claim

Nothing bounds this declaration at all, so it permits values the physical role forbids, including negative ones. It does **not** claim that any model actually sets such a value.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
