# FINDING-04385: `b1.m` in `MechanicalStructure`

| | |
|---|---|
| **Model** | `Modelica.Mechanics.MultiBody.Examples.Systems.RobotR3.Utilities.MechanicalStructure` |
| **Reached as** | `b1.m` |
| **Declaration** | `BodyShape.mo:23` |
| **Parameter** | `m` |
| **Claim** | the declaration explicitly permits zero (`min=0`) |
| **Kind** | `physical-bound-permits-zero` |
| **Severity** | low |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0183](../../site-reports/SITE-0183-m-physical-bound-permits-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | mechanical |
| `rule` | mech.mass.positive |
| `rule_origin` | m*a = f determines acceleration only for m > 0; negative mass is not a physical body |
| `rule_reference` | MSL Mechanics.Translational.Components.Mass |
| `required` | b1.m > 0 |
| `declared_min` | 0.0 |
| `variable_role` | parameter |
| `note` | the declaration explicitly permits zero (`min=0`); whether zero is actually admissible needs execution, and for Mass/Inertia it is not |
| `matched_by` | {'quantity': 'Mass', 'unit': 'kg', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `BodyShape.mo:23` is reached by this model through
`b1.m`, and the analysis reached it statically — no value has been observed
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
