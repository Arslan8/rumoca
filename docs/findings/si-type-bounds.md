# Study: MSL components inherit numeric bounds from the SI type system that their equations cannot honour

**Status: provisional.** The corpus sweep behind these numbers was at
389 of 827 models when this was written. The classification is stable; the
counts will grow.

## The observation

Most MSL components declare no numeric bound of their own. `Capacitor.mo` says
only:

```modelica
parameter SI.Capacitance C(start=1) "Capacitance";
```

There is no `min` anywhere in that file. It arrives with the type:

```modelica
// Modelica 4.1.0/Units.mo:505
type Capacitance = Real(final quantity="Capacitance", final unit="F", min=0);
```

So the declared domain of nearly every physical parameter in MSL is set once, in
`Units.mo`, on physical grounds — and inherited by every component that uses the
type, whether or not that component's equations survive the boundary.

This is why a checker has to resolve where a bound comes from. Reporting
`Capacitor.C`'s `min=0` against `Capacitor.mo` would send a maintainer to a file
that does not contain it.

## Three failure modes, all confirmed by execution

### 1. The type declares a bound the equations cannot honour

| Type | Bound | Component | Equation | Reach |
|---|---|---|---|---|
| `SI.Capacitance` | `min=0` | `Analog.Basic.Capacitor` | `i = C*der(v)` | 10 models |
| `SI.Temperature` | `min=0` | `Semiconductors.NPN`, `.PNP`, `.Diode` | thermal voltage `~k*T/q` | 5 models |

`min=0` on a temperature is physically right — absolute zero is the floor. It is
also fatal to any equation that divides by `T`. The bound is correct as physics
and wrong as a contract.

### 2. The type declares no bound at all

| Type | Bound | Component | Reach |
|---|---|---|---|
| `SI.Resistance` | none | `Analog.Basic.Resistor.R` | 12 models |
| `SI.Inductance` | none | `Analog.Basic.Inductor.L` | 7 models |
| `SI.Inertia` | none | — (`Rotational.Inertia` writes `min=0` itself) | 12 models |

With no bound, zero *and negative* values are permitted. Negative resistance and
negative inductance are not components.

### 3. The correctly-bounded type exists and is not used

This is the sharpest item in the study:

```modelica
// Units.mo:546
type Inductance = Real(final quantity="Inductance", final unit="H");
type SelfInductance = Inductance(min=0);          // :549
```

MSL defines `SelfInductance` — inductance bounded below by zero — for exactly
this purpose. `Modelica.Electrical.Analog.Basic.Inductor` declares plain
`SI.Inductance`.

The fix is one word, and MSL already made the decision; the component just does
not reflect it. See
[BUG-010](BUG-010-inductor-documents-zero-it-cannot-honour.md), where the same
component's documentation separately promises that zero works.

## Why this is one finding and not forty

Grouped by component, the sweep so far yields 73 core-library candidates. Nearly
all are instances of the three modes above, and most trace to a handful of type
definitions in `Units.mo`. Counting them individually would overstate how much
is wrong; the actionable set is small and concentrated.

It also suggests where a fix belongs. Tightening `Capacitor.mo` helps one
component; deciding what `SI.Capacitance` should promise, and whether
`SelfInductance` should be the default for self-inductance, addresses the class.

## The asymmetry that makes this a defect rather than a design choice

MSL is not careless here — it is inconsistent, and the inconsistency is
demonstrable within single packages:

| | Bounded correctly | Unbounded |
|---|---|---|
| Electrical | `SelfInductance(min=0)` *defined* | `Inductor` uses plain `Inductance` |
| Mechanics | `Mass(min=0)` on the type | `Inertia` has no type bound; the component adds it |
| Translational | `QuadraticSpeedDependentForce.v_nominal(min=eps)` | `Mass.m(min=0)`, which is fatal |

The same library, in the same package, makes both choices for the same kind of
quantity. That asymmetry is the evidence that the unbounded cases are omissions
rather than decisions.

## Reproducing

```bash
export PYTHONPATH=packages/rumoca-bitcode:packages/modelsan
xargs -a tools/sweep/omc.models -P 8 -I{} \
  python3 tools/sweep/omcsweep.py {} > sweep.jsonl
python3 tools/sweep/verify2.py sweep.jsonl verified.json
```

`verify2.py` prints, for each finding, the class that declares the parameter and
whether the bound came from the component, from its type, or from nothing.
