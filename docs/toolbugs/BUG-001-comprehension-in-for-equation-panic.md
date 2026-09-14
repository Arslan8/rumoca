# BUG-001: compiler panic on a comprehension outside the three expression lists the analysis walks

| | |
|---|---|
| **Severity** | High — process abort, no diagnostic |
| **Component** | `rumoca-phase-dae` |
| **Site** | `crates/rumoca-phase-dae/src/construction/expression.rs:1809` |
| **Root cause** | `all_model_expressions` (same file, :1930) walks 3 of the 9 expression-bearing fields of `flat::Model`. Covers the algorithm/`when`/`assert` triggers; the `for` trigger is a separate, undiagnosed one. |
| **Affects** | Any model with a comprehension in an algorithm section, a `when` chain, a `for`-equation, or an `assert` — including `examples/models/NeuralODEBackprop.mo`, which ships a scenario TOML |
| **Found by** | ModelSan corpus sweep, 2026-09-13; scope and cause corrected by construct probing the same day |
| **Status** | Reported, not fixed |

## Summary

`rumoca-phase-dae` pre-computes a lowering plan for every array comprehension in
the model, then looks that plan up while lowering. The pre-pass enumerates
expressions with `all_model_expressions`, which reads only three of the nine
fields of `flat::Model` that carry expressions. A comprehension in any of the
other six is never given a plan, so the lookup misses and

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

aborts the process. No diagnostic, no span, no error code.

## Reproducer

7 lines. No loop, no repetition, no library:

```modelica
model C6
  Real x(start=1,fixed=true); Real s;
algorithm
  s := sum({x*i for i in 1:2});
equation
  der(x) = -x;
end C6;
```

```console
$ rumoca compile C6.mo --model C6
thread 'main' panicked at crates/rumoca-phase-dae/src/construction/expression.rs:1809:14:
analysis proves the exact comprehension occurrence
```

## The trigger is the enclosing section, and nothing else

The same `sum({x*i for i in 1:2})` was placed in eight positions:

| Position | `flat::Model` field | Walked? | Result |
|---|---|---|---|
| top-level equation | `equations` | yes | compiles |
| `if`-equation branch | `equations` | yes | compiles |
| twice at top level | `equations` | yes | compiles |
| variable binding | `variables` attrs | yes | compiles |
| `initial equation` | `initial_equations` | yes | compiles |
| **algorithm section** | `algorithms` | **no** | **panic** |
| **`when` equation** | `when_chains` | **no** | **panic** |
| **`for`-equation** | `equations` (expanded) | yes | **panic** — see below |
| **`assert`** | `assert_equations` | **no** | **panic** |

The walked/not-walked column predicts every outcome **except the
`for`-equation**, which is a separate trigger addressed below. `initial
equation` and `assert` were run *as predictions* after the cause was
identified, and both came out as predicted.

## The walker

```rust
// crates/rumoca-phase-dae/src/construction/expression.rs:1930
pub(super) fn all_model_expressions(flat: &flat::Model) -> impl Iterator<Item = &Expression> {
    flat.variables
        .values()
        .flat_map(variable_attribute_expressions)
        .chain(flat.equations.iter().map(|equation| &equation.residual))
        .chain(flat.initial_equations.iter().map(|e| &e.residual))
}
```

`flat::Model` also declares `structured_equations`, `assert_equations`,
`initial_structured_equations`, `initial_assert_equations`, `algorithms`,
`initial_algorithms` and `when_chains`. All carry expressions; none are reached.

The function's name states the invariant the `.expect` at :1809 relies on. It
does not hold.

## The `for`-equation case is a second, distinct trigger

A `for`-equation is expanded into `flat.equations` before this analysis runs, so
its expressions *are* walked. Emitting Flat for a for-equation that compiles
shows the expansion:

```console
$ rumoca compile F1.mo --model F1.M --emit flat-mo
equation
  der(x) = (-x);
  a[1] = sq((x * 1));
  a[2] = sq((x * 2));
```

So the walker explanation does not cover it, and the mechanism there is **not
established**. What is known:

- It is not multiplicity. A `for k in 1:1` loop — one iteration, one expanded
  equation, one occurrence — still panics.
- It is not the loop index being referenced. The comprehension body in the
  reproducer does not mention the outer binder.

`ComprehensionKey` is built from `(provenance.span(), indices)` and the lowering
path also consults `enclosing_binders`, so the enclosing binder scope is the
plausible place to look. That is a pointer for whoever owns this code, not a
finding.

## The walker's incompleteness is known to its other callers

`all_model_expressions` has five other callers, and four of them work around it,
each with a *different* ad-hoc set of additions:

| Caller | Adds |
|---|---|
| `analyze_record_array_field_plans` (analysis.rs:1161) | structured + initial structured + function expressions |
| `collect_previous_operands` (model_roles.rs:69) | `when_chains` |
| `visit_equation_owners` (model_expression_owners.rs:26) | structured + initial structured |
| `discover_model_calls` (function_shapes/mod.rs:678) | algorithms, initial algorithms, `when_chains`, assert + initial assert |
| `analyze_comprehensions` (analysis.rs:636) | **nothing** |

`discover_model_calls` effectively reimplements the complete walk in 30 lines.
`analyze_comprehensions` is the only caller that takes the function's name at
face value, and it is the one that panics.

This was probed directly: user function calls placed inside a `for`-equation, a
`when`-equation and an `assert` all compile, because `discover_model_calls`
covers those sections by hand. The defect is therefore not "one missing field"
but a helper whose name promises a complete walk that it does not perform, with
each caller silently compensating to a different degree.

## Correcting the earlier version of this report

The first version of this report said the trigger was "a comprehension inside an
enclosing `for`-equation", and hypothesised that a loop instantiates one
comprehension per iteration against a single registered plan, so *the second*
lookup misses.

That is wrong, and the experiment that shows it is a one-iteration loop:

```modelica
for k in 1:1 loop            // exactly one iteration, one occurrence
  a[k] = sum({x*i for i in 1:2});
end for;
```

It still panics. There is no second lookup. The plan is never registered at all,
and the *first* lookup misses. The `for`-equation was incidental — it was simply
the first unwalked field the corpus happened to hit.

## Expected behaviour

Two independent fixes, both worth making:

1. **Make `all_model_expressions` actually complete**, and delete the four
   callers' ad-hoc compensation. That fixes the algorithm, `when` and `assert`
   triggers, and removes the trap for the next caller. The `for`-equation
   trigger is separate and needs its own diagnosis.
2. **Replace the `.expect` with a `DaeConstructionError`** carrying the
   comprehension's span. SPEC_0031 requires unproved semantics to fail with a
   typed diagnostic at their owning phase; a `.expect` on an invariant the
   analysis does not establish is neither typed nor diagnosable. Even after
   fix 1, this site should not be able to abort the process.

## Provenance checks

Not caused by any change in this branch:

- Panics on plain `rumoca compile` with no bitcode flags, and on `--emit dae-mo`.
- Reproduces with this branch's `rumoca-phase-flatten` change reverted to `main`.
- The reproducer contains no `connect(...)`, so the flatten change cannot execute.
