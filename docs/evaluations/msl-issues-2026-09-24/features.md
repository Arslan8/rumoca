# Why coverage stops, and what to implement

[Overview](README.md) · [Independent reproductions](independent.md) · [Seeded runtime results](runtime.md)

This is an implementation backlog derived from the current evaluation, **not
implementation performed by this evaluation**. Existing analyzers often already
find the arithmetic candidate. The missing piece can be orchestration, legal
test generation, compiler support, or an observation/oracle—not another generic
sanitizer.

## Recommended order

| Priority | Work | Evidence motivating it | Acceptance/regression requirement |
|---|---|---|---|
| 1 — high ROI | Decouple static analysis from backend preparation; provide a current CLI/campaign driver | SignalPWM has a direct static `f=0` finding, but `Pipeline.run` returns before static analysis when preparation rejects `string_conversion`. The advertised `modelsan.cli` module is absent. | A failed runtime preparation must retain all available static findings and report a separate coverage failure. A current supported entry point must execute the new APIs. |
| 2 — high ROI | Connect hints to legal, bounded testcase generation and execution | The pipeline collects hints but only executes nominal plus explicitly supplied cases. All seven independent variants have correct zero hints; that is not autonomous discovery. | Explicitly distinguish discovered versus externally seeded triggers. Preserve compound equalities, public visibility, component bounds/assertions, and a paired nominal control. Never mutate a protected/final field to manufacture a bug. |
| 3 — high ROI | Fix typed Boolean guard reasoning in the existing divisor consumer | Both CriticalDamping implementations retain `normalized=True` in current IR; the consumer drops the Boolean and leaves the `n=0` division unresolved. | Resolve literal/bound Boolean conditions and `not`/`and`/`or`; test both branches, unknown conditions, and earlier-branch exclusion. Do not treat UNKNOWN as true or false. |
| 4 — high impact | Preserve structural dependencies and add source-rebuild testcases; implement array shape/index obligations | CriticalDamping `n` determines `x[n]` but is exported tunable without a structural contract. An artifact override does not rebuild `x[0]`; exact source compilation rejects `x[1]` with ET009. | Carry shape/index/structural dependencies from their owning IR. Reject incompatible artifact overrides. Recompile legal public source configurations and attribute witness-specific elaboration failures separately from sanitizer detections. Include nominal `n=2`, invalid `n=0`, and valid empty-array controls. |
| 5 — high impact | Close actual bitcode/runtime observation and classification gaps | PWM rejects string conversion; CriticalDamping lacks requested array-state observations; CompareTransformers fails on an unknown coordinate even without instrumentation. | Preserve canonical identity and requested array elements. Implement missing expressions/coordinates or explicitly refuse the profile. Internal import/coordinate failures must be BACKEND_ERROR, not model bugs. Keep the original MSL witnesses in regression tests. |
| 6 — high impact | Extend native domain evidence to parameter bindings/starts, with source identity | Thyristor ITM/IH are found statically but runtime fails before Solve-row hooks, producing generic SolverSan evidence and an empty domain-fault list. | Report the actual pre-solve operation and operand, phase, legal witness, canonical/source anchor, and coverage. An empty fault list cannot imply safety when that evaluator is uninstrumented. |
| 7 — targeted expansion | Complete domain-operation coverage and source attribution | Native checks currently cover reached scalar SSA division, sqrt/log/inverse-trig. Unsupported tensor/call/assignment-prefix rows and `pow`/`mod`/`rem` are not fully covered. | Typed domain contracts for each implemented operation; reached-branch observation; zero/near-zero distinction; explicit omissions. Do not equate an instruction-level division fault elsewhere with the historical source denominator. |
| 8 — new oracle | Consume Jacobian telemetry with a scaled rank/conditioning analysis | Solver telemetry exists, but no runtime sanitizer uses it to establish algebraic rank/conditioning defects. Static structural counts are not a rank proof. | Match equation/variable identity, scaling, parameter configuration and solve phase; distinguish internal Newton trials from failed/accepted solves. Include structurally square but rank-deficient systems and well-conditioned controls. |
| 9 — correctness prerequisite for differential evaluation | Align comparable time/event grids before numerical comparison | Python DifferentialSan compares arrays by index and ignores the right trace's timestamps. | Compare only matched times with explicit event-side semantics, interpolation policy, variable identity, and exclusions. Different output grids must not produce a bug. Until fixed, use the existing official MSL trace comparator when making parity claims. |
| 10 — targeted expansion | Add explicit function/table/media contracts and enclosing witnesses for declaration-only records | 911 census entries have no executable model/witness. General finite-but-wrong formulas and function preconditions need an oracle not supplied by a division detector. | Generate a legal minimal enclosing model or analyze the source declaration directly. Use typed preconditions/invariants or documented assumptions; preserve UNKNOWN when semantics are absent. |

Priorities are engineering ROI judgments, not measured costs or promised recall
improvements. Fix the concrete producer/consumer first; do not hide a backend
failure by dropping its model from the corpus. The existing
[independent results](independent.md) provide small paired tests before rerunning
the complete report ledger.

## Existing capabilities versus actual gaps

- `DimensionSan`, `StructureSan`, `InitStaticSan`, and `NetworkSan` already exist
  but are not in `DEFAULT`; this audit explicitly enables them. Adding one to a
  profile is different from implementing an absent analysis.
- Component contracts and assumptions already exist. A negative resistance or
  zero inertia is not automatically a bug. Preserve component-specific limits,
  supported idealizations, disabled features, assertions, and intent advisories.
- EventSan/ZenoSan can consume native event timing, but temporal heuristics are
  not proofs of a library defect or event-condition identity.
- Numeric/range checks can observe invalid values but generally cannot explain
  a failure before samples exist. Literal declared bounds also do not replace a
  consistent API for evaluated bound expressions.
- NetworkSan needs complete connector identities and synchronized observations.
  Signed port power alone does not prove violation of passivity or energy
  conservation; stored energy and external sources matter.
- A wrong finite formula requires an independent invariant/reference. A model
  that runs without any numerical warning has not thereby been proved correct.
- Documentation, icons, API compatibility, and other nonnumerical upstream MSL
  issues are outside this numerical-sanitizer evaluation. This run did not
  enumerate the upstream GitHub issue tracker.

## Code owners to start with

| Concern | Current implementation |
|---|---|
| Static/runtime order and explicit testcase execution | [pipeline.py](../../../packages/modelsan/modelsan/pipeline.py) |
| Default versus opt-in analyzers | [sanitizer registry exports](../../../packages/modelsan/modelsan/sanitizers/__init__.py) |
| Witness proposals and guards | [witness.py](../../../packages/modelsan/modelsan/divisor/witness.py), [constraints.py](../../../packages/modelsan/modelsan/divisor/constraints.py), [sites.py](../../../packages/modelsan/modelsan/divisor/sites.py) |
| Override safety | [native overrides](../../../crates/rumoca/src/bitcode_execution/overrides.rs), [Rumoca backend](../../../packages/modelsan/modelsan/backends/rumoca.py) |
| Native reached-operation diagnostics | [domain_diagnostics.rs](../../../crates/rumoca-eval-solve/src/domain_diagnostics.rs), [DomainSan](../../../packages/modelsan/modelsan/sanitizers/domain.py) |
| Pre-solve binding domain failures | [NumericEvaluator](../../../crates/rumoca-eval-dae/src/numeric.rs), [runtime-value construction](../../../crates/rumoca-phase-solve/src/model_values.rs) |
| Solver telemetry interpretation | [rumoca_diagnostics.py](../../../packages/modelsan/modelsan/backends/rumoca_diagnostics.py), [SingularitySan](../../../packages/modelsan/modelsan/sanitizers/singularity.py) |
| Differential oracle | [comparison.py](../../../packages/modelsan/modelsan/sanitizers/comparison.py) |
| Component-contract/intent policy | [PhysicalSan](../../../packages/modelsan/modelsan/sanitizers/physical.py) |

## Reporting safeguards

Always retain separate fields for discovery, static candidate, seeded runtime
signal, source-specific verification, and independent bug adjudication. A
compiler rejection, unsupported importer, timeout, malformed trace, unrelated
same-target warning, or unsuccessful nominal run must not be counted as a
detected MSL issue. Conversely, an unobserved or unexecuted case must not be
counted as safe. Keep historical false-positive/non-defect controls in every
rerun and audit any renewed defect claim against the original reason.
