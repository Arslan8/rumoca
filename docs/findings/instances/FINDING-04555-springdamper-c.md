# FINDING-04555: `springDamper.c` in `SpringDamper`

| | |
|---|---|
| **Model** | `Modelica.Mechanics.Translational.Examples.Utilities.SpringDamper` |
| **Reached as** | `springDamper.c` |
| **Declaration** | `SpringDamperNoRelativeStates.mo:4` |
| **Parameter** | `c` |
| **Claim** | the declaration explicitly permits zero (`min=0`) |
| **Kind** | `physical-bound-permits-zero` |
| **Severity** | low |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0132](../../site-reports/SITE-0132-c-physical-bound-permits-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | mechanical |
| `rule` | mech.stiffness.positive |
| `rule_origin` | a spring with c <= 0 does not restore; c = 0 removes the constraint the component exists to impose |
| `rule_reference` |  |
| `required` | springDamper.c > 0 |
| `declared_min` | 0.0 |
| `variable_role` | parameter |
| `note` | the declaration explicitly permits zero (`min=0`); whether zero is actually admissible needs execution, and for Mass/Inertia it is not |
| `matched_by` | {'quantity': 'TranslationalSpringConstant', 'unit': 'N/m', 'confidence': 'QUANTITY'} |

## What this is

One occurrence. The declaration at `SpringDamperNoRelativeStates.mo:4` is reached by this model through
`springDamper.c`, and the analysis reached it statically — no value has been observed
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
