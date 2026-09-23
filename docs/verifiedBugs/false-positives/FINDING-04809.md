# FINDING-04809: LimPID already asserts that controller gain is nonzero

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | asserted-limpid-gain |
| Model | ModelicaTest.Blocks.Continuous_InitialState |
| Target | limPID.k |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-04809-continuous-initialstate-limpid-k.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | a4cd8baca71e95a65ec4183f7cbcf973fdd8b70be7e6a4f344d15a1aaecfb150 |

## Why this is a false positive

The anti-windup gain contains 1/(k*Ni), but the equation section explicitly asserts abs(k)>=Modelica.Constants.small with the diagnostic “Controller gain must be non-zero.” Ni also has a positive lower bound. The report overlooked the existing full domain enforcement; rejection at k=0 is intended behavior, not an unguarded missing-constraint bug.

## Source evidence

Compiler/source-resolved declaration: `Blocks/Continuous.mo:768`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Blocks/Continuous.mo — source snapshot](../evidence/sources/e0c05b204354b734-Continuous.mo)

```modelica
766:     parameter .Modelica.Blocks.Types.SimpleController controllerType=
767:            .Modelica.Blocks.Types.SimpleController.PID "Type of controller";
768:     parameter Real k = 1 "Gain of controller, must be non-zero";
769:     parameter SI.Time Ti(min=Modelica.Constants.small)=0.5
770:       "Time constant of Integrator block" annotation (Dialog(enable=
771:             controllerType == .Modelica.Blocks.Types.SimpleController.PI or
```

[Blocks/Continuous.mo — source snapshot](../evidence/sources/e0c05b204354b734-Continuous.mo)

```modelica
766:     parameter .Modelica.Blocks.Types.SimpleController controllerType=
767:            .Modelica.Blocks.Types.SimpleController.PID "Type of controller";
768:     parameter Real k = 1 "Gain of controller, must be non-zero";
769:     parameter SI.Time Ti(min=Modelica.Constants.small)=0.5
770:       "Time constant of Integrator block" annotation (Dialog(enable=
771:             controllerType == .Modelica.Blocks.Types.SimpleController.PI or
772:             controllerType == .Modelica.Blocks.Types.SimpleController.PID));
773:     parameter SI.Time Td(min=0)=0.1
774:       "Time constant of Derivative block" annotation (Dialog(enable=
775:             controllerType == .Modelica.Blocks.Types.SimpleController.PD or
776:             controllerType == .Modelica.Blocks.Types.SimpleController.PID));
777:     parameter Real yMax(start=1) "Upper limit of output";
778:     parameter Real yMin=-yMax "Lower limit of output";
779:     parameter Real wp(min=0) = 1
780:       "Set-point weight for Proportional block (0..1)";
781:     parameter Real wd(min=0) = 0 "Set-point weight for Derivative block (0..1)"
782:        annotation(Dialog(enable=controllerType==.Modelica.Blocks.Types.SimpleController.PD or
783:                                   controllerType==.Modelica.Blocks.Types.SimpleController.PID));
784:     parameter Real Ni(min=100*Modelica.Constants.eps) = 0.9
785:       "Ni*Ti is time constant of anti-windup compensation"
786:        annotation(Dialog(enable=controllerType==.Modelica.Blocks.Types.SimpleController.PI or
787:                                 controllerType==.Modelica.Blocks.Types.SimpleController.PID));
788:     parameter Real Nd(min=100*Modelica.Constants.eps) = 10
789:       "The higher Nd, the more ideal the derivative block"
```

[Blocks/Continuous.mo — source snapshot](../evidence/sources/e0c05b204354b734-Continuous.mo)

```modelica
846:     Modelica.Blocks.Math.Gain gainPID(k=k)
847:       annotation (Placement(transformation(extent={{20,-10},{40,10}})));
848:     Modelica.Blocks.Math.Add3 addPID
849:       annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
850:     Modelica.Blocks.Math.Add3 addI(k2=-1) if with_I
851:       annotation (Placement(transformation(extent={{-80,-60},{-60,-40}})));
852:     Modelica.Blocks.Math.Add addSat(k1=+1, k2=-1) if with_I annotation (Placement(
853:           transformation(
854:           origin={80,-50},
855:           extent={{-10,-10},{10,10}},
856:           rotation=270)));
857:     Modelica.Blocks.Math.Gain gainTrack(k=1/(k*Ni)) if with_I
858:       annotation (Placement(transformation(extent={{0,-80},{-20,-60}})));
859:     Modelica.Blocks.Nonlinear.Limiter limiter(
860:       uMax=yMax,
861:       uMin=yMin,
862:       strict=strict,
863:       homotopyType=homotopyType)
864:       annotation (Placement(transformation(extent={{70,-10},{90,10}})));
865:   protected
866:     parameter Boolean with_I = controllerType==SimpleController.PI or
867:                                controllerType==SimpleController.PID annotation(Evaluate=true, HideResult=true);
868:     parameter Boolean with_D = controllerType==SimpleController.PD or
869:                                controllerType==SimpleController.PID annotation(Evaluate=true, HideResult=true);
870:   public
871:     Modelica.Blocks.Sources.Constant Dzero(k=0) if not with_D
872:       annotation (Placement(transformation(extent={{-40,20},{-30,30}})));
873:     Modelica.Blocks.Sources.Constant Izero(k=0) if not with_I
874:       annotation (Placement(transformation(extent={{0,-55},{-10,-45}})));
875:     Modelica.Blocks.Sources.Constant FFzero(k=0) if not withFeedForward
876:       annotation (Placement(transformation(extent={{30,-35},{40,-25}})));
877:     Modelica.Blocks.Math.Add addFF(k1=1, k2=kFF)
878:       annotation (Placement(transformation(extent={{48,-6},{60,6}})));
879:   initial equation
880:     if initType==Init.InitialOutput then
881:       gainPID.y = y_start;
882:     end if;
883:   equation
884:     assert(abs(k) >= Modelica.Constants.small, "Controller gain must be non-zero.");
885:     if initType == Init.InitialOutput and (y_start < yMin or y_start > yMax) then
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/6eeeef65fb9ae772.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/asserted-limpid-gain.md) · [Index](../README.md)
