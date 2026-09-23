# FINDING-04733: `heatCapacitor1.C` in `TwoMass`

| | |
|---|---|
| **Model** | `Modelica.Thermal.FluidHeatFlow.Examples.TwoMass` |
| **Reached as** | `heatCapacitor1.C` |
| **Declaration** | `HeatCapacitor.mo:3` |
| **Parameter** | `C` |
| **Claim** | nothing bounds this declaration at all |
| **Kind** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0014](../../site-reports/SITE-0014-c-physical-domain-unenforced.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | thermal |
| `rule` | thermal.heat_capacity.positive |
| `rule_origin` | C*dT = dQ; a non-positive heat capacity makes a body cool when heated |
| `rule_reference` |  |
| `required` | heatCapacitor1.C > 0 |
| `declared_min` | None |
| `variable_role` | parameter |
| `note` | nothing bounds this declaration, so it permits values physics forbids |
| `matched_by` | {'quantity': 'HeatCapacity', 'unit': 'J/K', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `HeatCapacitor.mo:3` is reached by this model through
`heatCapacitor1.C`, and the analysis reached it statically — no value has been observed
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
