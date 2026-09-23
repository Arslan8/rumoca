# FINDING-02577: `rotorDisplacementAngle.m` in `SMPM_VoltageSource`

| | |
|---|---|
| **Model** | `Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource` |
| **Reached as** | `rotorDisplacementAngle.m` |
| **Declaration** | `RotorDisplacementAngle.mo:3` |
| **Parameter** | `m` |
| **Claim** | a settable parameter reaches a denominator, nothing excludes zero |
| **Kind** | `divisor-reachable-zero` |
| **Severity** | medium |
| **Sanitizer** | `divisor` |
| **Fix site** | [SITE-0094](../../site-reports/SITE-0094-m-divisor-reachable-zero.md) |
| **Status** | **candidate — not execution-confirmed** |

## Evidence

| key | value |
|---|---|
| `parameter` | rotorDisplacementAngle.m |
| `shape` | propagated |
| `path` | rotorDisplacementAngle.m -> rotorDisplacementAngle.ToSpacePhasorVS.m |
| `declared_min` | None |
| `divisor_sites` | 2 |
| `note` | reaches a denominator and nothing excludes zero |


## What this is

One occurrence. The declaration at `RotorDisplacementAngle.mo:3` is reached by this model through
`rotorDisplacementAngle.m`, and the analysis reached it statically — no value has been observed
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
