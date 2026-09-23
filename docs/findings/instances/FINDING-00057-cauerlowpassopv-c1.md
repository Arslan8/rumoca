# FINDING-00057: `c1` in `CauerLowPassOPV`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Analog.Examples.CauerLowPassOPV` |
| **Reached as** | `c1` |
| **Declaration** | `CauerLowPassOPV.mo:7` |
| **Parameter** | `c1` |
| **Claim** | the declaration explicitly permits zero (`min=0`) |
| **Kind** | `physical-bound-permits-zero` |
| **Severity** | low |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0578](../../site-reports/SITE-0578-c1-physical-bound-permits-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | electrical |
| `rule` | elec.capacitance.positive |
| `rule_origin` | stored energy is C*v^2/2, which a negative capacitance makes negative; C = 0 removes the state |
| `rule_reference` | MSL Electrical.Analog.Basic.Capacitor |
| `required` | c1 > 0 |
| `declared_min` | 0.0 |
| `variable_role` | parameter |
| `note` | the declaration explicitly permits zero (`min=0`); whether zero is actually admissible needs execution, and for Mass/Inertia it is not |
| `matched_by` | {'quantity': 'Capacitance', 'unit': 'F', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `CauerLowPassOPV.mo:7` is reached by this model through
`c1`, and the analysis reached it statically — no value has been observed
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
