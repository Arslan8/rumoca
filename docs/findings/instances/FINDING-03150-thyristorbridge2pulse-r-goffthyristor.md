# FINDING-03150: `rectifier.GoffThyristor` in `ThyristorBridge2Pulse_R`

| | |
|---|---|
| **Model** | `Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2Pulse.ThyristorBridge2Pulse_R` |
| **Reached as** | `rectifier.GoffThyristor` |
| **Declaration** | `ThyristorBridge2Pulse.mo:7` |
| **Parameter** | `GoffThyristor` |
| **Claim** | the declaration explicitly permits zero (`min=0`) |
| **Kind** | `physical-bound-permits-zero` |
| **Severity** | low |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0134](../../site-reports/SITE-0134-goffthyristor-physical-bound-permits-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | electrical |
| `rule` | elec.conductance.positive |
| `rule_origin` | the reciprocal of a passive resistance |
| `rule_reference` |  |
| `required` | rectifier.GoffThyristor > 0 |
| `declared_min` | 0.0 |
| `variable_role` | parameter |
| `note` | the declaration explicitly permits zero (`min=0`); whether zero is actually admissible needs execution, and for Mass/Inertia it is not |
| `matched_by` | {'quantity': 'Conductance', 'unit': 'S', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `ThyristorBridge2Pulse.mo:7` is reached by this model through
`rectifier.GoffThyristor`, and the analysis reached it statically — no value has been observed
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
