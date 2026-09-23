# Vehicle exposes zero regularization speed to reciprocal equations

Group `vehicle-regularization-speed` · 9 report instances · confirmed

Vehicle declares vReg=1e-3 without propagating the positive bound of RollingResistance.v0, then passes final v0=vReg. Every regularization branch divides by v0. The outer parameter therefore appears to allow zero even though the consumer requires at least Modelica.Constants.eps.

Mirror v0(final min=Modelica.Constants.eps) on Vehicle.vReg and add a clear assertion before constructing/evaluating regularization. Keep the exact positive bound consistent between wrapper and component.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-05099](../confirmed/FINDING-05099.md) | ModelicaTest.Translational.Vehicles | `vehicleDrag.vReg` |
| [FINDING-05101](../confirmed/FINDING-05101.md) | ModelicaTest.Translational.Vehicles | `vehicleDragInConst.vReg` |
| [FINDING-05103](../confirmed/FINDING-05103.md) | ModelicaTest.Translational.Vehicles | `vehicleDragInVar.vReg` |
| [FINDING-05105](../confirmed/FINDING-05105.md) | ModelicaTest.Translational.Vehicles | `vehicleRoll.vReg` |
| [FINDING-05107](../confirmed/FINDING-05107.md) | ModelicaTest.Translational.Vehicles | `vehicleRollInConst.vReg` |
| [FINDING-05109](../confirmed/FINDING-05109.md) | ModelicaTest.Translational.Vehicles | `vehicleRollInVar.vReg` |
| [FINDING-05111](../confirmed/FINDING-05111.md) | ModelicaTest.Translational.Vehicles | `vehicleInclination.vReg` |
| [FINDING-05113](../confirmed/FINDING-05113.md) | ModelicaTest.Translational.Vehicles | `vehicleInclinationInConst.vReg` |
| [FINDING-05115](../confirmed/FINDING-05115.md) | ModelicaTest.Translational.Vehicles | `vehicleInclinationInVar.vReg` |
