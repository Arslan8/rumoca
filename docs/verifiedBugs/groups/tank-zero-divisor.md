# Tank permits a direct zero divisor

Group `tank-zero-divisor` · 2 report instances · confirmed

The local model declares resistance with no strictly-positive enforcement that excludes zero and evaluates flow_out=level/resistance. The nominal simulation is clean; zero makes the model undefined. For area, min=0 explicitly advertises the invalid boundary.

Require and assert resistance>0 before evaluating the tank equations. Use a physically meaningful positive lower bound for editor/tool feedback; do not clamp zero because that changes the time constant.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [FINDING-05128](../confirmed/FINDING-05128.md) | Tank | `resistance` |
| [FINDING-05129](../confirmed/FINDING-05129.md) | Tank | `area` |
