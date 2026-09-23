# FINDING-01629: `aimcData.fsNominal` in `IMC_DOL`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL` |
| **Reached as** | `aimcData.fsNominal` |
| **Declaration** | `InductionMachineData.mo:9` |
| **Parameter** | `fsNominal` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0021](../../site-reports/SITE-0021-fsnominal-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | aimcData.fsNominal |
| `shape` | propagated |
| `path` | aimcData.fsNominal -> aimc.fsNominal |
| `declared_min` | None |
| `divisor_sites` | 9 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `InductionMachineData.mo:9` is reached by this model through
`aimcData.fsNominal`, and the analysis reached it statically — no value has been observed
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
