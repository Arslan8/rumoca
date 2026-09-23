# Filter cutoff frequency divides by zero

Group `cutoff-frequency` · 2 report instances · confirmed

The component is instantiated with T=1/(2*pi*fG). fG=0 gives a literal zero denominator and no finite time constant. Both engines fail after clean baselines; OpenModelica also fails with final-evaluated fG=0.

Require and assert fG>0 at the example design interface; guard the T calculation. If a zero-cutoff limiting filter is wanted, implement its limiting equations separately.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-00825](../confirmed/FINDING-00825.md) | Modelica.Electrical.Analog.Examples.OpAmps.HighPass | `fG` |
| [FINDING-00863](../confirmed/FINDING-00863.md) | Modelica.Electrical.Analog.Examples.OpAmps.LowPass | `fG` |
