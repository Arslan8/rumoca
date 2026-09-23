# FINDING-02207: `smeeData.xd` in `SMEE_DOL`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL` |
| **Reached as** | `smeeData.xd` |
| **Declaration** | `SynchronousMachineData.mo:25` |
| **Parameter** | `xd` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0258](../../site-reports/SITE-0258-xd-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | smeeData.xd |
| `shape` | propagated |
| `path` | smeeData.xd -> smeeData.xmd -> smeeData.Lmd -> smee.Lmd |
| `declared_min` | None |
| `divisor_sites` | 14 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `SynchronousMachineData.mo:25` is reached by this model through
`smeeData.xd`, and the analysis reached it statically — no value has been observed
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
