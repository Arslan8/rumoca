# LC oscillator design divides by zero

Group `oscillator-design` · 10 report instances · confirmed

The source computes C=1/((2*pi*f)^2*L) and gamma=(1-A)/(2*R*C). Setting the reported design parameter to zero makes an explicit denominator zero. This is separate from the zero-storage behavior of Basic.Capacitor/Inductor. The nominal example passes; the selected design-parameter perturbation fails.

Validate f>0, L>0, C>0 and R>0 at this example/design layer, with guarded derived-parameter calculations and actionable assertions. Do not prohibit zero in every primitive capacitor/inductor/resistor.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0114](../confirmed/DECL-0114.md) | — | `L` |
| [DECL-0617](../confirmed/DECL-0617.md) | — | `R` |
| [FINDING-00846](../confirmed/FINDING-00846.md) | Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator | `L` |
| [FINDING-00847](../confirmed/FINDING-00847.md) | Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator | `C` |
| [FINDING-00848](../confirmed/FINDING-00848.md) | Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator | `R` |
| [FINDING-00853](../confirmed/FINDING-00853.md) | Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator | `f` |
| [FINDING-00854](../confirmed/FINDING-00854.md) | Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator | `L` |
| [FINDING-00855](../confirmed/FINDING-00855.md) | Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator | `R` |
| [FINDING-00856](../confirmed/FINDING-00856.md) | Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator | `f` |
| [FINDING-00857](../confirmed/FINDING-00857.md) | Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator | `L` |
