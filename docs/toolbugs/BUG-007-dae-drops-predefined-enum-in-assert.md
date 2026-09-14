# BUG-007: DAE lowering rejects the predefined `AssertionLevel` literal that Flat resolved correctly

| | |
|---|---|
| **Severity** | Medium — the 3-argument form of `assert` is unusable; fails cleanly, not a crash |
| **Component** | `rumoca-phase-dae`. *Not* resolve or flatten — both handle it correctly (shown below). |
| **Affects** | Every model using `assert(..., level)` or declaring an `AssertionLevel` variable. 27 uses across 7 MSL files. |
| **Found by** | Construct probing, 2026-09-13 |
| **Status** | **Fixed** |

## Summary

`AssertionLevel` is a predefined Modelica enumeration:

```modelica
type AssertionLevel = enumeration(error, warning);
```

It is not declared by any library — MSL 4.1.0 contains no `type AssertionLevel`
— because it lives in the built-in scope, alongside the signature MLS §11.2.3
gives for `assert`:

```
assert(condition, message, level = AssertionLevel.error)
```

**Rumoca already knows this.** `crates/rumoca-core/src/modelica_builtins.rs:44`
registers it next to `StateSelect`:

```rust
pub const PREDEFINED_ENUM_LITERALS: &[(&str, &[&str])] = &[
    ("StateSelect", &["never", "avoid", "default", "prefer", "always"]),
    ("AssertionLevel", &["warning", "error"]),
];
```

Resolve and flatten honour it. Flat comes out correct:

```console
$ rumoca compile H1.mo --model H1 --emit flat-mo
class H1_assertlevel
  Real x(start = 1, fixed = true);
equation
  der(x) = (-x);
  assert((x > (-1)), "bound", AssertionLevel.warning);
end H1_assertlevel;
```

DAE lowering then rejects that same Flat:

```
[ED008] unresolved Flat reference `AssertionLevel.warning`
  help: Flat IR must carry a declared, fully resolved coordinate identity
```

It treats the predefined enumeration literal as an ordinary coordinate
reference and looks for a declaration that, by definition, no model provides.
The defect is one phase later than the diagnostic's wording suggests.

## Reproducer

5 lines:

```modelica
model H1
  Real x(start=1,fixed=true);
equation
  der(x) = -x;
  assert(x > -1, "bound", AssertionLevel.warning);
end H1;
```

```console
$ rumoca compile H1.mo --model H1
[ED008] unresolved Flat reference `AssertionLevel.warning`
```

## The third argument is the whole trigger

```console
assert(x > -1, "bound")                            -> compiles
assert(x > -1, "bound", AssertionLevel.error)      -> ED008
assert(x > -1, "bound", AssertionLevel.warning)    -> ED008
assert(x > -1, "bound", level=AssertionLevel.warning) -> ED008
parameter AssertionLevel lvl = AssertionLevel.error;  -> ED008
```

Both spellings MSL actually uses fail: the named-argument form
(`Blocks/Sources.mo:1690`) and the declared-type form
(`Blocks/Logical.mo:936`, `parameter AssertionLevel assertionLevel=AssertionLevel.error`).

So it is not only the literals that are missing — the *type* is unresolvable
too, which a fix has to cover.

## `StateSelect` works, which locates the fix

The other MLS predefined enumeration goes through cleanly:

```modelica
Real x(start=1, fixed=true, stateSelect=StateSelect.prefer);   // compiles
parameter StateSelect ss = StateSelect.always;                 // compiles
```

Both are in the same registry entry. The difference is position:
`StateSelect` appears as a *variable attribute*, which DAE lowering handles,
while `AssertionLevel` appears as a *call argument*, which it does not. So this
is not a missing built-in — it is a missing case in the DAE lowering of
predefined enumeration literals outside attribute position.

## There is already a test asserting this should work

`crates/rumoca-phase-flatten/tests/structural_assert_folding.rs` exercises
`AssertionLevel.warning` and `AssertionLevel.error` and expects
*"the predefined AssertionLevel.warning identity exists"*. It covers flatten
only, which is why it passes while `rumoca compile` on the same construct
fails.

## Cross-check

OpenModelica 1.27.0-dev accepts both:

```console
$ omc check.mos
"Check of H1_assertlevel completed successfully.
"Check of H2_assert_error completed successfully.
```

Neither model declares `AssertionLevel`, so OMC is resolving it from the
built-in scope, which is where MLS puts it.

## Where it bites in MSL

27 occurrences in 7 files — 21 `AssertionLevel.warning`, 6 `AssertionLevel.error`:

- `Modelica.Blocks.Sources` (`level=AssertionLevel.warning` in two places)
- `Modelica.Blocks.Logical` (`parameter AssertionLevel assertionLevel`)

`Blocks.Logical` and `Blocks.Sources` are among the most widely extended
packages in MSL, so the reach is larger than the occurrence count suggests.

## The fix

Two defects, stacked.

**1. Validation read the wrong role map.** `validate_assertions` checked
`message` and `level` against the *coordinate* plan, so an enumeration literal
could not resolve — the identical defect `when` bodies had before they were
given the expression roles. `analyze_initial_owners` and
`analyze_initial_algorithm_owners` now thread `expression_roles` through, and
`validate_assertions` uses it for `message` and `level` while the condition
keeps the coordinate plan, since it is an event-domain expression.

**2. Construction demanded a numeric level.** With validation passing, the model
reached `Events::assert_with_level`, which rejected anything non-numeric:

```rust
if !ty.is_scalar() || !ty.scalar_type().is_numeric() {
    return Err(DaeConstructionError::ExpectedNumeric { ... });
}
```

MLS §11.2.3 types that argument as the predefined `AssertionLevel` enumeration,
so `Enumeration` is the *expected* form here, not an exception. Integer and Real
stay accepted because the level reaches the runtime as an ordinal.

All five spellings now compile:

```console
assert(x > -1, "bound")                                  -> compiles
assert(x > -1, "bound", AssertionLevel.error)            -> compiles
assert(x > -1, "bound", AssertionLevel.warning)          -> compiles
assert(x > -1, "bound", level=AssertionLevel.warning)    -> compiles
parameter AssertionLevel lvl = AssertionLevel.error;     -> compiles
```

## What remains

Simulation of a model carrying an assertion level still refuses, fail-closed
and with a clear message:

```
unsupported checked DAE semantics: assertion levels do not yet have checked
Solve lowering
```

So the models now reach the static detectors, but not the dynamic search. That
is a separate, smaller gap in `rumoca-phase-solve`.

## Provenance

- Fails on plain `rumoca compile`, no bitcode flags involved.
- The reproducer contains no `connect(...)`, so this branch's
  `rumoca-phase-flatten` change cannot execute.
