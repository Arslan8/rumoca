# FINDING-03443: `rectifier.diode_p.idealDiode[2].Ron` in `DiodeCenterTap2mPulse`

| | |
|---|---|
| **Model** | `Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierCenterTap2mPulse.DiodeCenterTap2mPulse` |
| **Reached as** | `rectifier.diode_p.idealDiode[2].Ron` |
| **Declaration** | `IdealSemiconductor.mo:4` |
| **Parameter** | `Ron` |
| **Claim** | the declaration explicitly permits zero (`min=0`) |
| **Kind** | `physical-bound-permits-zero` |
| **Severity** | low |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0002](../../site-reports/SITE-0002-ron-physical-bound-permits-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | electrical |
| `rule` | elec.resistance.positive |
| `rule_origin` | a passive resistor dissipates energy; R <= 0 would make it a source, and R = 0 removes the equation that determines its current |
| `rule_reference` | MSL Electrical.Analog.Basic.Resistor |
| `required` | rectifier.diode_p.idealDiode[2].Ron > 0 |
| `declared_min` | 0.0 |
| `variable_role` | parameter |
| `note` | the declaration explicitly permits zero (`min=0`); whether zero is actually admissible needs execution, and for Mass/Inertia it is not |
| `matched_by` | {'quantity': 'Resistance', 'unit': 'Ohm', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `IdealSemiconductor.mo:4` is reached by this model through
`rectifier.diode_p.idealDiode[2].Ron`, and the analysis reached it statically — no value has been observed
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
