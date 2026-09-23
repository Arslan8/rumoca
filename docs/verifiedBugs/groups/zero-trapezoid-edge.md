# Zero trapezoid edge duration is handled by branch reachability

Group `zero-trapezoid-edge` · 16 report instances · false-positives

rising and falling explicitly have min=0. The division by rising is inside time<T_start+T_rising; when rising=0 that interval is empty. The falling division is similarly confined to an empty interval when falling=0. Zero therefore produces an instantaneous edge rather than a reachable divide-by-zero.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-00297](../false-positives/FINDING-00297.md) | Modelica.Electrical.Analog.Examples.HeatingNPN_NORGate | `V1.signalSource.rising` |
| [FINDING-00298](../false-positives/FINDING-00298.md) | Modelica.Electrical.Analog.Examples.HeatingNPN_NORGate | `V1.signalSource.falling` |
| [FINDING-00299](../false-positives/FINDING-00299.md) | Modelica.Electrical.Analog.Examples.HeatingNPN_NORGate | `V2.signalSource.rising` |
| [FINDING-00300](../false-positives/FINDING-00300.md) | Modelica.Electrical.Analog.Examples.HeatingNPN_NORGate | `V2.signalSource.falling` |
| [FINDING-00329](../false-positives/FINDING-00329.md) | Modelica.Electrical.Analog.Examples.HeatingPNP_NORGate | `V1.signalSource.rising` |
| [FINDING-00330](../false-positives/FINDING-00330.md) | Modelica.Electrical.Analog.Examples.HeatingPNP_NORGate | `V1.signalSource.falling` |
| [FINDING-00331](../false-positives/FINDING-00331.md) | Modelica.Electrical.Analog.Examples.HeatingPNP_NORGate | `V2.signalSource.rising` |
| [FINDING-00332](../false-positives/FINDING-00332.md) | Modelica.Electrical.Analog.Examples.HeatingPNP_NORGate | `V2.signalSource.falling` |
| [FINDING-00754](../false-positives/FINDING-00754.md) | Modelica.Electrical.Analog.Examples.NandGate | `VIN1.signalSource.rising` |
| [FINDING-00755](../false-positives/FINDING-00755.md) | Modelica.Electrical.Analog.Examples.NandGate | `VIN1.signalSource.falling` |
| [FINDING-00756](../false-positives/FINDING-00756.md) | Modelica.Electrical.Analog.Examples.NandGate | `VIN2.signalSource.rising` |
| [FINDING-00757](../false-positives/FINDING-00757.md) | Modelica.Electrical.Analog.Examples.NandGate | `VIN2.signalSource.falling` |
| [FINDING-01026](../false-positives/FINDING-01026.md) | Modelica.Electrical.Analog.Examples.SimpleTriacCircuit | `trapezoidCurrent.signalSource.rising` |
| [FINDING-01027](../false-positives/FINDING-01027.md) | Modelica.Electrical.Analog.Examples.SimpleTriacCircuit | `trapezoidCurrent.signalSource.falling` |
| [FINDING-04734](../false-positives/FINDING-04734.md) | Modelica.Thermal.FluidHeatFlow.Examples.WaterPump | `trapezoid.rising` |
| [FINDING-04735](../false-positives/FINDING-04735.md) | Modelica.Thermal.FluidHeatFlow.Examples.WaterPump | `trapezoid.falling` |
