# Execution-confirmed defects: `trapezoid-frequency`

**1 report instances**

[Back to Execution-confirmed defects](../confirmed.md) · [Overview](../README.md)

## Common decision rule

The source uses f directly in trapezoid timing (rising=0.2/f, width=0.3/f, falling=0.2/f, period=1/f). f=0 is not handled and gives undefined parameter bindings. Rumoca reports non-finite evaluation after a clean baseline. OpenModelica baseline-executable overrides also report zero division; recompilation can instead hit a template/code-generation error, which is not counted as independent runtime confirmation.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [BUG-006](../confirmed/BUG-006.md) | Modelica.Electrical.Analog.Examples.InvertingAmp | `f` | Prior paired execution | [BUG-invertingamp-f.md](../../bugs/BUG-invertingamp-f.md) |
