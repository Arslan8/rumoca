# FINDING-00041: `C1.C` in `CauerLowPassOPV`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Analog.Examples.CauerLowPassOPV` |
| **Reached as** | `C1.C` |
| **Declaration** | `Capacitor.mo:4` |
| **Parameter** | `C` |
| **Claim** | the declaration explicitly permits zero (`min=0`) |
| **Kind** | `physical-bound-permits-zero` |
| **Severity** | low |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0005](../../site-reports/SITE-0005-c-physical-bound-permits-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | electrical |
| `rule` | elec.capacitance.positive |
| `rule_origin` | stored energy is C*v^2/2, which a negative capacitance makes negative; C = 0 removes the state |
| `rule_reference` | MSL Electrical.Analog.Basic.Capacitor |
| `required` | C1.C > 0 |
| `declared_min` | 0.0 |
| `variable_role` | parameter |
| `note` | the declaration explicitly permits zero (`min=0`); whether zero is actually admissible needs execution, and for Mass/Inertia it is not |
| `matched_by` | {'quantity': 'Capacitance', 'unit': 'F', 'semantic_role': 'component.passive.capacitance', 'binding_source': 'component_type', 'confidence': 'QUANTITY_AND_UNIT', 'declaring_class': 'Modelica.Electrical.Analog.Basic.Capacitor', 'member': 'C'} |

## What this is

One occurrence. The declaration at `Capacitor.mo:4` is reached by this model through
`C1.C`, and the analysis reached it statically — no value has been observed
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
