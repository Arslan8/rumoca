# BUG-016: `IdealizedOpAmpLimited` divides by `Vps - Vns`, an invariant no bound can express

| | |
|---|---|
| **Severity** | Medium — and a distinct class: the missing constraint is *relational* |
| **Target** | MSL 4.1.0, `Modelica.Electrical.Analog.Ideal.IdealizedOpAmpLimited` |
| **Trigger** | `Vps = -15`, making it equal the default `Vns` |
| **Confirmed in** | Rumoca **and** OpenModelica 1.27.0-dev |
| **Found by** | ModelSan negative-value probe, cross-confirmed, 2026-09-14 |
| **Status** | Reported, not fixed |

## Summary

```modelica
// Electrical/Analog/Ideal/IdealizedOpAmpLimited.mo
parameter SI.Voltage Vps = +15 "Positive supply voltage";
parameter SI.Voltage Vns = -15 "Negative supply voltage";
...
SI.Current i_s = p_s/(vps - vns) "Supply current";
equation
  vps = Vps;
  vns = Vns;
```

Neither parameter carries a bound, and `SI.Voltage` supplies none — voltage is
legitimately signed, so there is no per-parameter bound that would help.

The constraint the component actually depends on is **`Vps > Vns`**, and that is
not stated anywhere. At `Vps = -15` the supply span collapses to zero and the
supply-current equation divides by it.

## Confirmed in both tools

`Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator` runs cleanly at its
declared values and fails in both tools at `opAmp.Vps = -15`. OpenModelica
names the expression itself:

```
division by zero at time 0, (a=0.0599775) / (b=0),
where divisor b expression is: opAmp.Vps - opAmp.Vns
```

## Why this is a different class from BUG-002 or BUG-010

Every previously reported finding here is a *single-parameter domain* problem:
one parameter, one bound, one value the bound wrongly admits. Tightening `min`
fixes each of them.

This one cannot be fixed that way. `Vps = -15` is a perfectly reasonable
voltage; `Vns = -15` is the library's own default. Neither value is wrong on its
own, and no `min` or `max` on either parameter would exclude the combination.
The invariant relates two parameters, and Modelica's declaration syntax has no
way to say so.

That is the finding: **`min`/`max` can only express box constraints, and some of
what a component requires is not a box.** Anywhere a model divides by a
*difference* of parameters, the declared domain is structurally incapable of
protecting it.

## How it was found

By the negative-value probe, which is new. Every earlier sweep tried zero and
declared bounds only, on the reasoning that zero is what makes coefficients
vanish and divisors blow up. That reasoning misses this entirely: zero is a fine
value for `Vps`, and it is *the sign flip* that collapses the difference.

`SI.Voltage`, `SI.Resistance`, `SI.Inductance`, `SI.Inertia` and
`SI.Conductance` all declare no lower bound, so negative values are permitted
throughout MSL and were never being tried.

## Suggested fix

A bound cannot express this, so an assertion is the available mechanism, and
MSL uses it elsewhere for exactly this purpose:

```modelica
assert(Vps > Vns,
       "IdealizedOpAmpLimited: positive supply must exceed negative supply");
```

This also makes the constraint machine-readable for tools, which is what turns
a solver error naming `opAmp.Vps - opAmp.Vns` into a diagnostic naming the
parameter the user actually set.

## Reproducing

```bash
export PYTHONPATH=packages/rumoca-bitcode:packages/modelsan
python3 tools/sweep/pipeline_sweep.py \
  "$MSL/Modelica 4.1.0/Electrical/Analog/Examples/OpAmps/LCOscillator.mo" \
  Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator
```
