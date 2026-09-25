# Evaluation method and limits

[Overview](README.md) · [Static results](static-summary.md) · [Independent cases](independent.md) · [Runtime campaign](runtime.md)

## Scope and ground truth

"All issues" here means **all locally documented MSL report instances in the
latest reviewed ledger**, plus the five independently written LLM reports. It
does not mean all possible defects in MSL or every upstream GitHub issue.

The authoritative input is [v2's reviewed index](../../v2/verified/index.json):

| Stratum | Records | Executable model names | Use |
|---|---:|---:|---|
| `Modelica.*` | 5,173 | 233 | Main MSL corpus |
| `ModelicaTest.*` | 303 | 22 | Tests instantiating MSL declarations; included |
| MSL declaration-only census | 911 | 0 | Accounted separately; no executable witness |
| Custom/non-MSL models | 53 | 7 | Retained in the index, outside MSL scoring |
| Total | 6,440 | 262 | Every input ID retained exactly once |

The executable MSL strata contain 819 historically confirmed, 3,321
false-positive/explicit-non-defect, 666 unresolved, 638 advisory, and 32 candidate
records. These are report instances, not unique root causes. Existing non-defect
explanations are controls, not erroneous alarms merely because they are present
in output.

Do not sum the older `docs/verifiedBugs`, `docs/verified bugs`, and v2 counts.
They overlap and include superseded verdicts and tool defects. The independent
five-report corpus also overlaps tool findings; it is not five automatically
additional bugs.

Historical ground truth has qualifications. `BUG-010`, `018`, `020`, and `022`
describe source-level inactive flux normalization that OpenModelica can remove
on source retranslation. They are **not four uniformly reproduced active-model
failures**. This evaluation retains the ledger verdict and its link; it does
not silently promote those qualifications away. Likewise, two CriticalDamping
tool reports remain unresolved historically even though the independently
written exact source wrappers reproduce the structural issue.

## Static campaign

For each of the 255 executable MSL/ModelicaTest models:

1. Locate the original source using the checked-in corpus inventory.
2. Compile fresh bitcode with the current executable and
   `--no-fold-parameter-bindings`. The latter preserves dependency expressions
   needed to propose a public-parameter witness.
3. Load the artifact through the current Python SDK and run all static/hint
   providers in `DEFAULT`, plus DimensionSan, StructureSan, InitStaticSan and
   NetworkSan, directly. This deliberately measures analysis independent of
   runtime preparation; it is not the integrated CLI success rate.
4. Retain full findings/hints, analysis exceptions, compiler diagnostics,
   artifact digests, and every report ID.
5. Match original reports conservatively to new output using original model,
   target, sanitizer family, source ownership/line, denominator or physical
   rule, and complete witness. Normalize formatting only; do not invent
   algebraic equivalence or branch reachability.

An exact static match means the archived reported operation/rule is identified
again. It does **not** independently establish a source defect. A same-target
warning at another denominator cannot count. If old evidence has only an
ambiguous basename, a missing witness, or a changed trigger, retain an
ambiguous match. Missing/unknown metadata kinds never default to bug candidates.

Budgets: three isolated model workers; 20 seconds per source compilation;
20 seconds per static/hint operation; 180 seconds per model worker; 8 GiB
address-space limit per static worker. One full-sweep attempt per model, no
success-by-retry. Two models were smoke-tested before the full sweep and then
both rebuilt during the full sweep. These smoke tests are not extra successful
models in the denominator.

The initial sweep began before run IDs were added to the evaluation harness.
Its final collection validates every checkpoint **and worker log** against the
earliest full-sweep worker timestamp, `1790248132.4483266`, and requires completed
worker state. This is recorded as timestamp-based adoption, not falsely claimed
as a launch-time run ID. Subsequent runs write a campaign UUID and requested
model list before dispatch; collection rejects stale or out-of-request files.
A partial `--model` run cannot borrow the other models from a prior campaign.

## Seeded runtime campaign

The runtime catalog merges exact historical source-verification witnesses,
the two physical witnesses, and inherited BUG triggers. It deduplicates exact
model/parameter assignments into 315 cases across 124 models while retaining
all 819 associated confirmed report IDs. In particular, the op-amp equality
probe uses the reviewed `Vps=-15`, not an unrelated zero probe.

The driver consumes fresh artifacts, checks their digests, prepares the current
backend, runs one nominal control per model, and only executes eligible scalar
parameter cases after a successful nominal. It invokes the current runtime
observers on actual results. Bad baselines, unavailable artifacts, unsupported
configuration, missing observations, timeouts and unrun cases stay visible.

These are **externally seeded** cases, not independent discovery. The new
pipeline collects hints but does not schedule them automatically. Same-kind
native domain signals carry backend instruction anchors; without source-site
identity they are not exact historical-site detections. A generic non-finite
failure is a symptom, not a diagnosed denominator. Successful runs can contain
informational internal-trial faults; compare with nominal and do not promote
trial evidence into a source bug.

Runtime overrides are not a substitute for source retranslation. In
particular, absent structural metadata is not proof that a parameter does not
control shape or conditional structure. Explicitly known protected/final,
structural, array, or folded-dependent cases require a legal source witness.
The CriticalDamping independent probes demonstrate why this distinction matters.

Budget and horizon are recorded in [runtime.md](runtime.md). A bounded clean
run does not establish safety for all times, inputs, or configurations. The
historical OMC corpus evidence is reused as the independent source-witness
reference; hundreds of OMC pairs were **not** rerun in this campaign.

## Independent challenge set

The five previously written LLM reports provide seven concrete witness
variants. Each receives a fresh nominal compile/static analysis, the actual
runtime attempt, exact source-trigger compilation, and a newly run paired OMC
control against the pinned local MSL 4.1.0 sources. All seven pairs and their
observed limitations are recorded [separately](independent.md).

Compiler rejection of an exact bad source is useful corroborating evidence
but is not a sanitizer detection. Generic solver failure is not exact causal
detection. A nominal importer/transport failure prevents attribution of a
subsequent failure to the proposed witness.

## Reproduce and inspect

Run from the repository root. The full run replaces this evaluation's current
checkpoints/results; preserve them elsewhere before a comparison run. Run only
one campaign against this output directory at a time. Do not edit/rebuild the
compiler, Python packages, or MSL inputs during a campaign; none were changed
during this evaluation. The input manifest is collected at the end, not a
claim that a start/end integrity comparison was performed.

```sh
PYTHONPATH=packages/rumoca-bitcode:packages/modelsan \
RUMOCA="$PWD/target/debug/rumoca" RAYON_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1 \
python3 docs/evaluations/msl-issues-2026-09-24/evaluate.py

CARGO_BUILD_JOBS=4 RUST_TEST_THREADS=4 RAYON_NUM_THREADS=4 \
python3 docs/evaluations/msl-issues-2026-09-24/runtime.py
python3 docs/evaluations/msl-issues-2026-09-24/runtime.py --check-boundaries
python3 docs/evaluations/msl-issues-2026-09-24/runtime.py --collect
python3 docs/evaluations/msl-issues-2026-09-24/build_tables.py
```

The table builder joins the static and seeded-runtime rows by report ID. Rerun
both campaigns before regenerating a new combined index; do not reuse old
runtime outcomes as current results. See the [runtime driver](runtime.py) and
[independent reproduction instructions](independent.md#evidence-and-reproduction)
for details. The [input manifest](input-manifest.json) pins the executed binary,
Python package inputs, ledger, inventory, and local MSL source digests. This is
the current **dirty working tree** at HEAD
`b38af3a38b0224bf22129cb1148ebf70e2492aa7`, not a clean-commit result.

Evaluation artifacts are under `target/msl-issue-evaluation-20260924/`; durable
JSON and Markdown summaries are beside this method. No production compiler or
sanitizer implementation was changed during this evaluation.

## What may be claimed in a paper

- Coverage of this **known-report regression corpus**, with explicit blocked,
  ambiguous and unresolved counts.
- Separate static matching, externally seeded runtime evidence, and independent
  source-witness confirmation; separate report instances and root causes.
- Small independent challenge-set performance, with all seven variants shown.

Do **not** present rediscovery of the tool's own past findings as an unbiased
estimate of recall over all MSL bugs. Do not count unresolved rows as positives
or negatives, advisories as errors, compiler failures as detections, and tool
bugs as MSL bugs. Broader claims require additional independently sampled bug
classes and matched non-defect controls. This is not the 566-model MSL trace
parity gate; no cohort simulation-parity percentage is claimed.
