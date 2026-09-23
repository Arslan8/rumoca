# BUG-035: `LCOscillator.opAmp.Vps` fails at `-15`, a value its declaration permits

| | |
|---|---|
| **Model** | `Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator` |
| **File** | `ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/OpAmps/LCOscillator.mo:18` |
| **Instance** | `opAmp` |
| **Parameter** | `Vps` |
| **Trigger** | `opAmp.Vps = -15` |
| **Reach** | this trigger reproduces in 1 model |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev |
| **Status** | Reported, not fixed |

## The instance

```modelica
// ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/OpAmps/LCOscillator.mo:18
Modelica.Electrical.Analog.Ideal.IdealizedOpAmpLimited opAmp
```

`opAmp` is an instance of `Modelica.Electrical.Analog.Ideal.IdealizedOpAmpLimited`.

## What happens

The model simulates cleanly at its declared values in both tools. Overriding
`opAmp.Vps` to `-15` — a value nothing in the declaration excludes — makes it fail in
both:

```console
$ rumoca compile-bitcode lcoscillator.rbc --simulate --check --param opAmp.Vps=-15
```

## Root cause

`Vps - Vns` is a divisor; no `min` can express a constraint between two parameters

The declaration to change is in the component, not in this model:
[BUG-016](BUG-016-relational-invariant-between-two-parameters.md) carries the
argument and the suggested patch.

```modelica
// the fix, in IdealizedOpAmpLimited
assert(Vps > Vns, "supply rails must differ");
```

## Why this instance has its own report

The root cause is one edit to `IdealizedOpAmpLimited`. This file exists because
that is not the only thing a developer needs: `LCOscillator.mo` was proven to
fail at this specific instance, and a maintainer looking at that model needs to
know which of its components was exercised and at what value. Sibling instances
in the same file are reported separately for the same reason.
