# FINDING-01653: `aimc.Lrsigma` in `IMC_Initialize`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Initialize` |
| **Reached as** | `aimc.Lrsigma` |
| **Declaration** | `IM_SquirrelCage.mo:29` |
| **Parameter** | `Lrsigma` |
| **Claim** | nothing bounds this declaration at all |
| **Kind** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0069](../../site-reports/SITE-0069-lrsigma-physical-domain-unenforced.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | electrical |
| `rule` | elec.inductance.positive |
| `rule_origin` | stored energy is L*i^2/2; L = 0 turns the differential equation into a constraint on voltage |
| `rule_reference` | MSL Electrical.Analog.Basic.Inductor |
| `required` | aimc.Lrsigma > 0 |
| `declared_min` | None |
| `variable_role` | parameter |
| `note` | nothing bounds this declaration, so it permits values physics forbids |
| `matched_by` | {'quantity': 'Inductance', 'unit': 'H', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `IM_SquirrelCage.mo:29` is reached by this model through
`aimc.Lrsigma`, and the analysis reached it statically — no value has been observed
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
