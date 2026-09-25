# Writable equation and execution IR: implementation inventory

This is the **pre-implementation inventory**. For the implemented APIs, native
demonstration and acceptance evidence, start with [README.md](README.md).

Inspected 2026-09-23 against fork HEAD
`a49b89dd99623de5e585adf8a93a8d543020157b` **plus the existing uncommitted
working tree**. The working tree already contains extensive RBC and SDK changes;
HEAD alone does not reproduce the inspected implementation.

This is delivery item 1 from [STUDENT_INSTRUCTIONS.md](STUDENT_INSTRUCTIONS.md).
It records current support and the implementation boundaries. It does not claim
that the supplied connector-logging example runs.

## Existing supported surfaces

| Surface | Evidence in this fork | Implication |
|---|---|---|
| Public equation interchange | [RBC schema](../crates/rumoca-bitcode/src/schema.rs), `RBC_VERSION = 2`; Python `VERSION = 2` | Extend the public contract explicitly; do not replace it with private Rust serialization. |
| Empty-model construction | [Python Model](../packages/rumoca-bitcode/rumoca_bitcode/__init__.py), `Model.empty`, `builder`, `raw_model`, `refresh`, `save` | Reuse the existing model and document owner. Empty models already own a source-table entry for generated spans. |
| Equation construction and rewriting | [Python Builder](../packages/rumoca-bitcode/rumoca_bitcode/builder.py), `add_variable`, `add_parameter`, `add_equation`, `add_derivative_equation`, `rewrite_equation`, `rewrite_operand` | Keep this as the equation-pass surface. Initial equations currently use `add_equation(..., initial=True)`. |
| Rust equation builder | [build.rs](../crates/rumoca-bitcode/src/build.rs) | Extend existing builders rather than creating a sanitizer-specific authoring API. |
| Validation and checked equation import | [validate.rs](../crates/rumoca-bitcode/src/validate.rs), [import.rs](../crates/rumoca-bitcode/src/import.rs), `rumoca bitcode check`, `compile-bitcode` | Structural validation exists; import reconstructs checked DAE. These are separate from executable freshness and backend support. |
| Numerical lowering | [phase-solve](../crates/rumoca-phase-solve/src/lib.rs), `lower_solve_package`, `lower_solve_model`, `lower_solve_artifacts` | Use the existing structural and Solve phases. Python must not implement another numerical lowering pipeline. |
| Scalar and tensor numerical programs | [ir-solve](../crates/rumoca-ir-solve/src/lib.rs), `ScalarProgramBlock`, `ComputeBlock`, `SolveProblem` | The numerical vocabulary and checked reconstruction already exist. Current internal `SOLVE_SCHEMA_VERSION` is 61. |
| Typed computation, regions and calls | [typed programs](../crates/rumoca-ir-solve/src/typed_program/program.rs), `TypedProgramBuilder`, `SolveOperation`, `conditional`, `fold`, `map`, `call` | Reuse these operations and construction rules for public execution editing; do not introduce a look-alike instruction interpreter in Python. |
| Internal complete-model replay | [model_wire.rs](../crates/rumoca-phase-solve/src/model_wire.rs), `solve_model_wire`, `deserialize_solve_model` | Internal schema version 1 already reconstructs checked numerical models and derived artifacts. It is an implementation mechanism, not the public RBC execution schema. |
| Consistent output publication | [ME session](../crates/rumoca-solver/src/fmi_me/session.rs), [host state](../crates/rumoca-solver/src/fmi_me/session/host_state.rs), [output driver](../crates/rumoca-solver/src/fmi_me/driver.rs) | Existing initialized, sampled and settled-event output paths are the integration points for executable publication. |
| Checked visible-value evaluation | `SolveModel.visible_value_rows`, `MeSimulationSession` output access, host `record_off_point` | Reuse output reconstruction and sampling transactions; do not guess slots or mutate solver history to log. Complete coverage of requested RBC connector members still needs to be established. |

## Missing public access to existing machinery

The following were checked by importing the current Python SDK and inspecting
the source and current CLI help:

| Target API in the example | Current status / adaptation |
|---|---|
| `Model.validate(strict=True)` | Absent. Expose the existing Rust validator and checked import through an installed compiler interface. `refresh()` only rebuilds Python views/counts. |
| `Builder.add_initial_equation(...)` | Absent convenience name; `add_equation(..., initial=True)` exists. |
| `ref`, `sub`, `mul`, `div` | Existing equation helpers use `coordinate`, `subtract`, `multiply`, `divide`. Final names may follow those helpers rather than duplicating them. |
| `owner=...`, `scalar_type=...` in the sample | Current `add_variable` uses a complete variable name and `value_type` ID. Component ownership must be supplied explicitly by a supported helper. |
| `Model.connectors` | Absent. There are `connections`, `connection_sets`, component entries, and per-variable connector roles. |
| `add_component`, `add_connector_type`, `add_connector`, `member`, `add_connection_set` | Absent public builder helpers. Existing RBC component, connection and flow-balance records are useful inputs; the helper must also generate the mathematical equations. |
| Equation/state removal | No dedicated public removal transaction was found. Raw table editing alone is insufficient: dense IDs and all references must be rebuilt consistently. |
| `rumoca_bitcode.execution.lower` and `Program` | The `rumoca_bitcode.execution` module does not exist. |
| Public execution insertion/replacement/removal | Absent. Checked Rust program construction is available but not exposed through the RBC SDK. |
| `rumoca bitcode run --execution=require` | Absent in the current source and CLI. `compile-bitcode --simulate` imports equations and performs lowering. |

The supplied script consequently requires substantive implementation before it
can run. It is not just a script whose method names need adjustment.

## Genuinely missing execution semantics

1. **Public executable artifact contract.** Define a versioned RBC projection of
   supported Solve programs, types, regions, calls and effects. Conversion must
   replay checked construction and reject unsupported variants. Publishing
   `serde_json::to_value(SolveModel)` as the SDK schema would violate the brief.
2. **Lifecycle and effects.** Add serializable `run_start`, `publish` and
   `run_finish` programs, snapshot reads, CSV resource declarations and ordered
   CSV operations to the canonical execution vocabulary. The current public RBC
   trace-point requests are not these executable instructions.
3. **Derivation and invalidation.** Bind execution to an equation digest,
   lowering version/options, revision and pass recipes. Recompute identity on
   verification/load/run, including raw edits. A changed equation must reject
   existing execution until explicit lowering and pass replay occur.
4. **Connector identity and observation mapping.** Add checked connector-instance
   identities and member ownership/type/order/orientation/provenance. Existing
   connection-set endpoint strings and member roles do not provide the complete
   requested identity contract. Bind member IDs to checked reconstruction
   expressions before elimination can lose them.
5. **Runtime execution of effects.** Execute lifecycle programs at the existing
   publication boundary, with read-only consistent snapshots, per-instance
   resources, structured failures and cleanup. A CSV loop over a returned
   trajectory would not implement this requirement.
6. **Pass replay.** Store pass identities, options and observation targets.
   Replay must detect a removed or changed target and fail visibly. A saved
   executable must run without the Python pass; explicit replay may require the
   registered authoring pass.

## Implementation sequence and ownership

| Step | Main owners | Acceptance evidence |
|---|---|---|
| 1. Finish the equation/connector authoring surface | Public RBC schema, checked importer, existing Python/Rust builders | Synthesize the two-state thermal model without source; validate/import it; prove two disjoint connection sets emit four equations exactly once. Add a multiway regression proving one flow sum per set. |
| 2. Expose executable programs | Public RBC execution schema and its checked mapping to `rumoca-ir-solve`; Python SDK facade | Inspect and replace an ordinary computation; edit supported control flow; reject wrong types and undefined registers using the shared authority. |
| 3. Add effects and artifact identity | Solve operation/type/effect definitions, RBC codec/validation and pass metadata | Lifecycle/resource validation, effect-order preservation, serialization, stale execution rejection after both builder and raw equation edits. |
| 4. Bind observations and publication | Structural/Solve lowering, existing solver output reconstruction and ME session | Resolve every requested member by semantic identity; publish one initialized row plus 50 samples without trial-evaluation rows or added physical events. |
| 5. Execute generic CSV effects | Real native runtime backend, CLI | Fresh process executes the saved programs and produces four files plus a manifest; duplicate sinks, unsupported operations and I/O failures are explicit. |
| 6. Demonstrate transformation and replay | Adapted supplied synthesis example, SDK integration tests | Run scales 1 and 2; compare logged and unlogged observables; modify an instrumented equation, reject stale execution, lower/replay, and verify the changed trajectory. |
| 7. Run complete acceptance gates | Supplied independent CSV checker plus SDK/Rust integration suites | Analytic temperatures/flows/energy, invalid programs, failed initialization, alias coverage, duplicate pass, cleanup and settled-event publication tests. |

The snapshot/logger additions need a documented extension to the active Solve
and public RBC contracts before implementation. The relevant existing governing
rules are [SPEC_0007](../spec/SPEC_0007_IR_PIPELINE.md) stages 3/4 and
[SPEC_0033](../spec/SPEC_0033_DEVELOPMENT_PROCESS.md) sections 2–6.
[SPEC_0045](../spec/SPEC_0045_SOLVE_EXECUTABLE_VOCABULARY_AND_PROFILES.md) is
currently **DRAFT**; its proposed operation taxonomy must not be described as
fully implemented or accepted. Adding lifecycle effects should extend existing
Solve ownership rather than create another canonical numerical stage.

## Checks performed for this inventory

The current SDK imports with RBC version 1. Capability probes confirmed the
present/missing methods above. `target/debug/rumoca bitcode --help` confirms
there is no execution `run` subcommand in that built binary; source inspection
also confirms the command is absent.

Existing builder regression baseline:

```sh
CARGO_BUILD_JOBS=4 RUST_TEST_THREADS=4 RAYON_NUM_THREADS=4 \
  python3 -m pytest -q packages/modelsan/tests/test_sdk_builder.py
```

Result: **8 passed**. The tests include empty-model validation, construction,
expression-order invariants and a synthetic decay simulation through
the existing binary. The binary was not rebuilt for this inventory, so this is
evidence for the available tool, not a fresh build of every working-tree change.

No connector CSV, execution-IR serialization, stale-artifact or replay acceptance
test has passed yet. The supplied checker is an independent oracle; its ability
to accept analytic fixtures cannot establish that Rumoca implemented logging.
