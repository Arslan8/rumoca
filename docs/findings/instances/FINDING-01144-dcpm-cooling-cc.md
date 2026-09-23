# FINDING-01144: `Cc` in `DCPM_Cooling`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Cooling` |
| **Reached as** | `Cc` |
| **Declaration** | `DCPM_Cooling.mo:15` |
| **Parameter** | `Cc` |
| **Claim** | nothing bounds this declaration at all |
| **Kind** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0680](../../site-reports/SITE-0680-cc-physical-domain-unenforced.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | thermal |
| `rule` | thermal.heat_capacity.positive |
| `rule_origin` | C*dT = dQ; a non-positive heat capacity makes a body cool when heated |
| `rule_reference` |  |
| `required` | Cc > 0 |
| `declared_min` | None |
| `variable_role` | parameter |
| `note` | nothing bounds this declaration, so it permits values physics forbids |
| `matched_by` | {'quantity': 'HeatCapacity', 'unit': 'J/K', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `DCPM_Cooling.mo:15` is reached by this model through
`Cc`, and the analysis reached it statically — no value has been observed
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
