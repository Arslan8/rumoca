# FINDING-01787: The alleged divisor is the mathematical constant pi

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | immutable-pi |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Inverter |
| Target | aimc.pi |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-01787-imc-inverter-aimc-pi.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 5f719e7907c3c8a0adc9755692619ee56c630c28067ad817b5f929b8416739cc |

## Why this is a false positive

This declaration is protected constant Real pi=Modelica.Constants.pi. It is immutable and nonzero, so the proposed zero witness is unreachable. The detector lost constant-role information while following derived parameter expressions.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo:117`. Role: `constant`; binding: `(2 * asin(1.0))`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo — source snapshot](../evidence/sources/9baf5b1d5152b001-PartialBasicInductionMachine.mo)

```modelica
115: protected
116:   final parameter SI.Impedance ZsRef = 1 "Reference phase impedance based on nominal voltage 100 V and nominal current 100 A; per phase";
117:   constant Real pi = Modelica.Constants.pi;
118:   replaceable
119:     Machines.Interfaces.InductionMachines.PartialThermalPortInductionMachines internalThermalPort(final m=m)
120:     annotation (Placement(transformation(extent={{-4,-84},{4,-76}})));
```

[Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo — source snapshot](../evidence/sources/9baf5b1d5152b001-PartialBasicInductionMachine.mo)

```modelica
1: within Modelica.Electrical.Machines.Interfaces;
2: partial model PartialBasicInductionMachine
3:   "Partial model for induction machine"
4:   final parameter Integer m=3 "Number of phases" annotation(Evaluate=true);
5:   parameter Integer p(min=1, start=2) "Number of pole pairs (Integer)";
6:   parameter SI.Frequency fsNominal(start=50)
```

[Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo — source snapshot](../evidence/sources/9baf5b1d5152b001-PartialBasicInductionMachine.mo)

```modelica
112:         extent={{-10,-10},{10,10}},
113:         rotation=270,
114:         origin={-30,-80})));
115: protected
116:   final parameter SI.Impedance ZsRef = 1 "Reference phase impedance based on nominal voltage 100 V and nominal current 100 A; per phase";
117:   constant Real pi = Modelica.Constants.pi;
118:   replaceable
119:     Machines.Interfaces.InductionMachines.PartialThermalPortInductionMachines internalThermalPort(final m=m)
120:     annotation (Placement(transformation(extent={{-4,-84},{4,-76}})));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8e3358d86efa2aa5.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/immutable-pi.md) · [Index](../README.md)
