# Saturating-inductor ordering is already asserted

Group `asserted-inductance-order` · 1 report instances · false-positives

The source asserts Lzer>Lnom*(1+eps) and Linf<Lnom*(1-eps), and documents the same ordering. The reported positive-nominal equality violates these existing relational constraints; the claim that no assertion excludes it is false. This is not a claim that every compiler schedules diagnostic assertions before evaluating invalid initial equations.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-00999](../false-positives/FINDING-00999.md) | Modelica.Electrical.Analog.Examples.ShowSaturatingInductor | `SaturatingInductance1.Lzer` |
