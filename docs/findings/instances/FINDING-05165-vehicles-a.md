# FINDING-05165: `vehicleInclination.A` in `Vehicles`

| | |
|---|---|
| **Model** | `ModelicaTest.Translational.Vehicles` |
| **Reached as** | `vehicleInclination.A` |
| **Declaration** | `Vehicle.mo:7` |
| **Parameter** | `A` |
| **Claim** | the declared value is outside the physical domain |
| **Kind** | `physical-invariant-violated` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0886](../../site-reports/SITE-0886-a-physical-invariant-violated.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | fluid |
| `rule` | fluid.area.positive |
| `rule_origin` | a flow cross-section is a divisor in every velocity relation; zero area admits no flow and divides by zero |
| `rule_reference` |  |
| `observed` | 0.0 |
| `required` | vehicleInclination.A > 0 |
| `where` | declaration |
| `matched_by` | {'quantity': 'Area', 'unit': 'm2', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `Vehicle.mo:7` is reached by this model through
`vehicleInclination.A`, and the analysis reached it statically — no value has been observed
breaking anything here.

The fix is at the declaration, not in this model. Other models reaching the same
declaration are separate files; the fix site groups them.

| Tier | Evidence | Where |
|---|---|---|
| confirmed | fails in two independent tools | [`INSTANCES.md`](../../verified%20bugs/INSTANCES.md) |
| **candidate** | **static analysis reached it** | **here** |
| latent | a declaration permits it | [`declaration-sites/`](../../declaration-sites/README.md) |

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
