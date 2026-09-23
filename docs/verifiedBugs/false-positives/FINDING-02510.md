# FINDING-02510: Zero stator resistance is a supported ideal-loss limit

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | ideal-stator-resistance |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource |
| Target | smpm.Rs |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smpm-voltagesource-smpm-rs-unbounded.md](../../v2/bugs/FINDING-smpm-voltagesource-smpm-rs-unbounded.md) — reviewed as `FINDING-02510-smpm-voltagesource-smpm-rs.md`, which a later run renamed |
| Original SHA-256 | 5d3161f1884732570a8862083c8717f7f03945ea19b10795a2e717b7356b7b26 |

## Why this is a false positive

Rs is passed to Polyphase.Basic.Resistor, which delegates to the scalar resistor contract that explicitly allows positive, zero, or negative resistance. Zero removes copper loss; the source does not divide by Rs. A real machine-data recommendation is not a universal equation-domain requirement.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo:11`. Role: `parameter`; binding: `smpmData.Rs`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo — source snapshot](../evidence/sources/9baf5b1d5152b001-PartialBasicInductionMachine.mo)

```modelica
9:     "Operational temperature of stator resistance" annotation (Dialog(group=
10:          "Operational temperatures", enable=not useThermalPort));
11:   parameter SI.Resistance Rs(start=0.03*ZsRef)
12:     "Stator resistance per phase at TRef"
13:     annotation (Dialog(tab="Nominal resistances and inductances"));
14:   parameter SI.Temperature TsRef(start=293.15)
```

[Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo — source snapshot](../evidence/sources/9baf5b1d5152b001-PartialBasicInductionMachine.mo)

```modelica
8:   parameter SI.Temperature TsOperational(start=293.15)
9:     "Operational temperature of stator resistance" annotation (Dialog(group=
10:          "Operational temperatures", enable=not useThermalPort));
11:   parameter SI.Resistance Rs(start=0.03*ZsRef)
12:     "Stator resistance per phase at TRef"
13:     annotation (Dialog(tab="Nominal resistances and inductances"));
```

[Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo — source snapshot](../evidence/sources/9baf5b1d5152b001-PartialBasicInductionMachine.mo)

```modelica
68:   Modelica.Electrical.Polyphase.Interfaces.NegativePlug plug_sn(final m=m)
69:     "Negative stator plug" annotation (Placement(transformation(extent={{-70,
70:             90},{-50,110}})));
71:   Modelica.Electrical.Polyphase.Basic.Resistor rs(
72:     final m=m,
73:     final R=fill(Rs, m),
74:     final T_ref=fill(TsRef, m),
75:     final alpha=fill(Machines.Thermal.convertAlpha(alpha20s, TsRef), m),
76:     final useHeatPort=true,
77:     final T=fill(TsRef, m)) annotation (Placement(transformation(extent={{
78:             60,70},{40,90}})));
79:   Machines.BasicMachines.Components.Inductor lssigma(final L=fill(Lssigma, 2))
80:     annotation (Placement(transformation(
81:         extent={{-10,-10},{10,10}},
82:         rotation=270,
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

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/d529fc5d98897b6a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/ideal-stator-resistance.md) · [Index](../README.md)
