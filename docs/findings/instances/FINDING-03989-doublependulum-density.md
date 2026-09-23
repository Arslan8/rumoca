# FINDING-03989: `boxBody1.density` in `DoublePendulum`

| | |
|---|---|
| **Model** | `Modelica.Mechanics.MultiBody.Examples.Elementary.DoublePendulum` |
| **Reached as** | `boxBody1.density` |
| **Declaration** | `BodyBox.mo:37` |
| **Parameter** | `density` |
| **Claim** | the declaration explicitly permits zero (`min=0`) |
| **Kind** | `physical-bound-permits-zero` |
| **Severity** | low |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0151](../../site-reports/SITE-0151-density-physical-bound-permits-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | fluid |
| `rule` | fluid.density.positive |
| `rule_origin` | mass per volume of a real fluid; density appears as a divisor throughout the Fluid library |
| `rule_reference` |  |
| `required` | boxBody1.density > 0 |
| `declared_min` | 0.0 |
| `variable_role` | parameter |
| `note` | the declaration explicitly permits zero (`min=0`); whether zero is actually admissible needs execution, and for Mass/Inertia it is not |
| `matched_by` | {'quantity': 'Density', 'unit': 'kg/m3', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `BodyBox.mo:37` is reached by this model through
`boxBody1.density`, and the analysis reached it statically — no value has been observed
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
