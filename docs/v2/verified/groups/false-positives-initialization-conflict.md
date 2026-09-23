# False positives and explicit non-defects: `initialization-conflict`

**8 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

The nominal example runs. Recompiling with the reported zero removes a storage state and exposes inconsistent fixed initial equations, not an unavoidable reciprocal in the primitive component. Control Mass1 keeps the zero and relaxes the relevant fixed initial conditions; it simulates successfully. The exact original trigger does fail, but its attribution to a generally invalid library min=0 is false. Fix the example initialization or constrain this particular example if it must retain those starts.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [BUG-001](../false-positives/BUG-001.md) | Modelica.Mechanics.Translational.Examples.Damper | `mass1.m` | Prior paired execution | [BUG-damper-mass1-m.md](../../bugs/BUG-damper-mass1-m.md) |
| [BUG-003](../false-positives/BUG-003.md) | Modelica.Mechanics.Translational.Examples.Damper | `mass2.m` | Prior paired execution | [BUG-damper-mass2-m.md](../../bugs/BUG-damper-mass2-m.md) |
| [BUG-007](../false-positives/BUG-007.md) | Modelica.Mechanics.Translational.Examples.Damper | `mass3.m` | Prior paired execution | [BUG-damper-mass3-m.md](../../bugs/BUG-damper-mass3-m.md) |
| [BUG-009](../false-positives/BUG-009.md) | Modelica.Electrical.Analog.Examples.ParallelResonance | `capacitor2.C` | Prior paired execution | [BUG-parallelresonance-capacitor2-c.md](../../bugs/BUG-parallelresonance-capacitor2-c.md) |
| [BUG-013](../false-positives/BUG-013.md) | Modelica.Electrical.Analog.Examples.ChuaCircuit | `C1.C` | Prior paired execution | [BUG-chuacircuit-c1-c.md](../../bugs/BUG-chuacircuit-c1-c.md) |
| [BUG-014](../false-positives/BUG-014.md) | Modelica.Electrical.Analog.Examples.ChuaCircuit | `C2.C` | Prior paired execution | [BUG-chuacircuit-c2-c.md](../../bugs/BUG-chuacircuit-c2-c.md) |
| [BUG-015](../false-positives/BUG-015.md) | Modelica.Mechanics.Rotational.Examples.ElasticBearing | `shaft.J` | Prior paired execution | [BUG-elasticbearing-shaft-j.md](../../bugs/BUG-elasticbearing-shaft-j.md) |
| [BUG-017](../false-positives/BUG-017.md) | Modelica.Mechanics.Translational.Examples.WhyArrows | `inertia2.m` | Prior paired execution | [BUG-whyarrows-inertia2-m.md](../../bugs/BUG-whyarrows-inertia2-m.md) |
