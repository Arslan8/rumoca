# `SI.Length` — 215 unbounded declarations

Domain: mechanical

`Units.mo` declares `type Length` with **no `min`**, so every
declaration below accepts a negative value.

## Exposed

| File | Line | Parameter | Declared modifiers |
|---|---|---|---|
| `Blocks/package.mo` | 2364 | `L` | `—` |
| `Electrical/Analog/Examples/Lines/CompareLineTrunks.mo` | 11 | `len` | `—` |
| `Electrical/Analog/Examples/Lines/CompareLosslessLines.mo` | 9 | `len` | `—` |
| `Electrical/Analog/Examples/Lines/LightningLosslessTransmissionLine.mo` | 12 | `len` | `—` |
| `Electrical/Analog/Examples/Lines/LightningSegmentedTransmissionLine.mo` | 12 | `len` | `—` |
| `Electrical/Analog/Examples/Lines/SmoothStep.mo` | 11 | `len` | `—` |
| `Electrical/Analog/Semiconductors/NMOS.mo` | 12 | `W` | `—` |
| `Electrical/Analog/Semiconductors/NMOS.mo` | 13 | `L` | `—` |
| `Electrical/Analog/Semiconductors/NMOS.mo` | 18 | `dW` | `—` |
| `Electrical/Analog/Semiconductors/NMOS.mo` | 19 | `dL` | `—` |
| `Electrical/Analog/Semiconductors/PMOS.mo` | 12 | `W` | `—` |
| `Electrical/Analog/Semiconductors/PMOS.mo` | 13 | `L` | `—` |
| `Electrical/Analog/Semiconductors/PMOS.mo` | 18 | `dW` | `—` |
| `Electrical/Analog/Semiconductors/PMOS.mo` | 19 | `dL` | `—` |
| `Electrical/Machines/Examples/InductionMachines/IMC_Conveyor.mo` | 17 | `r` | `—` |
| `Electrical/Spice3.mo` | 4455 | `L` | `—` |
| `Electrical/Spice3.mo` | 4456 | `W` | `—` |
| `Electrical/Spice3.mo` | 4459 | `PD` | `—` |
| `Electrical/Spice3.mo` | 4460 | `PS` | `—` |
| `Electrical/Spice3.mo` | 4623 | `TOX` | `—` |
| `Electrical/Spice3.mo` | 4629 | `LD` | `—` |
| `Electrical/Spice3.mo` | 4661 | `L` | `—` |
| `Electrical/Spice3.mo` | 4662 | `W` | `—` |
| `Electrical/Spice3.mo` | 4665 | `PD` | `—` |
| `Electrical/Spice3.mo` | 4666 | `PS` | `—` |
| `Electrical/Spice3.mo` | 4850 | `XJ` | `—` |
| `Electrical/Spice3.mo` | 5331 | `L` | `—` |
| `Electrical/Spice3.mo` | 5332 | `W` | `—` |
| `Electrical/Spice3.mo` | 5400 | `DEFW` | `—` |
| `Electrical/Spice3.mo` | 5401 | `NARROW` | `—` |
| `Electrical/Spice3.mo` | 5413 | `L` | `(start = 0)` |
| `Electrical/Spice3.mo` | 5414 | `W` | `—` |
| `Electrical/Spice3.mo` | 5492 | `DEFW` | `—` |
| `Electrical/Spice3.mo` | 5493 | `NARROW` | `—` |
| `Fluid/Examples/AST_BatchPlant.mo` | 11 | `pipeDiameter` | `—` |
| `Fluid/Examples/HeatExchanger.mo` | 120 | `perimeter_1` | `—` |
| `Fluid/Examples/HeatExchanger.mo` | 121 | `perimeter_2` | `—` |
| `Fluid/Examples/HeatExchanger.mo` | 406 | `s` | `—` |
| `Fluid/Fittings.mo` | 434 | `length` | `—` |
| `Fluid/Pipes.mo` | 228 | `length` | `—` |
| `Fluid/Pipes.mo` | 247 | `height_ab` | `—` |
| `Magnetic/FluxTubes/BaseClasses/Generic.mo` | 7 | `l` | `—` |
| `Magnetic/FluxTubes/BaseClasses/GenericHysteresis.mo` | 11 | `d` | `—` |
| `Magnetic/FluxTubes/Basic/EddyCurrent.mo` | 18 | `l` | `—` |
| `Magnetic/FluxTubes/Basic/ElectroMagneticConverterWithLeakageInductance.mo` | 26 | `L` | `—` |
| `Magnetic/FluxTubes/Examples/BasicExamples/QuadraticCoreAirgap.mo` | 4 | `l` | `—` |
| `Magnetic/FluxTubes/Examples/BasicExamples/QuadraticCoreAirgap.mo` | 5 | `a` | `—` |
| `Magnetic/FluxTubes/Examples/BasicExamples/QuadraticCoreAirgap.mo` | 7 | `delta` | `—` |
| `Magnetic/FluxTubes/Examples/BasicExamples/ToroidalCoreAirgap.mo` | 5 | `r` | `—` |
| `Magnetic/FluxTubes/Examples/BasicExamples/ToroidalCoreAirgap.mo` | 6 | `d` | `—` |
| `Magnetic/FluxTubes/Examples/BasicExamples/ToroidalCoreAirgap.mo` | 8 | `delta` | `—` |
| `Magnetic/FluxTubes/Examples/BasicExamples/ToroidalCoreQuadraticCrossSection.mo` | 6 | `r_o` | `—` |
| `Magnetic/FluxTubes/Examples/BasicExamples/ToroidalCoreQuadraticCrossSection.mo` | 7 | `r_i` | `—` |
| `Magnetic/FluxTubes/Examples/BasicExamples/ToroidalCoreQuadraticCrossSection.mo` | 8 | `l` | `—` |
| `Magnetic/FluxTubes/Examples/BasicExamples/ToroidalCoreQuadraticCrossSection.mo` | 10 | `delta` | `—` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer1PhaseWithHysteresis.mo` | 15 | `L1` | `(displayUnit="mm")` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer1PhaseWithHysteresis.mo` | 18 | `d1` | `(displayUnit="mm")` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer1PhaseWithHysteresis.mo` | 30 | `L2` | `(displayUnit="mm")` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer1PhaseWithHysteresis.mo` | 33 | `d2` | `(displayUnit="mm")` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer1PhaseWithHysteresis.mo` | 43 | `l1` | `(displayUnit="mm")` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer1PhaseWithHysteresis.mo` | 45 | `l2` | `(displayUnit="mm")` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer1PhaseWithHysteresis.mo` | 47 | `a` | `(displayUnit="mm")` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer1PhaseWithHysteresis.mo` | 48 | `b` | `(displayUnit="mm")` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer1PhaseWithHysteresis.mo` | 97 | `t` | `(displayUnit="mm")` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer1PhaseWithHysteresis.mo` | 99 | `L_l1` | `—` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer1PhaseWithHysteresis.mo` | 104 | `L_l2` | `—` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer3PhaseYyWithHysteresis.mo` | 11 | `L1` | `(displayUnit="mm")` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer3PhaseYyWithHysteresis.mo` | 14 | `d1` | `(displayUnit="mm")` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer3PhaseYyWithHysteresis.mo` | 26 | `L2` | `(displayUnit="mm")` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer3PhaseYyWithHysteresis.mo` | 29 | `d2` | `(displayUnit="mm")` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer3PhaseYyWithHysteresis.mo` | 39 | `l1` | `(displayUnit="mm")` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer3PhaseYyWithHysteresis.mo` | 41 | `l2` | `(displayUnit="mm")` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer3PhaseYyWithHysteresis.mo` | 43 | `a` | `(displayUnit="mm")` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer3PhaseYyWithHysteresis.mo` | 44 | `b` | `(displayUnit="mm")` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer3PhaseYyWithHysteresis.mo` | 98 | `t` | `(displayUnit="mm")` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer3PhaseYyWithHysteresis.mo` | 101 | `L_l1` | `—` |
| `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer3PhaseYyWithHysteresis.mo` | 106 | `L_l2` | `—` |
| `Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/PermeanceActuator.mo` | 13 | `l_PM` | `—` |
| `Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/PermeanceActuator.mo` | 15 | `t` | `—` |
| `Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/PermeanceActuator.mo` | 18 | `l_air` | `—` |
| `Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/PermeanceActuator.mo` | 21 | `l_FeOut` | `—` |
| `Magnetic/FluxTubes/Examples/SolenoidActuator/Components/AdvancedSolenoid.mo` | 17 | `l_yoke` | `—` |
| `Magnetic/FluxTubes/Examples/SolenoidActuator/Components/AdvancedSolenoid.mo` | 18 | `t_yokeBot` | `—` |
| `Magnetic/FluxTubes/Examples/SolenoidActuator/Components/AdvancedSolenoid.mo` | 21 | `l_pole` | `—` |
| `Magnetic/FluxTubes/Examples/SolenoidActuator/Components/AdvancedSolenoid.mo` | 22 | `t_poleBot` | `—` |
| `Magnetic/FluxTubes/Examples/SolenoidActuator/Components/AdvancedSolenoid.mo` | 25 | `t_airPar` | `—` |
| `Magnetic/FluxTubes/Examples/SolenoidActuator/Components/AdvancedSolenoid.mo` | 36 | `l_arm` | `—` |
| `Magnetic/FluxTubes/Examples/SolenoidActuator/Components/SimpleSolenoid.mo` | 13 | `l_yoke` | `—` |
| `Magnetic/FluxTubes/Examples/SolenoidActuator/Components/SimpleSolenoid.mo` | 14 | `t_yokeBot` | `—` |
| `Magnetic/FluxTubes/Examples/SolenoidActuator/Components/SimpleSolenoid.mo` | 17 | `l_pole` | `—` |
| `Magnetic/FluxTubes/Examples/SolenoidActuator/Components/SimpleSolenoid.mo` | 18 | `t_poleBot` | `—` |
| `Magnetic/FluxTubes/Examples/SolenoidActuator/Components/SimpleSolenoid.mo` | 21 | `t_airPar` | `—` |
| `Magnetic/FluxTubes/Examples/SolenoidActuator/Components/SimpleSolenoid.mo` | 32 | `l_arm` | `—` |
| `Magnetic/FluxTubes/Examples/Utilities/CoilDesign.mo` | 15 | `h_w` | `—` |
| `Magnetic/FluxTubes/Examples/Utilities/CoilDesign.mo` | 16 | `b_w` | `—` |
| `Magnetic/FluxTubes/Examples/Utilities/CoilDesign.mo` | 20 | `l_avg` | `—` |
| `Magnetic/FluxTubes/Examples/Utilities/TranslatoryArmatureAndStopper.mo` | 5 | `L` | `(start=0)` |
| `Magnetic/FluxTubes/Shapes/FixedShape/Cuboid.mo` | 8 | `l` | `—` |
| `Magnetic/FluxTubes/Shapes/FixedShape/Cuboid.mo` | 11 | `a` | `—` |
| `Magnetic/FluxTubes/Shapes/FixedShape/Cuboid.mo` | 13 | `b` | `—` |
| `Magnetic/FluxTubes/Shapes/FixedShape/GenericFluxTube.mo` | 8 | `l` | `—` |
| `Magnetic/FluxTubes/Shapes/FixedShape/HollowCylinderAxialFlux.mo` | 8 | `l` | `—` |
| `Magnetic/FluxTubes/Shapes/FixedShape/HollowCylinderCircumferentialFlux.mo` | 8 | `l` | `—` |
| `Magnetic/FluxTubes/Shapes/FixedShape/HollowCylinderRadialFlux.mo` | 8 | `l` | `—` |
| `Magnetic/FluxTubes/Shapes/Force/CuboidOrthogonalFlux.mo` | 10 | `a` | `—` |
| `Magnetic/FluxTubes/Shapes/Force/CuboidOrthogonalFlux.mo` | 11 | `b` | `—` |
| `Magnetic/FluxTubes/Shapes/Force/CuboidParallelFlux.mo` | 10 | `a` | `—` |
| `Magnetic/FluxTubes/Shapes/Force/CuboidParallelFlux.mo` | 11 | `b` | `—` |
| `Magnetic/FluxTubes/Shapes/Force/LeakageAroundPoles.mo` | 9 | `w` | `—` |
| `Magnetic/FluxTubes/Shapes/Leakage/CoaxCylindersEndFaces.mo` | 15 | `t` | `—` |
| `Magnetic/FluxTubes/Shapes/Leakage/EighthOfHollowSphere.mo` | 7 | `t` | `(start=0.01)` |
| `Magnetic/FluxTubes/Shapes/Leakage/HalfCylinder.mo` | 6 | `l` | `—` |
| `Magnetic/FluxTubes/Shapes/Leakage/HalfHollowCylinder.mo` | 7 | `l` | `—` |
| `Magnetic/FluxTubes/Shapes/Leakage/QuarterCylinder.mo` | 7 | `l` | `—` |
| `Magnetic/FluxTubes/Shapes/Leakage/QuarterHollowCylinder.mo` | 7 | `l` | `—` |
| `Magnetic/FluxTubes/Shapes/Leakage/QuarterHollowSphere.mo` | 7 | `t` | `(start=0.01)` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/InductionMachines/IMC_Conveyor.mo` | 17 | `r` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Basic/EddyCurrent.mo` | 17 | `l` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Examples/BasicExamples/QuadraticCoreAirgap.mo` | 5 | `l` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Examples/BasicExamples/QuadraticCoreAirgap.mo` | 6 | `a` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Examples/BasicExamples/QuadraticCoreAirgap.mo` | 8 | `delta` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Examples/BasicExamples/ToroidalCoreAirgap.mo` | 5 | `r` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Examples/BasicExamples/ToroidalCoreAirgap.mo` | 6 | `d` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Examples/BasicExamples/ToroidalCoreAirgap.mo` | 8 | `delta` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Examples/BasicExamples/ToroidalCoreQuadraticCrossSection.mo` | 5 | `r_o` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Examples/BasicExamples/ToroidalCoreQuadraticCrossSection.mo` | 6 | `r_i` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Examples/BasicExamples/ToroidalCoreQuadraticCrossSection.mo` | 7 | `l` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Examples/BasicExamples/ToroidalCoreQuadraticCrossSection.mo` | 9 | `delta` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Sensors/Transient/FundamentalWavePermabilitySensor.mo` | 7 | `l` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Sensors/Transient/Permeability.mo` | 7 | `l` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Shapes/FixedShape/Cuboid.mo` | 8 | `l` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Shapes/FixedShape/Cuboid.mo` | 11 | `a` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Shapes/FixedShape/Cuboid.mo` | 13 | `b` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Shapes/FixedShape/GenericFluxTube.mo` | 8 | `l` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Shapes/FixedShape/HollowCylinderAxialFlux.mo` | 8 | `l` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Shapes/FixedShape/HollowCylinderCircumferentialFlux.mo` | 7 | `l` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Shapes/FixedShape/HollowCylinderRadialFlux.mo` | 8 | `l` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Shapes/Leakage/CoaxCylindersEndFaces.mo` | 15 | `t` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Shapes/Leakage/EighthOfHollowSphere.mo` | 7 | `t` | `(start=0.01)` |
| `Magnetic/QuasiStatic/FluxTubes/Shapes/Leakage/HalfCylinder.mo` | 6 | `l` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Shapes/Leakage/HalfHollowCylinder.mo` | 7 | `l` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Shapes/Leakage/QuarterCylinder.mo` | 7 | `l` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Shapes/Leakage/QuarterHollowCylinder.mo` | 7 | `l` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Shapes/Leakage/QuarterHollowSphere.mo` | 7 | `t` | `(start=0.01)` |
| `Magnetic/QuasiStatic/FundamentalWave/Examples/BasicMachines/InductionMachines/IMC_Conveyor.mo` | 16 | `r` | `—` |
| `Mechanics/MultiBody/Examples/Loops/PlanarLoops_analytic.mo` | 5 | `rh` | `—` |
| `Mechanics/MultiBody/Examples/Loops/PlanarLoops_analytic.mo` | 7 | `rv` | `—` |
| `Mechanics/MultiBody/Examples/Loops/PlanarLoops_analytic.mo` | 10 | `r1b` | `—` |
| `Mechanics/MultiBody/Examples/Loops/PlanarLoops_analytic.mo` | 12 | `r1a` | `—` |
| `Mechanics/MultiBody/Examples/Loops/PlanarLoops_analytic.mo` | 15 | `r2b` | `—` |
| `Mechanics/MultiBody/Examples/Loops/PlanarLoops_analytic.mo` | 17 | `r2a` | `—` |
| `Mechanics/MultiBody/Examples/Loops/PlanarLoops_analytic.mo` | 20 | `r3b` | `—` |
| `Mechanics/MultiBody/Examples/Loops/PlanarLoops_analytic.mo` | 22 | `r3a` | `—` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/Cylinder.mo` | 4 | `cylinderTopPosition` | `—` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/Cylinder.mo` | 6 | `pistonLength` | `—` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/Cylinder.mo` | 7 | `rodLength` | `—` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/Cylinder.mo` | 8 | `crankLength` | `—` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/Cylinder.mo` | 9 | `crankPinOffset` | `—` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/Cylinder.mo` | 11 | `crankPinLength` | `—` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/Cylinder.mo` | 15 | `cylinderLength` | `—` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/CylinderBase.mo` | 4 | `cylinderTopPosition` | `—` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/CylinderBase.mo` | 6 | `crankLength` | `—` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/CylinderBase.mo` | 7 | `crankPinOffset` | `—` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/CylinderBase.mo` | 9 | `crankPinLength` | `—` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/CylinderBase.mo` | 15 | `pistonLength` | `—` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/CylinderBase.mo` | 17 | `pistonCenterOfMass` | `—` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/CylinderBase.mo` | 32 | `rodLength` | `—` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/CylinderBase.mo` | 34 | `rodCenterOfMass` | `—` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/CylinderBase.mo` | 48 | `cylinderLength` | `—` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/GasForce2.mo` | 6 | `L` | `—` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/GasForce2.mo` | 7 | `d` | `—` |
| `Mechanics/MultiBody/Forces/LineForceWithTwoMasses.mo` | 36 | `cylinderLength_a` | `—` |
| `Mechanics/MultiBody/Forces/LineForceWithTwoMasses.mo` | 43 | `cylinderLength_b` | `—` |
| `Mechanics/MultiBody/Forces/Spring.mo` | 10 | `s_unstretched` | `—` |
| `Mechanics/MultiBody/Forces/SpringDamperParallel.mo` | 6 | `s_unstretched` | `—` |
| `Mechanics/MultiBody/Forces/SpringDamperSeries.mo` | 7 | `s_unstretched` | `—` |
| `Mechanics/MultiBody/Forces/SpringDamperSeries.mo` | 10 | `s_damper_start` | `—` |
| `Mechanics/MultiBody/Parts/BodyBox.mo` | 28 | `length` | `—` |
| `Mechanics/MultiBody/Parts/BodyCylinder.mo` | 27 | `length` | `—` |
| `Mechanics/MultiBody/Parts/BodyShape.mo` | 105 | `length` | `—` |
| `Mechanics/MultiBody/Parts/Fixed.mo` | 35 | `length` | `—` |
| `Mechanics/MultiBody/Parts/FixedRotation.mo` | 72 | `length` | `—` |
| `Mechanics/MultiBody/Parts/FixedTranslation.mo` | 39 | `length` | `—` |
| `Mechanics/MultiBody/Visualizers/Advanced/PipeWithScalarField.mo` | 11 | `length` | `—` |
| `Mechanics/MultiBody/Visualizers/PipeWithScalarField.mo` | 9 | `length` | `—` |
| `Mechanics/MultiBody/Visualizers/VoluminousWheel.mo` | 24 | `ri` | `—` |
| `Mechanics/MultiBody/package.mo` | 65 | `gravityArrowLength` | `—` |
| `Mechanics/MultiBody/package.mo` | 93 | `groundLength_u` | `—` |
| `Mechanics/MultiBody/package.mo` | 97 | `groundLength_v` | `—` |
| `Mechanics/MultiBody/package.mo` | 108 | `nominalLength` | `—` |
| `Mechanics/MultiBody/package.mo` | 110 | `defaultAxisLength` | `—` |
| `Mechanics/MultiBody/package.mo` | 113 | `defaultJointLength` | `—` |
| `Mechanics/MultiBody/package.mo` | 116 | `defaultJointWidth` | `—` |
| `Mechanics/MultiBody/package.mo` | 119 | `defaultForceLength` | `—` |
| `Mechanics/MultiBody/package.mo` | 122 | `defaultForceWidth` | `—` |
| `Mechanics/MultiBody/package.mo` | 125 | `defaultBodyDiameter` | `—` |
| `Mechanics/MultiBody/package.mo` | 131 | `defaultArrowDiameter` | `—` |
| `Mechanics/MultiBody/package.mo` | 173 | `headLength` | `—` |
| `Mechanics/MultiBody/package.mo` | 175 | `headWidth` | `—` |
| `Mechanics/MultiBody/package.mo` | 177 | `lineLength` | `—` |
| `Mechanics/MultiBody/package.mo` | 178 | `lineWidth` | `—` |
| `Mechanics/MultiBody/package.mo` | 181 | `scaledLabel` | `—` |
| `Mechanics/MultiBody/package.mo` | 183 | `labelStart` | `—` |
| `Mechanics/MultiBody/package.mo` | 273 | `gravityHeadLength` | `—` |
| `Mechanics/MultiBody/package.mo` | 275 | `gravityHeadWidth` | `—` |
| `Mechanics/MultiBody/package.mo` | 276 | `gravityLineLength` | `—` |
| `Mechanics/Translational/Components/Vehicle.mo` | 6 | `R` | `—` |
| `Mechanics/Translational/Examples/Utilities/Spring.mo` | 6 | `s_rel0` | `—` |
| `Mechanics/Translational/Examples/Utilities/SpringDamper.mo` | 8 | `s_rel0` | `—` |
| `Mechanics/Translational/Examples/Utilities/SpringDamperNoRelativeStates.mo` | 6 | `s_rel0` | `—` |
| `Mechanics/Translational/Examples/Vehicle.mo` | 6 | `R` | `—` |
| `Mechanics/Translational/Interfaces/PartialRigid.mo` | 6 | `L` | `(start=0)` |
| `Thermal/FluidHeatFlow/Components/Cylinder.mo` | 7 | `L` | `—` |
| `Thermal/FluidHeatFlow/Components/OpenTank.mo` | 6 | `hTank` | `(start=1)` |
| `Thermal/FluidHeatFlow/Components/Pipe.mo` | 8 | `h_g` | `(start=0)` |

## Guarded — these add their own bound

Same library, same quantity, bound written. This is why the exposed
cases read as omissions rather than as a deliberate choice.

| File | Line | Parameter | Declared modifiers |
|---|---|---|---|
| `Electrical/Analog/Lines/M_OLine.mo` | 4 | `length` | `(final min=Modelica.Constants.small)` |
| `Electrical/Analog/Lines/OLine.mo` | 30 | `length` | `(final min=Modelica.Constants.small, start=1)` |
| `Electrical/Analog/Lines/ULine.mo` | 23 | `length` | `(final min=Modelica.Constants.small, start=1)` |
| `Fluid/Examples/HeatExchanger.mo` | 104 | `length` | `(min=0)` |
| `Fluid/Examples/HeatExchanger.mo` | 141 | `s_wall` | `(min=0)` |
| `Fluid/Pipes.mo` | 238 | `perimeter` | `(min=0)` |
| `Mechanics/MultiBody/Joints/Assemblies/JointSSP.mo` | 30 | `rod1Length` | `(min=Modelica.Constants.eps, start = 1)` |
| `Mechanics/MultiBody/Joints/Assemblies/JointSSR.mo` | 30 | `rod1Length` | `(min=Modelica.Constants.eps, start = 1)` |
| `Mechanics/MultiBody/Joints/SphericalSpherical.mo` | 13 | `rodLength` | `( min=Modelica.Constants.eps, fixed=not computeRodLength, start = 1)` |
| `Mechanics/Translational/Components/ElastoGap.mo` | 10 | `s_ref` | `(min=Modelica.Constants.eps)` |
