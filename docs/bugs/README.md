# Moved to [`../v2/bugs/`](../v2/bugs/README.md)

The per-instance reports are published in **[`docs/v2/bugs/`](../v2/bugs/README.md)**.

This directory held the first round: one file per instance, generated from the
run of 2026-09-16 and reviewed in
[`../verifiedBugs/`](../verifiedBugs/README.md), which labelled 3304 of its
6079 reports false positives.

Acting on that review changed enough that the second round is a different set
of claims rather than a correction to the first, so it is published beside it
instead of over it:

| | |
|---|---|
| [TOOLBUG-020](../toolbugs/TOOLBUG-020-zero-behaviour-was-decided-three-times.md) | one zero-behaviour contract shared by three detectors |
| [TOOLBUG-021](../toolbugs/TOOLBUG-021-locations-named-a-basename.md) | declarations identified by path, not basename |
| [TOOLBUG-022](../toolbugs/TOOLBUG-022-a-violated-invariant-never-consulted-the-contract.md) | the contract now gates violated invariants too |
| [TOOLBUG-023](../toolbugs/TOOLBUG-023-a-tensor-checked-one-entry-at-a-time.md) | inertia tensors judged as tensors; resistance scoped by component |

**3007 of the review's 3304 false positives (91%)** are no longer reported, or
are reported under a kind that makes no defect claim. The first round's files
are not kept: every one of them is reproducible from its run, which is archived
in [`../runs/data/`](../runs/data/), and the review that read them records each
report's SHA-256 in `../verifiedBugs/inventory.json`.

Round-two links out of the review pages point here into `../v2/bugs/`, so a
reviewed claim that survived can be opened in its current form and one that did
not ends at [`../v2/bugs/withdrawn.md`](../v2/bugs/withdrawn.md).
