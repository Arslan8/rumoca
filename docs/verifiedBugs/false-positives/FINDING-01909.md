# FINDING-01909: The alleged zero divisor is constant m=3

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | fixed-phase-count |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer |
| Target | aimc.spacePhasorS.m |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-01909-imc-transformer-aimc-spacephasors-m.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | f6d228e6438493d5fda1e95769f7ab4e0ff7174766ba5defc0b84500eb09fbd9 |

## Why this is a false positive

SpacePhasor declares constant Integer m=3. It is not a parameter and cannot be overridden to zero; the transformation matrices therefore divide by the fixed value three. The finding is a variable-role error, not a reachable boundary.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/SpacePhasors/Components/SpacePhasor.mo:5`. Role: `constant`; binding: `3`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/SpacePhasors/Components/SpacePhasor.mo — source snapshot](../evidence/sources/5f30ee9976dcc740-SpacePhasor.mo)

```modelica
3:   "Physical transformation: three-phase <-> space phasors"
4:   import Modelica.Constants.pi;
5:   constant Integer m=3 "Number of phases";
6:   parameter Real turnsRatio=1 "Turns ratio";
7:   SI.Voltage v[m] "Instantaneous phase voltages";
8:   SI.Current i[m] "Instantaneous phase currents";
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
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/ea078e37b0773dc4.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/fixed-phase-count.md) · [Index](../README.md)
