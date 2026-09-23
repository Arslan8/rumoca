# unitTime is an immutable nonzero unit constant

Group `constant-unit-time` · 11 report instances · false-positives

unitTime is declared constant SI.Time unitTime=1 and exists only to satisfy unit checking in ratios. It is not a tunable parameter and cannot take the proposed zero witness. Treating it as a reachable divisor is a role-classification false positive.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-04781](../false-positives/FINDING-04781.md) | ModelicaTest.Blocks.Continuous | `pID.unitTime` |
| [FINDING-04782](../false-positives/FINDING-04782.md) | ModelicaTest.Blocks.Continuous | `limPID.unitTime` |
| [FINDING-04794](../false-positives/FINDING-04794.md) | ModelicaTest.Blocks.Continuous_SteadyState | `pID.unitTime` |
| [FINDING-04795](../false-positives/FINDING-04795.md) | ModelicaTest.Blocks.Continuous_SteadyState | `limPID.unitTime` |
| [FINDING-04807](../false-positives/FINDING-04807.md) | ModelicaTest.Blocks.Continuous_InitialState | `pID.unitTime` |
| [FINDING-04808](../false-positives/FINDING-04808.md) | ModelicaTest.Blocks.Continuous_InitialState | `limPID.unitTime` |
| [FINDING-04815](../false-positives/FINDING-04815.md) | ModelicaTest.Blocks.StrictLimiters | `PID1.unitTime` |
| [FINDING-04817](../false-positives/FINDING-04817.md) | ModelicaTest.Blocks.StrictLimiters | `PID2.unitTime` |
| [FINDING-04841](../false-positives/FINDING-04841.md) | ModelicaTest.Blocks.UnitDeduction | `PID.unitTime` |
| [FINDING-04842](../false-positives/FINDING-04842.md) | ModelicaTest.Blocks.UnitDeduction | `PID1.unitTime` |
| [FINDING-05121](../false-positives/FINDING-05121.md) | PIDMSL | `pid.unitTime` |
