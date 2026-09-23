# Not yet established as a bug or a false positive

Group `needs-semantic-proof` · 31 report instances · unresolved

The nominal Rumoca run passes. Available perturbation outcomes are listed below, but no reviewed proof yet connects this exact claim to an unguarded invalid equation or refutes it. A failed post-translation override may change model structure; a passing zero probe alone does not prove the complete parameter domain safe.

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-00360](../unresolved/FINDING-00360.md) | Modelica.Electrical.Analog.Examples.InvertingAmp | `R1` |
| [FINDING-00361](../unresolved/FINDING-00361.md) | Modelica.Electrical.Analog.Examples.InvertingAmp | `R2` |
| [FINDING-00778](../unresolved/FINDING-00778.md) | Modelica.Electrical.Analog.Examples.OpAmps.Comparator | `R` |
| [FINDING-00779](../unresolved/FINDING-00779.md) | Modelica.Electrical.Analog.Examples.OpAmps.Comparator | `potentiometer.R` |
| [FINDING-00783](../unresolved/FINDING-00783.md) | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit | `feedbackA.R1` |
| [FINDING-00784](../unresolved/FINDING-00784.md) | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit | `feedbackA.R3` |
| [FINDING-00786](../unresolved/FINDING-00786.md) | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit | `PIA.R2` |
| [FINDING-00787](../unresolved/FINDING-00787.md) | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit | `PIA.C` |
| [FINDING-00789](../unresolved/FINDING-00789.md) | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit | `firstOrder1A.R1` |
| [FINDING-00791](../unresolved/FINDING-00791.md) | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit | `firstOrder1A.C` |
| [FINDING-00793](../unresolved/FINDING-00793.md) | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit | `addA.R` |
| [FINDING-00794](../unresolved/FINDING-00794.md) | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit | `addA.R1` |
| [FINDING-00795](../unresolved/FINDING-00795.md) | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit | `addA.R2` |
| [FINDING-00796](../unresolved/FINDING-00796.md) | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit | `firstOrder2A.R1` |
| [FINDING-00798](../unresolved/FINDING-00798.md) | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit | `firstOrder2A.C` |
| [FINDING-00815](../unresolved/FINDING-00815.md) | Modelica.Electrical.Analog.Examples.OpAmps.Differentiator | `der_.C` |
| [FINDING-00821](../unresolved/FINDING-00821.md) | Modelica.Electrical.Analog.Examples.OpAmps.HighPass | `derivative.R2` |
| [FINDING-00822](../unresolved/FINDING-00822.md) | Modelica.Electrical.Analog.Examples.OpAmps.HighPass | `derivative.C` |
| [FINDING-00829](../unresolved/FINDING-00829.md) | Modelica.Electrical.Analog.Examples.OpAmps.Integrator | `integrator.C` |
| [FINDING-00835](../unresolved/FINDING-00835.md) | Modelica.Electrical.Analog.Examples.OpAmps.InvertingAmplifier | `gain.R1` |
| [FINDING-00836](../unresolved/FINDING-00836.md) | Modelica.Electrical.Analog.Examples.OpAmps.InvertingAmplifier | `gain.R2` |
| [FINDING-00849](../unresolved/FINDING-00849.md) | Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator | `R1` |
| [FINDING-00850](../unresolved/FINDING-00850.md) | Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator | `R2` |
| [FINDING-00858](../unresolved/FINDING-00858.md) | Modelica.Electrical.Analog.Examples.OpAmps.LowPass | `firstOrder.R1` |
| [FINDING-00860](../unresolved/FINDING-00860.md) | Modelica.Electrical.Analog.Examples.OpAmps.LowPass | `firstOrder.C` |
| [FINDING-00869](../unresolved/FINDING-00869.md) | Modelica.Electrical.Analog.Examples.OpAmps.Multivibrator | `C` |
| [FINDING-00876](../unresolved/FINDING-00876.md) | Modelica.Electrical.Analog.Examples.OpAmps.NonInvertingAmplifier | `buffer.R1` |
| [FINDING-00934](../unresolved/FINDING-00934.md) | Modelica.Electrical.Analog.Examples.OpAmps.VoltageFollower | `Ri` |
| [FINDING-00935](../unresolved/FINDING-00935.md) | Modelica.Electrical.Analog.Examples.OpAmps.VoltageFollower | `Rl` |
| [FINDING-04375](../unresolved/FINDING-04375.md) | Modelica.Mechanics.Rotational.Examples.CompareBrakingTorque | `J` |
| [FINDING-04418](../unresolved/FINDING-04418.md) | Modelica.Mechanics.Translational.Examples.CompareBrakingForce | `m` |
