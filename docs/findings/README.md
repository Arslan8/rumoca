# ModelSan findings

Bugs in **target programs** — Modelica models and libraries. This is what
ModelSan is for and the only thing that counts as a result.

A finding is a model that is *valid* and *behaves incorrectly* under some
reachable parameter value, initial state, or execution condition. Not a model
that fails to parse, and not a limitation of any tool used to find it.

**How a candidate becomes a finding is written down separately**, in
[`../method/`](../method/README.md). Every stage there exists because something
was reported that turned out not to be a bug; the numbers each stage removed are
recorded with it.

Tool defects encountered along the way are in [`../toolbugs/`](../toolbugs/).
They are engineering cost, not results — they belong there for the same reason
a crash in AddressSanitizer is not a finding about the program under test. They
matter here only because they cap coverage, which the table below records.

## Findings

| ID | Severity | Target | Trigger | Cross-confirmed | Summary |
|---|---|---|---|---|---|
| [BUG-010](BUG-010-inductor-documents-zero-it-cannot-honour.md) | High | MSL 4.1.0 `Analog.Basic.Inductor` | `L = 0` | 3 models | No bound at all, and the documentation explicitly says zero is allowed. Both tools fail. `Capacitor` carries the identical sentence and honours it. |
| [BUG-011](BUG-011-fluxtubes-b-mymax-unguarded-divisor.md) | Medium | MSL 4.1.0 `SoftMagnetic.BaseData` | `B_myMax = 0` | 2 models | Unguarded divisor in two files, no declared lower bound. |
| [BUG-012](BUG-012-variablepermeance-unbounded-input.md) | Medium | MSL 4.1.0 `FluxTubes.VariablePermeance` | permeance input ≤ 0 | 1 model | Sole coefficient supplied as an *unbounded input*, where the declared bound is the only possible defense. |
| [BUG-002](BUG-002-msl-zero-mass-within-declared-bound.md) | Medium | MSL 4.1.0 `Translational.Mass`, `Rotational.Inertia` | `m = 0` | 4 models | `min=0` admits a value that makes the model structurally singular. |
| [BUG-003](BUG-003-switchedrlc-zero-resistance.md) | Low | `examples/models/SwitchedRLC.mo` | `R = 0` | — | Divides by a parameter with no declared lower bound. |
| [BUG-005](BUG-005-multibody-rotor1d-zero-inertia.md) | Medium | MSL 4.1.0 `MultiBody.Parts.Rotor1D` | `J = 0` | static only | Same defect as BUG-002 in a package that report did not cover. |
| [BUG-006](BUG-006-bound-propagated-into-a-different-component.md) | Medium | MSL 4.1.0 `OpAmpCircuits.Der` | `k = 0` | static only | The unsound bound and the singular coefficient are in *different components*, linked by `C = k/(2*pi*f*R)`. No per-component check finds it. |

**7 findings, 5 of them in MSL itself.** All are latent parameter-triggered
failures: the model simulates cleanly at its declared values and fails at a
value its own declaration permits.

**10 model instances are confirmed in two independent tools** — Rumoca and
OpenModelica 1.27.0-dev — each passing at declared values and failing at the
trigger. Cross-confirmation is required before anything is listed here, for the
reason below.

## Why every finding is cross-confirmed

A failure in one tool is ambiguous. `Inductor.L = 0` produces `0 = v`, which a
tool could plausibly fail on merely by not re-indexing a degenerate equation —
that would be a gap in the tool, not a defect in MSL. Running the same trigger
through a second, mature implementation settles it.

It changes the answer in practice. Of 12 parameter-triggered failures Rumoca
found in MSL and ModelicaTest:

| | Count |
|---|---|
| Confirmed — both tools pass at declared values and fail at the trigger | **10** |
| **Excluded** — OpenModelica survives the trigger, so the failure is Rumoca's | **2** |

The two excluded are `Rotational.Examples.CompareBrakingTorque` and
`Translational.Examples.CompareBrakingForce`. Without this stage they would have
been reported as MSL bugs, and they are not.

## In progress: OpenModelica-backed sweep

The findings above came from Rumoca, which compiles 332 of 847 models. The
dynamic search now also runs through OpenModelica, which builds ~93% — see
[the method note](../method/README.md) for why the pipeline is dual-backend
rather than switched.

**Provisional, at 453 of 827 models swept:**

| | Count |
|---|---|
| Candidate (class, parameter) groups | 394 |
| Verified past guard, reachability and attribution | 261 |
| …in core library rather than Examples/Utilities | **73** |
| — `zero-permitted-by-bound` (strongest claim) | 16 |
| — `zero-permitted-by-omission` | 54 |
| — `fails-at-its-own-positive-bound` | 3 |

These are **not yet filed as findings.** They still need cross-confirmation in
Rumoca where it can compile the model, and 133 were dropped for a known recall
gap — parameters declared in a base class, which the lookup does not follow yet.

Nearly all of them are instances of one thing, which is written up as a study
rather than as 73 bug reports: [MSL components inherit SI type bounds their
equations cannot honour](si-type-bounds.md).

## Studies

| | Summary |
|---|---|
| [SI type bounds](si-type-bounds.md) | Where MSL's declared domains actually come from, and the three ways components inherit a bound they cannot keep. Includes the sharpest single item found: MSL defines `SelfInductance(min=0)` and `Basic.Inductor` does not use it. |
| [min=0 census](min0-census.md) | 326 `min=0` declarations in MSL against 147 correctly guarded. Records that the source-text form of this check runs at 23% precision and why the detector belongs on the DAE. |

## Full-corpus sweep

847 models — MSL 4.1.0 examples, ModelicaTest, CogniPilot CMM, repo examples —
with every detector, 81 minutes:

| | Count |
|---|---|
| Models attempted | 847 |
| Compiled to bitcode | 332 |
| Refused at compile (typed diagnostic, fail-closed) | 515 |
| Exported only partially (bitcode v1 gaps) | 198 |
| Failed at declared values, nothing attributable | 27 |
| **Searched** (clean baseline, parameters varied) | **289** |
| **Parameter-triggered failures found** | **19** |
| …of which in MSL / ModelicaTest | 12 |
| …of which survive cross-confirmation in OpenModelica | **10** |

The remaining 7 are in repo examples and CMM, including three fixtures written
for this project, which are not counted as findings.

Compile refusals are dominated by one diagnostic — `ED019`
(`unsupported Flat semantic owner`) accounts for 267 of 515. That single gap,
not detector strength, is the binding constraint on how many findings this
corpus can yield.

## Detectors, and what each has produced

| Detector | Needs the model to compile? | Findings |
|---|---|---|
| Singular-coefficient risk (`find_singular_risks`) | yes | BUG-002, BUG-005, BUG-006, BUG-010, BUG-012 |
| Unsafe-domain parameter search (`find_domain_sites`) | yes | BUG-003, BUG-011 |
| Declared-range breach (`declared_ranges`) | yes | — |
| Declaration contradictions (`declcheck`) | **no** | 0 across 5 348 files (see below) |
| Cross-tool confirmation (`crossconfirm`) | yes | *filters* — removed 2 false findings |
| OMC-backed parameter search (`omc_backend`) | **no** | 73 core-library candidates, in verification |

`declcheck` looks for a declaration that contradicts itself: `min > max`, a
`start` or default outside the declared range, a non-positive `nominal`. It
reads source only, so it covers 100% of any corpus. It reports **zero** across all
5 348 files of MSL 4.1.0, ModelicaTest, CMM and the repo examples — a real
negative result, validated against a synthetic file where it catches all 8
planted contradictions and leaves the clean declaration alone. Mature Modelica
libraries do not contradict themselves *within* a declaration; the defects are
between a declaration and the equations that use it.

## The coverage problem, stated honestly

Every detector except `declcheck` needs Rumoca to compile the model, and Rumoca
compiles a minority of MSL. That is the binding constraint on how many findings
this can produce, and it is why the tool bugs in `../toolbugs/` were worth
fixing at all — each one widens the set of models the detectors can see.

Concretely: 515 of 847 models never reach a detector at all, and 198 more are
analysed from an incomplete picture. The findings above come from the 289 that
were fully searched.

## Reporting standard

A report here should let someone else act without rerunning anything:

1. **A reproducer that stands alone**, with exact command and exact output.
2. **The trigger isolated** — not "this model fails" but which single value
   makes the difference, shown against a variant that works.
3. **A nominal baseline** — the model simulating cleanly at declared values, so
   the failure is attributable to the trigger and not pre-existing.
4. **Honest severity.** BUG-002 is a latent fragility, not a crash in correct
   usage, and says so.
5. **Confirmed separated from inferred.** Where a model could not be simulated
   end-to-end, the report says which part is read off the source.
