# FINDING-01414: Lme is an immutable nonzero model constant

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | fixed-permanent-magnet-scale |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Temperature |
| Target | dcpm.Lme |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-dcpm-temperature-dcpm-lme-zerolimit.md](../../v2/bugs/FINDING-dcpm-temperature-dcpm-lme-zerolimit.md) — reviewed as `FINDING-01414-dcpm-temperature-dcpm-lme.md`, which a later run renamed |
| Original SHA-256 | e3809f6c6d4e70e16e0d6eebd0183c014106687eb541c50fed2749f01fad9071 |

## Why this is a false positive

DC_PermanentMagnet declares protected constant SI.Inductance Lme=1. It is a fixed equivalence scale, not a user parameter, and cannot reach the claimed zero witness. The finding lost constant/final role information.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/DCMachines/DC_PermanentMagnet.mo:38`. Role: `constant`; binding: `1`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/DCMachines/DC_PermanentMagnet.mo — source snapshot](../evidence/sources/e46f1d6f469b100a-DC_PermanentMagnet.mo)

```modelica
36:         extent={{-10,-10},{10,10}})));
37: protected
38:   constant SI.Inductance Lme=1
39:     "Field excitation inductance";
40:   constant SI.Current IeNominal=1
41:     "Equivalent excitation current";
```

[Electrical/Machines/BasicMachines/DCMachines/DC_PermanentMagnet.mo — source snapshot](../evidence/sources/e46f1d6f469b100a-DC_PermanentMagnet.mo)

```modelica
35:         origin={0,-40},
36:         extent={{-10,-10},{10,10}})));
37: protected
38:   constant SI.Inductance Lme=1
39:     "Field excitation inductance";
40:   constant SI.Current IeNominal=1
41:     "Equivalent excitation current";
42: equation
43:   connect(eGround.p, ie.p) annotation (Line(points={{-10,-30},{-10,-30},{
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f6a744925526df08.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/fixed-permanent-magnet-scale.md) · [Index](../README.md)
