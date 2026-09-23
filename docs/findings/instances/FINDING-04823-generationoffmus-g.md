# FINDING-04823: `conductor.G` in `GenerationOfFMUs`

| | |
|---|---|
| **Model** | `Modelica.Thermal.HeatTransfer.Examples.GenerationOfFMUs` |
| **Reached as** | `conductor.G` |
| **Declaration** | `Conduction.mo:4` |
| **Parameter** | `G` |
| **Claim** | nothing bounds this declaration at all |
| **Kind** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0303](../../site-reports/SITE-0303-g-physical-domain-unenforced.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | thermal |
| `rule` | thermal.conductance.positive |
| `rule_origin` | heat flows from hot to cold; G <= 0 reverses the second law |
| `rule_reference` |  |
| `required` | conductor.G > 0 |
| `declared_min` | None |
| `variable_role` | parameter |
| `note` | nothing bounds this declaration, so it permits values physics forbids |
| `matched_by` | {'quantity': 'ThermalConductance', 'unit': 'W/K', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `Conduction.mo:4` is reached by this model through
`conductor.G`, and the analysis reached it statically — no value has been observed
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
