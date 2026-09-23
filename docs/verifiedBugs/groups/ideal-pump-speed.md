# IdealPump permits zero nominal speed then divides by it

Group `ideal-pump-speed` · 2 report instances · confirmed

IdealPump declares wNominal without a positive bound and evaluates both w/wNominal and a flow characteristic derived from it. Zero is admitted but undefined even though the low-actual-speed runtime branch is guarded; the nominal scale is evaluated before that branch can make it safe.

Require wNominal>0 (or a documented nonzero signed convention) and assert it before pump-characteristic evaluation. Guard derived ratios so invalid configuration produces one clear parameter error.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-04625](../confirmed/FINDING-04625.md) | Modelica.Thermal.FluidHeatFlow.Examples.PumpAndValve | `idealPump.wNominal` |
| [FINDING-04739](../confirmed/FINDING-04739.md) | Modelica.Thermal.FluidHeatFlow.Examples.WaterPump | `idealPump.wNominal` |
