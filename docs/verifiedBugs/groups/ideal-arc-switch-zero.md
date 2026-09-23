# Arc-switch resistance/conductance are multiplicative ideal limits

Group `ideal-arc-switch-zero` · 18 report instances · false-positives

The quenched off-state is i=Goff*v and the closed state is v=Ron*i; neither parameter is divided. Ron=0 is the ideal closed switch and Goff=0 the ideal open switch, consistent with the base ideal-switch family. A particular connected circuit can still become structurally singular.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0051](../false-positives/DECL-0051.md) | — | `Goff` |
| [DECL-0659](../false-positives/DECL-0659.md) | — | `Ron` |
| [FINDING-00209](../false-positives/FINDING-00209.md) | Modelica.Electrical.Analog.Examples.ControlledSwitchWithArc | `switch2.Ron` |
| [FINDING-00210](../false-positives/FINDING-00210.md) | Modelica.Electrical.Analog.Examples.ControlledSwitchWithArc | `switch2.Goff` |
| [FINDING-01032](../false-positives/FINDING-01032.md) | Modelica.Electrical.Analog.Examples.SwitchWithArc | `switch2.Ron` |
| [FINDING-01033](../false-positives/FINDING-01033.md) | Modelica.Electrical.Analog.Examples.SwitchWithArc | `switch2.Goff` |
| [FINDING-01949](../false-positives/FINDING-01949.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `switchYDwithArc.idealCloser.closerWithArc[1].Ron` |
| [FINDING-01950](../false-positives/FINDING-01950.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `switchYDwithArc.idealCloser.closerWithArc[1].Goff` |
| [FINDING-01951](../false-positives/FINDING-01951.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `switchYDwithArc.idealCloser.closerWithArc[2].Ron` |
| [FINDING-01952](../false-positives/FINDING-01952.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `switchYDwithArc.idealCloser.closerWithArc[2].Goff` |
| [FINDING-01953](../false-positives/FINDING-01953.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `switchYDwithArc.idealCloser.closerWithArc[3].Ron` |
| [FINDING-01954](../false-positives/FINDING-01954.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `switchYDwithArc.idealCloser.closerWithArc[3].Goff` |
| [FINDING-01957](../false-positives/FINDING-01957.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `switchYDwithArc.idealOpener.openerWithArc[1].Ron` |
| [FINDING-01958](../false-positives/FINDING-01958.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `switchYDwithArc.idealOpener.openerWithArc[1].Goff` |
| [FINDING-01959](../false-positives/FINDING-01959.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `switchYDwithArc.idealOpener.openerWithArc[2].Ron` |
| [FINDING-01960](../false-positives/FINDING-01960.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `switchYDwithArc.idealOpener.openerWithArc[2].Goff` |
| [FINDING-01961](../false-positives/FINDING-01961.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `switchYDwithArc.idealOpener.openerWithArc[3].Ron` |
| [FINDING-01962](../false-positives/FINDING-01962.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `switchYDwithArc.idealOpener.openerWithArc[3].Goff` |
