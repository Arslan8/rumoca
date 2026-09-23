# Zero derivative time is explicitly handled

Group `guarded-zero-derivative-time` · 11 report instances · false-positives

Td has min=0. The derivative gain is Td/unitTime (Td is the numerator), while its filter time is max(Td/Nd, a strictly positive epsilon). Thus Td=0 disables the derivative contribution without producing a zero denominator. The report follows dependency reach rather than the complete guarded expression.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-04775](../false-positives/FINDING-04775.md) | ModelicaTest.Blocks.Continuous | `pID.Td` |
| [FINDING-04776](../false-positives/FINDING-04776.md) | ModelicaTest.Blocks.Continuous | `limPID.Td` |
| [FINDING-04788](../false-positives/FINDING-04788.md) | ModelicaTest.Blocks.Continuous_SteadyState | `pID.Td` |
| [FINDING-04789](../false-positives/FINDING-04789.md) | ModelicaTest.Blocks.Continuous_SteadyState | `limPID.Td` |
| [FINDING-04801](../false-positives/FINDING-04801.md) | ModelicaTest.Blocks.Continuous_InitialState | `pID.Td` |
| [FINDING-04802](../false-positives/FINDING-04802.md) | ModelicaTest.Blocks.Continuous_InitialState | `limPID.Td` |
| [FINDING-04813](../false-positives/FINDING-04813.md) | ModelicaTest.Blocks.StrictLimiters | `PID1.Td` |
| [FINDING-04814](../false-positives/FINDING-04814.md) | ModelicaTest.Blocks.StrictLimiters | `PID2.Td` |
| [FINDING-04839](../false-positives/FINDING-04839.md) | ModelicaTest.Blocks.UnitDeduction | `PID.Td` |
| [FINDING-04840](../false-positives/FINDING-04840.md) | ModelicaTest.Blocks.UnitDeduction | `PID1.Td` |
| [FINDING-05120](../false-positives/FINDING-05120.md) | PIDMSL | `pid.Td` |
