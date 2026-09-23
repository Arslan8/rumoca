# FINDING-04237: Tensor entries are not all strictly positive scalars

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | signed-inertia-tensor |
| Model | Modelica.Mechanics.MultiBody.Examples.Rotational3DEffects.BevelGear1D |
| Target | bodyBox.I |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-bevelgear1d-bodybox-i-tensorunknown.md](../../v2/bugs/FINDING-bevelgear1d-bodybox-i-tensorunknown.md) — reviewed as `FINDING-04237-bevelgear1d-bodybox-i.md`, which a later run renamed |
| Original SHA-256 | 8ff93a9b0d078eea14a8f175bd4f2fdeadde0041899e3d9c7d4b6902a403a61e |

## Why this is a false positive

Off-diagonal inertia tensor entries are signed (the declaration explicitly allows negative infinity as a lower bound); zero off-diagonal entries describe principal axes. The assembled tensor must satisfy matrix-level physical constraints, not elementwise strict positivity. This does not dismiss a separate invalid diagonal/eigenvalue report.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/MultiBody/Parts/BodyBox.mo:111`. Role: `parameter`; binding: `Modelica.Mechanics.MultiBody.Frames.resolveDyade1(bodyBox.R.T, bodyBox.R.w, diagonal(({((bodyBox.mo * ((bodyBox.width * bodyBox.width) + (bodyBox.height * bodyBox.height))) - (bodyBox.mi * ((bodyBox.innerWidth * bodyBox.innerWidth) + (bodyBox.innerHeight * bodyBox.innerHeight)))), ((bodyBox.mo * ((bodyBox.length * bodyBox.length) + (bodyBox.height * bodyBox.height))) - (bodyBox.mi * ((bodyBox.length * bodyBox.length) + (bodyBox.innerHeight * bodyBox.innerHeight)))), ((bodyBox.mo * ((bodyBox.length * bodyBox.length) + (bodyBox.width * bodyBox.width))) - (bodyBox.mi * ((bodyBox.length * bodyBox.length) + (bodyBox.innerWidth * bodyBox.innerWidth))))} / 12)))`; effective min: `None`; effective max: `None`. 

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

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/26b9a2fb6232f828.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/signed-inertia-tensor.md) · [Index](../README.md)
