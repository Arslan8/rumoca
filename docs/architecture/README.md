# ModelSan architecture

One semantic representation, thin layers around it.

```
Modelica -> Rumoca -> canonical DAE bitcode
                            |
              +-------------+-------------+
              |             |             |
          analysis      passes      instrumentation
              |             |             |
              +-------------+-------------+
                            |
                        backends
                            |
                      observations
                            |
                       sanitizers
                            |
                findings -> dedup -> reporting
```

## The rule everything else follows

There is exactly one model representation: Rumoca's canonical DAE bitcode.
`modelsan/dae/` holds **bindings** over it — views whose ids are DAE ids — not a
second IR. Nothing in ModelSan can express a model that the DAE cannot, and
there is no translation step.

A sanitizer defines what a violation is. It does not know how the DAE is
serialized, how a tool is launched, how test cases are generated, or how
findings are printed.

## Layers

| Directory | Owns | Must not |
|---|---|---|
| `dae/` | reading, writing, traversing the canonical DAE | interpret anything |
| `analysis/` | dependency graph, SCCs, blocks, parameter chains | copy DAE objects |
| `passes/` | explicit DAE transformations | hide edits inside sanitizers |
| `instrumentation/` | what to observe, planned against a backend | contain tool-specific code |
| `runtime/` | the observation vocabulary | describe the model |
| `sanitizers/` | what constitutes a violation | print, mutate, or launch |
| `fuzz/` | test cases and hints | know which sanitizers are enabled |
| `backends/` | execution; all tool-specific detail | leak into anything above |
| `findings/` | one Finding shape, signatures, grouping | decide presentation |
| `reporting/` | turning findings into output | decide what is a bug |

`analysis/` results are results, not representations: an `AlgebraicBlock` holds
DAE equation and variable **ids**, so a finding anchored on a block resolves
straight back to the model.

## Capabilities, not a base class

There is no `Sanitizer` superclass. Five protocols exist and a sanitizer
implements only what it uses; the registry discovers capabilities by
`isinstance`.

```
StaticAnalyzer            reads the DAE, no execution
RuntimeObserver           judges an observation stream
InstrumentationRequester  needs something observed
FuzzHintProvider          knows values worth trying
DifferentialOracle        compares backends
```

Measured on the current set:

| Sanitizer | Static | Runtime | Instrumentation | Hints | Active on OMC |
|---|---|---|---|---|---|
| DomainSan | | ✅ | ✅ | ✅ | hints only |
| NumericSan | | ✅ | | | ✅ |
| RangeSan | | ✅ | | ✅ | ✅ |
| SolverSan | | ✅ | | | failure only |
| AssertSan | ✅ | ✅ | | ✅ | ✅ |
| DiscontinuitySan | ✅ | | | ✅ | ✅ |
| SingularitySan | ✅ | | | ✅ | ✅ |
| InitSan | ✅ | | | ✅ | ✅ |
| EventSan | | ✅ | | | ✅ |
| ZenoSan | | ✅ | | | ✅ |
| PhysicalSan | ✅ | ✅ | | ✅ | ✅ |
| **DivisorSan** | ✅ | | | ✅ | ✅ |
| DeterminismSan | | comparative | | | ✅ |
| DifferentialSan | | comparative | | | needs 2 backends |

15 of 17 components active against OpenModelica. The two that are not —
DomainSan's runtime check and SolverSan's timestep collapse — are reported as
skipped with the missing capability named, never as clean results.

## Signature vs evidence

```
signature   what bug is this?     model properties only
evidence    how was it reached?   time, values, test case
```

`findings/signature.py` names the excluded fields explicitly, because a
signature that includes simulation time makes every run report new bugs.

## Sanitizers implemented

Each answers the seven required questions in its module docstring. Summary:

| | Bug class | Distinct because | Signal | Needs transform? | Fuzzing role | Signature |
|---|---|---|---|---|---|---|
| **DomainSan** | operation outside its mathematical domain | names the *operation*, where NumericSan sees only the contaminated value | operand leaves the domain | yes, to observe a non-variable operand | hints: the exact domain edge | operation expression id |
| **NumericSan** | run completes carrying inf/NaN | fires with no restricted operation present — overflow, cancellation | non-finite or extreme value | no | oracle only | first non-finite variable id |
| **RangeSan** | value outside the model's own declared bounds | needs neither a non-finite value nor a restricted operation | observed value past `min`/`max` | no | hints: the bounds themselves | variable id + which bound |
| **SolverSan** | integrator cannot proceed | fires when there is *no trajectory to inspect*, which is the common case | failure, or timestep collapse | no | graded oracle — collapse precedes failure | reason + named DAE entity |

Overlap is expected and is not suppressed at detection. A division by zero is a
DomainSan finding and a SolverSan finding; `findings/deduplicate.py` decides
they are one bug, and `BugDatabase.overlap()` reports which detectors saw it.

## Five rules the code enforces

**1. A failed execution is still a valid execution result.**
No backend returns `None`. A run that died in initialization returns an
`ExecutionResult` carrying the phase it reached, a classified `ExecutionFailure`
and the tool's raw message. `trace=None` is an explicit fact, not an absence to
be inferred from.

**2. Coverage is capability-driven and explicit.**
Sanitizers declare `requires` per *component*, and the planner resolves it
against the environment before anything runs:

```
Result:
    domain.hints: enabled
    domain.runtime: skipped (observe_expression unavailable)
    numeric.runtime: enabled
    range.runtime: enabled
    solver.failure: enabled
    solver.collapse: skipped (observe_solver_steps unavailable)
```

This exists so that "no finding" is never ambiguous. Without it, a clean model
and an unobservable one look identical, and no finding count means anything.

**3. Canonical and backend identity are different types.**
`CanonicalAnchor` means *this is an exact entity in the DAE*. `BackendAnchor`
means *this is what the tool called it*. Never a sentinel id, never a hashed
name, never a sequential id standing in for a DAE id. A finding reports its
`anchor_quality` so a reader knows which it has.

**4. A missing canonical anchor never discards a finding.**
RangeSan reports `pump.medium.X = -0.13` violating `min = 0` from OpenModelica,
labelled `backend-only`, with a backend-namespaced signature. Losing the bug
would cost coverage; faking the id would corrupt identity for everything
downstream.

**5. SolverSan is a failure oracle, not a root-cause sanitizer.**
A solver failure is often the last symptom of a chain — a configuration makes a
block singular, the block makes the solver fail. SolverSan reports that the
execution failed and how the runtime described it, and is *not* suppressed when
a more specific sanitizer also fires. Correlating them is the deduplicator's
job; `sequence` preserves the order that makes it possible.

## Signatures

Readable, with the primary anchor spelled out rather than hashed away:

```
range:below-min:var:91:62596a8d                    canonical
range:below-min:openmodelica/tank.level:9487dea6   backend-only
solver:initialization-failure:exec:0a90a3f3        no entity anchor
```

The two `below-min` signatures are deliberately different. The same name in two
tools is not known to be the same entity, and a signature must not assert it.
Merging them is a later cross-backend deduplication step that needs evidence.

### Comparative oracles

`DeterminismSan` and `DifferentialSan` judge a *set* of results rather than one,
so `Pipeline.run_comparative` schedules the extra executions. They are opt-in
rather than part of `DEFAULT` because those executions cost real time.

`DifferentialSan` is the one sanitizer that can adjudicate the others: a failure
only one backend produces is that backend's gap, not the model's defect. Its
findings say so explicitly, because treating a single-tool failure as a model
bug already produced two false MSL findings in this project.

## Distinct classes, not one cause seen many ways

The brief's warning is that NaN, timestep collapse and a range violation are
often three consequences of one singularity. Two things keep that from inflating
counts:

* **Two different questions, two mechanisms.** `BugDatabase` groups by
  signature and answers *have we seen this bug before?*. It cannot answer *are
  these findings one bug?*, because a signature begins with the sanitizer's
  name on purpose — DomainSan's view of a division by zero and SolverSan's view
  of the resulting failure are different statements about the model.

  So `BugDatabase.overlap()` is structurally almost always empty, and that is
  correct rather than a defect. Cross-sanitizer grouping is
  `findings/correlate.py`, which builds **episodes**: findings from one
  execution that share an anchor or occur within a few solver steps of each
  other.

  ```
    init  singularity    vanishing-coefficient
   0.300  solver         timestep-collapse
   0.310  numeric        nan
  ```

  Three findings, one episode, causal order preserved. It deliberately does not
  name a root cause — co-occurrence is not causation, and asserting otherwise
  would be the same overreach as calling a single-tool failure a model defect.

  `summarize()` reports `findings`, `episodes` and `multi_sanitizer_episodes`
  separately, which is what says whether the suite is diverse or merely
  redundant.
* **Sanitizers that could collapse into each other are calibrated apart.**
  Chattering and Zeno are the clearest case: both are event pathologies, but
  chattering wants a hysteresis band and Zeno wants the accumulation removed.
  `test_event_discrimination` pins that a burst is not reported as Zeno, an
  accumulation is not reported as chattering, and — the calibration that
  matters — the event *pair* MSL's `CoupledClutches` fires at every clutch
  engagement is reported as neither.

## Known gaps

- `passes/` exists but no instrumentation pass is implemented, so
  `OBSERVE_EXPRESSION` is unsatisfiable on every current backend and DomainSan's
  runtime half cannot fire. The planner reports it as `skipped`; DomainSan's
  hint component still runs, so the sanitizer is `PARTIAL`, not disabled.
- No backend provides `OBSERVE_SOLVER_STEPS`, so SolverSan's timestep-collapse
  component is skipped. Its failure component works everywhere.
- `CANONICAL_IDENTITY` is unavailable from OpenModelica. RangeSan and NumericSan
  work anyway, on backend anchors; a sanitizer that genuinely needs DAE identity
  should declare that capability so the planner can stand it down.
- `legacy/` still holds the pre-layering modules. The corpus sweep tooling runs
  against them; they are not to be extended.

## Tests

`packages/modelsan/tests/test_architecture.py` — 25 assertions covering failure
without a trajectory, unsupported instrumentation, backend-only anchors,
canonical anchors, and backend error vs model failure. Run it directly; it uses
doubles, so it needs no tool installed.
- `legacy/` still holds the pre-layering modules. The corpus sweep tooling runs
  against them; they are not to be extended.
