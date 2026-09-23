# FINDING-04775: Zero derivative time is explicitly handled

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | guarded-zero-derivative-time |
| Model | ModelicaTest.Blocks.Continuous |
| Target | pID.Td |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-04775-continuous-pid-td.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | bcba72e67cdf4216c09f6635aa7afcdf26e18f8a57596740d7ab3e14c39b0db2 |

## Why this is a false positive

Td has min=0. The derivative gain is Td/unitTime (Td is the numerator), while its filter time is max(Td/Nd, a strictly positive epsilon). Thus Td=0 disables the derivative contribution without producing a zero denominator. The report follows dependency reach rather than the complete guarded expression.

## Source evidence

Compiler/source-resolved declaration: `Blocks/Continuous.mo:608`. Role: `parameter`; binding: `0.1`; effective min: `0`; effective max: `None`. 

[Blocks/Continuous.mo — source snapshot](../evidence/sources/e0c05b204354b734-Continuous.mo)

```modelica
606:     parameter SI.Time Ti(min=Modelica.Constants.small, start=0.5)
607:       "Time Constant of Integrator";
608:     parameter SI.Time Td(min=0, start=0.1)
609:       "Time Constant of Derivative block";
610:     parameter Real Nd(min=Modelica.Constants.small) = 10
611:       "The higher Nd, the more ideal the derivative block";
```

[Blocks/Continuous.mo — source snapshot](../evidence/sources/e0c05b204354b734-Continuous.mo)

```modelica
605:     parameter Real k=1 "Gain";
606:     parameter SI.Time Ti(min=Modelica.Constants.small, start=0.5)
607:       "Time Constant of Integrator";
608:     parameter SI.Time Td(min=0, start=0.1)
609:       "Time Constant of Derivative block";
610:     parameter Real Nd(min=Modelica.Constants.small) = 10
611:       "The higher Nd, the more ideal the derivative block";
612:     parameter Init initType= Init.InitialState
613:       "Type of initialization (1: no init, 2: steady state, 3: initial state, 4: initial output)"
```

[Blocks/Continuous.mo — source snapshot](../evidence/sources/e0c05b204354b734-Continuous.mo)

```modelica
627:     Blocks.Math.Gain P(k=1) "Proportional part of PID controller"
628:       annotation (Placement(transformation(extent={{-60,60},{-20,100}})));
629:     Blocks.Continuous.Integrator I(k=unitTime/Ti, y_start=xi_start,
630:       initType=if initType==Init.SteadyState then
631:                   Init.SteadyState else
632:                if initType==Init.InitialState then
633:                   Init.InitialState else Init.NoInit)
634:       "Integral part of PID controller"
635:       annotation (Placement(transformation(extent={{-60,-20},{-20,20}})));
636:     Blocks.Continuous.Derivative D(k=Td/unitTime, T=max([Td/Nd, 100*Modelica.
637:           Constants.eps]), x_start=xd_start,
638:       initType=if initType==Init.SteadyState or
639:                   initType==Init.InitialOutput then Init.SteadyState else
640:                if initType==Init.InitialState then Init.InitialState else
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/45cdeda5c665c363.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/guarded-zero-derivative-time.md) · [Index](../README.md)
