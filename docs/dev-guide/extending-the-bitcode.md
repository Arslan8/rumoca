# Extending the bitcode

> **Fixtures are built, not spelled out.** `rumoca_bitcode::build::Builder`
> (Rust) and `rumoca_bitcode.Builder` (Python) fill a new field with its
> default, so adding one is a schema change and no longer a fixture change.
> Hand-written `RbcModel { .. }` literals were repaired four times in one week
> before the builders existed; if you find one, migrate it rather than
> repairing it.

A new field has to reach **seven** places. It was five when the format was
written; every addition since has been made by editing `schema.rs` and
following compiler errors, which finds six of the seven. The one it does not
find is the text parser: a field that is printed and not parsed compiles, round
-trips every model that does not have one, and fails the day somebody compiles
a model that does.

## The seven

| # | Place | What breaks if you skip it |
|---|---|---|
| 1 | `crates/rumoca-bitcode/src/schema.rs` | — |
| 2 | `export.rs` | the field is never populated; consumers see a default and cannot tell it from a real one |
| 3 | `import.rs` | reconstruction drops it, and `bitcode round-trip` fails |
| 4 | `text.rs` — printer | `emit-text` silently omits it |
| 5 | `text.rs` — parser | **compiles, and loses the field on assemble.** The one the compiler cannot find for you |
| 6 | `validate.rs` | a dangling id reaches reconstruction instead of being rejected at the door |
| 7 | `packages/rumoca-bitcode/` | the Python SDK cannot see it, so no analysis can |

Then: `tools/bitcode/gen_reference.py` to refresh the reference, and a doc
comment on the field, because the reference is generated from those.

## Compatibility

State it in the serde attributes, and the generated reference will report it:

```rust
#[serde(default, skip_serializing_if = "Option::is_none")]
pub class_name: Option<String>,
```

- **additive** — `Option` or `#[serde(default)]`. An artifact written before
  the field existed still loads. This is almost always what you want; every
  field added to v1 so far is additive.
- **required** — a plain field. Adding one is a version break: old artifacts
  fail to deserialize, and `RBC_VERSION` must go up.

A count added to `RbcSummary` is additive on the wire and still needs
`validate.rs` to check it, or the summary and the tables can disagree without
anything noticing.

## Checking the work

```sh
cargo test -p rumoca-bitcode                     # schema, text, validation, builder
tools/bitcode/gen_reference.py --check           # the reference is current
tools/bitcode/coverage.py --limit 200            # a model actually produces it
python3 tools/sweep/roundtrip_audit.py           # and it survives a round trip
```

`coverage.py` is the one that answers the question the others cannot: *does
any model in the corpus produce this construct at all?* An export path nothing
exercises and a broken one look identical. If your new field shows `GAP`,
either the corpus has no model with that construct — in which case add a test
and an entry to `NOT_EXPORTED` saying which test covers it — or it is not
being exported and you have found the bug early.

## Things the format will not accept

Before adding a construct, check it against
[§9a Computational power](../SPEC_RUMOCA_BITCODE.md#9a-computational-power).
The IR is deliberately total: no loops, no recursion, no cyclic references.
A construct that introduces unbounded iteration does not just add a feature —
it invalidates the termination argument every static analysis relies on, and
`cost_of_node` in `crates/rumoca-bitcode/src/tests.rs` will refuse to compile
until somebody classifies it and faces that.
