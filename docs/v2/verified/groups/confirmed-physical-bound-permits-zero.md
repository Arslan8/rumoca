# Execution-confirmed defects: `physical-bound-permits-zero`

**1 report instances**

[Back to Execution-confirmed defects](../confirmed.md) · [Overview](../README.md)

## Common decision rule

The reviewed component-specific physical contract excludes the reported value. With the exact zero or negative witness encoded before translation, the unmodified model ran cleanly and OpenModelica reproduced a numerical failure.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [FINDING-00925](../confirmed/FINDING-00925.md) | Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator | `C` | OMC: `witness-causes-omc-numerical-failure` | [FINDING-lcoscillator-c-bound.md](../../bugs/FINDING-lcoscillator-c-bound.md) |
