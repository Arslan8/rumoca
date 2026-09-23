# v2 report verification

This review accounts for **all 6,440 report instances** in `docs/v2/bugs`. The input mixes defect candidates with explicit supported-limit, guarded, unreachable, translation-generated and unresolved records; those are not all bugs.

| Verdict | Reports | Browse |
|---|---:|---|
| Execution-confirmed defect | 830 | [Verified reports](confirmed.md) |
| Static/source-supported candidate | 44 | [Candidates](candidates.md) |
| Intent question / advisory — no defect claimed | 638 | [Advisories](advisories.md) |
| False positive or explicit non-defect | 3373 | [Reasons](false-positives.md) |
| Unresolved — not called real or fake | 1555 | [Evidence gaps](unresolved.md) |
| Total | 6440 | [CSV](index.csv) · [JSON](index.json) |

Counts are report instances, not unique root causes. A repeated shared declaration may appear in many models.

[Divisor OMC evidence](omc-source-verification.md) · [Physical-witness OMC evidence](omc-physical-verification.md)
· [Current rerun audit and residual issues](current-rerun-audit.md)

## Important findings

- The current v2 analyzers explicitly identify 2018 supported-zero records, 122 assertion-guarded divisions, 121 unreachable divisions and 41 translation-introduced quotients. These are non-defects, not bugs.
- The analyzer retains 638 quantity-based anomalies as explicit intent questions. They preserve recall without asserting that a negative/zero value or permissive declaration is erroneous before a component contract or user assumption establishes that premise.
- Of 1520 source-denominator candidates, OpenModelica independently reproduced 817 report instances against clean baselines. It rejected 284 exact witnesses as illegal/protected; non-reproductions, baseline failures, timeouts, unsupported array modifiers and other failures remain unresolved.
- Of the current physical defect claims, 34 have paired OpenModelica witness results. The broader retained physical-witness ledger exercised 177 pre-policy report instances. These tests decide whether zero/negative values translate and execute, while the intended physical domain still comes from the component-specific source contract.
- The original 26 runtime `BUG-*` claims remain **11 confirmed and 15 refuted** under the independent translation and initialization controls retained in the earlier audit.
- Machine-winding resistance reports are left unresolved pending the corrected component-scoped `R >= 0` policy: generic `Basic.Resistor` is signed, while negative copper resistance is not ordinarily physical.

## Verification performed

- Reviewed every v2 finding kind and its claimed evidence semantics.
- Checked all reported source arithmetic sites: 270 of 276 unique SAT source locations contain a division on the cited line; the remaining six are multiline expressions whose division continues on adjacent lines.
- Reused the exact stable-ID review for all 26 BUG reports and 911 declaration census entries.
- Reused model/target source-semantic adjudications from the first exhaustive audit where the v2 physical claim matched uniquely.
- Re-ran the verification commands embedded in all 26 confirmed-tier reports and all 911 latent-tier reports; all reproduced their published analyzer/source result.
- Ran the combined semantics, physical-policy, zero-contract, symbol-contract and divisor regression suite: 113 tests passed.

## Limitations

- A clean short OMC run is recorded as unresolved, not as proof that a later conditional path can never execute.
- Declaration-only physical-policy claims remain unresolved unless a reviewed component contract establishes or refutes them.
- An advisory is not counted as a verified bug, candidate bug, false positive or unresolved bug; it is an intentional request for missing author intent.
- Four `divisor-zero-at-declared-values` results remain unresolved because a static broken-baseline claim needs independent execution and conditional-path review.
- No library or analyzer implementation was changed by this audit.

## Reproduce

```sh
python3 docs/v2/verified/omc_source_verify.py --jobs 4 --timeout 240
python3 docs/v2/verified/omc_physical_verify.py --jobs 4 --timeout 240
python3 docs/v2/verified/build_reports.py
python3 -m pytest -q packages/modelsan/tests/test_symbol_contract.py packages/modelsan/tests/test_divisor_reasoning.py
python3 -m pytest -q packages/modelsan/tests/test_physical.py packages/modelsan/tests/test_divisor_witness.py packages/modelsan/tests/test_divisor.py
```

[Input overview](../bugs/README.md) · [Earlier exhaustive audit](../../verifiedBugs/README.md) · [Validation](validation.json)
