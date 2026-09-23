# FINDING-04813: Zero derivative time is explicitly handled

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | guarded-zero-derivative-time |
| Model | ModelicaTest.Blocks.StrictLimiters |
| Target | PID1.Td |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-04813-strictlimiters-pid1-td.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 390444b196eb6fbf0968d67dacb3de75e9bc86c4e4367bc90c71c9de5d675ebe |

## Why this is a false positive

Td has min=0. The derivative gain is Td/unitTime (Td is the numerator), while its filter time is max(Td/Nd, a strictly positive epsilon). Thus Td=0 disables the derivative contribution without producing a zero denominator. The report follows dependency reach rather than the complete guarded expression.

## Source evidence

Compiler/source-resolved declaration: `Blocks/Continuous.mo:773`. Role: `parameter`; binding: `0.1`; effective min: `0`; effective max: `None`. 

[Blocks/Continuous.mo — source snapshot](../evidence/sources/e0c05b204354b734-Continuous.mo)

```modelica
771:             controllerType == .Modelica.Blocks.Types.SimpleController.PI or
772:             controllerType == .Modelica.Blocks.Types.SimpleController.PID));
773:     parameter SI.Time Td(min=0)=0.1
774:       "Time constant of Derivative block" annotation (Dialog(enable=
775:             controllerType == .Modelica.Blocks.Types.SimpleController.PD or
776:             controllerType == .Modelica.Blocks.Types.SimpleController.PID));
```

[Blocks/Continuous.mo — source snapshot](../evidence/sources/e0c05b204354b734-Continuous.mo)

```modelica
770:       "Time constant of Integrator block" annotation (Dialog(enable=
771:             controllerType == .Modelica.Blocks.Types.SimpleController.PI or
772:             controllerType == .Modelica.Blocks.Types.SimpleController.PID));
773:     parameter SI.Time Td(min=0)=0.1
774:       "Time constant of Derivative block" annotation (Dialog(enable=
775:             controllerType == .Modelica.Blocks.Types.SimpleController.PD or
776:             controllerType == .Modelica.Blocks.Types.SimpleController.PID));
777:     parameter Real yMax(start=1) "Upper limit of output";
778:     parameter Real yMin=-yMax "Lower limit of output";
```

[Blocks/Continuous.mo — source snapshot](../evidence/sources/e0c05b204354b734-Continuous.mo)

```modelica
831:     Modelica.Blocks.Continuous.Integrator I(
832:       k=unitTime/Ti,
833:       y_start=xi_start,
834:       initType=if initType == Init.SteadyState then Init.SteadyState else if
835:           initType == Init.InitialState
836:            then Init.InitialState else Init.NoInit) if with_I
837:       annotation (Placement(transformation(extent={{-50,-60},{-30,-40}})));
838:     Modelica.Blocks.Continuous.Derivative D(
839:       k=Td/unitTime,
840:       T=max([Td/Nd,1.e-14]),
841:       x_start=xd_start,
842:       initType=if initType == Init.SteadyState or initType == Init.InitialOutput
843:            then Init.SteadyState else if initType == Init.InitialState then
844:           Init.InitialState else Init.NoInit) if with_D
845:       annotation (Placement(transformation(extent={{-50,-10},{-30,10}})));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/da5e02db6db34fbd.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/guarded-zero-derivative-time.md) · [Index](../README.md)
