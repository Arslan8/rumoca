# False positives and explicit non-defects: `translation-sensitive-zero`

**7 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

The historical runtime-override failure reproduces, but the exact reported model simulates successfully when the same zero is set as a final parameter before translation with final-parameter evaluation enabled. The alleged unavoidable divide-by-zero is introduced by the chosen solved/state representation. This refutes the claimed necessity of globally banning zero; it does not promise every connected topology or tunable override is valid.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [BUG-002](../false-positives/BUG-002.md) | Modelica.Clocked.Examples.SimpleControlledDrive.Continuous | `load.J` | Prior paired execution | [BUG-continuous-load-j.md](../../bugs/BUG-continuous-load-j.md) |
| [BUG-004](../false-positives/BUG-004.md) | Modelica.Electrical.Analog.Examples.ParallelResonance | `inductor1.L` | Prior paired execution | [BUG-parallelresonance-inductor1-l.md](../../bugs/BUG-parallelresonance-inductor1-l.md) |
| [BUG-005](../false-positives/BUG-005.md) | Modelica.Electrical.Analog.Examples.ParallelResonance | `inductor2.L` | Prior paired execution | [BUG-parallelresonance-inductor2-l.md](../../bugs/BUG-parallelresonance-inductor2-l.md) |
| [BUG-008](../false-positives/BUG-008.md) | Modelica.Electrical.Analog.Examples.ParallelResonance | `capacitor1.C` | Prior paired execution | [BUG-parallelresonance-capacitor1-c.md](../../bugs/BUG-parallelresonance-capacitor1-c.md) |
| [BUG-012](../false-positives/BUG-012.md) | Modelica.Electrical.Analog.Examples.ChuaCircuit | `L.L` | Prior paired execution | [BUG-chuacircuit-l-l.md](../../bugs/BUG-chuacircuit-l-l.md) |
| [BUG-016](../false-positives/BUG-016.md) | Modelica.Mechanics.Rotational.Examples.ElasticBearing | `housing.J` | Prior paired execution | [BUG-elasticbearing-housing-j.md](../../bugs/BUG-elasticbearing-housing-j.md) |
| [BUG-026](../false-positives/BUG-026.md) | Modelica.Mechanics.Rotational.Examples.ElasticBearing | `idealGear.ratio` | Prior paired execution | [BUG-elasticbearing-idealgear-ratio.md](../../bugs/BUG-elasticbearing-idealgear-ratio.md) |
