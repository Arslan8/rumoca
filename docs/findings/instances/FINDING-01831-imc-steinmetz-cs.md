# FINDING-01831: `Cs` in `IMC_Steinmetz`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Steinmetz` |
| **Reached as** | `Cs` |
| **Declaration** | `IMC_Steinmetz.mo:12` |
| **Parameter** | `Cs` |
| **Claim** | the declaration explicitly permits zero (`min=0`) |
| **Kind** | `physical-bound-permits-zero` |
| **Severity** | low |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0617](../../site-reports/SITE-0617-cs-physical-bound-permits-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | electrical |
| `rule` | elec.capacitance.positive |
| `rule_origin` | stored energy is C*v^2/2, which a negative capacitance makes negative; C = 0 removes the state |
| `rule_reference` | MSL Electrical.Analog.Basic.Capacitor |
| `required` | Cs > 0 |
| `declared_min` | 0.0 |
| `variable_role` | parameter |
| `note` | the declaration explicitly permits zero (`min=0`); whether zero is actually admissible needs execution, and for Mass/Inertia it is not |
| `matched_by` | {'quantity': 'Capacitance', 'unit': 'F', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `IMC_Steinmetz.mo:12` is reached by this model through
`Cs`, and the analysis reached it statically — no value has been observed
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
