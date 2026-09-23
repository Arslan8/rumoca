# DECL-0419: `delta` declared without a lower bound

| | |
|---|---|
| **Declaration** | `Modelica 4.1.0/Magnetic/FluxTubes/Examples/BasicExamples/ToroidalCoreAirgap.mo:8` |
| **Parameter** | `delta` |
| **Quantity** | `SI.Length` |
| **Declared modifiers** | none |
| **Status** | **latent — a permitted value, not an observed failure** |

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
// Magnetic/FluxTubes/Examples/BasicExamples/ToroidalCoreAirgap.mo:8
parameter SI.Length delta(min=0) = ...;
```

See [si-type-bounds.md](../findings/si-type-bounds.md) for why the type is the
right place, and [`catalog/`](../findings/catalog/README.md) for the same data
grouped by type.
