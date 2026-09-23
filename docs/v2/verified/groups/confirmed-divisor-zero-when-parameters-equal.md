# Execution-confirmed defects: `divisor-zero-when-parameters-equal`

**13 report instances**

[Back to Execution-confirmed defects](../confirmed.md) · [Overview](../README.md)

## Common decision rule

The exact reported witness was placed in a generated Modelica subclass before translation. The unmodified model executed cleanly, while OpenModelica rejected the trigger with a numerical failure such as division by zero, a non-finite result, or a singular system.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [FINDING-00788](../confirmed/FINDING-00788.md) | Modelica.Electrical.Analog.Examples.OpAmps.Comparator | `Vps` | OMC: `confirmed-by-omc` | [FINDING-comparator-vps-divequal.md](../../bugs/FINDING-comparator-vps-divequal.md) |
| [FINDING-00789](../confirmed/FINDING-00789.md) | Modelica.Electrical.Analog.Examples.OpAmps.Comparator | `Vps` | OMC: `confirmed-by-omc` | [FINDING-comparator-vps-divequal-2.md](../../bugs/FINDING-comparator-vps-divequal-2.md) |
| [FINDING-00909](../confirmed/FINDING-00909.md) | Modelica.Electrical.Analog.Examples.OpAmps.InvertingSchmittTrigger | `opAmp.Vps` | OMC: `confirmed-by-omc` | [FINDING-invertingschmitttrigger-opamp-vps-divequal.md](../../bugs/FINDING-invertingschmitttrigger-opamp-vps-divequal.md) |
| [FINDING-00931](../confirmed/FINDING-00931.md) | Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator | `opAmp.Vps` | OMC: `confirmed-by-omc` | [FINDING-lcoscillator-opamp-vps-divequal.md](../../bugs/FINDING-lcoscillator-opamp-vps-divequal.md) |
| [FINDING-00959](../confirmed/FINDING-00959.md) | Modelica.Electrical.Analog.Examples.OpAmps.Multivibrator | `opAmp.Vps` | OMC: `confirmed-by-omc` | [FINDING-multivibrator-opamp-vps-divequal.md](../../bugs/FINDING-multivibrator-opamp-vps-divequal.md) |
| [FINDING-01031](../confirmed/FINDING-01031.md) | Modelica.Electrical.Analog.Examples.OpAmps.SchmittTrigger | `opAmp.Vps` | OMC: `confirmed-by-omc` | [FINDING-schmitttrigger-opamp-vps-divequal.md](../../bugs/FINDING-schmitttrigger-opamp-vps-divequal.md) |
| [FINDING-01051](../confirmed/FINDING-01051.md) | Modelica.Electrical.Analog.Examples.OpAmps.SignalGenerator | `opAmp1.Vps` | OMC: `confirmed-by-omc` | [FINDING-signalgenerator-opamp1-vps-divequal.md](../../bugs/FINDING-signalgenerator-opamp1-vps-divequal.md) |
| [FINDING-01052](../confirmed/FINDING-01052.md) | Modelica.Electrical.Analog.Examples.OpAmps.SignalGenerator | `opAmp2.Vps` | OMC: `confirmed-by-omc` | [FINDING-signalgenerator-opamp2-vps-divequal.md](../../bugs/FINDING-signalgenerator-opamp2-vps-divequal.md) |
| [FINDING-01063](../confirmed/FINDING-01063.md) | Modelica.Electrical.Analog.Examples.OpAmps.VoltageFollower | `opAmp.Vps` | OMC: `confirmed-by-omc` | [FINDING-voltagefollower-opamp-vps-divequal.md](../../bugs/FINDING-voltagefollower-opamp-vps-divequal.md) |
| [FINDING-02398](../confirmed/FINDING-02398.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `smeeData.xd` | OMC: `confirmed-by-omc` | [FINDING-smee-dol-smeedata-xd-divequal.md](../../bugs/FINDING-smee-dol-smeedata-xd-divequal.md) |
| [FINDING-02399](../confirmed/FINDING-02399.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `smeeData.xd` | OMC: `confirmed-by-omc` | [FINDING-smee-dol-smeedata-xd-divequal-2.md](../../bugs/FINDING-smee-dol-smeedata-xd-divequal-2.md) |
| [FINDING-02486](../confirmed/FINDING-02486.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `smeeData.xd` | OMC: `confirmed-by-omc` | [FINDING-smee-generator-smeedata-xd-divequal.md](../../bugs/FINDING-smee-generator-smeedata-xd-divequal.md) |
| [FINDING-02487](../confirmed/FINDING-02487.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `smeeData.xd` | OMC: `confirmed-by-omc` | [FINDING-smee-generator-smeedata-xd-divequal-2.md](../../bugs/FINDING-smee-generator-smeedata-xd-divequal-2.md) |
