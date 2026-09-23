# Zero thermal conductance is an insulating limit

Group `zero-thermal-conductance` · 20 report instances · false-positives

The complete constitutive equation is Q_flow=G*dT. G is only a multiplier; at zero the component transports no heat. There is no source reciprocal and the component represents a lumped effective conductance, so a blanket strictly-positive claim rejects the ordinary insulation/open-thermal-path limit. A larger network may still need another equation for each isolated temperature.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0894](../false-positives/DECL-0894.md) | — | `G` |
| [FINDING-00265](../false-positives/FINDING-00265.md) | Modelica.Electrical.Analog.Examples.HeatingMOSInverter | `TC1.G` |
| [FINDING-00268](../false-positives/FINDING-00268.md) | Modelica.Electrical.Analog.Examples.HeatingMOSInverter | `TC2.G` |
| [FINDING-00269](../false-positives/FINDING-00269.md) | Modelica.Electrical.Analog.Examples.HeatingMOSInverter | `TC3.G` |
| [FINDING-00281](../false-positives/FINDING-00281.md) | Modelica.Electrical.Analog.Examples.HeatingNPN_NORGate | `TC1.G` |
| [FINDING-00282](../false-positives/FINDING-00282.md) | Modelica.Electrical.Analog.Examples.HeatingNPN_NORGate | `TC2.G` |
| [FINDING-00313](../false-positives/FINDING-00313.md) | Modelica.Electrical.Analog.Examples.HeatingPNP_NORGate | `TC1.G` |
| [FINDING-00314](../false-positives/FINDING-00314.md) | Modelica.Electrical.Analog.Examples.HeatingPNP_NORGate | `TC2.G` |
| [FINDING-00346](../false-positives/FINDING-00346.md) | Modelica.Electrical.Analog.Examples.HeatingRectifier | `ThermalConductor1.G` |
| [FINDING-00975](../false-positives/FINDING-00975.md) | Modelica.Electrical.Analog.Examples.Resistor | `thermalConductor.G` |
| [FINDING-01237](../false-positives/FINDING-01237.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `armatureCore.G` |
| [FINDING-01239](../false-positives/FINDING-01239.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `coreCooling.G` |
| [FINDING-04503](../false-positives/FINDING-04503.md) | Modelica.Thermal.FluidHeatFlow.Examples.IndirectCooling | `thermalConductor.G` |
| [FINDING-04544](../false-positives/FINDING-04544.md) | Modelica.Thermal.FluidHeatFlow.Examples.OneMass | `thermalConductor.G` |
| [FINDING-04687](../false-positives/FINDING-04687.md) | Modelica.Thermal.FluidHeatFlow.Examples.TwoMass | `thermalConductor1.G` |
| [FINDING-04689](../false-positives/FINDING-04689.md) | Modelica.Thermal.FluidHeatFlow.Examples.TwoMass | `thermalConductor2.G` |
| [FINDING-04751](../false-positives/FINDING-04751.md) | Modelica.Thermal.HeatTransfer.Examples.ControlledTemperature | `thermalConductor.G` |
| [FINDING-04760](../false-positives/FINDING-04760.md) | Modelica.Thermal.HeatTransfer.Examples.GenerationOfFMUs | `conductor.thermalConductor.G` |
| [FINDING-04765](../false-positives/FINDING-04765.md) | Modelica.Thermal.HeatTransfer.Examples.TwoMasses | `conduction.G` |
| [FINDING-04769](../false-positives/FINDING-04769.md) | Modelica.Thermal.HeatTransfer.Examples.Utilities.Conduction | `thermalConductor.G` |
