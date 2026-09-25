# Historical false-positive controls: remaining precision gaps

This is a regression-test inventory, **not a claim that these problems were
introduced by the latest changes**. No previous-checkout delta was measured.
The new run analyzed all **255 Modelica / ModelicaTest models** in the local
issue corpus. It preserves the old adjudications rather than silently replacing
them with fresh analyzer output.

Start with the [evaluation overview](README.md), [complete result ledger](corpus-results.json),
[matching implementation](matching.py), and
[historical adjudications](../../v2/verified/README.md).

## Final control counts

There are **3,321 historical false-positive / explicit-non-defect report
instances** attached to these 255 models. The bucket intentionally includes
earlier outputs that already said “not a defect.” Such informational records
are not counted as current false-positive alarms.

| Current result at the historical reported operation | Reports |
|---|---:|
| Explicit non-defect explanation | 2,986 |
| Intent advisory, not a defect claim | 6 |
| Not reported | 1 |
| Re-emitted static defect candidate | **328** |
| Total | **3,321** |

The 328 candidates span 73 models. These are report-instance counts, not 328
distinct bugs. Matching checks the source path/line and complete denominator,
witness and recorded path for divisor reports; physical reports require the
same declaration site, rule and predicate. Formatting-only changes are
normalized. A different warning mentioning the same parameter does not count:
target-only matching would incorrectly produce **330**, rather than 328.

The 328 are **overlaps with historical refutations**, not 328 newly adjudicated
false positives. In particular, 33 machine-resistance records need policy and
ground-truth reconciliation, explained below. A 2026-09-24 static rerun does not
itself repeat the older OpenModelica execution tests.

| Historical group | Exact re-emitted candidates | Current interpretation |
|---|---:|---|
| `illegal-divisor-witness` | 284 | Same exact witness previously rejected by OMC: 224 final-modifier reports and 60 protected-element reports |
| `guarded-transmission-line` | 8 | Existing assertion is visible, but PhysicalSan still claims missing domain enforcement |
| `ideal-dc-armature-ra` | 17 | Nonnegative winding policy versus historical signed/zero-limit adjudication; re-review required |
| `ideal-dc-machine-data` | 14 | Same policy/adjudication mismatch |
| `ideal-stator-resistance` | 3 | One compound-denominator inference problem; two policy/adjudication cases |
| `ideal-stator-leakage` | 1 | A symbol inside a composite denominator is incorrectly promoted to an individual positive-domain requirement |
| `zero-machine-data-leakage` | 1 | Same composite-denominator inference problem |

All IDs remain individually inspectable in `corpus-results.json`: select
`verdict == "false-positive"` and `exact_candidate == true`. The underlying
fresh findings and canonical IDs remain in each row's `model_evidence` file.

## Priority / expected return

| Priority | Work | Directly relevant controls | Why spend time here? |
|---|---|---:|---|
| 1 | Legal public witness generation, including effective `final` modifiers and protected instance paths | 284 reports / 122 model-witness cases | Largest demonstrated source of refuted witnesses; split producer metadata repair from consumer eligibility |
| 2 | Share assertion/domain proof between DivisorSan and PhysicalSan | 8 | Small, concrete cross-detector inconsistency; the current artifact already has the assertion |
| 3 | Stop converting “appears inside a denominator” into a scalar sign/zero contract | 3 | Small observed count but a general soundness problem that can affect many future models |
| 4 | Reconcile machine-winding intent policy and stale adjudication reuse | 33 | Important for trustworthy evaluation; do not “fix” the detector by globally suppressing legitimate negative-resistance warnings |

These numbers are coverage of this fixed issue corpus, not a predicted precision
score or an estimate of every affected MSL component.

## 1. A zero witness must be a legal configuration change

### Protected value: information exists, consumer ignores it

[FINDING-00015](../../v2/verified/false-positives/FINDING-00015.md),
`Modelica.Clocked.Examples.Systems.Utilities.ComponentsMixingUnit.FilterOrder`,
still emits `mixingUnit.tau0 = 0` for the denominator `mixingUnit.tau0`.
See the [current findings](../../../target/msl-issue-evaluation-20260924/corpus/d5252c4962b43c83/static.json)
and [original report](../../v2/bugs/FINDING-filterorder-mixingunit-tau0-divzero.md).

The current artifact retains this contract on `mixingUnit.tau0`:

```json
{
  "variability": "parameter",
  "is_protected": true,
  "effective_value": 60.0,
  "declared_in": "Modelica.Clocked.Examples.Systems.Utilities.ComponentsMixingUnit.MixingUnit"
}
```

Its binding is the literal `60`. Nevertheless,
[`_Immutability.settable`](../../../packages/modelsan/modelsan/divisor/constraints.py)
produces `settable=True`, with domain `[-inf, inf]`. The code explicitly assumes
protected parameters can be set before translation. The retained OMC evidence
rejects this exact nested modification: **protected element `tau0` may not be
modified**. This is not missing protection metadata in this example; it is a
consumer-side failure to use it for the selected public witness interface.

### Final modifier: effective restriction is missing from the current artifact

[FINDING-00782](../../v2/verified/false-positives/FINDING-00782.md),
`Modelica.Electrical.Analog.Examples.OpAmps.Adder`, still emits
`add.opAmp.Vps = -15`. See the
[current findings](../../../target/msl-issue-evaluation-20260924/corpus/c7904b6685dc9ab4/static.json).
`PartialOpAmp.mo` configures its child with:

```modelica
Ideal.IdealizedOpAmpLimited opAmp(
  V0=V0,
  final useSupply=false,
  final Vps=Vps,
  final Vns=Vns);
```

OMC rejects the reported modification of the final child `Vps`. In the fresh
bitcode, however, `add.opAmp.Vps` has `binding_from_modification=true`,
`binding_depends_on=[34]`, and binding `add.Vps`, but **no `is_final` flag**;
it is also marked `tunable=true`. The producer must retain the effective final
modifier through flattening/export. Repairing the consumer alone cannot recover
a restriction that disappeared before the sanitizer read it.

### Required change without losing legitimate issues

Keep two different properties:

1. **Directly modifiable through this interface:** can the generated wrapper
   legally assign this exact qualified name?
2. **Can vary through legal dependencies:** can public settings change this
   derived or final value?

The first is false for the final child above, while the second can be true.
Follow `binding_depends_on` to `add.Vps`; propose and validate a public setting
there, instead of assigning `add.opAmp.Vps`. Do not count that proposed new
witness as verified until it passes declaration/branch constraints and an
independent source-modified test. Reject the old illegal witness even when the
underlying arithmetic problem is reachable through another legal setting.

The effective contract needs declaration prefixes **and modification-site
prefixes**, binding dependencies, owner/access scope, and restrictions along
the qualified component path. Existing leaf `is_protected`/`is_final` fields
are useful but do not by themselves prove external modifiability of every
nested name. A source-level access rule is also different from whether an
already-built executable happens to expose parameter storage.

Regression controls: retain the two examples above; fixed protected literal
parameters must not yield direct public assignments; final/protected derived
parameters depending on legal public knobs must still expose reachable faults
through those knobs; public FirstOrder `T=0` and the public equal-supply witness
in LCOscillator must remain discoverable. The
[OMC source ledger](../../v2/verified/omc-source-verification.json) retains all
122 refuted cases and their exact generated wrappers: 109 final cases and 13
protected cases, covering 224 and 60 report instances respectively.

## 2. PhysicalSan must honor a guard DivisorSan already recognizes

[FINDING-00500](../../v2/verified/false-positives/FINDING-00500.md),
`CompareLineTrunks.tLine1.Z0`, is representative of eight reports across three
models. The [current findings](../../../target/msl-issue-evaluation-20260924/corpus/1ffcf476bae0a4c2/static.json)
contain both:

- PhysicalSan: `physical-domain-unenforced`, requiring `tLine1.Z0 > 0`.
- DivisorSan: `divisor-guarded-by-assertion`, explicitly not a defect.

The source contains `assert(Z0 > 0, "Z0 has to be positive")`. The fresh
analysis environment retains `(tLine1.Z0 > 0)`, stores `tLine1.Z0` in
`guarded_shapes`, and records the reason `assert tLine1.Z0 greater 0`.
This is therefore **not an absent-assertion IR feature** in this example.

The scalar interval is nevertheless stored as `[0, inf]`, losing the strict
endpoint. [`contracts.infer._safe_denominator`](../../../packages/modelsan/modelsan/contracts/infer.py)
checks the interval instead of the complete assertion proof; the inferred
`DIRECT_DIVISOR` contract then wins and PhysicalSan says nothing enforces the
domain. Reuse a common scoped domain/enforcement proof, with strict endpoints,
instead of creating contradictory judgments in two detectors.

Regression IDs: `FINDING-00500`–`00503`, `00552`–`00554`, `00692`.
Test `assert(d > 0)` and `assert(d >= eps)` as excluded-zero cases, but keep
`assert(d >= 0)` distinct: it does **not** exclude zero. Conditional assertions
and disjunctions must retain their scope/logical structure; do not treat every
relation appearing inside an assertion as an independently enforced fact.
An unguarded `1/d`, or an insufficient/non-dominating guard, must still report.

## 3. A composite denominator is not a positivity contract on every member

The three relevant controls are:

| Historical refutation | Target | Fresh evidence |
|---|---|---|
| [FINDING-02270](../../v2/verified/false-positives/FINDING-02270.md) | `IMS_Start.aims.Rs` | [Current findings](../../../target/msl-issue-evaluation-20260924/corpus/2804e4f64ad6a33e/static.json) |
| [FINDING-02272](../../v2/verified/false-positives/FINDING-02272.md) | `IMS_Start.aims.Lssigma` | Same model artifact |
| [FINDING-02310](../../v2/verified/false-positives/FINDING-02310.md) | `IMS_Start.aimsData.Lssigma` | Same model artifact |

The contract inference labels each as `DIRECT_DIVISOR`, and PhysicalSan uses
`authority=source_arithmetic` to establish the existing scalar predicate. The
actual source denominator is of the form:

```text
sqrt(Rs^2 + (2*pi*fsNominal*(Lm + Lssigma))^2)
```

Evaluating the complete retained denominator using the fresh artifact gives:

| Single parameter changed, all other values nominal | Denominator |
|---|---:|
| No change | 3.0001499962501876 |
| `aims.Rs = 0` | 3.0 |
| `aims.Lssigma = 0` | 2.898378857223465 |
| `aimsData.Lssigma = 0` in the corresponding data formula | 2.898378857223465 |

These are expression evaluations, **not new whole-model simulations**. They
prove that simply occurring in this denominator does not establish the claimed
individual zero fault. It also cannot establish nonnegativity: `Rs` is squared,
and an arbitrary existing sign predicate is not a consequence of nonzero
division. A separate machine-winding policy may still be appropriate.

[`contracts.infer._walk`](../../../packages/modelsan/modelsan/contracts/infer.py)
recursively tags each parameter under `/` as a divisor when the entire interval
can include zero. This must reuse the complete-denominator/path witness proof,
not just membership of the denominator's expression tree. Only derive a scalar
contract when the corresponding implication is proved; otherwise retain a
relational constraint or a candidate for the complete expression.

Regression pairs: retain the nominal and single-zero cases above; also retain
a genuinely zero complete denominator, including a legal multi-parameter
witness when needed. Test `p + q`, `p - q`, `max(eps, abs(p))`, and sums of
squares. Do not suppress all composite denominators or all machine formulas.

## 4. Re-adjudicate machine-resistance policy; do not mistake stale labels for proof

The other **33** physical overlaps are 17 armature `Ra` reports, 14 machine-data
`Ra` reports, and two stator `Rs` reports (`FINDING-02817`, `FINDING-05214`).
Examples:

| Report | Current predicate / authority | Historical refutation |
|---|---|---|
| [FINDING-01304](../../v2/verified/false-positives/FINDING-01304.md), `DC_CompareCharacteristics.dcpm.Ra` | `Ra >= 0`, component winding contract | Zero-loss/signed Basic.Resistor delegation |
| [FINDING-01300](../../v2/verified/false-positives/FINDING-01300.md), `dcpmData.Ra` | `Ra >= 0`, component winding contract | Zero-loss record forwarded to multiplicative equations |
| [FINDING-02817](../../v2/verified/false-positives/FINDING-02817.md), `SMPM_VoltageSource.smpm.Rs` | `Rs >= 0`, component winding contract | Signed primitive / zero copper-loss limit |

Fresh evidence: [DC_CompareCharacteristics](../../../target/msl-issue-evaluation-20260924/corpus/f15341d4427cc3e0/static.json),
[SMPM_VoltageSource](../../../target/msl-issue-evaluation-20260924/corpus/d529fc5d98897b6a/static.json).

Supporting zero does not refute `R >= 0`; nor does a signed generic resistor
automatically establish that a particular physical winding intends negative
resistance. Conversely, a generic physical expectation is not proof of a
programming error in a custom/incremental model. These require a specific
contract/assumption and an appropriate distinction between advisory policy and
execution failure. This audit does **not** newly certify all 33 as false alarms.

There is also an evaluation defect to repair:
[`build_reports.py`](../../v2/verified/build_reports.py) reuses prior physical
verdicts by `(model, target)`. It special-cases one old resistance group for
re-review but inherits other zero-limit refutations without checking that the
predicate/authority stayed the same. Key adjudication reuse by the complete
claim—predicate, witness, authority, source identity and version—not merely
the parameter name. Otherwise improving a detector can look like a precision
failure against an obsolete label.

Preserve zero loss; retain negative-winding diagnostics when an explicit
component/application contract establishes them; keep unknown intent visible
as an advisory; never promote a permissive declaration alone to an observed
runtime defect. Re-run the same positive and negative controls after either
policy or ledger changes, keeping changed labels and their reasons visible.

## What this evaluation does not establish

No source models or sanitizers were fixed by this note. The older OMC evidence
is the witness-admissibility oracle for the 284 controls; the current run
establishes their re-emission with matching witnesses. These controls cannot
alone estimate MSL-wide precision, and a rejected direct modifier does not
prove every alternative public configuration safe. Finally, the 10 historical
confirmed BUG records with basename-only sources remain conservative automated
matching gaps, not newly discovered detector misses; the broader evaluation
keeps them separate from strict source-site matches.
