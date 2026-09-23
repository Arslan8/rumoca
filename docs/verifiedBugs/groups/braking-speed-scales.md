# Braking example fails to propagate positive speed-scale bounds

Group `braking-speed-scales` · 4 report instances · confirmed

The outer example declares w0 without a positive bound and forwards it to force/torque sources whose corresponding parameter has min=Modelica.Constants.eps and appears in reciprocal normalization. Thus the example interface admits zero while every consumer requires a positive scale.

Mirror the child min=Modelica.Constants.eps attribute on w0 and assert it at the example boundary before source-component parameter evaluation.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-04380](../confirmed/FINDING-04380.md) | Modelica.Mechanics.Rotational.Examples.CompareBrakingTorque | `w0` |
| [FINDING-04381](../confirmed/FINDING-04381.md) | Modelica.Mechanics.Rotational.Examples.CompareBrakingTorque | `w_nominal` |
| [FINDING-04423](../confirmed/FINDING-04423.md) | Modelica.Mechanics.Translational.Examples.CompareBrakingForce | `v0` |
| [FINDING-04424](../confirmed/FINDING-04424.md) | Modelica.Mechanics.Translational.Examples.CompareBrakingForce | `v_nominal` |
