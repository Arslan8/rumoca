# Machine inertia delegates to the zero-capable algebraic inertia component

Group `zero-machine-inertia` · 82 report instances · false-positives

Jr and Js are passed directly to Rotational.Components.Inertia. That component uses J*a=sum(tau), so J=0 produces an algebraic torque balance rather than an intrinsic reciprocal. Js is relevant only when the stator rotates. A particular drive train can have incompatible starts or constraints, but the declaration alone does not establish that both machine inertias must be strictly positive.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0316](../false-positives/DECL-0316.md) | — | `Jr` |
| [DECL-0317](../false-positives/DECL-0317.md) | — | `Js` |
| [FINDING-01141](../false-positives/FINDING-01141.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcpm.Jr` |
| [FINDING-01142](../false-positives/FINDING-01142.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcpm.Js` |
| [FINDING-01159](../false-positives/FINDING-01159.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcee.Jr` |
| [FINDING-01160](../false-positives/FINDING-01160.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcee.Js` |
| [FINDING-01177](../false-positives/FINDING-01177.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcse.Jr` |
| [FINDING-01178](../false-positives/FINDING-01178.md) | Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics | `dcse.Js` |
| [FINDING-01200](../false-positives/FINDING-01200.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCEE_Start | `dcee.Jr` |
| [FINDING-01201](../false-positives/FINDING-01201.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCEE_Start | `dcee.Js` |
| [FINDING-01229](../false-positives/FINDING-01229.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `dcpm.Jr` |
| [FINDING-01230](../false-positives/FINDING-01230.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling | `dcpm.Js` |
| [FINDING-01277](../false-positives/FINDING-01277.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_CurrentControlled | `dcpm.Jr` |
| [FINDING-01278](../false-positives/FINDING-01278.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_CurrentControlled | `dcpm.Js` |
| [FINDING-01310](../false-positives/FINDING-01310.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpm1.Jr` |
| [FINDING-01311](../false-positives/FINDING-01311.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpm1.Js` |
| [FINDING-01319](../false-positives/FINDING-01319.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpm2.Jr` |
| [FINDING-01320](../false-positives/FINDING-01320.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive | `dcpm2.Js` |
| [FINDING-01357](../false-positives/FINDING-01357.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpm1.Jr` |
| [FINDING-01358](../false-positives/FINDING-01358.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpm1.Js` |
| [FINDING-01369](../false-positives/FINDING-01369.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpm2.Jr` |
| [FINDING-01370](../false-positives/FINDING-01370.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_QuasiStatic | `dcpm2.Js` |
| [FINDING-01388](../false-positives/FINDING-01388.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Start | `dcpm.Jr` |
| [FINDING-01389](../false-positives/FINDING-01389.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Start | `dcpm.Js` |
| [FINDING-01409](../false-positives/FINDING-01409.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Temperature | `dcpm.Jr` |
| [FINDING-01410](../false-positives/FINDING-01410.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Temperature | `dcpm.Js` |
| [FINDING-01429](../false-positives/FINDING-01429.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpm1.Jr` |
| [FINDING-01430](../false-positives/FINDING-01430.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpm1.Js` |
| [FINDING-01441](../false-positives/FINDING-01441.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpm2.Jr` |
| [FINDING-01442](../false-positives/FINDING-01442.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses | `dcpm2.Js` |
| [FINDING-01482](../false-positives/FINDING-01482.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_SinglePhase | `dcse.Jr` |
| [FINDING-01483](../false-positives/FINDING-01483.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_SinglePhase | `dcse.Js` |
| [FINDING-01512](../false-positives/FINDING-01512.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_Start | `dcse.Jr` |
| [FINDING-01513](../false-positives/FINDING-01513.md) | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_Start | `dcse.Js` |
| [FINDING-01552](../false-positives/FINDING-01552.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking | `imc.Jr` |
| [FINDING-01553](../false-positives/FINDING-01553.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking | `imc.Js` |
| [FINDING-01580](../false-positives/FINDING-01580.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL | `aimc.Jr` |
| [FINDING-01581](../false-positives/FINDING-01581.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL | `aimc.Js` |
| [FINDING-01625](../false-positives/FINDING-01625.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize | `aimc.Jr` |
| [FINDING-01626](../false-positives/FINDING-01626.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize | `aimc.Js` |
| [FINDING-01724](../false-positives/FINDING-01724.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive | `aimc.Jr` |
| [FINDING-01725](../false-positives/FINDING-01725.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive | `aimc.Js` |
| [FINDING-01764](../false-positives/FINDING-01764.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Inverter | `aimc.Jr` |
| [FINDING-01765](../false-positives/FINDING-01765.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Inverter | `aimc.Js` |
| [FINDING-01804](../false-positives/FINDING-01804.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz | `aimc.Jr` |
| [FINDING-01805](../false-positives/FINDING-01805.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz | `aimc.Js` |
| [FINDING-01847](../false-positives/FINDING-01847.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer | `aimc.Jr` |
| [FINDING-01848](../false-positives/FINDING-01848.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer | `aimc.Js` |
| [FINDING-01926](../false-positives/FINDING-01926.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `aimc.Jr` |
| [FINDING-01927](../false-positives/FINDING-01927.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc | `aimc.Js` |
| [FINDING-01995](../false-positives/FINDING-01995.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD | `aimc.Jr` |
| [FINDING-01996](../false-positives/FINDING-01996.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YD | `aimc.Js` |
| [FINDING-02062](../false-positives/FINDING-02062.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aims.Jr` |
| [FINDING-02063](../false-positives/FINDING-02063.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aims.Js` |
| [FINDING-02126](../false-positives/FINDING-02126.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `smee.Jr` |
| [FINDING-02127](../false-positives/FINDING-02127.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `smee.Js` |
| [FINDING-02198](../false-positives/FINDING-02198.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `smee.Jr` |
| [FINDING-02199](../false-positives/FINDING-02199.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `smee.Js` |
| [FINDING-02265](../false-positives/FINDING-02265.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking | `smpm.Jr` |
| [FINDING-02266](../false-positives/FINDING-02266.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Braking | `smpm.Js` |
| [FINDING-02324](../false-positives/FINDING-02324.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_CurrentSource | `smpm.Jr` |
| [FINDING-02325](../false-positives/FINDING-02325.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_CurrentSource | `smpm.Js` |
| [FINDING-02367](../false-positives/FINDING-02367.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Inverter | `smpm.Jr` |
| [FINDING-02368](../false-positives/FINDING-02368.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_Inverter | `smpm.Js` |
| [FINDING-02425](../false-positives/FINDING-02425.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad | `smpm.Jr` |
| [FINDING-02426](../false-positives/FINDING-02426.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad | `smpm.Js` |
| [FINDING-02468](../false-positives/FINDING-02468.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking | `smpm.Jr` |
| [FINDING-02469](../false-positives/FINDING-02469.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_ResistiveBraking | `smpm.Js` |
| [FINDING-02517](../false-positives/FINDING-02517.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource | `smpm.Jr` |
| [FINDING-02518](../false-positives/FINDING-02518.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource | `smpm.Js` |
| [FINDING-02568](../false-positives/FINDING-02568.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL | `smr.Jr` |
| [FINDING-02569](../false-positives/FINDING-02569.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_DOL | `smr.Js` |
| [FINDING-02622](../false-positives/FINDING-02622.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter | `smr.Jr` |
| [FINDING-02623](../false-positives/FINDING-02623.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter | `smr.Js` |
| [FINDING-02697](../false-positives/FINDING-02697.md) | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer | `aimc.Jr` |
| [FINDING-02698](../false-positives/FINDING-02698.md) | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer | `aimc.Js` |
| [FINDING-03077](../false-positives/FINDING-03077.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive | `dcpm.Jr` |
| [FINDING-03078](../false-positives/FINDING-03078.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive | `dcpm.Js` |
| [FINDING-03238](../false-positives/FINDING-03238.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_DC_Drive | `dcpm.Jr` |
| [FINDING-03239](../false-positives/FINDING-03239.md) | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_DC_Drive | `dcpm.Js` |
| [FINDING-04864](../false-positives/FINDING-04864.md) | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses | `smpm.Jr` |
| [FINDING-04865](../false-positives/FINDING-04865.md) | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses | `smpm.Js` |
