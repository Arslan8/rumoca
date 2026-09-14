# BUG-001: compiler panic on a comprehension inside a `for`-equation

| | |
|---|---|
| **Severity** | High — process abort, no diagnostic |
| **Component** | `rumoca-phase-dae` |
| **Site** | `crates/rumoca-phase-dae/src/construction/expression.rs:1809` |
| **Affects** | `rumoca compile` on any input with this shape, including `examples/models/NeuralODEBackprop.mo`, which ships a scenario TOML |
| **Found by** | ModelSan corpus sweep, 2026-09-13 |
| **Status** | Reported, not fixed |

## Summary

A comprehension appearing as an argument to a built-in call, inside an
enclosing `for`-equation, aborts the process with a failed `.expect`. There is
no diagnostic, no span, and no error code — the compiler panics.

## Reproducer

14 lines, no library dependencies:

```modelica
model Q
  parameter Integer n = 2;
  Real e[n];
  Real g[n];
  Real x(start = 1);
equation
  der(x) = -x;
  for i in 1:n loop
    e[i] = x * i;
  end for;
  for i in 1:n loop
    g[i] = sum(e[b] for b in 1:n);   // comprehension in a builtin, inside a for-equation
  end for;
end Q;
```

```console
$ rumoca compile Q.mo --model Q
thread 'main' panicked at crates/rumoca-phase-dae/src/construction/expression.rs:1809:14:
analysis proves the exact comprehension occurrence
```

## The exact trigger

Bisection narrowed it to one condition: **the comprehension must be inside an
enclosing `for`-equation.** Hoisting the identical `sum` out of the loop
compiles cleanly:

```modelica
  g = sum(e[b] for b in 1:n);      // compiles
```

```modelica
  for i in 1:n loop
    g[i] = sum(e[b] for b in 1:n); // panics
  end for;
```

Note the comprehension body does not reference the outer index `i`. The
enclosing loop alone is sufficient.

## Where it fails

```rust
// crates/rumoca-phase-dae/src/construction/expression.rs:1804-1810
let key = ComprehensionKey::new(provenance.span(), indices)
    .expect("analysis proves comprehension-owner provenance");
symbols
    .functions
    .comprehension_plans
    .get(&key, indices)
    .expect("analysis proves the exact comprehension occurrence")   // <-- line 1809
```

Call path from the backtrace:

```
lower_builtin_call
  └── lower_array_comprehension
        └── comprehension_plans.get(..).expect(..)
```

## Probable mechanism

`ComprehensionKey` is built from `provenance.span()` plus the binder indices.
A comprehension written once inside a `for`-equation is *instantiated* once per
loop iteration, but every instance shares one source span. If the analysis pass
registers one plan per span while lowering requests one per occurrence, every
request after the first misses the map and the `.expect` fires.

This is a hypothesis from reading the code and the backtrace, not a verified
root cause. It predicts the observed behaviour — no enclosing loop means one
occurrence per span, and the panic disappears — but the fix belongs to whoever
owns the analysis/lowering contract.

## Why the assertion is the wrong shape regardless of cause

`.expect("analysis proves the exact comprehension occurrence")` states an
invariant the analysis is supposed to establish. It does not hold here, so the
user sees a Rust panic instead of a diagnostic. Whatever the underlying fix,
this site should either carry a real `DaeConstructionError` with the
comprehension's span, or the analysis should be strengthened so the invariant
is true by construction.

## How it was found

ModelSan sweeps a corpus by compiling every model to bitcode. The sweep
recorded two compile failures whose text mentioned a Rust backtrace, which is
how a panic is distinguishable from a normal refusal.

## Provenance checks

This is not caused by any change in this branch:

- The panic occurs on plain `rumoca compile` with no bitcode flags, and also on
  `--emit dae-mo`.
- It reproduces with this branch's `rumoca-phase-flatten` change reverted to
  `main`.
- The reproducer contains no `connect(...)`, so the flatten change's code path
  cannot execute.
