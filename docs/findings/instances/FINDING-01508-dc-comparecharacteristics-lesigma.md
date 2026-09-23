# FINDING-01508: `dcse.Lesigma` in `DC_CompareCharacteristics`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics` |
| **Reached as** | `dcse.Lesigma` |
| **Declaration** | `DC_SeriesExcited.mo:86` |
| **Parameter** | `Lesigma` |
| **Claim** | the declared value is outside the physical domain |
| **Kind** | `physical-invariant-violated` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0225](../../site-reports/SITE-0225-lesigma-physical-invariant-violated.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | electrical |
| `rule` | elec.inductance.positive |
| `rule_origin` | stored energy is L*i^2/2; L = 0 turns the differential equation into a constraint on voltage |
| `rule_reference` | MSL Electrical.Analog.Basic.Inductor |
| `observed` | 0.0 |
| `required` | dcse.Lesigma > 0 |
| `where` | declaration |
| `matched_by` | {'quantity': 'Inductance', 'unit': 'H', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `DC_SeriesExcited.mo:86` is reached by this model through
`dcse.Lesigma`, and the analysis reached it statically — no value has been observed
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
