# The connection graph

Every other analysis in this project has one declaration or one equation as its
subject. That is why the physical rules needed component contracts bolted on: a
declaration in isolation does not say what the thing *is*.

A connector view changes the subject to the network. A component is a box with
ports; a port carries a potential and a flow; a node is where several ports
meet, equate their potentials and conserve their flows. Questions with no form
at declaration level have an obvious one here.

## What the artifact carries now

The bitcode had `connections` — pairwise endpoints — and only ever the
*potential* half. `Flow` and `Stream` were in the schema and never emitted, so
every consumer saw equalities and no conservation, which is the half that makes
an acausal model worth analysing as a network. See
[TOOLBUG-025](../toolbugs/TOOLBUG-025-the-conserved-half-was-never-exported.md).

`RbcConnectionSet` is the node:

```
connset 3 at "C1.n" at "C2.n" at "Gnd.p" at "Nr.n" at "Ro.n"
        pot %12 pot %59 pot %47 pot %40 pot %54
        balance eq 31 +%13 +%60 +%48 +%41 +%55 end
```

Three properties it has that the pairwise table did not:

**A node is n-ary.** `connect` is written in pairs and the object it creates is
not: Chua's ground joins five pins, sharing one potential and one conservation
law. The pairs are closed transitively into sets.

**A node may conserve more than one thing.** A MultiBody frame conserves a
force *and* a torque — separate sums, separate equations, the same node. They
are kept as separate `balances`, and a check that merged them reported every
frame in the corpus as a force-versus-torque unit mismatch.

**A component knows its class.** `RbcComponent` carried a path and nothing
else, so the graph could say a node joins `L.n` to `Ro.p` and not that it joins
an inductor to a resistor.

## What crosses a port

`potential * flow` is power in some domains and not others, so the rule is
looked up and the answer is `UNKNOWN` where none applies:

| domain | form | power |
|---|---|---|
| electrical | product | `v * i` |
| translational | rate product | `der(s) * f` |
| rotational | rate product | `der(phi) * tau` |
| thermal | flow is power | `Q_flow` |
| fluid | unknown | needs the medium's enthalpy |
| magnetic | unknown | `V_m * Phi` is not a power |

A component with one unknown term has no usable balance and says so: a missing
term can be any size, so a negative sum over the rest proves nothing.

Across the corpus, **5,630 components have a complete power expression** —
13,246 products, 2,476 flows that are already powers, 2,343 rate products — and
290 do not, almost all fluid.

That matters because a passive component's power balance is checkable *without
a contract saying it is passive in a particular way*. It is the definition of
passivity, and unlike a sign rule on a declaration it needs no statement of
intent.

## Instrumentation

A connector observation is a pair, tagged with the node it belongs to.
Observing both members and not knowing which node they share answers every part
of the request except the question, so `OBSERVE_CONNECTOR` is a separate
capability from `OBSERVE_VARIABLE`, and `CONNECTION_GRAPH` is a separate static
one from `CANONICAL_MODEL` — an artifact written before the exporter emitted
sets has one and not the other, and a network pass must report itself skipped
rather than clean.

`RbcTracePoint` has carried a `connection` field since the schema was written,
commented *"when it came from connector instrumentation"*. It now has a
`connection_set` beside it, because an edge and a node are different things and
a conservation law lives at the node.

```python
from modelsan.network import build
from modelsan.instrumentation import connector

network = build(model)
connector.requests(network)      # what to observe, in the planner's vocabulary
connector.instrument(model)      # write the trace points into the artifact
model.save("instrumented.rbc")   # validates under `rumoca bitcode check --strict`
```

Idempotent, and the artifact round-trips through the textual IR unchanged.

## What NetworkSan reports

| kind | claim | severity |
|---|---|---|
| `network-balance-quantity-mismatch` | one conservation law sums two quantities | high |
| `network-boundary-port` | a connector of the model itself, open on one side | low, not a defect |
| `network-port-unconnected` | nothing attached; MLS §9.2 forces the flow to zero | low, not a defect |
| `network-component-isolated` | every port of an instance is unconnected | low, not a defect |

Runtime, requiring `OBSERVE_CONNECTOR`:

| kind | claim |
|---|---|
| `network-conservation-violated` | the node's signed flow sum is not zero in the observed trajectory |
| `network-passive-component-sources-power` | a component a contract establishes as passive delivered energy on net |

The second keeps the premise discipline of the
[intent policy](physical-intent-policy.md): `passive` is a statement about a
component, only a contract supplies it, and a source is *supposed* to source
power.

## The corpus

312 of the 333 analysable models have a connection graph; 21 have no `connect`
at all. **3,955 nodes and 17,740 ports**: 3,153 acausal, 666 signal, 136
unconnected.

### It corrected a claim this project had been making

`RESULTS.md` and the paper said the structural findings were explained by
sub-circuits compiled standalone, whose *unconnected connectors* contribute a
`flow = 0` without a matching unknown. Measured directly against the graph,
only **4** of the 24 models with structural findings have an unconnected
connector.

The mechanism is a **boundary port**, which is a different thing. A sub-circuit
keeps its own interface pins; they are wired to its internals and open on the
other side. Nothing forces their flow — MLS §9.2 forces only a connector with
nothing attached — so the node is a half-node and a structural matching reports
an unmatched unknown without being able to say why.

| | models |
|---|---:|
| structural findings explained by a boundary port | **20** |
| explained by an unconnected connector | **4** |
| unexplained | **0** |

The conclusion the project drew was right and the reason it gave was wrong, and
the difference was invisible until the graph existed to measure it.
