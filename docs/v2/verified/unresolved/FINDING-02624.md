# FINDING-02624: `smpmData.Rs` in `SMPM_CurrentSource`

| Field | Value |
|---|---|
| Verdict | unresolved |
| Review group | `machine-resistance-policy` |
| Original tier | Candidate |
| Sanitizer result | `physical-domain-unenforced` |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_CurrentSource |
| Target | `smpmData.Rs` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo:10` |
| Original report | [FINDING-smpm-currentsource-smpmdata-rs-unbounded.md](../../bugs/FINDING-smpm-currentsource-smpmdata-rs-unbounded.md) |
| Original SHA-256 | `dd1ca82b44435bd6ac4cdd772fc43567ab33e572d86a8bee456dabb90ceb3790` |

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
