# False positives and explicit non-defects: `signed-polyphase-element`

**2 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

This component is an array wrapper that passes each R or G to Basic.Resistor/Conductor. The scalar contract explicitly allows positive, zero and negative values and uses a multiplicative constitutive equation. A universal strictly-positive rule is therefore wrong here; a particular singular network requires topology-specific evidence.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0064](../false-positives/DECL-0064.md) | — | `G` | Source/semantic review | [DECL-conductor-g-4-2.md](../../bugs/DECL-conductor-g-4-2.md) |
| [DECL-0734](../false-positives/DECL-0734.md) | — | `R` | Source/semantic review | [DECL-resistor-r-4-2.md](../../bugs/DECL-resistor-r-4-2.md) |
