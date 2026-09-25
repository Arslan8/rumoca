> Historical preliminary record. GitHub access and the census are now complete; access-status statements below are superseded by [the current evaluation](README.md) and [focused results](focused-results.md). Existing execution evidence remains historical evidence, not a fresh run.

# Focused checks of upstream MSL issues

These checks concern **upstream GitHub issues**, not our own historical bug
reports. They cover two requested issues only and do not establish coverage of
the complete open-issue inventory.

| Upstream issue | Readable evidence | Current result |
|---|---|---|
| [#4771 — Simulation error when using MoistAir.T_psX](https://github.com/modelica/ModelicaStandardLibrary/issues/4771) | Issue body and linked-PR identity; original attachment and PR discussion unavailable | Reported failure pattern reproduced with OMC. Rumoca rejects both paired controls before producing bitcode; **no sanitizer detection credited**. |
| [#4807 — Modelica.Math.Nonlinear.quadratureLobatto](https://github.com/modelica/ModelicaStandardLibrary/issues/4807) | Title/open status/labels from the [upstream issue list](https://github.com/modelica/ModelicaStandardLibrary/issues) | Body and proposed PR unavailable. **Unassessed**, not a sanitizer miss or success. |

## #4771: reduced composition vector is sliced as a full vector

The upstream report describes a failed temperature calculation with the
one-element water-composition vector; supplying the complementary air fraction
makes it work. It points to `T_psX` taking `X[1:nX]` and proposes constructing
the missing fraction for reduced input. The issue links
[PR #4781](https://github.com/modelica/ModelicaStandardLibrary/pull/4781).
The accessible issue page exposed no discussion beyond its body; that is not
proof that no additional comments exist.
[Source: upstream #4771](https://github.com/modelica/ModelicaStandardLibrary/issues/4771).

### Applicability to our local library

The local MSL 4.1.0 source contains the reported operation:

- `Media/Air/MoistAir.mo:5–6` declares water/air and `reducedX=true`.
- `T_psX`, lines 1253–1273, accepts an open-size composition vector but passes
  `X[1:nX]` to its nested nonlinear function; this medium has two species.
- `setState_psX`, lines 1282–1300, reconstructs a full state composition in the
  reduced-input branch, but calls `T_psX` with the unreconstructed input.
- The public `temperature_psX` wrapper is in `Media/package.mo:4522`.

Thus this is an **interprocedural array-shape contract failure**, not a zero
denominator. Detecting some division elsewhere in these functions would not
count as finding this issue.

### Fresh execution evidence

The original attached zip could not be fetched. The checked-in
[probe driver](probes.py) therefore creates an explicitly labeled
**issue-body-derived** pair using the real, unmodified MSL public API. It does
not claim attachment equivalence.

Both controls compute entropy from full dry-air composition at `p=100000 Pa`,
`T=300 K`; the only changed call argument is the composition vector given to
`MoistAir.temperature_psX`:

| Control | Argument | OpenModelica 1.27.1 result | Current Rumoca result |
|---|---|---|---|
| Full composition | `{water, 1-water}`, `water=0` | Initializes/simulates successfully; CSV reports `T=300` | Compilation blocked at entropy parameter `s` evaluation |
| Reduced composition | `{water}`, `water=0` | Initialization fails: an access requests index 2 from an array of extent 1 | Same earlier compilation blocker |

OMC used the pinned local MSL 4.1.0, `CC=gcc`, one worker, ordinary `.mos`
execution, and a 60-second process-group timeout. The full and reduced
simulations took approximately 1.37 and 1.32 seconds respectively. The failure
is an array-index assertion, agreeing with the upstream report's mechanism.

Rumoca's failure is **not** that array access. Both controls stop earlier with
`ED019`: a numeric/type mismatch while evaluating `s`, at
`Media/package.mo:5180`, `invMMX[i] := 1/MMX[i]`. Since neither control yields a
canonical artifact, the current ModelSan static/runtime checks cannot run on
this probe. This is a compiler coverage blocker, not proof the sanitizer
recognized the upstream defect and not a new verdict against valid full input.

### Features needed for this issue

1. **Compiler support to reach the real call.** Resolve the demonstrated media
   function evaluation blocker; retain higher-order/nested function calls,
   actual argument shapes, and source locations through the analysis boundary.
2. **Array extent/index contracts across calls.** Prove that `X[1:nX]` requires
   an input extent of at least `nX`, propagate the caller's one-element shape,
   and reason about the reduced/full branch. An assertion or explicit
   precondition can be consumed as a contract rather than inferred intent.
3. **Array-access runtime evidence.** If static proof is unavailable, record
   the executed index/range, actual extent, call context, and canonical source
   location; classify a bounds failure distinctly from a generic solver error.
4. **A reduced/full representation equivalence oracle.** For valid compositions,
   compare temperature computed from reduced and completed composition vectors,
   and check entropy/temperature round trips. This is a targeted semantic test,
   not a universal property of arbitrary vectors.

The current [DimensionSan](../../../packages/modelsan/modelsan/sanitizers/dimension.py)
checks **physical units**, not array dimensions. DomainSan checks numerical
domains such as division/log/sqrt; neither currently supplies this shape
contract analysis. Generic failure reporting could notice the OMC abort when
given a probe, but would not automatically discover or attribute the array/API
contract defect.

## #4807: insufficient accessible issue evidence

The accessible upstream list identifies an open, high-priority Math bug titled
`Modelica.Math.Nonlinear.quadratureLobatto`, and the pull-request list contains
[PR #4808 — Updated Lobatto](https://github.com/modelica/ModelicaStandardLibrary/pull/4808).
The issue body, PR body/diff, and discussion were unavailable through the
available web access. Browser access was also unavailable.
[Sources: issue list](https://github.com/modelica/ModelicaStandardLibrary/issues),
[pull-request list](https://github.com/modelica/ModelicaStandardLibrary/pulls).

Local `Math/Nonlinear.mo:443–632` contains `quadratureLobatto`, including a
recursive `quadStep` and a function-valued integrand. That establishes the
function exists locally; it **does not establish** that the unseen upstream
witness applies to this version. No arbitrary quadrature test was substituted
for the issue. The exact failure, relevant input, intended behavior, and
required sanitizer/oracle remain unassessed until the body/discussion can be
read. In particular, no claim is made that this issue is divide-by-zero,
nontermination, or inaccurate integration solely from its title.

## Reproduction and provenance

[Machine-readable evidence](probes-results.json) preserves both compiler
diagnostics, OMC output, exact generated source, library SHA-256 digests, and
the Rumoca executable digest. Generated scripts/results are under
`target/msl-upstream-open-issues-20260924/probes-run-01/`.

From the repository root, choose a fresh output directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  docs/evaluations/msl-upstream-open-issues-2026-09-24/probes.py \
  --output target/msl-upstream-open-issues-20260924/probes-run-02
```

This uses the existing dirty-tree executable/Python implementation and the
bundled MSL 4.1.0; no production/library code was changed. Web observations were
made on 2026-09-24 and may reflect cached GitHub pages. These two rows must stay
separate from any future complete upstream-issue recall measurement.
