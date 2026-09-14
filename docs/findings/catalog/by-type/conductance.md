# `SI.Conductance` — 43 unbounded declarations

Domain: electrical

`Units.mo` declares `type Conductance` with **no `min`**, so every
declaration below accepts a negative value.

## Exposed

| File | Line | Parameter | Declared modifiers |
|---|---|---|---|
| `Electrical/Analog/Basic/Conductor.mo` | 3 | `G` | `(start=1)` |
| `Electrical/Analog/Basic/Gyrator.mo` | 4 | `G1` | `(start=1)` |
| `Electrical/Analog/Basic/Gyrator.mo` | 5 | `G2` | `(start=1)` |
| `Electrical/Analog/Basic/VCC.mo` | 4 | `transConductance` | `(start=1)` |
| `Electrical/Analog/Examples/Rectifier.mo` | 9 | `Goff` | `—` |
| `Electrical/Analog/Examples/Utilities/Conductor.mo` | 4 | `G` | `—` |
| `Electrical/Analog/Examples/Utilities/NonlinearResistor.mo` | 5 | `Ga` | `—` |
| `Electrical/Analog/Examples/Utilities/NonlinearResistor.mo` | 6 | `Gb` | `—` |
| `Electrical/Analog/Interfaces/IdealSwitchWithArc.mo` | 5 | `Goff` | `—` |
| `Electrical/Analog/Semiconductors/Diode2.mo` | 13 | `Gp` | `—` |
| `Electrical/Analog/Semiconductors/NPN.mo` | 16 | `Gbc` | `—` |
| `Electrical/Analog/Semiconductors/NPN.mo` | 17 | `Gbe` | `—` |
| `Electrical/Analog/Semiconductors/PNP.mo` | 16 | `Gbc` | `—` |
| `Electrical/Analog/Semiconductors/PNP.mo` | 17 | `Gbe` | `—` |
| `Electrical/Machines/Examples/ControlledDCDrives/Utilities/DcdcInverter.mo` | 13 | `GoffT` | `—` |
| `Electrical/Machines/Examples/ControlledDCDrives/Utilities/DcdcInverter.mo` | 22 | `GoffD` | `—` |
| `Electrical/Machines/Examples/ControlledDCDrives/Utilities/SwitchingDcDc.mo` | 7 | `GoffT` | `—` |
| `Electrical/Machines/Examples/ControlledDCDrives/Utilities/SwitchingDcDc.mo` | 13 | `GoffD` | `—` |
| `Electrical/Machines/Losses/CoreParameters.mo` | 18 | `GcRef` | `—` |
| `Electrical/Machines/Utilities/SwitchYD.mo` | 5 | `Goff` | `—` |
| `Electrical/Machines/Utilities/SwitchYDwithArc.mo` | 5 | `Goff` | `—` |
| `Electrical/Polyphase/Basic/Conductor.mo` | 4 | `G` | `(start=fill(1, m)` |
| `Electrical/Polyphase/Examples/Rectifier.mo` | 13 | `Goff` | `—` |
| `Electrical/PowerConverters/DCAC/Polyphase2Level.mo` | 7 | `GoffTransistor` | `—` |
| `Electrical/PowerConverters/DCAC/Polyphase2Level.mo` | 13 | `GoffDiode` | `—` |
| `Electrical/PowerConverters/DCAC/SinglePhase2Level.mo` | 6 | `GoffTransistor` | `—` |
| `Electrical/PowerConverters/DCAC/SinglePhase2Level.mo` | 12 | `GoffDiode` | `—` |
| `Electrical/PowerConverters/DCDC/ChopperBuckBoost.mo` | 8 | `GoffTransistor` | `—` |
| `Electrical/PowerConverters/DCDC/ChopperBuckBoost.mo` | 14 | `GoffDiode` | `—` |
| `Electrical/PowerConverters/DCDC/ChopperStepDown.mo` | 7 | `GoffTransistor` | `—` |
| `Electrical/PowerConverters/DCDC/ChopperStepUp.mo` | 7 | `GoffTransistor` | `—` |
| `Electrical/PowerConverters/DCDC/HBridge.mo` | 10 | `GoffTransistor` | `—` |
| `Electrical/PowerConverters/DCDC/HBridge.mo` | 16 | `GoffDiode` | `—` |
| `Electrical/QuasiStatic/Polyphase/Basic/Conductor.mo` | 4 | `G_ref` | `(start=fill(1, m)` |
| `Electrical/QuasiStatic/SinglePhase/Basic/Admittance.mo` | 18 | `G_ref` | `—` |
| `Electrical/QuasiStatic/SinglePhase/Basic/Conductor.mo` | 6 | `G_ref` | `(start=1)` |
| `Electrical/Spice3.mo` | 2511 | `transConductance` | `(start=0)` |
| `Electrical/Spice3.mo` | 5319 | `G` | `—` |
| `Magnetic/FundamentalWave/BasicMachines/Components/SymmetricPolyphaseWinding.mo` | 47 | `GcRef` | `—` |
| `Magnetic/FundamentalWave/Examples/Components/EddyCurrentLosses.mo` | 8 | `Gc` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/BasicMachines/Components/SymmetricPolyphaseWinding.mo` | 44 | `GcRef` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/Examples/Components/EddyCurrentLosses.mo` | 8 | `Gc` | `—` |
| `Magnetic/QuasiStatic/FundamentalWave/Utilities/SwitchYD.mo` | 5 | `Goff` | `—` |

## Guarded — these add their own bound

Same library, same quantity, bound written. This is why the exposed
cases read as omissions rather than as a deliberate choice.

| File | Line | Parameter | Declared modifiers |
|---|---|---|---|
| `Electrical/Analog/Ideal/ControlledIdealIntermediateSwitch.mo` | 6 | `Goff` | `(final min=0)` |
| `Electrical/Analog/Ideal/ControlledIdealTwoWaySwitch.mo` | 5 | `Goff` | `(final min=0)` |
| `Electrical/Analog/Ideal/IdealIntermediateSwitch.mo` | 4 | `Goff` | `(final min=0)` |
| `Electrical/Analog/Ideal/IdealTriac.mo` | 5 | `Goff` | `(final min=0)` |
| `Electrical/Analog/Ideal/IdealTwoWaySwitch.mo` | 4 | `Goff` | `(final min=0)` |
| `Electrical/Analog/Interfaces/IdealSemiconductor.mo` | 6 | `Goff` | `(final min=0)` |
| `Electrical/Analog/Interfaces/IdealSwitch.mo` | 6 | `Goff` | `(final min=0)` |
| `Electrical/Analog/Sources/DCPowerSupply.mo` | 9 | `Gcc` | `(final min = eps)` |
| `Electrical/Polyphase/Ideal/CloserWithArc.mo` | 6 | `Goff` | `(final min=zeros(m)` |
| `Electrical/Polyphase/Ideal/IdealClosingSwitch.mo` | 6 | `Goff` | `(final min=zeros(m)` |
| `Electrical/Polyphase/Ideal/IdealCommutingSwitch.mo` | 6 | `Goff` | `(final min=zeros(m)` |
| `Electrical/Polyphase/Ideal/IdealDiode.mo` | 6 | `Goff` | `(final min=zeros(m)` |
| `Electrical/Polyphase/Ideal/IdealGTOThyristor.mo` | 6 | `Goff` | `(final min=zeros(m)` |
| `Electrical/Polyphase/Ideal/IdealIntermediateSwitch.mo` | 6 | `Goff` | `(final min=zeros(m)` |
| `Electrical/Polyphase/Ideal/IdealOpeningSwitch.mo` | 6 | `Goff` | `(final min=zeros(m)` |
| `Electrical/Polyphase/Ideal/IdealThyristor.mo` | 6 | `Goff` | `(final min=zeros(m)` |
| `Electrical/Polyphase/Ideal/OpenerWithArc.mo` | 6 | `Goff` | `(final min=zeros(m)` |
| `Electrical/PowerConverters/ACAC/PolyphaseTriac.mo` | 6 | `Goff` | `(final min=0)` |
| `Electrical/PowerConverters/ACAC/SinglePhaseTriac.mo` | 7 | `Goff` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/DiodeBridge2Pulse.mo` | 7 | `GoffDiode` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/DiodeBridge2mPulse.mo` | 8 | `GoffDiode` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/DiodeCenterTap2Pulse.mo` | 7 | `GoffDiode` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/DiodeCenterTap2mPulse.mo` | 8 | `GoffDiode` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/DiodeCenterTapmPulse.mo` | 8 | `GoffDiode` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/HalfControlledBridge2Pulse.mo` | 8 | `GoffDiode` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/HalfControlledBridge2Pulse.mo` | 14 | `GoffThyristor` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/HalfControlledBridge2mPulse.mo` | 9 | `GoffDiode` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/HalfControlledBridge2mPulse.mo` | 15 | `GoffThyristor` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/ThyristorBridge2Pulse.mo` | 7 | `GoffThyristor` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/ThyristorBridge2mPulse.mo` | 8 | `GoffThyristor` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/ThyristorCenterTap2Pulse.mo` | 8 | `GoffThyristor` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/ThyristorCenterTap2mPulse.mo` | 9 | `GoffThyristor` | `(final min=0)` |
| `Electrical/PowerConverters/ACDC/ThyristorCenterTapmPulse.mo` | 9 | `GoffThyristor` | `(final min=0)` |
| `Electrical/PowerConverters/DCDC/ChopperStepDown.mo` | 13 | `GoffDiode` | `(final min=0)` |
| `Electrical/PowerConverters/DCDC/ChopperStepUp.mo` | 13 | `GoffDiode` | `(final min=0)` |
| `Electrical/QuasiStatic/Polyphase/Ideal/IdealClosingSwitch.mo` | 6 | `Goff` | `(final min=zeros(m)` |
| `Electrical/QuasiStatic/Polyphase/Ideal/IdealCommutingSwitch.mo` | 6 | `Goff` | `(final min=zeros(m)` |
| `Electrical/QuasiStatic/Polyphase/Ideal/IdealIntermediateSwitch.mo` | 6 | `Goff` | `(final min=zeros(m)` |
| `Electrical/QuasiStatic/Polyphase/Ideal/IdealOpeningSwitch.mo` | 6 | `Goff` | `(final min=zeros(m)` |
| `Electrical/QuasiStatic/SinglePhase/Ideal/IdealClosingSwitch.mo` | 7 | `Goff` | `(final min=0)` |
| `Electrical/QuasiStatic/SinglePhase/Ideal/IdealCommutingSwitch.mo` | 6 | `Goff` | `(final min=0)` |
| `Electrical/QuasiStatic/SinglePhase/Ideal/IdealIntermediateSwitch.mo` | 6 | `Goff` | `(final min=0)` |
| `Electrical/QuasiStatic/SinglePhase/Ideal/IdealOpeningSwitch.mo` | 7 | `Goff` | `(final min=0)` |
| `Magnetic/FluxTubes/Basic/EddyCurrent.mo` | 12 | `G` | `(min=0)` |
| `Magnetic/FundamentalWave/Components/EddyCurrent.mo` | 6 | `G` | `(min=0)` |
| `Magnetic/QuasiStatic/FluxTubes/Basic/EddyCurrent.mo` | 11 | `G` | `(min=0)` |
| `Magnetic/QuasiStatic/FundamentalWave/Components/EddyCurrent.mo` | 7 | `G` | `(min=0)` |
