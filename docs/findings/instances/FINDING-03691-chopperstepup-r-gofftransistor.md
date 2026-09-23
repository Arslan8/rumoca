# FINDING-03691: `chopperStepUp.GoffTransistor` in `ChopperStepUp_R`

| | |
|---|---|
| **Model** | `Modelica.Electrical.PowerConverters.Examples.DCDC.ChopperStepUp.ChopperStepUp_R` |
| **Reached as** | `chopperStepUp.GoffTransistor` |
| **Declaration** | `ChopperStepUp.mo:7` |
| **Parameter** | `GoffTransistor` |
| **Claim** | nothing bounds this declaration at all |
| **Kind** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0661](../../site-reports/SITE-0661-gofftransistor-physical-domain-unenforced.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | electrical |
| `rule` | elec.conductance.positive |
| `rule_origin` | the reciprocal of a passive resistance |
| `rule_reference` |  |
| `required` | chopperStepUp.GoffTransistor > 0 |
| `declared_min` | None |
| `variable_role` | parameter |
| `note` | nothing bounds this declaration, so it permits values physics forbids |
| `matched_by` | {'quantity': 'Conductance', 'unit': 'S', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `ChopperStepUp.mo:7` is reached by this model through
`chopperStepUp.GoffTransistor`, and the analysis reached it statically — no value has been observed
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
