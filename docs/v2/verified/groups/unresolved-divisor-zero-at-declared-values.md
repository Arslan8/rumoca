# Unresolved reports: `divisor-zero-at-declared-values`

**4 report instances**

[Back to Unresolved reports](../unresolved.md) · [Overview](../README.md)

## Common decision rule

The static artifact says a denominator is zero at declared values, but these four cases lack an independent clean-baseline execution and may still involve conditional-component or path reconstruction. They remain unresolved rather than being called broken baselines.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [FINDING-01140](../unresolved/FINDING-01140.md) | Modelica.Electrical.Analog.Examples.ShowSaturatingInductor | `SaturatingInductance1.i` | Source/semantic review | [FINDING-showsaturatinginductor-saturatinginductance1-i-divbaseline.md](../../bugs/FINDING-showsaturatinginductor-saturatinginductance1-i-divbaseline.md) |
| [FINDING-01468](../unresolved/FINDING-01468.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_CurrentControlled | `PID.k` | Source/semantic review | [FINDING-dcpm-currentcontrolled-pid-k-divbaseline.md](../../bugs/FINDING-dcpm-currentcontrolled-pid-k-divbaseline.md) |
| [FINDING-01930](../unresolved/FINDING-01930.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive | `pwm.svPWM.uMax` | Source/semantic review | [FINDING-imc-inverterdrive-pwm-svpwm-umax-divbaseline.md](../../bugs/FINDING-imc-inverterdrive-pwm-svpwm-umax-divbaseline.md) |
| [FINDING-02316](../unresolved/FINDING-02316.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aims.spacePhasorR.turnsRatio` | Source/semantic review | [FINDING-ims-start-aims-spacephasorr-turnsratio-divbaseline.md](../../bugs/FINDING-ims-start-aims-spacephasorr-turnsratio-divbaseline.md) |
