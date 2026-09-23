# The friction denominator is protected by an ordering assertion

Group `asserted-friction-flow-order` · 19 report instances · false-positives

The only difference denominator is (V_flowNominal-V_flowLaminar)^2. V_flowLaminar has min=Modelica.Constants.small, and the initial algorithm asserts V_flowNominal>V_flowLaminar before computing k. Consequently V_flowNominal cannot be zero or equal to the laminar value in an admissible initialization. The detector ignored the inherited positive bound and relational assertion.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-01267](../false-positives/FINDING-01267.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `cooling.V_flowNominal` |
| [FINDING-04527](../false-positives/FINDING-04527.md) | Modelica.Thermal.FluidHeatFlow.Examples.IndirectCooling | `pipe1.V_flowNominal` |
| [FINDING-04528](../false-positives/FINDING-04528.md) | Modelica.Thermal.FluidHeatFlow.Examples.IndirectCooling | `outerPipe.V_flowNominal` |
| [FINDING-04529](../false-positives/FINDING-04529.md) | Modelica.Thermal.FluidHeatFlow.Examples.IndirectCooling | `innerPipe.V_flowNominal` |
| [FINDING-04547](../false-positives/FINDING-04547.md) | Modelica.Thermal.FluidHeatFlow.Examples.OneMass | `pipe.V_flowNominal` |
| [FINDING-04573](../false-positives/FINDING-04573.md) | Modelica.Thermal.FluidHeatFlow.Examples.ParallelCooling | `pipe1.V_flowNominal` |
| [FINDING-04574](../false-positives/FINDING-04574.md) | Modelica.Thermal.FluidHeatFlow.Examples.ParallelCooling | `pipe2.V_flowNominal` |
| [FINDING-04575](../false-positives/FINDING-04575.md) | Modelica.Thermal.FluidHeatFlow.Examples.ParallelCooling | `pipe3.V_flowNominal` |
| [FINDING-04601](../false-positives/FINDING-04601.md) | Modelica.Thermal.FluidHeatFlow.Examples.ParallelPumpDropOut | `pipe1.V_flowNominal` |
| [FINDING-04602](../false-positives/FINDING-04602.md) | Modelica.Thermal.FluidHeatFlow.Examples.ParallelPumpDropOut | `pipe2.V_flowNominal` |
| [FINDING-04603](../false-positives/FINDING-04603.md) | Modelica.Thermal.FluidHeatFlow.Examples.ParallelPumpDropOut | `pipe3.V_flowNominal` |
| [FINDING-04630](../false-positives/FINDING-04630.md) | Modelica.Thermal.FluidHeatFlow.Examples.PumpAndValve | `pipe.V_flowNominal` |
| [FINDING-04647](../false-positives/FINDING-04647.md) | Modelica.Thermal.FluidHeatFlow.Examples.PumpDropOut | `pipe.V_flowNominal` |
| [FINDING-04664](../false-positives/FINDING-04664.md) | Modelica.Thermal.FluidHeatFlow.Examples.SimpleCooling | `pipe.V_flowNominal` |
| [FINDING-04692](../false-positives/FINDING-04692.md) | Modelica.Thermal.FluidHeatFlow.Examples.TwoMass | `pipe1.V_flowNominal` |
| [FINDING-04693](../false-positives/FINDING-04693.md) | Modelica.Thermal.FluidHeatFlow.Examples.TwoMass | `pipe2.V_flowNominal` |
| [FINDING-04694](../false-positives/FINDING-04694.md) | Modelica.Thermal.FluidHeatFlow.Examples.TwoMass | `pipe3.V_flowNominal` |
| [FINDING-04711](../false-positives/FINDING-04711.md) | Modelica.Thermal.FluidHeatFlow.Examples.TwoTanks | `pipe.V_flowNominal` |
| [FINDING-04749](../false-positives/FINDING-04749.md) | Modelica.Thermal.FluidHeatFlow.Examples.WaterPump | `pipe.V_flowNominal` |
