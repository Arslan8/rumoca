# FINDING-03431: `L` in `ThyristorCenterTap2Pulse_RLV_Characteristic`

| | |
|---|---|
| **Model** | `Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierCenterTap2Pulse.ThyristorCenterTap2Pulse_RLV_Characteristic` |
| **Reached as** | `L` |
| **Declaration** | `ThyristorCenterTap2Pulse_RLV_Characteristic.mo:9` |
| **Parameter** | `L` |
| **Claim** | nothing bounds this declaration at all |
| **Kind** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0852](../../site-reports/SITE-0852-l-physical-domain-unenforced.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | electrical |
| `rule` | elec.inductance.positive |
| `rule_origin` | stored energy is L*i^2/2; L = 0 turns the differential equation into a constraint on voltage |
| `rule_reference` | MSL Electrical.Analog.Basic.Inductor |
| `required` | L > 0 |
| `declared_min` | None |
| `variable_role` | parameter |
| `note` | nothing bounds this declaration, so it permits values physics forbids |
| `matched_by` | {'quantity': 'Inductance', 'unit': 'H', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `ThyristorCenterTap2Pulse_RLV_Characteristic.mo:9` is reached by this model through
`L`, and the analysis reached it statically — no value has been observed
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
