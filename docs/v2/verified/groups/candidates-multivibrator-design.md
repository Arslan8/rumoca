# Static/source-supported candidates: `multivibrator-design`

**5 report instances**

[Back to Static/source-supported candidates](../candidates.md) · [Overview](../README.md)

## Common decision rule

C=1/f/(2*R*log(1+2*R1/R2)). f=0 or R=0 zeros a factor, R2=0 divides inside the logarithm, and R1=0 makes log(1)=0. All four witnesses fail independently after successful baselines, including final-evaluated recompilation.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0620](../candidate/DECL-0620.md) | — | `R1` | Source/semantic review | [DECL-multivibrator-r1-7.md](../../bugs/DECL-multivibrator-r1-7.md) |
| [DECL-0621](../candidate/DECL-0621.md) | — | `R2` | Source/semantic review | [DECL-multivibrator-r2-8.md](../../bugs/DECL-multivibrator-r2-8.md) |
| [DECL-0622](../candidate/DECL-0622.md) | — | `R` | Source/semantic review | [DECL-multivibrator-r-9.md](../../bugs/DECL-multivibrator-r-9.md) |
| [FINDING-00954](../candidate/FINDING-00954.md) | Modelica.Electrical.Analog.Examples.OpAmps.Multivibrator | `R1` | OMC: `witness-admitted-with-warning` | [FINDING-multivibrator-r1-unbounded.md](../../bugs/FINDING-multivibrator-r1-unbounded.md) |
| [FINDING-00956](../candidate/FINDING-00956.md) | Modelica.Electrical.Analog.Examples.OpAmps.Multivibrator | `R` | OMC: `witness-admitted-with-warning` | [FINDING-multivibrator-r-unbounded.md](../../bugs/FINDING-multivibrator-r-unbounded.md) |
