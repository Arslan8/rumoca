# Rumoca Bitcode — Milestone 0 Notes

Findings from studying Rumoca before implementing Rumoca Bitcode (`.rbc`).

Everything here was checked against `rumoca 0.10.0` at commit `97eb3ab7`.
Claims marked *(verified)* were reproduced by running the compiler; claims
about code cite the file and line.

General orientation on the four IRs, the code-generation path, and provenance
lives in [`rumoca_notes.md`](rumoca_notes.md). This document covers only what
matters for the bitcode project.

**Headline:** two findings change the plan materially.

1. **Import validation is mostly already built.** DAE deserialization does not
   populate structs — it *replays construction operations* through the same
   checked constructors production compilation uses, and there are 70 distinct
   construction invariants. Milestone 3 is not "write a validator"; it is
   "translate RBC into construction operations."
2. **Connector provenance is lost in two places, not one.** The set-level
   structure never reaches Flat's output at all, and the per-equation endpoints
   are dropped at one identifiable line in DAE lowering. Milestone 6 needs
   changes at both layers.

---

## 1–3. Build, compile, inspect

`cargo check --workspace` passes. `cargo build -p rumoca --bin rumoca` gives a
working CLI. Toolchain is pinned `nightly-2026-02-27`; the first cargo
invocation downloads it. Build under `/data` — `target/` exceeds 5 GB.

IR dumps: `--emit {ast-json, flat-mo, flat-json, dae-mo, dae-json, solve-json}`.

Source-root discovery loads every `.mo` beside the target file, so compiling
anything in `examples/models/` fails on unresolved `Modelica.*` unless
`cargo xtask repo modelica-deps ensure` has run. Copy individual models to an
isolated directory instead.

*(verified)* The residual transformation, end to end:

| Stage | `der(x) = -k*x` |
|---|---|
| Source | `der(x) = -k*x;` |
| Flat | `der(x) = (-(k * x));` |
| DAE | `0.0 = (der(x) - (-(k * x)));` |
| Solve | `LoadP[0]`, `LoadY[0]`, `Mul`, `Neg`, `StoreOutput` |

---

## 4. The existing DAE serialization code

`crates/rumoca-ir-dae/src/model/wire.rs` (1800 lines) plus seven submodules:
`records.rs`, `expression_wire.rs`, `equation_systems.rs`, `function_graph.rs`,
`function_replay.rs`, `quotient_projection.rs`, `helpers.rs`.

### It is operation-shaped replay, not a data dump

This is the single most important thing to understand. From `wire.rs:155`:

> The columns are operation-shaped: each record names the semantic owners,
> exact provenance, explicit operands, and references one construction
> operation needs. Facts the operation itself produces — derived types,
> variabilities, domains, scopes, and generated fold results — are absent,
> because replay re-issues them through the same checked operation.

And the decode path (`wire.rs:201`):

```rust
impl<'de> Deserialize<'de> for Dae {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error> {
        let wire = DaeWire::deserialize(deserializer)?;
        if wire.schema_version != DAE_SCHEMA_VERSION { /* reject */ }
        Dae::construct(wire.source_map, |dae| reconstruct(&wire.storage, dae))
            .map_err(serde::de::Error::custom)
    }
}
```

There is **no unchecked path into a DAE.** Decoding runs the same
`Dae::construct` closure production compilation runs, so every invariant in §6
is enforced on every decode.

### Consequences for this project

- **Milestone 3's hardest requirement is largely satisfied by the existing
  architecture.** The brief says "Rumoca MUST NOT trust imported bitcode" and
  lists schema → reference → type → invariant validation. For the DAE layer,
  reference/type/invariant validation already happens by construction. Our
  importer needs to translate RBC into construction operations and let the
  existing machinery reject what is invalid.
- **`Dae::construct` is `pub`** (`model.rs:589`). A *new workspace crate* can
  build a checked DAE without living inside `rumoca-ir-dae`. This is what lets
  RBC stay decoupled from the internal wire schema.
- **The wire records are private** (`struct DaeWire`, `struct StorageWire` —
  no `pub`). We cannot and should not reuse them. That matches the brief's §7
  requirement; it is enforced by the module system rather than by discipline.
- **The operation-shaped design is worth imitating at the public level.** An
  RBC record that names owners, provenance, and operands maps cleanly onto the
  construction API. An RBC that mirrors Rust struct layout would not.

### Two JSONs, do not confuse them

| | `--emit dae-json` | template projection |
|---|---|---|
| Producer | `Serialize for Dae` | `codegen/dae_backend.rs::project` |
| Version | `DAE_SCHEMA_VERSION` = **33** | template schema **5** |
| Shape | `{schema_version, source_map, storage{…}}` | `{schema, variables[], systems{…}}` |
| Purpose | persistence + checked replay | semantic arrays for templates |

The template projection has held at 5 while the internal wire went to 33 —
useful evidence that a curated public projection can be stable over an
unstable internal one. It is a reasonable starting point for RBC's *content*,
but it is read-only (no replay path) and is not a container format.

### Size measurements *(verified)*

Internal `--emit dae-json`, which sets an upper bound on a naive format:

```
SympyDecay      8,842 bytes    2 vars    1 eq     9 expr-nodes
SwitchedRLC    29,933 bytes    9 vars    5 eqs   43 expr-nodes
Circuit.Test   76,967 bytes   23 vars   20 eqs  104 expr-nodes
```

~750 bytes per expression node. A four-component RC circuit is 77 KB; an
MSL-scale model extrapolates to double-digit MB. Much of this is the embedded
full source text plus per-node provenance records. A binary encoding and a
leaner provenance representation both matter.

---

## 5. Round-trip tests

About a dozen round-trip tests across `crates/rumoca-ir-dae/src/tests/`:
`range_wire.rs`, `external_functions.rs`, `runtime_owner_replay.rs`,
`derived_wire.rs`, `model_event_transactions.rs`, `b1c_owners.rs`, and the
property harness `wire_roundtrip_verification.rs` (783 lines).

### The dual-codec property is the interesting part

`wire_roundtrip_verification.rs` encodes under **both** `bincode`
(ordinal-tagged) and `serde_json` (name-tagged), decodes, re-encodes, and
demands identical bytes. Its header documents why: `bincode` tags an enum
variant by declaration index, so it catches ordinal-shift bugs a name-tagged
codec sails past. Two real near-misses are recorded — schema 14 *inserted*
`ConditionNodeWire::Always` mid-enum, schema 15 *appended*
`CoordinateWire::PreState`/`PreAlgebraic`. There is a comment in
`expression/nodes.rs:164` explaining that a variant was appended rather than
grouped with its siblings for exactly this reason.

`derived_wire.rs` asserts the complementary property: the wire **omits**
constructor-derived facts and still round-trips canonically.

Note `bincode` is a **dev-dependency** of `rumoca-ir-dae`, not a shipped one.
Nothing in production emits binary DAE. Production `bincode` use in
`rumoca-compile` is for parsed-source-root caches and `StoredDefinition`, not IR.

### Lessons for RBC

- Test RBC under a name-tagged *and* an ordinal-tagged view from day one. If
  RBC uses protobuf, field numbers are the ordinal identity — the same class of
  bug applies.
- "Re-encode what you decoded and demand identical bytes" is a cheap, strong
  determinism test, and Milestone 2 asks for byte-identical output anyway.
- The existing harness walks enum variants through a total match with no
  wildcard arm, so adding a variant without covering it fails to compile.
  Worth copying for RBC's expression and role enums.

---

## 6. DAE invariants checked during construction

`DaeConstructionError` (`crates/rumoca-ir-dae/src/error.rs`, 390 lines) has
**70 variants**. This is the validator's work list, and every one is already
enforced on decode. Grouped:

| Group | Variants |
|---|---|
| Provenance and source | `MissingProvenance`, `UnknownSource`, `InvalidSourceRange` |
| Types and shapes | `InvalidEffectiveTypeId`, `ConflictingEffectiveType`, `TypeMismatch`, `ShapeMismatch`, `ExpectedScalar`, `ExpectedNumeric`, `ExpectedPrimitiveRelation`, `InvalidVariableType` |
| Identity and references | `UnknownId`, `DuplicateDefinition`, `DuplicateTopology`, `DuplicateKey`, `CapacityExceeded` |
| Expressions | `InvalidExpressionForm`, `InvalidArity`, `EmptyArray`, `ZeroRangeStep`, `InvalidRangeBound`, `RangeExtentOverflow`, `InvalidArrayExtent`, `InvalidSubscript`, `InvalidEnumerationOrdinal` |
| Functions | `InvalidFunctionScope`, `InvalidFunctionValueRead`, `InvalidFunctionCoordinate`, `InvalidFunctionDependency`, `InvalidRecursiveFunctionGroup`, `MissingFunctionCallCertificate`, `InvalidCallProjectionOwner`, `InvalidBinderScope`, `IllegalImpureCallContext` |
| Clocks and time | `InvalidClockLattice`, `MissingPreviousClockOwner`, `InvalidClockedOperand`, `MissingClockDomainOwner`, `MissingClockOwnership`, `ConflictingClockOwnership`, `InvalidDynamicTimeEventDeadline`, `NonStaticDiscontinuity` |
| Discrete and events | `InvalidDiscreteTopologyPlan`, `InvalidDiscreteTargetOrder`, `EmptyDiscreteValueOwner`, `InvalidDiscreteBranchSet`, `UnissuedDiscreteDependency`, `EmptyModelEventTransaction`, `UndeclaredModelEventTarget`, `IncompleteModelEventTransaction`, `UnsupportedStructuredEvent` |
| Roles and domains | `InvalidVariableRole`, `InvalidDomain`, `UndefinedBuiltinDomain`, `InvalidPositiveParameter` |
| Strings | `ConflictingPredefinedString`, `ConflictingPredefinedStringRegistration`, `MissingPredefinedString`, `InvalidStringConversionSource`, `InvalidSignificantDigitsSource`, `InvalidStringFormatSource` |
| External functions | `InvalidExternalSymbol`, `InvalidExternalLinkage` |
| Replay bookkeeping | `DuplicateRuntimeQuotientOwner`, `InvalidQuotientReplayStage`, `UnconsumedQuotientReplay`, `MissingHistoryOperatorCertificate`, `IncompleteDefinition` |
| **Wire-specific** | `InvalidSchemaVersion`, `MalformedWire` |
| Scope | `Binder`, `Function`, `ScopeViolation` |

The last two rows matter most for us: `InvalidSchemaVersion` and
`MalformedWire` are the only two variants that exist *because* of
deserialization. Every other invariant is a property of a valid DAE regardless
of how it was built — which is why replay gets them for free.

**Adversarial import tests (Milestone 39 in the brief)** map onto these
directly: "reference to nonexistent variable" → `UnknownId`; "duplicate ID" →
`DuplicateDefinition` / `DuplicateKey`; "wrong expression type" →
`TypeMismatch` / `InvalidExpressionForm`; "malformed event" →
`IncompleteModelEventTransaction` / `UndeclaredModelEventTarget`; "invalid
connector reference" → `UnknownId`. The rejection machinery exists; our tests
must prove RBC decoding actually reaches it rather than bypassing it.

---

## 7. Connector provenance — what survives flattening

**This is the finding that costs the most work, and it is worse than a single
lossy line.**

### What Flat *builds* but does not keep

`rumoca-ir-flat/src/connections.rs` defines a full connector model:

```rust
pub struct ConnectionSet {
    pub variables: IndexSet<ConnectedVariable>,
    pub is_flow: bool,
    pub is_stream: bool,
}

pub struct ConnectedVariable {
    pub name: VarName,
    pub source_span: Span,
    pub is_inside: bool,                    // MLS §9.2 sign: +1 inside, -1 outside
    pub connector_type: Option<DefId>,
}
```

plus `ConnectionSets`, `ConnectionGraph`, `GraphNode`, `RootStatus`.

That is almost exactly the metadata Milestone 6 asks for — endpoints, spans,
flow-vs-potential, connector type identity, inside/outside sign.

**But these types are transient.** They appear only in
`rumoca-phase-flatten/src/vcg.rs` (virtual connection graph) and its
`errors.rs`. They are **not fields of `flat::Model`** — verified by absence:
the identifiers `ConnectionSets` / `ConnectionGraph` occur in
`rumoca-ir-flat/src/lib.rs` only in the re-export on line 66, never as a field
type. They are built during flattening, used to generate equations, and
dropped.

### What Flat *does* keep

Per-equation, in `flat::EquationOrigin` (`lib.rs:1260`):

```rust
Connection { lhs: String, rhs: String },
FlowSum { description: String },
UnconnectedFlow { variable: String },
ComponentEquation { component: String },
```

Model-level: `top_level_connectors: IndexSet<String>`, `branches`,
`potential_roots`, `definite_roots`, plus per-variable flags
(`used_in_connection`, expandable-connector).

So Flat retains *which two endpoints produced this equation*, but not the
connection-set grouping, not flow/stream classification, and not connector type
identity. And the endpoints are `String`, which SPEC_0001 prohibits as semantic
identity — any extension should carry `VarName`/`DefId`.

### Where the rest dies

One function, `crates/rumoca-phase-dae/src/construction.rs:1927`:

```rust
fn equation_generation(origin: &flat::EquationOrigin) -> Option<dae::DaeGeneration> {
    match origin {
        flat::EquationOrigin::ComponentEquation { .. } => None,
        flat::EquationOrigin::Connection { .. } => Some(dae::DaeGeneration::ConnectionEquation),
        flat::EquationOrigin::FlowSum { .. }
        | flat::EquationOrigin::UnconnectedFlow { .. } => Some(dae::DaeGeneration::FlowBalanceEquation),
        …
    }
}
```

The `{ .. }` patterns discard `lhs`, `rhs`, `description`, and `component`.
`DaeGeneration` is a fieldless enum, so all that reaches DAE is a tag plus a
span.

*(verified)* On `Circuit.Test`, of 20 continuous equations: 13 `source`, 3
`flow_balance_equation`, 4 `connection_equation`. All four connection equations
carry span `Circuit.mo[33:39]` = `Real v` — the connector *member declaration*
inside `Pin` — and all three flow balances carry `Circuit.mo[58:64]` =
`Real i`. Not the `connect(...)` statement. There is no way to recover
`connect(src.p, res.p)` from the DAE.

### What Milestone 6 therefore requires

Two changes, in order:

1. **Flatten must retain what it already computes.** Add a connection
   inventory to `flat::Model` — connection sets with their members, flow/stream
   classification, `is_inside`, connector-type `DefId`, and the span of the
   originating `connect(...)`. The data exists in `vcg.rs`; it is thrown away.
2. **DAE must carry it through.** Either give `DaeGeneration` payload variants
   or add a side table keyed by equation. Either touches the wire schema
   (33 → 34) and the round-trip property tests.

Neither is enormous, but this is real compiler work, not serialization work,
and it should be scheduled accordingly. A useful intermediate: RBC v1 can
expose connector information at whatever fidelity Flat currently offers, with
the schema shaped for the richer version so v1 → v2 is additive.

---

## 8. Source provenance into DAE

Rich, and better than needed. Covered in detail in
[`rumoca_notes.md`](rumoca_notes.md) §8; the essentials:

```rust
pub struct DaeProvenance { origin: DaeProvenanceOrigin, span: ProvenanceSpan }
pub enum DaeProvenanceOrigin { Source, Generated(DaeGeneration) }  // 24 generation kinds
```

Construction **refuses a dummy span** (`DaeProvenance::try_new` →
`MissingProvenance`). Every expression node, variable, equation, relation,
condition, root, event action and value type carries one. The `Dae` owns its
`SourceMap` (`Dae::source_map()` is `pub`), and
`rumoca_compile::compile::source_span_location(&map, span)` converts a span to
`{file_name, start: TextPosition, end}`.

*(verified)* on `SympyDecay.mo`: variable `x` → `19..25` = `Real x`; expression
`k*x` → `83..86`; residual → `73..86` = `der(x) = -k*x`.

Two traps for RBC:

- **A span is not a unique key.** `TwoPin`'s `v = p.v - n.v` at
  `Circuit.mo[142:155]` appears three times in `Circuit.Test`'s DAE — once per
  instance, because `extends` inlines it. RBC equation IDs must be independent
  of span.
- **`Span.source` is a hash-derived `SourceId`,** not a slot index — it is
  derived from the source *name*. Stable across invocations when file names
  match, which is what makes cross-version diffing (brief §25) feasible if RBC
  carries the file name rather than the raw hash.

---

## 9. One model traced through to Solve

Covered above and in `rumoca_notes.md`. The Solve-level point relevant to RBC:
names are gone, replaced by `Y[]`/`P[]` slot indices, recoverable only through
`layout.bindings` (`{"x": {"Y": {"index": 0}}}`). `program_spans` still carries
provenance. RBC should be a DAE-level artifact; anything Solve-level is a
different and lossier thing.

---

## Implications per milestone

| Milestone | Finding | Effect |
|---|---|---|
| 1 — spec | Internal wire is operation-shaped and private; template projection is curated and stable at v5 | Model RBC on operation-shaped records; use the template projection as a content checklist, not a format |
| 2 — export | Byte-identical determinism already tested for the internal wire | Reuse the "re-encode and compare bytes" property |
| 3 — import | Decode already runs `Dae::construct`; 70 invariants enforced; `Dae::construct` is public | Build `RBC → construction operations`, not a validator. **Much smaller than the brief assumes** |
| 4 — Python SDK | No blockers found | — |
| 5 — analyses | Dependency structure needs `rumoca-eval-dae`'s scalar coordinate projection at export time; `Incidence` omits parameters/inputs | Export edges computed by the compiler, do not make Python re-derive them from expressions |
| 6 — connector provenance | Set structure never reaches `flat::Model`; endpoints dropped at `construction.rs:1927` | **Real compiler work in two crates plus a wire-schema bump** |
| 7–8 — logging + execute | Trace points are observation metadata; the brief's "keep physical equations unchanged" matches how `[Trace]`-style sampling already works elsewhere | Represent trace points as a separate RBC section, not as equations |

## Open questions for Milestone 1

1. **Format.** The brief says evaluate protobuf first. Requirements met:
   explicit versions, cross-language, unknown-field tolerance, stable field
   identity, binary, Python tooling. Worth weighing against CBOR/FlatBuffers
   on one axis the brief cares about — `rumoca bitcode dump` readability — and
   one it does not yet mention: whether unknown-field *preservation* is needed
   so a v1 pass can round-trip a v2 file without destroying fields it does not
   understand. Protobuf preserves unknown fields; most alternatives do not.
   That single property may decide it.
2. **Does RBC carry expressions at v1?** Full expression trees are most of the
   bytes. Milestone 5's three passes (summary, dependency graph, connector
   graph) need none of them if dependency edges are exported directly.
   Connector logging needs none either. Deferring expressions to v2 would make
   v1 dramatically smaller and simpler — but transformation passes that rewrite
   equations need them, so this decides how soon §13's "modify expressions" is
   possible.
3. **Do RBC IDs need to be stable across compilations?** The brief requires
   uniqueness within one artifact (§10). Cross-artifact diffing (§25) needs
   more — a matcher keyed on `VarName` + role + type + unit, since DAE ids are
   allocation-ordered and spans are not unique.
