# FINDING-01092: `superCap.Qnom` in `SuperCapDischargeCharge`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Batteries.Examples.SuperCapDischargeCharge` |
| **Reached as** | `superCap.Qnom` |
| **Declaration** | `SuperCap.mo:8` |
| **Parameter** | `Qnom` |
| **Claim** | nothing bounds this declaration at all |
| **Kind** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0808](../../site-reports/SITE-0808-qnom-physical-domain-unenforced.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | battery |
| `rule` | battery.capacity.positive |
| `rule_origin` | capacity is the divisor that normalises charge into SOC |
| `rule_reference` |  |
| `required` | superCap.Qnom > 0 |
| `declared_min` | None |
| `variable_role` | parameter |
| `note` | nothing bounds this declaration, so it permits values physics forbids |
| `matched_by` | {'quantity': 'ElectricCharge', 'unit': 'C', 'confidence': 'QUANTITY_AND_UNIT'} |

## What this is

One occurrence. The declaration at `SuperCap.mo:8` is reached by this model through
`superCap.Qnom`, and the analysis reached it statically — no value has been observed
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
