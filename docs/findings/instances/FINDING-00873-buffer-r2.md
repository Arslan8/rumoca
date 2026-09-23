# FINDING-00873: `R2` in `Buffer`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.Buffer` |
| **Reached as** | `R2` |
| **Declaration** | `Buffer.mo:6` |
| **Parameter** | `R2` |
| **Claim** | the declared value is outside the physical domain |
| **Kind** | `physical-invariant-violated` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0884](../../site-reports/SITE-0884-r2-physical-invariant-violated.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | electrical |
| `rule` | elec.resistance.positive |
| `rule_origin` | a passive resistor dissipates energy; R <= 0 would make it a source, and R = 0 removes the equation that determines its current |
| `rule_reference` | MSL Electrical.Analog.Basic.Resistor |
| `observed` | 0.0 |
| `required` | R2 > 0 |
| `where` | declaration |
| `matched_by` | {'quantity': 'Resistance', 'unit': 'Ohm', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `Buffer.mo:6` is reached by this model through
`R2`, and the analysis reached it statically — no value has been observed
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
