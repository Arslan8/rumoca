# False positives and explicit non-defects: `ideal-dc-machine-data`

**18 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

This field represents zero armature inductance and is forwarded to a component that uses it multiplicatively: torque balance for inertia, v=R*i for resistance, or v=L*der(i) for inductance. None intrinsically requires division by the field. A specific drive train can still be inconsistent; the missing strictly-positive record bound alone is not a bug.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0159](../false-positives/DECL-0159.md) | — | `La` | Source/semantic review | [DECL-dcpermanentmagnetdata-la-28.md](../../bugs/DECL-dcpermanentmagnetdata-la-28.md) |
| [DECL-0318](../false-positives/DECL-0318.md) | — | `Jr` | Source/semantic review | [DECL-dcpermanentmagnetdata-jr-5.md](../../bugs/DECL-dcpermanentmagnetdata-jr-5.md) |
| [DECL-0319](../false-positives/DECL-0319.md) | — | `Js` | Source/semantic review | [DECL-dcpermanentmagnetdata-js-6.md](../../bugs/DECL-dcpermanentmagnetdata-js-6.md) |
| [DECL-0713](../false-positives/DECL-0713.md) | — | `Ra` | Source/semantic review | [DECL-dcpermanentmagnetdata-ra-19.md](../../bugs/DECL-dcpermanentmagnetdata-ra-19.md) |
| [FINDING-01300](../false-positives/FINDING-01300.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcpmData.Ra` | Source/semantic review | [FINDING-dc-comparecharacteristics-dcpmdata-ra-unbounded.md](../../bugs/FINDING-dc-comparecharacteristics-dcpmdata-ra-unbounded.md) |
| [FINDING-01314](../false-positives/FINDING-01314.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dceeData.Ra` | Source/semantic review | [FINDING-dc-comparecharacteristics-dceedata-ra-unbounded.md](../../bugs/FINDING-dc-comparecharacteristics-dceedata-ra-unbounded.md) |
| [FINDING-01332](../false-positives/FINDING-01332.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcseData.Ra` | Source/semantic review | [FINDING-dc-comparecharacteristics-dcsedata-ra-unbounded.md](../../bugs/FINDING-dc-comparecharacteristics-dcsedata-ra-unbounded.md) |
| [FINDING-01375](../false-positives/FINDING-01375.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCEE_Start | `dceeData.Ra` | Source/semantic review | [FINDING-dcee-start-dceedata-ra-unbounded.md](../../bugs/FINDING-dcee-start-dceedata-ra-unbounded.md) |
| [FINDING-01418](../false-positives/FINDING-01418.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `dcpmData.Ra` | Source/semantic review | [FINDING-dcpm-cooling-dcpmdata-ra-unbounded.md](../../bugs/FINDING-dcpm-cooling-dcpmdata-ra-unbounded.md) |
| [FINDING-01476](../false-positives/FINDING-01476.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpmData.Ra` | Source/semantic review | [FINDING-dcpm-drive-dcpmdata-ra-unbounded.md](../../bugs/FINDING-dcpm-drive-dcpmdata-ra-unbounded.md) |
| [FINDING-01560](../false-positives/FINDING-01560.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpmData.Ra` | Source/semantic review | [FINDING-dcpm-quasistatic-dcpmdata-ra-unbounded.md](../../bugs/FINDING-dcpm-quasistatic-dcpmdata-ra-unbounded.md) |
| [FINDING-01582](../false-positives/FINDING-01582.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Start | `dcpmData.Ra` | Source/semantic review | [FINDING-dcpm-start-dcpmdata-ra-unbounded.md](../../bugs/FINDING-dcpm-start-dcpmdata-ra-unbounded.md) |
| [FINDING-01603](../false-positives/FINDING-01603.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Temperature | `dcpmData.Ra` | Source/semantic review | [FINDING-dcpm-temperature-dcpmdata-ra-unbounded.md](../../bugs/FINDING-dcpm-temperature-dcpmdata-ra-unbounded.md) |
| [FINDING-01635](../false-positives/FINDING-01635.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpmData1.Ra` | Source/semantic review | [FINDING-dcpm-withlosses-dcpmdata1-ra-unbounded.md](../../bugs/FINDING-dcpm-withlosses-dcpmdata1-ra-unbounded.md) |
| [FINDING-01673](../false-positives/FINDING-01673.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_SinglePhase | `dcseData.Ra` | Source/semantic review | [FINDING-dcse-singlephase-dcsedata-ra-unbounded.md](../../bugs/FINDING-dcse-singlephase-dcsedata-ra-unbounded.md) |
| [FINDING-01700](../false-positives/FINDING-01700.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_Start | `dcseData.Ra` | Source/semantic review | [FINDING-dcse-start-dcsedata-ra-unbounded.md](../../bugs/FINDING-dcse-start-dcsedata-ra-unbounded.md) |
| [FINDING-03482](../false-positives/FINDING-03482.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive | `dcpmData.Ra` | Source/semantic review | [FINDING-thyristorbridge2mpulse-dc-drive-dcpmdata-ra-unbounded.md](../../bugs/FINDING-thyristorbridge2mpulse-dc-drive-dcpmdata-ra-unbounded.md) |
| [FINDING-03674](../false-positives/FINDING-03674.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_DC_Drive | `dcpmData.Ra` | Source/semantic review | [FINDING-thyristorbridge2pulse-dc-drive-dcpmdata-ra-unbounded.md](../../bugs/FINDING-thyristorbridge2pulse-dc-drive-dcpmdata-ra-unbounded.md) |
