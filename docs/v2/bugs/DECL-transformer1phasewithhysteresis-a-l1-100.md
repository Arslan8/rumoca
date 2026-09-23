# DECL-0025: `A_l1` declared without a lower bound

|  |  |
|---|---|
| **Tier** | **Latent** — a permitted value, not an observed failure |
| **Declaration** | `Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer1PhaseWithHysteresis.mo:100` |
| **Parameter** | `A_l1` |
| **Type** | `SI.Area` |
| **Declared modifiers** | `—` |
| **Found by** | **the SI type-bound census** — `tools/sweep/min0_census.py`, the same bound rule PhysicalSan applies, run over declarations rather than over one model's variables |
| **From run** | `docs/findings/catalog/by-type/`, from `tools/sweep/min0_census.py` |
| **Status** | **latent — nothing has been observed failing here** |


## The claim

`SI.Area` declares no `min` in `Units.mo`, and this declaration adds none of its own. It therefore accepts a negative value, and a negative cross-section is not a geometry.

It does **not** claim that any model sets such a value, or that anything fails. This is the weakest tier in this project and the one most likely to contain deliberate choices.

## How to verify

**1. Read the declaration** (seconds):

```console
$ sed -n '100p' "target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer1PhaseWithHysteresis.mo"
```

It should declare `A_l1` with type `SI.Area` and no `min`.

**2. Confirm the type supplies no bound either** — this is the whole claim, and
a bound inherited from the type would refute it:

```console
$ grep -n "type Area " "target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Units.mo"
```

If that line carries no `min`, the type supplies no bound and the claim stands.

**3. Check it is not a sentinel.** Some MSL packages encode "unset" as a
negative magic number and test for it before use:

```console
$ grep -n -- "-1e40\|-1E40" "target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer1PhaseWithHysteresis.mo" | head
```

If this file uses that idiom, the negative value is deliberate — see
[sentinel-parameters](../../findings/sentinel-parameters.md) — and this report
should be withdrawn.


## What would disprove this

- `SI.Area` turns out to carry a `min` after all, or this declaration carries one that the catalog missed.
- The parameter is a sentinel, as above.
- The negative range is meaningful for this quantity in this context — a signed offset rather than a magnitude.

## The fix is not here

This site is one of **911** that inherit from **17 type definitions** in `Units.mo` that declare no `min`. Bounding the type is one edit and closes every site that inherits it:

```modelica
// Units.mo
type Area = Real (
    final quantity="Area",
    final unit="...",
    min=0);
```

Bounding this one declaration instead is correct but local:

```modelica
// Magnetic/FluxTubes/Examples/Hysteresis/Components/Transformer1PhaseWithHysteresis.mo:100
parameter SI.Area A_l1(min=0) = ...;
```

See [si-type-bounds](../../findings/si-type-bounds.md) for why the type is the right place.

## How strong is this?

| Tier | Evidence |
|---|---|
| **Confirmed** | fails under **two independent tools**, and the model is clean at its declared values |
| **Candidate** | static analysis of the canonical DAE reached it; **no execution has decided it either way** |
| -> **Latent** | a declaration *permits* a physically impossible value; **nothing has been observed failing** |

This instance is in the **Latent** tier.
