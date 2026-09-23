# FINDING-05129: Tank permits a direct zero divisor

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | tank-zero-divisor |
| Model | Tank |
| Target | area |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-tank-area-divzero.md](../../v2/bugs/FINDING-tank-area-divzero.md) — reviewed as `FINDING-05129-tank-area.md`, which a later run renamed |
| Original SHA-256 | d144452db78a4106534bb4178b8052fd79d823a07b6e6a566859416252444dee |

## Verification and root cause

The local model declares area with no strictly-positive enforcement that excludes zero and evaluates der(level)=-flow_out/area. The nominal simulation is clean; zero makes the model undefined. For area, min=0 explicitly advertises the invalid boundary.

## Source evidence

Compiler/source-resolved declaration: `/data/mrumoca/rumoca/examples/modelsan/Tank.mo:2`. Role: `parameter`; binding: `1.0`; effective min: `0.0`; effective max: `None`. 

[/data/mrumoca/rumoca/examples/modelsan/Tank.mo — source snapshot](../evidence/sources/9ef56c9f627e0ea9-Tank.mo)

```modelica
1: model Tank "Drains through a flow restriction."
2:   parameter Real area(min = 0.0) = 1.0 "tank cross-section";
3:   parameter Real resistance = 2.0 "flow restriction";
4:   Real level(start = 1.0, min = 0.0, max = 2.0) "liquid level";
5:   Real flow_out "outflow rate";
```

[/data/mrumoca/rumoca/examples/modelsan/Tank.mo — source snapshot](../evidence/sources/9ef56c9f627e0ea9-Tank.mo)

```modelica
1: model Tank "Drains through a flow restriction."
2:   parameter Real area(min = 0.0) = 1.0 "tank cross-section";
3:   parameter Real resistance = 2.0 "flow restriction";
4:   Real level(start = 1.0, min = 0.0, max = 2.0) "liquid level";
5:   Real flow_out "outflow rate";
6: equation
7:   flow_out = level / resistance;
8:   der(level) = -flow_out / area;
9: end Tank;
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/c0b21fb164deefc9.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `area=0` | reported-failure |

Diagnostic: solve-IR evaluation failed: non-finite derivative evaluation for state 'level'

## Proposed fix

Require and assert area>0 before evaluating the tank equations. Use a physically meaningful positive lower bound for editor/tool feedback; do not clamp zero because that changes the time constant.

## Fix validation

Test nominal draining, area=0, negative area, and small positive values with an explicit configuration diagnostic.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/tank-zero-divisor.md) · [Index](../README.md)
