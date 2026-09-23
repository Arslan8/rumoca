# FINDING-05128: Tank permits a direct zero divisor

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | tank-zero-divisor |
| Model | Tank |
| Target | resistance |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-tank-resistance-divzero.md](../../v2/bugs/FINDING-tank-resistance-divzero.md) — reviewed as `FINDING-05128-tank-resistance.md`, which a later run renamed |
| Original SHA-256 | 58dbf5d4c2b08264b67b0f9544c0195fd1f97ea06a891d9d9276be1ea321eea3 |

## Verification and root cause

The local model declares resistance with no strictly-positive enforcement that excludes zero and evaluates flow_out=level/resistance. The nominal simulation is clean; zero makes the model undefined. For area, min=0 explicitly advertises the invalid boundary.

## Source evidence

Compiler/source-resolved declaration: `/data/mrumoca/rumoca/examples/modelsan/Tank.mo:3`. Role: `parameter`; binding: `2.0`; effective min: `None`; effective max: `None`. 

[/data/mrumoca/rumoca/examples/modelsan/Tank.mo — source snapshot](../evidence/sources/9ef56c9f627e0ea9-Tank.mo)

```modelica
1: model Tank "Drains through a flow restriction."
2:   parameter Real area(min = 0.0) = 1.0 "tank cross-section";
3:   parameter Real resistance = 2.0 "flow restriction";
4:   Real level(start = 1.0, min = 0.0, max = 2.0) "liquid level";
5:   Real flow_out "outflow rate";
6: equation
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
| `resistance=0` | reported-failure |

Diagnostic: solve-IR evaluation failed: non-finite (inf) value computed for `flow_out` @ Span { source: SourceId(17683934560766090435), start: BytePos(229), end: BytePos(242) }

## Proposed fix

Require and assert resistance>0 before evaluating the tank equations. Use a physically meaningful positive lower bound for editor/tool feedback; do not clamp zero because that changes the time constant.

## Fix validation

Test nominal draining, resistance=0, negative resistance, and small positive values with an explicit configuration diagnostic.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/tank-zero-divisor.md) · [Index](../README.md)
