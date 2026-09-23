# FINDING-02685: `smr.Rrd` in `SMR_Inverter`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter` |
| **Reached as** | `smr.Rrd` |
| **Declaration** | `SM_ReluctanceRotor.mo:62` |
| **Parameter** | `Rrd` |
| **Claim** | nothing bounds this declaration at all |
| **Kind** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0352](../../site-reports/SITE-0352-rrd-physical-domain-unenforced.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | electrical |
| `rule` | elec.resistance.positive |
| `rule_origin` | a passive resistor dissipates energy; R <= 0 would make it a source, and R = 0 removes the equation that determines its current |
| `rule_reference` | MSL Electrical.Analog.Basic.Resistor |
| `required` | smr.Rrd > 0 |
| `declared_min` | None |
| `variable_role` | parameter |
| `note` | nothing bounds this declaration, so it permits values physics forbids |
| `matched_by` | {'quantity': 'Resistance', 'unit': 'Ohm', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `SM_ReluctanceRotor.mo:62` is reached by this model through
`smr.Rrd`, and the analysis reached it statically — no value has been observed
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
