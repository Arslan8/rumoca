# CriticalDamping accepts zero order then divides by it

Group `critical-damping-order` · 8 report instances · confirmed

CriticalDamping declares Integer n=2 without min=1. It computes alpha=sqrt(2^(1/n)-1), allocates x[n], and indexes x[1] and x[n]. n=0 therefore causes division/index/domain failures. Filter order is structurally required to be at least one.

Declare n(min=1)=2 and retain an explicit assertion for tools that do not enforce parameter bounds before structural evaluation. Ensure array dimensions and alpha are never evaluated for invalid n.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-00018](../confirmed/FINDING-00018.md) | Modelica.Clocked.Examples.Systems.Utilities.ComponentsMixingUnit.MixingUnitWithContinuousControl | `filter.n` |
| [FINDING-00020](../confirmed/FINDING-00020.md) | Modelica.Clocked.Examples.Systems.Utilities.ComponentsMixingUnit.MixingUnitWithContinuousControl | `filter.n` |
| [FINDING-04784](../confirmed/FINDING-04784.md) | ModelicaTest.Blocks.Continuous | `criticalDamping.n` |
| [FINDING-04786](../confirmed/FINDING-04786.md) | ModelicaTest.Blocks.Continuous | `criticalDamping.n` |
| [FINDING-04797](../confirmed/FINDING-04797.md) | ModelicaTest.Blocks.Continuous_SteadyState | `criticalDamping.n` |
| [FINDING-04799](../confirmed/FINDING-04799.md) | ModelicaTest.Blocks.Continuous_SteadyState | `criticalDamping.n` |
| [FINDING-04810](../confirmed/FINDING-04810.md) | ModelicaTest.Blocks.Continuous_InitialState | `criticalDamping.n` |
| [FINDING-04812](../confirmed/FINDING-04812.md) | ModelicaTest.Blocks.Continuous_InitialState | `criticalDamping.n` |
