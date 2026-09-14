# `SI.Inductance` — 190 unbounded declarations

Domain: electrical

`Units.mo` declares `type Inductance` with **no `min`**, so every
declaration below accepts a negative value.

## Exposed

| File | Line | Parameter | Declared modifiers |
|---|---|---|---|
| `Electrical/Analog/Basic/Inductor.mo` | 4 | `L` | `(start=1)` |
| `Electrical/Analog/Basic/M_Transformer.mo` | 8 | `L` | `—` |
| `Electrical/Analog/Basic/M_Transformer.mo` | 18 | `Lm` | `(each final fixed=false)` |
| `Electrical/Analog/Basic/SaturatingInductor.mo` | 10 | `Lnom` | `(start=1)` |
| `Electrical/Analog/Basic/SaturatingInductor.mo` | 12 | `Lzer` | `(start=2*Lnom)` |
| `Electrical/Analog/Basic/SaturatingInductor.mo` | 14 | `Linf` | `(start=Lnom/2)` |
| `Electrical/Analog/Basic/Transformer.mo` | 4 | `L1` | `(start=1)` |
| `Electrical/Analog/Basic/Transformer.mo` | 5 | `L2` | `(start=1)` |
| `Electrical/Analog/Basic/Transformer.mo` | 6 | `M` | `(start=1)` |
| `Electrical/Analog/Basic/VariableInductor.mo` | 14 | `Lmin` | `—` |
| `Electrical/Analog/Examples/CauerLowPassAnalog.mo` | 5 | `l1` | `—` |
| `Electrical/Analog/Examples/CauerLowPassAnalog.mo` | 6 | `l2` | `—` |
| `Electrical/Analog/Examples/CompareTransformers.mo` | 13 | `L1sigma` | `—` |
| `Electrical/Analog/Examples/CompareTransformers.mo` | 15 | `Lm1` | `—` |
| `Electrical/Analog/Examples/CompareTransformers.mo` | 17 | `L2sigma` | `—` |
| `Electrical/Analog/Examples/CompareTransformers.mo` | 22 | `L1` | `—` |
| `Electrical/Analog/Examples/CompareTransformers.mo` | 24 | `L2` | `—` |
| `Electrical/Analog/Examples/CompareTransformers.mo` | 26 | `M` | `—` |
| `Electrical/Analog/Examples/OpAmps/LCOscillator.mo` | 8 | `L` | `—` |
| `Electrical/Analog/Examples/Rectifier.mo` | 7 | `LAC` | `—` |
| `Electrical/Analog/Examples/ResonanceCircuits.mo` | 7 | `L` | `—` |
| `Electrical/Analog/Examples/ShowSaturatingInductor.mo` | 5 | `Lzer` | `—` |
| `Electrical/Analog/Examples/ShowSaturatingInductor.mo` | 6 | `Lnom` | `—` |
| `Electrical/Analog/Examples/ShowSaturatingInductor.mo` | 9 | `Linf` | `—` |
| `Electrical/Analog/Ideal/IdealTransformer.mo` | 7 | `Lm1` | `(start=1)` |
| `Electrical/Analog/Lines/OLine.mo` | 74 | `lm` | `—` |
| `Electrical/Machines/BasicMachines/Components/AirGapDC.mo` | 4 | `Le` | `—` |
| `Electrical/Machines/BasicMachines/Components/AirGapR.mo` | 3 | `Lmd` | `—` |
| `Electrical/Machines/BasicMachines/Components/AirGapR.mo` | 5 | `Lmq` | `—` |
| `Electrical/Machines/BasicMachines/Components/AirGapR.mo` | 11 | `L` | `—` |
| `Electrical/Machines/BasicMachines/Components/AirGapS.mo` | 3 | `Lm` | `—` |
| `Electrical/Machines/BasicMachines/Components/AirGapS.mo` | 8 | `L` | `—` |
| `Electrical/Machines/BasicMachines/Components/DamperCage.mo` | 3 | `Lrsigmad` | `—` |
| `Electrical/Machines/BasicMachines/Components/DamperCage.mo` | 5 | `Lrsigmaq` | `—` |
| `Electrical/Machines/BasicMachines/Components/Inductor.mo` | 3 | `L` | `—` |
| `Electrical/Machines/BasicMachines/Components/InductorDC.mo` | 5 | `L` | `(start=1)` |
| `Electrical/Machines/BasicMachines/Components/SquirrelCage.mo` | 3 | `Lrsigma` | `—` |
| `Electrical/Machines/BasicMachines/DCMachines/DC_ElectricalExcited.mo` | 33 | `Le` | `(start=1)` |
| `Electrical/Machines/BasicMachines/DCMachines/DC_ElectricalExcited.mo` | 80 | `Lme` | `—` |
| `Electrical/Machines/BasicMachines/DCMachines/DC_ElectricalExcited.mo` | 82 | `Lesigma` | `—` |
| `Electrical/Machines/BasicMachines/DCMachines/DC_SeriesExcited.mo` | 35 | `Le` | `(start=0.0005)` |
| `Electrical/Machines/BasicMachines/DCMachines/DC_SeriesExcited.mo` | 84 | `Lme` | `—` |
| `Electrical/Machines/BasicMachines/DCMachines/DC_SeriesExcited.mo` | 86 | `Lesigma` | `—` |
| `Electrical/Machines/BasicMachines/InductionMachines/IM_SlipRing.mo` | 27 | `Lm` | `(start=3*ZsRef*sqrt(1 - 0.0667)` |
| `Electrical/Machines/BasicMachines/InductionMachines/IM_SlipRing.mo` | 30 | `Lrsigma` | `(start=3*ZsRef*(1 - sqrt(1 - 0.0667)` |
| `Electrical/Machines/BasicMachines/InductionMachines/IM_SlipRing.mo` | 34 | `Lrzero` | `—` |
| `Electrical/Machines/BasicMachines/InductionMachines/IM_SquirrelCage.mo` | 26 | `Lm` | `(start=3*ZsRef*sqrt(1 - 0.0667)` |
| `Electrical/Machines/BasicMachines/InductionMachines/IM_SquirrelCage.mo` | 29 | `Lrsigma` | `(start=3*ZsRef*(1 - sqrt(1 - 0.0667)` |
| `Electrical/Machines/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo` | 63 | `Lrsigmaq` | `—` |
| `Electrical/Machines/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo` | 161 | `Lesigma` | `—` |
| `Electrical/Machines/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo` | 65 | `Lrsigmaq` | `—` |
| `Electrical/Machines/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo` | 57 | `Lrsigmaq` | `—` |
| `Electrical/Machines/Examples/InductionMachines/IMC_InverterDrive.mo` | 12 | `LGrid` | `—` |
| `Electrical/Machines/Examples/InductionMachines/IMC_YDarc.mo` | 10 | `LLine` | `—` |
| `Electrical/Machines/Examples/SynchronousMachines/SMEE_LoadDump.mo` | 16 | `LLoad` | `—` |
| `Electrical/Machines/Interfaces/PartialBasicDCMachine.mo` | 26 | `La` | `(start=0.0015)` |
| `Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo` | 20 | `Lszero` | `—` |
| `Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo` | 23 | `Lssigma` | `(start=3*ZsRef*(1 - sqrt(1 - 0.0667)` |
| `Electrical/Machines/Interfaces/PartialBasicTransformer.mo` | 18 | `L1sigma` | `(start=78E-6/(if C1 == "D" then 1 else 3)` |
| `Electrical/Machines/Interfaces/PartialBasicTransformer.mo` | 30 | `L2sigma` | `(start=78E-6/(if C2 == "d" then 1 else 3)` |
| `Electrical/Machines/Utilities/DQCurrentController.mo` | 12 | `Ld` | `—` |
| `Electrical/Machines/Utilities/DQCurrentController.mo` | 13 | `Lq` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/DcElectricalExcitedData.mo` | 15 | `Le` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/DcPermanentMagnetData.mo` | 28 | `La` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/DcSeriesExcitedData.mo` | 14 | `Le` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/IM_SlipRingData.mo` | 6 | `Lm` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/IM_SlipRingData.mo` | 9 | `Lrsigma` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/IM_SlipRingData.mo` | 16 | `Lrzero` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/IM_SquirrelCageData.mo` | 6 | `Lm` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/IM_SquirrelCageData.mo` | 9 | `Lrsigma` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo` | 20 | `Lszero` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo` | 23 | `Lssigma` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/SM_ReluctanceRotorData.mo` | 6 | `Lmd` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/SM_ReluctanceRotorData.mo` | 9 | `Lmq` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/SM_ReluctanceRotorData.mo` | 15 | `Lrsigmad` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/SM_ReluctanceRotorData.mo` | 20 | `Lrsigmaq` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/TransformerData.mo` | 26 | `L1sigma` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/TransformerData.mo` | 38 | `L2sigma` | `—` |
| `Electrical/Machines/Utilities/SynchronousMachineData.mo` | 95 | `Lssigma` | `—` |
| `Electrical/Machines/Utilities/SynchronousMachineData.mo` | 101 | `Lmd` | `—` |
| `Electrical/Machines/Utilities/SynchronousMachineData.mo` | 104 | `Lmq` | `—` |
| `Electrical/Machines/Utilities/SynchronousMachineData.mo` | 107 | `Lrsigmad` | `—` |
| `Electrical/Machines/Utilities/SynchronousMachineData.mo` | 110 | `Lrsigmaq` | `—` |
| `Electrical/Machines/Utilities/TransformerData.mo` | 40 | `L1sigma` | `—` |
| `Electrical/Machines/Utilities/TransformerData.mo` | 48 | `L2sigma` | `—` |
| `Electrical/Polyphase/Basic/Inductor.mo` | 4 | `L` | `(start=fill(1, m)` |
| `Electrical/Polyphase/Basic/MutualInductor.mo` | 5 | `L` | `—` |
| `Electrical/Polyphase/Basic/SaturatingInductor.mo` | 6 | `Lnom` | `(start=fill(1, m)` |
| `Electrical/Polyphase/Basic/SaturatingInductor.mo` | 8 | `Lzer` | `(start={2*Lnom[j] for j in 1 :m})` |
| `Electrical/Polyphase/Basic/SaturatingInductor.mo` | 10 | `Linf` | `(start={Lnom[j]/2 for j in 1 :m})` |
| `Electrical/Polyphase/Basic/Transformer.mo` | 4 | `L1` | `(start=fill(1, m)` |
| `Electrical/Polyphase/Basic/Transformer.mo` | 6 | `L2` | `(start=fill(1, m)` |
| `Electrical/Polyphase/Basic/Transformer.mo` | 8 | `M` | `(start=fill(1, m)` |
| `Electrical/Polyphase/Basic/VariableInductor.mo` | 5 | `Lmin` | `—` |
| `Electrical/Polyphase/Basic/ZeroInductor.mo` | 4 | `Lzero` | `—` |
| `Electrical/Polyphase/Examples/Rectifier.mo` | 8 | `L` | `—` |
| `Electrical/Polyphase/Examples/TestSensors.mo` | 10 | `L` | `—` |
| `Electrical/Polyphase/Examples/TransformerYD.mo` | 7 | `Lm` | `—` |
| `Electrical/Polyphase/Examples/TransformerYD.mo` | 8 | `LT` | `—` |
| `Electrical/Polyphase/Examples/TransformerYY.mo` | 7 | `Lm` | `—` |
| `Electrical/Polyphase/Examples/TransformerYY.mo` | 8 | `LT` | `—` |
| `Electrical/Polyphase/Examples/Utilities/PolyphaseRectifierData.mo` | 22 | `LDC` | `—` |
| `Electrical/Polyphase/Ideal/IdealTransformer.mo` | 7 | `Lm1` | `(start=fill(1, m)` |
| `Electrical/PowerConverters/Examples/ACAC/ExampleTemplates/Dimmer.mo` | 11 | `LLoad` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2Pulse/DiodeBridge2Pulse.mo` | 9 | `L` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2Pulse/ThyristorBridge2Pulse_DC_Drive.mo` | 16 | `LMains` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2Pulse/ThyristorBridge2Pulse_DC_Drive.mo` | 18 | `Ld` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2Pulse/ThyristorBridge2Pulse_RL.mo` | 11 | `L` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2Pulse/ThyristorBridge2Pulse_RLV.mo` | 11 | `L` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2Pulse/ThyristorBridge2Pulse_RLV_Characteristic.mo` | 11 | `L` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/ThyristorBridge2mPulse_DC_Drive.mo` | 18 | `LMains` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/ThyristorBridge2mPulse_DC_Drive.mo` | 21 | `Ld` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/ThyristorBridge2mPulse_RL.mo` | 12 | `L` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/ThyristorBridge2mPulse_RLV.mo` | 11 | `L` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/ThyristorBridge2mPulse_RLV_Characteristic.mo` | 12 | `L` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTap2Pulse/ThyristorCenterTap2Pulse_RL.mo` | 11 | `L` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTap2Pulse/ThyristorCenterTap2Pulse_RLV.mo` | 11 | `L` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTap2Pulse/ThyristorCenterTap2Pulse_RLV_Characteristic.mo` | 9 | `L` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTap2mPulse/ThyristorCenterTap2mPulse_RL.mo` | 11 | `L` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTap2mPulse/ThyristorCenterTap2mPulse_RLV.mo` | 11 | `L` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTap2mPulse/ThyristorCenterTap2mPulse_RLV_Characteristic.mo` | 9 | `L` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTapmPulse/ThyristorCenterTapmPulse_RL.mo` | 11 | `L` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTapmPulse/ThyristorCenterTapmPulse_RLV.mo` | 11 | `L` | `—` |
| `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTapmPulse/ThyristorCenterTapmPulse_RLV_Characteristic.mo` | 9 | `L` | `—` |
| `Electrical/PowerConverters/Examples/DCAC/PolyphaseTwoLevel/PolyphaseTwoLevel_RL.mo` | 10 | `L` | `—` |
| `Electrical/PowerConverters/Examples/DCAC/SinglePhaseTwoLevel/SinglePhaseTwoLevel_RL.mo` | 10 | `L` | `—` |
| `Electrical/PowerConverters/Examples/DCDC/ChopperStepDown/ChopperStepDown_RL.mo` | 5 | `LLoad` | `—` |
| `Electrical/PowerConverters/Examples/DCDC/ExampleTemplates/ChopperBuckBoost.mo` | 10 | `L` | `—` |
| `Electrical/PowerConverters/Examples/DCDC/ExampleTemplates/ChopperStepDown.mo` | 6 | `L` | `—` |
| `Electrical/PowerConverters/Examples/DCDC/ExampleTemplates/ChopperStepUp.mo` | 6 | `L` | `—` |
| `Electrical/PowerConverters/Examples/DCDC/HBridge/HBridge_DC_Drive.mo` | 9 | `Ld` | `—` |
| `Electrical/PowerConverters/Examples/DCDC/HBridge/HBridge_RL.mo` | 6 | `L` | `—` |
| `Electrical/PowerConverters/Examples/DCDC/HBridge/HBridge_TrianglePWM_RL.mo` | 6 | `L` | `—` |
| `Electrical/QuasiStatic/Machines/Interfaces/PartialBasicTransformer.mo` | 20 | `L1sigma` | `(start=78E-6/(if C1 == "D" then 1 else 3)` |
| `Electrical/QuasiStatic/Machines/Interfaces/PartialBasicTransformer.mo` | 34 | `L2sigma` | `(start=78E-6/(if C2 == "d" then 1 else 3)` |
| `Electrical/QuasiStatic/Polyphase/Basic/Inductor.mo` | 4 | `L` | `(start=fill(1, m)` |
| `Electrical/QuasiStatic/Polyphase/Basic/MutualInductor.mo` | 6 | `L` | `—` |
| `Electrical/QuasiStatic/Polyphase/Examples/BalancingDelta.mo` | 8 | `L` | `—` |
| `Electrical/QuasiStatic/Polyphase/Examples/BalancingStar.mo` | 8 | `L` | `—` |
| `Electrical/QuasiStatic/Polyphase/Examples/TestSensors.mo` | 10 | `L` | `—` |
| `Electrical/QuasiStatic/SinglePhase/Basic/Inductor.mo` | 5 | `L` | `(start=1)` |
| `Electrical/QuasiStatic/SinglePhase/Basic/Transformer.mo` | 4 | `L1` | `(start=1)` |
| `Electrical/QuasiStatic/SinglePhase/Basic/Transformer.mo` | 5 | `L2` | `(start=1)` |
| `Electrical/QuasiStatic/SinglePhase/Basic/Transformer.mo` | 6 | `M` | `(start=1)` |
| `Electrical/QuasiStatic/SinglePhase/Examples/MultipleResonance.mo` | 10 | `L1` | `—` |
| `Electrical/QuasiStatic/SinglePhase/Examples/MultipleResonance.mo` | 11 | `L2` | `—` |
| `Electrical/QuasiStatic/SinglePhase/Examples/MultipleResonance.mo` | 13 | `M` | `—` |
| `Electrical/QuasiStatic/SinglePhase/Examples/MultipleResonance.mo` | 16 | `L` | `—` |
| `Electrical/Spice3.mo` | 2342 | `L` | `(start=0)` |
| `Magnetic/FluxTubes/Examples/MovingCoilActuator/Components/ConstantActuator.mo` | 7 | `L` | `—` |
| `Magnetic/FundamentalWave/BaseClasses/Machine.mo` | 33 | `Lssigma` | `(start=3*ZsRef*(1 - sqrt(1 - 0.0667)` |
| `Magnetic/FundamentalWave/BaseClasses/Machine.mo` | 39 | `Lszero` | `—` |
| `Magnetic/FundamentalWave/BasicMachines/Components/SinglePhaseWinding.mo` | 39 | `Lsigma` | `—` |
| `Magnetic/FundamentalWave/BasicMachines/Components/SymmetricPolyphaseCageWinding.mo` | 23 | `Lsigma` | `—` |
| `Magnetic/FundamentalWave/BasicMachines/Components/SymmetricPolyphaseWinding.mo` | 42 | `Lsigma` | `—` |
| `Magnetic/FundamentalWave/BasicMachines/Components/SymmetricPolyphaseWinding.mo` | 45 | `Lzero` | `—` |
| `Magnetic/FundamentalWave/BasicMachines/InductionMachines/IM_SlipRing.mo` | 34 | `Lm` | `(start=3*ZsRef*sqrt(1 - 0.0667)` |
| `Magnetic/FundamentalWave/BasicMachines/InductionMachines/IM_SlipRing.mo` | 38 | `Lrsigma` | `(start=3*ZsRef*(1 - sqrt(1 - 0.0667)` |
| `Magnetic/FundamentalWave/BasicMachines/InductionMachines/IM_SlipRing.mo` | 45 | `Lrzero` | `—` |
| `Magnetic/FundamentalWave/BasicMachines/InductionMachines/IM_SquirrelCage.mo` | 23 | `Lm` | `(start=3*ZsRef*sqrt(1 - 0.0667)` |
| `Magnetic/FundamentalWave/BasicMachines/InductionMachines/IM_SquirrelCage.mo` | 27 | `Lrsigma` | `(start=3*ZsRef*(1 - sqrt(1 - 0.0667)` |
| `Magnetic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo` | 49 | `Lrsigmaq` | `—` |
| `Magnetic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo` | 169 | `Lesigma` | `—` |
| `Magnetic/FundamentalWave/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo` | 47 | `Lrsigmaq` | `—` |
| `Magnetic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo` | 46 | `Lrsigmaq` | `—` |
| `Magnetic/FundamentalWave/Components/PolyphaseElectroMagneticConverter.mo` | 45 | `Lsigma` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/ComparisonPolyphase/SMEE_Generator_Polyphase.mo` | 21 | `Lssigma` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/ComparisonPolyphase/SMEE_Generator_Polyphase.mo` | 23 | `Lmd` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/ComparisonPolyphase/SMEE_Generator_Polyphase.mo` | 25 | `Lmq` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/ComparisonPolyphase/SMEE_Generator_Polyphase.mo` | 27 | `Lrsigmad` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/ComparisonPolyphase/SMEE_Generator_Polyphase.mo` | 30 | `Lrsigmaq` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/SMEE_Generator.mo` | 19 | `Lssigma` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/SMEE_Generator.mo` | 21 | `Lmd` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/SMEE_Generator.mo` | 23 | `Lmq` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/SMEE_Generator.mo` | 25 | `Lrsigmad` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/SMEE_Generator.mo` | 28 | `Lrsigmaq` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/SMEE_LoadDump.mo` | 17 | `LLoad` | `—` |
| `Magnetic/FundamentalWave/Examples/Components/PolyphaseInductance.mo` | 9 | `L` | `—` |
| `Magnetic/FundamentalWave/Examples/Components/SinglePhaseInductance.mo` | 7 | `L` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/BaseClasses/Machine.mo` | 34 | `Lssigma` | `(start=3*(1 - sqrt(1 - 0.0667)` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/Components/SymmetricPolyphaseCageWinding.mo` | 24 | `Lsigma` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/Components/SymmetricPolyphaseWinding.mo` | 41 | `Lsigma` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/InductionMachines/IM_SlipRing.mo` | 33 | `Lm` | `(start=3*ZsRef*sqrt(1 - 0.0667)` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/InductionMachines/IM_SlipRing.mo` | 37 | `Lrsigma` | `(start=3*ZsRef*(1 - sqrt(1 - 0.0667)` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/InductionMachines/IM_SquirrelCage.mo` | 22 | `Lm` | `(start=3*ZsRef*sqrt(1 - 0.0667)` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/InductionMachines/IM_SquirrelCage.mo` | 26 | `Lrsigma` | `(start=3*ZsRef*(1 - sqrt(1 - 0.0667)` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo` | 48 | `Lrsigmaq` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo` | 46 | `Lrsigmaq` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo` | 42 | `Lrsigmaq` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/Examples/Components/PolyphaseInductance.mo` | 8 | `L` | `—` |

## Guarded — these add their own bound

Same library, same quantity, bound written. This is why the exposed
cases read as omissions rather than as a deliberate choice.

| File | Line | Parameter | Declared modifiers |
|---|---|---|---|
| `Electrical/Analog/Examples/Utilities/DirectInductor.mo` | 4 | `L` | `(min=0)` |
| `Electrical/Analog/Examples/Utilities/InverseInductor.mo` | 4 | `L` | `(min=0)` |
| `Electrical/Machines/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo` | 48 | `Lmd` | `(start=1.5*ZsRef/(2*pi*fsNominal)` |
| `Electrical/Machines/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo` | 51 | `Lmq` | `(start=1.5*ZsRef/(2*pi*fsNominal)` |
| `Electrical/Machines/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo` | 57 | `Lrsigmad` | `(start=0.05*ZsRef/(2*pi* fsNominal)` |
| `Electrical/Machines/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo` | 50 | `Lmd` | `(start=0.3*ZsRef/(2*pi*fsNominal)` |
| `Electrical/Machines/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo` | 53 | `Lmq` | `(start=0.3*ZsRef/(2*pi*fsNominal)` |
| `Electrical/Machines/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo` | 59 | `Lrsigmad` | `(start=0.05*ZsRef/(2*pi* fsNominal)` |
| `Electrical/Machines/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo` | 42 | `Lmd` | `(start=2.9*ZsRef/(2*pi*fsNominal)` |
| `Electrical/Machines/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo` | 45 | `Lmq` | `(start=0.9*ZsRef/(2*pi*fsNominal)` |
| `Electrical/Machines/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo` | 51 | `Lrsigmad` | `(start=0.05*ZsRef/(2*pi* fsNominal)` |
| `Magnetic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo` | 31 | `Lmd` | `(start=1.5*ZsRef/(2*pi*fsNominal)` |
| `Magnetic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo` | 35 | `Lmq` | `(start=1.5*ZsRef/(2*pi*fsNominal)` |
| `Magnetic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo` | 42 | `Lrsigmad` | `(start=0.05*ZsRef/(2*pi* fsNominal)` |
| `Magnetic/FundamentalWave/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo` | 29 | `Lmd` | `(start=0.3*ZsRef/(2*pi*fsNominal)` |
| `Magnetic/FundamentalWave/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo` | 33 | `Lmq` | `(start=0.3*ZsRef/(2*pi*fsNominal)` |
| `Magnetic/FundamentalWave/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo` | 40 | `Lrsigmad` | `(start=0.05*ZsRef/(2*pi* fsNominal)` |
| `Magnetic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo` | 28 | `Lmd` | `(start=2.9*ZsRef/(2*pi*fsNominal)` |
| `Magnetic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo` | 32 | `Lmq` | `(start=0.9*ZsRef/(2*pi*fsNominal)` |
| `Magnetic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo` | 39 | `Lrsigmad` | `(start=0.05*ZsRef/(2*pi* fsNominal)` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo` | 30 | `Lmd` | `(start=1.5*ZsRef/(2*pi*fsNominal)` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo` | 34 | `Lmq` | `(start=1.5*ZsRef/(2*pi*fsNominal)` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo` | 41 | `Lrsigmad` | `(start=0.05*ZsRef/(2*pi* fsNominal)` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo` | 28 | `Lmd` | `(start=0.3*ZsRef/(2*pi*fsNominal)` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo` | 32 | `Lmq` | `(start=0.3*ZsRef/(2*pi*fsNominal)` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/SynchronousMachines/SM_PermanentMagnet.mo` | 39 | `Lrsigmad` | `(start=0.05*ZsRef/(2*pi* fsNominal)` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo` | 24 | `Lmd` | `(start=2.9*ZsRef/(2*pi*fsNominal)` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo` | 28 | `Lmq` | `(start=0.9*ZsRef/(2*pi*fsNominal)` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo` | 35 | `Lrsigmad` | `(start=0.05*ZsRef/(2*pi* fsNominal)` |
