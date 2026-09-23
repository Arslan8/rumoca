# FINDING-02934: `transformer1.L2sigma` in `Rectifier6pulse`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.Transformers.Rectifier6pulse` |
| **Reached as** | `transformer1.L2sigma` |
| **Declaration** | `PartialBasicTransformer.mo:30` |
| **Parameter** | `L2sigma` |
| **Claim** | nothing bounds this declaration at all |
| **Kind** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0114](../../site-reports/SITE-0114-l2sigma-physical-domain-unenforced.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | electrical |
| `rule` | elec.inductance.positive |
| `rule_origin` | stored energy is L*i^2/2; L = 0 turns the differential equation into a constraint on voltage |
| `rule_reference` | MSL Electrical.Analog.Basic.Inductor |
| `required` | transformer1.L2sigma > 0 |
| `declared_min` | None |
| `variable_role` | parameter |
| `note` | nothing bounds this declaration, so it permits values physics forbids |
| `matched_by` | {'quantity': 'Inductance', 'unit': 'H', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `PartialBasicTransformer.mo:30` is reached by this model through
`transformer1.L2sigma`, and the analysis reached it statically — no value has been observed
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
