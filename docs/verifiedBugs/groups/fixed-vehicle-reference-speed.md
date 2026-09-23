# vRef is a protected nonzero constant

Group `fixed-vehicle-reference-speed` · 9 report instances · false-positives

Vehicle declares protected constant SI.Velocity vRef=1. It is an immutable unit/reference scale passed into the drag component and cannot reach zero through model parameter modification. The report lost constant/protected role information.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-05098](../false-positives/FINDING-05098.md) | ModelicaTest.Translational.Vehicles | `vehicleDrag.vRef` |
| [FINDING-05100](../false-positives/FINDING-05100.md) | ModelicaTest.Translational.Vehicles | `vehicleDragInConst.vRef` |
| [FINDING-05102](../false-positives/FINDING-05102.md) | ModelicaTest.Translational.Vehicles | `vehicleDragInVar.vRef` |
| [FINDING-05104](../false-positives/FINDING-05104.md) | ModelicaTest.Translational.Vehicles | `vehicleRoll.vRef` |
| [FINDING-05106](../false-positives/FINDING-05106.md) | ModelicaTest.Translational.Vehicles | `vehicleRollInConst.vRef` |
| [FINDING-05108](../false-positives/FINDING-05108.md) | ModelicaTest.Translational.Vehicles | `vehicleRollInVar.vRef` |
| [FINDING-05110](../false-positives/FINDING-05110.md) | ModelicaTest.Translational.Vehicles | `vehicleInclination.vRef` |
| [FINDING-05112](../false-positives/FINDING-05112.md) | ModelicaTest.Translational.Vehicles | `vehicleInclinationInConst.vRef` |
| [FINDING-05114](../false-positives/FINDING-05114.md) | ModelicaTest.Translational.Vehicles | `vehicleInclinationInVar.vRef` |
