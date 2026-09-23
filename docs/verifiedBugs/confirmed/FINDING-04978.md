# FINDING-04978: Zero flux-tube length divides by zero

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | flux-length |
| Model | ModelicaTest.Magnetic.FluxTubes.Sources |
| Target | genericFluxTube1.l |
| Student classification | divisor-reachable-zero |
| Original report | [BUG-sources-genericfluxtube1-l.md](../../v2/bugs/BUG-sources-genericfluxtube1-l.md) — reviewed as `FINDING-04978-sources-genericfluxtube1-l.md`, which a later run renamed |
| Original SHA-256 | 26a31d5a09865c04cab9cc857cc67da0b248bdc8e6e5e84ca609ee0f13fc1968 |

## Verification and root cause

G_m = mu_0*mu_r*A/l is evaluated with l=0. The numerator is nonzero for the nominal positive area/permeability. Baseline passes; the l=0 source-modified and final-evaluated models explicitly report division by zero.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Shapes/FixedShape/GenericFluxTube.mo:8`. Role: `parameter`; binding: `0.01`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Shapes/FixedShape/GenericFluxTube.mo — source snapshot](../evidence/sources/c77fa8018b97298b-GenericFluxTube.mo)

```modelica
6:   extends Modelica.Magnetic.FluxTubes.Icons.Reluctance;
7: 
8:   parameter SI.Length l=0.01 "Length in direction of flux"
9:     annotation(Dialog(group="Fixed geometry", groupImage=
10:       "modelica://Modelica/Resources/Images/Magnetic/FluxTubes/Shapes/GenericFluxTube.png"));
11:   parameter SI.CrossSection area=0.0001 "Area of cross section"
```

[Magnetic/FluxTubes/Shapes/FixedShape/GenericFluxTube.mo — source snapshot](../evidence/sources/c77fa8018b97298b-GenericFluxTube.mo)

```modelica
1: within Modelica.Magnetic.FluxTubes.Shapes.FixedShape;
2: model GenericFluxTube
3:   "Flux tube with fixed cross-section and length; linear or non-linear material characteristics"
4: 
5:   extends BaseClasses.FixedShape;
6:   extends Modelica.Magnetic.FluxTubes.Icons.Reluctance;
7: 
8:   parameter SI.Length l=0.01 "Length in direction of flux"
9:     annotation(Dialog(group="Fixed geometry", groupImage=
10:       "modelica://Modelica/Resources/Images/Magnetic/FluxTubes/Shapes/GenericFluxTube.png"));
11:   parameter SI.CrossSection area=0.0001 "Area of cross section"
12:     annotation (Dialog(group="Fixed geometry"));
13: equation
14:   A = area;
15:   G_m = mu_0*mu_r*A/l;
16: 
17:   annotation (defaultComponentName="generic", Documentation(info="<html>
18: <p>
19: Please refer to the enclosing sub-package <a href=\"modelica://Modelica.Magnetic.FluxTubes.Shapes.FixedShape\">FixedShape</a> for a description of all elements of this package and to <a href=\"modelica://Modelica.Magnetic.FluxTubes.UsersGuide.Literature\">[Ro41]</a> for derivation and/or coefficients of the equation for permeance G_m.
20: </p>
21: </html>",
22:     revisions="<html>
23: <h5>Version 3.2.2, 2014-01-15 (Christian&nbsp;Kral)</h5>
24: <ul>
25: <li>Added GenericFluxTube</li>
```

[Magnetic/FluxTubes/BaseClasses/FixedShape.mo — source snapshot](../evidence/sources/e6a90b5ee04b025e-FixedShape.mo)

```modelica
28:   Real B_N "Absolute value of normalized B";
29: 
30: equation
31:   B_N = abs(B/material.B_myMax);
32:   mu_r = if nonLinearPermeability then
33:     1 + (material.mu_i - 1 + material.c_a*B_N)/(1 + material.c_b*B_N + B_N^material.n) else mu_rConst;
34: 
35:   R_m = 1/G_m;
36:   V_m = Phi*R_m;
37:   B = Phi/A;
38:   H = B/(mu_0*mu_r);
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8bb9ef7f1f1c7179.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `genericFluxTube1.l=0` | reported-failure |

Diagnostic: algebraic projection did not converge at event boundary: worst scaled residual row=34 target=genericFluxTube1.mu_r value=-inf ratio=inf norm=inf row_scale=1.000000e0 scaled_tolerance=1.000000e-10

[Independent OpenModelica wrappers and complete output](../evidence/omc-8bb9ef7f1f1c7179.json). Baseline: simulation succeeded.

- `genericFluxTube1.l=0` set before translation: LOG_ASSERT        | debug   | division by zero at time 0, (a=0.0001) / (b=0), where divisor b expression is: genericFluxTube1.l.
- Same value declared final, with final-parameter evaluation: LOG_ASSERT        | debug   | division by zero at time 0, (a=0.0001) / (b=0), where divisor b expression is: 0.0.

## Proposed fix

Validate strictly positive l and area at GenericFluxTube and guard reciprocal evaluation. Add meaningful positive parameter bounds for editor feedback, plus assertions for runtime enforcement. If zero geometry is intended, introduce a separate limiting magnetic element with consistent equations instead of evaluating 1/0.

## Fix validation

Add a nominal regression and the exact boundary witness below. Require a clear domain diagnostic (or a documented finite limiting model), never NaN/Inf or an unrelated solver error. Re-run both engines.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/flux-length.md) · [Index](../README.md)
