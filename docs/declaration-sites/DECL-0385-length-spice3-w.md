# DECL-0385: `W` declared without a lower bound

| | |
|---|---|
| **Declaration** | `Modelica 4.1.0/Electrical/Spice3.mo:4456` |
| **Parameter** | `W` |
| **Quantity** | `SI.Length` |
| **Declared modifiers** | none |
| **Status** | **latent — a permitted value, not an observed failure** |

> **Read the sentinel study first.** `Spice3.mo` encodes an unset parameter as `-1e40`
> and tests against it before use (`Spice3.mo:157`). If this declaration carries that
> default, the negative value is deliberate and this is not a defect — see
> [sentinel-parameters.md](../findings/sentinel-parameters.md).

## What is wrong

`SI.Length` declares no `min` in `Units.mo`, and this
declaration adds none of its own. It therefore accepts a negative value, and
a negative length is not a geometry.

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
type Length = Real (
    final quantity="Length",
    final unit="...",
    min=0);
```

Bounding this one declaration instead is correct but local:

```modelica
// Electrical/Spice3.mo:4456
parameter SI.Length W(min=0) = ...;
```

See [si-type-bounds.md](../findings/si-type-bounds.md) for why the type is the
right place, and [`catalog/`](../findings/catalog/README.md) for the same data
grouped by type.
