# Equal machine reactances divide by zero

Group `machine-reactance-equality` · 6 report instances · confirmed

The record defines xe=xmd^2/(xd-xdTransient), xrd with /(xdTransient-xdSubtransient), and xrq=xmq^2/(xq-xqSubtransient), without relational assertions. The equality in this report zeros the corresponding denominator. A minimal model using the actual library record tests the nominal data and all three equalities independently; the full reported machine cannot be simulated by the current Rumoca bitcode runtime. Verification is of the shared declaration, not a claim that the full machine was independently run.

Validate xd>xdTransient>xdSubtransient and xq>xqSubtransient in the data-conversion layer (or explicitly define any supported degenerate machine representation). Guard parameter calculations and use a checked helper function with assertions, since record bindings may be evaluated before model initial equations.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-02178](../confirmed/FINDING-02178.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `smeeData.xd` |
| [FINDING-02179](../confirmed/FINDING-02179.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `smeeData.xdTransient` |
| [FINDING-02180](../confirmed/FINDING-02180.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `smeeData.xq` |
| [FINDING-02242](../confirmed/FINDING-02242.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `smeeData.xd` |
| [FINDING-02243](../confirmed/FINDING-02243.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `smeeData.xdTransient` |
| [FINDING-02244](../confirmed/FINDING-02244.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `smeeData.xq` |
