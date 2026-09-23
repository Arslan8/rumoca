# BUG-010: `Inductor` documents that zero inductance is allowed, declares no bound, and fails at zero in both tools

| | |
|---|---|
| **Severity** | High — the library states the value is supported, so a user has every reason to use it |
| **Target** | MSL 4.1.0, `Modelica.Electrical.Analog.Basic.Inductor` |
| **Trigger** | `L = 0` |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev, on 3 MSL example models; 8 models in the full OMC sweep |
| **Found by** | ModelSan parameter sweep over 847 models, cross-confirmed against OMC, 2026-09-13 |
| **Status** | Reported, not fixed |

## Summary

```modelica
// Electrical/Analog/Basic/Inductor.mo
parameter SI.Inductance L(start=1) "Inductance";
equation
  L*der(i) = v;
```

Two things are wrong together:

1. **No bound at all.** Not `min=0` — *nothing*. Zero and negative inductance
   are both permitted by the declaration.
2. **The documentation promises zero works.** From the same file:

   > The Inductance *L* is allowed to be positive, or zero.

At `L = 0` the equation becomes `0 = v`. That is not merely a vanishing
coefficient — it turns a differential equation into an algebraic constraint on
`v` and removes `i` as a state. Neither tool survives it.

## Confirmed on three MSL examples, in two independent tools

Each model simulates cleanly at its declared values and fails at `L = 0`:

| Model | Parameter | OMC baseline | OMC at 0 | Rumoca at 0 |
|---|---|---|---|---|
| `Electrical.Analog.Examples.ChuaCircuit` | `L.L` | passes | **fails** | **fails** |
| `Electrical.Analog.Examples.ParallelResonance` | `inductor1.L` | passes | **fails** | **fails** |
| `Electrical.Analog.Examples.SeriesResonance` | `inductor1.L` | passes | **fails** | **fails** |

```console
$ omc   # ChuaCircuit, -override L.L=0
Simulation execution failed for model: Modelica.Electrical.Analog.Examples.ChuaCircuit
division by zero
division by zero

$ rumoca compile-bitcode chua.rbc --simulate --check --param L.L=0
"solve-IR evaluation failed: non-finite derivative evaluation for state 'L.i'"
```

The cross-check matters. A failure in one tool is ambiguous — it could be that
tool not re-indexing a degenerate equation. Two independent implementations
failing on a value the library says is supported is not ambiguous.

## `Capacitor` makes the identical claim and honours it only sometimes

```modelica
// Electrical/Analog/Basic/Capacitor.mo
parameter SI.Capacitance C(start=1) "Capacitance";
equation
  i = C*der(v);
```
> The Capacitance *C* is allowed to be positive or zero.

```console
$ omc   # CauerLowPassAnalog, -override C1.C=0
BASE: OMC OK
C=0:  OMC OK
```

`C = 0` works *here*, because `i = 0` is an open circuit and the rest of this
network still determines the node. It is not universally safe:
`ChuaCircuit` with `C1.C = 0` fails in both tools. Zero capacitance is
topology-dependent — see
[BUG-013](BUG-013-capacitor-zero-capacitance-topology-dependent.md).

`L = 0` is different in kind: `0 = v` imposes a constraint on a variable the
rest of the circuit also determines, and it failed in every model tested (3 of
3 confirmed, 8 in the wider sweep).

**The asymmetry that survives this correction is the declaration, not the
outcome.** `SI.Capacitance` declares `min=0`, so zero is a value the library
deliberately admits. `SI.Inductance` declares *nothing*, so zero and negative
inductance are admitted by omission — and MSL separately defines
`SelfInductance = Inductance(min=0)` which `Basic.Inductor` does not use.

## Negative inductance is permitted too

With no `min`, nothing stops `L = -1`, which is not a physical component at all.
`Capacitor`, `Resistor` and `Conductor` are all declared the same way — `R(start=1)`,
`C(start=1)`, `G(start=1)`, no bounds — so the whole `Analog.Basic` package
relies on users not entering unphysical values.

## Suggested fix

Either make the declaration match the documentation's intent:

```modelica
parameter SI.Inductance L(min=Modelica.Constants.small, start=1) "Inductance";
```

and correct the sentence to say zero is *not* allowed — or keep `L = 0`
supported and handle the degenerate case structurally, the way
`Magnetic.FundamentalWave.Components.EddyCurrent` already does elsewhere in MSL:

```modelica
if G > 0 then
  (pi/2)*V_m.re = G*der(Phi.re);
else
  V_m.re = 0;
end if;
```

Tightening the bound is the smaller change. Whichever is chosen, the
declaration and the documentation should agree.

## Reproducing

```bash
cargo xtask repo modelica-deps ensure
export PYTHONPATH=packages/rumoca-bitcode:packages/modelsan
python3 tools/sweep/crossconfirm.py --findings ALL.json --out cross.json
```
