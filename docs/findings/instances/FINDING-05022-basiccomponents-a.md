# FINDING-05022: `eddyCurrent.A` in `BasicComponents`

| | |
|---|---|
| **Model** | `ModelicaTest.Magnetic.FluxTubes.BasicComponents` |
| **Reached as** | `eddyCurrent.A` |
| **Declaration** | `EddyCurrent.mo:20` |
| **Parameter** | `A` |
| **Claim** | nothing bounds this declaration at all |
| **Kind** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0707](../../site-reports/SITE-0707-a-physical-domain-unenforced.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | fluid |
| `rule` | fluid.area.positive |
| `rule_origin` | a flow cross-section is a divisor in every velocity relation; zero area admits no flow and divides by zero |
| `rule_reference` |  |
| `required` | eddyCurrent.A > 0 |
| `declared_min` | None |
| `variable_role` | parameter |
| `note` | nothing bounds this declaration, so it permits values physics forbids |
| `matched_by` | {'quantity': 'Area', 'unit': 'm2', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `EddyCurrent.mo:20` is reached by this model through
`eddyCurrent.A`, and the analysis reached it statically — no value has been observed
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
