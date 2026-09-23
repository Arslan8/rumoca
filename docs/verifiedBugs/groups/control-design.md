# Control-circuit time constants create zero divisions

Group `control-design` · 3 report instances · confirmed

kp=T2/(2*T1), Ti=T2 and PIA.C=Ti/kp/PIA.R1. T1=0 directly divides by zero; T2=0 sets both Ti and kp to zero and yields 0/0 in PIA.C. These are explicit design formulas, not just solver-selected state divisions. Both triggers fail after clean baselines.

Validate T1>0 and T2>0 at ControlCircuit; use guarded design formulas so invalid input reports the time-constant constraint before parameter evaluation produces NaN/Inf. Keep the analog/block comparison consistent.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-00800](../confirmed/FINDING-00800.md) | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit | `T2` |
| [FINDING-00801](../confirmed/FINDING-00801.md) | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit | `T1` |
| [FINDING-00802](../confirmed/FINDING-00802.md) | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit | `T1` |
