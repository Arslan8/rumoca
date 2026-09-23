# Zero effective drag area switches off aerodynamic drag

Group `disabled-drag` · 6 report instances · false-positives

Here A enters f_nominal=-Cd*A*rho*vRef^2/2 as a multiplier; the speed normalization uses the separate protected vRef=1. A=0 is a no-aerodynamic-drag configuration, not a zero geometric divisor. The reported invariant is too broad for this effective coefficient.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-05044](../false-positives/FINDING-05044.md) | ModelicaTest.Translational.Vehicles | `vehicleRoll.A` |
| [FINDING-05045](../false-positives/FINDING-05045.md) | ModelicaTest.Translational.Vehicles | `vehicleRollInConst.A` |
| [FINDING-05046](../false-positives/FINDING-05046.md) | ModelicaTest.Translational.Vehicles | `vehicleRollInVar.A` |
| [FINDING-05047](../false-positives/FINDING-05047.md) | ModelicaTest.Translational.Vehicles | `vehicleInclination.A` |
| [FINDING-05048](../false-positives/FINDING-05048.md) | ModelicaTest.Translational.Vehicles | `vehicleInclinationInConst.A` |
| [FINDING-05049](../false-positives/FINDING-05049.md) | ModelicaTest.Translational.Vehicles | `vehicleInclinationInVar.A` |
