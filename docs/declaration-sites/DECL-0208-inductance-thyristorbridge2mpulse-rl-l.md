# DECL-0208: `L` declared without a lower bound

| | |
|---|---|
| **Declaration** | `Modelica 4.1.0/Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/ThyristorBridge2mPulse_RL.mo:12` |
| **Parameter** | `L` |
| **Quantity** | `SI.Inductance` |
| **Declared modifiers** | none |
| **Status** | **latent — a permitted value, not an observed failure** |

## What is wrong

`SI.Inductance` declares no `min` in `Units.mo`, and this
declaration adds none of its own. It therefore accepts a negative value, and
stored energy is L*i^2/2, which a negative L makes negative.

## What this is not

Nothing has been observed failing here. This is a declaration that *permits* an
impossible value, which is the weakest of the three tiers this project reports:

| Tier | Evidence | Where |
|---|---|---|
| confirmed | fails in two independent tools | [`INSTANCES.md`](../verified%20bugs/INSTANCES.md) |
| candidate | static analysis reached it | [`site-reports/`](../site-reports/README.md) |
| **latent** | **the declaration permits it** | **here** |

## The fix is not here

This site and 910 others inherit from **17 type definitions** in
`Units.mo` that declare no `min`. Adding the bound to the type fixes every site
that inherits it, and is one edit rather than 911:

```modelica
// Units.mo
type Inductance = Real (
    final quantity="Inductance",
    final unit="...",
    min=0);
```

Bounding this one declaration instead is correct but local:

```modelica
// Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/ThyristorBridge2mPulse_RL.mo:12
parameter SI.Inductance L(min=0) = ...;
```

See [si-type-bounds.md](../findings/si-type-bounds.md) for why the type is the
right place, and [`catalog/`](../findings/catalog/README.md) for the same data
grouped by type.
