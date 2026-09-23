# Zero-storage example has incompatible fixed initial conditions

Group `initialization-conflict` · 8 report instances · false-positives

The nominal example runs. Recompiling with the reported zero removes a storage state and exposes inconsistent fixed initial equations, not an unavoidable reciprocal in the primitive component. Control Mass1 keeps the zero and relaxes the relevant fixed initial conditions; it simulates successfully. The exact original trigger does fail, but its attribution to a generally invalid library min=0 is false. Fix the example initialization or constrain this particular example if it must retain those starts.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [BUG-001](../false-positives/BUG-001.md) | Modelica.Mechanics.Translational.Examples.Damper | `mass1.m` |
| [BUG-003](../false-positives/BUG-003.md) | Modelica.Mechanics.Translational.Examples.Damper | `mass2.m` |
| [BUG-007](../false-positives/BUG-007.md) | Modelica.Mechanics.Translational.Examples.Damper | `mass3.m` |
| [BUG-009](../false-positives/BUG-009.md) | Modelica.Electrical.Analog.Examples.ParallelResonance | `capacitor2.C` |
| [BUG-013](../false-positives/BUG-013.md) | Modelica.Electrical.Analog.Examples.ChuaCircuit | `C1.C` |
| [BUG-014](../false-positives/BUG-014.md) | Modelica.Electrical.Analog.Examples.ChuaCircuit | `C2.C` |
| [BUG-015](../false-positives/BUG-015.md) | Modelica.Mechanics.Rotational.Examples.ElasticBearing | `shaft.J` |
| [BUG-017](../false-positives/BUG-017.md) | Modelica.Mechanics.Translational.Examples.WhyArrows | `inertia2.m` |
