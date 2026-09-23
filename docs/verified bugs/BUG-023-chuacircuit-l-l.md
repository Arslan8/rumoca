# BUG-023: `ChuaCircuit.L.L` fails at `0`, a value its declaration permits

| | |
|---|---|
| **Model** | `Modelica.Electrical.Analog.Examples.ChuaCircuit` |
| **File** | `ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/ChuaCircuit.mo:5` |
| **Instance** | `L` |
| **Parameter** | `L` |
| **Trigger** | `L.L = 0` |
| **Reach** | this trigger reproduces in 8 models |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev |
| **Status** | Reported, not fixed |

## The instance

```modelica
// ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/ChuaCircuit.mo:5
Modelica.Electrical.Analog.Basic.Inductor L
```

`L` is an instance of `Modelica.Electrical.Analog.Basic.Inductor`.

## What happens

The model simulates cleanly at its declared values in both tools. Overriding
`L.L` to `0` — a value nothing in the declaration excludes — makes it fail in
both:

```console
$ rumoca compile-bitcode chuacircuit.rbc --simulate --check --param L.L=0
```

## Root cause

`SI.Inductance L` with no bound, documented as permitting zero

The declaration to change is in the component, not in this model:
[BUG-010](BUG-010-inductor-documents-zero-it-cannot-honour.md) carries the
argument and the suggested patch.

```modelica
// the fix, in Inductor
parameter SI.Inductance L(min=Modelica.Constants.small, start=1);
```

## Why this instance has its own report

The root cause is one edit to `Inductor`. This file exists because
that is not the only thing a developer needs: `ChuaCircuit.mo` was proven to
fail at this specific instance, and a maintainer looking at that model needs to
know which of its components was exercised and at what value. Sibling instances
in the same file are reported separately for the same reason.
