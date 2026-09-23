# A zero-duration ramp is a supported step

Group `zero-duration-ramp` · 62 report instances · false-positives

The declaration explicitly says duration=0 gives a Step. Division by duration occurs only after time>=startTime and while time<startTime+duration. For duration=0 those conditions cannot both hold, so that branch is unreachable. The independent Ramp control also runs at zero. A Rumoca projection failure for a step is not evidence of a reachable division in this source.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-00002](../false-positives/FINDING-00002.md) | Modelica.Clocked.Examples.SimpleControlledDrive.ClockedWithDiscreteController | `ramp.duration` |
| [FINDING-00004](../false-positives/FINDING-00004.md) | Modelica.Clocked.Examples.SimpleControlledDrive.ClockedWithDiscreteTextbookController | `ramp.duration` |
| [FINDING-00006](../false-positives/FINDING-00006.md) | Modelica.Clocked.Examples.SimpleControlledDrive.Continuous | `ramp.duration` |
| [FINDING-00008](../false-positives/FINDING-00008.md) | Modelica.Clocked.Examples.SimpleControlledDrive.ExactlyClockedWithDiscreteController | `ramp.duration` |
| [FINDING-00023](../false-positives/FINDING-00023.md) | Modelica.ComplexBlocks.Examples.TestConversionBlock | `len.duration` |
| [FINDING-00024](../false-positives/FINDING-00024.md) | Modelica.ComplexBlocks.Examples.TestConversionBlock | `phi.duration` |
| [FINDING-00213](../false-positives/FINDING-00213.md) | Modelica.Electrical.Analog.Examples.DemoPowerSupply | `ramp.duration` |
| [FINDING-00235](../false-positives/FINDING-00235.md) | Modelica.Electrical.Analog.Examples.DifferenceAmplifier | `V2.signalSource.duration` |
| [FINDING-00236](../false-positives/FINDING-00236.md) | Modelica.Electrical.Analog.Examples.DifferenceAmplifier | `I1.signalSource.duration` |
| [FINDING-00278](../false-positives/FINDING-00278.md) | Modelica.Electrical.Analog.Examples.HeatingMOSInverter | `V.signalSource.duration` |
| [FINDING-00296](../false-positives/FINDING-00296.md) | Modelica.Electrical.Analog.Examples.HeatingNPN_NORGate | `V.signalSource.duration` |
| [FINDING-00328](../false-positives/FINDING-00328.md) | Modelica.Electrical.Analog.Examples.HeatingPNP_NORGate | `V.signalSource.duration` |
| [FINDING-00438](../false-positives/FINDING-00438.md) | Modelica.Electrical.Analog.Examples.Lines.CompareLineTrunks | `ramp.duration` |
| [FINDING-00758](../false-positives/FINDING-00758.md) | Modelica.Electrical.Analog.Examples.NandGate | `VDD.signalSource.duration` |
| [FINDING-00953](../false-positives/FINDING-00953.md) | Modelica.Electrical.Analog.Examples.ParallelResonance | `ramp.duration` |
| [FINDING-00990](../false-positives/FINDING-00990.md) | Modelica.Electrical.Analog.Examples.SeriesResonance | `ramp.duration` |
| [FINDING-01001](../false-positives/FINDING-01001.md) | Modelica.Electrical.Analog.Examples.ShowVariableResistor | `Ramp1.duration` |
| [FINDING-01337](../false-positives/FINDING-01337.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `ramp1.duration` |
| [FINDING-01338](../false-positives/FINDING-01338.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `ramp2.duration` |
| [FINDING-01745](../false-positives/FINDING-01745.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive | `ramp.duration` |
| [FINDING-02164](../false-positives/FINDING-02164.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `rampVoltage.signalSource.duration` |
| [FINDING-02228](../false-positives/FINDING-02228.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `rampCurrent.signalSource.duration` |
| [FINDING-02438](../false-positives/FINDING-02438.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad | `ramp.duration` |
| [FINDING-03000](../false-positives/FINDING-03000.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.Rectifier1Pulse.Thyristor1Pulse_R_Characteristic | `ramp.duration` |
| [FINDING-03096](../false-positives/FINDING-03096.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive | `ramp.duration` |
| [FINDING-03148](../false-positives/FINDING-03148.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_RLV_Characteristic | `ramp.duration` |
| [FINDING-03251](../false-positives/FINDING-03251.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_DC_Drive | `ramp.duration` |
| [FINDING-03283](../false-positives/FINDING-03283.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_RLV_Characteristic | `ramp.duration` |
| [FINDING-03369](../false-positives/FINDING-03369.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierCenterTap2mPulse.ThyristorCenterTap2mPulse_RLV_Characteristic | `ramp.duration` |
| [FINDING-03435](../false-positives/FINDING-03435.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierCenterTap2Pulse.ThyristorCenterTap2Pulse_RLV_Characteristic | `ramp.duration` |
| [FINDING-03489](../false-positives/FINDING-03489.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierCenterTapmPulse.ThyristorCenterTapmPulse_RLV_Characteristic | `ramp.duration` |
| [FINDING-03583](../false-positives/FINDING-03583.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.ChopperStepDown.ChopperStepDown_RL | `vRef.duration` |
| [FINDING-03599](../false-positives/FINDING-03599.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.ChopperStepDown.ChopperStepDown_R | `vRef.duration` |
| [FINDING-03615](../false-positives/FINDING-03615.md) | Modelica.Electrical.PowerConverters.Examples.DCDC.ChopperStepUp.ChopperStepUp_R | `vRef.duration` |
| [FINDING-03731](../false-positives/FINDING-03731.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.QuadraticCoreAirgap | `rampCurrent.signalSource.duration` |
| [FINDING-03748](../false-positives/FINDING-03748.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.ToroidalCoreAirgap | `rampCurrent.signalSource.duration` |
| [FINDING-03759](../false-positives/FINDING-03759.md) | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.ToroidalCoreQuadraticCrossSection | `rampCurrent.signalSource.duration` |
| [FINDING-04386](../false-positives/FINDING-04386.md) | Modelica.Mechanics.Rotational.Examples.EddyCurrentBrake | `ramp.duration` |
| [FINDING-04392](../false-positives/FINDING-04392.md) | Modelica.Mechanics.Rotational.Examples.ElasticBearing | `ramp.duration` |
| [FINDING-04434](../false-positives/FINDING-04434.md) | Modelica.Mechanics.Translational.Examples.EddyCurrentBrake | `ramp.duration` |
| [FINDING-04628](../false-positives/FINDING-04628.md) | Modelica.Thermal.FluidHeatFlow.Examples.PumpAndValve | `speedRamp.duration` |
| [FINDING-04629](../false-positives/FINDING-04629.md) | Modelica.Thermal.FluidHeatFlow.Examples.PumpAndValve | `valveRamp.duration` |
| [FINDING-04754](../false-positives/FINDING-04754.md) | Modelica.Thermal.HeatTransfer.Examples.ControlledTemperature | `ramp.duration` |
| [FINDING-04779](../false-positives/FINDING-04779.md) | ModelicaTest.Blocks.Continuous | `ramp.duration` |
| [FINDING-04780](../false-positives/FINDING-04780.md) | ModelicaTest.Blocks.Continuous | `ramp1.duration` |
| [FINDING-04792](../false-positives/FINDING-04792.md) | ModelicaTest.Blocks.Continuous_SteadyState | `ramp.duration` |
| [FINDING-04793](../false-positives/FINDING-04793.md) | ModelicaTest.Blocks.Continuous_SteadyState | `ramp1.duration` |
| [FINDING-04805](../false-positives/FINDING-04805.md) | ModelicaTest.Blocks.Continuous_InitialState | `ramp.duration` |
| [FINDING-04806](../false-positives/FINDING-04806.md) | ModelicaTest.Blocks.Continuous_InitialState | `ramp1.duration` |
| [FINDING-04820](../false-positives/FINDING-04820.md) | ModelicaTest.Blocks.LimitersHomotopy | `ramp1.duration` |
| [FINDING-04823](../false-positives/FINDING-04823.md) | ModelicaTest.Blocks.LimitersHomotopy | `ramp2.duration` |
| [FINDING-04826](../false-positives/FINDING-04826.md) | ModelicaTest.Blocks.LimitersHomotopy | `ramp3.duration` |
| [FINDING-04829](../false-positives/FINDING-04829.md) | ModelicaTest.Blocks.LimitersHomotopy | `ramp4.duration` |
| [FINDING-04832](../false-positives/FINDING-04832.md) | ModelicaTest.Blocks.LimitersHomotopy | `ramp5.duration` |
| [FINDING-04835](../false-positives/FINDING-04835.md) | ModelicaTest.Blocks.LimitersHomotopy | `ramp6.duration` |
| [FINDING-04852](../false-positives/FINDING-04852.md) | ModelicaTest.Blocks.Exponentiation | `negativeToPositiveRamp.duration` |
| [FINDING-04853](../false-positives/FINDING-04853.md) | ModelicaTest.Blocks.ZeroThresholds | `ramp.duration` |
| [FINDING-04979](../false-positives/FINDING-04979.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `ramp.duration` |
| [FINDING-04980](../false-positives/FINDING-04980.md) | ModelicaTest.Magnetic.FluxTubes.Sources | `ramp1.duration` |
| [FINDING-04994](../false-positives/FINDING-04994.md) | ModelicaTest.Magnetic.FluxTubes.Sensors | `ramp.duration` |
| [FINDING-04995](../false-positives/FINDING-04995.md) | ModelicaTest.Magnetic.FluxTubes.VariableComponents | `rampPermeance.duration` |
| [FINDING-04996](../false-positives/FINDING-04996.md) | ModelicaTest.Magnetic.FluxTubes.VariableComponents | `rampReluctance.duration` |
