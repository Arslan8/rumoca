# BUG-003: `SwitchedRLC.mo` has an unguarded divisor with no declared bound

| | |
|---|---|
| **Severity** | Low — an example model, not library code |
| **Component** | `examples/models/SwitchedRLC.mo` |
| **Found by** | ModelSan parameter sweep, 2026-09-13 |
| **Status** | Reported, not fixed |

## Summary

```modelica
parameter Resistance R = 100;
...
i_R = V/R;
```

`R` is a divisor with no `min`, so `R = 0` is permitted by the declaration and
produces a NaN that the solver then fails to resolve at an event boundary.

## Reproducer

```console
$ rumoca compile examples/models/SwitchedRLC.mo --model SwitchedRLC \
      --emit-bitcode rlc.rbc
$ rumoca compile-bitcode rlc.rbc --simulate --t-end 0.5 --check --param R=0
[
  {
    "kind": "simulation-failure",
    "detail": "solve-IR evaluation failed: algebraic projection did not converge
               at event boundary: worst scaled residual row=1 target=i_R
               value=NaN ratio=NaN norm=inf"
  }
]
```

Baseline with declared values is clean.

## Why report an example model

Two reasons, neither of which is "this model is wrong".

The model is used as a test fixture (`rumoca-scenario.switched_rlc.toml`,
and the MSL variant in the parity gate). A fixture that becomes NaN under a
legal parameter value is a fixture that cannot be used for parameter-sweep
testing without a guard.

It is also the same shape as BUG-002 in miniature: a divisor whose declaration
does not exclude zero. The one-character fix

```modelica
parameter Resistance R(min=Modelica.Constants.small) = 100;
```

makes the constraint machine-readable, which is what lets a tool reject the
configuration instead of the solver discovering it numerically.

## Note on the diagnostic

The runtime message names `i_R` and reports `value=NaN ratio=NaN norm=inf`,
which is accurate but does not name `R`. Tracing from "the algebraic projection
diverged at `i_R`" back to "you set `R` to zero" is exactly the step ModelSan
automates, and exactly the step a user would otherwise do by hand.
