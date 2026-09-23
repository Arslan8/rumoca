# LimPID already asserts that controller gain is nonzero

Group `asserted-limpid-gain` · 9 report instances · false-positives

The anti-windup gain contains 1/(k*Ni), but the equation section explicitly asserts abs(k)>=Modelica.Constants.small with the diagnostic “Controller gain must be non-zero.” Ni also has a positive lower bound. The report overlooked the existing full domain enforcement; rejection at k=0 is intended behavior, not an unguarded missing-constraint bug.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-04783](../false-positives/FINDING-04783.md) | ModelicaTest.Blocks.Continuous | `limPID.k` |
| [FINDING-04796](../false-positives/FINDING-04796.md) | ModelicaTest.Blocks.Continuous_SteadyState | `limPID.k` |
| [FINDING-04809](../false-positives/FINDING-04809.md) | ModelicaTest.Blocks.Continuous_InitialState | `limPID.k` |
| [FINDING-04816](../false-positives/FINDING-04816.md) | ModelicaTest.Blocks.StrictLimiters | `PID1.k` |
| [FINDING-04818](../false-positives/FINDING-04818.md) | ModelicaTest.Blocks.StrictLimiters | `PID2.k` |
| [FINDING-04848](../false-positives/FINDING-04848.md) | ModelicaTest.Blocks.LimPID | `PID1.k` |
| [FINDING-04849](../false-positives/FINDING-04849.md) | ModelicaTest.Blocks.LimPID | `PID2.k` |
| [FINDING-04850](../false-positives/FINDING-04850.md) | ModelicaTest.Blocks.LimPID | `PID3.k` |
| [FINDING-04851](../false-positives/FINDING-04851.md) | ModelicaTest.Blocks.LimPID | `PID4.k` |
