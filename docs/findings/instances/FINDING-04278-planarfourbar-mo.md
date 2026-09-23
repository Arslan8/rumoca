# FINDING-04278: `body4.mo` in `PlanarFourbar`

| | |
|---|---|
| **Model** | `Modelica.Mechanics.MultiBody.Examples.Loops.PlanarFourbar` |
| **Reached as** | `body4.mo` |
| **Declaration** | `BodyBox.mo:101` |
| **Parameter** | `mo` |
| **Claim** | the declaration explicitly permits zero (`min=0`) |
| **Kind** | `physical-bound-permits-zero` |
| **Severity** | low |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0148](../../site-reports/SITE-0148-mo-physical-bound-permits-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | mechanical |
| `rule` | mech.mass.positive |
| `rule_origin` | m*a = f determines acceleration only for m > 0; negative mass is not a physical body |
| `rule_reference` | MSL Mechanics.Translational.Components.Mass |
| `required` | body4.mo > 0 |
| `declared_min` | 0.0 |
| `variable_role` | parameter |
| `note` | the declaration explicitly permits zero (`min=0`); whether zero is actually admissible needs execution, and for Mass/Inertia it is not |
| `matched_by` | {'quantity': 'Mass', 'unit': 'kg', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `BodyBox.mo:101` is reached by this model through
`body4.mo`, and the analysis reached it statically — no value has been observed
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
