# What blocks the corpus, measured

The binding constraint on ModelSan is not detector strength — it is that 515 of
847 models never reach a detector. This is that number broken down, by
re-running every failure and capturing the full diagnostic
(`tools/sweep/why.tsv`).

It is recorded here, in toolbugs, because none of it is a defect in any model.

| Blocker | Models | Tractability |
|---|---|---|
| `function value type` — MLS §12.9 **external objects** (`ExternalCombiTimeTable`) | 86 | Large. Needs C interop at runtime. |
| `Medium.BaseProperties` cannot instantiate partial class | 30 | Large. Fluid media. |
| `ED008`/`EF023` unresolved `v`, `v.re` | ~30 | [BUG-004](BUG-004-record-array-destructured-without-subscript.md). Contained but needs a `Reference` mutation API. |
| `impure call context` | 12 | Unassessed |
| `EF025` missing function-selection identity | 8 | Unassessed |
| `ED001` unbalanced model | 55 | Unassessed; OMC accepts many of these |
| `EF004` if-equation branch mismatch | 6 | Unassessed |

## Why this list changed the plan rather than the backlog

External objects and Fluid media are months of compiler work. Chasing them to
reach "full coverage" through Rumoca is the wrong plan, because coverage does
not have to be a property of one front end — see
[the method note](../method/README.md). Running the dynamic search through
OpenModelica reaches ~93% of the corpus today.

Rumoca coverage still matters, because it is what supplies incidence analysis
and the second opinion for cross-confirmation. It is no longer the ceiling.

## One attempt, abandoned deliberately

BUG-004 looked like the best target: ~30 models, already diagnosed. The first
fix was wrong. I assumed the destructured argument was a `FieldAccess` node and
made `insert_record_array_full_slice` recurse into call arguments. It is
actually a `VarRef` already named `v.re`, with the record-array part carrying no
subscript, so the change was inert. A correct fix needs to rebuild the reference
as `v[:].re`, and `Reference`'s parts are private with no mutation API.

Reverted rather than left in the tree. Recorded so the next attempt starts from
the right node type.
