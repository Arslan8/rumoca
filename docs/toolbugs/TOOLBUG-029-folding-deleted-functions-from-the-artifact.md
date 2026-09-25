# TOOLBUG-029: constant folding deleted functions from the artifact

**Status:** fixed 2026-09-25
**Found:** while repairing the in-flight flatten work. 26 workspace tests were
failing; 25 of them were this.

## The defect

`fold_pure_constant_calls` evaluated *every* pure call whose arguments were
settled at translation time, anywhere in the model, and replaced it with its
result. Two consequences, neither intended.

**Pruning then deleted the callee.** The pass ran before
`prune_unreachable_functions`, so a folded call left its function with no
references and reachability removed it — although the source calls it. This
emptied the collected function table for every fixture whose calls take
literal arguments, including the author's own
`inherited_default_arguments_keep_their_concrete_package_binding`, which
iterates `flat.functions` and evaluates each one.

**The function never reached the DAE.** Ordinary source such as

```modelica
scaled = elementLoop({{1.0, 2.0, 3.0}, ...}, {0.5, 1.0, 2.0});
```

folded whole, so `elementLoop` was absent from the compiler's own output
artifact. Twelve slice-compaction tests pin the loop nesting and statement
shape of exactly that function; their file says so explicitly, because
"otherwise refusing every compaction would satisfy this file".

## Why it matters beyond the tests

Deleting a declared function from the DAE because of how one call site happened
to be written is not recoverable downstream. Every consumer that reads
`model.functions` — the bitcode exporter, `ModelSan`, anything doing
reachability or coverage over callables — sees a model whose functions depend
on whether a caller used literals. A simulation is unaffected, which is what
makes it dangerous: the value is right and the structure is gone.

## Fix

Two changes, both small:

1. **Reachability is decided before folding.** `prune_unreachable_functions`
   now runs first, so the call graph as written determines what is kept.
2. **Folding is scoped to what its own docstring claims** — "pure calls whose
   actual inputs are settled at translation time" — meaning the bindings and
   attributes of parameters and constants, not arbitrary equations. The
   structural need the module was written for (a constant `fill`/`zeros`
   dimension reaching checked DAE as a literal integer) is already served by
   `package_constants.rs`, which folds shape expressions.

Three fixtures whose calls take literal arguments were switched to `time`, the
same shape the author's own new fixtures use (`Local.f(time)`); each of those
tests observes a surviving call rather than asserting that folding must not
happen.

## Measured

| Configuration | passed | failed |
|---|---:|---:|
| HEAD (pre-existing repo debt) | 6853 | 10 |
| In-flight work, unmodified | 5778 | 46 |
| + reachability before folding | 6418 | 36 |
| + folding scoped | 6880 | 11 |
| + [TOOLBUG-030](TOOLBUG-030-evidence-defaulted-to-empty.md) | **6880** | **10** |

The final 10 are the pre-existing failures that also fail at HEAD; nothing
beyond them remains. No test required the unscoped folding: with it disabled
entirely, only the same pre-existing set failed.

## Note for whoever owns the feature

With reachability decided first, a function whose only call folds away is now
retained as dead weight. If shrinking the table was part of the intent, that
wants a *second* pruning pass after folding, explicitly allowed to drop what
folding orphaned, kept distinct from reachability-as-written. That was not
added here, because it changes what the feature does.
