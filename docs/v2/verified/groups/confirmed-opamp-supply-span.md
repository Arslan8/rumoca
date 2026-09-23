# Execution-confirmed defects: `opamp-supply-span`

**1 report instances**

[Back to Execution-confirmed defects](../confirmed.md) · [Overview](../README.md)

## Common decision rule

The source defines i_s = p_s/(vps-vns) with no nonzero-span assertion. In LCOscillator and Comparator, Vns=-15; setting Vps=-15 makes the denominator exactly zero. The correct equality witness is -15, not Vps=0. Both nominal examples pass; the actual equality fails in Rumoca and in ordinary and final-evaluated OpenModelica models.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [BUG-024](../confirmed/BUG-024.md) | Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator | `opAmp.Vps` | Prior paired execution | [BUG-lcoscillator-opamp-vps.md](../../bugs/BUG-lcoscillator-opamp-vps.md) |
