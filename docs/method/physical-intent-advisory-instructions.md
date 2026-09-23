# Student instructions: preserve physical issues without guessing intent

## Goal

Fix PhysicalSan's confidence policy without losing legitimate findings.

A negative resistance, mass-like value, or other unusual sign should remain
visible when the analyzer only has a quantity/unit heuristic. It must be phrased
as a question to the programmer, not as an error:

> Negative resistance is unusual for this uncatalogued component. Is this
> intentional? Add a component contract or assumption to declare the intended
> signed domain.

Do **not** solve the false-positive problem by suppressing every unknown case.
That would improve apparent precision by destroying recall. Preserve the signal
as a non-blocking advisory and promote it only when stronger evidence establishes
the premise.

## The distinction the implementation must carry

The analyzer needs two independent facts:

1. **Predicate:** for example, `R > 0`.
2. **Authority for applying it here:** an explicit passive-resistor contract,
   a user assumption, or merely the fact that the value has unit `Ohm`.

An SI quantity identifies what kind of value this is. It does not identify the
component's purpose. `SI.Resistance` can describe a passive resistor, an active
negative impedance, a linearized incremental model, an optimization variable,
or a fault-injection input. Without the component premise, the analyzer does not
know the programmer's intention.

Carry an explicit premise state through the analysis and finding:

| Premise state | Meaning | Required result |
|---|---|---|
| `ESTABLISHED` | component/delegated contract or user assumption applies | enforce the predicate |
| `REFUTED` | authoritative component contract permits the value | no violation; optional non-defect audit record |
| `UNKNOWN` | only quantity, unit, name, or generic heuristic matched | non-blocking advisory question |

Do not encode these states only as severity. The JSON/IR must retain the state,
authority, matched role, canonical declaration, and provenance so later stages
cannot accidentally turn an advisory back into an error.

## Authority order

Use the following order. Lower authorities cannot contradict higher ones.

1. Intent-independent source facts, such as an active denominator that becomes
   zero. These cannot be waived by a physical assumption.
2. Source declaration/type bounds and assertions.
3. Explicit user assumptions. The programmer is supplying missing application
   intent; report conflicts with source facts rather than silently overriding
   them.
4. Component and delegated-component contracts, including contracts inherited
   through arrays/wrappers.
5. Quantity and unit matching.
6. Name heuristics, which remain opt-in.

The required rule for this change is simple: **component semantics override a
generic physical heuristic**. A catalogued signed resistor must not inherit a
generic `Resistance > 0` verdict. An uncatalogued resistance remains visible,
but only as an intent question.

## Required finding policy

| Evidence and observation | Kind / severity | Blocking? |
|---|---|---|
| established contract is violated by an observed/default value | contract violation, high | yes |
| established contract is not enforced by the declaration | contract-gap candidate, medium | no until independently confirmed |
| unknown premise and suspicious value or permissive declaration | intent advisory, low | no |
| authoritative contract permits the value | non-defect/info or suppress normal output | no |
| executable arithmetic fails independently | numerical defect, high | yes |

For compatibility, the existing
`physical-invariant-violated-by-quantity-alone` kind may be retained, but it
must carry `premise=UNKNOWN`, low severity, advisory wording, and non-blocking
status. A clearer new name such as `physical-intent-question` is acceptable if
all report generators and consumers are migrated together.

An advisory-only run must exit successfully. Advisories must not enter the
confirmed-bug count or be described as “physics forbids this value.” They should
say the value is unusual under a fallback heuristic and ask whether it was
intended.

## Implementation steps

1. In `packages/modelsan/modelsan/physical/rules.py`, make the result of rule
   matching expose whether a confirming role established the premise, an
   excluded role refuted it, or the match fell back to quantity/unit metadata.
   Do not return `None` for the unknown fallback: that would lose recall.
2. In `packages/modelsan/modelsan/physical/engine.py`, copy premise state and
   authority into every `PhysicalInvariant`. Keep the provenance when the
   invariant is deferred or classified as an unenforced declaration.
3. In `packages/modelsan/modelsan/sanitizers/physical.py`, apply the same premise
   classification to both paths:
   - an already-observed/default value that violates a predicate;
   - a declaration whose bounds permit a future violating value.

   The first path already distinguishes established roles from quantity-only
   matches. The `unbounded()` path is the important remaining trap: it currently
   can describe an unknown quantity match as a medium-severity domain defect.
   Change that unknown case to a low advisory without removing it.
4. Resolve zero/sign contracts before applying the generic rule. `ALLOWED`
   refutes the generic sign premise; `ALGEBRAIC_LIMIT` and `FEATURE_DISABLED`
   excuse exactly zero, not arbitrary negative values.
5. Preserve qualified component type and canonical declaration through wrapper
   and array instances. Otherwise the analyzer will forget that a polyphase
   resistor delegates to a signed scalar resistor.
6. Update JSON and text reporting so an advisory contains:
   `premise_state`, `authority`, `semantic_role`, `contract_source`, the observed
   value or permissive bound, and the user-facing intent question.
7. Ensure downstream report generation and paper-evaluation scripts count
   advisories separately from bugs, false positives, and unresolved results.

## Regression tests: do not lose legitimate issues

### Unknown intent must remain visible

Add synthetic uncatalogued variables carrying `quantity="Resistance"` and unit
`Ohm` with a negative value and with no lower bound. Each must produce exactly
one low-severity, non-blocking advisory with `premise_state=UNKNOWN`. It must not
produce zero findings, and it must not produce a contract violation.

Repeat this for an uncatalogued mass-like parameter so the behavior is not
special-cased to electrical names.

### Explicit contracts must still enforce real restrictions

- A synthetic component explicitly bound as a passive resistance with `R=-1`
  must produce a high-severity violation with `premise_state=ESTABLISHED`.
- A machine-winding resistance must allow `R=0` and reject `R<0`.
- A user assumption `sign_domain="nonnegative"` must promote a negative value
  from advisory to established violation.
- A user assumption `sign_domain="signed"` must refute the generic positive
  heuristic, while any contradictory source assertion is still reported.

### Existing false positives must remain fixed

Use these reviewed cases as regression fixtures:

| Case | Expected result |
|---|---|
| `Modelica.Electrical.Analog.Basic.Resistor.R` negative | no positivity violation; its component contract is signed |
| Chua circuit `Nr.Ga < 0` | no passive-conductance error; the negative slope is the device |
| `SwitchedCapacitor.R=-1` | no sign error; the component explicitly supports either sign |
| polyphase resistor negative element | inherit the scalar signed contract |
| machine winding `R=0` | accepted ideal lossless limit |
| negative off-diagonal inertia entry | evaluate the assembled tensor, not a scalar positivity rule |
| `Basic.Inductor.L=0` | accepted algebraic ideal-short limit |

The reviewed source sets are linked from:

- [`signed-electrical-element`](../v2/verified/groups/false-positives-signed-electrical-element.md)
- [`signed-polyphase-element`](../v2/verified/groups/false-positives-signed-polyphase-element.md)
- [`signed-inertia-tensor`](../v2/verified/groups/false-positives-signed-inertia-tensor.md)
- [`physical-zero-is-a-supported-limit`](../v2/verified/groups/false-positives-physical-zero-is-a-supported-limit.md)

### Independently confirmed defects must not be downgraded

The intent policy applies only to heuristic physical claims. It must not hide an
independent mathematical failure:

| Case | Required result |
|---|---|
| [`LCOscillator.C=0`](../v2/verified/confirmed/FINDING-00925.md) | remain confirmed: OMC reports division by zero in `C*R` |
| [`Multivibrator.R2=-1`](../v2/verified/confirmed/FINDING-00955.md) | remain confirmed: OMC reports an invalid logarithm argument |
| `SwitchedRLC.R=0` | remain a divide-by-zero defect |
| `Tank.resistance=0` and `Tank.area=0` | remain divide-by-zero defects |

Also retain the divisor regressions in
[`divide-by-zero-analysis.md`](divide-by-zero-analysis.md). A physical contract
must never suppress a proven active zero denominator.

## Tests to change or add

- Update `packages/modelsan/tests/test_semantics.py`: an unknown semantic-rule
  fallback must still match, but its policy result is low/advisory rather than
  medium/error. Keep the established-role and excluded-role assertions.
- Extend `packages/modelsan/tests/test_physical.py` to cover both observed-value
  and unenforced-declaration paths for all three premise states.
- Extend `packages/modelsan/tests/test_aggregate_and_sign.py` for winding zero,
  winding negative, signed scalar/wrapper resistance, and unknown resistance.
- Retain `packages/modelsan/tests/test_zero_contracts.py` to prove that a
  zero-only contract does not excuse a negative value.
- Add a reporting/CLI test proving an advisory-only result exits zero and is not
  counted as a confirmed bug.

## Required rerun after implementation

Baseline before this policy change: the focused command below completed with
**94 passed** on 2026-09-17. The post-change suite should contain additional
advisory/exit-status cases, so its test count must not fall below 94 without a
documented test replacement.

Run the focused tests first:

```sh
python3 -m pytest -q \
  packages/modelsan/tests/test_semantics.py \
  packages/modelsan/tests/test_physical.py \
  packages/modelsan/tests/test_aggregate_and_sign.py \
  packages/modelsan/tests/test_zero_contracts.py \
  packages/modelsan/tests/test_symbol_contract.py \
  packages/modelsan/tests/test_divisor_reasoning.py \
  packages/modelsan/tests/test_divisor_witness.py
```

Then rerun the corpus analysis; do not compare only the total finding count:

```sh
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out docs/runs/data/STATIC_INTENT_POLICY.jsonl --keep-parameter-chains
python3 tools/sweep/adjudicate.py docs/runs/data/STATIC_INTENT_POLICY.jsonl
```

Finally rerun the independent OMC controls and rebuild the v2 ledger:

```sh
python3 docs/v2/verified/omc_source_verify.py --jobs 4 --timeout 240
python3 docs/v2/verified/omc_physical_verify.py --jobs 4 --timeout 240
python3 docs/v2/verified/build_reports.py
```

## Acceptance gates

The change is complete only when all of these hold:

1. Unknown physical intent produces an advisory rather than silence or error.
2. Explicit positive/nonnegative contracts still catch violations.
3. Explicit signed/zero-limit contracts override generic heuristics.
4. Advisory-only runs are non-blocking and excluded from confirmed-bug counts.
5. All previously confirmed numerical cases remain confirmed.
6. Every downgraded result records which missing premise prevented an error.
7. The complete focused suite, corpus sweep, and OMC verification are rerun;
   report-count changes are explained by category, not celebrated merely because
   the total became smaller.
