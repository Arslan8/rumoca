# FINDING-02605: SpacePhasor permits zero turns ratio then divides by it

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | space-phasor-turns-ratio |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL |
| Target | smr.spacePhasorS.turnsRatio |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-smr-dol-smr-spacephasors-turnsratio-divzero.md](../../v2/bugs/FINDING-smr-dol-smr-spacephasors-turnsratio-divzero.md) — reviewed as `FINDING-02605-smr-dol-smr-spacephasors-turnsratio.md`, which a later run renamed |
| Original SHA-256 | 9891967272f0a60213b9cdba055af7af2dcda228e4533ce159e9437a145f8532 |

## Verification and root cause

turnsRatio is an unconstrained parameter and the equation v/turnsRatio=plug_p.pin.v-plug_n.pin.v divides by it directly. Zero is admitted but undefined. This is a declaration/equation defect even when the enclosing machine example is blocked by unrelated runtime limitations.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/SpacePhasors/Components/SpacePhasor.mo:6`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/SpacePhasors/Components/SpacePhasor.mo — source snapshot](../evidence/sources/5f30ee9976dcc740-SpacePhasor.mo)

```modelica
4:   import Modelica.Constants.pi;
5:   constant Integer m=3 "Number of phases";
6:   parameter Real turnsRatio=1 "Turns ratio";
7:   SI.Voltage v[m] "Instantaneous phase voltages";
8:   SI.Current i[m] "Instantaneous phase currents";
9: protected
```

[Electrical/Machines/SpacePhasors/Components/SpacePhasor.mo — source snapshot](../evidence/sources/5f30ee9976dcc740-SpacePhasor.mo)

```modelica
2: model SpacePhasor
3:   "Physical transformation: three-phase <-> space phasors"
4:   import Modelica.Constants.pi;
5:   constant Integer m=3 "Number of phases";
6:   parameter Real turnsRatio=1 "Turns ratio";
7:   SI.Voltage v[m] "Instantaneous phase voltages";
8:   SI.Current i[m] "Instantaneous phase currents";
9: protected
10:   parameter Real InverseTransformation[m, 2]={{cos(-(k - 1)/m*2*pi),-sin(
11:       -(k - 1)/m*2*pi)} for k in 1:m};
12:   parameter Real TransformationMatrix[2, m]=2/m*{{cos(+(k - 1)/m*2*pi)
13:       for k in 1:m},{+sin(+(k - 1)/m*2*pi) for k in 1:m}};
14: public
15:   Modelica.Electrical.Polyphase.Interfaces.PositivePlug plug_p(final m=m)
16:     annotation (Placement(transformation(extent={{-110,90},{-90,110}})));
17:   Modelica.Electrical.Polyphase.Interfaces.NegativePlug plug_n(final m=m)
18:     annotation (Placement(transformation(extent={{-110,-110},{-90,-90}})));
19:   Modelica.Electrical.Analog.Interfaces.PositivePin zero annotation (
20:       Placement(transformation(extent={{90,-10},{110,10}})));
21:   Modelica.Electrical.Analog.Interfaces.NegativePin ground annotation (
22:       Placement(transformation(extent={{90,-110},{110,-90}})));
23:   Machines.Interfaces.SpacePhasor spacePhasor
24:     annotation (Placement(transformation(extent={{90,90},{110,110}})));
25: equation
26:   v/turnsRatio = plug_p.pin.v - plug_n.pin.v;
27:   i*turnsRatio = +plug_p.pin.i;
28:   i*turnsRatio = -plug_n.pin.i;
29:   m*zero.v = sum(v);
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/c3f17a08fd4d3c9d.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Proposed fix

Require and assert a nonzero turnsRatio before the transformation equation is evaluated. If negative ratios encode winding orientation, enforce abs(turnsRatio)>=small rather than positivity; if only magnitude is supported, document and enforce turnsRatio>0.

## Fix validation

Test nominal one, a valid non-unit ratio, the documented sign policy, zero, and near-zero values with a clear ratio-domain diagnostic.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/space-phasor-turns-ratio.md) · [Index](../README.md)
