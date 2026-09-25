# Inherited package constants: compiler repair

The inherited package constant blocker is fixed in Flatten. The unmodified
MSL 4.1.0 GasControl, GasRoundTrip, and WaterRoundTrip probes now emit RBC and
run through Rumoca's native source simulation path. This fixes compiler access
to the reported behavior; detecting the finite wrong result still requires an
explicit round-trip contract.

| Probe | Before RBC export | After RBC export | Native recovered temperature |
|---|---|---|---:|
| GasControl | ED008: unbound `cp_const` | succeeds | 299.99999999999994 K |
| GasRoundTrip, upstream #4749 | ED008: unbound `cp_const` | succeeds | 5204.053616778445 K |
| WaterRoundTrip, upstream #4750 | ED008: unbound `cp_const` | succeeds | 327.4574409665021 K |

All three inputs request 300 K. Native runs used `t_end=0.1`, `dt=0.025`, and
completed with five samples and no termination. The two faulty round trips
remain finite, illustrating why a generic nonfinite-value sanitizer cannot
establish these defects by itself.

## Root cause and ownership

A reduced source with no MSL names reproduces the first divergence:

```modelica
partial package Base
  constant Real cp;
  function f
    input Real x;
    output Real y;
  algorithm
    y := cp*x;
  end f;
end Base;
package Concrete
  extends Base(cp=3);
end Concrete;
model Probe
  Real y=Concrete.f(time);
end Probe;
```

Resolve supplies the correct constant declaration identity. Flat publishes a
callable exposed as `Concrete.f`, but its body still reads the unbound `Base.cp`
and has no effective concrete binding. The DAE constructor correctly rejects
that producer error with ED008. Both direct and locally aliased calls fail,
ruling out record constructors, the MSL equations, and native integration as
the cause.

Flatten now builds a constant environment for the exact package exposure from
resolved declaration IDs and resolved modifier targets. It specializes function
bodies, defaults, and shapes without changing explicitly qualified reads from
another package or function-local declarations. Declaration-only shape folding
previously erased the reference too early; function metadata now preserves it
until exposure specialization. Scalar constant expressions such as `size(...)`
are evaluated before checked array construction. DAE validation remains strict.

The governing rules are MLS §5.3 (enclosing constants), §7.2 (modification
context and precedence), §4.4.4 (acyclic bindings), SPEC_0001 (resolved identity),
SPEC_0007 (Flat ownership), and SPEC_0033 (first divergent phase and validation).
No model name or reported issue number participates in the compiler behavior.

## Validation and limits

`cargo test -p rumoca-phase-flatten --lib --tests --quiet` passed **682 tests**:
620 unit tests and 62 integration tests. Six new integration cases exercise
distinct inherited values, an abstract unbound constant, local shadowing,
explicit qualification, modified array dimensions, and default arguments.

The fixed 20-model SPEC_0033 canary ran before and after, with one attempt per
phase and the default time budgets. Both commands exited zero. The baseline
disabled only this fix and restored the previous function metadata producer;
all other existing worktree changes were preserved. Afterward the fix was
restored and the final CLI rebuilt. No baseline was promoted.

| Canary observation | Before | After |
|---|---:|---:|
| Selected models | 20 | 20 |
| Models reaching DAE | 11 | 11 |
| Native simulation completions | 8 | 8 |
| Compared traces in high-agreement band | 8 | 8 |
| DAE refusals | 9 | 9 |
| Later solve/runtime failures | 3 | 3 |
| Candidate traces missing or skipped | 0 | 0 |

There are **no per-model status changes** in this canary. It is a focused
partial snapshot, not a 566-model cohort parity claim. The remaining canary
failures are retained by name and reason in the evidence JSON.

Changed files pass rustfmt and `git diff --check`. Clippy is blocked by existing
complexity errors in unchanged functions: `process_component_instance` in
Flatten (107 lines), `analyze` in DAE (107 lines), and excessive nesting in
Instantiate's `attributes.rs`. The library-only check independently reaches the
same existing Flatten failure. These checks are recorded as failures, not passes.

The [durable result record](compiler-specialization-results.json) includes
commands, binary/source hashes, per-model canary rows, and native values. Full
before/after Flat, RBC, HTML, and log artifacts are under
`target/modelsan-media-specialization-20260924/`. The native runs are behavioral
evidence. The subsequent [ModelSan detection campaign](detection-followup.md)
records the actual contract-pipeline violations separately.
