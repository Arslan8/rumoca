# Audit of the 2026-09-17 rerun

[Verification overview](README.md) · [Machine-readable index](index.csv)

The refreshed `docs/v2/bugs` corpus contains the same 6,440 stable report IDs.
The verification ledger was rebuilt from the refreshed files and accounts for
every ID exactly once.

## What the student fix got right

- All 638 `physical-intent-question` reports are low severity and carry
  `premise_state=unknown`, `authority=quantity_or_unit`, and a question for the
  author. They remain visible without being counted as defect claims.
- All 224 current-run physical defect claims have an established premise: 122
  from a component contract and 102 from intent-independent source arithmetic.
- The two independently reproduced physical failures remain defect claims:
  `LCOscillator.C` (zero reaches a division) and `Multivibrator.R2` (the
  negative witness reaches an invalid logarithm argument).
- All 681 `physical-rule-does-not-apply` reports remain visible as explicit
  non-defects rather than disappearing.
- The divisor finding population and witnesses were not suppressed by the
  intent-policy change.

## Residual issues

### Four refutations omit the final premise metadata

The following reports correctly include the signed-resistance component
contract and correctly decline the generic positivity rule, but their final
evidence table omits `premise_state=refuted` and
`authority=component_contract`:

- [FINDING-00122](../bugs/FINDING-cauerlowpasssc-r4-r-ruleoff.md)
- [FINDING-00123](../bugs/FINDING-cauerlowpasssc-r5-r-ruleoff.md)
- [FINDING-00124](../bugs/FINDING-cauerlowpasssc-r8-r-ruleoff.md)
- [FINDING-00125](../bugs/FINDING-cauerlowpasssc-r9-r-ruleoff.md)

These four take the observed-value supported-contract branch in
`PhysicalSan.analyze`. That branch constructs the finding directly instead of
using the common refutation helper. The verdicts are correct, but the promised
end-to-end premise-state schema is incomplete. Add those two fields (and the
canonical declaration/semantic role where available) to that branch, then use
these four reports as regression fixtures.

### The input tier still overstates what is proven

The input README says all 26 `BUG-*` reports are proven. Independent controls
confirm 11 and refute 15; reproducing the analyzer output is not the same as
verifying the defect attribution. The split is retained in the
[verified defects](confirmed.md) and [false-positive](false-positives.md)
indexes.

The `Candidate` tier also contains explicit non-defects and intent questions.
That makes the source reports say “candidate” even when their finding kind says
“not a claim.” The verification ledger therefore keeps advisory, non-defect,
candidate and unresolved outcomes separate.

### One generated count is stale

`docs/v2/bugs/README.md` says “400 of 5142” candidate reports were sampled,
while this rerun contains 5,503 `FINDING-*` files. The stale `5142` is
hard-coded in `tools/sweep/gen_bug_reports.py`; it should be generated from the
current tier count. This is a documentation/counting defect, not a sanitizer
result.

## Checks run

- 113 focused semantics, physical-intent, zero-contract, symbol-contract and
  divisor regression tests passed.
- The embedded commands in all 26 confirmed-tier reports reproduced their
  published analyzer result.
- The embedded commands in all 911 latent reports reproduced their source
  census result.
- The refreshed OMC ledgers retain paired, source-instantiated evidence for the
  divisor and physical witnesses. See [divisor OMC evidence](omc-source-verification.md)
  and [physical OMC evidence](omc-physical-verification.md).

Passing the embedded command checks proves that the report is reproducible; it
does not by itself prove that its bug attribution is correct. The independent
OMC and source-contract adjudications determine the verification verdict.
