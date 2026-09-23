# SwitchedRLC divides directly by unconstrained resistance

Group `example-rlc-resistance` · 1 report instances · confirmed

The local example declares R without a bound and computes i_R=V/R. R=0 is an immediate divide by zero; unlike the MSL Basic.Resistor formulation, this hand-written example chose explicit reciprocal form.

Either require/assert abs(R)>0 before i_R evaluation, or reformulate the branch implicitly as R*i_R=V if the ideal zero-resistance limit is meant to be supported. Document whether negative active resistance is valid.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-05122](../confirmed/FINDING-05122.md) | SwitchedRLC | `R` |
