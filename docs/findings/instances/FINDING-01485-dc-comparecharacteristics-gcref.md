# FINDING-01485: `dcee.coreParameters.GcRef` in `DC_CompareCharacteristics`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics` |
| **Reached as** | `dcee.coreParameters.GcRef` |
| **Declaration** | `CoreParameters.mo:18` |
| **Parameter** | `GcRef` |
| **Claim** | the declared value is outside the physical domain |
| **Kind** | `physical-invariant-violated` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0010](../../site-reports/SITE-0010-gcref-physical-invariant-violated.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | electrical |
| `rule` | elec.conductance.positive |
| `rule_origin` | the reciprocal of a passive resistance |
| `rule_reference` |  |
| `observed` | 0.0 |
| `required` | dcee.coreParameters.GcRef > 0 |
| `where` | declaration |
| `matched_by` | {'quantity': 'Conductance', 'unit': 'S', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `CoreParameters.mo:18` is reached by this model through
`dcee.coreParameters.GcRef`, and the analysis reached it statically — no value has been observed
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
