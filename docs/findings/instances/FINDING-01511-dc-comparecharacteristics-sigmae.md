# FINDING-01511: `dceeData.sigmae` in `DC_CompareCharacteristics`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.DCMachines.DC_CompareCharacteristics` |
| **Reached as** | `dceeData.sigmae` |
| **Declaration** | `DcElectricalExcitedData.mo:18` |
| **Parameter** | `sigmae` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0235](../../site-reports/SITE-0235-sigmae-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | dceeData.sigmae |
| `shape` | propagated |
| `path` | dceeData.sigmae -> dcee.sigmae -> dcee.Lme -> dcee.psi_eNominal |
| `declared_min` | 0.0 |
| `divisor_sites` | 2 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `DcElectricalExcitedData.mo:18` is reached by this model through
`dceeData.sigmae`, and the analysis reached it statically — no value has been observed
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
