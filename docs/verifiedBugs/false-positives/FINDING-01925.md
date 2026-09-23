# FINDING-01925: ZsRef is fixed to the nonzero value one

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | fixed-reference-impedance |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc |
| Target | aimc.ZsRef |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-ydarc-aimc-zsref-zerolimit.md](../../v2/bugs/FINDING-imc-ydarc-aimc-zsref-zerolimit.md) — reviewed as `FINDING-01925-imc-ydarc-aimc-zsref.md`, which a later run renamed |
| Original SHA-256 | d845274fc868f1d8bdddbbe8ee3a89acc5c48ba0e9419ba12272f3bff8b6262d |

## Why this is a false positive

The reported parameter is protected final parameter ZsRef=1, used as a dimensional reference. It cannot be modified to zero in a valid extension, so a zero-domain report against it is unreachable.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo:116`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo — source snapshot](../evidence/sources/9baf5b1d5152b001-PartialBasicInductionMachine.mo)

```modelica
114:         origin={-30,-80})));
115: protected
116:   final parameter SI.Impedance ZsRef = 1 "Reference phase impedance based on nominal voltage 100 V and nominal current 100 A; per phase";
117:   constant Real pi = Modelica.Constants.pi;
118:   replaceable
119:     Machines.Interfaces.InductionMachines.PartialThermalPortInductionMachines internalThermalPort(final m=m)
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

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/a03f73e52ba0cfd4.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/fixed-reference-impedance.md) · [Index](../README.md)
