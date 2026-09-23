# Multivibrator capacitance formula has zero divisors

Group `multivibrator-design` · 11 report instances · confirmed

C=1/f/(2*R*log(1+2*R1/R2)). f=0 or R=0 zeros a factor, R2=0 divides inside the logarithm, and R1=0 makes log(1)=0. All four witnesses fail independently after successful baselines, including final-evaluated recompilation.

Validate strictly positive f,R,R1,R2 for this positive-resistance oscillator design before computing C; guard the derived expression and issue a clear domain assertion. If other sign combinations are supported, validate both the logarithm argument and the complete denominator explicitly.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0620](../confirmed/DECL-0620.md) | — | `R1` |
| [DECL-0621](../confirmed/DECL-0621.md) | — | `R2` |
| [DECL-0622](../confirmed/DECL-0622.md) | — | `R` |
| [FINDING-00866](../confirmed/FINDING-00866.md) | Modelica.Electrical.Analog.Examples.OpAmps.Multivibrator | `R1` |
| [FINDING-00867](../confirmed/FINDING-00867.md) | Modelica.Electrical.Analog.Examples.OpAmps.Multivibrator | `R2` |
| [FINDING-00868](../confirmed/FINDING-00868.md) | Modelica.Electrical.Analog.Examples.OpAmps.Multivibrator | `R` |
| [FINDING-00871](../confirmed/FINDING-00871.md) | Modelica.Electrical.Analog.Examples.OpAmps.Multivibrator | `R` |
| [FINDING-00872](../confirmed/FINDING-00872.md) | Modelica.Electrical.Analog.Examples.OpAmps.Multivibrator | `R1` |
| [FINDING-00873](../confirmed/FINDING-00873.md) | Modelica.Electrical.Analog.Examples.OpAmps.Multivibrator | `R2` |
| [FINDING-00874](../confirmed/FINDING-00874.md) | Modelica.Electrical.Analog.Examples.OpAmps.Multivibrator | `f` |
| [FINDING-00875](../confirmed/FINDING-00875.md) | Modelica.Electrical.Analog.Examples.OpAmps.Multivibrator | `R2` |
