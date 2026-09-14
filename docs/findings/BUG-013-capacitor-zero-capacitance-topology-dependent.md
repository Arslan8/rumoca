# BUG-013: `SI.Capacitance` admits zero, which most circuits survive and some do not

| | |
|---|---|
| **Severity** | Medium — the bound is declared library-wide, and whether it holds depends on the network |
| **Target** | MSL 4.1.0, `Modelica.Units.SI.Capacitance` → `Electrical.Analog.Basic.Capacitor` |
| **Trigger** | `C = 0` |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev |
| **Reach** | 12 models in the full 827-model sweep |
| **Found by** | OMC-backed parameter sweep, cross-confirmed, 2026-09-13 |
| **Status** | Reported, not fixed |

## Summary

`Capacitor.mo` declares no bound of its own:

```modelica
parameter SI.Capacitance C(start=1) "Capacitance";
equation
  i = C*der(v);
```

The bound comes from the type, in `Units.mo:505`:

```modelica
type Capacitance = Real(final quantity="Capacitance", final unit="F", min=0);
```

So `C = 0` is a value the library admits everywhere the type is used. At that
value the equation reads `i = 0` — an open circuit. Whether that is well posed
depends on whether the rest of the network still determines the node voltage.

## It is topology-dependent, which is the point

```console
$ omc  # -override C1.C=0
  OMC OK    Modelica.Electrical.Analog.Examples.CauerLowPassAnalog
  OMC FAILS Modelica.Electrical.Analog.Examples.ChuaCircuit
```

Rumoca agrees on `ChuaCircuit`: clean at declared values, fails at `C1.C = 0`.

That is what makes this worth reporting rather than dismissing. A bound that
holds in some networks and not others cannot be checked by looking at the
component, and a user has no way to know which case they are in. The
declaration promises `C = 0` unconditionally.

`Capacitor`'s documentation states the same thing:

> The Capacitance *C* is allowed to be positive or zero.

True for `CauerLowPassAnalog`, false for `ChuaCircuit`.

## Relationship to BUG-010

[BUG-010](BUG-010-inductor-documents-zero-it-cannot-honour.md) reported the
inductor, and originally used "Capacitor honours the same claim" as its contrast.
That contrast was drawn from a single circuit and is corrected there.

The two are different defects:

| | `Inductor` | `Capacitor` |
|---|---|---|
| Type bound | **none** — negative permitted | `min=0` |
| At zero | `0 = v`, a constraint on a shared variable | `i = 0`, an open circuit |
| Failed in | every model tested | some networks, not others |
| Fix available in MSL | `SelfInductance(min=0)`, unused | none; the bound is deliberate |

The inductor is an omission. The capacitor is a deliberate bound whose validity
is conditional on something the declaration cannot express.

## Suggested direction

There may be no bound that is right for every network, which is itself worth
saying. Two options:

1. Keep `min=0` and document that zero capacitance is well posed only where the
   node voltage is otherwise determined — so the promise matches what the
   library can guarantee.
2. Have the component state the degenerate case structurally, as
   `Magnetic.FundamentalWave.Components.EddyCurrent` does for its conductance.

## Reproducing

```bash
export PYTHONPATH=packages/rumoca-bitcode:packages/modelsan
python3 tools/sweep/omcsweep.py Modelica.Electrical.Analog.Examples.ChuaCircuit
```
