# FINDING-02096: Zero/signed machine resistance is an ideal electrical limit

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | signed-machine-data-resistance |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start |
| Target | aimsData.Rs |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-ims-start-aimsdata-rs-unbounded.md](../../v2/bugs/FINDING-ims-start-aimsdata-rs-unbounded.md) — reviewed as `FINDING-02096-ims-start-aimsdata-rs.md`, which a later run renamed |
| Original SHA-256 | 0d9b2b55aaf45d07b07a777e9e08c2252126f9cae973ad33e1583c74cdd4a175 |

## Why this is a false positive

Rs is a stator resistance data field passed to resistor components. The underlying Basic.Resistor contract explicitly permits positive, zero and negative resistance and uses v=R_actual*i. A real machine normally has positive copper resistance, but the ideal zero-loss limit is mathematically supported; a blanket missing-bound finding is not a bug.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo:10`. Role: `parameter`; binding: `0.03`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo — source snapshot](../evidence/sources/8d312108fd6330eb-InductionMachineData.mo)

```modelica
8:   parameter Integer p(min=1) = 2 "Number of pole pairs (Integer)";
9:   parameter SI.Frequency fsNominal=50 "Nominal frequency";
10:   parameter SI.Resistance Rs=0.03
11:     "Stator resistance per phase at TRef"
12:     annotation (Dialog(tab="Nominal resistances and inductances"));
13:   parameter SI.Temperature TsRef=293.15
```

[Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo — source snapshot](../evidence/sources/8d312108fd6330eb-InductionMachineData.mo)

```modelica
8:   parameter Integer p(min=1) = 2 "Number of pole pairs (Integer)";
9:   parameter SI.Frequency fsNominal=50 "Nominal frequency";
10:   parameter SI.Resistance Rs=0.03
11:     "Stator resistance per phase at TRef"
12:     annotation (Dialog(tab="Nominal resistances and inductances"));
13:   parameter SI.Temperature TsRef=293.15
14:     "Reference temperature of stator resistance"
```

[Electrical/Analog/Basic/Resistor.mo — source snapshot](../evidence/sources/f3257fcb99588782-Resistor.mo)

```modelica
14: equation
15:   assert((1 + alpha*(T_heatPort - T_ref)) >= Modelica.Constants.eps,
16:     "Temperature outside scope of model!");
17:   R_actual = R*(1 + alpha*(T_heatPort - T_ref));
18:   v = R_actual*i;
19:   LossPower = v*i;
20:   annotation (
21:     Documentation(info="<html>
22: <p>The linear resistor connects the branch voltage <em>v</em> with the branch current <em>i</em> by <em>i*R = v</em>. The Resistance <em>R</em> is allowed to be positive, zero, or negative.</p>
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2804e4f64ad6a33e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/signed-machine-data-resistance.md) · [Index](../README.md)
