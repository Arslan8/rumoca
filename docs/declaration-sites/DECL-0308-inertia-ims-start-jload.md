# DECL-0308: `JLoad` declared without a lower bound

| | |
|---|---|
| **Declaration** | `Modelica 4.1.0/Electrical/Machines/Examples/InductionMachines/IMS_Start.mo:16` |
| **Parameter** | `JLoad` |
| **Quantity** | `SI.Inertia` |
| **Declared modifiers** | none |
| **Status** | **latent — a permitted value, not an observed failure** |

## What is wrong

`SI.Inertia` declares no `min` in `Units.mo`, and this
declaration adds none of its own. It therefore accepts a negative value, and
J*a = tau determines angular acceleration only for J > 0.

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
type Inertia = Real (
    final quantity="Inertia",
    final unit="...",
    min=0);
```

Bounding this one declaration instead is correct but local:

```modelica
// Electrical/Machines/Examples/InductionMachines/IMS_Start.mo:16
parameter SI.Inertia JLoad(min=0) = ...;
```

See [si-type-bounds.md](../findings/si-type-bounds.md) for why the type is the
right place, and [`catalog/`](../findings/catalog/README.md) for the same data
grouped by type.
