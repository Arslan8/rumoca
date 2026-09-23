# Static/source-supported candidates: `oscillator-design`

**4 report instances**

[Back to Static/source-supported candidates](../candidates.md) · [Overview](../README.md)

## Common decision rule

The source computes C=1/((2*pi*f)^2*L) and gamma=(1-A)/(2*R*C). Setting the reported design parameter to zero makes an explicit denominator zero. This is separate from the zero-storage behavior of Basic.Capacitor/Inductor. The nominal example passes; the selected design-parameter perturbation fails.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0114](../candidate/DECL-0114.md) | — | `L` | Source/semantic review | [DECL-lcoscillator-l-8.md](../../bugs/DECL-lcoscillator-l-8.md) |
| [DECL-0617](../candidate/DECL-0617.md) | — | `R` | Source/semantic review | [DECL-lcoscillator-r-10.md](../../bugs/DECL-lcoscillator-r-10.md) |
| [FINDING-00924](../candidate/FINDING-00924.md) | Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator | `L` | OMC: `witness-admitted-with-warning` | [FINDING-lcoscillator-l-unbounded.md](../../bugs/FINDING-lcoscillator-l-unbounded.md) |
| [FINDING-00926](../candidate/FINDING-00926.md) | Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator | `R` | OMC: `witness-executes-cleanly` | [FINDING-lcoscillator-r-unbounded.md](../../bugs/FINDING-lcoscillator-r-unbounded.md) |
