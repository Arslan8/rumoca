# MSL RLC wrapper delegates to zero/signed-capable primitive equations

Group `msl-rlc-zero-component` · 3 report instances · false-positives

This local wrapper only passes L, R and C into Basic.Inductor, Basic.Resistor and Basic.Capacitor. Those source components use implicit/multiplicative equations; L and C explicitly document zero support, while R explicitly documents signed and zero support. A connected zero configuration may require retranslating states or different initialization, but the blanket physical-domain claim is not valid.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-05123](../false-positives/FINDING-05123.md) | SwitchedRLC_MSL | `L` |
| [FINDING-05124](../false-positives/FINDING-05124.md) | SwitchedRLC_MSL | `R` |
| [FINDING-05125](../false-positives/FINDING-05125.md) | SwitchedRLC_MSL | `C` |
