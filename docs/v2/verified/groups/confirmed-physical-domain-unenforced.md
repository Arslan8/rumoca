# Execution-confirmed defects: `physical-domain-unenforced`

**1 report instances**

[Back to Execution-confirmed defects](../confirmed.md) · [Overview](../README.md)

## Common decision rule

The reviewed component-specific physical contract excludes the reported value. With the exact zero or negative witness encoded before translation, the unmodified model ran cleanly and OpenModelica reproduced a numerical failure.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [FINDING-00955](../confirmed/FINDING-00955.md) | Modelica.Electrical.Analog.Examples.OpAmps.Multivibrator | `R2` | OMC: `witness-causes-omc-numerical-failure` | [FINDING-multivibrator-r2-unbounded.md](../../bugs/FINDING-multivibrator-r2-unbounded.md) |
