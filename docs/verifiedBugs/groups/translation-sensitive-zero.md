# Runtime override does not prove a missing library bound

Group `translation-sensitive-zero` · 7 report instances · false-positives

The historical runtime-override failure reproduces, but the exact reported model simulates successfully when the same zero is set as a final parameter before translation with final-parameter evaluation enabled. The alleged unavoidable divide-by-zero is introduced by the chosen solved/state representation. This refutes the claimed necessity of globally banning zero; it does not promise every connected topology or tunable override is valid.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [BUG-002](../false-positives/BUG-002.md) | Modelica.Clocked.Examples.SimpleControlledDrive.Continuous | `load.J` |
| [BUG-004](../false-positives/BUG-004.md) | Modelica.Electrical.Analog.Examples.ParallelResonance | `inductor1.L` |
| [BUG-005](../false-positives/BUG-005.md) | Modelica.Electrical.Analog.Examples.ParallelResonance | `inductor2.L` |
| [BUG-008](../false-positives/BUG-008.md) | Modelica.Electrical.Analog.Examples.ParallelResonance | `capacitor1.C` |
| [BUG-012](../false-positives/BUG-012.md) | Modelica.Electrical.Analog.Examples.ChuaCircuit | `L.L` |
| [BUG-016](../false-positives/BUG-016.md) | Modelica.Mechanics.Rotational.Examples.ElasticBearing | `housing.J` |
| [BUG-026](../false-positives/BUG-026.md) | Modelica.Mechanics.Rotational.Examples.ElasticBearing | `idealGear.ratio` |
