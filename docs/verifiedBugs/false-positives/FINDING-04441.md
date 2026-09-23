# FINDING-04441: Zero example damping is supported by ElastoGap

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-elastogap-example-damping |
| Model | Modelica.Mechanics.Translational.Examples.ElastoGap |
| Target | d |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-elastogap-d-intent.md](../../v2/bugs/FINDING-elastogap-d-intent.md) — reviewed as `FINDING-04441-elastogap-d.md`, which a later run renamed |
| Original SHA-256 | 3f296658638ed1441f18e96c03b0a2cffb5b85533f5b52a6f705408724afa819 |

## Why this is a false positive

The example passes d to ElastoGap, whose contact damping force is d*v_rel and is limited by the spring force. d=0 removes dissipation without division. The physical-domain heuristic is too strict for this example parameter.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Translational/Examples/ElastoGap.mo:45`. Role: `parameter`; binding: `1.5`; effective min: `None`; effective max: `None`. 

[Mechanics/Translational/Examples/ElastoGap.mo — source snapshot](../evidence/sources/87cd10aa20ef6e4b-ElastoGap.mo)

```modelica
43:     v(fixed=true))
44:     annotation (Placement(transformation(extent={{-10,-40},{10,-20}})));
45:   parameter SI.TranslationalDampingConstant d=1.5 "Damping constant";
46: equation
47: 
48:   connect(rod1.flange_b, fixed.flange) annotation (Line(
```

[Mechanics/Translational/Examples/ElastoGap.mo — source snapshot](../evidence/sources/87cd10aa20ef6e4b-ElastoGap.mo)

```modelica
40:     s(fixed=true, start=2),
41:     L=0,
42:     m=1,
43:     v(fixed=true))
44:     annotation (Placement(transformation(extent={{-10,-40},{10,-20}})));
45:   parameter SI.TranslationalDampingConstant d=1.5 "Damping constant";
46: equation
47: 
48:   connect(rod1.flange_b, fixed.flange) annotation (Line(
49:       points={{-20,0},{0,0}}, color={0,127,0}));
50:   connect(fixed.flange, rod2.flange_a) annotation (Line(
```

[Mechanics/Translational/Components/ElastoGap.mo — source snapshot](../evidence/sources/3ca2ae3355d6bee9-ElastoGap.mo)

```modelica
29:   // Modify contact force, so that it is only "pushing" and not
30:   // "pulling/sticking" and that it is continuous
31:   contact = s_rel < s_rel0;
32:   ratio = (s_rel - s_rel0)/s_ref;
33:   f_c = smooth(1, noEvent(if contact then -f_ref*abs(ratio)^n else 0));
34:   f_d2 = if contact then d*v_rel else 0;
35:   f_d = smooth(0, noEvent(if contact then min(max(f_d2, f_c), -f_c) else 0));
36:   f = f_c + f_d;
37:   lossPower = f_d*v_rel;
38:   annotation (
39:     Documentation(info="<html>
40: <p>
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/13c4a836eb58d87a.json). Baseline: **clean**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-elastogap-example-damping.md) · [Index](../README.md)
