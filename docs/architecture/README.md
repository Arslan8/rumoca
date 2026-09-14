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

| Sanitizer | Static | Runtime | Instrumentation | Hints |
|---|---|---|---|---|
| DomainSan | | ✅ | ✅ | ✅ |
| NumericSan | | ✅ | | |
| RangeSan | | ✅ | | ✅ |
| SolverSan | | ✅ | | |

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

## Known gaps

- `passes/` exists as a directory but no instrumentation pass is implemented, so
  `RequestKind.OBSERVE_EXPRESSION` is unsatisfiable on every current backend and
  DomainSan's runtime half never fires. The planner reports this as unsupported
  rather than letting DomainSan look clean.
- The OpenModelica backend reports variable *names*, not DAE ids, so
  `variable_id` is -1 for its observations and RangeSan cannot anchor on them.
  Inventing an id there would break every downstream anchor, so it is left
  unset and the sanitizer simply does not fire.
- `legacy/` still holds the pre-layering modules. The corpus sweep tooling runs
  against them; they are not to be extended.
