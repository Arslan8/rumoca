# False positives and explicit non-defects: `ideal-dc-armature-ra`

**18 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

Ra is passed to Basic.Resistor, whose contract explicitly supports zero and signed resistance; zero removes armature copper loss. The partial machine source has no unconditional reciprocal of this parameter. A particular initialization can still be topology-dependent.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0707](../false-positives/DECL-0707.md) | — | `Ra` | Source/semantic review | [DECL-partialbasicdcmachine-ra-17.md](../../bugs/DECL-partialbasicdcmachine-ra-17.md) |
| [FINDING-01304](../false-positives/FINDING-01304.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcpm.Ra` | Source/semantic review | [FINDING-dc-comparecharacteristics-dcpm-ra-unbounded.md](../../bugs/FINDING-dc-comparecharacteristics-dcpm-ra-unbounded.md) |
| [FINDING-01322](../false-positives/FINDING-01322.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcee.Ra` | Source/semantic review | [FINDING-dc-comparecharacteristics-dcee-ra-unbounded.md](../../bugs/FINDING-dc-comparecharacteristics-dcee-ra-unbounded.md) |
| [FINDING-01340](../false-positives/FINDING-01340.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcse.Ra` | Source/semantic review | [FINDING-dc-comparecharacteristics-dcse-ra-unbounded.md](../../bugs/FINDING-dc-comparecharacteristics-dcse-ra-unbounded.md) |
| [FINDING-01361](../false-positives/FINDING-01361.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCEE_Start | `dcee.Ra` | Source/semantic review | [FINDING-dcee-start-dcee-ra-unbounded.md](../../bugs/FINDING-dcee-start-dcee-ra-unbounded.md) |
| [FINDING-01443](../false-positives/FINDING-01443.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_CurrentControlled | `dcpm.Ra` | Source/semantic review | [FINDING-dcpm-currentcontrolled-dcpm-ra-unbounded.md](../../bugs/FINDING-dcpm-currentcontrolled-dcpm-ra-unbounded.md) |
| [FINDING-01478](../false-positives/FINDING-01478.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpm1.Ra` | Source/semantic review | [FINDING-dcpm-drive-dcpm1-ra-unbounded.md](../../bugs/FINDING-dcpm-drive-dcpm1-ra-unbounded.md) |
| [FINDING-01487](../false-positives/FINDING-01487.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpm2.Ra` | Source/semantic review | [FINDING-dcpm-drive-dcpm2-ra-unbounded.md](../../bugs/FINDING-dcpm-drive-dcpm2-ra-unbounded.md) |
| [FINDING-01538](../false-positives/FINDING-01538.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpm1.Ra` | Source/semantic review | [FINDING-dcpm-quasistatic-dcpm1-ra-unbounded.md](../../bugs/FINDING-dcpm-quasistatic-dcpm1-ra-unbounded.md) |
| [FINDING-01550](../false-positives/FINDING-01550.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpm2.Ra` | Source/semantic review | [FINDING-dcpm-quasistatic-dcpm2-ra-unbounded.md](../../bugs/FINDING-dcpm-quasistatic-dcpm2-ra-unbounded.md) |
| [FINDING-01570](../false-positives/FINDING-01570.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Start | `dcpm.Ra` | Source/semantic review | [FINDING-dcpm-start-dcpm-ra-unbounded.md](../../bugs/FINDING-dcpm-start-dcpm-ra-unbounded.md) |
| [FINDING-01591](../false-positives/FINDING-01591.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Temperature | `dcpm.Ra` | Source/semantic review | [FINDING-dcpm-temperature-dcpm-ra-unbounded.md](../../bugs/FINDING-dcpm-temperature-dcpm-ra-unbounded.md) |
| [FINDING-01611](../false-positives/FINDING-01611.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpm1.Ra` | Source/semantic review | [FINDING-dcpm-withlosses-dcpm1-ra-unbounded.md](../../bugs/FINDING-dcpm-withlosses-dcpm1-ra-unbounded.md) |
| [FINDING-01621](../false-positives/FINDING-01621.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpm2.Ra` | Source/semantic review | [FINDING-dcpm-withlosses-dcpm2-ra-unbounded.md](../../bugs/FINDING-dcpm-withlosses-dcpm2-ra-unbounded.md) |
| [FINDING-01659](../false-positives/FINDING-01659.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_SinglePhase | `dcse.Ra` | Source/semantic review | [FINDING-dcse-singlephase-dcse-ra-unbounded.md](../../bugs/FINDING-dcse-singlephase-dcse-ra-unbounded.md) |
| [FINDING-01686](../false-positives/FINDING-01686.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_Start | `dcse.Ra` | Source/semantic review | [FINDING-dcse-start-dcse-ra-unbounded.md](../../bugs/FINDING-dcse-start-dcse-ra-unbounded.md) |
| [FINDING-03471](../false-positives/FINDING-03471.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive | `dcpm.Ra` | Source/semantic review | [FINDING-thyristorbridge2mpulse-dc-drive-dcpm-ra-unbounded.md](../../bugs/FINDING-thyristorbridge2mpulse-dc-drive-dcpm-ra-unbounded.md) |
| [FINDING-03663](../false-positives/FINDING-03663.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_DC_Drive | `dcpm.Ra` | Source/semantic review | [FINDING-thyristorbridge2pulse-dc-drive-dcpm-ra-unbounded.md](../../bugs/FINDING-thyristorbridge2pulse-dc-drive-dcpm-ra-unbounded.md) |
