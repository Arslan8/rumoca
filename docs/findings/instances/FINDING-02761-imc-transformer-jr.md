# FINDING-02761: `aimcData.Jr` in `IMC_Transformer`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer` |
| **Reached as** | `aimcData.Jr` |
| **Declaration** | `InductionMachineData.mo:6` |
| **Parameter** | `Jr` |
| **Claim** | nothing bounds this declaration at all |
| **Kind** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0025](../../site-reports/SITE-0025-jr-physical-domain-unenforced.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | mechanical |
| `rule` | mech.inertia.positive |
| `rule_origin` | the rotational analogue of mass; J = 0 leaves angular acceleration undetermined |
| `rule_reference` | MSL Mechanics.Rotational.Components.Inertia |
| `required` | aimcData.Jr > 0 |
| `declared_min` | None |
| `variable_role` | parameter |
| `note` | nothing bounds this declaration, so it permits values physics forbids |
| `matched_by` | {'quantity': 'MomentOfInertia', 'unit': 'kg.m2', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `InductionMachineData.mo:6` is reached by this model through
`aimcData.Jr`, and the analysis reached it statically — no value has been observed
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
