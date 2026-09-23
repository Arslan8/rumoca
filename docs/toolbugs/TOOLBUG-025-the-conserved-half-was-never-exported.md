# TOOLBUG-025: the conserved half of every connection was never exported

| | |
|---|---|
| **Component** | `rumoca-bitcode::export`, `rumoca-ir-flat::EquationOrigin` |
| **Severity** | High — it made a whole class of analysis impossible, silently |
| **Found by** | Designing the connector analysis, 2026-09-22 |
| **Status** | Fixed. `RbcConnectionSet` carries both halves; 18 cases in `tests/test_network.py`. |

## The defect

A Modelica `connect` asserts two things: the potentials are equal, and the
flows sum to zero. The artifact carried the first and never the second.

`RbcQuantityKind` has had `Flow` and `Stream` since the schema was written. I
checked four models across four domains — Chua, `Rotational.First`,
`SimpleCooling`, `FreeBody` — and every exported connection was `Potential`.
Not most. All of them.

The flow balances were in the flattened model the whole time, as
`EquationOrigin::FlowSum`, and the exporter did not look at them. They reach
the DAE as anonymous residuals like `0 - (L.p.i + L.n.i)`, with nothing tying
them back to the connection they came from.

## Why it was invisible

Nothing failed. `bitcode check --strict` passed, every round-trip held, and
the connections that *were* exported were correct. A consumer reading
`model.connections` got a well-formed graph of equalities and had no way to
know that the conservation half existed and was missing — which is the half
that makes an acausal model worth analysing as a network rather than as a pile
of equations.

This is the same shape as
[TOOLBUG-014](TOOLBUG-014-structured-equations-not-exported.md) and
[TOOLBUG-016](TOOLBUG-016-incidence-edges-lost-and-invented.md): the artifact
was consistent with itself and short of the model.

## The fix

`RbcConnectionSet` — the node, not the edge — with the connectors that meet
there, the potentials equated, and the conservation laws asserted:

```
connset 3 at "C1.n" at "C2.n" at "Gnd.p" at "Nr.n" at "Ro.n"
        pot %12 pot %59 pot %47 pot %40 pot %54
        balance eq 31 +%13 +%60 +%48 +%41 +%55 end
```

Three things it had to get right, each found by building it:

**A node is n-ary.** `connect` is pairwise; the object is not. Chua's ground
joins five pins and the pairs close transitively into one set.

**A node may conserve several things.** A MultiBody frame conserves a force and
a torque: separate sums, separate equations, one node. The first version
emitted one set per balance, which made one frame node look like four; the
second merged them and then a quantity check reported every frame in the corpus
as a force-versus-torque unit mismatch. The node holds a list of `balances`,
and the check's subject is the balance.

**`FlowSum` carried a rendered string.** `description: "-a.i + b.i = 0"` and
nothing structured, so the endpoints could only be recovered by parsing
formatted text — which the repository's own architecture test forbids, for
good reason. It now carries `members: Vec<FlowMember>` with the sign on each.
Name simplification had also been skipping that description, so it could hold
variable names the model no longer had; the members are remapped and the
description rebuilt from them.

`RbcComponent` gained a `class_name` at the same time: the graph could say a
node joins `L.n` to `Ro.p` and not that it joins an inductor to a resistor,
which is most of what a connection graph is for.

## Effect

312 of 333 analysable models now expose a graph: **3,955 nodes, 17,740 ports**,
3,153 of the nodes carrying a conservation law. **5,630 components have a
complete power expression** computable from their ports alone.

It also corrected a claim this project had been publishing. `RESULTS.md` and
the paper explained the structural findings as sub-circuits compiled standalone
whose *unconnected connectors* leave a `flow = 0` without a matching unknown.
Measured against the graph, only 4 of the 24 models involved have an
unconnected connector; 20 have a **boundary port** — an interface pin of the
model itself, wired inside and open on the other side, which nothing forces.
Zero are unexplained. The conclusion was right, the mechanism named for it was
wrong, and no measurement could tell the difference until the graph existed.
