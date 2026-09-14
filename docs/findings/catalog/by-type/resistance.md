# `SI.Resistance` — 281 unbounded declarations

Domain: electrical

`Units.mo` declares `type Resistance` with **no `min`**, so every
declaration below accepts a negative value.

## Exposed

| File | Line | Parameter | Declared modifiers |
|---|---|---|---|
| `Electrical/Analog/Basic/CCV.mo` | 5 | `transResistance` | `(start=1)` |
| `Electrical/Analog/Basic/OpAmpDetailed.mo` | 5 | `Rdm` | `—` |
| `Electrical/Analog/Basic/OpAmpDetailed.mo` | 7 | `Rcm` | `—` |
| `Electrical/Analog/Basic/OpAmpDetailed.mo` | 23 | `Rout` | `—` |
| `Electrical/Analog/Basic/Potentiometer.mo` | 3 | `R` | `(start=1)` |
| `Electrical/Analog/Basic/Resistor.mo` | 3 | `R` | `(start=1)` |
| `Electrical/Analog/Examples/CompareTransformers.mo` | 11 | `R1` | `—` |
| `Electrical/Analog/Examples/CompareTransformers.mo` | 19 | `R2` | `—` |
| `Electrical/Analog/Examples/CompareTransformers.mo` | 21 | `RL` | `—` |
| `Electrical/Analog/Examples/InvertingAmp.mo` | 9 | `R1` | `—` |
| `Electrical/Analog/Examples/InvertingAmp.mo` | 10 | `R2` | `—` |
| `Electrical/Analog/Examples/Lines/CompareLineTrunks.mo` | 6 | `Rload` | `—` |
| `Electrical/Analog/Examples/Lines/LightningLosslessTransmissionLine.mo` | 7 | `Rload` | `—` |
| `Electrical/Analog/Examples/Lines/LightningSegmentedTransmissionLine.mo` | 7 | `Rload` | `—` |
| `Electrical/Analog/Examples/Lines/SmoothStep.mo` | 6 | `Rload` | `—` |
| `Electrical/Analog/Examples/OpAmps/Comparator.mo` | 10 | `R` | `—` |
| `Electrical/Analog/Examples/OpAmps/InvertingSchmittTrigger.mo` | 10 | `R1` | `—` |
| `Electrical/Analog/Examples/OpAmps/InvertingSchmittTrigger.mo` | 11 | `R2` | `—` |
| `Electrical/Analog/Examples/OpAmps/LCOscillator.mo` | 10 | `R` | `—` |
| `Electrical/Analog/Examples/OpAmps/LCOscillator.mo` | 11 | `R1` | `—` |
| `Electrical/Analog/Examples/OpAmps/LCOscillator.mo` | 12 | `R2` | `—` |
| `Electrical/Analog/Examples/OpAmps/Multivibrator.mo` | 7 | `R1` | `—` |
| `Electrical/Analog/Examples/OpAmps/Multivibrator.mo` | 8 | `R2` | `—` |
| `Electrical/Analog/Examples/OpAmps/Multivibrator.mo` | 9 | `R` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Add.mo` | 8 | `R` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Add.mo` | 9 | `R1` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Add.mo` | 10 | `R2` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Buffer.mo` | 5 | `R1` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Buffer.mo` | 6 | `R2` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Der.mo` | 7 | `R` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Derivative.mo` | 6 | `R1` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Derivative.mo` | 7 | `R2` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/DifferentialAmplifierData.mo` | 8 | `RLoad` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/DifferentialAmplifierData.mo` | 10 | `RGround` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/DifferentialAmplifierData.mo` | 18 | `R1` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/DifferentialAmplifierData.mo` | 20 | `R2` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/DifferentialAmplifierData.mo` | 22 | `R3` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/DifferentialAmplifierData.mo` | 24 | `R4` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/DifferentialAmplifierData.mo` | 26 | `RInstrument` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Feedback.mo` | 7 | `R1` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Feedback.mo` | 8 | `R3` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/FirstOrder.mo` | 6 | `R1` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/FirstOrder.mo` | 7 | `R2` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Gain.mo` | 5 | `R1` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Gain.mo` | 6 | `R2` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Integrator.mo` | 7 | `R` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/PI.mo` | 6 | `R1` | `—` |
| `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/PI.mo` | 7 | `R2` | `—` |
| `Electrical/Analog/Examples/OpAmps/SchmittTrigger.mo` | 10 | `R1` | `—` |
| `Electrical/Analog/Examples/OpAmps/SchmittTrigger.mo` | 11 | `R2` | `—` |
| `Electrical/Analog/Examples/OpAmps/SignalGenerator.mo` | 8 | `R1` | `—` |
| `Electrical/Analog/Examples/OpAmps/SignalGenerator.mo` | 9 | `R2` | `—` |
| `Electrical/Analog/Examples/OpAmps/SignalGenerator.mo` | 11 | `R` | `—` |
| `Electrical/Analog/Examples/OpAmps/VoltageFollower.mo` | 8 | `Ri` | `—` |
| `Electrical/Analog/Examples/OpAmps/VoltageFollower.mo` | 10 | `Rl` | `—` |
| `Electrical/Analog/Examples/Rectifier.mo` | 8 | `Ron` | `—` |
| `Electrical/Analog/Examples/Utilities/Resistor.mo` | 4 | `R` | `—` |
| `Electrical/Analog/Examples/Utilities/SwitchedCapacitor.mo` | 5 | `R` | `(start=1)` |
| `Electrical/Analog/Ideal/AD_Converter.mo` | 27 | `Rin` | `(start=10^6)` |
| `Electrical/Analog/Ideal/IdealTriac.mo` | 11 | `Rdis` | `—` |
| `Electrical/Analog/Interfaces/IdealSwitchWithArc.mo` | 4 | `Ron` | `—` |
| `Electrical/Analog/Lines/OLine.mo` | 72 | `rm` | `—` |
| `Electrical/Analog/Lines/TLine.mo` | 5 | `Z0` | `(start=1)` |
| `Electrical/Analog/Lines/TLine1.mo` | 6 | `Z0` | `(start=1)` |
| `Electrical/Analog/Lines/TLine2.mo` | 6 | `Z0` | `(start=1)` |
| `Electrical/Analog/Lines/TLine3.mo` | 6 | `Z0` | `(start=1)` |
| `Electrical/Analog/Lines/ULine.mo` | 48 | `rm` | `—` |
| `Electrical/Analog/Semiconductors/Diode.mo` | 8 | `R` | `—` |
| `Electrical/Analog/Semiconductors/Diode2.mo` | 7 | `Rs` | `—` |
| `Electrical/Analog/Semiconductors/NMOS.mo` | 20 | `RDS` | `—` |
| `Electrical/Analog/Semiconductors/PMOS.mo` | 20 | `RDS` | `—` |
| `Electrical/Analog/Semiconductors/Thyristor.mo` | 38 | `Ron` | `—` |
| `Electrical/Analog/Semiconductors/Thyristor.mo` | 40 | `Roff` | `—` |
| `Electrical/Analog/Semiconductors/ZDiode.mo` | 8 | `R` | `—` |
| `Electrical/Batteries/BatteryStacks/SuperCap.mo` | 9 | `Rs` | `—` |
| `Electrical/Batteries/ParameterRecords/CellData.mo` | 26 | `Ri` | `—` |
| `Electrical/Batteries/ParameterRecords/CellData.mo` | 31 | `R0` | `—` |
| `Electrical/Batteries/ParameterRecords/TransientData/RCData.mo` | 5 | `R` | `—` |
| `Electrical/Machines/BasicMachines/Components/DamperCage.mo` | 7 | `Rrd` | `—` |
| `Electrical/Machines/BasicMachines/Components/DamperCage.mo` | 9 | `Rrq` | `—` |
| `Electrical/Machines/BasicMachines/Components/SquirrelCage.mo` | 5 | `Rr` | `—` |
| `Electrical/Machines/BasicMachines/DCMachines/DC_ElectricalExcited.mo` | 24 | `Re` | `(start=100)` |
| `Electrical/Machines/BasicMachines/DCMachines/DC_SeriesExcited.mo` | 26 | `Re` | `(start=0.01)` |
| `Electrical/Machines/BasicMachines/InductionMachines/IM_SlipRing.mo` | 37 | `Rr` | `(start=0.04*ZsRef)` |
| `Electrical/Machines/BasicMachines/InductionMachines/IM_SquirrelCage.mo` | 33 | `Rr` | `(start=0.04*ZsRef)` |
| `Electrical/Machines/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo` | 68 | `Rrd` | `(start=0.04*ZsRef)` |
| `Electrical/Machines/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo` | 73 | `Rrq` | `—` |
| `Electrical/Machines/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo` | 96 | `Re` | `(start=2.5)` |
| `Electrical/Machines/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo` | 70 | `Rrd` | `(start=0.04*ZsRef)` |
| `Electrical/Machines/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo` | 75 | `Rrq` | `—` |
| `Electrical/Machines/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo` | 62 | `Rrd` | `(start=0.04*ZsRef)` |
| `Electrical/Machines/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo` | 67 | `Rrq` | `—` |
| `Electrical/Machines/Examples/ControlledDCDrives/Utilities/DcdcInverter.mo` | 10 | `RonT` | `—` |
| `Electrical/Machines/Examples/ControlledDCDrives/Utilities/DcdcInverter.mo` | 19 | `RonD` | `—` |
| `Electrical/Machines/Examples/ControlledDCDrives/Utilities/DriveDataDCPM.mo` | 11 | `Ra` | `—` |
| `Electrical/Machines/Examples/ControlledDCDrives/Utilities/SwitchingDcDc.mo` | 5 | `RonT` | `—` |
| `Electrical/Machines/Examples/ControlledDCDrives/Utilities/SwitchingDcDc.mo` | 11 | `RonD` | `—` |
| `Electrical/Machines/Examples/DCMachines/DCPM_CurrentControlled.mo` | 8 | `Ra` | `—` |
| `Electrical/Machines/Examples/DCMachines/DCPM_CurrentControlled.mo` | 16 | `k` | `—` |
| `Electrical/Machines/Examples/InductionMachines/IMC_InverterDrive.mo` | 11 | `RGrid` | `—` |
| `Electrical/Machines/Examples/InductionMachines/IMC_YDarc.mo` | 9 | `RLine` | `—` |
| `Electrical/Machines/Examples/InductionMachines/IMS_Start.mo` | 9 | `Rstart` | `—` |
| `Electrical/Machines/Examples/SynchronousMachines/SMEE_LoadDump.mo` | 14 | `RLoad` | `—` |
| `Electrical/Machines/Examples/SynchronousMachines/SMEE_Rectifier.mo` | 11 | `RLoad` | `—` |
| `Electrical/Machines/Examples/SynchronousMachines/SMPM_Braking.mo` | 8 | `R` | `—` |
| `Electrical/Machines/Examples/Transformers/AsymmetricalLoad.mo` | 4 | `RL` | `—` |
| `Electrical/Machines/Examples/Transformers/Rectifier6pulse.mo` | 8 | `RL` | `—` |
| `Electrical/Machines/Examples/Transformers/TransformerTestbench.mo` | 4 | `RL` | `—` |
| `Electrical/Machines/Interfaces/PartialBasicDCMachine.mo` | 17 | `Ra` | `(start=0.05)` |
| `Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo` | 11 | `Rs` | `(start=0.03*ZsRef)` |
| `Electrical/Machines/Interfaces/PartialBasicTransformer.mo` | 9 | `R1` | `(start=5E-3/(if C1 == "D" then 1 else 3)` |
| `Electrical/Machines/Interfaces/PartialBasicTransformer.mo` | 21 | `R2` | `(start=5E-3/(if C2 == "d" then 1 else 3)` |
| `Electrical/Machines/Utilities/DQCurrentController.mo` | 11 | `Rs` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/DcElectricalExcitedData.mo` | 6 | `Re` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/DcPermanentMagnetData.mo` | 19 | `Ra` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/DcSeriesExcitedData.mo` | 5 | `Re` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/IM_SlipRingData.mo` | 19 | `Rr` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/IM_SquirrelCageData.mo` | 13 | `Rr` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo` | 10 | `Rs` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/SM_ElectricalExcitedData.mo` | 13 | `Re` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/SM_ReluctanceRotorData.mo` | 25 | `Rrd` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/SM_ReluctanceRotorData.mo` | 30 | `Rrq` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/TransformerData.mo` | 17 | `R1` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/TransformerData.mo` | 29 | `R2` | `—` |
| `Electrical/Machines/Utilities/RampedRheostat.mo` | 10 | `RStart` | `—` |
| `Electrical/Machines/Utilities/SwitchYD.mo` | 4 | `Ron` | `—` |
| `Electrical/Machines/Utilities/SwitchYDwithArc.mo` | 4 | `Ron` | `—` |
| `Electrical/Machines/Utilities/SwitchedRheostat.mo` | 10 | `RStart` | `—` |
| `Electrical/Machines/Utilities/SynchronousMachineData.mo` | 88 | `Rs` | `—` |
| `Electrical/Machines/Utilities/SynchronousMachineData.mo` | 113 | `Rrd` | `—` |
| `Electrical/Machines/Utilities/SynchronousMachineData.mo` | 120 | `Rrq` | `—` |
| `Electrical/Machines/Utilities/SynchronousMachineData.mo` | 127 | `Re` | `—` |
| `Electrical/Machines/Utilities/TransformerData.mo` | 37 | `R1` | `—` |
| `Electrical/Machines/Utilities/TransformerData.mo` | 45 | `R2` | `—` |
| `Electrical/Polyphase/Basic/MultiStarResistance.mo` | 6 | `R` | `—` |
| `Electrical/Polyphase/Basic/Resistor.mo` | 4 | `R` | `(start=fill(1, m)` |
| `Electrical/Polyphase/Examples/Rectifier.mo` | 9 | `RL` | `—` |
| `Electrical/Polyphase/Examples/Rectifier.mo` | 11 | `RE` | `—` |
| `Electrical/Polyphase/Examples/Rectifier.mo` | 12 | `Ron` | `—` |
| `Electrical/Polyphase/Examples/TestSensors.mo` | 9 | `R` | `—` |
| `Electrical/Polyphase/Examples/TransformerYD.mo` | 10 | `RT` | `—` |
| `Electrical/Polyphase/Examples/TransformerYD.mo` | 11 | `RL` | `—` |
| `Electrical/Polyphase/Examples/TransformerYY.mo` | 10 | `RT` | `—` |
| `Electrical/Polyphase/Examples/TransformerYY.mo` | 11 | `RL` | `—` |
| `Electrical/Polyphase/Examples/Utilities/PolyphaseRectifierData.mo` | 20 | `RLoad` | `—` |
| `Electrical/Polyphase/Examples/Utilities/PolyphaseRectifierData.mo` | 21 | `RDC` | `—` |
| `Electrical/Polyphase/Examples/Utilities/PolyphaseRectifierData.mo` | 23 | `RGnd` | `—` |
| `Electrical/PowerConverters/DCAC/Polyphase2Level.mo` | 5 | `RonTransistor` | `—` |
| `Electrical/PowerConverters/DCAC/Polyphase2Level.mo` | 11 | `RonDiode` | `—` |
| `Electrical/PowerConverters/DCAC/SinglePhase2Level.mo` | 4 | `RonTransistor` | `—` |
| `Electrical/PowerConverters/DCAC/SinglePhase2Level.mo` | 10 | `RonDiode` | `—` |
| `Electrical/PowerConverters/DCDC/ChopperBuckBoost.mo` | 6 | `RonTransistor` | `—` |
| `Electrical/PowerConverters/DCDC/ChopperBuckBoost.mo` | 12 | `RonDiode` | `—` |
| `Electrical/PowerConverters/DCDC/ChopperStepDown.mo` | 5 | `RonTransistor` | `—` |
| `Electrical/PowerConverters/DCDC/ChopperStepUp.mo` | 5 | `RonTransistor` | `—` |
| `Electrical/PowerConverters/DCDC/HBridge.mo` | 8 | `RonTransistor` | `—` |
| `Electrical/PowerConverters/DCDC/HBridge.mo` | 14 | `RonDiode` | `—` |
| `Electrical/PowerConverters/Examples/ACAC/ExampleTemplates/Dimmer.mo` | 10 | `RLoad` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/Rectifier1Pulse/Thyristor1Pulse_R.mo` | 12 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/Rectifier1Pulse/Thyristor1Pulse_R_Characteristic.mo` | 8 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2Pulse/DiodeBridge2Pulse.mo` | 8 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2Pulse/HalfControlledBridge2Pulse.mo` | 10 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2Pulse/ThyristorBridge2Pulse_DC_Drive.mo` | 14 | `RMains` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2Pulse/ThyristorBridge2Pulse_R.mo` | 10 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2Pulse/ThyristorBridge2Pulse_RL.mo` | 10 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2Pulse/ThyristorBridge2Pulse_RLV.mo` | 10 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2Pulse/ThyristorBridge2Pulse_RLV_Characteristic.mo` | 10 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/DiodeBridge2mPulse.mo` | 9 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/HalfControlledBridge2mPulse.mo` | 11 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/ThyristorBridge2mPulse_DC_Drive.mo` | 16 | `RMains` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/ThyristorBridge2mPulse_R.mo` | 10 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/ThyristorBridge2mPulse_RL.mo` | 11 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/ThyristorBridge2mPulse_RLV.mo` | 10 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/ThyristorBridge2mPulse_RLV_Characteristic.mo` | 11 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTap2Pulse/DiodeCenterTap2Pulse.mo` | 8 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTap2Pulse/ThyristorCenterTap2Pulse_R.mo` | 10 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTap2Pulse/ThyristorCenterTap2Pulse_RL.mo` | 10 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTap2Pulse/ThyristorCenterTap2Pulse_RLV.mo` | 10 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTap2Pulse/ThyristorCenterTap2Pulse_RLV_Characteristic.mo` | 8 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTap2mPulse/DiodeCenterTap2mPulse.mo` | 9 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTap2mPulse/ThyristorCenterTap2mPulse_R.mo` | 10 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTap2mPulse/ThyristorCenterTap2mPulse_RL.mo` | 10 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTap2mPulse/ThyristorCenterTap2mPulse_RLV.mo` | 10 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTap2mPulse/ThyristorCenterTap2mPulse_RLV_Characteristic.mo` | 8 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTapmPulse/DiodeCenterTapmPulse.mo` | 9 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTapmPulse/ThyristorCenterTapmPulse_R.mo` | 10 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTapmPulse/ThyristorCenterTapmPulse_RL.mo` | 10 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTapmPulse/ThyristorCenterTapmPulse_RLV.mo` | 10 | `R` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTapmPulse/ThyristorCenterTapmPulse_RLV_Characteristic.mo` | 8 | `R` | `—` |
| `Electrical/PowerConverters/Examples/DCAC/PolyphaseTwoLevel/PolyphaseTwoLevel_R.mo` | 8 | `R` | `—` |
| `Electrical/PowerConverters/Examples/DCAC/PolyphaseTwoLevel/PolyphaseTwoLevel_RL.mo` | 9 | `R` | `—` |
| `Electrical/PowerConverters/Examples/DCAC/SinglePhaseTwoLevel/SinglePhaseTwoLevel_R.mo` | 9 | `R` | `—` |
| `Electrical/PowerConverters/Examples/DCAC/SinglePhaseTwoLevel/SinglePhaseTwoLevel_RL.mo` | 9 | `R` | `—` |
| `Electrical/PowerConverters/Examples/DCDC/ExampleTemplates/ChopperBuckBoost.mo` | 5 | `RiLV` | `—` |
| `Electrical/PowerConverters/Examples/DCDC/ExampleTemplates/ChopperBuckBoost.mo` | 7 | `RiHV` | `—` |
| `Electrical/PowerConverters/Examples/DCDC/ExampleTemplates/ChopperBuckBoost.mo` | 11 | `R` | `—` |
| `Electrical/PowerConverters/Examples/DCDC/ExampleTemplates/ChopperStepDown.mo` | 10 | `RLoad` | `—` |
| `Electrical/PowerConverters/Examples/DCDC/ExampleTemplates/ChopperStepUp.mo` | 10 | `RLoad` | `—` |
| `Electrical/PowerConverters/Examples/DCDC/HBridge/HBridge_R.mo` | 5 | `R` | `—` |
| `Electrical/PowerConverters/Examples/DCDC/HBridge/HBridge_RL.mo` | 5 | `R` | `—` |
| `Electrical/PowerConverters/Examples/DCDC/HBridge/HBridge_TrianglePWM_RL.mo` | 5 | `R` | `—` |
| `Electrical/QuasiStatic/Machines/Examples/TransformerTestbench.mo` | 5 | `RL` | `—` |
| `Electrical/QuasiStatic/Machines/Interfaces/PartialBasicTransformer.mo` | 9 | `R1` | `(start=5E-3/(if C1 == "D" then 1 else 3)` |
| `Electrical/QuasiStatic/Machines/Interfaces/PartialBasicTransformer.mo` | 23 | `R2` | `(start=5E-3/(if C2 == "d" then 1 else 3)` |
| `Electrical/QuasiStatic/Polyphase/Basic/MultiStarResistance.mo` | 7 | `R` | `—` |
| `Electrical/QuasiStatic/Polyphase/Basic/Resistor.mo` | 4 | `R_ref` | `(start=fill(1, m)` |
| `Electrical/QuasiStatic/Polyphase/Examples/BalancingDelta.mo` | 7 | `R` | `—` |
| `Electrical/QuasiStatic/Polyphase/Examples/BalancingStar.mo` | 7 | `R` | `—` |
| `Electrical/QuasiStatic/Polyphase/Examples/TestSensors.mo` | 9 | `R` | `—` |
| `Electrical/QuasiStatic/SinglePhase/Basic/Impedance.mo` | 18 | `R_ref` | `—` |
| `Electrical/QuasiStatic/SinglePhase/Basic/Resistor.mo` | 6 | `R_ref` | `(start=1)` |
| `Electrical/QuasiStatic/SinglePhase/Examples/MultipleResonance.mo` | 15 | `R` | `—` |
| `Electrical/Spice3.mo` | 2269 | `R` | `(start=1000)` |
| `Electrical/Spice3.mo` | 2571 | `transResistance` | `(start=0)` |
| `Electrical/Spice3.mo` | 4599 | `RD` | `—` |
| `Electrical/Spice3.mo` | 4600 | `RS` | `—` |
| `Electrical/Spice3.mo` | 4613 | `RSH` | `—` |
| `Electrical/Spice3.mo` | 5024 | `RE` | `—` |
| `Electrical/Spice3.mo` | 5025 | `RC` | `—` |
| `Electrical/Spice3.mo` | 5027 | `RB` | `—` |
| `Electrical/Spice3.mo` | 5028 | `RBM` | `—` |
| `Electrical/Spice3.mo` | 5192 | `RD` | `—` |
| `Electrical/Spice3.mo` | 5193 | `RS` | `—` |
| `Electrical/Spice3.mo` | 5305 | `RS` | `—` |
| `Electrical/Spice3.mo` | 5328 | `R` | `—` |
| `Electrical/Spice3.mo` | 5397 | `RSH` | `—` |
| `Magnetic/FluxTubes/Basic/EddyCurrent.mo` | 23 | `R` | `—` |
| `Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/ConstantActuator.mo` | 6 | `R` | `—` |
| `Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/PermeanceActuator.mo` | 8 | `R` | `—` |
| `Magnetic/FluxTubes/Examples/SolenoidActuator/Components/AdvancedSolenoid.mo` | 8 | `R` | `—` |
| `Magnetic/FluxTubes/Examples/SolenoidActuator/Components/AdvancedSolenoid.mo` | 9 | `R_par` | `—` |
| `Magnetic/FluxTubes/Examples/SolenoidActuator/Components/SimpleSolenoid.mo` | 5 | `R` | `—` |
| `Magnetic/FluxTubes/Examples/Utilities/CoilDesign.mo` | 41 | `R_calculated` | `—` |
| `Magnetic/FluxTubes/Examples/Utilities/CoilDesign.mo` | 58 | `R_actual` | `—` |
| `Magnetic/FundamentalWave/BaseClasses/Machine.mo` | 21 | `Rs` | `(start=ZsRef*0.03)` |
| `Magnetic/FundamentalWave/BasicMachines/Components/SinglePhaseWinding.mo` | 24 | `RRef` | `—` |
| `Magnetic/FundamentalWave/BasicMachines/Components/SymmetricPolyphaseCageWinding.mo` | 8 | `RRef` | `—` |
| `Magnetic/FundamentalWave/BasicMachines/Components/SymmetricPolyphaseWinding.mo` | 27 | `RRef` | `—` |
| `Magnetic/FundamentalWave/BasicMachines/InductionMachines/IM_SlipRing.mo` | 48 | `Rr` | `(start=0.04*ZsRef)` |
| `Magnetic/FundamentalWave/BasicMachines/InductionMachines/IM_SquirrelCage.mo` | 31 | `Rr` | `(start=0.04*ZsRef)` |
| `Magnetic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo` | 55 | `Rrd` | `(start=0.04*ZsRef)` |
| `Magnetic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo` | 60 | `Rrq` | `—` |
| `Magnetic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo` | 93 | `Re` | `(start=2.5)` |
| `Magnetic/FundamentalWave/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo` | 53 | `Rrd` | `(start=0.04*ZsRef)` |
| `Magnetic/FundamentalWave/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo` | 58 | `Rrq` | `—` |
| `Magnetic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo` | 52 | `Rrd` | `(start=0.04*ZsRef)` |
| `Magnetic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo` | 57 | `Rrq` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/InductionMachines/ComparisonPolyphase/IMS_Start_Polyphase.mo` | 14 | `RStart` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/InductionMachines/IMS_Start.mo` | 10 | `RStart` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/ComparisonPolyphase/SMEE_Generator_Polyphase.mo` | 19 | `Rs` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/ComparisonPolyphase/SMEE_Generator_Polyphase.mo` | 32 | `Rrd` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/ComparisonPolyphase/SMEE_Generator_Polyphase.mo` | 34 | `Rrq` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/SMEE_Generator.mo` | 17 | `Rs` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/SMEE_Generator.mo` | 30 | `Rrd` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/SMEE_Generator.mo` | 32 | `Rrq` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/SMEE_LoadDump.mo` | 15 | `RLoad` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/SMEE_Rectifier.mo` | 12 | `RLoad` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/SMPM_Braking.mo` | 8 | `R` | `—` |
| `Magnetic/FundamentalWave/Examples/Components/EddyCurrentLosses.mo` | 6 | `R` | `—` |
| `Magnetic/FundamentalWave/Examples/Components/PolyphaseInductance.mo` | 7 | `R` | `—` |
| `Magnetic/FundamentalWave/Examples/Components/SinglePhaseInductance.mo` | 6 | `R` | `—` |
| `Magnetic/QuasiStatic/FluxTubes/Basic/EddyCurrent.mo` | 22 | `R` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/BaseClasses/Machine.mo` | 21 | `Rs` | `(start=0.03)` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/Components/QuasiStaticAnalogWinding.mo` | 22 | `RRef` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/Components/SymmetricPolyphaseCageWinding.mo` | 9 | `RRef` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/Components/SymmetricPolyphaseWinding.mo` | 26 | `RRef` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/InductionMachines/IM_SlipRing.mo` | 41 | `Rr` | `(start=0.04*ZsRef)` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/InductionMachines/IM_SquirrelCage.mo` | 30 | `Rr` | `(start=0.04*ZsRef)` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo` | 54 | `Rrd` | `(start=0.04*ZsRef)` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo` | 59 | `Rrq` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo` | 92 | `Re` | `(start=2.5)` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo` | 52 | `Rrd` | `(start=0.04*ZsRef)` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo` | 57 | `Rrq` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo` | 48 | `Rrd` | `(start=0.04*ZsRef)` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo` | 53 | `Rrq` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/Examples/BasicMachines/InductionMachines/IMS_Characteristics.mo` | 10 | `Rr` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/Examples/BasicMachines/InductionMachines/IMS_Start.mo` | 11 | `RStart` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/Examples/Components/EddyCurrentLosses.mo` | 7 | `R` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/Examples/Components/PolyphaseInductance.mo` | 7 | `R` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/Utilities/SwitchYD.mo` | 4 | `Ron` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/Utilities/SwitchedRheostat.mo` | 10 | `RStart` | `—` |

## Guarded — these add their own bound

Same library, same quantity, bound written. This is why the exposed
cases read as omissions rather than as a deliberate choice.

| File | Line | Parameter | Declared modifiers |
|---|---|---|---|
| `Electrical/Analog/Ideal/ControlledIdealIntermediateSwitch.mo` | 5 | `Ron` | `(final min=0)` |
| `Electrical/Analog/Ideal/ControlledIdealTwoWaySwitch.mo` | 4 | `Ron` | `(final min=0)` |
| `Electrical/Analog/Ideal/IdealIntermediateSwitch.mo` | 3 | `Ron` | `(final min=0)` |
| `Electrical/Analog/Ideal/IdealTriac.mo` | 4 | `Ron` | `(final min=0)` |
| `Electrical/Analog/Ideal/IdealTwoWaySwitch.mo` | 3 | `Ron` | `(final min=0)` |
| `Electrical/Analog/Interfaces/IdealSemiconductor.mo` | 4 | `Ron` | `(final min=0)` |
| `Electrical/Analog/Interfaces/IdealSwitch.mo` | 4 | `Ron` | `(final min=0)` |
| `Electrical/Analog/Sources/DCPowerSupply.mo` | 7 | `Rcv` | `(final min = eps)` |
| `Electrical/Polyphase/Ideal/CloserWithArc.mo` | 4 | `Ron` | `(final min=zeros(m)` |
| `Electrical/Polyphase/Ideal/IdealClosingSwitch.mo` | 4 | `Ron` | `(final min=zeros(m)` |
| `Electrical/Polyphase/Ideal/IdealCommutingSwitch.mo` | 4 | `Ron` | `(final min=zeros(m)` |
| `Electrical/Polyphase/Ideal/IdealDiode.mo` | 4 | `Ron` | `(final min=zeros(m)` |
| `Electrical/Polyphase/Ideal/IdealGTOThyristor.mo` | 4 | `Ron` | `(final min=zeros(m)` |
| `Electrical/Polyphase/Ideal/IdealIntermediateSwitch.mo` | 4 | `Ron` | `(final min=zeros(m)` |
| `Electrical/Polyphase/Ideal/IdealOpeningSwitch.mo` | 4 | `Ron` | `(final min=zeros(m)` |
| `Electrical/Polyphase/Ideal/IdealThyristor.mo` | 4 | `Ron` | `(final min=zeros(m)` |
| `Electrical/Polyphase/Ideal/OpenerWithArc.mo` | 4 | `Ron` | `(final min=zeros(m)` |
| `Electrical/PowerConverters/ACAC/PolyphaseTriac.mo` | 4 | `Ron` | `(final min=0)` |
| `Electrical/PowerConverters/ACAC/SinglePhaseTriac.mo` | 5 | `Ron` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/DiodeBridge2Pulse.mo` | 5 | `RonDiode` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/DiodeBridge2mPulse.mo` | 6 | `RonDiode` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/DiodeCenterTap2Pulse.mo` | 5 | `RonDiode` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/DiodeCenterTap2mPulse.mo` | 6 | `RonDiode` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/DiodeCenterTapmPulse.mo` | 6 | `RonDiode` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/HalfControlledBridge2Pulse.mo` | 6 | `RonDiode` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/HalfControlledBridge2Pulse.mo` | 12 | `RonThyristor` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/HalfControlledBridge2mPulse.mo` | 7 | `RonDiode` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/HalfControlledBridge2mPulse.mo` | 13 | `RonThyristor` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/ThyristorBridge2Pulse.mo` | 5 | `RonThyristor` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/ThyristorBridge2mPulse.mo` | 6 | `RonThyristor` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/ThyristorCenterTap2Pulse.mo` | 6 | `RonThyristor` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/ThyristorCenterTap2mPulse.mo` | 7 | `RonThyristor` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/ThyristorCenterTapmPulse.mo` | 7 | `RonThyristor` | `(final min=0)` |
| `Electrical/PowerConverters/DCDC/ChopperStepDown.mo` | 11 | `RonDiode` | `(final min=0)` |
| `Electrical/PowerConverters/DCDC/ChopperStepUp.mo` | 11 | `RonDiode` | `(final min=0)` |
| `Electrical/QuasiStatic/Polyphase/Ideal/IdealClosingSwitch.mo` | 4 | `Ron` | `(final min=zeros(m)` |
| `Electrical/QuasiStatic/Polyphase/Ideal/IdealCommutingSwitch.mo` | 4 | `Ron` | `(final min=zeros(m)` |
| `Electrical/QuasiStatic/Polyphase/Ideal/IdealIntermediateSwitch.mo` | 4 | `Ron` | `(final min=zeros(m)` |
| `Electrical/QuasiStatic/Polyphase/Ideal/IdealOpeningSwitch.mo` | 4 | `Ron` | `(final min=zeros(m)` |
| `Electrical/QuasiStatic/SinglePhase/Ideal/IdealClosingSwitch.mo` | 6 | `Ron` | `(final min=0)` |
| `Electrical/QuasiStatic/SinglePhase/Ideal/IdealCommutingSwitch.mo` | 5 | `Ron` | `(final min=0)` |
| `Electrical/QuasiStatic/SinglePhase/Ideal/IdealIntermediateSwitch.mo` | 5 | `Ron` | `(final min=0)` |
| `Electrical/QuasiStatic/SinglePhase/Ideal/IdealOpeningSwitch.mo` | 6 | `Ron` | `(final min=0)` |
