# Rumoca Bitcode v1

**Status:** implemented, v1.
**Scope:** the public interchange format for a compiled Modelica model.

Rumoca Bitcode (`.rbc`) is a versioned, machine-readable representation of a
compiled Modelica model, intended for analysis and transformation by tools
outside the Rumoca source tree.

A tool that reads or writes `.rbc` needs no Rumoca checkout, no Rust, no
matching compiler version, and no linkage against Rumoca's crates. **The file
format is the interface.**

---

## 1. What this is not

Bitcode is deliberately **not** Rumoca's internal DAE serialization.

| | internal wire | Rumoca Bitcode |
|---|---|---|
| Produced by | `Serialize for Dae` (`--emit dae-json`) | `rumoca-bitcode::export` |
| Version | `DAE_SCHEMA_VERSION`, currently 33 | `RBC_VERSION`, currently 1 |
| Compatibility | single version only; SPEC_0033 requires the old reader be deleted on every change | versioned public contract |
| Audience | the compiler | external tools |
| Stability | changes freely | changes only when the public contract changes |

This separation is the point. Rumoca may reorganise its Rust structs, rename
internal types, renumber internal ids, or restructure its crates without
touching `RBC_VERSION`. Conversely, a bitcode version change is a statement
about the public contract, not about compiler internals.

The two must not be conflated: publishing the internal schema would freeze
Rumoca's representation and create a plugin-versus-compiler upgrade deadlock.

## 2. Container

```
RbcFile
  magic            "RUMOCA-RBC"
  bitcode_version  1
  producer         e.g. "rumoca 0.10.0"   (informational only)
  model            RbcModel
```

A reader **must** reject a file whose `magic` differs, and **must** reject a
`bitcode_version` it does not implement. Both checks happen before any other
field is interpreted.

`producer` is informational. A consumer must not change behaviour based on it.

## 3. Encodings

The same schema is carried by two encodings:

| Encoding | Use | Detection |
|---|---|---|
| **CBOR** | production, default | any first non-whitespace byte other than `{` |
| **JSON** | debugging, diffing, hand-editing | first non-whitespace byte is `{` |

Encoding is detected on read, so a consumer is never told which it was handed.
`rumoca bitcode convert` moves between them; `rumoca bitcode dump` prints any
artifact as JSON.

CBOR is map-keyed and self-describing, so a field a reader does not recognise
is skipped rather than shifting every field after it. This is a deliberate
contrast with an ordinal-tagged codec, where inserting an enum variant silently
changes how older payloads decode — a class of bug Rumoca's own wire tests
exist to catch.

## 4. Versioning

`RBC_VERSION` is the public contract version. It is independent of every
internal schema.

**Compatible** (no version bump):
- adding an optional field
- adding a new enum variant with an explicit `kind` tag
- adding a new collection

**Incompatible** (bump `RBC_VERSION`):
- removing a field
- renaming a `kind` tag
- changing a field's meaning

Every enum is externally tagged by an explicit `kind` string, never by
declaration order, so appending or reordering variants in the producer cannot
change how an existing file decodes.

v1 implements exactly one version. Migration infrastructure is deliberately
absent until a v2 exists; the design constraint it must satisfy is that a
breaking *internal* Rust change never forces a bitcode version change.

## 5. Identity

Every object carries an explicit `id` field. IDs are dense and ordered within
each collection, but a consumer reads the `id` rather than assuming array
position is identity.

| Property | Guarantee |
|---|---|
| Unique within one artifact | **yes** |
| Stable across two compilations of the same source | **no** |
| Stable across compiler versions | **no** |
| Derived from a rendered name | **never** |

Expressions reference variables through typed *coordinates*
(`state`, `derivative`, `parameter`, `pre_state`, …), never by string. A pass
must not parse pretty-printed names to recover identity.

For cross-artifact comparison — diffing two versions of a model — match on
`name` + `role` + `type` + `unit`, not on ids. Two independent compilations
allocate ids independently.

## 6. Provenance

Every variable, expression, equation, relation, condition, root, event and
connection carries:

```
provenance
  origin   "source" | { "generated", generation }
  span     { source, start, end, line, column }
```

`line` and `column` are 1-based and precomputed at export time, so a pass can
report `Motor.mo:52` without the source text. `start`/`end` are byte offsets
and are authoritative.

`generation` names the lowering kind for generated objects —
`connection_equation`, `flow_balance_equation`, `binding_equation`,
`index_reduction`, and so on — so a consumer distinguishes them without
guessing from shape.

**A span is not a unique key.** An equation inherited through `extends` appears
once per instance with the same span. Use `id` for identity and provenance for
explanation.

Sources may embed their full text (`--emit-bitcode` does by default), which
makes the artifact self-contained and lets a pass print the exact source of any
object.

## 7. Model contents

```
RbcModel
  name                model name as compiled
  sources[]           files, optionally with text
  types[]             scalar kind + array dimensions
  variables[]         every variable, in every role
  expressions[]       flat arena, topologically ordered
  equations[]         continuous residuals: residual == 0
  initial_equations[] initialization residuals
  relations[]         primitive comparisons that can generate events
  conditions[]        boolean activation algebra
  roots[]             zero-crossing surfaces
  events[]            reinitialize / assert / terminate
  time_events[]       scheduled events
  components[]        component instances
  connections[]       connector-level provenance
  trace_points[]      observation requests (added by passes)
  summary             denormalised counts
```

### Variables

Carry `role` (the Appendix B partition: state, parameter, constant, input,
algebraic, output, discrete real, discrete value) and `causality` (the
interface annotation) **separately**, because they are orthogonal. Also carry
type, scalar count, unit, description, `start`/`binding`/`min`/`max`/`nominal`
expressions, `fixed`, `tunable`, and connector semantics when the variable is a
connector member.

### Expressions

A flat arena in topological order: **every operand references a strictly lower
`ExprId`**. This makes the arena a DAG by construction, lets a consumer build
the tree in one forward pass, and makes a cycle unrepresentable rather than
something to detect.

v1 represents literals, coordinates, unary and binary operators, and
conditionals. Anything else is recorded as `unsupported` with a detail string.
A consumer that requires completeness must treat an `unsupported` node as "this
artifact does not fully describe the model", never as a default value.

### Equations

Residual form: the model asserts `residual == 0`. Each equation carries
`reads` and `reads_derivative` — the variables it depends on, computed by the
compiler's own dependency projection, which resolves function calls and runtime
array selection correctly. **A consumer should use these rather than walking
the expression tree**, which would produce a weaker answer.

### Connections

A connection is an equality between two connector endpoints plus the
conservation law over the flow members of its connection set. It is **not** a
directional message: `left` and `right` are symmetric.

`quantity` is `potential` (equated across the connection),
`flow` (signed sum is zero) or `stream`. Preserving this distinction is the
reason connections are modelled at all rather than left as raw equations.

### Trace points

Observation requests: a variable, a label, optionally the connection and
physical quantity it belongs to, and the tool that added it.

Trace points are **observation metadata, deliberately separate from the
physical equations**. Adding one cannot change what the model computes, which
is why instrumentation does not require a pass to rewrite equations. A
transformation pass that genuinely needs to change behaviour edits equations
instead; trace points are the narrow, safe path for the common case.

### Trace output

`--simulate --trace-out FILE` writes one row per trace point per output time:

```
time,trace_id,connection,variable,quantity,unit,value
0.1,1,inertia.b <-> spring.a,inertia.b.tau,flow,N.m,4.272051
0.1,2,inertia.b <-> spring.a,spring.a.tau,flow,N.m,-4.272051
```

The structured form is the contract; the table `--simulate` prints without
`--trace-out` is one presentation of it. A trace point naming a variable the
solver does not report is warned about, never silently dropped.

### Summary

Denormalised counts. A reader checks them against the actual collections, so a
truncated or carelessly hand-edited artifact fails loudly. A pass that edits a
model must recompute the summary before writing; the Python SDK's `save()` does
this automatically.

## 8. Validation

An artifact that has been through an external pass is **untrusted**. Import
runs two gates:

```
.rbc
  ↓ decode          rejects malformed bytes, foreign magic, unknown version
  ↓ validate        references, dense ids, duplicate names, topological order,
  ↓                 summary agreement, unsupported nodes
  ↓ construct       the DAE's own checked constructors
checked DAE
```

The second gate is the important one. Import does not fill in structs; it
issues the same checked construction operations the compiler uses when
compiling from source. All 70 of the DAE's construction invariants therefore
apply to imported bitcode exactly as they apply to a freshly compiled model.

**An invalid external pass cannot produce an invalid DAE — only a rejection.**

Validation returns *every* problem it finds, not the first, so a pass author
fixes one round of errors rather than playing whack-a-mole.

## 9. Command-line interface

```bash
# export
rumoca compile Model.mo --model Model --emit-bitcode model.rbc
rumoca compile Model.mo --model Model --emit-bitcode model.json --bitcode-format json

# examine
rumoca bitcode inspect model.rbc
rumoca bitcode dump model.rbc                 # JSON, whatever the on-disk encoding
rumoca bitcode check model.rbc                # validate without rebuilding
rumoca bitcode convert model.rbc -o model.json --format json   # lossless
rumoca bitcode round-trip model.rbc           # prove import/export fidelity

# import
rumoca compile-bitcode model.rbc --summary

# import, simulate, and emit the trace points an external pass requested
rumoca compile-bitcode model-traced.rbc --simulate --t-end 1.0
rumoca compile-bitcode model-traced.rbc --simulate --t-end 1.0 --trace-out traces.csv
```

A full external transformation:

```bash
rumoca compile Motor.mo --model Motor --emit-bitcode motor.rbc
python connector_logger.py motor.rbc -o motor-traced.rbc
rumoca compile-bitcode motor-traced.rbc --simulate --t-end 1.0 --trace-out traces.csv
```

## 10. Known limits of v1

Stated plainly, because a format that hides its gaps is worse than one that
names them.

| Limit | Effect | Path |
|---|---|---|
| Expressions cover literals, coordinates, unary, binary, conditional | Other forms export as `unsupported`; import refuses them | extend `RbcExprNode` |
| No function definitions or calls | Models with functions do not round-trip | v2 |
| No arrays beyond type dimensions; no records or enumerations as structured types | Records collapse to a scalar kind | v2 |
| No clocks or synchronous features | Clocked conditions refuse on import | v2 |
| Type aliases collapse on import | `Voltage` and `Current` both become `Real`; structure is preserved, alias identity is not | carry alias names in `RbcType` |
| Connection-set grouping beyond two members, inside/outside sign, connector-type `DefId` | A three-way connection reports as pairs | retain a connection inventory on `flat::Model` |
| `--target` from bitcode covers `ir = "dae"` only | `dae-modelica` and custom DAE targets render. FMI packaging needs the artifact session the `compile` path owns; Flat/AST/Algorithm-Code targets need artifacts bitcode does not carry. | thread `Option<&CompilationResult>` through `ManifestRenderer::render` and the packaging functions |

## 10a. Forward compatibility

`dump` and `convert` operate on the raw document, so a field written by a newer
producer survives both. This is deliberate: changing how an artifact is
*stored* must not change what it *contains*.

The typed path is the contrast. `import` rebuilds only what it understands, and
the Python SDK preserves the whole document because it never round-trips
through a typed schema. So a v1 pass can load, edit and re-save a v2 artifact
without destroying the parts it does not know.

The one thing that does not survive is a v1 *reader* meeting a v2 enum variant
it cannot interpret: it is refused, not guessed. Adding a variant is a
compatible change for the format and a hard stop for an older reader, which is
the honest trade.

## 11. Connector provenance: what was recovered, and what was not

The DAE retains **no** connector structure. Of the original `connect(...)`, only
a `connection_equation` / `flow_balance_equation` tag survives, anchored to the
connector member declaration.

v1 recovers connections at export time by joining the DAE with the Flat model,
which retains per-equation `EquationOrigin::Connection { lhs, rhs }` and
per-variable `flow` / `stream` / `connected` flags. That is enough for
endpoints, flow-versus-potential classification, connector membership, and
component grouping — enough for the connector-logging application.

Connection spans now point at the `connect(...)` statement. That required one
fix in the compiler: `build_connection_sets` recorded the connect span only for
*direct* endpoints, so a connector-level `connect(a.p, b.p)` left its expanded
members (`a.p.v`, `a.p.i`) to fall back to their own declaration — the connector
*type*. Recording the span for each expanded member closes it, and the struct's
own doc comment already said this was the intent.

What is still lost: the connection-set grouping for sets with more than two
members, the inside/outside sign, and the connector type's `DefId`.
`ConnectionSet` and `ConnectionGraph` exist in `rumoca-ir-flat` but are built
and discarded inside `rumoca-phase-flatten/src/vcg.rs`; they are not fields of
`flat::Model`. The schema is already shaped for the richer data, so v1 → v2
would be additive.
