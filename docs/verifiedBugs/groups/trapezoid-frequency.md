# Example waveform timing divides by zero frequency

Group `trapezoid-frequency` · 19 report instances · confirmed

The source uses f directly in trapezoid timing (rising=0.2/f, width=0.3/f, falling=0.2/f, period=1/f). f=0 is not handled and gives undefined parameter bindings. Rumoca reports non-finite evaluation after a clean baseline. OpenModelica baseline-executable overrides also report zero division; recompilation can instead hit a template/code-generation error, which is not counted as independent runtime confirmation.

At the example frequency declaration, specify and assert f>0 and guard the timing calculations so the assertion can diagnose invalid input. If f=0 should mean DC, provide an explicit DC branch; do not silently clamp frequency to epsilon.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [BUG-006](../confirmed/BUG-006.md) | Modelica.Electrical.Analog.Examples.InvertingAmp | `f` |
| [FINDING-00362](../confirmed/FINDING-00362.md) | Modelica.Electrical.Analog.Examples.InvertingAmp | `f` |
| [FINDING-00363](../confirmed/FINDING-00363.md) | Modelica.Electrical.Analog.Examples.InvertingAmp | `f` |
| [FINDING-00780](../confirmed/FINDING-00780.md) | Modelica.Electrical.Analog.Examples.OpAmps.Comparator | `f` |
| [FINDING-00782](../confirmed/FINDING-00782.md) | Modelica.Electrical.Analog.Examples.OpAmps.Comparator | `f` |
| [FINDING-00817](../confirmed/FINDING-00817.md) | Modelica.Electrical.Analog.Examples.OpAmps.Differentiator | `f` |
| [FINDING-00818](../confirmed/FINDING-00818.md) | Modelica.Electrical.Analog.Examples.OpAmps.Differentiator | `f` |
| [FINDING-00824](../confirmed/FINDING-00824.md) | Modelica.Electrical.Analog.Examples.OpAmps.HighPass | `f` |
| [FINDING-00827](../confirmed/FINDING-00827.md) | Modelica.Electrical.Analog.Examples.OpAmps.HighPass | `f` |
| [FINDING-00831](../confirmed/FINDING-00831.md) | Modelica.Electrical.Analog.Examples.OpAmps.Integrator | `f` |
| [FINDING-00834](../confirmed/FINDING-00834.md) | Modelica.Electrical.Analog.Examples.OpAmps.Integrator | `f` |
| [FINDING-00837](../confirmed/FINDING-00837.md) | Modelica.Electrical.Analog.Examples.OpAmps.InvertingAmplifier | `f` |
| [FINDING-00838](../confirmed/FINDING-00838.md) | Modelica.Electrical.Analog.Examples.OpAmps.InvertingAmplifier | `f` |
| [FINDING-00862](../confirmed/FINDING-00862.md) | Modelica.Electrical.Analog.Examples.OpAmps.LowPass | `f` |
| [FINDING-00865](../confirmed/FINDING-00865.md) | Modelica.Electrical.Analog.Examples.OpAmps.LowPass | `f` |
| [FINDING-00878](../confirmed/FINDING-00878.md) | Modelica.Electrical.Analog.Examples.OpAmps.NonInvertingAmplifier | `f` |
| [FINDING-00879](../confirmed/FINDING-00879.md) | Modelica.Electrical.Analog.Examples.OpAmps.NonInvertingAmplifier | `f` |
| [FINDING-00936](../confirmed/FINDING-00936.md) | Modelica.Electrical.Analog.Examples.OpAmps.VoltageFollower | `f` |
| [FINDING-00937](../confirmed/FINDING-00937.md) | Modelica.Electrical.Analog.Examples.OpAmps.VoltageFollower | `f` |
