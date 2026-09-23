# Zero example damping is supported by ElastoGap

Group `zero-elastogap-example-damping` · 1 report instances · false-positives

The example passes d to ElastoGap, whose contact damping force is d*v_rel and is limited by the spring force. d=0 removes dissipation without division. The physical-domain heuristic is too strict for this example parameter.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-04441](../false-positives/FINDING-04441.md) | Modelica.Mechanics.Translational.Examples.ElastoGap | `d` |
