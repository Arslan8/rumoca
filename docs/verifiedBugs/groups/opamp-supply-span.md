# Equal op-amp supplies divide by zero

Group `opamp-supply-span` · 2 report instances · confirmed

The source defines i_s = p_s/(vps-vns) with no nonzero-span assertion. In LCOscillator and Comparator, Vns=-15; setting Vps=-15 makes the denominator exactly zero. The correct equality witness is -15, not Vps=0. Both nominal examples pass; the actual equality fails in Rumoca and in ordinary and final-evaluated OpenModelica models.

In IdealizedOpAmpLimited validate vps > vns (including useSupply=true pins), and make the zero-span behavior explicit. Do not divide before validation; use a guarded expression plus a domain assertion. If collapsed supplies are to be supported, specify and implement their power/current behavior rather than substituting an epsilon.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [BUG-024](../confirmed/BUG-024.md) | Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator | `opAmp.Vps` |
| [FINDING-00781](../confirmed/FINDING-00781.md) | Modelica.Electrical.Analog.Examples.OpAmps.Comparator | `Vps` |
