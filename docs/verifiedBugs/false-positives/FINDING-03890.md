# FINDING-03890: Zero ElastoGap stiffness is handled without division

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-elastogap-stiffness |
| Model | Modelica.Magnetic.FluxTubes.Examples.Utilities.TranslatoryArmatureAndStopper |
| Target | stopper_xMin.c |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-translatoryarmatureandstopper-stopper-xmin-c-zerolimit.md](../../v2/bugs/FINDING-translatoryarmatureandstopper-stopper-xmin-c-zerolimit.md) — reviewed as `FINDING-03890-translatoryarmatureandstopper-stopper-xmin-c.md`, which a later run renamed |
| Original SHA-256 | f3d87a8d9a7fe6e97c0ee74c76ba5a0de450d2b0c125b554465a5091db70100b |

## Why this is a false positive

c has min=0 and only forms f_ref=c*s_ref. The normalization divides by the separately positive s_ref, not by c; at c=0 the contact spring force is zero and the limiter keeps damping force within that zero spring force. The reported strict-positivity rule confuses a multiplier with a divisor.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Translational/Components/ElastoGap.mo:4`. Role: `parameter`; binding: `c`; effective min: `0`; effective max: `None`. 

[Mechanics/Translational/Components/ElastoGap.mo — source snapshot](../evidence/sources/3ca2ae3355d6bee9-ElastoGap.mo)

```modelica
2: model ElastoGap "1D translational spring damper combination with gap"
3:   extends Modelica.Mechanics.Translational.Interfaces.PartialCompliantWithRelativeStates;
4:   parameter SI.TranslationalSpringConstant c(final min=0, start=1)
5:     "Spring constant";
6:   parameter SI.TranslationalDampingConstant d(final min=0, start=1)
7:     "Damping constant";
```

[Mechanics/Translational/Components/ElastoGap.mo — source snapshot](../evidence/sources/3ca2ae3355d6bee9-ElastoGap.mo)

```modelica
2: model ElastoGap "1D translational spring damper combination with gap"
3:   extends Modelica.Mechanics.Translational.Interfaces.PartialCompliantWithRelativeStates;
4:   parameter SI.TranslationalSpringConstant c(final min=0, start=1)
5:     "Spring constant";
6:   parameter SI.TranslationalDampingConstant d(final min=0, start=1)
7:     "Damping constant";
8:   parameter SI.Position s_rel0=0 "Unstretched spring length";
9:   parameter SI.Force f_ref(min=0) = c*s_ref "Reference spring force at s_ref" annotation(Dialog(tab="Advanced"));
10:   parameter SI.Length s_ref(min=Modelica.Constants.eps) = 1 "Reference relative compression at which f_c = f_ref" annotation(Dialog(tab="Advanced"));
11:   parameter Real n(final min=1) = 1
12:     "Exponent of spring force ( f_c = -f_ref*|(s_rel-s_rel0)/s_ref|^n )";
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

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/be0cb9eabb9cc64c.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `stopper_xMin.c=0` | clean |

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-elastogap-stiffness.md) · [Index](../README.md)
