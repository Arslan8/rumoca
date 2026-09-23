# Vehicle parameter has a multiplicative zero limit

Group `vehicle-zero-idealization` · 28 report instances · false-positives

J is passed to Rotational.Inertia and used in torque balance. At zero it removes that inertia or aerodynamic term; the Vehicle source does not divide by it. A physical production vehicle has positive values, but this component also supports idealized/lumped configurations, so a blanket strictly-positive sanitizer finding is not a verified bug.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0367](../false-positives/DECL-0367.md) | — | `J` |
| [FINDING-05050](../false-positives/FINDING-05050.md) | ModelicaTest.Translational.Vehicles | `vehicleDrag.m` |
| [FINDING-05051](../false-positives/FINDING-05051.md) | ModelicaTest.Translational.Vehicles | `vehicleDrag.J` |
| [FINDING-05053](../false-positives/FINDING-05053.md) | ModelicaTest.Translational.Vehicles | `vehicleDrag.rho` |
| [FINDING-05056](../false-positives/FINDING-05056.md) | ModelicaTest.Translational.Vehicles | `vehicleDragInConst.m` |
| [FINDING-05057](../false-positives/FINDING-05057.md) | ModelicaTest.Translational.Vehicles | `vehicleDragInConst.J` |
| [FINDING-05059](../false-positives/FINDING-05059.md) | ModelicaTest.Translational.Vehicles | `vehicleDragInConst.rho` |
| [FINDING-05062](../false-positives/FINDING-05062.md) | ModelicaTest.Translational.Vehicles | `vehicleDragInVar.m` |
| [FINDING-05063](../false-positives/FINDING-05063.md) | ModelicaTest.Translational.Vehicles | `vehicleDragInVar.J` |
| [FINDING-05065](../false-positives/FINDING-05065.md) | ModelicaTest.Translational.Vehicles | `vehicleDragInVar.rho` |
| [FINDING-05068](../false-positives/FINDING-05068.md) | ModelicaTest.Translational.Vehicles | `vehicleRoll.m` |
| [FINDING-05069](../false-positives/FINDING-05069.md) | ModelicaTest.Translational.Vehicles | `vehicleRoll.J` |
| [FINDING-05070](../false-positives/FINDING-05070.md) | ModelicaTest.Translational.Vehicles | `vehicleRoll.rho` |
| [FINDING-05073](../false-positives/FINDING-05073.md) | ModelicaTest.Translational.Vehicles | `vehicleRollInConst.m` |
| [FINDING-05074](../false-positives/FINDING-05074.md) | ModelicaTest.Translational.Vehicles | `vehicleRollInConst.J` |
| [FINDING-05075](../false-positives/FINDING-05075.md) | ModelicaTest.Translational.Vehicles | `vehicleRollInConst.rho` |
| [FINDING-05078](../false-positives/FINDING-05078.md) | ModelicaTest.Translational.Vehicles | `vehicleRollInVar.m` |
| [FINDING-05079](../false-positives/FINDING-05079.md) | ModelicaTest.Translational.Vehicles | `vehicleRollInVar.J` |
| [FINDING-05080](../false-positives/FINDING-05080.md) | ModelicaTest.Translational.Vehicles | `vehicleRollInVar.rho` |
| [FINDING-05083](../false-positives/FINDING-05083.md) | ModelicaTest.Translational.Vehicles | `vehicleInclination.m` |
| [FINDING-05084](../false-positives/FINDING-05084.md) | ModelicaTest.Translational.Vehicles | `vehicleInclination.J` |
| [FINDING-05085](../false-positives/FINDING-05085.md) | ModelicaTest.Translational.Vehicles | `vehicleInclination.rho` |
| [FINDING-05088](../false-positives/FINDING-05088.md) | ModelicaTest.Translational.Vehicles | `vehicleInclinationInConst.m` |
| [FINDING-05089](../false-positives/FINDING-05089.md) | ModelicaTest.Translational.Vehicles | `vehicleInclinationInConst.J` |
| [FINDING-05090](../false-positives/FINDING-05090.md) | ModelicaTest.Translational.Vehicles | `vehicleInclinationInConst.rho` |
| [FINDING-05093](../false-positives/FINDING-05093.md) | ModelicaTest.Translational.Vehicles | `vehicleInclinationInVar.m` |
| [FINDING-05094](../false-positives/FINDING-05094.md) | ModelicaTest.Translational.Vehicles | `vehicleInclinationInVar.J` |
| [FINDING-05095](../false-positives/FINDING-05095.md) | ModelicaTest.Translational.Vehicles | `vehicleInclinationInVar.rho` |
