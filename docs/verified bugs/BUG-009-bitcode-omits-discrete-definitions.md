# BUG-009: bitcode v1 carried no MLS Appendix B.1c definitions, so any discrete-valued variable broke round-trip

| | |
|---|---|
| **Severity** | High — broke round-trip for a very common construct; export reported success |
| **Component** | `rumoca-bitcode` (`schema.rs`, `export.rs`, `import.rs`, `validate.rs`) |
| **Found by** | Round-trip audit over 60+ construct probes, 2026-09-13 |
| **Status** | **Fixed**, with regression tests |

## Summary

`RbcModel` had `equations` (continuous residuals) and `events` (reinit, assert,
terminate) and no field for MLS Appendix B.1c — the definitions that say what a
discrete-valued variable *equals*. Those live in a separate DAE arena, and
export never read it.

So a model like this exported "successfully":

```modelica
model L1
  Real x(start=1, fixed=true);
  Boolean b;
equation
  der(x) = -x;
  b = x < 0.5;
end L1;
```

and then could not come back:

```console
$ rumoca compile L1.mo --model L1 --emit-bitcode l1.rbc
wrote bitcode v1 (cbor) to l1.rbc

$ rumoca compile-bitcode l1.rbc --summary
cannot rebuild a checked DAE from this bitcode:
  missing B.1c topology definition for identity 1
```

Dumping the artifact shows exactly what was lost — `b` is declared, and nothing
says what it is:

```jsonc
"variables": [
  {"id": 0, "name": "x", "role": "state"},
  {"id": 1, "name": "b", "role": "discrete_value"}   // declared…
],
"equations": [ {"id": 0, "residual": 5, "reads": [0]} ],   // …only der(x) = -x
"events": [],
"conditions": [ ... ],   // the relation x < 0.5 survives, unattached
```

The relation is carried as a condition, but the *binding* of `b` to it is gone.

## Scope

Every discrete-valued variable defined by a plain equation. That is a large
fraction of real models — every comparison producing a Boolean, every
`Modelica.Blocks.Logical` block, every Integer state machine variable.

Bisected to a sharp boundary:

| Construct | Round-trip |
|---|---|
| `Boolean b; b = x < 0.5;` | **failed** |
| `discrete Boolean b(start=false, fixed=true); b = x < 0.5;` | **failed** |
| `when change(b) then c = pre(c) + 1; end when;` | **failed** (via the `b` above) |
| `discrete Real d` assigned in a `when` | passed |
| pure continuous | passed |
| Integer *parameter* | passed |

The trigger is a discrete-valued variable with a B.1c definition — not `pre`,
not `change`, not `when`, all of which were red herrings in the first bisection.

## Why the test suite missed it

The 23 existing tests built `RbcModel` values directly and checked validation
and the codec. None constructed a discrete variable, and — more importantly —
**validation had no invariant requiring one to be defined**. The artifact was
internally consistent by every rule the validator knew. It was only the DAE's
reconstruction, one layer further on, that noticed.

That is the same shape as BUG-008: a defect in the *agreement* between two
components, invisible to any test of either one alone.

## The fix

1. **`schema.rs`** — `RbcDiscreteDefinition { targets, branches, provenance }`,
   `RbcDiscreteBranch { activation, values, provenance }`, and
   `RbcDiscreteActivation::{Always, When { trigger, guard }}`, plus
   `RbcModel::discrete_definitions` and a summary count. `Always` is a plain
   equation; `When` carries the trigger and guard that distinguish a `when`
   branch on the same target.
2. **`export.rs`** — `export_discrete_definitions` walks
   `discrete_value_owner_count` / `discrete_value_owner`, reading targets,
   branches and activations.
3. **`import.rs`** — `rebuild_discrete_definitions` replays through
   `construction.b1c(plan, ...)`, which takes the complete target plan up front
   so the topology is one transaction.
4. **`validate.rs`** — two new invariants, so a producer cannot write this
   artifact again:
   - `UndefinedDiscreteValue` — a `discrete_value` variable that no definition
     targets.
   - `DiscreteBranchArity` — a branch whose value count differs from its
     definition's target count.

## Verification

Semantics, not just acceptance. After the fix, `L1` round-trips *and* computes
the right answer:

```console
$ rumoca compile-bitcode l1-traced.rbc --simulate --t-end 1.0 --trace-out l1.csv
  x: 1 -> 0.3678        # e^-1
  b -> true at t=0.693  # ln 2, exactly where x crosses 0.5
```

Round-trip audit over 60+ construct probes: **0 export-but-cannot-import**,
down from 1 class covering 9 models; models that round-trip went 18 → 27.

The remaining 18 refusals are honest, declared v1 gaps
(`unsupported node: expression form not in bitcode v1`) — export marks them and
validation refuses. That is the fail-closed behaviour the format promises, and
is categorically different from this bug, where export claimed success.

Tests: 29 passing, was 23.

## Note on the diagnostic that found it

`missing B.1c topology definition for identity 1` names the variable's identity,
not its name, so the first read suggests a corrupt index rather than a missing
field. Resolving `identity 1` to `b` is a one-line improvement that would have
made this obvious immediately.
