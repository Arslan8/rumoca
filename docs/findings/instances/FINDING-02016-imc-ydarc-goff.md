# FINDING-02016: `switchYDwithArc.idealCloser.Goff` in `IMC_YDarc`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc` |
| **Reached as** | `switchYDwithArc.idealCloser.Goff` |
| **Declaration** | `CloserWithArc.mo:6` |
| **Parameter** | `Goff` |
| **Claim** | nothing bounds this declaration at all |
| **Kind** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0663](../../site-reports/SITE-0663-goff-physical-domain-unenforced.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | electrical |
| `rule` | elec.conductance.positive |
| `rule_origin` | the reciprocal of a passive resistance |
| `rule_reference` |  |
| `required` | switchYDwithArc.idealCloser.Goff > 0 |
| `declared_min` | None |
| `variable_role` | parameter |
| `note` | nothing bounds this declaration, so it permits values physics forbids |
| `matched_by` | {'quantity': 'Conductance', 'unit': 'S', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `CloserWithArc.mo:6` is reached by this model through
`switchYDwithArc.idealCloser.Goff`, and the analysis reached it statically — no value has been observed
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
