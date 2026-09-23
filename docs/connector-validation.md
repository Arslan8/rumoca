# Native connection-contract validation

The public scalar connector profile now checks connection semantics at the
**native artifact boundary**, not just in Python's `add_connection_set` helper.
Checks apply to raw JSON/CBOR edits as well as SDK-authored artifacts.

```bash
rumoca bitcode check combined.rbc --strict --connections
```

```python
combined.validate(connections=True)
```

`--connections` requires complete port declarations. Plain `check`, import,
link, execution lowering and saved-program validation already enforce the laws
whenever explicit connector declarations exist. The flag additionally refuses
legacy graph annotations that lack those declarations. Ordinary checking prints
`connection laws NOT certified` for those legacy artifacts; it does not upgrade
them into a verified wiring interface.

## Root cause and reproduction

Previously Rust checked member references, ownership, scalar types and units,
but did not compare a connection set's metadata with its actual equations.
Replacing a thermal port's flow-balance residual with literal `0.0` therefore
passed `rumoca bitcode check --strict`: every referenced object still existed.
The Python helper's type/overlap checks were bypassable by editing the file.

`new_inst/test_connection_validation.py::test_flow_law_cannot_be_replaced_by_zero`
was run before the fix and failed because the native command incorrectly
accepted the mutated model. The fix is in `rumoca-bitcode`'s connector validator,
the first native consumer boundary. The DAE validator and numerical solver have
not been weakened or taught to repair a broken connection.

The contract follows SPEC_0022 CONN-001/002/003/005/008/026 and MLS §9.2:
compatible primitive members, equality of corresponding potentials, and signed
flow conservation. Public port orientation uses the existing
`positive_into_owner` convention; reversing the entire residual's sign does
not change its zero set.

## Enforced invariants

| Area | Rejected problems |
|---|---|
| Declarations | Missing owners/types/variables/provenance; duplicate paths or member ownership; unsupported stream/array/non-Real members; declaration/member disagreement in names, roles, units or quantities |
| Set membership | Empty sets, repeated ports, overlapping finalized sets, unknown port paths, wrong singleton or connected flags |
| Compatibility | Different ordered member names, scalar types, potential/flow roles, units, quantities or flow conventions; module-local type IDs may differ |
| Potential equations | Missing/extra equations or members; cross-field equalities; unrelated, constant or otherwise invalid residuals; a duplicate/cyclic edge set that fails to connect every port |
| Flow equations | Missing/extra balances or members; duplicate members/field balances; incorrect orientation signs; absent equation references; residuals that do not implement the declared signed sum |
| Equation ownership | One equation claimed more than once; contradictory optional edge metadata; leftover generated connection/boundary equations after deleting their set |
| Hostile expressions | Cyclic/non-topological expression graphs, dangling references, coefficient overflow or proof-budget exhaustion; clean refusal instead of recursion/panic |

The supported connector profile is deliberately narrower than all Modelica
connector semantics. It requires exact unit/quantity strings and ordered field
contracts; it does not infer unit conversion, stream behavior, expandable or
overconstrained connectors, or causal signal connections.

## Equation proof, not a numeric spot check

The checker constructs exact integer coefficient maps for the referenced
connection equations. Supported syntax consists of scalar Real state/algebraic
coordinates, literal real zero, addition, subtraction and unary negation.
Potential equalities must form a spanning tree separately for each field. Each
flow law must have exactly the declared members and orientation signs.

It accepts reordered terms, different valid potential spanning trees, and
global sign reversal. It does not evaluate a sample state or assume that a
parameter-dependent multiplier is nonzero. Multiplication, division, function
calls and other unsupported rewrites of connection equations fail closed—even
if a human could prove a particular rewrite equivalent. Use the canonical
connection equations or extend the proof profile with regressions.

Proof limits are 100,000 reachable expression nodes, 4,096 nonzero coefficients
per expression and 1,000,000 stored coefficient entries. These are explicit
resource limits, not physics judgments. Unrelated constitutive equations are
not required to fit this additive syntax.

## Transactional SDK wiring

`add_connection_set` builds a detached candidate, invokes the native checker
with complete-contract checking enabled, and commits the candidate only on
success. Rejected metadata, unavailable native tools or failed equation proofs
leave equations, connected flags, summaries and builder counters unchanged.
Negative, Boolean and out-of-range IDs are rejected before Python indexing.

Generated potential and flow equations now carry their appropriate provenance
kinds. A singleton connection set explicitly closes a port with zero flow;
attempting to reuse it in another set is rejected. Deleting the set while
leaving its generated equation behind is also rejected. Existing saved
execution programs are not silently relowered: equation edits leave them stale.

## What this does not prove

This verifies **the declared interface contract and its connection equations**,
not the physical correctness or solvability of every other equation in a model.
An arbitrary unannotated user equation can impose a boundary or contradict
another equation; identifying all such constraints requires whole-model
analysis. The checker does not guess that intent or delete constraints.

Legacy exported graph provenance may lack complete port declarations or exact
equation pairing. It remains available for inspection and independent linking,
but fails complete-contract checking and cannot be passed to the SDK wiring
helper as an open declared port. Mixing legacy graph data into an artifact that
claims complete scalar port declarations also fails when coverage is missing.
To compose such a component, author/export an explicit interface and handle its
boundary equations explicitly. This is not a trusted-signature system: deleting
all interface information does not leave enough information to certify it.

## Regressions

```bash
PYTHONPATH=packages/rumoca-bitcode:new_inst RUMOCA="$PWD/target/debug/rumoca" \
  python3 -m unittest discover -s new_inst -p 'test_*.py' -v
```

Adversarial tests mutate files without calling the connection helper and check
native `check`, `check --strict`, `compile-bitcode`, `lower-execution` and `link`
in both JSON and CBOR. Positive tests cover singleton boundaries, mixed
orientation, multiway/multifield sets, reordered/global-sign-equivalent laws,
alternative spanning trees and linked thermal systems. Negative tests cover
metadata/law mismatches, cyclic graphs, unsupported expressions, integer
overflow, atomic rollback and missing legacy contracts.

See [the verification record](../new_inst/LINK_VERIFICATION.md) for actual runs
and unresolved broader validation gates.
