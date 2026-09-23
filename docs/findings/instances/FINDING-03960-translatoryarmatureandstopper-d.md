# FINDING-03960: `d` in `TranslatoryArmatureAndStopper`

| | |
|---|---|
| **Model** | `Modelica.Magnetic.FluxTubes.Examples.Utilities.TranslatoryArmatureAndStopper` |
| **Reached as** | `d` |
| **Declaration** | `TranslatoryArmatureAndStopper.mo:11` |
| **Parameter** | `d` |
| **Claim** | nothing bounds this declaration at all |
| **Kind** | `physical-domain-unenforced` |
| **Severity** | medium |
| **Sanitizer** | `physical` |
| **Fix site** | [SITE-0122](../../site-reports/SITE-0122-d-physical-domain-unenforced.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `domain` | mechanical |
| `rule` | mech.damping.non_negative |
| `rule_origin` | a damper dissipates; d < 0 injects energy. Zero is a legitimate frictionless idealisation, so the bound is >= |
| `rule_reference` |  |
| `required` | d >= 0 |
| `declared_min` | None |
| `variable_role` | parameter |
| `note` | nothing bounds this declaration, so it permits values physics forbids |
| `matched_by` | {'quantity': 'TranslationalDampingConstant', 'unit': 'N.s/m', 'confidence': 'QUANTITY'} |

## What this is

One occurrence. The declaration at `TranslatoryArmatureAndStopper.mo:11` is reached by this model through
`d`, and the analysis reached it statically — no value has been observed
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
