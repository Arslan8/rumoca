# FINDING-03076: Zero DC-machine inductance is an algebraic ideal limit

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-dc-machine-inductance |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive |
| Target | dcpm.la.L |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-thyristorbridge2mpulse-dc-drive-dcpm-la-l-zerolimit.md](../../v2/bugs/FINDING-thyristorbridge2mpulse-dc-drive-dcpm-la-l-zerolimit.md) — reviewed as `FINDING-03076-thyristorbridge2mpulse-dc-drive-dcpm-la-l.md`, which a later run renamed |
| Original SHA-256 | 18910ce497c47bbdac06fbe516e14fdc9914edc1e144acd2a7fd09cf96771be9 |

## Why this is a false positive

InductorDC uses v=if quasiStatic then 0 else L*der(i); it never divides by L. At L=0 the dynamic branch also imposes v=0. A missing positive bound is therefore not an intrinsic source defect, although a surrounding machine configuration may have incompatible state selections or constraints.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/Components/InductorDC.mo:5`. Role: `parameter`; binding: `dcpm.La`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/Components/InductorDC.mo — source snapshot](../evidence/sources/72ab8f755e24ff0e-InductorDC.mo)

```modelica
3:   "Ideal linear electrical inductor for electrical DC machines"
4:   extends Modelica.Electrical.Analog.Interfaces.OnePort;
5:   parameter SI.Inductance L(start=1) "Inductance";
6:   parameter Boolean quasiStatic(start=false)
7:     "No electrical transients if true" annotation (Evaluate=true);
8: equation
```

[Electrical/Machines/BasicMachines/Components/InductorDC.mo — source snapshot](../evidence/sources/72ab8f755e24ff0e-InductorDC.mo)

```modelica
2: model InductorDC
3:   "Ideal linear electrical inductor for electrical DC machines"
4:   extends Modelica.Electrical.Analog.Interfaces.OnePort;
5:   parameter SI.Inductance L(start=1) "Inductance";
6:   parameter Boolean quasiStatic(start=false)
7:     "No electrical transients if true" annotation (Evaluate=true);
8: equation
9:   v = if quasiStatic then 0 else L*der(i);
10:   annotation (defaultComponentName="inductor",
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/d8e62ee37d41ac80.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-dc-machine-inductance.md) · [Index](../README.md)
