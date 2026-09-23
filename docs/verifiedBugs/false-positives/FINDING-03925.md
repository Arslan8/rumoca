# FINDING-03925: Tensor entries are not all strictly positive scalars

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | signed-inertia-tensor |
| Model | Modelica.Mechanics.MultiBody.Examples.Elementary.DoublePendulum |
| Target | boxBody1.I |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-doublependulum-boxbody1-i-tensorunknown.md](../../v2/bugs/FINDING-doublependulum-boxbody1-i-tensorunknown.md) — reviewed as `FINDING-03925-doublependulum-boxbody1-i.md`, which a later run renamed |
| Original SHA-256 | 02399e0557d73f838eb6a95403b83246be1121f7a8df06e1db12e126adfe7121 |

## Why this is a false positive

Off-diagonal inertia tensor entries are signed (the declaration explicitly allows negative infinity as a lower bound); zero off-diagonal entries describe principal axes. The assembled tensor must satisfy matrix-level physical constraints, not elementwise strict positivity. This does not dismiss a separate invalid diagonal/eigenvalue report.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/MultiBody/Parts/BodyBox.mo:111`. Role: `parameter`; binding: `Modelica.Mechanics.MultiBody.Frames.resolveDyade1(boxBody1.R.T, boxBody1.R.w, diagonal(({((boxBody1.mo * ((boxBody1.width * boxBody1.width) + (boxBody1.height * boxBody1.height))) - (boxBody1.mi * ((boxBody1.innerWidth * boxBody1.innerWidth) + (boxBody1.innerHeight * boxBody1.innerHeight)))), ((boxBody1.mo * ((boxBody1.length * boxBody1.length) + (boxBody1.height * boxBody1.height))) - (boxBody1.mi * ((boxBody1.length * boxBody1.length) + (boxBody1.innerHeight * boxBody1.innerHeight)))), ((boxBody1.mo * ((boxBody1.length * boxBody1.length) + (boxBody1.width * boxBody1.width))) - (boxBody1.mi * ((boxBody1.length * boxBody1.length) + (boxBody1.innerWidth * boxBody1.innerWidth))))} / 12)))`; effective min: `None`; effective max: `None`. 

[Mechanics/MultiBody/Parts/BodyBox.mo — source snapshot](../evidence/sources/698eec27fd1d9230-BodyBox.mo)

```modelica
109:       normalizeWithAssert(lengthDirection)*length/2
110:     "Position vector from origin of frame_a to center of mass, resolved in frame_a";
111:   final parameter SI.Inertia I[3, 3]=Frames.resolveDyade1(R, diagonal({mo*(
112:       width*width + height*height) - mi*(innerWidth*innerWidth + innerHeight*
113:       innerHeight),mo*(length*length + height*height) - mi*(length*length +
114:       innerHeight*innerHeight),mo*(length*length + width*width) - mi*(length*
```

[Mechanics/MultiBody/Parts/BodyBox.mo — source snapshot](../evidence/sources/698eec27fd1d9230-BodyBox.mo)

```modelica
109:       normalizeWithAssert(lengthDirection)*length/2
110:     "Position vector from origin of frame_a to center of mass, resolved in frame_a";
111:   final parameter SI.Inertia I[3, 3]=Frames.resolveDyade1(R, diagonal({mo*(
112:       width*width + height*height) - mi*(innerWidth*innerWidth + innerHeight*
113:       innerHeight),mo*(length*length + height*height) - mi*(length*length +
114:       innerHeight*innerHeight),mo*(length*length + width*width) - mi*(length*
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/69ffce7f37cd1d7e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/signed-inertia-tensor.md) · [Index](../README.md)
