# Bug reports

Findings from running [ModelSan](../../packages/modelsan/README.md) over the
Modelica available in this tree.

Each report is self-contained: what the defect is, a minimal reproducer, how it
was found, and — where it matters — what was checked to rule out the reporter
being wrong.

## Open

| ID | Severity | Component | Summary |
|---|---|---|---|
| [BUG-001](BUG-001-comprehension-in-for-equation-panic.md) | High | `rumoca-phase-dae` | Compiler panics on a comprehension inside a `for`-equation. No diagnostic, process abort. 14-line reproducer. |
| [BUG-002](BUG-002-msl-zero-mass-within-declared-bound.md) | Medium | MSL 4.1.0 | `Mass(min=0)` and `Inertia(min=0)` admit a value that makes the model structurally singular. Three MSL examples affected. |
| [BUG-003](BUG-003-switchedrlc-zero-resistance.md) | Low | `examples/models` | `SwitchedRLC.mo` divides by an unbounded parameter. |

## Recorded limitations

| ID | Component | Summary |
|---|---|---|
| [LIMITATION-001](LIMITATION-001-index-reduction-drops-fixed-start.md) | `rumoca-phase-structural` | Index reduction refuses models where demoting a state would discard a `fixed = true` initial value. Deliberate and correct; filed so the coverage cost is visible. |

## Corpus swept

| Corpus | Models | Compiled | Exported partially | Notes |
|---|---|---|---|---|
| `examples/models` + `examples/modelsan` | 17 | 15 | 3 | 1 panic (BUG-001), 1 fail-closed refusal |
| MSL 4.1.0 examples (Electrical, Mechanics, Thermal, Blocks) | 74 | 51 | 32 | 23 refused, mostly unimplemented semantic owners |
| CogniPilot CMM examples | 4 | 3 | 3 | 1 refused (`unsupported semantic owner`) |

"Exported partially" means bitcode v1 could not represent every expression in
the model — functions, records and general arrays are not yet carried — so any
analysis of those models is working from an incomplete picture. ModelSan says
so before reporting anything else.

## MSL outcome in detail

74 models, 513 s:

| | Count |
|---|---|
| Compiled to bitcode | 51 |
| Refused at compile (fail-closed) | 23 |
| Exported partially (bitcode v1 gaps) | 32 |
| No property to search | 3 |
| Failed with declared values, nothing attributable | 2 (LIMITATION-001) |
| Searched | 46 |
| **Parameter-triggered failures found** | **3** (all BUG-002) |

Three findings across 46 searched models, all the same root cause, with no
false positives. The same sweep *before* the ModelSan baseline fix reported
five, of which two were misattributed pre-existing failures — which is why the
fix is recorded below rather than quietly applied.

## What is deliberately not listed here

**Fail-closed refusals.** Rumoca rejecting a construct with a typed diagnostic
is designed behaviour, not a defect. The most common was
`unsupported semantic owner ... rejected before simulation until its checked
DAE representation is implemented`. These are coverage limits, and only one is
filed (LIMITATION-001) because it blocks standard MSL models for a specific and
arguably closable reason.

**Bugs in ModelSan itself.** Three were found by running it on MSL and fixed in
`01c758d2`. Two of them produced *false bug reports*, which is the worst
failure mode a bug finder has:

- No nominal baseline, so a model that already failed had the first candidate
  blamed as its trigger. Two of five MSL findings were this.
- Candidate values outside a parameter's own declared range, so a "failure"
  could be ModelSan breaking a rule the model stated.
- A crash on a String-valued parameter's default.

**A miscount I made.** An early CMM sweep reported "78 of 81 models fail to
compile". That was a list-building error on my side — the list included partial
models, interfaces and package files, which are not runnable models. With a
corrected list, 3 of 4 compile. It is recorded here because the number appeared
in a status report before it was checked.

## Reproducing a sweep

```bash
cargo build -p rumoca --bin rumoca
cargo xtask repo modelica-deps ensure          # fetches MSL and CMM

export PYTHONPATH=packages/rumoca-bitcode:packages/modelsan
python3 -m modelsan.cli path/to/Model.mo \
    --model-name Full.Model.Name \
    --source-root target/msl/ModelicaStandardLibrary-4.1.0 \
    --rumoca ./target/debug/rumoca
```

## Reporting standard

A report here should let someone else decide whether to act without rerunning
anything:

1. **A reproducer that stands alone.** Minimal, no library dependencies where
   possible, with the exact command and exact output.
2. **The trigger, isolated.** Not "this model fails" but which single
   construct or value makes the difference, shown against a variant that
   works.
3. **Provenance.** What was checked to confirm the finding is not caused by
   local changes, and not a pre-existing failure being misattributed.
4. **An honest severity.** BUG-002 is a latent fragility, not a crash in
   correct usage, and says so.
5. **Root cause separated from hypothesis.** BUG-001 gives a probable
   mechanism and labels it as a hypothesis from reading the code, because it
   was not verified.
