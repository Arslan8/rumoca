# OneWayValve divides by unconstrained nominal scales

Group `one-way-valve-scales` · 2 report instances · confirmed

The valve declares V_flowNominal and dpNominal without positive bounds, then evaluates dpForward/V_flowNominal and V_flowBackward/dpNominal in its piecewise constitutive equations. Either zero scale is directly undefined.

Require and assert strictly positive nominal flow magnitude and nominal backward pressure before forming the slopes. If signed configuration is intended, separate direction from positive magnitudes rather than allowing a zero denominator.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-04744](../confirmed/FINDING-04744.md) | Modelica.Thermal.FluidHeatFlow.Examples.WaterPump | `oneWayValve.V_flowNominal` |
| [FINDING-04745](../confirmed/FINDING-04745.md) | Modelica.Thermal.FluidHeatFlow.Examples.WaterPump | `oneWayValve.dpNominal` |
