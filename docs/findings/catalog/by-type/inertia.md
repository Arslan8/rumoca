# `SI.Inertia` — 83 unbounded declarations

Domain: mechanical

`Units.mo` declares `type Inertia` with **no `min`**, so every
declaration below accepts a negative value.

## Exposed

| File | Line | Parameter | Declared modifiers |
|---|---|---|---|
| `Blocks/package.mo` | 2727 | `JLoad` | `—` |
| `Electrical/Machines/Examples/ControlledDCDrives/Utilities/DriveDataDCPM.mo` | 42 | `JL` | `—` |
| `Electrical/Machines/Examples/DCMachines/DCEE_Start.mo` | 12 | `JLoad` | `—` |
| `Electrical/Machines/Examples/DCMachines/DCPM_Cooling.mo` | 9 | `JLoad` | `—` |
| `Electrical/Machines/Examples/DCMachines/DCPM_CurrentControlled.mo` | 7 | `JLoad` | `—` |
| `Electrical/Machines/Examples/DCMachines/DCPM_QuasiStatic.mo` | 10 | `JLoad` | `—` |
| `Electrical/Machines/Examples/DCMachines/DCPM_Start.mo` | 11 | `JLoad` | `—` |
| `Electrical/Machines/Examples/DCMachines/DCPM_Temperature.mo` | 10 | `JLoad` | `—` |
| `Electrical/Machines/Examples/DCMachines/DCPM_withLosses.mo` | 16 | `JLoad` | `—` |
| `Electrical/Machines/Examples/DCMachines/DCSE_SinglePhase.mo` | 11 | `JLoad` | `—` |
| `Electrical/Machines/Examples/DCMachines/DCSE_Start.mo` | 11 | `JLoad` | `—` |
| `Electrical/Machines/Examples/DCMachines/DC_CompareCharacteristics.mo` | 10 | `JLoad` | `—` |
| `Electrical/Machines/Examples/InductionMachines/IMC_Conveyor.mo` | 15 | `JLoad` | `—` |
| `Electrical/Machines/Examples/InductionMachines/IMC_DCBraking.mo` | 8 | `JLoad` | `—` |
| `Electrical/Machines/Examples/InductionMachines/IMC_DOL.mo` | 13 | `JLoad` | `—` |
| `Electrical/Machines/Examples/InductionMachines/IMC_Initialize.mo` | 15 | `JLoad` | `—` |
| `Electrical/Machines/Examples/InductionMachines/IMC_Inverter.mo` | 13 | `JLoad` | `—` |
| `Electrical/Machines/Examples/InductionMachines/IMC_InverterDrive.mo` | 17 | `JLoad` | `—` |
| `Electrical/Machines/Examples/InductionMachines/IMC_Steinmetz.mo` | 20 | `JLoad` | `—` |
| `Electrical/Machines/Examples/InductionMachines/IMC_Transformer.mo` | 15 | `JLoad` | `—` |
| `Electrical/Machines/Examples/InductionMachines/IMC_YD.mo` | 14 | `JLoad` | `—` |
| `Electrical/Machines/Examples/InductionMachines/IMC_YDarc.mo` | 16 | `JLoad` | `—` |
| `Electrical/Machines/Examples/InductionMachines/IMS_Start.mo` | 16 | `JLoad` | `—` |
| `Electrical/Machines/Examples/SynchronousMachines/SMPM_Braking.mo` | 11 | `JLoad` | `—` |
| `Electrical/Machines/Examples/SynchronousMachines/SMPM_CurrentSource.mo` | 12 | `JLoad` | `—` |
| `Electrical/Machines/Examples/SynchronousMachines/SMPM_Inverter.mo` | 13 | `JLoad` | `—` |
| `Electrical/Machines/Examples/SynchronousMachines/SMPM_ResistiveBraking.mo` | 7 | `JLoad` | `—` |
| `Electrical/Machines/Examples/SynchronousMachines/SMPM_VoltageSource.mo` | 12 | `JLoad` | `—` |
| `Electrical/Machines/Examples/SynchronousMachines/SMR_DOL.mo` | 13 | `JLoad` | `—` |
| `Electrical/Machines/Examples/SynchronousMachines/SMR_Inverter.mo` | 13 | `JLoad` | `—` |
| `Electrical/Machines/Interfaces/PartialBasicMachine.mo` | 5 | `Jr` | `—` |
| `Electrical/Machines/Interfaces/PartialBasicMachine.mo` | 8 | `Js` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/DcPermanentMagnetData.mo` | 5 | `Jr` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/DcPermanentMagnetData.mo` | 6 | `Js` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo` | 6 | `Jr` | `—` |
| `Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo` | 7 | `Js` | `—` |
| `Electrical/PowerConverters/Examples/ACAC/SoftStarter.mo` | 10 | `JLoad` | `—` |
| `Magnetic/FundamentalWave/BaseClasses/Machine.mo` | 7 | `Jr` | `(start=0.29)` |
| `Magnetic/FundamentalWave/BaseClasses/Machine.mo` | 10 | `Js` | `(start=Jr)` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/InductionMachines/ComparisonPolyphase/IMC_DOL_CommonLeakage.mo` | 15 | `J_Load` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/InductionMachines/ComparisonPolyphase/IMC_DOL_Polyphase.mo` | 15 | `J_Load` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/InductionMachines/ComparisonPolyphase/IMS_Start_Polyphase.mo` | 22 | `J_Load` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/InductionMachines/IMC_Conveyor.mo` | 15 | `JLoad` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/InductionMachines/IMC_DOL.mo` | 13 | `J_Load` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/InductionMachines/IMC_Initialize.mo` | 15 | `JLoad` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/InductionMachines/IMC_Inverter.mo` | 14 | `JLoad` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/InductionMachines/IMC_Steinmetz.mo` | 21 | `JLoad` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/InductionMachines/IMC_Transformer.mo` | 16 | `JLoad` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/InductionMachines/IMC_YD.mo` | 15 | `JLoad` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/InductionMachines/IMS_Start.mo` | 18 | `J_Load` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/ComparisonPolyphase/SMPM_Inverter_Polyphase.mo` | 17 | `J_Load` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/ComparisonPolyphase/SMR_Inverter_Polyphase.mo` | 16 | `J_Load` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/SMPM_Braking.mo` | 11 | `JLoad` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/SMPM_CurrentSource.mo` | 12 | `JLoad` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/SMPM_Inverter.mo` | 14 | `J_Load` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/SMPM_VoltageSource.mo` | 12 | `JLoad` | `—` |
| `Magnetic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/SMR_Inverter.mo` | 14 | `J_Load` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/BaseClasses/Machine.mo` | 7 | `Jr` | `(start=0.29)` |
| `Magnetic/QuasiStatic/FundamentalWave/BaseClasses/Machine.mo` | 10 | `Js` | `(start=Jr)` |
| `Magnetic/QuasiStatic/FundamentalWave/Examples/BasicMachines/InductionMachines/IMC_Conveyor.mo` | 14 | `JLoad` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/Examples/BasicMachines/InductionMachines/IMC_DOL.mo` | 14 | `J_Load` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/Examples/BasicMachines/InductionMachines/IMC_Initialize.mo` | 14 | `JLoad` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/Examples/BasicMachines/InductionMachines/IMC_Inverter.mo` | 14 | `JLoad` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/Examples/BasicMachines/InductionMachines/IMC_Transformer.mo` | 15 | `JLoad` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/Examples/BasicMachines/InductionMachines/IMC_YD.mo` | 14 | `JLoad` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/Examples/BasicMachines/InductionMachines/IMS_Start.mo` | 19 | `J_Load` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/SMPM_CurrentSource.mo` | 14 | `JLoad` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/SMPM_MTPA.mo` | 12 | `JLoad` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/SMPM_Mains.mo` | 11 | `J_Load` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/Examples/BasicMachines/SynchronousMachines/SMR_CurrentSource.mo` | 14 | `JLoad` | `—` |
| `Mechanics/MultiBody/Parts/Body.mo` | 114 | `I` | `—` |
| `Mechanics/MultiBody/Parts/BodyBox.mo` | 111 | `I` | `—` |
| `Mechanics/MultiBody/Parts/BodyCylinder.mo` | 105 | `I22` | `—` |
| `Mechanics/MultiBody/Parts/BodyCylinder.mo` | 114 | `I` | `—` |
| `Mechanics/MultiBody/Parts/RollingWheel.mo` | 10 | `I_axis` | `—` |
| `Mechanics/MultiBody/Parts/RollingWheel.mo` | 11 | `I_long` | `—` |
| `Mechanics/MultiBody/Parts/RollingWheelSet.mo` | 16 | `I_wheelAxis` | `—` |
| `Mechanics/MultiBody/Parts/RollingWheelSet.mo` | 17 | `I_wheelLong` | `—` |
| `Mechanics/MultiBody/Parts/Rotor1D.mo` | 147 | `nJ` | `—` |
| `Mechanics/Rotational/Examples/CompareBrakingTorque.mo` | 4 | `J` | `—` |
| `Mechanics/Rotational/Examples/Utilities/InverseInertia.mo` | 4 | `J` | `—` |
| `Mechanics/Translational/Components/Vehicle.mo` | 5 | `J` | `—` |
| `Utilities/Examples.mo` | 390 | `J` | `—` |

## Guarded — these add their own bound

Same library, same quantity, bound written. This is why the exposed
cases read as omissions rather than as a deliberate choice.

| File | Line | Parameter | Declared modifiers |
|---|---|---|---|
| `Mechanics/MultiBody/Examples/Loops/Utilities/CylinderBase.mo` | 22 | `pistonInertia_11` | `(min=0)` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/CylinderBase.mo` | 25 | `pistonInertia_22` | `(min=0)` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/CylinderBase.mo` | 28 | `pistonInertia_33` | `(min=0)` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/CylinderBase.mo` | 39 | `rodInertia_11` | `(min=0)` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/CylinderBase.mo` | 42 | `rodInertia_22` | `(min=0)` |
| `Mechanics/MultiBody/Examples/Loops/Utilities/CylinderBase.mo` | 45 | `rodInertia_33` | `(min=0)` |
| `Mechanics/MultiBody/Examples/Systems/RobotR3/Utilities/AxisType2.mo` | 16 | `J` | `(min=0)` |
| `Mechanics/MultiBody/Examples/Systems/RobotR3/Utilities/Motor.mo` | 4 | `J` | `(min=0)` |
| `Mechanics/MultiBody/Parts/Body.mo` | 17 | `I_11` | `(min=0)` |
| `Mechanics/MultiBody/Parts/Body.mo` | 19 | `I_22` | `(min=0)` |
| `Mechanics/MultiBody/Parts/Body.mo` | 21 | `I_33` | `(min=0)` |
| `Mechanics/MultiBody/Parts/Body.mo` | 23 | `I_21` | `(min=-C.inf)` |
| `Mechanics/MultiBody/Parts/Body.mo` | 25 | `I_31` | `(min=-C.inf)` |
| `Mechanics/MultiBody/Parts/Body.mo` | 27 | `I_32` | `(min=-C.inf)` |
| `Mechanics/MultiBody/Parts/BodyShape.mo` | 24 | `I_11` | `(min=0)` |
| `Mechanics/MultiBody/Parts/BodyShape.mo` | 26 | `I_22` | `(min=0)` |
| `Mechanics/MultiBody/Parts/BodyShape.mo` | 28 | `I_33` | `(min=0)` |
| `Mechanics/MultiBody/Parts/BodyShape.mo` | 30 | `I_21` | `(min=-C.inf)` |
| `Mechanics/MultiBody/Parts/BodyShape.mo` | 32 | `I_31` | `(min=-C.inf)` |
| `Mechanics/MultiBody/Parts/BodyShape.mo` | 34 | `I_32` | `(min=-C.inf)` |
| `Mechanics/MultiBody/Parts/Rotor1D.mo` | 7 | `J` | `(min=0,start=1)` |
| `Mechanics/MultiBody/Parts/Rotor1D.mo` | 78 | `J` | `(min=0)` |
| `Mechanics/Rotational/Components/Inertia.mo` | 4 | `J` | `(min=0, start=1)` |
| `Mechanics/Rotational/Examples/First.mo` | 7 | `Jmotor` | `(min=0)` |
| `Mechanics/Rotational/Examples/First.mo` | 8 | `Jload` | `(min=0)` |
| `Mechanics/Rotational/Examples/FirstGrounded.mo` | 8 | `Jmotor` | `(min=0)` |
| `Mechanics/Rotational/Examples/FirstGrounded.mo` | 9 | `Jload` | `(min=0)` |
| `Mechanics/Rotational/Examples/Utilities/DirectInertia.mo` | 4 | `J` | `(min=0)` |
