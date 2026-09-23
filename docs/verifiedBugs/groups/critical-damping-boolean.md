# normalized=false selects a safe explicit branch

Group `critical-damping-boolean` · 4 report instances · false-positives

normalized is Boolean, not a numeric divisor. The binding is alpha=if normalized then sqrt(2^(1/n)-1) else 1.0. Setting it false makes alpha exactly one, so the later division by alpha remains safe. The detector confused branch control with denominator data.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-00019](../false-positives/FINDING-00019.md) | Modelica.Clocked.Examples.Systems.Utilities.ComponentsMixingUnit.MixingUnitWithContinuousControl | `filter.normalized` |
| [FINDING-04785](../false-positives/FINDING-04785.md) | ModelicaTest.Blocks.Continuous | `criticalDamping.normalized` |
| [FINDING-04798](../false-positives/FINDING-04798.md) | ModelicaTest.Blocks.Continuous_SteadyState | `criticalDamping.normalized` |
| [FINDING-04811](../false-positives/FINDING-04811.md) | ModelicaTest.Blocks.Continuous_InitialState | `criticalDamping.normalized` |
