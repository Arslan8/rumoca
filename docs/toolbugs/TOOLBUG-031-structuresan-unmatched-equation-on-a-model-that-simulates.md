# TOOLBUG-031: StructureSan reports an unmatched equation in a model that simulates

**Status:** open
**Found:** 2026-09-26, first run of the sanitizers over
[FIRE_CP_Glimpse](../findings/external/fire-cp-glimpse-2026-09-26.md).

## The defect

`StructureSan` reports, at **high** severity:

```
UNMATCHED_EQUATION   equation: ?   scalar_rows: 1   rows_matched: 0
  anchors: ['equ:16777217']
  note: this constraint has no unknown left to determine;
        the region is over-constrained
```

for `RoverExample.Components.RoverLowFidelity`, together with a
`non-square-block` reporting 20 equations against 19 variables.

The model simulates:

```
Simulating RoverExample.Components.RoverLowFidelity to t=1...
Simulation complete: 501 time points, 53 variables
```

It is not over-constrained. Both findings are false.

## Why it is worth fixing rather than tolerating

The same sanitizer, in the same run, was **right** about
`RoverHighFidelity`, where rumoca's own proof reports `EL005 structurally
singular system: 116 matched out of 117`. So the kind cannot be dismissed and
cannot be trusted: on one model it agrees with the compiler and on the next it
contradicts it, with the same severity and the same wording.

High severity is the claim that a reviewer should act on first. A structural
claim that is right half the time spends their attention and teaches them to
skip the kind, which costs the true positive too.

## What the evidence already shows

Two details point at the cause without settling it:

- the anchor is `equ:16777217` = `0x1000001`, an *equation family* key rather
  than a scalar equation id, and the evidence prints `equation: ?` because the
  reverse lookup failed. The finding cannot name what it is about.
- the model carries 4 equation families (9, 3, 9 and 3 scalar rows) beside 25
  scalar equations, and `when`-form equations among them. Matching counts
  family rows through `structural.family_key`; a family whose rows are counted
  but whose determined variables are not would produce exactly this shape —
  one row with nothing to match.

A finding that cannot name its own equation should not be emitted at high
severity. That is the smaller, independent fix.

## Fix

1. Resolve the family key before reporting, and *withhold* the finding when the
   lookup fails — an anchor a reader cannot follow is not evidence.
2. Establish whether family rows and the variables they determine are counted
   on the same side of the matching, using this model as the regression.
3. Where rumoca's own structural proof is available, prefer it: `EL005`
   settles the question the sanitizer is guessing at.

## Regression

`RoverExample.Components.RoverLowFidelity` from FIRE_CP_Glimpse must produce no
`UNMATCHED_EQUATION`, and `RoverHighFidelity` must continue to produce one. The
pair is the test; either alone can be satisfied by a sanitizer that is simply
silent or simply loud.
