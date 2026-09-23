# Zero feedback resistance is the unity-gain buffer

Group `unity-buffer` · 3 report instances · false-positives

R2=(k-1)*R1 deliberately gives zero at the default k=1. R2 feeds a Basic.Resistor, whose documented domain includes zero, and there is no reciprocal R2 in this buffer. Rejecting the nominal unity-gain configuration is a false positive.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0627](../false-positives/DECL-0627.md) | — | `R2` |
| [FINDING-00877](../false-positives/FINDING-00877.md) | Modelica.Electrical.Analog.Examples.OpAmps.NonInvertingAmplifier | `buffer.R2` |
| [FINDING-00883](../false-positives/FINDING-00883.md) | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Buffer | `R2` |
