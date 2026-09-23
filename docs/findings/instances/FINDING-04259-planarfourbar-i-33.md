# FINDING-04259: `body1.body.I_33` in `PlanarFourbar`

| | |
|---|---|
| **Model** | `Modelica.Mechanics.MultiBody.Examples.Loops.PlanarFourbar` |
| **Reached as** | `body1.body.I_33` |
| **Declaration** | `Body.mo:21` |
| **Parameter** | `I_33` |
| **Claim** | the declaration explicitly permits zero (`min=0`) |
| **Kind** | `physical-bound-permits-zero` |
| **Severity** | low |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0036](../../site-reports/SITE-0036-i-33-physical-bound-permits-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | mechanical |
| `rule` | mech.inertia.positive |
| `rule_origin` | the rotational analogue of mass; J = 0 leaves angular acceleration undetermined |
| `rule_reference` | MSL Mechanics.Rotational.Components.Inertia |
| `required` | body1.body.I_33 > 0 |
| `declared_min` | 0.0 |
| `variable_role` | parameter |
| `note` | the declaration explicitly permits zero (`min=0`); whether zero is actually admissible needs execution, and for Mass/Inertia it is not |
| `matched_by` | {'quantity': 'MomentOfInertia', 'unit': 'kg.m2', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `Body.mo:21` is reached by this model through
`body1.body.I_33`, and the analysis reached it statically — no value has been observed
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
