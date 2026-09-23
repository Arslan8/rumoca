# FINDING-04516: `mass3a.m` in `GenerationOfFMUs`

| | |
|---|---|
| **Model** | `Modelica.Mechanics.Translational.Examples.GenerationOfFMUs` |
| **Reached as** | `mass3a.m` |
| **Declaration** | `Mass.mo:3` |
| **Parameter** | `m` |
| **Claim** | the declaration explicitly permits zero (`min=0`) |
| **Kind** | `physical-bound-permits-zero` |
| **Severity** | low |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0011](../../site-reports/SITE-0011-m-physical-bound-permits-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | mechanical |
| `rule` | mech.mass.positive |
| `rule_origin` | m*a = f determines acceleration only for m > 0; negative mass is not a physical body |
| `rule_reference` | MSL Mechanics.Translational.Components.Mass |
| `required` | mass3a.m > 0 |
| `declared_min` | 0.0 |
| `variable_role` | parameter |
| `note` | the declaration explicitly permits zero (`min=0`); whether zero is actually admissible needs execution, and for Mass/Inertia it is not |
| `matched_by` | {'quantity': 'Mass', 'unit': 'kg', 'semantic_role': 'component.translational.mass', 'binding_source': 'component_type', 'confidence': 'QUANTITY_AND_UNIT', 'declaring_class': 'Modelica.Mechanics.Translational.Components.Mass', 'member': 'm'} |

## What this is

One occurrence. The declaration at `Mass.mo:3` is reached by this model through
`mass3a.m`, and the analysis reached it statically — no value has been observed
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
