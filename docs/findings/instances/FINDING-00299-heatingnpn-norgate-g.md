# FINDING-00299: `TC1.G` in `HeatingNPN_NORGate`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Analog.Examples.HeatingNPN_NORGate` |
| **Reached as** | `TC1.G` |
| **Declaration** | `ThermalConductor.mo:5` |
| **Parameter** | `G` |
| **Claim** | nothing bounds this declaration at all |
| **Kind** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0054](../../site-reports/SITE-0054-g-physical-domain-unenforced.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | thermal |
| `rule` | thermal.conductance.positive |
| `rule_origin` | heat flows from hot to cold; G <= 0 reverses the second law |
| `rule_reference` |  |
| `required` | TC1.G > 0 |
| `declared_min` | None |
| `variable_role` | parameter |
| `note` | nothing bounds this declaration, so it permits values physics forbids |
| `matched_by` | {'quantity': 'ThermalConductance', 'unit': 'W/K', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `ThermalConductor.mo:5` is reached by this model through
`TC1.G`, and the analysis reached it statically — no value has been observed
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
