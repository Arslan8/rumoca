# `SI.Area` — 42 unbounded declarations

Domain: mechanical

`Units.mo` declares `type Area` with **no `min`**, so every
declaration below accepts a negative value.

## Exposed

| File | Line | Parameter | Declared modifiers |
|---|---|---|---|
| `Electrical/Spice3.mo` | 4457 | `AD` | `—` |
| `Electrical/Spice3.mo` | 4458 | `AS` | `—` |
| `Electrical/Spice3.mo` | 4663 | `AD` | `—` |
| `Electrical/Spice3.mo` | 4664 | `AS` | `—` |
| `Fluid/Dissipation.mo` | 12629 | `A_cross` | `—` |
| `Fluid/Dissipation.mo` | 12631 | `A_cross_nom` | `—` |
| `Fluid/Examples/AST_BatchPlant.mo` | 604 | `crossArea` | `—` |
| `Fluid/Examples/AST_BatchPlant.mo` | 605 | `top_pipeArea` | `—` |
| `Fluid/Examples/AST_BatchPlant.mo` | 606 | `side_pipeArea` | `—` |
| `Fluid/Examples/AST_BatchPlant.mo` | 607 | `bottom_pipeArea` | `—` |
| `Fluid/Examples/AST_BatchPlant.mo` | 1445 | `crossArea` | `—` |
| `Fluid/Examples/HeatExchanger.mo` | 118 | `crossArea_1` | `—` |
| `Fluid/Examples/HeatExchanger.mo` | 119 | `crossArea_2` | `—` |
| `Fluid/Examples/HeatExchanger.mo` | 138 | `area_h_1` | `—` |
| `Fluid/Examples/HeatExchanger.mo` | 139 | `area_h_2` | `—` |
| `Fluid/Examples/HeatExchanger.mo` | 151 | `area_h` | `—` |
| `Fluid/Examples/HeatExchanger.mo` | 407 | `area_h` | `—` |
| `Fluid/Machines.mo` | 9 | `pistonCrossArea` | `—` |
| `Fluid/Pipes.mo` | 235 | `crossArea` | `—` |
| `Fluid/Vessels.mo` | 57 | `crossArea` | `—` |
| `Fluid/Vessels.mo` | 276 | `vesselArea` | `—` |
| `Magnetic/FluxTubes/BaseClasses/Generic.mo` | 10 | `A` | `—` |
| `Magnetic/FluxTubes/Basic/EddyCurrent.mo` | 20 | `A` | `—` |
| `Magnetic/FluxTubes/Basic/ElectroMagneticConverterWithLeakageInductance.mo` | 28 | `A` | `—` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer1PhaseWithHysteresis.mo` | 100 | `A_l1` | `—` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer1PhaseWithHysteresis.mo` | 106 | `A_l2` | `—` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer3PhaseYyWithHysteresis.mo` | 102 | `A_l1` | `—` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer3PhaseYyWithHysteresis.mo` | 108 | `A_l2` | `—` |
| `Magnetic/FluxTubes/Examples/Utilities/CoilDesign.mo` | 18 | `A_w` | `—` |
| `Magnetic/FluxTubes/Examples/Utilities/CoilDesign.mo` | 38 | `A_wireCalculated` | `—` |
| `Magnetic/FluxTubes/Examples/Utilities/CoilDesign.mo` | 55 | `A_wireChosen` | `—` |
| `Magnetic/FluxTubes/Shapes/Force/CuboidParallelFlux.mo` | 16 | `A` | `—` |
| `Magnetic/FluxTubes/Shapes/Force/HollowCylinderAxialFlux.mo` | 16 | `A` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Basic/EddyCurrent.mo` | 19 | `A` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Sensors/Transient/FundamentalWavePermabilitySensor.mo` | 6 | `A` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Sensors/Transient/Permeability.mo` | 5 | `A` | `—` |
| `Mechanics/Translational/Components/Vehicle.mo` | 7 | `A` | `(start=1)` |
| `Mechanics/Translational/Examples/Vehicle.mo` | 7 | `A` | `—` |
| `StateGraph.mo` | 1538 | `A` | `—` |
| `StateGraph.mo` | 1539 | `a` | `—` |
| `Thermal/FluidHeatFlow/Components/Cylinder.mo` | 6 | `A` | `—` |
| `Thermal/FluidHeatFlow/Components/OpenTank.mo` | 5 | `ATank` | `(start=1)` |

## Guarded — these add their own bound

Same library, same quantity, bound written. This is why the exposed
cases read as omissions rather than as a deliberate choice.

| File | Line | Parameter | Declared modifiers |
|---|---|---|---|
| `Fluid/Valves.mo` | 495 | `Av` | `( fixed= CvData == Modelica.Fluid.Types.CvTypes.Av, start=m_flow_nomin` |
