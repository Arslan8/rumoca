# BUG-008: bitcode export degraded enumeration values to integers, so import rejected its own output

| | |
|---|---|
| **Severity** | High — broke the format's central guarantee on real models |
| **Component** | `rumoca-bitcode` (`export.rs`, `import.rs`, `schema.rs`) |
| **Found by** | Trying to test BUG-006 against the real MSL model rather than an isolated shape, 2026-09-13 |
| **Status** | **Fixed**, with regression tests |

## Summary

`RbcLiteral` had four variants — `Real`, `Integer`, `Boolean`, `String` — and no
enumeration. Export mapped enumerations onto `Integer`:

```rust
// export.rs:504, before
dae::DaeLiteral::Enumeration(ordinal) => RbcLiteral::Integer { value: *ordinal },
```

The DAE's own literal type does distinguish them (`DaeLiteral::Enumeration(i64)`
next to `Integer(i64)`), and reconstruction type-checks. So a model containing
any enumeration exported *successfully* and then failed to come back:

```console
$ rumoca compile .../OpAmpCircuits/Der.mo --model ...Der --emit-bitcode der.rbc
$ rumoca compile-bitcode der.rbc --simulate
cannot rebuild a checked DAE from this bitcode:
  expression type mismatch: expected Enumeration, found Integer
```

Export and import disagreeing is the one failure an interchange format cannot
have. Every external pass reading such an artifact sees an `Integer` where the
model has an enumeration, and anything it writes back is unloadable.

## How it was found

Not by the test suite — the 23 tests built `RbcModel` values directly and
checked validation and the codec, none of which involves the DAE's type
checker. It surfaced only when BUG-006 was checked against the actual MSL model
instead of an isolated reproducer, and that model happened to carry
`opAmp.homotopyType`, an enumeration parameter.

That is the general lesson: schema-level tests could not see this, because the
defect was in the *agreement* between two mappings, not in either one alone.

## Second defect, uncovered by fixing the first

Adding `RbcLiteral::Enumeration { ordinal }` and mapping it to
`DaeLiteral::Enumeration` moved the failure rather than removing it:

```
cannot rebuild a checked DAE from this bitcode:
  invalid one-based enumeration ordinal 0
```

The artifact's ordinals were 1–4; none was 0. The DAE has two constructors, and
the general one refuses enumerations with a hardcoded placeholder in the error:

```rust
// rumoca-ir-dae/src/expression/leaf_nodes.rs:4
pub fn literal(self, value: DaeLiteral) -> Result<ExprId<'dae>, DaeConstructionError> {
    if matches!(value, DaeLiteral::Enumeration(_)) {
        return Err(DaeConstructionError::InvalidEnumerationOrdinal {
            ordinal: 0,                      // <- not the real ordinal
            ...
```

`enumeration_literal(ordinal)` is the correct entry point; it proves the ordinal
one-based (MLS §4.9.5) before interning. Import was calling `literal` for every
literal kind.

**Worth noting separately:** that error reports `ordinal: 0` for *any*
enumeration reaching `literal`, which is actively misleading — it sent this
investigation looking for a zero in the artifact that was never there. The
placeholder should be the real ordinal, or the variant should say "enumeration
literals must use `enumeration_literal`".

## The fix

1. `schema.rs` — a real `RbcLiteral::Enumeration { ordinal: i64 }` variant.
2. `export.rs` — map `DaeLiteral::Enumeration` to it instead of to `Integer`.
3. `import.rs` — route it to `enumeration_literal`, not `literal`. The
   `literal_of` arm is kept so any future caller fails closed on a typed
   `InvalidEnumerationOrdinal` rather than panicking.
4. `bitcode_cli.rs` — `--param`'s numeric view reads enumeration ordinals too.

Verified on the model that exposed it: `OpAmpCircuits.Der` now round-trips.
(It is then reported structurally singular, which is a separate and correct
finding — neither Rumoca nor OMC can simulate that fragment standalone.)

## Regression tests

Two, in `crates/rumoca-bitcode/src/tests.rs`:

- `enumeration_literal_keeps_its_type_through_the_codec` — an enumeration
  literal survives CBOR and JSON as an enumeration, not an integer.
- `enumeration_ordinal_is_carried_verbatim_for_reconstruction_to_judge` — a
  zero ordinal is transported unchanged, so reconstruction rejects it with a
  span rather than the codec silently repairing it.

Suite: 25 passing, was 23.

## What this says about the round-trip claim

The earlier statement that bitcode "round-trips on all test models" was true and
insufficient: the test models contained no enumerations. Round-trip fidelity has
to be asserted per *construct*, not per model, and the corpus sweep is what
supplies constructs no hand-written fixture will.
