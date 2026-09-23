# TOOLBUG-012: exported connection ids had holes, so artifacts failed their own validator

| | |
|---|---|
| **Component** | Rumoca, `crates/rumoca-bitcode/src/export.rs` |
| **Severity** | High — the compiler wrote artifacts it could not read back |
| **Status** | Fixed, 2026-09-15 |

## What went wrong

```rust
flat_connections
    .into_iter()
    .enumerate()
    .filter_map(|(index, (lhs, rhs, span))| {
        let left = *by_name.get(lhs)?;          // drops the entry
        ...
        Some(RbcConnection { id: ConnectionId(index as u32), .. })
    })
```

The id came from the index of the **unfiltered** iteration. A connector
endpoint that is not a DAE variable — a clocked signal removed during lowering
— makes `by_name.get` return `None`, the entry is dropped, and the index has
already advanced. `SubSample` exported connections with ids `[0, 2]`.

`validate` requires `position == id`, so the artifact failed its own validator:

```console
$ rumoca compile ...SubSample --emit-bitcode a.rbc
$ rumoca bitcode check a.rbc
  - connections entry at position 1 declares id 2, expected 1
```

The compiler wrote a file it would refuse to load.

## Scale

**28 of 35** freshly compiled `Modelica.Clocked.*` models. Not limited to
Clocked: `Modelica.Electrical.Polyphase.Examples.Rectifier` failed the same way
at position 129, which had been dismissed earlier in this project as a v1
coverage gap. It was this.

## How it was found

By building the [textual IR](../bitcode-reading.md) and running
print → parse → encode over the corpus. `assemble` validates before writing, so
it refused these artifacts — and the first assumption was that the round-trip
was lossy. It was not: running `bitcode check` on the *original* showed the
input was already invalid.

Worth stating, because it is the argument for the round-trip sweep: 20
hand-picked artifacts round-tripped byte-identically and none of them had a
removed connector. The corpus found it on the first batch.

## Fix

Number after filtering. The original index is still used to pair a connection
with its DAE equation, because those are in unfiltered order — the two indices
are genuinely different things and the bug was conflating them.

```rust
    })
    .enumerate()
    .map(|(position, connection)| RbcConnection {
        id: ConnectionId(position as u32),
        ..connection
    })
    .collect()
```

## Regression

`crates/rumoca-bitcode/src/tests.rs::connection_ids_are_dense_after_filtering`
— a hole must be a validation error, and dense ids must validate.
