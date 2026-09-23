# Static/source-supported candidates: `fluid-medium-cp`

**1 report instances**

[Back to Static/source-supported candidates](../candidates.md) · [Overview](../README.md)

## Common decision rule

The Medium record gives cp no strictly-positive bound or assertion. FluidHeatFlow.BaseClasses.TwoPort evaluates T_a=flowPort_a.h/medium.cp and T_b=flowPort_b.h/medium.cp. Therefore zero is admitted by the material record and makes the common consumer undefined. The report instances share this declaration-level defect; nominal models blocked in the current Rumoca runtime are not falsely described as independently simulated.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0890](../candidate/DECL-0890.md) | — | `cp` | Source/semantic review | [DECL-medium-cp-5.md](../../bugs/DECL-medium-cp-5.md) |
