# FINDING-04137: Zero MultiBody visualization fraction divides geometry by zero

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | multibody-visual-scale |
| Model | Modelica.Mechanics.MultiBody.Examples.Elementary.SpringWithMass |
| Target | world.defaultFrameDiameterFraction |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-springwithmass-world-defaultframediameterfraction-divzero-2.md](../../v2/bugs/FINDING-springwithmass-world-defaultframediameterfraction-divzero-2.md) — reviewed as `FINDING-04137-springwithmass-world-defaultframediameterfraction.md`, which a later run renamed |
| Original SHA-256 | 574e1d0bfc12b91f882a4653777102e4d13d6332001ab2dd3059799337ad7273 |

## Verification and root cause

World exposes this parameter without a positive bound, while default body/frame dimensions divide a length by it. Zero is therefore admitted and makes animation geometry undefined. Although visual rather than physical dynamics, it is a real unguarded parameter-domain defect.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/MultiBody/package.mo:134`. Role: `parameter`; binding: `40`; effective min: `None`; effective max: `None`. 

[Mechanics/MultiBody/package.mo — source snapshot](../evidence/sources/552fe43071e197ff-package.mo)

```modelica
132:     "Default for arrow diameter (e.g., of forces, torques, sensors)"
133:     annotation (Dialog(tab="Defaults"));
134:   parameter Real defaultFrameDiameterFraction=40
135:     "Default for arrow diameter of a coordinate system as a fraction of axis length"
136:     annotation (Dialog(tab="Defaults"));
137:   parameter Real defaultSpecularCoefficient(min=0) = 0.7
```

[Mechanics/MultiBody/package.mo — source snapshot](../evidence/sources/552fe43071e197ff-package.mo)

```modelica
120:     "Default for the fixed length of a shape representing a force (e.g., damper)"
121:     annotation (Dialog(tab="Defaults"));
122:   parameter SI.Length defaultForceWidth=nominalLength/20
123:     "Default for the fixed width of a shape representing a force (e.g., spring, bushing)"
124:     annotation (Dialog(tab="Defaults"));
125:   parameter SI.Length defaultBodyDiameter=nominalLength/9
126:     "Default for diameter of sphere representing the center of mass of a body"
127:     annotation (Dialog(tab="Defaults"));
128:   parameter Real defaultWidthFraction=20
129:     "Default for shape width as a fraction of shape length (e.g., for Parts.FixedTranslation)"
130:     annotation (Dialog(tab="Defaults"));
131:   parameter SI.Length defaultArrowDiameter=nominalLength/40
132:     "Default for arrow diameter (e.g., of forces, torques, sensors)"
133:     annotation (Dialog(tab="Defaults"));
134:   parameter Real defaultFrameDiameterFraction=40
135:     "Default for arrow diameter of a coordinate system as a fraction of axis length"
136:     annotation (Dialog(tab="Defaults"));
```

[Mechanics/MultiBody/package.mo — source snapshot](../evidence/sources/552fe43071e197ff-package.mo)

```modelica
42:     "= true, if 3-dim. mechanical effects of Parts.Mounting1D/Rotor1D/BevelGear1D shall be taken into account";
43: 
44:   parameter SI.Distance axisLength=nominalLength/2
45:     "Length of world axes arrows"
46:     annotation (Dialog(tab="Animation", group="if animateWorld = true", enable=enableAnimation and animateWorld));
47:   parameter SI.Distance axisDiameter=axisLength/defaultFrameDiameterFraction
48:     "Diameter of world axes arrows"
49:     annotation (Dialog(tab="Animation", group="if animateWorld = true", enable=enableAnimation and animateWorld));
50:   parameter Boolean axisShowLabels=true "= true, if labels shall be shown"
51:     annotation (Dialog(tab="Animation", group="if animateWorld = true", enable=enableAnimation and animateWorld));
52:   input Types.Color axisColor_x=Modelica.Mechanics.MultiBody.Types.Defaults.FrameColor
53:     "Color of x-arrow"
54:     annotation (Dialog(colorSelector=true,tab="Animation", group="if animateWorld = true", enable=enableAnimation and animateWorld));
55:   input Types.Color axisColor_y=axisColor_x
56:     annotation (Dialog(colorSelector=true,tab="Animation", group="if animateWorld = true", enable=enableAnimation and animateWorld));
57:   input Types.Color axisColor_z=axisColor_x "Color of z-arrow"
58:     annotation (Dialog(colorSelector=true,tab="Animation", group="if animateWorld = true", enable=enableAnimation and animateWorld));
59: 
60:   parameter SI.Position gravityArrowTail[3]={0,0,0}
61:     "Position vector from origin of world frame to arrow tail, resolved in world frame"
62:     annotation (Dialog(tab="Animation", group=
63:           "if animateGravity = true and gravityType = UniformGravity",
64:           enable=enableAnimation and animateGravity and gravityType == GravityTypes.UniformGravity));
65:   parameter SI.Length gravityArrowLength=axisLength/2 "Length of gravity arrow"
66:     annotation (Dialog(tab="Animation", group=
67:           "if animateGravity = true and gravityType = UniformGravity",
68:           enable=enableAnimation and animateGravity and gravityType == GravityTypes.UniformGravity));
69:   parameter SI.Diameter gravityArrowDiameter=gravityArrowLength/
70:       defaultWidthFraction "Diameter of gravity arrow" annotation (Dialog(tab=
71:           "Animation", group=
72:           "if animateGravity = true and gravityType = UniformGravity",
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/ff82a44032b79121.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Proposed fix

Add a meaningful strictly-positive lower bound and explicit assertion for the fraction before dependent animation dimensions are evaluated. Keep animation=false paths lazy so unused visualization settings need not block physical simulation.

## Fix validation

Test animation enabled at defaults, zero and negative fractions with clear diagnostics, small positive values, and animation disabled with unused invalid visualization data according to the chosen lazy-evaluation contract.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/multibody-visual-scale.md) · [Index](../README.md)
