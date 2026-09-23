# FirstOrder divides by an unconstrained zero time constant

Group `first-order-time-constant` · 21 report instances · confirmed

Blocks.Continuous.FirstOrder declares T without a positive bound and evaluates der(y)=(k*u-y)/T. T=0 is admitted by the declaration and makes that equation undefined, even though the transfer-function limit at T=0 is the algebraic gain y=k*u. The shared source defect is established independently of nominal models the current runtime cannot execute.

Choose and document the contract. To support the natural zero-time-constant limit, formulate T*der(y)=k*u-y and handle state/initialization selection structurally. Otherwise require T>0 with a meaningful lower bound and an assertion evaluated before division. Do not silently replace zero by epsilon.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-00631](../confirmed/FINDING-00631.md) | Modelica.Electrical.Analog.Examples.Lines.SmoothStep | `firstOrder.T` |
| [FINDING-04774](../confirmed/FINDING-04774.md) | ModelicaTest.Blocks.Continuous | `firstOrder.T` |
| [FINDING-04787](../confirmed/FINDING-04787.md) | ModelicaTest.Blocks.Continuous_SteadyState | `firstOrder.T` |
| [FINDING-04800](../confirmed/FINDING-04800.md) | ModelicaTest.Blocks.Continuous_InitialState | `firstOrder.T` |
| [FINDING-04819](../confirmed/FINDING-04819.md) | ModelicaTest.Blocks.LimitersHomotopy | `controllerFeedbackPart1.T` |
| [FINDING-04821](../confirmed/FINDING-04821.md) | ModelicaTest.Blocks.LimitersHomotopy | `firstOrder1.T` |
| [FINDING-04822](../confirmed/FINDING-04822.md) | ModelicaTest.Blocks.LimitersHomotopy | `controllerFeedbackPart2.T` |
| [FINDING-04824](../confirmed/FINDING-04824.md) | ModelicaTest.Blocks.LimitersHomotopy | `firstOrder2.T` |
| [FINDING-04825](../confirmed/FINDING-04825.md) | ModelicaTest.Blocks.LimitersHomotopy | `controllerFeedbackPart3.T` |
| [FINDING-04827](../confirmed/FINDING-04827.md) | ModelicaTest.Blocks.LimitersHomotopy | `firstOrder3.T` |
| [FINDING-04828](../confirmed/FINDING-04828.md) | ModelicaTest.Blocks.LimitersHomotopy | `controllerFeedbackPart4.T` |
| [FINDING-04830](../confirmed/FINDING-04830.md) | ModelicaTest.Blocks.LimitersHomotopy | `firstOrder4.T` |
| [FINDING-04831](../confirmed/FINDING-04831.md) | ModelicaTest.Blocks.LimitersHomotopy | `controllerFeedbackPart5.T` |
| [FINDING-04833](../confirmed/FINDING-04833.md) | ModelicaTest.Blocks.LimitersHomotopy | `firstOrder5.T` |
| [FINDING-04834](../confirmed/FINDING-04834.md) | ModelicaTest.Blocks.LimitersHomotopy | `controllerFeedbackPart6.T` |
| [FINDING-04836](../confirmed/FINDING-04836.md) | ModelicaTest.Blocks.LimitersHomotopy | `firstOrder6.T` |
| [FINDING-04838](../confirmed/FINDING-04838.md) | ModelicaTest.Blocks.UnitDeduction | `firstOrder.T` |
| [FINDING-04844](../confirmed/FINDING-04844.md) | ModelicaTest.Blocks.LimPID | `firstOrder1.T` |
| [FINDING-04845](../confirmed/FINDING-04845.md) | ModelicaTest.Blocks.LimPID | `firstOrder2.T` |
| [FINDING-04846](../confirmed/FINDING-04846.md) | ModelicaTest.Blocks.LimPID | `firstOrder3.T` |
| [FINDING-04847](../confirmed/FINDING-04847.md) | ModelicaTest.Blocks.LimPID | `firstOrder4.T` |
